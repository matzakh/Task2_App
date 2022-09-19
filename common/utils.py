from flask_restful import abort


def abort_if_not_exist(item):
    abort(404, message="{} doesn't exist".format(str(item)))


def parse_clauses_for_query(key, operator, value):
    if '|' in value:
        variants = value.split('|')
        return '(' + ' OR '.join([key + ' ' + operator + ' ' + v for v in variants]) + ')'
    else:
        return '(' + key + ' ' + operator + ' ' + value + ')'

