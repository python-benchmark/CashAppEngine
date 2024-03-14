
def param_exist(var, req):
    try:
        return (var in req and req[var]!="")
    except KeyError:
        pass

def sortMethod(req, value = None):
    if (value):
        sort = value
    else:
        sort = req['sort']
    if param_exist("dir",req) and req['dir'].upper()=="DESC":
        sort = "-"+sort
    return sort
