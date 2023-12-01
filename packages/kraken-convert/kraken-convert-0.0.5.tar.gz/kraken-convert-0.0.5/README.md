# kraken convert

## Overview
Converts records using a mapping record


## github
https://github.com/tactik8/krakenconvert2

## pypi


## methods:
- convert: converts records


## How to use:

### Basics
```
input_records = [
        {
        "record_id": "1234",
        "firstName": "firstName1",
        "lastName": "lastName1",
        "email": "test1@test.com"
        }
    ]

    map = {
        "@type": "'test'",
        "@id": "'/system/table/' + str(r.record_id)",
        "givenName": "r.firstName",
        "familyName": "r.lastName",
        "email": "r.email"
    }

    results = convert(input_records, map)
    print(results)

```

