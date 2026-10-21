"""Hybrid retrieval: a weighted sum of bm25 and dense scores.

A document's fused score is w * bm25 / (the query's best bm25 score) + its dense cosine similarity,
with w = 0.1, over every document. search_chunks does the same over chunks, so `p2 answer` can use
hybrid's chunks.

Why this form, after three that did not work (all measured on the shared practice queries):
- Reciprocal rank fusion (RRF) with the 13 lab's k = 60: MRR@10 0.471, below bm25 and dense. bm25 and
  dense find different sections, and k = 60 rewards a section both rank in the middle over one that
  either ranks first.
- RRF with k = 10: MRR@10 0.587, but CI could not reproduce it. dense's scores differ by about 0.0001
  between macOS and Linux, enough to swap near-tied sections, and with k = 10 one place moves a fused
  score by more than the 0.001 that `p2 check` allows.
- Each system's top-100 scores scaled to 0-1 and averaged: MRR@10 0.581, but the scaling divides
  dense's small spread (about 0.1), which multiplies that noise past 0.001 too.
bm25's scores are exact on every machine, so scaling them is safe; dense's cosine passes through
unscaled, so the fused score moves no more than dense's own score does. With w = 0.1 the practice
MRR@10 is 0.642 (0.547 at w = 0.2, 0.533 at w = 0.3), and noise of 0.0001 broke none of 300 trials.
rrf() stays here because the reranker's first stage uses it, and CI never runs the reranker again.

Settings, all optional, in p2.toml:

    [hybrid]
    bm25_weight = 0.1
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


def weighted_sum(keyword: list[tuple[str, float]], dense: list[tuple[str, float]], weight: float) -> list[tuple[str, float]]:
    """weight * keyword score / the best keyword score + dense score, for every item dense ranks."""
    best = keyword[0][1] if keyword and keyword[0][1] > 0 else 1.0
    scaled = {item: score / best for item, score in keyword}
    return order((item, weight * scaled.get(item, 0.0) + score) for item, score in dense)


class Hybrid:
    def __init__(self, corpus, cfg):
        self.weight = float(cfg.table("hybrid").get("bm25_weight", 0.1))
        self.bm25 = build_system("bm25", corpus, cfg)
        self.dense = build_system("dense", corpus, cfg)
        self.n_docs = len(corpus.docs)
        self.n_chunks = len(corpus.chunks(cfg.chunk_words, cfg.chunk_overlap))

    def search(self, text: str, k: int) -> list[tuple[str, float]]:
        n = self.n_docs
        return weighted_sum(self.bm25.search(text, n), self.dense.search(text, n), self.weight)[:k]

    def search_chunks(self, text: str, k: int) -> list[tuple[str, float]]:
        n = self.n_chunks
        return weighted_sum(self.bm25.search_chunks(text, n), self.dense.search_chunks(text, n), self.weight)[:k]


def build(corpus, cfg):
    return Hybrid(corpus, cfg)
