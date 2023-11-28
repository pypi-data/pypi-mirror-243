#!/bin/bash

# shellcheck disable=SC2046
# shellcheck disable=SC2005
echo $(cat .gitignore) | xargs -t git restore
