"""Hybrid retrieval: reciprocal rank fusion (RRF) of bm25 and dense.

A port of rrf() in the 13 lab's pipeline.py: each document scores the sum of 1 / (k + rank) over
the rankings it appears in, rank counted from 1. The lab's k is 60; here it is 10, chosen on the
shared practice queries, where bm25 and dense find different sections and k = 60 buried a section
one of them ranked first (MRR@10 0.471 at 60, 0.587 at 10). The fusion runs over full rankings (every document
of the corpus), not top-10 lists, because a document that is 11th in both can belong in the fused
top 10. search_chunks does the same fusion over chunk rankings, so `p2 answer` and the reranker can
use hybrid's chunks.

The two systems and the RRF constant can be changed in p2.toml:

    [hybrid]
    systems = ["bm25", "dense"]
    rrf_k = 10
"""

from __future__ import annotations

from p2.retrievers import build as build_system
from p2.runfile import order

NEEDS_CLAUDE = False


def rrf(rankings: list[list[tuple[str, float]]], k: int) -> list[tuple[str, float]]:
    """Fuse rankings of (id, score) pairs, best first, into one ranking by RRF."""
    scores: dict[str, float] = {}
    for ranking in rankings:
        for rank, (item, _) in enumerate(ranking, start=1):
            scores[item] = scores.get(item, 0.0) + 1 / (k + rank)
    return order(scores.items())


class Hybrid:
    def __init__(self, corpus, cfg):
        settings = cfg.table("hybrid")
        self.corpus = corpus
        self.rrf_k = int(settings.get("rrf_k", 10))
        self.systems = [build_system(name, corpus, cfg) for name in settings.get("systems", ["bm25", "dense"])]
        self.n_chunks = len(corpus.chunks(cfg.chunk_words, cfg.chunk_overlap))

    def search(self, text: str, k: int) -> list[tuple[str, float]]:
        n = len(self.corpus.docs)
        return rrf([s.search(text, n) for s in self.systems], self.rrf_k)[:k]

    def search_chunks(self, text: str, k: int) -> list[tuple[str, float]]:
        return rrf([s.search_chunks(text, self.n_chunks) for s in self.systems], self.rrf_k)[:k]


def build(corpus, cfg):
    return Hybrid(corpus, cfg)
