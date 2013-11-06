import inspect
from itertools import islice

import opster

from .swda import CorpusReader


class Dispatcher(opster.Dispatcher):
    def __init__(self, *globaloptions):
        globaloptions = (
            tuple(globaloptions) +
            (
                ('v', 'verbose', False, 'Be verbose.'),
                ('l', 'limit', 0, 'Limit the number of utterances by this value.'),
                ('p', 'path', './swda', 'The path to the swda dir.'),
            )
        )

        super(Dispatcher, self).__init__(
            globaloptions=globaloptions,
            middleware=_middleware,
        )


def _middleware(func):
    def wrapper(*args, **kwargs):
        if func.__name__ == 'help_inner':
            return func(*args, **kwargs)

        f_args = inspect.getargspec(func)[0]

        verbose = kwargs.pop('verbose')
        limit = kwargs.pop('limit')
        path = kwargs.pop('path')

        corpus = CorpusReader(path)
        utterances = corpus.iter_utterances(display_progress=False)
        if limit:
            utterances = islice(utterances, limit)

        if 'utterances' in f_args:
            kwargs['utterances'] = utterances

        return func(*args, **kwargs)

    return wrapper
