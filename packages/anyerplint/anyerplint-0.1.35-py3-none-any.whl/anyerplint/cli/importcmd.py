import argparse

from anyerplint import business_logic


def handle_import(args: argparse.Namespace) -> None:
    """Implement argument handling here.

    Don't put business logic here. Only parse the arguments and pass forward.
    """
    business_logic.do_import(args.target)


def init_parser(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
    """Declare arguments you need here."""
    parser.add_argument("target", nargs="+", help="Zip file to import definitions from")

    parser.set_defaults(func=handle_import)
    return parser
