from importlib import import_module


def load_integration_type(integration_key):
    module = import_module(
        name=integration_key
    )
    return module


def load_operation(integration_key, operation_key):
    module = import_module(
        name=f'{integration_key}.{operation_key}'
    )
    return module


def format_data(record, schema):
    data = dict()
    for k, v in schema.items():
        val = None
        if isinstance(v, list):
            val = [format_data(record=record, schema=i) for i in v]
        elif isinstance(v, dict):
            if all(i in ['value', 'path', 'default'] for i in v.keys()):
                if 'value' in v.keys():
                    val = v['value']
                elif 'path' in v.keys():
                    parser = ng_parse(v['path'])
                    val = [i.value for i in parser.find(record)]
                    if len(val) == 0:
                        val = None
                    elif len(val) == 1:
                        val = val[0]
                if val is None and 'default' in v.keys():
                    val = v['default']
            else:
                val = v
        data[k] = val
    return data
