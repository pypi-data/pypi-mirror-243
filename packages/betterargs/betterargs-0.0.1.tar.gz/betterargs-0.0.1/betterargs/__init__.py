"""Main models"""


# Builtin imports
from argparse import ArgumentParser, _SubParsersAction
from typing import Any


def get_sub_dicts(dict_: dict):
    """Split a dictionary into sub dictionary"""
    dicts_ = []
    for key, value in dict_.items():
        dicts_ += [{key: value}]
    return dicts_


class __Component:
    """Represents node in argument tree"""

    def __init__(self, tree: dict[str, Any], depth: str) -> None:
        self.name = list(tree.keys())[0]

        component_map = {
            "root": {
                "children": ["args", "subparsers"],
                "configs": [],
                "defaults": {},
                "name": {"prog": self.name},
            },
            "subparsers": {
                "children": ["args", "parsers"],
                "configs": [],
                "defaults": {},
                "name": {"title": self.name},
            },
            "parsers": {
                "children": ["args"],
                "configs": [],
                "defaults": {},
                "name": {"name": self.name},
            },
            "args": {
                "children": [],
                "configs": ["atype"],
                "defaults": {
                    "atype": "flag",
                    "default": "",
                    # "nargs": "?",
                    # "required": False,
                    # "type": str,
                },
                "name": {},
            },
        }

        assert len(list(tree.keys())) == 1, "Component can have only one key"

        children = component_map[depth]["children"]
        configs = component_map[depth]["configs"]
        defaults = component_map[depth]["defaults"]

        self.names = component_map[depth]["name"]
        self.params = {}

        component_attributes = defaults
        component_attributes.update(tree[self.name])

        for key, value in component_attributes.items():
            if key in configs:
                self.__setattr__(key, value)
            elif key in children:
                children_components = []
                for child in get_sub_dicts(value):
                    children_components += [__Component(child, key)]
                self.__setattr__(key, children_components)
            else:
                self.params[key] = value


class __RootTreeConverter(ArgumentParser):
    """Load command tree to argument parser"""

    def __init__(self, tree: dict[str, Any]) -> None:
        self.__make_root(__Component(tree, "root"))
        self.vals = self.root_parser.parse_args().__dict__

    def __make_root(self, root_component: "__Component") -> None:
        """Create root parser"""
        self.root_parser = ArgumentParser(
            **root_component.names, **root_component.params
        )

        for subparser_component in root_component.subparsers:
            self.__make_subparser(subparser_component, self.root_parser)
        for arg_component in root_component.args:
            self.__make_arg(arg_component, self.root_parser)

    def __make_subparser(
        self, subparser_component: "__Component", parent: ArgumentParser
    ) -> None:
        """Create sub parser"""
        subparser = parent.add_subparsers(
            **subparser_component.names,
            **subparser_component.params,
        )
        for parser_component in subparser_component.parsers:
            self.__make_parser(parser_component, subparser)

    def __make_parser(
        self, parser_component: "__Component", parent: _SubParsersAction
    ) -> None:
        """Create parser"""
        parser = parent.add_parser(**parser_component.names, **parser_component.params)
        for arg_component in parser_component.args:
            self.__make_arg(arg_component, parser)

    def __make_arg(self, arg_component: "__Component", parent: ArgumentParser) -> None:
        """Create argument"""
        name = []
        if arg_component.atype == "positional":
            name += [arg_component.name]
        elif arg_component.atype == "flag":
            name += [
                f"-{''.join([letter[0] for letter in arg_component.name.split('-')])}",
                f"--{arg_component.name}",
            ]

        parent.add_argument(*name, **arg_component.params)


def create_argument_parser(tree: dict[str, Any]) -> dict[str, Any]:
    """Create command line arguments"""
    return __RootTreeConverter(tree).vals


def load_to_globals(globals_dict: dict[str, Any], tree: dict[str, Any]) -> None:
    """Add parsed arguments to current global variable namespace"""
    globals_dict.update(create_argument_parser(tree))
