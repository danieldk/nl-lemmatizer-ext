#!/usr/bin/env python3

import argparse

from conllu import parse_incr

parser = argparse.ArgumentParser(
    prog="remove_lemma_underscores", description="Remove underscores from lemmas"
)
parser.add_argument("input")
parser.add_argument("output")

if __name__ == "__main__":
    args = parser.parse_args()
    with open(args.input, "r", encoding="utf-8") as f:
        with open(args.output, "w", encoding="utf-8") as f_out:
            for tokens in parse_incr(f):
                for token in tokens:
                    # Ideally we'd want to do some string alignment here
                    # to handle multiple dashes or underscores. But it's
                    # not worth the effort for the small number of cases.
                    form = token["form"]
                    lemma = token["lemma"]
                    if "-" in form:
                        token["lemma"] = lemma.replace("_", "-")
                    elif "_" not in form:
                        token["lemma"] = lemma.replace("_", "")

                f_out.write(tokens.serialize())
