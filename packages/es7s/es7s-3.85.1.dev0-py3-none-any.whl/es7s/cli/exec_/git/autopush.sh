#!/bin/bash
#-------------------------------------------------------------------------------
# es7s/core | auto-commit changes, set upstream to current branch and push
# (c) 2023 A. Shavykin <0.delameter@gmail.com>
#-------------------------------------------------------------------------------

function es7s.__cmd() { printf "\e[34m> $*\e[m"$'\n' >&2 ; logger <<< "$@" -t es7s/shell -p local7.info ; }
function es7s.call() { es7s.__cmd "$@" ; "$@" ; }
function es7s.prompt() { es7s.__cmd "$@" ; read -n1 -p "Continue? (^C to abort): " ; "$@" ; }

_make_msg() {
    [[ $# -gt 0 ]] && echo "$*" && return

    echo "Automatic delivery $(date "+%-e-%b-%y %R")"
    echo # <<< you need two line breaks in a row or else git will remove all of them
    git diff --staged --shortstat --color=never
}
_main() {
    set -e
    local gitbranch="$(git branch --show-current 2>/dev/null)"

    git add .
    _make_msg "$@" | git commit -F -
    es7s.prompt git push --set-upstream "origin" "$gitbranch"
}

#export GIT_COMMITTER_NAME="sunlightd"
#export GIT_COMMITTER_EMAIL="sunlightd@localhost"
# export GIT_COMMITTER_DATE="$(date --iso-8601=seconds -d 20:00:00)"
# export GIT_AUTHOR_DATE="$GIT_COMMITTER_DATE"
export LC_TIME=en_US.UTF-8

[[ $* =~ (--)?help ]] && echo "USAGE: $0 [COMMIT_MSG...]" && exit
_main "$@"
