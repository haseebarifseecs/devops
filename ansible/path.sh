#!/bin/bash
path=$(dpkg-query -L python3)

# iterate over each path in the variable
for p in $path; do
  # check if the path is a file
  if [ -f "$p" ]; then
    echo "$p"
  fi
done


#if test -n "$(dpkg-query -L postgresql-common | grep '^/etc/\|^/etc/.*\/')"; then dpkg-query -L postgresql-common | grep '^/etc/\|^/etc/.*\/' | xargs file -F'/' | grep -v 'directory' | cut -d: -f1; fi
