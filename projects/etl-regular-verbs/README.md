<!-- WEASEL: AUTO-GENERATED DOCS START (do not remove) -->

# 🪐 Weasel Project: Train the lemmatizer without irregular verb inflections

This project creates a pipeline that uses lookup-based lemmatization for inflections that are in the GiGaNT-Molex lexicon and the edit tree lemmatizer for word forms that are not in GiGaNT-Molex. Additionally, the edit tree lemmatizer is trained without verbs that have an irregular inflection paradigm.
Two assets need to be placed in the `assets` directory by hand to use this project. `molex_22_02_2022.tsv` from [GiGaNT-Molex](https://taalmaterialen.ivdnt.org/download/tstc-gigant-molex-c/) and `rbn.sql` from [Referentiebestand Nederlands](https://taalmaterialen.ivdnt.org/download/tstc-referentiebestand-nederlands/).


## 📋 project.yml

The [`project.yml`](project.yml) defines the data assets required by the
project, as well as the available commands and workflows. For details, see the
[Weasel documentation](https://github.com/explosion/weasel).

### ⏯ Commands

The following commands are defined by the project. They
can be executed using [`weasel run [name]`](https://github.com/explosion/weasel/tree/main/docs/cli.md#rocket-run).
Commands are only re-run if their inputs have changed.

| Command | Description |
| --- | --- |
| `unpack-model` | Unpack spaCy model to source word vectors and NER from |
| `convert-rbn` | Convert Referentiebestand Nederlands |
| `convert-gigant-molex` | Convert GiGaNT-Molex |
| `remove-lemma-underscores` | Remove underscores from lemmas |
| `convert-lassysmall` | Convert Lassy Small data to spaCy format |
| `train` | Train the pipeline |
| `merge-ner` | Merge NER components from the upstream spacy pipeline |
| `extend-lemmatizer` | Extend the lemmatizer with the GiGaNT-Molex lemmatizer |
| `evaluate` | Evaluate the pipeline on the dev corpus. |

### ⏭ Workflows

The following workflows are defined by the project. They
can be executed using [`weasel run [name]`](https://github.com/explosion/weasel/tree/main/docs/cli.md#rocket-run)
and will run the specified commands in order. Commands are only re-run if their
inputs have changed.

| Workflow | Steps |
| --- | --- |
| `all` | `unpack-model` &rarr; `convert-rbn` &rarr; `convert-gigant-molex` &rarr; `remove-lemma-underscores` &rarr; `convert-lassysmall` &rarr; `train` &rarr; `merge-ner` &rarr; `extend-lemmatizer` &rarr; `evaluate` |

### 🗂 Assets

The following assets are defined by the project. They can
be fetched by running [`weasel assets`](https://github.com/explosion/weasel/tree/main/docs/cli.md#open_file_folder-assets)
in the project directory.

| File | Source | Description |
| --- | --- | --- |
| `assets/UD_Dutch-Alpino` | Git |  |
| `assets/UD_Dutch-LassySmall` | Git |  |
| `assets/models/nl_core_news_lg-3.7.0.tar.gz` | URL | spaCy model to source NER from |

<!-- WEASEL: AUTO-GENERATED DOCS END (do not remove) -->
