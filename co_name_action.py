# -*- coding=UTF-8 -*-
import re
co_name_rules = {}
co_name_actions=[]
year_str=r'(?:1|2)\d{3}(?:\s*\W\s*(?:1|2)\d{1,3})?'
def co_name_action(name):
    def decorator(f):
        co_name_rules[name] = f
        co_name_actions.append(name)
        return f
    return decorator

@co_name_action('all_right')
def all_right(data):
    data = data.decode('utf-8')
    re_rule=re.compile(year_str+r'(.*?)all\s+right', re.I)
    return find_all(re_rule, data)


@co_name_action('eng_keys')
def eng_keys(data):
    eng_keys = ['co', 'inc', 'llc', 'ltd', 'corp', 'gmbh', 'limited', 'association', 'corporation', 'college',
                'school', 'group', 'club', 'park']
    re_rule = re.compile(r'(.*?\W(?:' + '|'.join(eng_keys) + '))\W?(?:\W|$)', re.I)
    return find_all(re_rule, data)


@co_name_action('chn_keys')
def chn_keys(data):
    chn_keys = ['公司', '集团', '学院', '会社','协会']
    re_rule = re.compile(r'.*?(?:' + '|'.join(chn_keys) + ')', re.I)
    return find_all(re_rule, data)


@co_name_action('all_right_other')
def all_right_other(data):

    re_rule = re.compile(r'(.*?)(?:版权所有|all\s+right)', re.I)
    return find_all(re_rule, data)

@co_name_action('russia')
def russia(data):
    re_rule = re.compile(r'(?:ООО|\d{4}|OOO)\s*(?:"|«)(.*?)(?:"|»)', re.I)
    return find_all(re_rule, data)

@co_name_action('keywords_other')
def keywords_other(data):
    re_rule = re.compile(r'(.*?)\|', re.I)
    return find_all(re_rule, data)

@co_name_action('after_year')
def after_year(data):
    data = data.decode('utf-8')
    re_rule = re.compile(r'^'+year_str+'(.{1,20})(?:\.(?=\W)|\s{2,5}|$)', re.I)
    return find_all(re_rule, data)

@co_name_action('before_year')
def before_year(data):
    data = data.decode('utf-8')
    re_rule = re.compile(r'^(.{1,20})(?:1|2)\d{3}(?:\W|$)')
    return find_all(re_rule,data)

@co_name_action('single_words')
def single_words(data):
    re_rule = re.compile(r'^\s*\w*?\s*\w*?\s*\w*?\s*$')
    return find_all(re_rule,data)

def find_all(re_rule,data):
    co_name = re_rule.findall(data)
    return co_name

