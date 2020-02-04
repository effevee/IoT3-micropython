import ure

def valid_name(name):
    regex = ure.compile('[^A-Za-z0-9\.]')
    if regex.search(name)==None:
        return True
    else:
        return False
    
 
print(valid_name('boot.py#'))
print(valid_name('boot.py'))     