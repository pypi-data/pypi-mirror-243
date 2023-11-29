"""Creates a SQLite database if the CNN and DailyMail summarization dataset.

"""
__author__ = 'Paul Landes'

from dataclasses import dataclass, field
from enum import Enum, auto
import logging
from pathlib import Path
import itertools as it
from zensols.util import stdout
from zensols.config import ConfigFactory
from zensols.cli import ApplicationError
from . import Article, Corpus

logger = logging.getLogger(__name__)


class _KeyType(Enum):
    db = auto()
    org = auto()
    short = auto()


class _Format(Enum):
    text = auto()
    json = auto()
    yaml = auto()

    @property
    def ext(self) -> str:
        ext: str = {
            self.text: 'txt',
        }.get(self)
        return self.name if ext is None else ext


@dataclass
class Application(object):
    """Creates a SQLite database if the CNN and DailyMail summarization dataset.

    """
    config_factory: ConfigFactory = field()
    """Used to create objects for :meth:`load`."""

    corpus: Corpus = field()
    """The corpus which contains a stash that creates instances of :`.Article`.

    """
    def load(self):
        """Load the SQLite database with the CNN/DailyMail corpus."""
        from .load import DatabaseLoader
        loader: DatabaseLoader = self.config_factory('cnndmdb_loader')
        loader.load()

    def write_keys(self, limit: int = 1):
        """Print the keys of the corpus.

        :param limit: the max number of keys to write

        """
        print('\n'.join(it.islice(self.corpus.stash.keys(), limit)))

    def write_article(self, key: str, key_type: _KeyType = _KeyType.org,
                      format: _Format = _Format.text,
                      output_file: Path = Path('-')) -> Article:
        """Write an article.

        :param key: the key to the article

        :param key_type: ``db`` for numeric, database, ``org`` for corpus
                         original, ``short`` for Kth shortest article

        :param format: the output format

        """
        try:
            art: Article = {
                _KeyType.db: lambda k: self.corpus.stash[k],
                _KeyType.org: self.corpus.get_by_corp_id,
                _KeyType.short: lambda k: self.corpus.get_kth_shortest(int(k)),
            }[key_type](key)
        except KeyError:
            raise ApplicationError(f'No such key exists: {key}')
        with stdout(output_file, recommend_name=key,
                    extension=format.ext, logger=logger) as f:
            {_Format.text: lambda: art.write(writer=f),
             _Format.json: lambda: art.asjson(writer=f, indent=4),
             _Format.yaml: lambda: art.asyaml(writer=f, indent=4),
             }[format]()
        return art


@dataclass
class PrototypeApplication(object):
    CLI_META = {'is_usage_visible': False}

    app: Application = field()

    def proto(self):
        """Prototype test."""
        self.app.write_article(205334, _KeyType.db)
