#!/bin/sh

find -regextype sed -regex '.*/gen_.*\.\w\w[0-9]\{1,2\}' -delete
if [ "$1" = "-a" ]; then
    find -regextype sed -regex '.*/out_.*\.txt' -delete
    find -regextype sed -regex '.*/gen_.*\.cir' -delete
fi
