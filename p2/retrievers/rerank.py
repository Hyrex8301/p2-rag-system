"""Reranking: Claude reorders a first stage's top 20.

A port of rerank_one() in the 13 lab's pipeline.py. The first stage gives its top 20; each one goes
to Claude as a numbered passage, and the reply is forced into {"order": [20 numbers]}, each from 1
to 20. A reply that is not each number exactly once keeps the first-stage order. Documents below the
20 keep their first-stage order underneath.

The first stage is reciprocal rank fusion (RRF, k = 10) of bm25 and dense, which puts a relevant
section in the top 20 for 18 of the 20 shared practice queries (16 with the lab's k = 60). It is not
the hybrid system: hybrid uses score fusion, because RRF with k = 10 does not reproduce exactly
between macOS and Linux (see hybrid.py), and CI runs hybrid again but never the reranker, whose runs
are checked against their traces.

One change from the lab: a document's passage is its best chunk for this query in the first stage's
chunk ranking (with the document's title in front), not the document's first characters, so a long
document is shown by the part that matched. Every passage is cut to PASSAGE_CHARS characters.

search_chunks, which `p2 answer` uses, does the same over the first stage's top 20 chunks.
Every call goes through p2.claude.call, which caches the reply and adds its tokens to the trace.

Settings, all optional, in p2.toml:

    [rerank]
    first = ["bm25", "dense"]
    rrf_k = 10
    candidates = 20
    passage_chars = 600
"""

from __future__ import annotations

import sys

from p2 import claude
from p2.retrievers import build as build_system
from p2.retrievers.hybrid import rrf

NEEDS_CLAUDE = True

CANDIDATES = 20
PASSAGE_CHARS = 600
PROMPT = """Below are {n} passages from a document collection, numbered 1 to {n}, and a search query.
Order the passages from the most useful for answering the query to the least useful.
Reply with all {n} passage numbers, each exactly once, best first.

Query: {query}

{passages}"""


def schema(n: int) -> dict:
    numbers = {"type": "integer", "minimum": 1, "maximum": n}
    return {
        "type": "object",
        "properties": {"order": {"type": "array", "items": numbers, "minItems": n, "maxItems": n}},
        "required": ["order"],
    }


class Rerank:
    def __init__(self, corpus, cfg, candidates: int | None = None):
        settings = cfg.table("rerank")
        self.corpus = corpus
        self.cfg = cfg
        self.model = cfg.model
        self.candidates = candidates or int(settings.get("candidates", CANDIDATES))
        self.passage_chars = int(settings.get("passage_chars", PASSAGE_CHARS))
        self.rrf_k = int(settings.get("rrf_k", 10))
        self.systems = [build_system(name, corpus, cfg) for name in settings.get("first", ["bm25", "dense"])]
        self.chunk_texts = corpus.chunk_texts(cfg.chunk_words, cfg.chunk_overlap)

    def first_docs(self, text: str, k: int) -> list[tuple[str, float]]:
        n = len(self.corpus.docs)
        return rrf([s.search(text, n) for s in self.systems], self.rrf_k)[:k]

    def first_chunks(self, text: str, k: int) -> list[tuple[str, float]]:
        n = len(self.chunk_texts)
        return rrf([s.search_chunks(text, n) for s in self.systems], self.rrf_k)[:k]

    def passage(self, chunk_id: str) -> str:
        docid, n = chunk_id.rsplit("#", 1)
        text = self.chunk_texts[chunk_id]
        if n != "0":  # only a document's first chunk starts with its title line
            text = f"# {self.corpus.docs[docid].title}\n{text}"
        return text[: self.passage_chars]

    def reorder(self, query: str, items: list[str], passages: list[str]) -> list[str]:
        """Claude's order of items, or items unchanged when the reply is not usable."""
        n = len(items)
        numbered = "\n\n".join(f"[{i}] {p}" for i, p in enumerate(passages, 1))
        prompt = PROMPT.format(n=n, query=query, passages=numbered)
        reply = claude.call(prompt, schema(n), model=self.cfg.model, cache_dir=claude.cache_folder(self.cfg))
        order = (reply.output or {}).get("order")
        if reply.error or not isinstance(order, list) or sorted(order) != list(range(1, n + 1)):
            print(f"rerank: kept the first-stage order for {query[:60]!r} ({reply.error or f'reply was {order}'})", file=sys.stderr)
            return items
        return [items[i - 1] for i in order]

    def search(self, text: str, k: int) -> list[tuple[str, float]]:
        first = [d for d, _ in self.first_docs(text, max(k, self.candidates))]
        top = first[: self.candidates]
        if not top:
            return []
        wanted, best_chunk = set(top), {}
        for chunk_id, _ in self.first_chunks(text, len(self.chunk_texts)):
            docid = chunk_id.rsplit("#", 1)[0]
            if docid in wanted and docid not in best_chunk:
                best_chunk[docid] = chunk_id
                if len(best_chunk) == len(wanted):
                    break
        ranked = self.reorder(text, top, [self.passage(best_chunk[d]) for d in top]) + first[self.candidates :]
        return [(d, float(len(ranked) - i)) for i, d in enumerate(ranked)][:k]

    def search_chunks(self, text: str, k: int) -> list[tuple[str, float]]:
        first = [c for c, _ in self.first_chunks(text, max(k, self.candidates))]
        top = first[: self.candidates]
        if not top:
            return []
        ranked = self.reorder(text, top, [self.passage(c) for c in top]) + first[self.candidates :]
        return [(c, float(len(ranked) - i)) for i, c in enumerate(ranked)][:k]


def build(corpus, cfg):
    return Rerank(corpus, cfg)
