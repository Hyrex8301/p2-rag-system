"""Dense retrieval: embed every chunk once, embed the query, and rank chunks by cosine similarity.

A port of the embedding arm of the 12 lab's retrieve.py (dense_rankings): the chunk vectors are
computed once and cached by p2.embed.doc_vectors, every vector has length 1, so one matrix product
with the query vector gives the cosine similarity of every chunk. ChunkScorer lifts the chunk scores
to documents (a document scores its best chunk) and gives search_chunks for `p2 answer`.

The embedder is bge-small-en-v1.5 unless p2.toml has a [dense] table naming another model:

    [dense]
    model = "minishlab/potion-retrieval-32M"
"""

from __future__ import annotations

import numpy as np

from p2 import embed
from p2.retrievers import ChunkScorer

NEEDS_CLAUDE = False


class Dense(ChunkScorer):
    def __init__(self, corpus, cfg):
        super().__init__(corpus, cfg)
        self.model = cfg.table("dense").get("model", embed.BGE)
        self.embedder = embed.load(self.model)
        self.vectors = embed.doc_vectors(self.embedder, [c.text for c in self.chunks], cfg.root)

    def score_chunks(self, text: str) -> np.ndarray:
        if not self.chunks:
            return np.zeros(0, dtype=np.float32)
        query = self.embedder.encode([text])[0]
        return self.vectors @ query


def build(corpus, cfg):
    return Dense(corpus, cfg)
