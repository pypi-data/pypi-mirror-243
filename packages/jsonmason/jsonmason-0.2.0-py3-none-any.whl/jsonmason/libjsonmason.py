"""
libjsonmason: Deconstruct and reconstruct container types.
Any nested container type inheriting from ``Sequence`` or ``Mapping`` is supported for deconstruction.
However, any such sequence or mapping will be squashed to a list or a dict, respectively; those are the only ones supported
in JSON.
Thus deserialized JSON in particular will survive a roundtrip through deconstruction and reconstruction; the resulting structure
will be a semantically identical copy of the original.

The following deconstruction example shows the intermediary format:

>>> my_deserialized_json = [34, {"hello": [["a", "b"], ["c", "d"]], "world": 42}]
>>> node_generator = deconstruct(my_deserialized_json)
>>> next(node_generator)
Node(path=(), value=typing.List, is_leaf=False)
>>> next(node_generator)
Node(path=(typing.List, 0), value=34, is_leaf=True)
>>> next(node_generator)
Node(path=(typing.List, 1), value=typing.Dict, is_leaf=False)
>>> next(node_generator)
Node(path=(typing.List, 1, typing.Dict, 'hello'), value=typing.List, is_leaf=False)

and so on.
A full roundtrip of deserialized JSON results in a semantically identical structure, as promised:

>>> reconstruct(deconstruct(my_deserialized_json))
[34, {'hello': [['a', 'b'], ['c', 'd']], 'world': 42}]

Adding an inline transformation makes things more interesting:

>>> reconstruct(map(lambda node: node.clone(value = node.value * 2) if node.is_leaf else node, deconstruct(my_deserialized_json)))
[68, {'hello': [['aa', 'bb'], ['cc', 'dd']], 'world': 84}]
"""


from functools import reduce, partial
from dataclasses import dataclass, field
from collections.abc import Sequence, Mapping
from typing import Union, List, Dict, Tuple, Any, Iterable
from json import dumps as jsondumps

CONTAINER_MAP = {List: list, Dict: dict}


@dataclass
class Node:
    path: Tuple
    """Full logical path to the node"""
    containerpath: Tuple = field(repr=False, compare=False)
    """References to enveloping containers"""
    value: Any
    """The value at the path"""
    is_leaf: bool
    """Informational: Whether the value is a leaf value"""

    @property
    def itempath(self):
        """
        The path, devoid of container types
        """
        return tuple(filter(lambda el: el not in CONTAINER_MAP, self.path))

    @property
    def assignment(self):
        """
        A string expressing the assignment, JS-style
        """
        def stringulate(thing):
            try:
                return {List: '[]', Dict: '{}'}[thing]
            except KeyError:
                return jsondumps(thing)

        return "json{} = {};".format(
            ''.join(f'[{jsondumps(item)}]' for item in self.itempath),
            stringulate(self.value)
        )

    @property
    def container(self):
        """
        The containing container. Useful for getting sibling items without going through traverse().
        """
        try:
            return self.containerpath[-1]
        except IndexError:
            return  # root node

    def clone(self, **kwargs):
        """
        Return a copy, optionally replacing one or more field values
        """
        me = dict(
            path=self.path,
            containerpath=self.containerpath,
            value=self.value,
            is_leaf=self.is_leaf,
        )
        return Node(**{**me, **kwargs})


def traverse(container, path):
    """
    Return the node at ``path`` in the nested ``container``

    >>> traverse([34, {'hello': [['a', 'b'], ['c', 'd']], 'world': 42}], [0])
    34
    >>> traverse([34, {'hello': [['a', 'b'], ['c', 'd']], 'world': 42}], [1, 'world'])
    42
    >>> traverse([34, {'hello': [['a', 'b'], ['c', 'd']], 'world': 42}], [1, 'hello', 1, 0])
    'c'
    """
    try:
        return reduce(lambda cur_node, pathcomp: cur_node[pathcomp], path, container)
    except (KeyError, IndexError):
        raise ValueError("Invalid path for container")


def assign_at(container, path, value, container_mapping=CONTAINER_MAP):
    """
    Assign ``value`` at ``path`` in ``container``
    """
    *into_container_path, where = path
    assign_to = traverse(container, into_container_path)
    assign_what = container_mapping.get(value, lambda: value)()
    if isinstance(assign_to, List):
        assign_to.append(assign_what)
    elif isinstance(assign_to, Dict):
        assign_to[where] = assign_what
    return container


def _node_gen(path: Tuple, containerpath: Tuple, branch_or_leaf):

    def descend_typetest(entity):
        for choice in (str, List, Dict, Sequence, Mapping):
            if isinstance(entity, choice):
                return choice

    def gen_leaf():
        # Terminate, yield a leaf node
        yield Node(path, containerpath, branch_or_leaf, True)

    def gen_from_container(containerclass: Union[Dict, List]):
        # Descend into container types
        yield Node(path, containerpath, containerclass, not branch_or_leaf)

        def expand(branch_or_leaf):
            if containerclass == List:
                return enumerate(branch_or_leaf)
            if containerclass == Dict:
                return branch_or_leaf.items()

        containerpath_logical = path + (containerclass,)
        containerpath_refs = containerpath + (branch_or_leaf,)
        for subscript, item in expand(branch_or_leaf):
            yield from _node_gen(containerpath_logical + (subscript,), containerpath_refs, item)

    gen_as_list = partial(gen_from_container, List)
    gen_as_dict = partial(gen_from_container, Dict)

    action_map = {
        str: gen_leaf,
        None: gen_leaf,
        List: gen_as_list,
        Dict: gen_as_dict,
        Sequence: gen_as_list,
        Mapping: gen_as_dict,
    }

    yield from action_map[descend_typetest(branch_or_leaf)]()


def deconstruct(thejson: Union[Dict, List]):
    """
    Yields path nodes through nested container types, depth-first, emitting ``Node`` objects.
    """
    yield from _node_gen((), (), thejson)


def reconstruct(nodes: Iterable[Node], container_mapping=CONTAINER_MAP):
    """
    Reconstruct an object from its ``Node`` components (as acquired from deconstruct()).
    """
    try:
        n = next(nodes)
        if n.path:
            raise ValueError("Root node should have empty path.")
        root = container_mapping[n.value]()
    except KeyError:
        raise ValueError("Root node is not a list or dict.")
    except StopIteration:
        return  # no nodes in, no result out.

    for n in nodes:
        assign_at(root, n.itempath, n.value, container_mapping=container_mapping)

    return root
