#!/usr/bin/env python3

from sys import argv as sysargv, stdin, stderr
from pathlib import Path
from json import load as jsonload

from . import deconstruct


def main():
    invocation_map = {
        'jsonmason-nodedump': lambda n: n,
        'jsonmason-jsdump': lambda n: n.assignment
    }
    invocation = Path(sysargv[0]).name
    try:
        stringgetter = invocation_map[invocation]
        try:
            for n in deconstruct(jsonload(stdin)):
                print(stringgetter(n), flush=True)
        except (BrokenPipeError, KeyboardInterrupt):
            stderr.close()
    except (KeyError, TypeError):
        exit(f'Unexpected invocation: "{invocation}"')


if __name__ == "__main__":
    main()
