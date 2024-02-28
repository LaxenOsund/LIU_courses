def fac(x):
#calculates x!
    if x == 0:
        return 1
    return x*fac(x-1)

def perms(n,k):
#calculates n!/k!, if k is 1 less than n function returns k+1
    if n == k:
        return 1
    if n == k+1:
        return k+1
    return n * perms(n-1, k)


def choose(n, k):
#check what value k or q is biggest and sends it to perms to calculate
#fewest amount of operations as possible
    q = n-k
    if k >= q:
        return perms(n,k) // fac(q)
    else:
        return perms(n,q) // fac(k)




