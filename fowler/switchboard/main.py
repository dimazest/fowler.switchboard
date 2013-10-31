from collections import Counter, deque

from opster import command
from opster import dispatch  # noqa

from .swda import CorpusReader


@command()
def transcripts(path):
    """Print all the transcripts in a human readable way."""
    corpus = CorpusReader(path)

    for transcript in corpus.iter_transcripts(display_progress=False):
        for utterance in transcript.utterances:
            print('{u.caller} {u.act_tag}: {u.text}'.format(u=utterance))

        print()


@command()
def tags(path):
    """Count tag frequencies in the corpora."""
    corpus = CorpusReader(path)

    utterences = corpus.iter_utterances(display_progress=False)
    counter = Counter(u.act_tag for u in utterences)

    for tag, freq in counter.most_common():
        print(freq, tag)


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
        for word in utterance.text_words(filter_disfluency=True):
            yield word, document_id


@command()
def cooccurrence(
    path,
    mode=('m', 'inner', 'Mode. innger, before, word-document'),
    context_len=('c', 3, 'Length of the context in "before mode."'),
    ngram_len=('n', 1, 'Length of the tokens (bigrams, ngrams).')
):
    """Build the co-occurrence matrix.

    Each line in the output file consists of 3 elements separated by space::

        `element1` `element2` `count`

    The modes are:

        * "inner"

        * "before"

        * "word-document" counts co-occurrence of a word and a dialog act. In
          the output file `element1` is a word, `element2` is the utterance
          id. Utterance id does not have any meaning and only identifies
          utterances uniquely.

    """
    corpus = CorpusReader(path)

    utterances = corpus.iter_utterances(display_progress=False)

    if mode == 'inner':
        pairs = tokens(utterances, n=ngram_len)
    elif mode == 'before':
        pairs = ContextBefore(utterances, 3, ngram_len=ngram_len)
    elif mode == 'word-document':
        pairs = WordUtterance(utterances, ngram_len=ngram_len)
    else:
        raise NotImplementedError('The mode is not implemented.')

    counter = Counter(pairs)

    for (tag, lemma), count in counter.items():
        print('{} {} {}'.format(tag, lemma, count))
