from books import db
from match import match

pattern1 = [['författare', ['&', 'zelle']], ['titel', ['--', 'python', '--']], ['år', '&']]
pattern2 = ['--', ['år', 2042], '--']
pattern3 = ['--', ['titel', ['&', '&']], '--']



def match(seq, pattern):
    """
    Returns whether given sequence matches the given pattern
    """
   
    if not pattern:
        return not seq
    elif pattern[0] == '--':
        if match(seq, pattern[1:]):
            return True
        elif not seq:
            return False
        else:
            return match(seq[1:], pattern)
    elif not seq:
        return False
    elif pattern[0] == '&':
        return match(seq[1:], pattern[1:])
    elif seq[0] == pattern[0]:
        return match(seq[1:], pattern[1:])
    elif isinstance(seq[0], list) and isinstance(pattern[0], list):
        return match(seq[0], pattern[0]) and match(seq[1:], pattern[1:])  
    else:
        return False
    

def search(pattern, db):
    
    lista =[]
    for i in range(0,len(db)):
        if match(db[i], pattern):
            lista.append(db[i])
            return lista
    else:
        return []
    
def tests():
    pattern1 = [['författare', ['&', 'zelle']], ['titel', ['--', 'python', '--']], ['år', '&']]
    pattern2 = ['--', ['år', 2042], '--']
    pattern3 = ['--', ['titel', ['&', '&']], '--']   

    assert pattern1 == [[['författare', ['john', 'zelle']], ['titel', ['python', 'programming', 'an', 'introduction',
'to', 'computer', 'science']], ['år', 2010]], [['författare', ['john', 'zelle']], ['titel',
['data', 'structures', 'and', 'algorithms', 'using', 'python', 'and', 'c++']], ['år', 2009]]]
    assert pattern2 == []
    assert pattern3 == [[['författare', ['armen', 'asratian']], ['titel', ['diskret', 'matematik']], ['år', 2012]]]
    print("code passed all the tests")
tests()
      