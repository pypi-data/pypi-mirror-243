from typing import Dict
from typing import List

from dict_tools.data import NamespaceDict


def namespaced(hub, value):
    if isinstance(value, Dict):
        return NamespaceDict(**value)
    elif isinstance(value, List):
        ret = []
        for i in value:
            ret.append(hub.tool.type.dict.namespaced(i))
        return ret
    else:
        return value
