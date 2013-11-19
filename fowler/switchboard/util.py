import sys
from itertools import chain
from collections import Counter, deque
from functools import wraps

from .io import write_cooccurrence_matrix


def utterance_ngrams(utterance, ngram_len=1):
    ngram = deque(['<BEGIN>'], ngram_len)

    words = chain(utterance.pos_words(), ['<END>'])

    for w in words:
        ngram.append(w)

        yield '_'.join(ngram)


def WordUtterance(utterances, ngram_len, verbose=False):
    for document_id, utterance in enumerate(utterances):
        ngrams = utterance_ngrams(utterance, ngram_len=ngram_len)

        if verbose:
            sys.stderr.write(
                'Document id: {document_id}\n'
                'Words: {ngrams}\n'
                '\n'.format(
                    document_id=document_id,
                    ngrams=' '.join(ngrams),
                )
            )

        # TODO: it would be nice to treat utterances that don't
        # contain any word differently.
        if not ngrams:
            yield '<NON_VERBAL>', document_id
        for ngram in ngrams:
            yield ngram, document_id


def writer(
    command,
    extra_options=tuple(),
):
    def wrapper(f):
        options = extra_options + (
            ('n', 'ngram_len', 1, 'Length of the tokens (bigrams, ngrams).'),
            ('o', 'output', 'swda-{limit}items-{ngram_len}gram.h5', 'The output file.'),
            ('v', 'verbose', False, 'Be verbose.'),
        )

        @command(options=options)
        @wraps(f)
        def wrapped(
            utterances_iter,
            output,
            corpus,
            limit,
            **context
        ):
            counter = Counter(f(utterances_iter(), **context))

            output = output.format(
                limit=limit,
                ngram_len=context['ngram_len'],
            )

            return write_cooccurrence_matrix(counter, output, utterances_iter())

        return wrapped

    return wrapper
