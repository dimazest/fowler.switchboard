from collections import Counter

from .util import (
    tokens,
    ContextBefore,
    WordUtterance,
    writer,
)
from .options import Dispatcher


dispatcher = Dispatcher()
command = dispatcher.command
dispatch = dispatcher.dispatch


@command()
def transcripts(
    utterances,
    format=('f', '{u.caller} {u.act_tag}: {u.text}', 'Format.'),
):
    """Print all the transcripts in a human readable way."""
    caller = None
    for utterance in utterances:
        if caller != utterance.caller:
            if caller is not None:
                print()
            caller = utterance.caller

        print(format.format(u=utterance))


@command()
def tags(utterances):
    """Count tag frequencies in the corpora."""
    counter = Counter(u.act_tag for u in utterances)

    for tag, freq in counter.most_common():
        print(freq, tag)


@writer(command)
def word_document(utterances, ngram_len):
    """Word document."""
    return WordUtterance(utterances, ngram_len=ngram_len)


@writer(command)
def inner(utterances, ngram_len):
    return tokens(utterances, n=ngram_len)


@writer(
    command,
    extra_options=(
        ('c', 'context-len', 3, 'Length of the context in "before mode.'),
    )
)
def before(utterances, ngram_len, context_len):
    return ContextBefore(utterances, context_len, ngram_len=ngram_len)


