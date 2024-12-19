import os

from loguru import logger
from jsonpath_rw import parse

from favorites_crawler.constants.path import DEFAULT_FAVORS_HOME


def get_favors_home():
    return os.path.expanduser(os.getenv('FAVORS_HOME', DEFAULT_FAVORS_HOME))


class DictRouter:
    def __init__(self, dict_):
        self.dict_ = dict_

    def route_to(self, path, default=None):
        """return target value by path.
        :param path: qualified name of target. e.g. a.0.c
        :param default: return when target not exists.
        :return: target value of path.
        """
        value = self.dict_
        for key in path.split('.'):
            if key.isdigit():
                key = int(key)
            try:
                value = value[key]
            except Exception as e:
                logger.error('Failed to get {} from {!r}. Reason: {!r}', path, self.dict_, e)
                return default
        return value

    def find(self, jsonpath_expr):
        expr = parse(jsonpath_expr)
        return [match.value for match in expr.find(self.dict_)]
