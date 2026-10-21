# Evaluation report

This is the report on what you built and what the numbers let you claim.
Two kinds of text live here.

The tables between a `p2:begin` comment line and its matching `p2:end` comment line are written by `uv run p2 score` from your committed run files and answers files.
Please do not edit anything between those two lines, because `uv run p2 check` recomputes them and fails when they differ.
A table that says no runs or answers exist yet is waiting for data; run `uv run p2 score` after you commit the files it needs.

Everything else is yours.
Each prompt ends with a marker line that you replace with your own writing; `uv run p2 check --final` fails while one is left.
Write what you measured, including what did not work.
What I read for is whether each claim matches its interval, not whether the result is good news.

Words used below: recall@10, MRR@10 and nDCG@10 are the three scores, each averaged over the queries of a set; step 7 of stage 1 in the README defines them, and lecture 14 goes deeper.
A paired interval is the 95% interval of the mean difference between two systems on the same queries, found by resampling the queries 10,000 times.
When an interval includes zero, the gold set cannot tell the two systems apart, and the right words are "not distinguishable on this gold set".
The minimum detectable difference is the smallest gap this many queries could reliably show, so a difference below it is invisible to this gold set, not absent.

---

## 1. Stage 1 - the shared corpus (30 CFR Chapter I)

### What you built

For each of `dense`, `hybrid` and `rerank`, one or two sentences: the embedding model, how documents were chunked, what was fused and how, how many candidates the reranker saw, and anything you changed from the 12 and 13 lab code.

For dense, I use the bge-small-en-v1.5 embedding model. It is the same as the lab12's bge, and it compares the query's meanings with every chunk. Each chunk has 300-word chunks with 50 words of overlap.

