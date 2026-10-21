"""Stretch option 3 (cost and latency): the reranker over 10 candidates instead of 20.

The one change is the number of candidates Claude sees; the first stage (RRF k = 10 of bm25 and
dense), the prompt, the passages and the model are rerank's. Half the passages should mean about
half the input tokens per call; the stretch-cost table in EVAL.md says what that saves and what it
costs in MRR@10 against rerank, with a paired interval.
"""

from p2.retrievers.rerank import Rerank

NEEDS_CLAUDE = True
CANDIDATES = 10


def build(corpus, cfg):
    return Rerank(corpus, cfg, candidates=CANDIDATES)
