"""Hybrid retrieval: score fusion of bm25 and dense.

Each system's top 100 scores are scaled to 0-1 (the best becomes 1, the 100th becomes 0), and a
document's fused score is the mean of its scaled scores (0 from a system that does not rank it in
its top 100). search_chunks does the same over chunk rankings, so `p2 answer` can use hybrid's chunks.

Why not the reciprocal rank fusion (RRF) of the 13 lab: on the shared practice queries RRF with the
lab's k = 60 scored below both bm25 and dense (MRR@10 0.471), because bm25 and dense find different
sections and k = 60 rewards a section both rank in the middle over one that either ranks first.
RRF with k = 10 fixed that (MRR@10 0.587) but did not reproduce in CI: dense's scores differ by about
0.000002 between macOS and Linux, enough to swap two near-tied sections, and with k = 10 one place
moves a fused score by more than the 0.001 that `p2 check` allows. Score fusion moves only as much as
the scores do (MRR@10 0.581, and no mismatch in 100 noisy trials). rrf() stays here because the
reranker's first stage uses it, and CI never runs the reranker again.

Settings, all optional, in p2.toml:

    [hybrid]
    systems = ["bm25", "dense"]
    depth = 100
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


def scaled_sum(rankings: list[list[tuple[str, float]]], depth: int) -> list[tuple[str, float]]:
    """Fuse rankings by the mean of each one's top-`depth` scores scaled to 0-1."""
    fused: dict[str, float] = {}
    for ranking in rankings:
        top = ranking[:depth]
        if not top:
            continue
        hi, lo = top[0][1], top[-1][1]
        span = (hi - lo) or 1.0
        for item, score in top:
            fused[item] = fused.get(item, 0.0) + (score - lo) / span / len(rankings)
    return order(fused.items())


class Hybrid:
    def __init__(self, corpus, cfg):
        settings = cfg.table("hybrid")
        self.depth = int(settings.get("depth", 100))
        self.systems = [build_system(name, corpus, cfg) for name in settings.get("systems", ["bm25", "dense"])]

    def search(self, text: str, k: int) -> list[tuple[str, float]]:
        depth = max(self.depth, k)
        return scaled_sum([s.search(text, depth) for s in self.systems], depth)[:k]

    def search_chunks(self, text: str, k: int) -> list[tuple[str, float]]:
        depth = max(self.depth, k)
        return scaled_sum([s.search_chunks(text, depth) for s in self.systems], depth)[:k]


def build(corpus, cfg):
    return Hybrid(corpus, cfg)
