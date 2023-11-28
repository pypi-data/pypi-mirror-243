#!/bin/bash
# check relay reverse port connection, kill sshd if connection is dead
# in order for autossh on client to reconnect

function __log() {
    logger -p "local7.${1:-info}" -t "es7s/${0##*/}" -s
}

function __main() {
    local RELAY_REV_PORT="${1:?Relay reverse port required}"
    __log <<< "Processing backtunnel port $RELAY_REV_PORT"

    if nc localhost ${RELAY_REV_PORT} <<< '\x00' -w 10 | grep SSH ; then
        __log <<< "Connection seems OK, no action required"
        return
    fi
    __log warning <<< "Connection refused or timed out"

    local sshd_pid=$(netstat -tuWlpaN | grep -Ee :${RELAY_REV_PORT}.+sshd | sed -nEe '1s|.+\s+([0-9]+)/sshd.+|\1|p')
    if [[ -n $sshd_pid ]] ; then
        __log <<< "Found sshd process that occupies port $RELAY_REV_PORT, PID $sshd_pid"
        kill $sshd_pid && __log <<< "Killed PID $sshd_pid" || __log error <<< "Failed to kill PID $sshd_pid"
    else
        __log <<< "No corresponding sshd process found"
    fi
}

__main "$@" | __log
