#!/bin/bash
#'''''''''''''''''''''''''''''''''''''#
#             es7s/core               #
#       (c) 2023 A. Shavykin          #
#      <0.delameter@gmail.com>        #
#.....................................#
[[ $* =~ -?-h(elp)? ]] && echo "Usage :
$(basename "${0%.*}")" && exit 0; PB(){
printf "%s\n" "$PATH"| tr : '\n'|sort |
uniq|xargs -I{} -n1 find {} -maxdepth \
1 -executable \( -xtype f -or -type f \
\) -printf $'%36h\t\e[1m\t%f\x1b[2m\t%l
' | sed -Ee '/^\s*\/usr/s/\x1b\[/&34;/1
/^\s*\/home/s/\x1b\[/&33;/1;s|\S+|&\/|1
s|( *)'"${HOME//\//\\\/}"'|\1~|;/\S+/!d
/^\s+/s/\x1b\[/&35;/1;s/(\s)$/\1\x1b[m/
s/(\t)([^ []+)$/@\x1b[;2m\1\2\x1b[m/' |
sort -k3,3| tr -s ' '| column -ts$'\t'|
sed -E 's/(\S+)( *)/\2\1/1'|cat -n;cat\
<<<____________________>>/dev/null;};PB
