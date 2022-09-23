from flask_restful import abort


def abort_if_not_exist(item):
    abort(404, message="{} doesn't exist".format(str(item)))


def parse_clauses_for_query(key, operator, value, is_string=False):
    if not isinstance(value, str):
        return '(' + key + ' ' + operator + ' ' + str(value) + ')'
    if '|' in value:
        variants = value.split('|')
        if is_string:
            return '(' + ' OR '.join([key + ' ' + operator + ' "' + v + '"' for v in variants]) + ')'
        return '(' + ' OR '.join([key + ' ' + operator + ' ' + v for v in variants]) + ')'
    else:
        if is_string:
            return '(' + key + ' ' + operator + ' "' + value + '")'
        return '(' + key + ' ' + operator + ' ' + value + ')'


def parse_key_val_with_operator(keystr):
    if '>=' in keystr:
        return keystr.split('>=')[0], '>=', keystr.split('>=')[1]
    elif '<=' in keystr:
        return keystr.split('<=')[0], '<=', keystr.split('<=')[1]
    elif '>' in keystr:
        return keystr.split('>')[0], '>', keystr.split('>')[1]
    elif '<' in keystr:
        return keystr.split('<')[0], '<', keystr.split('<')[1]
    else:
        return None


def if_none_replace_with_strnull(val):
    if val is None:
        return 'NULL'
    return val
