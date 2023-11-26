#!/bin/bash
#-------------------------------------------------------------------------------
# es7s/core | execute the command and display the output padded with spaces
# (c) 2022-2023 A. Shavykin <0.delameter@gmail.com>
#-------------------------------------------------------------------------------
# shellcheck disable=SC2153,SC2209,SC2059,SC2086

function _help {
  cat <<EOF

    Execute the command and pad the output. Suggested usage is as
    a helper for making consistent terminal screenshots which are
    easy to crop.

USAGE
    padbox [COMMAND [ARGS...]]

DESCRIPTION
    When launched with at least one argument: execute the COMMAND
    with ARGS, and return the output padded with an empty line(s)
    and spaces. Also prepend the output with the COMMAND and ARGS
    as if they were typed in manually.

    When launched without arguments: read standard input, process
    it as described above, except that a line with the COMMAND is
    omitted from the output.

ENVIRONMENT
    ES7S_PADBOX_HEADER
        Display specified string instead of COMMAND ARGS... .
    ES7S_PADBOX_NO_HEADER
        Non-empty value disables displaying COMMAND ARGS... line.
    ES7S_PADBOX_NO_CLEAR
        Non-empty value disables preliminary screen clearing.
    ES7S_PADBOX_PAD_X
        Add specified number of spaces to the left and right [3].
    ES7S_PADBOX_PAD_Y
        Add specified number of empty lines above and below [1].
    ES7S_PADBOX_LINE_LIMIT
        Non-empty value limits the output with specified amount of lines.

    Values in square brackets indicate the default values.

EXAMPLES
    padbox git status
    git status | padbox
EOF
}

function _main {
  pad_x() { printf "%${ES7S_PADBOX_PAD_X:-3}s" ; }
  pad_y() { printf "%${ES7S_PADBOX_PAD_Y:-1}s" | tr ' ' $'\n' ; }

  local pager=cat
  command -v "${PAGER:-""}" &>/dev/null && pager="$PAGER"
  [[ $pager == less ]] && pager="$pager -RS"
  local nopager ; [[ $pager == cat ]] && nopager=true

  header() {
    [[ -n $ES7S_PADBOX_NO_HEADER ]] && return

    local text="> ${ES7S_PADBOX_HEADER:-$*}"
    while read -r head ; do
      if [[ $nopager ]] ; then
        printf "\x1b[1G\x1b[48;5;16m\x1b[0K%s" "$(pad_x)$head"
        [[ -n "$head" ]] && printf "\x1b[m\n"
      else
        printf "%s%$((cols - ${#head}))s\n" "$head" ""
      fi
    done < <(echo "$text") | bgdrawer
  }

  bgdrawer() {
    [[ $nopager ]] && cat && return
    sed -Ee 's/(^|$|\x1b\[[0-9;:]*m)/&\x1b[48;5;16m/g; s/$/\x1b[49m/; '
  }

  limiter() {
    local lim=$((ES7S_PADBOX_LINE_LIMIT))
    [[ $lim -lt 1 ]] && cat && return
    sed -Ee "\$q ; ${lim}s/$/\n.../g; T; q"
  }

  [[ -z $ES7S_PADBOX_NO_CLEAR ]] && PS1="> " && clear
  unset PROPMT_COMMAND
  local cols=$(($(tput cols) - 6))

  ( pad_y
    [[ $# -eq 0 ]] && set "cat"
    header "$@"
    COLUMNS=$cols "$@" 2>&1 | limiter
    pad_y
  ) | sed -Ee "/\S/ s/^/$(pad_x)/" | $pager
}

[[ ${*/ /s} =~ (^| )-{,2}h(elp)?( |$) ]] && _help && exit
_main "$@"
