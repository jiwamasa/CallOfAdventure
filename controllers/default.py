#default controller

@auth.requires_login()
def index():
    return dict();

def user():
    return dict(form=auth())
