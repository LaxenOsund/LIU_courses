import string

LOWERCASE = string.ascii_lowercase + "åäö"
UPPERCASE = string.ascii_uppercase + "ÅÄÖ"
CASE1 = LOWERCASE + "_" + "."
CASE2 = UPPERCASE + " " + "|"

def split_rec(string):
    """splits a string into 2 messages recursively
    -msg 1 can only cointain case 1
    -msg 2 can only cointain case 2
       """
    if not string:
        return ("", "")
    c = string[0]
    msg1, msg2 = split_rec(string[1:])
    msg1 = c + msg1 if c in CASE1 else msg1
    msg2 = c + msg2 if c in CASE2 else msg2
    return msg1, msg2

def split_it(string):
    """splits a string into 2 meassages iterative
    - msg 1 can only contain case 1
    - msg 2 can only contain case 2
       """
    msg1 = msg2 = ""
    for char in string:
        if char in CASE1:
            msg1 = msg1 + char
        if char in CASE2:
            msg2 = msg2 + char
    return (msg1, msg2)
