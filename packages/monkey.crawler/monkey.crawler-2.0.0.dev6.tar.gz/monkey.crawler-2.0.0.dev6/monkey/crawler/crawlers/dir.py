# -*- coding: utf-8 -*-
import os

from monkey.crawler.crawler import Crawler


class DirEntryWrapper:

    def __init__(self, dir_entry: os.DirEntry):
        self._dir_entry: os.DirEntry = dir_entry

    def name(self):
        return self._dir_entry.name

    def path(self):
        return self._dir_entry.path

    def as_dict(self) -> dict:
        d = {'name': self.name(), 'path': self.path()}
        return d


class DirectoryCrawler(Crawler):

    def __init__(self, source_name: str, path: str, recurse: bool = True):
        super().__init__(source_name)
        self.path = path
        self.recurse = recurse

    def _get_records(self, offset: int = 0):
        """Returns an iterator on files"""
        self._entries = os.scandir(self.path)
        return self

    def _get_start_message(self):
        return f'Crawling {self.path} directory.'

    def __iter__(self):
        return self

    def __next__(self):
        try:
            return DirEntryWrapper(self._entries.__next__())
        except StopIteration as e:
            raise e
