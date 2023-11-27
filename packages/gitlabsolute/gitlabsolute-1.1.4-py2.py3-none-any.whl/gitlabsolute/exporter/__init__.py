import argparse
import os
import sys

from imxdparser import ChildParser

from . import export


def main(main_parser, _parser_error):
    exporter = ChildParser(main_parser, "exporter")
    exporter.attach()

    export.main(project_badge)
