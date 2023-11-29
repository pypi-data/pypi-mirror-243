"""Command line entry point to the application.

"""
__author__ = 'Paul Landes'

from typing import List, Any, Dict
import sys
from zensols.config import ConfigFactory
from zensols.cli import ActionResult, CliHarness
from zensols.cli import ApplicationFactory as CliApplicationFactory
from . import Corpus


class ApplicationFactory(CliApplicationFactory):
    def __init__(self, *args, **kwargs):
        kwargs['package_resource'] = 'zensols.cnndmdb'
        super().__init__(*args, **kwargs)

    @classmethod
    def get_corpus(cls) -> Corpus:
        """Return the section predictor using the app context."""
        harness: CliHarness = cls.create_harness()
        fac: ConfigFactory = harness.get_config_factory()
        return fac('cnndmdb_corpus')


def main(args: List[str] = sys.argv, **kwargs: Dict[str, Any]) -> ActionResult:
    harness: CliHarness = ApplicationFactory.create_harness(relocate=False)
    harness.invoke(args, **kwargs)
