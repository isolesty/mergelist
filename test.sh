#!/bin/bash
# cd /srv/packages/deepin/checklist/
_date=$(date +%Y-%m-%d~%H%M%S)

# get the last rsync log
_last=$(readlink current)

python3 mergelist.py rsync.log-bak ${_date} ${_last}

# now current is the new rsync log
ln -sf ${_date} current

# clean
# rm /tmp/rsync-${_date}
