# -*- coding=UTF-8 -*-
import sys
import re
import copyright_action
import co_name_action
import filter_str
reload(sys)
sys.setdefaultencoding('utf-8')

class CoName():
    def __init__(self, html):
        self.html = html

    def get_copyright(self):
        html = filter_str.filter_before(self.html)
        marks = ['©', 'copyright', 'Copyright', '(c)', '版权']
        if filter(lambda x: x in html, marks):
            rules = copyright_action.copyright_rules
            actions = copyright_action.copyright_actions
            for key in actions:
                try:
                    f = rules.get(key)
                except KeyError:
                    pass
                    # return json.dumps(...)
                else:
                    results = f(html)
                    if results:
                        index = self._guess_index(results)
                        copyright = filter_str.filter_last(results[index])
                        if copyright:
                            return copyright.decode('utf-8')[:150].encode('utf-8')
            return ''
        else:
            return ''

    @staticmethod
    def get_co_name(copyright):
        if not copyright:
            return
        copyright=filter_str.filter_co_name_before(copyright)
        rules = co_name_action.co_name_rules
        actions = co_name_action.co_name_actions
        for key in actions:
            try:
                f = rules.get(key)
            except KeyError:
                pass
                # return json.dumps(...)
            else:
                results = f(copyright)
                if results:
                    co_name = filter_str.filter_co_name_after(results[0])
                    if co_name:
                        return co_name
        return ''


    @staticmethod
    def _guess_index(copyrights):
        index = 0
        if len(copyrights) > 1:
            for i, copyright in enumerate(copyrights):
                if re.findall(r'\Wall\s+right.*|版权', copyright, re.I):
                    index = i
                    break
                if re.findall(r'is|are', copyright, re.I):
                    continue
        return index
