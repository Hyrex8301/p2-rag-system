# Decision log

Your methods section, in your own words.
About one to two pages in total.

Answer these as you go, not the night before it is due.
Each answer is easier to write while the decision is still fresh, and prompt 1 only works if you write it before you see your own-corpus numbers.
Specifics beat polish: a short, honest answer with a number in it is worth more than a long vague one.

Each prompt ends with a marker line.
Replace that line with your answer.
`uv run p2 check` reports a marker as unfinished work, and `uv run p2 check --final` fails while any marker is left, so a finished log is part of being done.

Please do not let the agent write these for you.
These answers are about what you chose and what you knew, and the agent cannot know that.
Prompt 3 in particular only works in your own words.

---

## 1. Why this corpus, and what you expected

Why did you pick the corpus you used in stage 2, and why does it belong to a field or a question you care about?
Then say what you expected before you measured anything: which of `bm25`, `dense`, `hybrid` and `rerank` do you think will win on it, and which will do worst, and why?

Commit this answer before your first `uv run p2 score` on the own corpus.
Git history then shows that the expectation came first, which is what lets it be wrong in a way that teaches you something.
If you were surprised later, say so in prompt 4 or in EVAL.md; do not come back and rewrite this one.

I chose the corpus I use in stage 2 mostly because I like the outdoors and I thought it would be interesting to see if the rag would be able to pick all of this up. There are a few other options I was comparing it against. One of them was video games, but I found that the outdoors would be more interesting and it would have a wider variety of stuff to look up and ask. From before, I expected BM25 to do pretty well if you were directly quoting the article, because it could just look up those keywords. And I also expected dense to do pretty well with normal language and just a user prompting the query. I also expected the hybrid to do better than both of the dense and BM25. Because it's a combination of the two, so it can use keyword and it can use context clues to actually get the answer. And I expect Rerank to do the best of all four. Rerank will be number one because it uses Claude calls and hybrid doesn't. And Claude is able to read a passage from each of the top 20 and judge which one answers the question, instead of just scoring keywords and meaning. Therefore, I think re-rank will do the best, and BM25 will do the worst. And in between those two will be hybrid and dense. This is mostly because the type of questions we will be asking will use simple language and won't directly correlate to the article, unless you're asking about like elevation or stuff like that. Then BM25 will do very well, but overall, we'll be asking about stuff that will use human language instead of direct keywords. And I also am writing this after I already ran the experiment, because I didn't know we were supposed to write this in beforehand. But this is what I would have predicted. If I had written it earlier, and I can base these predictions off of lab 12 because we had already used some of these measurements.

---

## 2. A fork in the road

Name one real design choice where you could have gone two ways: the chunk size, the embedding model, how the two systems are fused, how many documents the reranker sees, a sentence in `prompts/answer.txt`, how you cleaned the corpus.

Say which you picked, what the alternative was, and what you gave up by not taking it.
If you measured both, give both numbers.
If you rejected the alternative without measuring it, say why that was a fair call, and what it cost you in time, tokens or complexity.

"There was no alternative" is not an answer.
Find the fork.

TODO: your answer to prompt 2.

---

## 3. Where you overruled the agent

One time Claude suggested, wrote or claimed something and you did not take it.
It might be a relevance judgment you disagreed with, a retriever it called finished when a run file showed otherwise, a number it summarized wrongly, or a license it said was fine.

What did it do?
How did you notice?
What did you do instead?

If it genuinely never happened, say so plainly, and then say what you would have had to check in order to notice.
Being honest here costs you far less than a story you cannot defend when you record your video.

TODO: your answer to prompt 3.

---

## 4. A number you do not trust

Pick one number in `EVAL.md` that you do not fully trust, and say why.
It could be a mean over a small query class, a difference whose interval includes zero, a verified share of 100%, a score on a gold set you wrote yourself, or a result you got only once.

What would have to be true for you to trust it?
Did you do anything to test it, and what did that show?

TODO: your answer to prompt 4.

---

## 5. What is still wrong

One thing in your system, your corpus or your gold set that is not right, not finished, or that you do not fully understand.

What would you do next, and how would you find out whether it matters?
Name the file, the query or the document where someone could look.

TODO: your answer to prompt 5.
