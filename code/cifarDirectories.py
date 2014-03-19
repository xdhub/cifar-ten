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
    
def mnist():
    return os.path.join(data(), 'mnist')
    
def cifar10():
    return os.path.join(data(), 'cifar10')
    
def cifar100():
    return os.path.join(data(), 'cifar100')
    
def cifarKaggle():
    return os.path.join(data(), 'cifarKaggle')
    

