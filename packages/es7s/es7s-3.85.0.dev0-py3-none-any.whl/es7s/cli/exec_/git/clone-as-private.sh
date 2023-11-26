#!/bin/bash
#-------------------------------------------------------------------------------
# es7s/core | git repo full-copy utility
# (c) 2022-2023 A. Shavykin <0.delameter@gmail.com>
#-------------------------------------------------------------------------------
declare SELF="${0##*/}"

__usage() {
    echo "USAGE:"
    echo "  $SELF SRC_REPO [DST_REPO]"
    echo
    echo "TL;DR:"
    echo "  MAKE A FULL CLONE OF REMOTE REPO WITHOUT FORKING"
    echo
    echo "DESCRIPTION:"
    echo "  Clone the (remote) SRC_REPO locally, make a private empty "
    echo "  repo on github, sync that repo with fresh local copy by "
    echo "  pushing all branches and tags."
    echo
    echo "  Requires installed gh-cli: https://cli.github.com/"
    echo "  which should be configured (i.e., you should be logged in)."
    echo "  That's a requirement for creating a private repo the source "
    echo "  will be cloned into."
    echo
    echo "  The utility doesn't write anything to persistent storage, as "
    echo "  it works in a temporary directory which is purged afterwards."
    echo
    echo "ARGUMENTS:"
    echo "  SRC_REPO    Remote repo in format 'OWNER/NAME', the original"
    echo "              one that will be cloned."
    echo "  DST_REPO    Target repo in format '[OWNER/]NAME' that will be"
    echo "              created automatically and pushed the clone commits "
    echo "              into. If omitted, NAME will be same as of SRC_REPO,"
    echo "              and OWNER will be the default account that you "
    echo "              logged into with gh-cli."
    echo
    echo "EXAMPLE:"
    echo "  $SELF k3a/telegram-emoji-list tg-emoji-list"
    echo
    echo "  which will result in a clone of 'k3a/telegram-emoji-list' repo "
    echo "  placed in '<YOUR_ACCOUNT>/tg-emoji-list' as a private independent "
    echo "  repository (i.e., it will not be a fork of the original one)."
    echo
}
__call() {
    __printcmd ">" "$*"
    __run "$@" || {
        local ex=$?
        echo "Terminating (code $ex)" | __pperr
        exit $ex
    }
}
__callwe(){
    __printcmd "»" "$*"
    __run "$@" || {
        local ex=$?
        echo "Subprocess exited with code $ex" | __ppwarn
    }
}
__callck(){
    __printcmd "?" "$*"
    __run "$@" &>/dev/null
}
__printcmd(){
    local ico="${1:->}"
    shift
    printf "\e[94;1m $ico\e[;34;2m %s\e[m\n" "$*"
}
__ppout () { sed --unbuffered -Ee $'s/^/   /' ; }
__pperx () { sed --unbuffered -Ee $'s/^.+$/\e[2m   &\e[m/' ; }
__pperr () { sed --unbuffered -Ee $'s/^.+$/\e[31m   &\e[m/' ; }
__ppwarn () { sed --unbuffered -Ee $'s/^.+$/\e[33m   &\e[m/' ; }
__run() {
    "$@" 2> >(__pperx) > >(__ppout)
}
__max_len() {
    local result=0
    for var in $* ; do
        result=$(( $result < ${#var} ? ${#var} : $result ))
    done
    echo $result
}
__sep() {
    printf "\e[2m%$((5+$max_len))s\e[m\n" "" | tr " " -
}
__print_repos() {
    printf "\e[1m%7s  \e[%dm%7s\e[;37;2m %-.60s\e[m\n" "$@"
}
__main() {
    local upstream_repo="${1:?Repo in format OWNER/NAME required}"
    [[ $upstream_repo =~ : ]] || upstream_repo="git@github.com:$upstream_repo"

    local upstream_repo_url="${upstream_repo/://}"
    upstream_repo_url="https://${upstream_repo_url/#*@/}"

    local upstream_repo_name="$(sed -Ee 's|^.+/(.+)$|\1|; s|\.git$||' <<< "$upstream_repo")"

    local target_repo_name="${2:-$upstream_repo_name}"
    local target_repo_gh="$(printf "${ES7S_REPO_DIST_GH_TPL:-}" "${2:-$target_repo_name}")"
    local target_repo_glab="$(printf "${ES7S_REPO_DIST_GLAB_TPL:-}" "${2:-$target_repo_name}")"
    local target_repo_glab_ns="$(printf "${ES7S_REPO_DIST_GLAB_TPL:-}" "")"
    local max_len=$(__max_len "$upstream_repo" "$target_repo_gh" "$target_repo_glab")

    __print_repos "" 36 source "$upstream_repo"
    [[ -n "$target_repo_gh" ]]   && __print_repos ""  35 destin1 "$target_repo_gh"
    [[ -n "$target_repo_glab" ]] && __print_repos ""  35 destin2 "$target_repo_glab"
    __sep

    __call mkdir -p /tmp/gpf
    __call pushd /tmp/gpf

    __call rm -rf "$target_repo_name"
    __call git clone "$upstream_repo" "$target_repo_name"  # "--mirror", when gitlab-cli will recognize bare repos
    __call pushd "$target_repo_name"

    local branch="$(git branch --show)"
    local upstream_commits="$(git log --oneline "$branch" | wc -l)"
    __call git remote remove origin

    local origin_name="${ES7S_REPO_REMOTE_ORIGIN_NAME:-origin}"
    local backup_name="${ES7S_REPO_REMOTE_BACKUP_NAME:-backup}"

    local origin_url="git@github.com:$target_repo_gh"
    local backup_url="git@gitlab.com:$target_repo_glab"

    if [[ -n "$target_repo_gh" ]] ; then
        local gh_repo_created_now
        if ! command -v gh &>/dev/null ; then
            echo -e "\e[33mgithub-cli (gh) not found in PATH\e[m" | __ppout
        elif __callck gh repo view "$target_repo_gh" ; then
            echo -e "Repo already exists: \e[1m$target_repo_gh\e[m" | __ppout
        else
            __call gh repo create "$target_repo_gh" --private
            gh_repo_created_now=true
        fi
        __call git remote add "$origin_name" "$origin_url"
        __call git push "$origin_name" --all
        __call git push "$origin_name" --tags
        [[ -n $gh_repo_created_now ]] && __callwe gh repo edit --homepage "$upstream_repo_url"
    fi

    if [[ -n "$target_repo_glab" ]] ; then
        if ! command -v glab &>/dev/null ; then
            echo -e "\e[33mgitlab-cli (glab) not found in PATH\e[m" | __ppout
        elif __callck glab repo view "$target_repo_glab" ; then
            echo -e "Repo already exists: \e[1m$target_repo_glab\e[m" | __ppout
        else
            __call glab repo create "$target_repo_name" \
                    -g "${target_repo_glab_ns/%\//}" \
                    --private
        fi
        __call git remote add "$backup_name" "$backup_url"
        __call git push "$backup_name" --all
        __call git push "$backup_name" --tags
    fi

    __sep
    printf "\e[97;1mCOMMITS\e[m\n"
    __print_repos \
        "$upstream_commits"                                   36 source  "$upstream_repo" \
        "$(git log --oneline "$branch" | wc -l)"              39 local   "$(pwd)" \
        "$(git log --oneline "$origin_name/$branch" | wc -l)" 35 destin1 "$origin_url" \
        "$(git log --oneline "$backup_name/$branch" | wc -l)" 35 destin2 "$backup_url"

    __call popd
    __call rm -rf "$target_repo_name"
    __call popd

    echo -e "\e[32;1mDone\e[m"
}

[[ $* =~ ^--?h(elp)? || $# -eq 0 ]] && __usage && exit
# -@temp---------------------------
ES7S_REPO_DIST_GH_TPL=dl-dist/%s
ES7S_REPO_DIST_GLAB_TPL=dp3.dl/import/dist/%s
#ES7S_REPO_REMOTE_ORIGIN_NAME=dp3
ES7S_REPO_REMOTE_ORIGIN_NAME=origin
ES7S_REPO_REMOTE_BACKUP_NAME=dp3
# -@temp---------------------------
__main "$@"
