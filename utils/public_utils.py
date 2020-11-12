
import json
from datetime import date
from datetime import datetime



class JsonExtendEncoder(json.JSONEncoder):
    """
        This class provide an extension to json serialization for datetime/date.
    """
    def default(self, o):
        """
            provide a interface for datetime/date
        """
        if isinstance(o, datetime):
            return o.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(o, date):
            return o.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, o)


def titleLower(xstr):
    return xstr[0].lower() + xstr[1:]


import inspect

# 找出模块里所有的类名
def get_classes(arg):
    class_dic = dict()
    clsmembers = inspect.getmembers(arg, inspect.isclass)
    for (name, _) in clsmembers:
        if name in ("ForeignKey", "FormatColumns", "CharField"):
            continue
        class_dic.setdefault(titleLower(name), _)
    return class_dic