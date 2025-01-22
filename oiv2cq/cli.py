import argparse
from .prereqs import main as prereqs_main
from .template_create import main as template_create_main

def main():
    parser = argparse.ArgumentParser(description="oiv2cq CLI")
    subparsers = parser.add_subparsers(dest="command")

    # Prereqs command
    prereqs_parser = subparsers.add_parser("setup", help="Run prerequisite setup")
    prereqs_parser.set_defaults(func=prereqs_main)

    # Template command
    template_parser = subparsers.add_parser("template", help="Clone the cloudquery-plugins repo and generate a local CloudQuery plugin template for development.")
    template_parser.set_defaults(func=template_create_main)

    args = parser.parse_args()
    if args.command:
        args.func()
    else:
        parser.print_help()
