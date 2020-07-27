#!/bin/bash

wget "http://mattnappo.com/columbia_data/nltk_data.zip"
mkdir ~/nltk_data/
unzip nltk_data.zip ~/nltk_data/

wget "http://mattnappo.com/columbia_data/stanford_zipped.zip"
unzip stanford_zipped.zip ./stanford-corenlp-latest
