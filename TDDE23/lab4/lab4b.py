def interpret(exp, inter):
    """
    Interprets a logical expression. Returns a string; 'true' 
    if the expression is correct, and 'false' if it's incorrect.
    """
    if isinstance(exp, str):
        if exp in inter.keys():
            return inter[exp]
        return exp

    elif len(exp) == 3:
        if exp[1] == "AND":
            return "true" if interpret(exp[0], inter) == "true" and \
                interpret(exp[2], inter) == "true" else "false"
        elif exp[1] == "OR":
            return "true" if interpret(exp[0], inter) == "true" or \
                interpret(exp[2], inter) == "true" else "false"

    elif len(exp) == 2 :
        return "false" if interpret(exp[1], inter) == "true" else "true"