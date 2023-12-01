
import copy
from types import SimpleNamespace

from dateutil.parser import *
from datetime import *

def mapping_engine(record, map):

    new_record = _mapping_engine(record, map)
    
    return new_record



def _mapping_engine(record, map):
    """Given a record and a mapping, evaluates the mapping to build output record
    """
    map = _remove_dots(map, True)
    record = _remove_dots(record, False)


    #Initialize r to be accessed with dot notation
    r = _to_dot_notation(record)

    if isinstance(map, dict):

        # Handle presence of base
        base = map.get('_base', None)
        if base:
            try:
                base_records = eval(base)
                base_records = base_records if isinstance(base_records, list) else [base_records]
                results = []
                new_map = copy.deepcopy(map)
                new_map.pop('_base')
                for i in base_records:
                    results.append(_mapping_engine(i, new_map))
                return results
            except Exception as e:
                a=1
        
        # Else
        new_record = {}
        for k, v in map.items():
            if not k.startswith('_'):
                new_record[k] = _mapping_engine(record, v)
        return new_record

    elif isinstance(map, list):
        new_record = []
        for i in map:
            new_record.append(_mapping_engine(record, i))
        return new_record
    else:
        try:
            
            return eval(map)
        except Exception as e:
            
            return ''




def _remove_dots(record, is_map=False):

    if isinstance(record, dict):
        new_record = {}
        for k, v in record.items():
            new_k = k
            if is_map is False:
                new_k = new_k.replace('@', '_____')
                new_k = new_k.replace(':', '____')
                new_k = new_k.replace('#', '___')
            new_record[new_k] = _remove_dots(v, is_map)
        return new_record

    elif isinstance(record, list):
        new_record = []
        for i in record:
            new_record.append(_remove_dots(i, is_map))
        return new_record
    else:
        if isinstance(record, str):
            new_record = record
            if is_map is True:
                new_record = new_record.replace('@', '_____')
                new_record =  new_record.replace(':', '____')
                new_record = new_record.replace('#', '___')
                new_record = new_record.replace('https____', 'https:')
            return new_record
            
        else:
            return record



def _to_dot_notation(data):
    """Transform record into dot notation capable
        r = _to_dot_notation(record)
        value = r.a.b[2].c
    """

    if type(data) is list:
        return list(map(_to_dot_notation, data))
    elif type(data) is dict:
        sns = SimpleNamespace()
        for key, value in data.items():
            setattr(sns, key, _to_dot_notation(value))
        return sns
    else:
        return data



def _set_datetime(data):
    """Transform record into dot notation capable
        r = _to_dot_notation(record)
        value = r.a.b[2].c
    """

    if type(data) is list:
        return list(map(_set_datetime, data))
    elif type(data) is dict:
        for k, v in data.items():
            data[k] = _set_datetime(v)
        return data
    else:
        if isinstance(data, str) and len(data) > 6:
            try:
                data = parse(data)
            except Exception as e:
                a=1
        return data



