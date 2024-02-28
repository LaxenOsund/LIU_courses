
def empty_tree_fn():
    return 0
def leaf_fn(key):
    return key**2
def inner_node_fn(key, left_value, right_value):
    if left_value == None:
        left_value = 0
    if key == None:
        key = 0
    return key + left_value
def is_empty_tree(tree):
    return isinstance(tree,list) and not tree
def is_leaf(tree):
    return isinstance(tree,int)
def subtree_left(tree):
    return tree[0]
def subtree_right(tree):
    return tree[2]

def is_inner_node_func(tree):
    if  len(tree) == 3 \
        and isinstance(subtree_left(tree), (int,list)) \
        and isinstance(subtree_right(tree), (int,list)):
        return True
    else:
        return False    

def magic_key(tree):

    m_key = tree[1]
    if tree[1] == []:
        m_key = 0
        return m_key
    else:
        return m_key

# I
def traverse(tree, inner_node_func, leaf_func,empty_tree_func):
    if is_empty_tree(tree):
        return empty_tree_func()
    
    elif is_leaf(tree):

        return leaf_func(tree)
        
    elif is_inner_node_func(tree):
        left = traverse(subtree_left(tree), inner_node_func, \
                leaf_func, empty_tree_func)

        right = traverse(subtree_right(tree), inner_node_func, \
                leaf_func, empty_tree_func)
    
        
        return inner_node_func(magic_key(tree),left,right)
        

# II
def contains_key(search_key, tree):
    """checks if tree contains a key"""
    def inner_node_func(tree, left, right):
        return tree == search_key or left or right
    def leaf_func(tree):
        return tree == search_key
    def empty_tree_func():
        return False
    return traverse(tree, inner_node_func, leaf_func, empty_tree_func)

# III
def tree_size(tree):
    """calculates the size of the tree"""
    def inner_node_func(key,left,right):
        return right + left + 1
    def leaf_func(tree):
        return 1
    def empty_tree_func():
        return 0
    return traverse(tree, inner_node_func, leaf_func, empty_tree_func)    

# IV
def tree_depth(tree):
    """calculates the depth of the tree"""
    def inner_node_func(tree,left,right):
        return max(left, right) + 1
        
    def leaf_func(tree):
        return 1
    def empty_tree_func(tree):
        return 0
    return traverse(tree, inner_node_func, leaf_func, empty_tree_func)



def tests():
   

    test1_traverse = traverse([6, 7, 8], inner_node_fn, leaf_fn, empty_tree_fn)
    test2_traverse = traverse([[4, 2, []], [], [[], 5, 6]], inner_node_fn, leaf_fn, empty_tree_fn)
    test3_traverse = traverse(([[], 1, 5]), inner_node_fn, leaf_fn, empty_tree_fn)

    assert test1_traverse == 43
    assert test2_traverse == 18
    assert test3_traverse == 1

    test1_contains_key = contains_key(6, [6, 7, 8])
    test2_contains_key = contains_key(2, [6, 7, [[2, 3, 4], 0, []]])
    test3_contains_key = contains_key(2, [[], 1, 5])

    assert test1_contains_key == True
    assert test2_contains_key == True
    assert test3_contains_key == False
    
    test1_tree_size = tree_size([2, 7, []])
    test2_tree_size = tree_size([])
    test3_tree_size = tree_size([[1, 2, []], 4, [[], 5, 6]])

    assert test1_tree_size == 2
    assert test2_tree_size == 0
    assert test3_tree_size == 5

    test1_tree_depth = tree_depth(9)
    test2_tree_depth = tree_depth([1, 5, [10, 7, 14]])
    
    assert test1_tree_depth == 1
    assert test2_tree_depth == 3

    print("the code passed all the tests")
tests()