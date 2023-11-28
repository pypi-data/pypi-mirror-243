# JsonMason

## What

A utility/library for transforming an object into an editable stream, and reconstructing an object from that stream.
To be precise:

- Transform an an object of acyclic nested collections into an iterable of assignment operations (deconstruction)
- Create an object of acyclic nested collections from an iterable of assignment operations (reconstruction)

## Why

Deconstructing only to reconstruct does not seem very useful in itself. The power is in operating on the intermediary format — the iterable of nodes
lends itself well to pattern matching, transformations, and other forms of computation.

## How

### In the shell

If you've installed this package (eg `pipx install jsonmason`), then you should have two executables on your `$PATH`. Both accept JSON on standard input, and print the deconstruction of that JSON on standard output.

* `jsonmason-nodedump` makes it easy to `grep` for patterns - this is a bit like [`gron`](https://github.com/tomnomnom/gron), but is intended to make it easy to find patterns for creating transformations in your Python code.
* `jsonmason-jsdump` is even more like , as it prints JS-style assignments that can be pasted straight into a JS console.

### In Python code


The basics:
```
from jsonmason import deconstruct, reconstruct
```

In addition there is a module `attrdict` which makes it possible to address dicts by "dot-attribute-paths" (as in JS).
```
from jsonmason import AttrDict
```

For examples, have a look at the module docstrings:

* [libjsonmason](https://github.com/blinkingtwelve/jsonmason/blob/master/doc/libjsonmason.rst)
* [attrdict](https://github.com/blinkingtwelve/jsonmason/blob/master/doc/attrdict.rst)

## Testing

Run `test.py`.