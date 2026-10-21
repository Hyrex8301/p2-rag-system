# Ingest report

Written by `uv run p2 ingest`.
It lists every document in this corpus that ingest added, with what the cleaning pass did and anything that looks wrong.
Running ingest again adds to the table and replaces the "last run" section, and `uv run p2 ingest --report` rewrites it for the documents in docs/ now, after you removed some.

## Summary

- Documents: 278 (the final check needs at least 200)
- Words: 162,058
- Estimated tokens (words times 1.4): 226,881 (`p2 check` warns above 800,000 and fails above 1,000,000)
- Flagged documents: 0

## Documents

| docid | words | characters per page | flags | cleaning |
|---|---:|---:|---|---|
| `adobe-creek-reservoir` | 253 | - | - | - |
| `alpine-tunnel` | 564 | - | - | - |
| `american-discovery-trail` | 1,853 | - | - | - |
| `arapahoe-basin` | 1,953 | - | - | - |
| `argentine-pass` | 1,121 | - | - | - |
| `arkansas-headwaters-recreation-area` | 333 | - | - | - |
| `aspen-colorado` | 2,798 | - | - | - |
| `aspen-highlands` | 821 | - | - | - |
| `aspen-mountain-ski-area` | 873 | - | - | - |
| `aspen-snowmass` | 159 | - | - | - |
| `baker-mountain-colorado` | 233 | - | - | - |
| `barr-trail` | 478 | - | - | - |
| `beaver-creek-resort` | 913 | - | - | - |
| `berthoud-pass` | 883 | - | - | - |
| `big-meadows-reservoir` | 259 | - | - | - |
| `birds-of-prey-ski-course` | 773 | - | - | - |
| `black-canyon-of-the-gunnison-national-park` | 2,967 | - | - | - |
| `black-ridge-canyons-wilderness` | 632 | - | - | - |
| `blanca-peak` | 842 | - | - | - |
| `blue-creek-canyon` | 267 | - | - | - |
| `blue-mesa-summit` | 193 | - | - | - |
| `blue-sky-basin` | 179 | - | - | - |
| `bluff-lake-nature-center` | 184 | - | - | - |
| `boreas-pass` | 558 | - | - | - |
| `breckenridge-ski-resort` | 4,167 | - | - | - |
| `browns-canyon-national-monument` | 492 | - | - | - |
| `buttermilk-ski-area` | 208 | - | - | - |
| `cameo-shooting-and-education-complex` | 166 | - | - | - |
| `cameron-pass` | 333 | - | - | - |
| `camp-hale` | 1,624 | - | - | - |
| `canyons-of-the-ancients-national-monument` | 2,342 | - | - | - |
| `capitol-peak-colorado` | 596 | - | - | - |
| `castle-peak-colorado` | 331 | - | - | - |
| `castlewood-canyon-state-park` | 352 | - | - | - |
| `cerro-summit` | 182 | - | - | - |
| `challenger-point` | 211 | - | - | - |
| `chatfield-state-park` | 309 | - | - | - |
| `cherry-creek-state-park` | 223 | - | - | - |
| `cheyenne-mountain-state-park` | 387 | - | - | - |
| `chiefs-head-peak` | 213 | - | - | - |
| `chimney-rock-national-monument` | 1,305 | - | - | - |
| `clear-creek-colorado` | 447 | - | - | - |
| `cochetopa-pass` | 363 | - | - | - |
| `collegiate-peaks-wilderness` | 667 | - | - | - |
| `colorado-parks-and-wildlife` | 701 | - | - | - |
| `colorado-trail` | 945 | - | - | - |
| `continental-divide-trail` | 3,883 | - | - | - |
| `copper-mountain-colorado` | 1,322 | - | - | - |
| `cordova-pass` | 288 | - | - | - |
| `cottonwood-pass` | 417 | - | - | - |
| `crested-butte-mountain-resort` | 684 | - | - | - |
| `crestone-needle` | 285 | - | - | - |
| `crestone-peak` | 506 | - | - | - |
| `crestones` | 238 | - | - | - |
| `cucharas-river` | 240 | - | - | - |
| `culebra-peak` | 185 | - | - | - |
| `cumberland-pass` | 209 | - | - | - |
| `cumbres-pass` | 376 | - | - | - |
| `dallas-divide` | 165 | - | - | - |
| `de-beque-canyon` | 169 | - | - | - |
| `deer-creek-trail-colorado` | 453 | - | - | - |
| `douglas-pass` | 197 | - | - | - |
| `eagles-nest-wilderness` | 479 | - | - | - |
| `east-inlet-trail` | 212 | - | - | - |
| `echo-lake-park` | 299 | - | - | - |
| `echo-mountain-ski-area` | 425 | - | - | - |
| `eldora-mountain-resort` | 1,034 | - | - | - |
| `eldorado-canyon-state-park` | 499 | - | - | - |
| `eleven-mile-state-park` | 403 | - | - | - |
| `elkhead-reservoir-state-park` | 184 | - | - | - |
| `ellingwood-point` | 211 | - | - | - |
| `englemann-canyon` | 454 | - | - | - |
| `escalante-canyon` | 204 | - | - | - |
| `fall-river-pass` | 223 | - | - | - |
| `fishers-peak-state-park` | 538 | - | - | - |
| `flat-tops-wilderness-area` | 664 | - | - | - |
| `fourmile-canyon` | 991 | - | - | - |
| `fremont-pass-colorado` | 321 | - | - | - |
| `geneva-basin-ski-area` | 693 | - | - | - |
| `glenwood-canyon` | 403 | - | - | - |
| `goose-creek-south-platte-river` | 291 | - | - | - |
| `gore-canyon` | 482 | - | - | - |
| `gore-pass` | 244 | - | - | - |
| `grand-lake-colorado` | 330 | - | - | - |
| `grays-peak` | 484 | - | - | - |
| `grays-peak-trail` | 345 | - | - | - |
| `great-western-loop` | 340 | - | - | - |
| `green-knoll` | 180 | - | - | - |
| `grizzly-reservoir` | 447 | - | - | - |
| `guanella-pass` | 281 | - | - | - |
| `guffey-gorge-colorado` | 181 | - | - | - |
| `gunsight-pass` | 246 | - | - | - |
| `hagerman-pass` | 238 | - | - | - |
| `hallett-peak` | 296 | - | - | - |
| `hanging-lake` | 769 | - | - | - |
| `hayden-spire` | 257 | - | - | - |
| `heritage-square-golden-colorado` | 800 | - | - | - |
| `hermosa-creek-wilderness` | 616 | - | - | - |
| `hesperus-ski-area` | 186 | - | - | - |
| `hidden-valley-ski-estes-park` | 274 | - | - | - |
| `high-line-canal` | 817 | - | - | - |
| `holy-cross-wilderness` | 255 | - | - | - |
| `hoosier-pass` | 432 | - | - | - |
| `howard-mountain` | 309 | - | - | - |
| `howelsen-hill-ski-area` | 361 | - | - | - |
| `humboldt-peak-colorado` | 216 | - | - | - |
| `huron-peak` | 354 | - | - | - |
| `imogene-pass` | 235 | - | - | - |
| `independence-pass` | 3,967 | - | - | - |
| `indian-peaks-wilderness` | 909 | - | - | - |
| `john-martin-reservoir-state-park` | 186 | - | - | - |
| `kannah-creek` | 504 | - | - | - |
| `kendall-mountain-ski-area` | 161 | - | - | - |
| `kenosha-pass` | 785 | - | - | - |
| `keystone-resort` | 1,527 | - | - | - |
| `kit-carson-peak` | 601 | - | - | - |
| `la-garita-wilderness` | 175 | - | - | - |
| `la-plata-peak` | 273 | - | - | - |
| `la-poudre-pass` | 278 | - | - | - |
| `la-veta-pass` | 302 | - | - | - |
| `lake-pueblo-state-park` | 395 | - | - | - |
| `lake-san-cristobal` | 449 | - | - | - |
| `lathrop-state-park` | 230 | - | - | - |
| `lead-mountain-grand-county-colorado` | 229 | - | - | - |
| `left-hand-creek-colorado` | 429 | - | - | - |
| `list-of-colorado-fourteeners` | 208 | - | - | - |
| `list-of-colorado-ski-resorts` | 250 | - | - | - |
| `list-of-lakes-of-colorado` | 1,133 | - | - | - |
| `little-bear-peak` | 373 | - | - | - |
| `lizard-head-wilderness` | 165 | - | - | - |
| `lizard-lake-gunnison-county` | 183 | - | - | - |
| `longs-peak` | 1,881 | - | - | - |
| `los-pinos-pass` | 366 | - | - | - |
| `lost-creek-wilderness` | 365 | - | - | - |
| `lost-man-reservoir` | 159 | - | - | - |
| `loveland-pass` | 567 | - | - | - |
| `loveland-ski-area` | 1,283 | - | - | - |
| `lulu-mountain` | 323 | - | - | - |
| `maroon-bells` | 967 | - | - | - |
| `marshall-pass` | 607 | - | - | - |
| `mcclure-pass` | 210 | - | - | - |
| `mchenrys-peak` | 235 | - | - | - |
| `mcinnis-canyons-national-conservation-area` | 375 | - | - | - |
| `milner-pass` | 249 | - | - | - |
| `mineral-belt-national-recreation-trail` | 213 | - | - | - |
| `moffat-tunnel` | 1,898 | - | - | - |
| `monarch-mountain-ski-area` | 659 | - | - | - |
| `monarch-pass` | 879 | - | - | - |
| `mosca-pass` | 180 | - | - | - |
| `mount-antero` | 304 | - | - | - |
| `mount-bierstadt` | 339 | - | - | - |
| `mount-blue-sky` | 3,073 | - | - | - |
| `mount-chapin` | 269 | - | - | - |
| `mount-cirrus` | 369 | - | - | - |
| `mount-columbia-colorado` | 166 | - | - | - |
| `mount-craig-colorado` | 196 | - | - | - |
| `mount-cumulus` | 327 | - | - | - |
| `mount-democrat` | 772 | - | - | - |
| `mount-elbert` | 1,289 | - | - | - |
| `mount-eolus` | 210 | - | - | - |
| `mount-evans-wilderness` | 175 | - | - | - |
| `mount-harvard` | 547 | - | - | - |
| `mount-lincoln-colorado` | 295 | - | - | - |
| `mount-massive` | 368 | - | - | - |
| `mount-massive-wilderness` | 303 | - | - | - |
| `mount-meeker` | 198 | - | - | - |
| `mount-nimbus` | 290 | - | - | - |
| `mount-of-the-holy-cross` | 652 | - | - | - |
| `mount-princeton` | 190 | - | - | - |
| `mount-richthofen` | 215 | - | - | - |
| `mount-shavano` | 183 | - | - | - |
| `mount-sherman` | 243 | - | - | - |
| `mount-sneffels` | 269 | - | - | - |
| `mount-stratus` | 254 | - | - | - |
| `mount-wilson-colorado` | 512 | - | - | - |
| `mount-yale` | 342 | - | - | - |
| `mount-zirkel-wilderness` | 749 | - | - | - |
| `muddy-pass-continental-divide` | 213 | - | - | - |
| `napoleon-pass` | 283 | - | - | - |
| `navajo-state-park` | 548 | - | - | - |
| `never-summer-wilderness` | 503 | - | - | - |
| `north-pass` | 518 | - | - | - |
| `north-sterling-state-park` | 279 | - | - | - |
| `northgate-canyon` | 828 | - | - | - |
| `ohio-pass` | 189 | - | - | - |
| `old-monarch-pass` | 258 | - | - | - |
| `original-monarch-pass` | 325 | - | - | - |
| `otis-peak` | 262 | - | - | - |
| `pagoda-mountain` | 183 | - | - | - |
| `painted-canyon-purgatoire-river` | 298 | - | - | - |
| `paonia-state-park` | 191 | - | - | - |
| `pearl-lake-state-park` | 253 | - | - | - |
| `picture-canyon-colorado` | 606 | - | - | - |
| `pikes-peak` | 2,396 | - | - | - |
| `pikes-peak-greenway` | 544 | - | - | - |
| `platte-canyon` | 373 | - | - | - |
| `platte-river-wilderness` | 179 | - | - | - |
| `poncha-pass` | 196 | - | - | - |
| `poudre-canyon` | 1,186 | - | - | - |
| `powderhorn-resort` | 649 | - | - | - |
| `powderhorn-wilderness` | 720 | - | - | - |
| `purgatory-resort` | 363 | - | - | - |
| `pyramid-peak-colorado` | 243 | - | - | - |
| `quandary-peak` | 231 | - | - | - |
| `rabbit-ears-pass` | 1,221 | - | - | - |
| `raton-pass` | 550 | - | - | - |
| `rattlesnake-canyon-colorado` | 240 | - | - | - |
| `rawah-wilderness` | 188 | - | - | - |
| `red-mountain-pass` | 313 | - | - | - |
| `ridgway-state-park` | 249 | - | - | - |
| `rifle-falls-state-park` | 211 | - | - | - |
| `rollins-pass` | 5,904 | - | - | - |
| `roxborough-state-park` | 360 | - | - | - |
| `royal-gorge` | 1,113 | - | - | - |
| `ruby-hill-terrain-park` | 643 | - | - | - |
| `runyon-lake` | 153 | - | - | - |
| `sangre-de-cristo-wilderness` | 601 | - | - | - |
| `schofield-pass` | 181 | - | - | - |
| `serpents-trail` | 252 | - | - | - |
| `shrine-pass` | 247 | - | - | - |
| `silverton-mountain` | 566 | - | - | - |
| `ski-cooper` | 355 | - | - | - |
| `ski-idlewild` | 604 | - | - | - |
| `sloan-lake-colorado` | 972 | - | - | - |
| `slumgullion-pass` | 333 | - | - | - |
| `snowmass-lake` | 161 | - | - | - |
| `snowmass-mountain` | 300 | - | - | - |
| `south-cheyenne-ca-on` | 998 | - | - | - |
| `spanish-peaks-wilderness` | 375 | - | - | - |
| `spinney-mountain-state-park` | 155 | - | - | - |
| `sprague-mountain` | 229 | - | - | - |
| `spring-creek-pass` | 179 | - | - | - |
| `spring-gulch` | 197 | - | - | - |
| `st-vrain-state-park` | 2,259 | - | - | - |
| `stagecoach-colorado` | 268 | - | - | - |
| `stapp-lakes` | 450 | - | - | - |
| `staunton-state-park` | 240 | - | - | - |
| `steamboat-lake-state-park` | 218 | - | - | - |
| `steamboat-ski-resort` | 859 | - | - | - |
| `stones-peak` | 251 | - | - | - |
| `summit-lake-park` | 233 | - | - | - |
| `summit-reservoir` | 288 | - | - | - |
| `sunlight-peak` | 222 | - | - | - |
| `sunlight-ski-area` | 163 | - | - | - |
| `sunshine-peak` | 196 | - | - | - |
| `sweetwater-lake-state-park` | 1,483 | - | - | - |
| `switzerland-trail` | 680 | - | - | - |
| `tabeguache-peak` | 168 | - | - | - |
| `telluride-ski-resort` | 867 | - | - | - |
| `tennessee-pass` | 1,891 | - | - | - |
| `terra-tomah-mountain` | 310 | - | - | - |
| `thatchtop` | 193 | - | - | - |
| `the-sharkstooth` | 175 | - | - | - |
| `tomichi-pass` | 281 | - | - | - |
| `torreys-peak` | 404 | - | - | - |
| `trappers-lake` | 269 | - | - | - |
| `trout-creek-pass` | 305 | - | - | - |
| `trout-lake-colorado` | 842 | - | - | - |
| `twin-lakes-lake-county-colorado` | 431 | - | - | - |
| `twin-sisters-peaks` | 235 | - | - | - |
| `unaweep-canyon` | 403 | - | - | - |
| `uncompahgre-peak` | 392 | - | - | - |
| `uncompahgre-wilderness` | 240 | - | - | - |
| `ute-pass` | 617 | - | - | - |
| `vail-pass` | 392 | - | - | - |
| `vail-resorts` | 879 | - | - | - |
| `vail-ski-resort` | 2,272 | - | - | - |
| `vega-state-park` | 887 | - | - | - |
| `wagon-wheel-gap-colorado` | 305 | - | - | - |
| `weminuche-wilderness` | 1,231 | - | - | - |
| `west-encore-rosis-run` | 433 | - | - | - |
| `wetterhorn-peak` | 226 | - | - | - |
| `willow-creek-pass-colorado` | 199 | - | - | - |
| `wilson-peak` | 656 | - | - | - |
| `windom-peak` | 173 | - | - | - |
| `winter-park-resort` | 963 | - | - | - |
| `wolf-creek-pass` | 882 | - | - | - |
| `wolf-creek-ski-area` | 2,012 | - | - | - |

