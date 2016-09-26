#!/bin/bash

if [ $(uname) == "Darwin" ]
then
    alias xarg=gxarg
fi

pre-commit.git-lint.sh

