#!/usr/bin/env python2
# Static site generator
# Author: Breanna Devore-McDonald

# yaml front matter ex.
# ---
# title:
# date:
# tag:
# ---

# TODO: add next/previous posts on each page

import os
import sys
import shutil
import yaml
import markdown
import markdown.extensions.tables
from markdown2 import markdown_path
from datetime import date, datetime
import jinja2
from jinja2 import FileSystemLoader
from jinja2.environment import Environment

reload(sys)  
sys.setdefaultencoding('utf8')

SRC_PATH_PAGE = "./pages"

def convert_mds(source):
    listing = os.listdir(source)
    for infile in listing:
        if infile[0] != '.':
            if infile[0] == 'index.md':
                create_index()
            else:
                filepath = os.path.join(source, infile)
                filename, fileext = os.path.splitext(infile)
                
                directory = filename
                if not os.path.exists(directory):
                        os.makedirs(os.path.join(directory, 'templates'))
                shutil.copy(os.path.join('.', 'templates', 'base.html'), os.path.join(directory, 'templates'))
                outfilepath = os.path.join('.', directory, 'templates', 'index.html')
                outlink =  os.path.join('.', directory)
                outfile = open(outfilepath, 'w')
                output = markdown_path(filepath, extras=['metadata', 'fenced-code-blocks', 'tables'])
                
                content = '''
    {{% extends "base.html" %}}
    {{% block content %}}
    {}
    {{% endblock %}}
    '''.format(output)
                outfile.write(content)
                outfile.close()

def create_index():
    try:
	os.remove("./templates/index.html")
    except Exception as e:
	pass
    index = open("./templates/index.html", 'w')
    content = '{% extends "base.html" %}'

    output = markdown_path(os.path.join('.', 'pages', 'index.md'))
    content = content + '''
{{% block content %}}
{}
{{% endblock %}}'''.format(output)

    index.write(content)
    index.close()


def render_jinja():
    pass
    # TODO: make this work, instead of using staticjinja
    #env = Environment(loader=FileSystemLoader('.'))
    #template = env.get_template("./templates/index_template.html")
    #html = template.render(title="dg")

if __name__ == '__main__':

    convert_mds(SRC_PATH_PAGE)
    create_index()
    #render_jinja()

