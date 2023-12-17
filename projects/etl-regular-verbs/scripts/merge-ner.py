#!/usr/bin/env python3

import argparse

import spacy


parser = argparse.ArgumentParser(
    prog="merge-ner", description="Merge spaCy NER model into trained pipeline"
)
parser.add_argument("pipeline")
parser.add_argument("ner_pipeline")
parser.add_argument("output")

if __name__ == "__main__":
    args = parser.parse_args()
    nlp = spacy.load(args.pipeline)
    nlp_ner = spacy.load(args.ner_pipeline)

    # NER uses an embedded tok2vec model, so we can safely add the pipe
    # to another pipeline.
    nlp.add_pipe("ner", source=nlp_ner)

    nlp.to_disk(args.output)
