from flask_restful import abort

def abort_if_not_exist(item, tbl):
    # TODO
    if item not in tbl:
        abort(404, message="{} doesn't exist".format(item))