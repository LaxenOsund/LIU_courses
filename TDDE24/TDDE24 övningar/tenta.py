import math


def expand(mem, msg):
  result = []
  for item in msg:
    if isinstance(item, int):
      result.append(mem[item])
    elif isinstance(item, list):
      result.append(expand(mem, item))
    else:
      result.append(item)
  return result

mem = [" ","att","lycka","tenta","till","på","är","kanske","tentan"]

def expand_concat(mem, msg):
  result = []
  current_str = ''
  for item in msg:
    if isinstance(item, int):
      current_str += mem[item]
    elif isinstance(item, list):
      sublist_result = expand_concat(mem, item)
      if current_str:
        result.append(current_str)
        current_str = ''
      result.append(sublist_result)
    else:
      current_str += item
  if current_str:
    result.append(current_str)
  return result

def divide(n, seq):
  if len(seq) % n == 0:
    sublist_len = len(seq) // n
  else:
    sublist_len = (len(seq) // n) + 1


  sublists = []


  for i in range(n):

    start = i * sublist_len
    end = start + sublist_len

    sublists.append(seq[start:end])
    
  return sublists

def consecutive_parts_i(seq: tuple) -> list:
  if not seq:
    return []
  result = []
  current_number = [seq[0]]
  for i in range(1,len(seq)):
    if seq[i] == current_number[-1] + 1:
      #1,2,3,5
      #är 1 lika med 1+1 nej
      #är 2 lika med 1+1 ja
      #[1,2]
      #är 3 lika med 2+1 ja
      #[1,2,3]
      current_number.append(seq[i])
    else:
        result.append(current_number)
        current_number = [seq[i]] 
  result.append(current_number)
  return result


def consecutive_parts_r(seq: list):
  if not seq:
    return []
  i = 1
  while i < len(seq) and seq[i] == seq[i - 1] + 1:
    i+=1
  if i > 1:
    return [seq[:i]] + consecutive_parts_r(seq[i:])
  else:
    return [[seq[0]] + consecutive_parts_r(seq[1:])]

#print(consecutive_parts_r((1,2,3,6,7,2,8,11,33,34)))
def find_nearest(nseq1, seq2):
  result = []
  for search in nseq1:
    if isinstance(search,list):
      result.insert(0,[])
    else:
      return search
  for value in seq2:
    pass
""""""
def find_least_close(seq1, seq2):
  # En tom lista att fylla med resultat
  result = []
  # För varje tal x i seq1
  for x in seq1:
    # Om seq2 är tom, så är x det tal som är längst bort från x själv
    if not seq2:
      least_close = x
    else:
      # Anta att det första talet i seq2 är det tal som är längst bort från x
      least_close = seq2[0]

      # För varje tal y i seq2
      for y in seq2:
        # Om y är närmare x än det tal som är längst bort just nu
        
          if abs(y - x) >= least_close - x :
            if y == least_close:
              least_close = max(y,least_close)

              
      
          # Uppdatera least_close till y och least_distance till avståndet mellan x och y
            """   
            least_close = max(abs(y),abs(x))
          if least_close == -y and least_close == abs(y) or least_close == -x and least_close == abs(x):
            neg_check = True
          else:
            neg_check = False
          """



      result.append(least_close)
  

  return result


def split_by_first(sec: list[str]):
  result = dict()
  for word in sec:
    key = word[0]
    if key in result:
      result[key].append(word)
    else:
      result[key] = [word]
  return result




def split_lists(seq, sizes: str):
    result = []

    # For every number of elements...
    for count in sizes:
        count = int(count)
        if len(seq) < count:
            # Not enough elements left
            return None, None

        # OK, pick the desired number of elements (0 or more)
        # and step forward in the sequence (creates a copy of the sequence).
        result.append(seq[:count])
        seq = seq[count:]

    # Took care of the entire 'sizes'
    if seq:
        # Too many elements in seq
        return None, None
    else:
        # Got exactly as many elements as we needed
        return result


def doubled_odds1(seq: list):
  
  unested = []
  for number in seq:
    
    if isinstance(number, list):
      extra = doubled_odds1(number)
      unested += extra
    else:
      unested.append(number)
  #now checks if number is odd
  result = []
  for value in unested:
    if value % 2 != 0:
      result.append(value*2)
    else:
      result.append(value)
  return result

def doubled_odds2(seq: list):
  
  result = []
  for i in seq:
    if isinstance(i, list):
      result.append(doubled_odds2(i))
    elif isinstance(i , int) and i % 2 == 1:
      result.append(i*2)
    else:
      result.append(i)
  return result




def merge_r(s1: list, s2: list):
  result = []
  if s1:
    if s2:
      if s1[0] > s2[0]:
        result.append(s2[0])
        e1 = result.append(merge_r(s1,s2[1:]))
        result += e1
      else:
        result.append(s1[0])
        e2 = result.append(merge_r(s1[1:],s2))
        result += e2
    else:
      result.append(s1[0])
      e2 = result.append(merge_r(s1[1:],s2))
      result += e2    
  else:
    result.append(s2[0])
    e1 = result.append(merge_r(s1,s2[1:]))
    result += e1
  if len(s1) == 0 and len(s2) == 0:
    return result
  


def roundrobin(seq: list):
  result = []

  maxlen = max(len(subseq) for subseq in seq)
  for index in range(maxlen):
    for subseq in seq:
      if index < len(subseq):
        result.append(subseq[index])
  return result

print(roundrobin([[1,2,3], [0], ['abc',6]]))

def by_sensor_i(seq:list):
  result = dict()
  for tuple in seq:
    if tuple[0] in result:
      result[tuple[0]].append(tuple[1])
    else:
      result[tuple[0]] = [tuple[1]]
  return result



import math

def divide(n: int, seq:list) -> list:
  length = math.ceil(len(seq)/n)
  result = []
  for i in range(n):
    subseq = seq[i * length: (i+1) *length]
    result.append(list(subseq))
  return result

print(divide(4, (1, 2, 3, 4, 3)))


def make_val_finder(val):
  def checker(seq):
    if val in seq:
      return True
    else:
      return False
    
  return checker
contains_14 = make_val_finder(14)
print(contains_14([1,14,"x"]))

def is_anagram(word1: str, word2: str) -> bool:
  if len(word1) == len(word2):
    test = 0
    for i in word1:
      if i in word2:
        test += 1
    if len(word1) == test:
      return True
  return False

print(is_anagram("themorsecode", "herecomedots"))

def rle_i (seq: str):
  result = []
  while seq:
    current = seq[0]
    count = 1
    while count < len(seq) and seq[count] == current:
      count +=1
    result += [current, count]
    seq = seq[count:]
  return result

def rle_r(seq:str):
  if not seq:
    return []
  rle_rest = rle_r(seq[1:])
  if rle_rest and seq[0] == rle_rest[0]:
    return [rle_rest[0], rle_rest[1] + 1] + rle_rest[2:]
  else:
    return [seq[0],1] + rle_rest



def doors():
  result = []
  
  for count in range(100):
    for i in range(count + 1 ,101,count + 1):
      if i in result:
        result.remove(i)
      else:
        result.append(i)
  return result
print(doors())


def fusc(n):
  if n < 2:
    return n 
  if (n > 1) and (n%2 == 0):
    return fusc(n//2)
  else:
    return fusc((n-1)//2) + fusc((n+1)//2)
  
def fusc_i(n):


