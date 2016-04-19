#!/usr/bin/env python3

import re
import sys
import os
import json

if __name__ == '__main__':
    """python3 mergelist.py rsync.log currenttime lasttime
    example:
    python3 mergelist.py rsync.log currenttime lasttime
    """

    if len(sys.argv) != 4:
        os._exit(1)

    logfile = sys.argv[1]

    currenttime = sys.argv[2]
    lasttime = sys.argv[3]

    with open(logfile, "r") as f:
        data = f.read()

    datalines = data.split('\n')
    # print(datalines)
    totalre = re.compile(r'total size is (.*) speed')
    rsyncsize = re.findall(totalre, data)
    size = 0
    for x in rsyncsize:
        if ',' in x:
            x = x.replace(',', '')
        size += int(x.strip())

    # print(size)

    totallen = len(datalines)
    filelist = []
    deletelist = []
    addlist = []
    num = 0
    timere = re.compile(r'\d+:\d+:\d+')
    while num < totallen:
        if 'Sync' in datalines[num]:
            pass
        elif not datalines[num]:
            pass
        elif datalines[num].endswith('/'):
            pass
        elif 'sending incremental file' in datalines[num]:
            pass
        elif 'bytes/sec' in datalines[num]:
            pass
        elif 'total size is' in datalines[num]:
            pass
        elif 'GUARD' in datalines[num]:
            pass
        elif re.findall(timere, datalines[num]):
            pass
        elif datalines[num].startswith('deleting'):
            filepath = datalines[num].strip().split(' ')[1]
            if 'dists/' in filepath:
                pass
            else:
                filesize = 0
                deletelist.append({
                    "filepath": filepath,
                    "filesize": "0"
                })

        else:
            filepath = datalines[num].strip()
            # only show files in pools
            if 'dists/' in filepath:
                pass
            elif 'non-free/' in filepath or 'main/' in filepath or 'contrib/' in filepath:
                filepath = "pool/" + filepath
                filesize = 0
                step = 0
                maxnum = totallen - num
                while step < maxnum:
                    if '100%' in datalines[num + step] and 'xfer' in datalines[num + step]:
                        # 63447734 100%    2.19MB/s    0:00:27 (xfer#113,
                        # to-check=1079/189807)
                        filesize = datalines[num + step].strip().split(' ')[0].replace(",", "")
                        addlist.append({
                            "filepath": filepath,
                            "filesize": filesize
                        })
                        num = num + step
                        break
                    else:
                        step += 1

        num += 1

    jsondata = {
        "size": size,
        "added": addlist,
        "deleted": deletelist,
        "preview": lasttime,
        "current": currenttime
    }

    with open(currenttime + ".json", 'w') as f:
        json.dump(jsondata, f)
