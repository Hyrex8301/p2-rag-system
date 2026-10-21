"""Ablation: dense with 100-word chunks instead of 300.

The one change is the chunk size. Everything else is dense as it is: the same embedder
(bge-small-en-v1.5 unless p2.toml's [dense] names another), cosine similarity, and a document
scored by its best chunk. The overlap shrinks in proportion, from 50 words to 20, so neighbouring
chunks still share about a sixth of their words.

Why this change: the own corpus's articles are about five times longer than the shared corpus's
sections (median 340 words against 68), and 58% of them span more than one 300-word chunk (13% on
the shared corpus), so the chunk size has more to do there.
"""

from p2.retrievers.dense import Dense

NEEDS_CLAUDE = False
BASE = "dense"
CHUNK_WORDS = 100
CHUNK_OVERLAP = 20


def build(corpus, cfg):
    return Dense(corpus, cfg.replace(chunk_words=CHUNK_WORDS, chunk_overlap=CHUNK_OVERLAP))
