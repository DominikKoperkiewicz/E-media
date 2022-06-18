import numpy

def primesfrom3to(n):
    #""" Returns a array of primes, 3 <= p < n """
    sieve = numpy.ones(n//2, dtype=bool)
    for i in range(3,int(n**0.5)+1,2):
        if sieve[i//2]:
            sieve[i*i//2::i] = False
    return 2*numpy.nonzero(sieve)[0][1::]+1

def NWD(a, b):
    while b != 0:
        c = a % b
        a = b
        b = c
    return a

def findE(T):
    i = 8
    while NWD(i, T) != 1:
        i += 1
    return i

def findD(e, T):
    eps = 0.0001
    k = 1
    d = (1+k*T) / e
    while d % 1 > eps:
        k += 1
        d = (1+k*T) / e
    return int(d)


def keygen():
    pr = primesfrom3to(99999)
    x = int(pr[len(pr) - 1])
    y = int(pr[len(pr) - 77])

    print("X = ", x)
    print("Y = ", y)

    N = x*y
    T = (x-1)*(y-1)
    
    print("N = ", N)
    print("T = ", T)

    e = findE(T)
    d = findD(e, T) # pow(int(e), -1, int(T))
    # print(x, " - ", y)
    return [e, d, N]

def encrypt(key, mess):
    return pow(mess, key[0], key[1])

def decrypt(key, cyph):
    return pow(cyph, key[0], key[1])

# print(primesfrom3to(99999));
keys = keygen()
pub = [keys[0], keys[2]]
priv = [keys[1], keys[2]]


print(" PUBLIC: ", pub)
print("PRIVATE: ", priv)

M = 327
C = encrypt(pub, M)
print("Cyphe: ", C)
D = decrypt(priv, C)
print("Decrypted: ", D)



#a = 13
#m = 160
#res = findD(a, m)# pow(a, -1, m)
#print("The required modular inverse is: "+ str(res))