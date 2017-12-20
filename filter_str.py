# -*- coding=UTF-8 -*-
import re

def filter_co_name_before(str):
    if not str:
        return
    re_extra = re.compile(r'(?:website|design|powered)\s*by?|\stel.*$', re.I)
    str = re_extra.sub(' ', str)
    str = re.sub(r'™', "", str)
    str = re.sub(r"[-_\w\.]{0,64}@([-\w]{1,63}\.)*[-\w]{1,63}", ' ', str)
    re_url=re.compile(r'((ht|f)tps?):\/\/[\w\-]+(\.[\w\-]+)+([\w\-\.,@?^=%&:\/~\+#]*[\w\-\@?^=%&\/~\+#])|(?:\w|\.)*www(?:\w|\.)*',re.I)
    str = re_url.sub(' ',str)
    return str

def filter_co_name_after(str):
    if not str:
        return
    re_extra = re.compile(r'\w+@.*|\ball.*?reserved|,|^\.|\bby\b|\.co\s', re.I)
    str = re_extra.sub(' ', str)
    str = re.sub(r'\.|/|”|“|"|::|\(', "", str)
    str = str.decode('utf-8')
    str = re.sub(r'(?:1|2)\d{3}(?:\s*\W\s*(?:1|2)\d{3})?', "", str)
    str = re.sub(r'^\s*\W(\s|\s*(?=\w))', "", str)
    str = re.sub(r'(?:^\w?|\s+)\W?\s*$', '', str)
    str = str.encode('utf-8')
    str = re.sub(r'(?:\w|\.)*com(?:\w|\.)*', " ", str)
    str = re.sub(r'^\s*\w{0,3}\s*$', "", str)
    str = re.sub(r'\s{2,50}', " ", str)
    str = re.sub(r'^\s*', "", str)
    return str


def filter_last(str):
    if not str:
        return
    str = re.sub(r"</?\w+[^>]*>|\n", " ", str)
    re_script = re.compile(r'©|copyright|\(c\)|®|版权所有|版权归|所有|版权声明|声明|保留权利', re.I | re.S)
    str = re_script.sub('', str)
    str = re.sub(r"amp;|&nbsp;|,|Â|•|-{2,10}", " ", str)
    str = re.sub(r"\d{5,50}", " ", str)
    str = str.decode('utf-8')
    str = re.sub(r'^\s*\W\s+', "", str)
    str = re.sub(r'(?<=\w)\s*\W\s*$', "", str)
    str = str.encode('utf-8')
    str = re.sub(r'\s{2,50}', " ", str)
    str = re.sub(r'^\s*', "", str)
    return str

def filter_before(html):
    if not html:
        return
    extra_tags = ['frameset', 'noframes', 'script', 'style', 'ymaps', 'noscript']
    exist_tags = filter(lambda x: x in html, extra_tags)
    for tag in exist_tags:
        re_tag = re.compile('<\s*' + tag + '[^>]*>.*?<\s*/\s*' + tag + '\s*>', re.I | re.S)
        html = re_tag.sub('', html)
    re_cdata = re.compile('//<!\[CDATA\[[^>]*//\]\]>', re.I)
    re_comment = re.compile('<!--.*?-->', re.S)  # HTML注释
    html = re_cdata.sub('', html)  # 去掉CDATA
    html = re_comment.sub('', html)  # 去掉HTML注释
    html = re.sub(r'<img[^>]*>', '', html)  # 去掉HTML注释
    return html






