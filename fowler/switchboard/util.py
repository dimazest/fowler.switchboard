from collections import Counter, deque
from functools import wraps

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
        words = utterance.pos_words()
        # TODO: it would be nice to treat utterances that don't
        # contain any word differently.
        if not words:
            yield '<NON_VERBAL>', document_id
        for word in words:
            yield word, document_id


def writer(
    command,
    extra_options=tuple(),
):
    def wrapper(f):
        options = extra_options + (
            ('n', 'ngram_len', 1, 'Length of the tokens (bigrams, ngrams).'),
            ('o', 'output', 'out.h5', 'The output file.'),
        )

        @command(options=options)
        @wraps(f)
        def wrapped(
            utterances_iter,
            output,
            corpus,
            **context
        ):
            counter = Counter(f(utterances_iter(), **context))
            return write_cooccurrence_matrix(counter, output, utterances_iter())

        return wrapped

    return wrapper
