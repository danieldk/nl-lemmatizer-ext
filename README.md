# `nl-lemmatizer-ext`

## Introduction

This packages contains extensions for Dutch lemmatization.

Pipelines:

- `gigant_lemmatizer`: a pipe that uses the GiGaNT-Molex lexicon for
  lemmatization.

CLI commands:

- `nl-lemmatizer-util convert`: convert GiGaNT-Molex TSV file to a
  JSON lexicon for the `gigant_lemmatizer` pipe.
- `nl-lemmatizer-util extend-model`: add the `gigant_lemmatizer` pipe
  to an existing pipeline.

## Adding the `gigant_lemmatizer` pipe to a pipeline

Install this package and get the
[GiGaNT-Molex](https://taalmaterialen.ivdnt.org/download/tstc-gigant-molex-c/)
dataset from Instituut voor de Nederlandse Taal.

First convert the tab-separated file from the dataset:

```shell
nl-lemmatizer-util convert molex_22_02_2022.tsv/molex_22_02_2022.tsv gigant-molex.json
```

Then add the `gigant-molex` pipe to an existing pipeline:

```shell
nl-lemmatizer-util extend-pipeline nl_core_news_lg gigant-molex.json nl_core_news_gigant
```
