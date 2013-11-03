from collections import Counter, deque
from functools import wraps

from .swda import CorpusReader
from .io import write_cooccurrence_matrix


def tokens(utterances, n=1):
    for utterance in utterances:
        ngram = deque([], n)
        for w, _ in utterance.pos_lemmas():
            ngram.append(w)
            yield utterance.act_tag, '_'.join(ngram)


def ContextBefore(utterances, context_len=3, ngram_len=1):
    context = deque([], context_len)

    for utterance in utterances:
        context.append(utterance)

        for token in tokens(context, ngram_len):
            yield token


def WordUtterance(utterances, ngram_len):
    for document_id, utterance in enumerate(utterances):
        for word, _ in utterance.pos_lemmas():
            yield word, document_id


def writer(command, extra_options=tuple()):
    def wrapper(f):
        options = extra_options + (
            ('n', 'ngram_len', 1, 'Length of the tokens (bigrams, ngrams).'),
        )

        @command(options=options)
        @wraps(f)
        def wrapped(
            path,
            output='out.h5',
            **context
        ):
            corpus = CorpusReader(path)
            utterances = corpus.iter_utterances(display_progress=False)

            counter = Counter(f(utterances, **context))

            return write_cooccurrence_matrix(counter, output)

        return wrapped

    return wrapper
