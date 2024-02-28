
def fusc(n):
  if n < 2:
    return n 
  if (n > 1) and (n%2 == 0):
    return fusc(n//2)
  else:
    return fusc((n-1)//2) + fusc((n+1)//2)
  
