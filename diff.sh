#!/usr/bin/env bash

for i in `git ls-files`
do
  if [[ $i == "proposal.tex" ]]; then
    continue
  fi
  if [[ $i == ".gitignore" ]]; then
    continue
  fi
  diff -uw $PWD/$i $1/$i
done
