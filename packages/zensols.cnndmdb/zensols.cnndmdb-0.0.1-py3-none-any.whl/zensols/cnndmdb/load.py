"""Classes to populate the database.  For data sources see :mod:`zensols.stash`.

"""
__author__ = 'Paul Landes'

from typing import Dict, Tuple, List, Iterable
from dataclasses import dataclass, field
import logging
import itertools as it
from itertools import chain
import pandas as pd
from pathlib import Path
from tensorflow.data import Dataset
import tensorflow_datasets as tfds
from zensols.util import time
from zensols.db import BeanDbPersister

logger = logging.getLogger(__name__)


@dataclass
class DatabaseLoader(object):
    """Loads the CNN/DailyMail into a new SQLite database file.  If the file
    already exists, it is deleted.  This takes about 2 to load.

    """
    persister: BeanDbPersister = field()
    """The DB access object."""

    chunk_size: int = field()
    """Number of rows to insert into SQLite at a time."""

    dataset_name: str = field(default='cnn_dailymail')
    """The name of the dataset to load from."""

    split_spec: Dict[str, str] = field(default=None)
    """Used to create the split format for loading the dataset."""

    @property
    def db_file(self) -> Path:
        """The SQLite file."""
        return self.persister.conn_manager.db_file

    def _get_dataset(self) -> Dict[str, Dataset]:
        if self.split_spec is None:
            return tfds.load(self.dataset_name)
        else:
            spec_items: Tuple[str, str] = tuple(self.split_spec.items())
            spec_names: Iterable[str] = map(lambda t: t[0], spec_items)
            spec: Tuple[str] = tuple(map(lambda t: t[1], spec_items))
            builder = tfds.builder(self.dataset_name)
            splits: List[Dataset] = builder.as_dataset(split=spec)
            return dict(zip(spec_names, splits))

    def _split_col(self, df: pd.DataFrame, col_name: str):
        def iter_rows() -> Iterable[Tuple[str, str]]:
            dfg: pd.DataFrame = df[['id', col_name]]
            for id, col in dfg.itertuples(index=False, name=None):
                yield map(lambda x: (id, *x), zip(it.count(), col.split('\n')))

        return pd.DataFrame(
            chain.from_iterable(iter_rows()),
            columns=['id', 'seq', col_name])

    def _load(self):
        self.persister.conn_manager.drop()
        splits: Dict[str, Dataset] = self._get_dataset()
        for name, split in splits.items():
            df: pd.DataFrame = tfds.as_dataframe(split)
            for col in df.columns:
                df[col] = df[col].str.decode('utf-8')
            df['split'] = {
                'train': 'r',
                'test': 't',
                'validation': 'v',
            }[name]
            self.persister.insert_name = 'insert_article'
            self.persister.insert_dataframe(
                df['id split publisher article'.split()],
                chunk_size=self.chunk_size)
            self.persister.insert_name = 'insert_highlight'
            self.persister.insert_dataframe(
                self._split_col(df, 'highlights'),
                chunk_size=self.chunk_size)
        logger.info(f'wrote: {self.db_file}')

    def load(self):
        """Load the SQLite database with the CNN/DailyMail corpus."""
        logger.info(f'loading database to {self.db_file}')
        with time('loaded database'):
            self._load()
        with time('cleanup (vacuume)'):
            self.persister.execute('vacuum')
