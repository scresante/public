#!/bin/sh

[ "$1" == "-b" ] && SHOWBROKEN=1

function id {
    stat -t -f -c %i $1 2>/dev/null
}

fs_id=$(id .)

OIFS="$IFS"
IFS=$'\n'
for link in $(find . -type l); do
    #echo "$link"
    [ -z "$link" ] && continue
    link_id=$(id "$link")
    if [ -z "$link_id" ]; then
        [ $SHOWBROKEN ] && echo link is broken: $link
    elif [ "$link_id" != "$fs_id" ]; then
        #echo "link is outside $link ( $link_id )"
        echo "$link -> $(readlink -f "$link")"
        fi
    done

IFS="$OIFS"
