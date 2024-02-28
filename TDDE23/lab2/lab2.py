# Här kan du skriva programkod för labb 2.
# Du behöver strikt sett inte lämna in koden för denna labb,
# men vi lägger ändå in en förberedd fil för att förenkla.
# Om du har skrivit labbkoden någon annanstans är det också OK.

def ental(a):
    return a % 10

def tiotal(a):
    return (a-ental(a))//10

def produkt(x):
    return ental(x)+tiotal(x)

def multi(y):
    #multiplicerar med två på varannan
    multi = 1
    if y % 2 ==0:
        multi = 2
    return multi

def summa(y=[]):
    #räknar summan av alla tal i personnumret förutom kontroll siffran
    sum = 0
    for i in range(9):
        mul = multi(i)
        prod = mul * y[i]
        sum += produkt(prod)
    return sum

def närmstatio(x):
    if x%10 == 0:
        return x
    return (x-ental(x)+10)

def check_pnr(pnr=[]):
    sum = summa(pnr)
    sumnärmsta = närmstatio(sum)
    kontroll = sumnärmsta-sum
    return kontroll == pnr[-1]

print(check_pnr([0,1,0,6,1,4,3,3,7,3]))
print(check_pnr([0,1,0,6,1,4,3,3,6,3]))
