# -*- coding=UTF-8 -*-
import re
copyright_rules = {}
copyright_actions=[]
def copyright_action(name):
    def decorator(f):
        copyright_rules[name] = f
        copyright_actions.append(name)
        return f
    return decorator

@copyright_action('html_tag')
def html_tag(data):
    re_html_tag = re.compile(r'<(\w*?)[^>]*copyright[^>]*>(.*?)</\1>', re.I | re.S)
    results = re_html_tag.findall(data)
    copyright=''
    if results:
        copyright = filter(lambda c: c.strip(), [x[-1] for x in results])
    return copyright


@copyright_action('meta')
def meta(data):
    re_meta = re.compile(r'<meta[^>]*copyright[^>]*content="(.*?)"[^>]*>', re.I)
    copyright = filter(lambda x: x.strip(), re_meta.findall(data))
    return copyright


@copyright_action('keywords')
def keywords(data):
    re_key = re.compile(r'<(\w*?)[^>]*>[^<]*(?:©|copyright|\(c\)|版权)(.*?)</\1>', re.I | re.S)
    results = re_key.findall(data)
    copyright=''
    if results:
        copyright = filter(lambda c: c.strip(), [x[-1] for x in results])
    return copyright


@copyright_action('keywords_other')
def keywords_other(data):
    re_key_other = re.compile(r'>\s*(?:©|copyright|\(c\))(.*?)\s*</', re.I | re.S | re.M)
    copyright = filter(lambda x: x.strip(), re_key_other.findall(data))
    return copyright