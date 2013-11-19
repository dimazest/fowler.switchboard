from collections import Counter

from .util import WordUtterance, writer
from .options import Dispatcher


dispatcher = Dispatcher()
command = dispatcher.command
dispatch = dispatcher.dispatch


@command()
def transcripts(
    utterances,
    format=('f', '{u.caller} {damsl_act_tag}: {u.text}', 'Format.'),
):
    """Print all the transcripts in a human readable way."""
    caller = None
    for utterance in utterances:
        if caller != utterance.caller:
            if caller is not None:
                print()
            caller = utterance.caller

        print(format.format(
            u=utterance,
            damsl_act_tag=utterance.damsl_act_tag(),
        ))


@command()
def tags(
    utterances,
    damsl=('d', False, 'Use the DAMSL tags.')
):
    """Count tag frequencies in the corpora."""
    if not damsl:
        counter = Counter(u.act_tag for u in utterances)
    else:
        counter = Counter(u.damsl_act_tag() for u in utterances)

    for tag, freq in counter.most_common():
        print(freq, tag)


@writer(command)
def word_document(utterances, ngram_len, verbose):
    """Word document."""
    return WordUtterance(utterances, ngram_len=ngram_len, verbose=verbose)
