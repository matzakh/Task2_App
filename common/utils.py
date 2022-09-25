import pytz

from flask_restful import abort
from datetime import datetime as dt


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
    if '<=' in keystr:
        return keystr.split('<=')[0], '<=', keystr.split('<=')[1]
    if '>' in keystr:
        return keystr.split('>')[0], '>', keystr.split('>')[1]
    if '<' in keystr:
        return keystr.split('<')[0], '<', keystr.split('<')[1]
    return None


def if_none_replace_with_strnull(val):
    if val is None:
        return 'NULL'
    return val


def strdate_timezone_to_utc_convert(str_dt, timezone, pattern="%Y-%m-%d %H:%M:%S"):
    input_date = dt.strptime(str_dt, pattern).replace(tzinfo=pytz.timezone(timezone))
    output_date = input_date.astimezone(pytz.utc)
    return output_date.strftime(pattern)

