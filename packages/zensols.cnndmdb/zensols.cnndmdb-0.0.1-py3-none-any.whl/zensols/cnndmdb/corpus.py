"""Data access objects (DAO) for the CNN/DailyMail news summarization corpus,
which is sourced from a `Tensorflow`_ dataset instance, which in turn uses the
Abi See `GitHub`_ repo.

:link: `Tensorflow <https://www.tensorflow.org/datasets/catalog/cnn_dailymail>`_

:link: `GitHub <https://github.com/abisee/cnn-dailymail>`

"""
__author__ = 'Paul Landes'

from typing import Tuple, Dict, Any
from dataclasses import dataclass, field
from enum import Enum
import sys
from collections import OrderedDict
from io import TextIOBase
import logging
from zensols.persist import Stash
from zensols.config import Dictable
from zensols.db import BeanStash, BeanDbPersister

logger = logging.getLogger(__name__)


class Split(Enum):
    """The split of the news article"""
    train = 'r'
    test = 't'
    validation = 'v'


class Publisher(Enum):
    """The source of the article."""
    cnn = 'c'
    daily_mail = 'd'


@dataclass
class Article(Dictable):
    """Represents an article from the CNN/DailyMail corpus.

    """
    id: int = field()
    """The database unique identifier."""

    corp_id: str = field()
    """The original corpus unique identifier."""

    split: Split = field()
    """The split ."""

    publisher: Publisher = field()
    """The source of the article."""

    text: str = field()
    """The article's (story) text."""

    highlights: Tuple[str, ...] = field(default=None)
    """The highlights, or summarization, of the article."""

    def asflatdict(self, *args, **kwargs) -> Dict[str, Any]:
        dct = super().asflatdict()
        dct['split'] = self.split.name
        dct['publisher'] = self.publisher.name.replace('_', ' ')
        return dct

    def write(self, depth: int = 0, writer: TextIOBase = sys.stdout):
        dct = self.asflatdict()
        article = dct['text']
        dct = OrderedDict(
            map(lambda k: (k, dct[k]),
                'id corp_id split publisher highlights'.split()))
        self._write_dict(dct, depth, writer)
        self._write_line('article:', depth, writer)
        self._write_wrap(article, depth + 1, writer)


@dataclass
class _CorpusStash(BeanStash):
    """A stash for accessing and mapping the corpus as :class:`.Article`
    instances.

    """
    persister: BeanDbPersister = field()
    """The DB access object."""

    def load(self, name: str) -> Article:
        art: Article = self.persister.execute_singleton_by_name(
            'select_article_by_id', params=(name,), row_factory=Article)
        highlight_lines: Tuple[str, ...] = self.persister.execute_by_name(
            'select_highlight_by_id',
            params=(name,),
            map_fn=lambda t: t[0])
        art.split = Split(art.split)
        art.publisher = Publisher(art.publisher)
        art.highlights = highlight_lines
        return art


@dataclass
class Corpus(object):
    """Contains access to the CNN/DailyMail corpus.

    """
    persister: BeanDbPersister = field()
    """The DB access object."""

    stash: Stash = field()
    """A stash for accessing and mapping the corpus as :class:`.Article`
    instances.

    """
    def get_by_corp_id(self, name: str) -> Article:
        """Get an article using the original corpus ID.

        :param name: the long 40 character unique identifier from the original
                     corpus.

        """
        rowid: Tuple[int] = self.persister.execute_singleton_by_name(
            'select_id_by_corp_id', params=(name,))
        if rowid is None:
            raise KeyError(name)
        return self.stash[rowid[0]]

    def get_kth_shortest(self, k: int) -> Article:
        rowids: Tuple[int] = self.persister.execute_by_name(
            'select_article_shortest_ids',
            params=(k + 1,),
            map_fn=lambda r: r[0])
        return self.stash[rowids[-1]]