For hybrid I did the formula of 0.1 × (bm25 ÷ the query's best bm25 score) + dense's score over every document. This changed from the lab's reciprocal rank fusion, or RRF, of k equals 60, which scored 0.471 MRR@10 on the 20 practice queries, below both bm25 (0.507) and dense (0.562). With a k equal to 10, it scored 0.587, but failed the CI, as did a scaled version (0.581). The final version scores a 0.642 and reproduces on the CI. Once again, the chunking is 300-word chunks with 50 words of overlap.

For the rerank, I used Claude Sonnet version. And it reorders the top twenty from RRF of k equals 10 of BM25 and dense. The RRF k equals 10 is fine because the CI never re-runs the reranker: it calls Claude, so its runs are checked against the saved traces instead. This changed from the lab as each candidate is shown as its best matching chunk with the section title, not the start of the document. The passages are capped at 600 characters and the reply only uses numbers 1 through 20. Once again, the chunking uses 300 word chunks with 50 words of overlap.

### Practice queries (20)

Scores per system.

<!-- p2:begin shared-practice -->
| System | Recall@10 | MRR@10 | nDCG@10 |
| --- | ---: | ---: | ---: |
| bm25 | 0.625 | 0.507 | 0.518 |
| dense | 0.558 | 0.562 | 0.480 |
| hybrid | 0.608 | 0.642 | 0.568 |
| rerank | 0.758 | 0.850 | 0.777 |
| rerank_c10 | 0.817 | 0.856 | 0.796 |

20 judged queries; nDCG uses binary labels; a random ranking of the 2,484 documents would get recall@10 near 0.004.
<!-- p2:end shared-practice -->

The same scores per query class.

<!-- p2:begin shared-practice-classes -->
| System | Metric | identifier (n=7) | paraphrase (n=7) | mixed (n=6) |
| --- | --- | ---: | ---: | ---: |
| bm25 | Recall@10 | 1.000 | 0.000 | 0.917 |
| bm25 | MRR@10 | 0.810 | 0.000 | 0.746 |
| bm25 | nDCG@10 | 0.857 | 0.000 | 0.728 |
| dense | Recall@10 | 0.214 | 0.595 | 0.917 |
| dense | MRR@10 | 0.333 | 0.714 | 0.653 |
| dense | nDCG@10 | 0.211 | 0.593 | 0.661 |
| hybrid | Recall@10 | 0.500 | 0.452 | 0.917 |
| hybrid | MRR@10 | 0.571 | 0.571 | 0.806 |
| hybrid | nDCG@10 | 0.480 | 0.457 | 0.801 |
| rerank | Recall@10 | 0.786 | 0.595 | 0.917 |
| rerank | MRR@10 | 0.857 | 0.714 | 1.000 |
| rerank | nDCG@10 | 0.805 | 0.626 | 0.922 |
| rerank_c10 | Recall@10 | 1.000 | 0.548 | 0.917 |
| rerank_c10 | MRR@10 | 0.873 | 0.714 | 1.000 |
| rerank_c10 | nDCG@10 | 0.891 | 0.592 | 0.922 |
<!-- p2:end shared-practice-classes -->

Differences between every pair of systems, each with its paired interval and the minimum detectable difference.

<!-- p2:begin shared-practice-pairs -->
| Comparison | Metric | Mean difference | 95% interval | MDD | Reading |
| --- | --- | ---: | ---: | ---: | --- |
| dense minus bm25 | Recall@10 | -0.067 | [-0.350, +0.225] | 0.415 | not distinguishable |
| dense minus bm25 | MRR@10 | +0.055 | [-0.225, +0.343] | 0.412 | not distinguishable |
| dense minus bm25 | nDCG@10 | -0.039 | [-0.302, +0.231] | 0.385 | not distinguishable |
| hybrid minus bm25 | Recall@10 | -0.017 | [-0.258, +0.225] | 0.350 | not distinguishable |
| hybrid minus bm25 | MRR@10 | +0.135 | [-0.098, +0.375] | 0.340 | not distinguishable |
| hybrid minus bm25 | nDCG@10 | +0.050 | [-0.162, +0.262] | 0.308 | not distinguishable |
| hybrid minus dense | Recall@10 | +0.050 | [-0.100, +0.175] | 0.201 | not distinguishable |
| hybrid minus dense | MRR@10 | +0.079 | [-0.104, +0.271] | 0.272 | not distinguishable |
| hybrid minus dense | nDCG@10 | +0.088 | [-0.070, +0.240] | 0.223 | not distinguishable |
| rerank minus bm25 | Recall@10 | +0.133 | [-0.075, +0.342] | 0.308 | not distinguishable |
| rerank minus bm25 | MRR@10 | +0.343 | [+0.100, +0.576] | 0.344 | rerank higher |
| rerank minus bm25 | nDCG@10 | +0.259 | [+0.033, +0.474] | 0.320 | rerank higher |
| rerank minus dense | Recall@10 | +0.200 | [+0.050, +0.375] | 0.236 | rerank higher |
| rerank minus dense | MRR@10 | +0.287 | [+0.117, +0.471] | 0.259 | rerank higher |
| rerank minus dense | nDCG@10 | +0.298 | [+0.145, +0.467] | 0.236 | rerank higher |
| rerank minus hybrid | Recall@10 | +0.150 | [+0.000, +0.350] | 0.251 | not distinguishable |
| rerank minus hybrid | MRR@10 | +0.208 | [+0.050, +0.392] | 0.242 | rerank higher |
| rerank minus hybrid | nDCG@10 | +0.209 | [+0.059, +0.387] | 0.238 | rerank higher |
| rerank_c10 minus bm25 | Recall@10 | +0.192 | [+0.050, +0.358] | 0.223 | rerank_c10 higher |
| rerank_c10 minus bm25 | MRR@10 | +0.348 | [+0.115, +0.576] | 0.335 | rerank_c10 higher |
| rerank_c10 minus bm25 | nDCG@10 | +0.277 | [+0.088, +0.467] | 0.274 | rerank_c10 higher |
| rerank_c10 minus dense | Recall@10 | +0.258 | [+0.083, +0.450] | 0.270 | rerank_c10 higher |
| rerank_c10 minus dense | MRR@10 | +0.293 | [+0.122, +0.476] | 0.257 | rerank_c10 higher |
| rerank_c10 minus dense | nDCG@10 | +0.316 | [+0.159, +0.484] | 0.237 | rerank_c10 higher |
| rerank_c10 minus hybrid | Recall@10 | +0.208 | [+0.050, +0.384] | 0.242 | rerank_c10 higher |
| rerank_c10 minus hybrid | MRR@10 | +0.214 | [+0.058, +0.394] | 0.240 | rerank_c10 higher |
| rerank_c10 minus hybrid | nDCG@10 | +0.228 | [+0.091, +0.388] | 0.214 | rerank_c10 higher |
| rerank_c10 minus rerank | Recall@10 | +0.058 | [-0.033, +0.183] | 0.163 | not distinguishable |
| rerank_c10 minus rerank | MRR@10 | +0.006 | [+0.000, +0.017] | 0.016 | not distinguishable |
| rerank_c10 minus rerank | nDCG@10 | +0.018 | [-0.023, +0.067] | 0.070 | not distinguishable |

The interval is a paired bootstrap (10,000 resamples of the queries); MDD is the smallest difference this many queries detect 80% of the time.
<!-- p2:end shared-practice-pairs -->

The 40 test queries have no answer key in this repo.
Your test run files are scored by the course and the score comes back to you as feedback, so nothing goes here for them.

### What the intervals let you claim

Which differences are distinguishable from zero and which are not?
What is the minimum detectable difference at 20 queries, and what does that say about any gap smaller than it?
Which claim from lecture 12 or 13 did your numbers support, and which did they leave open?

Re-rank is higher than any of the other three, as all three intervals are above 0. This shows that rerank is higher, by somewhere between 0.05 and 0.39 against hybrid, against bm25 it's [+0.100, +0.576], and against dense it's [+0.117, +0.471]. However, this is only true on the 20 practice queries.

The other three are not as distinguishable. For example dense - bm25 has the interval [−0.225, +0.343] so the real difference can be large in either direction. 20 queries is not able to tell.

The minimum detectable difference at 20 queries is 0.27 to 0.41, for BM25 dense and hybrid, and 0.24 to 0.34 for anything involving the re-rank. Therefore, when we're looking at the 20 queries, you can't reliably see a difference of that size, even if there is a difference. Each of 0.055, 0.135, and 0.079 is smaller than its MDD, so it being non distinguishable doesn't make the systems equal.

In lecture 12, we found that every retriever has a failure that we can predict and measure. And this was shown when the BM25 scored 0 on the paraphrase, and 0.810 on identifiers, this was very clear that BM25 is pretty bad at paraphrasing, and just can't do very well on it. While if it has to identify something very specific, it can do that. And dense scored 0.333 on identifiers, and 0.714 on paraphrases. And this makes sense, as dense was expected to have scored higher on paraphrases which it did. However, this was only tested over 7 queries per class.

In lecture 13, Fusion helps a weaker partner and hurts an already strong retriever. On identifiers, fusion pulled BM25, which was the strong system, down from (0.810) to (0.571). While on paraphrases, it lifted the weak one, BM25, from 0 to 0.571, but pulled dense down from 0.714 to 0.571. Hybrid isn't distinguishable from either system as its intervals include 0. The class pattern points towards the fusion claim but with 7 queries per class and a non distinguishable result the claim stays open. Lecture 13 also says that the re-ranker cannot rescue a document that is not among its candidates. And this was shown in P10 and P14, that are both paraphrases where no relevant section was in the first stage's top 20. And re-rank found no relevant section in its top 10 for either of them.

---

## 2. Stage 1 - cited answers on the 12 shared questions

<!-- p2:begin answers -->
| Label | System | Verified (in) | 95% interval | not_found (in) | Declined (out) | 95% interval | Quotes found |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| rerank | rerank | 8 of 8 (100%) | [0.676, 1.000] | 0 of 8 (0%) | 4 of 4 (100%) | [0.510, 1.000] | 16 of 16 |
<!-- p2:end answers -->

Which system answered, and why that one?
What did you change in `prompts/answer.txt`, if anything, and did the verified share or the declined share move?

Then read three in-corpus answers that `uv run p2 verify` passed.
For each one, open the cited chunk and say whether the quote really supports the claim next to it.
The check proves a quote is a real piece of the chunk and cannot prove that it supports the claim, so this reading is the part only you can do.

Rerank answered all 12 questions. This is because it had the best MRR@10 of 0.850. So it put the most relevant section first most often. And each answer only uses the top 5 chunks, so ranking well is important. It cost 2 Claude calls per question, one of them was to re-rank and the other one was to answer. With a total of 24 calls. If we answered with hybrid, we only needed one call per question, which would just be 12 calls.

I didn't change `prompts/answer.txt`. It's still on the lab 13 prompt. And I didn't compare anything against it, so there's no change to report.

a03 had one claim that was supported, it dropped the words "and to visitors", but I don't think it changes the overall claim and support.

For a06, claims 1, 2, and 4 are fully supported, and claim 3 is partly supported. It said, lower than the PEL, but that isn't in the quote, so it is partially supported as it included everything else. And the answer had a main sentence that also included PEL, which is correct, but no quote backs it up. Claude never saw the definition of the PEL. It was in a chunk that wasn't given, so it combined two claims together.

For a07, claims 1, 2, and 3 are partly supported, and claim 4 is supported. Claims 1 and 2 say surface and claim 3 says underground, but that isn't in the quote. Surface and underground are both implied, but the quotes don't say them, so both of them are only partly supported. The overall answer leaves out an exception, but I don't think it changes the overall message.

All 16 of the quotes were real, but in a06's main answer, there was no quote to back it up. And some claims carried words that Claude added, and therefore the check can't prove that it supports the claim.

---

## 3. Stage 2 - your corpus and your gold set

### The corpus

What is it, where did it come from, how many documents and how many megabytes, and what is the license basis for publishing it?
Name the one or two documents you were least sure about and what you decided.
Say which of the allowed sources in the brief it comes from.

My corpus is 278 Wikipedia articles, about 'outdoors in Colorado.' They came from multiple categories, including 14ers, mountain passes, wilderness areas, state parks, hiking trails, and National Recreation Trails. Lakes, canyons, ski areas, national monuments, and the mountains of Rocky Mountain National Park. They came from plain text through Wikipedia's API. There were 446 articles in these categories and 168 of these articles were under 150 words, so they were left out. This left a total of 278 documents, around 162,000 words, around 227,000 tokens, and 1.0 MB. Wikipedia text is CC BY-SA 4.0, with attribution, and each row in `corpora/own/manifest.tsv` links to the exact article version. Everything passed the licensing check, so I wasn't worried about the licensing. But I was more worried about the fit. And one of these documents was Aspen Colorado. Which is a town article rather than an outdoor place, but it's also categorized as one of the ski areas, so I decided to include it in there. I also had one article, Rollins Pass, that was longer than 6,000 words, so the fetch script cut it at a paragraph break down to 5,907 words. I was debating whether to keep it in or just cut it short, and I kept it in, cut to 5,907 words.

### The gold set

How many queries, how many with origin `hand` and how many with origin `claude`, and which query classes did you use and why?
How did you decide that a document is relevant: write your relevance rule in two or three sentences, the way the brief does for the shared corpus.
How did you find candidates (the systems' top 10, a keyword search, reading), and did you read every document before you labeled it?
Your labels are binary (`rel` 1) unless you say otherwise: if you use graded labels, declare the scale here, for example 2 means the document answers the query fully and 1 means it helps.

I had a total of 31 queries with 10 hand and 21 Claude. As for the classes, I had 14 identifier, 10 paraphrase, and 7 mixed. And these are the same 3 classes as the shared set. So the class scores line up for the cross-corpus comparison. Identifier names the place it asks about, paraphrase names no place, mixed, I tried to name a nearby place, road, or agency, while the answer is about a different place. My rule was: "An article is only relevant if it states the answer to the question directly." There were some close cases, such as c04, and I counted articles that stated the answer directly, but in passing, inside an article about something else. There were also topics without the answer, such as articles that only mention the topic, didn't count, an example of this was the Tennessee Pass, which mentions the Moffat Tunnel, but it gave no date. Lastly, for h01, I had it written as how long, and distance and time both counted for this. There were 536 candidates in all, around 14 to 21 per query. And they came from the top 10 of BM25, Dense, and Hybrid. As well as a keyword search of article titles, and for every candidate, Claude Code searched the full article text for specific answers and showed me the matching sentences. I made every relevance decision. I did not read every document, I just judged from each article's opening sentences, the closest sentences, and the matches from the full text search. I never read an article in full. Along the way, I had some spelling errors in my h01 and h10. I had to fix them because when I actually did the search for h01, nothing was able to pop up with the misspelling, so I fixed both at the same time. I also had to replace h05, h08, and h09 because not a single article answered them. They were more open-ended questions about advice instead of simple facts that Wikipedia states. Overall, there were 45 judgments. 21 queries have one relevant article, 9 have two relevant articles, and c04 has 6 relevant articles.

---

## 4. Stage 2 - results on your corpus

Scores per system on your gold set.

<!-- p2:begin own -->
| System | Recall@10 | MRR@10 | nDCG@10 |
| --- | ---: | ---: | ---: |
| bm25 | 0.968 | 0.899 | 0.903 |
| dense | 0.871 | 0.839 | 0.793 |
| hybrid | 0.962 | 0.892 | 0.886 |
| rerank | 0.984 | 1.000 | 0.986 |
| ablation/dense_c100 | 0.984 | 0.816 | 0.847 |

31 judged queries; nDCG uses binary labels; a random ranking of the 278 documents would get recall@10 near 0.036.
<!-- p2:end own -->

The same scores per query class.

<!-- p2:begin own-classes -->
| System | Metric | paraphrase (n=10) | identifier (n=14) | mixed (n=7) |
| --- | --- | ---: | ---: | ---: |
| bm25 | Recall@10 | 0.900 | 1.000 | 1.000 |
| bm25 | MRR@10 | 0.820 | 0.964 | 0.881 |
| bm25 | nDCG@10 | 0.816 | 0.968 | 0.897 |
| dense | Recall@10 | 0.700 | 0.964 | 0.929 |
| dense | MRR@10 | 0.600 | 0.964 | 0.929 |
| dense | nDCG@10 | 0.544 | 0.946 | 0.842 |
| hybrid | Recall@10 | 0.883 | 1.000 | 1.000 |
| hybrid | MRR@10 | 0.767 | 0.964 | 0.929 |
| hybrid | nDCG@10 | 0.768 | 0.968 | 0.889 |
| rerank | Recall@10 | 1.000 | 1.000 | 0.929 |
| rerank | MRR@10 | 1.000 | 1.000 | 1.000 |
| rerank | nDCG@10 | 0.996 | 1.000 | 0.945 |
| ablation/dense_c100 | Recall@10 | 0.950 | 1.000 | 1.000 |
| ablation/dense_c100 | MRR@10 | 0.613 | 0.917 | 0.905 |
| ablation/dense_c100 | nDCG@10 | 0.694 | 0.938 | 0.885 |
<!-- p2:end own-classes -->

The same scores for the queries you wrote yourself (`hand`) and the ones a model drafted (`claude`), with the difference between the two groups and its interval.
Once both groups have queries, the table also says whether `bm25`'s lead over `dense` differs between them, and what share of each query's content words its best relevant document contains, which is stretch option 6.

<!-- p2:begin own-origins -->
| System | Metric | hand (n=10) | claude (n=21) | hand minus claude | 95% interval | Reading |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| bm25 | Recall@10 | 1.000 | 0.952 | +0.048 | [+0.000, +0.143] | not distinguishable |
| bm25 | MRR@10 | 0.867 | 0.914 | -0.048 | [-0.267, +0.140] | not distinguishable |
| bm25 | nDCG@10 | 0.884 | 0.912 | -0.028 | [-0.199, +0.132] | not distinguishable |
| dense | Recall@10 | 0.850 | 0.881 | -0.031 | [-0.226, +0.164] | not distinguishable |
| dense | MRR@10 | 0.900 | 0.810 | +0.090 | [-0.105, +0.281] | not distinguishable |
| dense | nDCG@10 | 0.810 | 0.785 | +0.026 | [-0.147, +0.205] | not distinguishable |
| hybrid | Recall@10 | 1.000 | 0.944 | +0.056 | [+0.000, +0.159] | not distinguishable |
| hybrid | MRR@10 | 0.900 | 0.889 | +0.011 | [-0.160, +0.180] | not distinguishable |
| hybrid | nDCG@10 | 0.901 | 0.878 | +0.023 | [-0.112, +0.162] | not distinguishable |
| rerank | Recall@10 | 1.000 | 0.976 | +0.024 | [+0.000, +0.071] | not distinguishable |
| rerank | MRR@10 | 1.000 | 1.000 | +0.000 | [+0.000, +0.000] | not distinguishable |
| rerank | nDCG@10 | 1.000 | 0.980 | +0.020 | [+0.000, +0.059] | not distinguishable |
| ablation/dense_c100 | Recall@10 | 0.950 | 1.000 | -0.050 | [-0.150, +0.000] | not distinguishable |
| ablation/dense_c100 | MRR@10 | 0.737 | 0.854 | -0.117 | [-0.351, +0.112] | not distinguishable |
| ablation/dense_c100 | nDCG@10 | 0.775 | 0.882 | -0.107 | [-0.298, +0.075] | not distinguishable |

The hand and claude queries are different queries, so the interval of hand minus claude comes from resampling the queries within each group (10,000 times), not from pairing them.

Do model-written queries favor keyword search? bm25's lead over dense (bm25 minus dense, per query) on the claude queries and on the hand queries, and claude minus hand:

| Metric | Lead on claude | Lead on hand | Claude minus hand | 95% interval | Reading |
| --- | ---: | ---: | ---: | ---: | --- |
| Recall@10 | +0.071 | +0.150 | -0.079 | [-0.298, +0.140] | not distinguishable |
| MRR@10 | +0.105 | -0.033 | +0.138 | [+0.019, +0.288] | bm25 gains more on claude queries |
| nDCG@10 | +0.127 | +0.074 | +0.054 | [-0.116, +0.228] | not distinguishable |

Mean content-word overlap, the share of a query's content words found in its best relevant document: hand 0.67 (10 queries), claude 0.82 (21 queries).

Stretch option 6 asks for at least 20 judged queries of each origin; here there are 10 hand and 21 claude.
<!-- p2:end own-origins -->

Differences between every pair of systems.

<!-- p2:begin own-pairs -->
| Comparison | Metric | Mean difference | 95% interval | MDD | Reading |
| --- | --- | ---: | ---: | ---: | --- |
| dense minus bm25 | Recall@10 | -0.097 | [-0.226, +0.016] | 0.177 | not distinguishable |
| dense minus bm25 | MRR@10 | -0.060 | [-0.156, +0.016] | 0.127 | not distinguishable |
| dense minus bm25 | nDCG@10 | -0.110 | [-0.206, -0.025] | 0.133 | bm25 higher |
| hybrid minus bm25 | Recall@10 | -0.005 | [-0.097, +0.091] | 0.131 | not distinguishable |
| hybrid minus bm25 | MRR@10 | -0.006 | [-0.051, +0.032] | 0.060 | not distinguishable |
| hybrid minus bm25 | nDCG@10 | -0.017 | [-0.066, +0.031] | 0.071 | not distinguishable |
| hybrid minus dense | Recall@10 | +0.091 | [+0.022, +0.183] | 0.116 | hybrid higher |
| hybrid minus dense | MRR@10 | +0.054 | [-0.003, +0.121] | 0.091 | not distinguishable |
| hybrid minus dense | nDCG@10 | +0.093 | [+0.036, +0.161] | 0.090 | hybrid higher |
| rerank minus bm25 | Recall@10 | +0.016 | [-0.048, +0.097] | 0.102 | not distinguishable |
| rerank minus bm25 | MRR@10 | +0.101 | [+0.016, +0.205] | 0.138 | rerank higher |
| rerank minus bm25 | nDCG@10 | +0.083 | [+0.007, +0.178] | 0.125 | rerank higher |
| rerank minus dense | Recall@10 | +0.113 | [+0.016, +0.226] | 0.155 | rerank higher |
| rerank minus dense | MRR@10 | +0.161 | [+0.056, +0.274] | 0.161 | rerank higher |
| rerank minus dense | nDCG@10 | +0.193 | [+0.093, +0.301] | 0.150 | rerank higher |
| rerank minus hybrid | Recall@10 | +0.022 | [-0.043, +0.102] | 0.103 | not distinguishable |
| rerank minus hybrid | MRR@10 | +0.108 | [+0.027, +0.204] | 0.133 | rerank higher |
| rerank minus hybrid | nDCG@10 | +0.100 | [+0.027, +0.190] | 0.119 | rerank higher |
| ablation/dense_c100 minus bm25 | Recall@10 | +0.016 | [-0.048, +0.097] | 0.102 | not distinguishable |
| ablation/dense_c100 minus bm25 | MRR@10 | -0.083 | [-0.178, +0.004] | 0.133 | not distinguishable |
| ablation/dense_c100 minus bm25 | nDCG@10 | -0.055 | [-0.132, +0.021] | 0.111 | not distinguishable |
| ablation/dense_c100 minus dense | Recall@10 | +0.113 | [+0.032, +0.210] | 0.141 | ablation/dense_c100 higher |
| ablation/dense_c100 minus dense | MRR@10 | -0.023 | [-0.116, +0.068] | 0.133 | not distinguishable |
| ablation/dense_c100 minus dense | nDCG@10 | +0.054 | [-0.021, +0.132] | 0.111 | not distinguishable |
| ablation/dense_c100 minus hybrid | Recall@10 | +0.022 | [-0.043, +0.102] | 0.103 | not distinguishable |
| ablation/dense_c100 minus hybrid | MRR@10 | -0.076 | [-0.160, -0.004] | 0.115 | hybrid higher |
| ablation/dense_c100 minus hybrid | nDCG@10 | -0.038 | [-0.111, +0.025] | 0.101 | not distinguishable |
| ablation/dense_c100 minus rerank | Recall@10 | +0.000 | [-0.048, +0.048] | 0.065 | not distinguishable |
| ablation/dense_c100 minus rerank | MRR@10 | -0.184 | [-0.294, -0.083] | 0.152 | rerank higher |
| ablation/dense_c100 minus rerank | nDCG@10 | -0.139 | [-0.231, -0.053] | 0.128 | rerank higher |

The interval is a paired bootstrap (10,000 resamples of the queries); MDD is the smallest difference this many queries detect 80% of the time.
<!-- p2:end own-pairs -->

Which differences are distinguishable and which are not, at your gold-set size?
Do the `hand` queries and the `claude` queries tell the same story?
Did your prediction in `DECISIONS.md` prompt 1 hold?

Re-rank is distinguishably higher than each of the others. When compared to BM25, dense and hybrid. The other three pairs aren't distinguishable. The MDD is 0.06 to 0.16, which is much smaller than the shared set's 0.24 to 0.41. And this is mostly because our scores are high and they have very little difference between queries. Our rerank scored 1.000 in every class. Since there is no room above 1, our gold set can't show whether re-rank would stay ahead if the queries were harder. Surprisingly, when looking at the paraphrase, which we had 10 of, BM25 had an MRR@10 of 0.820, which outranked dense and hybrid, which is very surprising, and I believe this is because the paraphrase queries share 77% of the words with the answer, while it was 9% in the shared set. As far as everything else goes, BM25 scored very high on the identifier, which is the same as the dense and hybrid, and BM25 scored the lowest on the mixed. While the dense and hybrid did very well in the mixed and the identifier. These per-class gaps are averages over 7 to 14 queries with no intervals, so they are not tested. And then, of course, re-rank scored a 1 overall, so it did very well. When comparing the hand and Claude queries, the difference is not distinguishable for any system. The re-rank is 1 in both groups. The one difference that is distinguishable is that BM25's lead over dense is bigger on the Claude queries (+0.138 [+0.019, +0.288], MRR@10 only). A likely reason is that Claude reads the articles and knows what to put in the query beforehand, while I made my queries before actually looking at the article itself: the Claude queries contain 82% of their answer article's words, and mine 67%. The only other difference could be that there are only 10 hand queries and 21 Claude queries, so there could be discrepancy in that.

I predicted that the rerank would do the best, which it did, as it is distinguishably above all three, so that means my prediction held here. I also predicted that BM25 would be the worst, however, BM25 had the highest average of the three non-Claude systems, so it did not hold by the averages. But none of these three differences are distinguishable, so the data can't show the reverse order either. I next predicted that hybrid would be above both, it was below BM25 and above dense, but it is distinguishable from neither. And lastly, my reason here was that the queries would use everyday language and not the article's words, however all 31 queries contained 78% of the article's words, the paraphrases have 77%, and the Claude queries have 82%. So this assumption didn't hold, which is most likely why BM25 did better than I expected.

---

## 5. The ablation

Change one thing and keep everything else the same.
Write your hypothesis here before you run it, in one sentence with a direction: "I expect X to raise MRR@10 on my corpus because Y."
The run file for it lives in `runs/own/ablation/`.

**Hypothesis** (written before the run, 2026-10-21; the change is `dense` with 100-word chunks instead of 300, in `p2/retrievers/dense_c100.py`):
The articles that I have are a lot longer when compared to the regulation sections. So having a smaller chunk will hold fewer topics, but it will be more precise as the facts in the chunk take up a larger portion. For example, when looking at Cheyenne Mountain State Park article, it is hard to find information about dogs and is buried. Therefore, by lowering the words in the chunk, you are able to see the information about dog allowability as it has its own section in the chunk. From this, I expect it to raise MRR@10. But it will make generic statements less accurate while having the precise question more accurate.

<!-- p2:begin own-ablation -->
| Comparison | Metric | Mean difference | 95% interval | MDD | Reading |
| --- | --- | ---: | ---: | ---: | --- |
| ablation/dense_c100 minus bm25 | Recall@10 | +0.016 | [-0.048, +0.097] | 0.102 | not distinguishable |
| ablation/dense_c100 minus bm25 | MRR@10 | -0.083 | [-0.178, +0.004] | 0.133 | not distinguishable |
| ablation/dense_c100 minus bm25 | nDCG@10 | -0.055 | [-0.132, +0.021] | 0.111 | not distinguishable |
| ablation/dense_c100 minus dense | Recall@10 | +0.113 | [+0.032, +0.210] | 0.141 | ablation/dense_c100 higher |
| ablation/dense_c100 minus dense | MRR@10 | -0.023 | [-0.116, +0.068] | 0.133 | not distinguishable |
| ablation/dense_c100 minus dense | nDCG@10 | +0.054 | [-0.021, +0.132] | 0.111 | not distinguishable |
| ablation/dense_c100 minus hybrid | Recall@10 | +0.022 | [-0.043, +0.102] | 0.103 | not distinguishable |
| ablation/dense_c100 minus hybrid | MRR@10 | -0.076 | [-0.160, -0.004] | 0.115 | hybrid higher |
| ablation/dense_c100 minus hybrid | nDCG@10 | -0.038 | [-0.111, +0.025] | 0.101 | not distinguishable |
| ablation/dense_c100 minus rerank | Recall@10 | +0.000 | [-0.048, +0.048] | 0.065 | not distinguishable |
| ablation/dense_c100 minus rerank | MRR@10 | -0.184 | [-0.294, -0.083] | 0.152 | rerank higher |
| ablation/dense_c100 minus rerank | nDCG@10 | -0.139 | [-0.231, -0.053] | 0.128 | rerank higher |

The interval is a paired bootstrap (10,000 resamples of the queries); MDD is the smallest difference this many queries detect 80% of the time.
<!-- p2:end own-ablation -->

The queries your ablation helped and hurt, against the system it varies, by reciprocal rank.
`p2 score` finds that system from a line such as `BASE = "bm25"` in your variant's file, or else from its name: `bm25_lab` varies `bm25`.

<!-- p2:begin own-ablation-queries -->
ablation/dense_c100 against dense (BASE = "dense" in p2/retrievers/dense_c100.py): it helped 4 queries, hurt 4 and left 23 unchanged.

| Query | Class | Origin | dense RR | ablation/dense_c100 RR | Change | Effect |
| --- | --- | --- | ---: | ---: | ---: | --- |
| c09 | paraphrase | claude | 0.250 | 1.000 | +0.750 | helped |
| c18 | paraphrase | claude | 0.000 | 0.333 | +0.333 | helped |
| c12 | paraphrase | claude | 0.250 | 0.500 | +0.250 | helped |
| c01 | paraphrase | claude | 0.000 | 0.100 | +0.100 | helped |
| h05 | paraphrase | hand | 1.000 | 0.200 | -0.800 | hurt |
| h10 | identifier | hand | 1.000 | 0.333 | -0.667 | hurt |
| c20 | paraphrase | claude | 1.000 | 0.500 | -0.500 | hurt |
| h09 | mixed | hand | 0.500 | 0.333 | -0.167 | hurt |

RR is the reciprocal rank of the first relevant document in the top 10 (0 when none is there), the per-query value behind MRR@10; the queries at the top of each list are the ones to read.
<!-- p2:end own-ablation-queries -->

What did you change, what happened, and does the interval support the claim you want to make?
If the result is not distinguishable, say what size of effect your gold set could have seen.
Read the queries at the top of each list in the second table, and say whether your change explains them.

The change I made was to change dense with 100 word chunks instead of 300. And the corpus went from 723 chunks to 2,091 chunks. The MRR@10 had a difference of −0.023 (0.839 to 0.816, interval [−0.116, +0.068]), and it was not distinguishable because its interval includes zero. The MDD for this was 0.133, so anything smaller than 0.13 was invisible with 31 queries. The results did not support my hypothesis, but it is also a very little change from what it actually was, and 31 queries can't tell whether it made a difference either way. It helped 4 queries (c09, c18, c12, c01) and hurt 4 (h05, h10, c20, h09). The rest of them were left unchanged. The ones that were most helped were because the fact was sitting in a short chunk of its own instead of being mixed into the article's opening. As well as making the chunk a full sentence that helped instead of splitting it apart. So it makes sense that the ones that were most hurt were splitting multiple of the important information into multiple chunks, for example, for h05, Hanging Lake went from rank 1 to rank 5, because "2 hours of hiking time", the lake, and the hike were split into different chunks. And for h10, how dangerous is quandary? It went from rank 1 to rank 3. The opening, with "class 1", "easy ascent" and "less danger from avalanche", was split up into different chunks. For h09, which is dogs at Cheyenne Mountain, went from rank 2 to 3, which is slightly worse. The article is only 392 words at 300 word chunks. The dog rule was already in a short last chunk of its own. And smaller chunks couldn't isolate it further, so it didn't really change too much. So I suppose I should have chose a better example. I originally expected the most help to be for this h09, again, I didn't look at the full article, but since it was pretty generic, and I thought the information would be hard to find in all of the different chunks. That when you made it into smaller chunks, all the information would be set into one chunk, but the dog rule stayed in one chunk and a North Sterling State Park chunk moved above it, making it slightly worse.

---

## 6. Failure analysis

Pick the queries where your best system on your own corpus failed: the relevant document is missing from the top 10, or sits far below the top.
Take at least five, and read what the system returned next to what was relevant.
Then sort the failures by cause, for example a vocabulary mismatch, near-duplicate documents, a chunk that cut the answer in half, a query that is ambiguous, or a label that was wrong, because sometimes the gold set is what failed.

Re-rank was the best system, and only fell short in 2 queries, which were c03 and c04. So the table also includes other queries where the other models also fell short.

| qid | what the best system returned | what was relevant | cause | what you would try |
|---|---|---|---|---|
| c03 | rerank: independence-pass at 1, aspen-colorado not in its top 10 (bm25, dense and hybrid had it at 3) | independence-pass, aspen-colorado | A chunk that got the answer cut off: the 600-character passage Claude saw for aspen-colorado ended just before the closure sentence | Make the chunk smaller |
| c04 | rerank: all 6 in its top 10, but aspen-colorado at 8 and vail-ski-resort at 10; dense found only 3 of the 6 | camp-hale, ski-cooper, aspen-colorado, aspen-mountain-ski-area, tennessee-pass, vail-ski-resort | Vocabulary mismatch: the articles say troops or 10th Mountain Division instead of the soldiers in the query | Try adding synonyms |
| c01 | dense and hybrid: not in their top 10 (eleven-mile-state-park, gore-canyon first); bm25: 5th | hanging-lake | Vocabulary mismatch: the query says thousand and climbs, the article says 1,000 feet and ascends | Try adding synonyms |
| c12 | bm25: not in its top 10 (mount-yale first); dense 4th, hybrid 6th | mount-elbert | Vocabulary mismatch: the query says tallest and the article says highest, so bm25 is going to miss it | Treat synonyms like tallest and highest as the same word; you could also rely on dense |
| c18 | dense: not in its top 10 (hanging-lake first); hybrid 2nd | rifle-falls-state-park | Both articles are about travertine | Use hybrid, which looks for the correct information |
| c09 | dense: 4th (trout-lake-colorado first) | trappers-lake | Two similar articles | Instead of looking for trout, look for the second largest lake |
| c07 | dense: 2nd (aspen-mountain-ski-area first) | silverton-mountain | Vocabulary mismatch | Try adding synonyms |
| h02 | bm25, dense and hybrid: 2nd (mount-blue-sky or hermosa-creek-wilderness first) | clear-creek-colorado | Similar documents: two places named Clear Creek | Add more information, such as Clear Creek in Golden, Colorado |
| h09 | bm25: 6th (castlewood-canyon-state-park first); dense and hybrid 2nd | cheyenne-mountain-state-park | Vocabulary mismatch: the query says dog and the article says Dogs | Count dog and dogs as the same word |

The cause that shows up most is a vocabulary mismatch or something similar. The system that misses the most is dense. Synonyms would help BM25, and to help dense instead you'd have to do something like read the whole sentence, so Trout Lake doesn't count for trout.

---

## 7. Cross-corpus comparison

The two tables to compare are the shared-corpus scores in section 1 and your own-corpus scores in section 4, with their intervals.
If you want them side by side, copy the rows you need into a table here and say that you copied them.

Did the winner change between the shared corpus and yours?
Why, or why not: what is different about the two collections (document length, vocabulary, identifiers, near-duplicates, how the queries were written), and which of your explanations did you test and which are guesses?
Say what 20 queries on one side and your gold-set size on the other cannot support.

The winner didn't change: re-rank was able to win on both. The things that actually changed are the other models. For example, on the shared set, BM25 had the lowest average, but on my set, BM25 had the highest of the three. But the difference among the three is not distinguishable on either of the corpuses. This could come down to a bunch of different things. Namely, the document length: the shared set had a median of 68 words, and only 13% of its sections are longer than one chunk; mine had a median of 340 words, and 58% are longer than one chunk. It could also come down to how the queries were worded. As the shared set had a 0.46 overall, and a 0.09 for paraphrasing. I had a 0.78 for overall and a 0.77 for paraphrases. While the Claude queries for mine had a 0.82 and my hand queries had a 0.67. Also, 32% of the shared sections nearly repeated another section. While 0% of the articles that I found do. The shared set has 2.00 relevant documents per query and mine has 1.45. The differences of these were measured, but none of them was tested as the cause; for example, the word overlap would explain why BM25 did much better on my corpus, which is not tested. The 20 shared queries can't support the separation of BM25, dense and hybrid, as the MDD is 0.27 to 0.41. Next, on the 31 queries re-rank has a ceiling of 1. The two corpuses have different queries, so you can't test whether BM25 did better on my corpus than on the shared one, besides just comparing the averages.

---

## 8. Stretch

498E: the stretch is one of the six options in the brief's "One stretch" section, and that section says what earns the 25 points for each.
It is optional, so `uv run p2 check --final` never waits on this section.
598E: the rider is your stretch, so write "rider" below and put its results in section 9; the other options add no points, because the project is capped at 150.

Whichever option you chose, write these five things:

1. The option's name.
2. What you did, and the files that hold it.
3. The table `p2 score` wrote for it, by name: one of the three below, `own-ablation` and `own-ablation-queries` in section 5 for a second ablation, `own-origins` in section 4 for the hand and claude queries, or `repeats` in section 9 for the rider.
4. What its interval lets you claim, and what it does not.
5. One thing you would do next, and what result would tell you it worked.

For a second ablation, write its hypothesis here before you run it, and commit it, so your history shows that it came first.
For the hand and claude queries, do the same with your prediction before you score.

### Claim-level faithfulness check (option 2)

Claude's verdicts from `p2 judge` against your own verdicts in the calibration file.

<!-- p2:begin stretch-judge -->
_No judged answers yet (stretch option 2): `uv run p2 judge answers/shared/LABEL.json` writes them, your own verdicts go in answers/shared/LABEL.calibration.tsv, and then `uv run p2 score` fills this table._
<!-- p2:end stretch-judge -->

### Cost and latency (option 3)

The Claude calls, tokens and seconds in every trace you committed, and what a cheaper system or answers file saves against what it loses.

<!-- p2:begin stretch-cost -->
Every trace in traces/ that records a Claude call:

| Trace | System | Spans | Claude calls | Saved | Input tokens | Output tokens | Seconds | Input per span | Output per span | Seconds per span |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| traces/answers-rerank.jsonl | rerank | 12 | 24 | 4 | 267,263 | 11,358 | 169.8 | 22,272 | 946 | 14.1 |
| traces/own-own-rerank.jsonl | rerank | 31 | 31 | 2 | 464,993 | 7,929 | 146.9 | 15,000 | 256 | 4.7 |
| traces/shared-practice-rerank.jsonl | rerank | 20 | 20 | 2 | 326,305 | 6,857 | 123.5 | 16,315 | 343 | 6.2 |
| traces/shared-practice-rerank_c10.jsonl | rerank_c10 | 20 | 20 | 2 | 271,507 | 4,201 | 97.3 | 13,575 | 210 | 4.9 |
| traces/shared-test-rerank.jsonl | rerank | 40 | 40 | 0 | 631,306 | 13,470 | 236.5 | 15,783 | 337 | 5.9 |

A span is one query of a run, one question of an answers file, or one claim of a judged file. A saved reply costs nothing now, so it counts the tokens and the seconds of the call that made it.

Every pair of systems on the same queries where at least one calls Claude, the one with fewer Claude input tokens per query first:

| Cheaper minus dearer | Queries | MRR@10 difference | 95% interval | Input tokens saved per query | Seconds saved per query | Reading |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| shared practice: bm25 minus rerank | 20 | -0.343 | [-0.576, -0.100] | 16,315 | 6.2 | rerank higher |
| shared practice: dense minus rerank | 20 | -0.287 | [-0.471, -0.117] | 16,315 | 6.2 | rerank higher |
| shared practice: hybrid minus rerank | 20 | -0.208 | [-0.392, -0.050] | 16,315 | 6.2 | rerank higher |
| shared practice: bm25 minus rerank_c10 | 20 | -0.348 | [-0.576, -0.115] | 13,575 | 4.9 | rerank_c10 higher |
| shared practice: dense minus rerank_c10 | 20 | -0.293 | [-0.476, -0.122] | 13,575 | 4.9 | rerank_c10 higher |
| shared practice: hybrid minus rerank_c10 | 20 | -0.214 | [-0.394, -0.058] | 13,575 | 4.9 | rerank_c10 higher |
| shared practice: rerank_c10 minus rerank | 20 | +0.006 | [+0.000, +0.017] | 2,740 | 1.3 | not distinguishable |
| own: bm25 minus rerank | 31 | -0.101 | [-0.205, -0.016] | 15,000 | 4.7 | rerank higher |
| own: dense minus rerank | 31 | -0.161 | [-0.274, -0.056] | 15,000 | 4.7 | rerank higher |
| own: hybrid minus rerank | 31 | -0.108 | [-0.204, -0.027] | 15,000 | 4.7 | rerank higher |

The difference is the cheaper system's score minus the dearer one's, with its paired interval; the savings count Claude calls only, so a system that makes none saves all of the other's.

Systems that do not call Claude, from traces/retrieval/ on the machine that last ran `p2 score` (git ignores that folder, so `p2 check` does not compare this part):

| Trace | System | Queries | Seconds | Milliseconds per query |
| --- | --- | ---: | ---: | ---: |
| traces/retrieval/own-own-ablation-dense_c100.jsonl | dense_c100 | 31 | 0.15 | 4.7 |
| traces/retrieval/own-own-bm25.jsonl | bm25 | 31 | 0.01 | 0.4 |
| traces/retrieval/own-own-dense.jsonl | dense | 31 | 0.14 | 4.7 |
| traces/retrieval/own-own-hybrid.jsonl | hybrid | 31 | 0.15 | 4.9 |
| traces/retrieval/shared-practice-bm25.jsonl | bm25 | 20 | 0.03 | 1.6 |
| traces/retrieval/shared-practice-dense.jsonl | dense | 20 | 0.16 | 7.9 |
| traces/retrieval/shared-practice-hybrid.jsonl | hybrid | 20 | 0.21 | 10.3 |
| traces/retrieval/shared-test-bm25.jsonl | bm25 | 40 | 0.06 | 1.6 |
| traces/retrieval/shared-test-dense.jsonl | dense | 40 | 0.24 | 5.9 |
| traces/retrieval/shared-test-hybrid.jsonl | hybrid | 40 | 0.45 | 11.1 |
<!-- p2:end stretch-cost -->

### The grep agent (option 5)

Your stretch run on some of your own queries against the four systems on the same queries.

<!-- p2:begin stretch-agent -->
_No stretch runs yet (stretch option 5): `uv run p2 run --corpus own --queries eval/own/agent.queries.tsv --system agent --stretch` writes one to runs/own/stretch/, then `uv run p2 score` fills this table._
<!-- p2:end stretch-agent -->

### Your stretch

Write the five things here.

---

## 9. 598E only - repeats and the pre-registered claim

498E students can leave this section as it is; nothing checks it.
598E students replace each line that starts with "598E: write", and `uv run p2 check --final` counts those lines as work still to do until they are gone.

### Repeats on the shared corpus

Three runs of the reranker on the practice queries, and three answers files, with their run-to-run spread and Wilson intervals.

<!-- p2:begin repeats -->
_No repeated runs or answers files yet (598E: `p2 run ... --repeat 3` and `p2 answer ... --repeat 3`)._
<!-- p2:end repeats -->

Does the reranker's gain over its first stage survive the run-to-run variation?
Write what the spread is, how it compares with the gain, and what the Wilson intervals on the verified share and the declined share say about 8 and 4 questions.

598E: write the repeats result here.

### The pre-registered claim

The claim, the smallest effect, the gold-set size and the test are in `PREREG.md`, committed before your own gold-set judgments.
Here, say whether you followed the plan, what the interval turned out to be, and what that means.
The outcome section of `PREREG.md` holds the short version.

598E: write the claim and its outcome here.
