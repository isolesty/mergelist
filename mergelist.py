#!/usr/bin/env python3

import re
import sys
import os
import json


def translate_time(timestr):
    # timestr example: 2016-04-20~100003
    newdate = ''
    datere = re.compile("(\d+)-(\d+)-(\d+)~(\d\d)(\d\d)(\d\d)")

    dateitem = re.findall(datere, timestr)[0]
    newdate = dateitem[0] + "-" + dateitem[1] + "-" + dateitem[2] + \
        " " + dateitem[3] + ":" + dateitem[4] + ":" + dateitem[5]

    datecmd = "date -d '" + newdate + "'"

    trdate = os.popen(datecmd).read().strip()

    return trdate


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
    logtype = 'second'
    # sendpath should start with sendpath[0]
    sendflag = -1
    sendpath = ["",
                "pool/",
                "dists/unstable/main/binary-amd64/Packages.diff/",
                "dists/unstable/main/binary-i386/Packages.diff/",
                "dists/unstable/main/source/Sources.diff/",
                "dists/unstable/main/binary-amd64/by-hash/",
                "dists/unstable/main/binary-i386/by-hash/",
                "dists/unstable/main/source/by-hash/",
                "dists/unstable/contrib/binary-amd64/Packages.diff/",
                "dists/unstable/contrib/binary-i386/Packages.diff/",
                "dists/unstable/contrib/source/Sources.diff/",
                "dists/unstable/contrib/binary-amd64/by-hash/",
                "dists/unstable/contrib/binary-i386/by-hash/",
                "dists/unstable/contrib/source/by-hash/",
                "dists/unstable/non-free/binary-amd64/Packages.diff/",
                "dists/unstable/non-free/binary-i386/Packages.diff/",
                "dists/unstable/non-free/source/Sources.diff/",
                "dists/unstable/non-free/binary-amd64/by-hash/",
                "dists/unstable/non-free/binary-i386/by-hash/",
                "dists/unstable/non-free/source/by-hash/"]

    while num < totallen:
        if 'sending incremental file list' == datalines[num]:
            logtype = 'first'
            sendflag += 1
        elif 'UPLOAD' in datalines[num]:
            pass
        elif 'Sync' in datalines[num]:
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
        elif 'building file list' in datalines[num]:
            pass
        elif 'files...' in datalines[num]:
            pass
        elif 'files to consider' in datalines[num]:
            pass
        # elif 'GUARD' in datalines[num]:
        #     pass
        elif re.findall(timere, datalines[num]):
            pass
        elif datalines[num].startswith('deleting'):
            filepath = datalines[num].strip().split(' ')[1]
            filesize = 0
            deletelist.append({
                "filepath": filepath,
                "filesize": "0"
            })

        else:

            filepath = datalines[num].strip()
            if logtype == 'first':
                pathprefix = sendpath[sendflag]
                filepath = pathprefix + filepath

            filesize = 0
            step = 0
            maxnum = totallen - num
            while step < maxnum:
                if '100%' in datalines[num + step] and '#' in datalines[num + step]:
                    # 63447734 100%    2.19MB/s    0:00:27 (xfer#113,
                    # to-check=1079/189807)
                    filesize = datalines[
                        num + step].strip().split(' ')[0].replace(",", "")
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
