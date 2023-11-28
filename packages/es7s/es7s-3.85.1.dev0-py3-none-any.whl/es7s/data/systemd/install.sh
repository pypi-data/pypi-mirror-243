#!/bin/bash
#-------------------------------------------------------------------------------
# es7s/core
# (c) 2023 A. Shavykin <0.delameter@gmail.com>
#-------------------------------------------------------------------------------
# shellcheck disable=SC2059

.f() { printf "\e[%sm" "$(tr -s ' ' \; <<<"$*")"; }
.fsudo() { .f 38 2 248 184 137 ; }
.r() { .f 0 ; }

declare -A DEST_PATHS=(
  [global]=/etc/systemd/system
  [user]=$HOME/.config/systemd/user
)

declare -a SYSTEMD_PATHS=(
    /usr/local/lib/systemd/system
    /usr/lib/systemd/system
    "${DEST_PATHS[*]}"
)

declare -a SERVICES
declare services_num=0

__main() {
    # shellcheck disable=SC2178
    SERVICES=$(__find_services)
    services_num=$(wc -w <<<"${SERVICES[*]}")

    printf "Services found: $(.f 1)%s$(.r)\n" "$services_num"

    __uninstall
    __install

    printf "$(.f 32 1)DONE$(.r)\n"
}

__find_services() {
    local source_path="$(dirname "$(realpath "${BASH_SOURCE[0]}")")"
    find "$source_path" -type f \
        -regextype posix-extended \
        -regex '.+\.(service|target)' \
        -print0 |
        xargs -0 -n1 |
        sort -k1n -t.
}

__uninstall() {
    printf "$(.fsudo)Uninstall$(.r) current $(.f 1)es7s$(.r) services?"
    __prompt || return

    for svc_path in ${SERVICES[*]}; do
        __uninstall_service "$svc_path"
    done

    (scope=user   ; __systemctl daemon-reload)
    (scope=global ; __systemctl daemon-reload)
    (scope=global ; __systemctl  reset-failed)
}
__uninstall_service() {
    local svc_path="${1:?Required}"
    local svc_file="$(basename "$svc_path")"
    local svc_name="${svc_file#*.}"
    local scope=$(__get_scope "$svc_path")

    printf "Uninstalling $(.f 1)%s$(.r) ($scope)\n" "$svc_name"
#    __prompt || return 0

    set -e
    if __systemctlq is-active "$svc_name"; then
       __systemctl stop "$svc_name"
    fi
    if __systemctlq is-enabled "$svc_name"; then
       __systemctl disable "$svc_name"
    fi

    for systemd_path in ${SYSTEMD_PATHS[*]}; do
        local realpath="$systemd_path/$svc_name"
        [[ -f "$realpath" ]] && __call rm "$realpath"
    done
    set +e
}

__install() {
    local idx=1
    for svc_path in ${SERVICES[*]}; do
        __install_service "$svc_path" "$((idx++))"
    done
    (scope=user   ; __systemctl daemon-reload)
    (scope=global ; __systemctl daemon-reload)
}
__install_service() {
    local svc_path="${1:?Required}"
    local svc_file="$(basename "$svc_path")"
    local svc_name="${svc_file#*.}"
    local scope=$(__get_scope "$svc_path")
    local dest_path="${DEST_PATHS[$scope]}/$svc_name"
    local idx="${2:-?}"

    local fscope="$(.f 34)" ; [[ $scope == global ]] && fscope=$(.fsudo)
    printf "${fscope}[$(.f 1)%2d$(.f 22)/%2d]$(.r) Install $(.f 1)%s$(.r)?" \
                          "$idx"   "$services_num"    "${svc_name/.*/}"
    __prompt || return 0

    set -e
    __call cp "$svc_path" "$dest_path"
    __call sed "$dest_path" -i -Ee "s/%UID/$(id -u)/g; s/%USER/$(id -un)/g"
    __systemctl enable "$svc_name"
    if [[ ! $svc_name =~ @ ]]; then
        __systemctl restart "$svc_name"
        __systemctl status "$svc_name" --lines 5 --no-pager --quiet
        echo
    fi
    set +e
}

# shellcheck disable=SC2120
__prompt() {
    local msg="${1:-} (y/n/q): "
    while true; do
        read -n1 -sr -p "$msg" yn
        echo
        case $yn in
            [Yy]*) return 0 ;;
            [Nn]*) return 1 ;;
            [Qq]*)   exit 1 ;;
                *) continue ;;
        esac
    done
}

__get_scope()  { sed -nEe '/^# @SCOPE=/ s/.+=(.+)/\1/p' "$1" ; }
__systemctlq() { __systemctl -q "$@" &>/dev/null ; }
__systemctl()  { if [[ $scope == global ]] ; then __call systemctl "$@" ; else __call systemctl --$scope "$@" ; fi ; }
__call()       { if [[ $scope == global ]] ; then __fcall sudo "$@" ; else __fcall "$@" ; fi }
__fcall()      { __fmtcmd "$@" ; "$@" ; }
__fmtcmd()     {
  local cmd="$1" fcmd=$(.f 94)
  shift
  if [[ $cmd == sudo ]] ; then
    cmd+=" $1" ; fcmd=$(.fsudo)
    shift
  fi
  printf "${fcmd}$(.f 1)>$(.r) ${fcmd}%s$(.r) $(.f 34)%s$(.r)\n" "$cmd" "$*"
}

echo -ne "$(.f 30 103 1)TODO: make appropriate .env files in .es7s dir for shocks\e[0K "
read -sn1 -p "(y/y):" && .r
echo

__main "$@"
