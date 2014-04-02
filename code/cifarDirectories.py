import os

def base():
    basePath = '.'
        
    try:
        homeDir = os.environ['HOME']
        basePath = os.path.join(homeDir, 'cifar-ten') 
    except KeyError:
        pass

    return basePath
    
def code():
    return os.path.join(base(), 'code')

def data():
    return os.path.join(base(), 'data')
    
def cifarKaggle():
    return os.path.join(data(), 'cifarKaggle')
    

