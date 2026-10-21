"""Reranking: Claude reorders a first-stage system's top 20.

A port of rerank_one() in the 13 lab's pipeline.py. The first stage (hybrid) gives its top 20; each
one goes to Claude as a numbered passage, and the reply is forced into {"order": [20 numbers]}, each
from 1 to 20. A reply that is not each number exactly once keeps the first-stage order. Documents
below the 20 keep their first-stage order underneath.

One change from the lab: a document's passage is its best chunk for this query in the first stage's
chunk ranking (with the document's title in front), not the document's first characters, so a long
document is shown by the part that matched. Every passage is cut to PASSAGE_CHARS characters.

search_chunks, which `p2 answer` uses, does the same over the first stage's top 20 chunks.
Every call goes through p2.claude.call, which caches the reply and adds its tokens to the trace.

Settings, all optional, in p2.toml:

    [rerank]
    first = "hybrid"
    candidates = 20
    passage_chars = 600
"""

from __future__ import annotations

import sys

from p2 import claude
from p2.retrievers import build as build_system

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
        self.first = build_system(settings.get("first", "hybrid"), corpus, cfg)
        self.chunk_texts = corpus.chunk_texts(cfg.chunk_words, cfg.chunk_overlap)

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
        first = [d for d, _ in self.first.search(text, max(k, self.candidates))]
        top = first[: self.candidates]
        if not top:
            return []
        wanted, best_chunk = set(top), {}
        for chunk_id, _ in self.first.search_chunks(text, len(self.chunk_texts)):
            docid = chunk_id.rsplit("#", 1)[0]
            if docid in wanted and docid not in best_chunk:
                best_chunk[docid] = chunk_id
                if len(best_chunk) == len(wanted):
                    break
        ranked = self.reorder(text, top, [self.passage(best_chunk[d]) for d in top]) + first[self.candidates :]
        return [(d, float(len(ranked) - i)) for i, d in enumerate(ranked)][:k]

    def search_chunks(self, text: str, k: int) -> list[tuple[str, float]]:
        first = [c for c, _ in self.first.search_chunks(text, max(k, self.candidates))]
        top = first[: self.candidates]
        if not top:
            return []
        ranked = self.reorder(text, top, [self.passage(c) for c in top]) + first[self.candidates :]
        return [(c, float(len(ranked) - i)) for i, c in enumerate(ranked)][:k]


def build(corpus, cfg):
    return Rerank(corpus, cfg)