## Not added in the last run

Nothing was left out.

## What to check by eye

Ingest cleans text by rules, and rules miss things.
Take five minutes to open the shortest, a middle one and the longest document next to its original and read one page of each.

- Search the documents for `þ`, `¼`, `(cid:` and the replacement character.
  A hit usually means the PDF's font map is wrong, which no tool can repair, so treat it as a defect and leave that document out.
- Look at the end of a few papers.
  Ingest drops a trailing reference list when it finds a References heading or a run of numbered entries.
  A paper whose list has neither can keep it, and then every author and journal name matches queries it should not.
- Open the first lines of a few documents.
  Author lists, copyright pages and tables of contents are not removed automatically, and you may want to cut them.
- Compare one table with the PDF.
  A PDF prints footnote marks as small raised digits, and the converter glues them onto the word or number next to them: `ALUMINUM1` is the heading ALUMINUM with footnote 1, and `11210,000` can be 210,000 with footnote 11.
  Quotes still match the stored text, but a number read from it can be wrong, so check before you trust a figure in a query, a judgment or an answer.
- Fix the `license` column in the manifest for every document, then run `uv run p2 license`.
  It is `unknown` until you do, and `unknown` does not pass.

## If a document is flagged as scanned

A scan is a picture of a page, so there is no text for ingest to read.
This template does not install an OCR tool, because it is large and most students never need it.
If you do need one, the opt-in route is pymupdf4llm with rapidocr, run on its own outside the template's environment:

```
uv run --no-project --with pymupdf4llm --with rapidocr python -c "import pymupdf4llm, sys, pathlib; pathlib.Path(sys.argv[2]).write_text(pymupdf4llm.to_markdown(sys.argv[1], use_ocr=True, force_ocr=True), encoding='utf-8')" scan.pdf scan.md
```

Put the resulting `.md` file in your folder and ingest the folder again.
It costs about 2 seconds a page, and OCR text needs a second look: it misreads ligatures, hyphens and numbers.
pymupdf4llm is AGPL-3.0 software, so use it only as a tool on your own machine, and do not add it to this repo's dependencies or copy its code into the repo.
