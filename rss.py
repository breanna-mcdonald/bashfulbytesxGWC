#!/usr/bin/env python2
# Generate rss file when new post is published
# in makefile, under publish
# cycle through posts/ 
# generate xml file (delete previous)

import os
import sys
import time as ostime
from email.Utils import formatdate
from datetime import datetime
from markdown2 import markdown_path

TIMES = {}
NEWEST = []

reload(sys)

def scan():
    for source in ["./hackers_md"]:
        listing = os.listdir(source)

        for fn in listing:
            fp_md = os.path.join(source, fn)
            fp_html = os.path.join(source.replace('_md', ''), fn.replace('.md','.html'))
            md= markdown_path(fp_md, extras=['metadata'])
            try:
                TIMES[fp_html] = [md.metadata['date'], md.metadata['title'], md.metadata['summary']]
            except KeyError as e:
                if 'summary' not in md.metadata:
                    TIMES[fp_html] = [md.metadata['date'], md.metadata['title'], '']


def gather_data():
    for filename, [time, title, summary] in TIMES.iteritems():
        dt = [int(d) for d in time.split()]
        dtime = datetime(*dt)
        unixtime = ostime.mktime(dtime.timetuple())
        time = formatdate(unixtime)

        name = filename
        tmp = name
        
        NEWEST.append({
                'name': name,
                'dtime': dtime,
                'time': time,
                'title': title, 
                'summary': summary})

#       if len(NEWEST) > 5:
#           for n, [t, title, summary] in NEWEST.iteritems():
#               if t < oldest_time: # new oldest
#                   oldest_time = t
#                   tmp = n
#           NEWEST.pop(tmp, None)
        
def sort():
    global NEWEST
    NEWEST[:] = sorted(NEWEST, key=lambda k: k['dtime'], reverse=True)

def generate_xml():
    global NEWEST

    content = """<?xml version="1.0" encoding="utf-8"?>
<rss version="2.0">
<channel>

<title>BashfulBytes RSS Feed</title>
<link>http://bashfulbytes.com/</link>
<description>Weblog on computer scientist and young researcher encounters</description>
"""
    for _, [fn, time, title, summary] in enumerate([d['name'], d['time'], d['title'], d['summary']] for d in NEWEST):
        print fn
        link = "http://bashfulbytes.com/hackers" + fn.replace('./hackers', '')
        content = content + """
<item>
    <title>{}</title>
    <link>{}</link>
    <guid>{}</guid>
    <pubDate>{}</pubDate>
    <description>![CDATA[ {} ]]</description>
</item>
""".format(title, link, link, time, summary)

    content = content + """
</channel>
</rss>
"""
    try:
        os.remove("./rss.xml")
    except Exception as e:
        pass
    rss = open("./rss.xml", 'w')
    rss.write(content)
    rss.close

if __name__ == '__main__':
    scan()
    gather_data()
    sort()
    generate_xml()

