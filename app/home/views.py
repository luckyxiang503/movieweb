from . import home

@home.route('/')
def home():
    return 'this is home'