from types import SimpleNamespace




def flatten_to_dot(records, key=None):
    """Flatten series of records in list of dot records
    """

    def _flatten_to_list(records, key=None):
        results = []

        if isinstance(records, list):
            results += [{"key": key, "value": "list"}]
            value = 0
            for i in records:
                new_key = f'{str(key)}[{str(value)}]'
                value += 1
                results += _flatten_to_list(i, new_key)

        elif isinstance(records, dict): 
            if key:
                results += [{"key": key, "value": "object"}]
            for k, v in records.items():
                new_key = f'{str(key)}.{str(k)}' if key else f'{str(k)}'
                results += _flatten_to_list(v, new_key)

        else:
            results += [{"key": key, "value": records }]

        return results

    results = _flatten_to_list(records, key)

    # Convert from list to dict
    record = {}
    for i in results:
        k = i.get('key', None)
        v = i.get('value', None)
        record[k] = v
    return record



def parse(data):
    if type(data) is list:
        return list(map(parse, data))
    elif type(data) is dict:
        sns = SimpleNamespace()
        for key, value in data.items():
            setattr(sns, key, parse(value))
        return sns
    else:
        return data
