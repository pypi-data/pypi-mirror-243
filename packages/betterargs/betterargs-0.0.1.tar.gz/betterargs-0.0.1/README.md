# betterargs

A tool to create a command-line interface for your app using python

## Installation

**Requirements**

- yaml (`pip install`)
- argparse

```bash
git clone github.com/danielmuringe/betterargs
```

## Usage

- Import the package into python file
```python
import betterargs
```

- Define argument tree using YAML format
```python
yaml_tree = """
git:
    args:
        path:
            atype: flag
            help: Path of the repo
    subparsers:
        parsers:
            clone:
                args:
                    quiet-clone:
                        atype: flag
                        help: Operate quietly. Progress is not reported to the standard error stream.
                    no-checkout:
                        help: No checkout of HEAD is performed after the clone is complete
            init:
                args:
                    quiet-init:
                        atype: flag
                        help: Operate quietly. Progress is not reported to the standard error stream.
"""
```

- Convert YAML to command line argument parser
```python
betterargs.create_arguments(yaml_tree)
```
