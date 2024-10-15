from Crypto import Random
from Crypto.Random import random
from Crypto.Util import number




import sys

def generate(param):
    q = param[1]
    g = param[2]
    h = param[3]
    return q, g, h

class verifier:
    def setup(self, security):
        p = number.getPrime(security, Random.new().read)
        q = number.getPrime(2 * security, Random.new().read)
        g = number.getRandomRange(1, q-1)
        s = number.getRandomRange(1, q-1)
        h = pow(g, s, q)

        param = (p, q, g, h)
        return param

    def open(self, param, c, x, *r):
        result = "False"
        q, g, h = generate(param)

        sum_r = sum(r)
        res = (pow(g, x, q) * pow(h, sum_r, q)) % q

        if c == res:
            result = "True"
        return result

    def add(self, param, *cm):
        q = param[1]
        addCM = 1
        for x in cm:
            addCM *= x
        addCM = addCM % q
        return addCM

    def decrypt(self, param, c, x, r):
        # Reveals the original commitment by showing the value `x` and randomness `r`
        q, g, h = generate(param)
        # The decrypted value is (c, x, r), where x is the original value and r is the randomness
        return (c, x, r)

class prover:
    def commit(self, param, x):
        q, g, h = generate(param)
        r = number.getRandomRange(1, q-1)
        c = (pow(g, x, q) * pow(h, r, q)) % q
        return c, r

# Security parameter and messages
security = 80
msg1 = 1
msg2 = 2

if len(sys.argv) > 1:
    msg1 = int(sys.argv[1])

if len(sys.argv) > 2:
    msg2 = int(sys.argv[2])

v = verifier()
p = prover()

# Setup phase
param = v.setup(security)

# Commitments
c1, r1 = p.commit(param, msg1)
c2, r2 = p.commit(param, msg2)

# Add commitments (this corresponds to adding the messages)
addCM = v.add(param, c1, c2)

print("\nMsg1:", msg1)
print("Msg2:", msg2)
print("\nc1, r1:", c1, ",", r1)
print("c2, r2:", c2, ",", r2)

print("\nWe can now multiply c1 and c2, which is the same as adding Msg1 and Msg2")
print("\nCommitment of adding (Msg1 + Msg2):\t", addCM)

# Verification
result1 = v.open(param, c1, msg1, r1)
result2 = v.open(param, c2, msg2, r2)

print("\nResult of verifying c1:\t\t", result1)
print("Result of verifying c2:\t\t", result2)

# Verify the sum of the messages
result = v.open(param, addCM, msg1 + msg2, r1, r2)
print("Result of verifying Msg1 + Msg2:\t", result)

# Decrypt the commitments (reveal the original values and randomness)
decrypt1 = v.decrypt(param, c1, msg1, r1)
decrypt2 = v.decrypt(param, c2, msg2, r2)

print("\nDecryption of c1:", decrypt1)
print("Decryption of c2:", decrypt2)

# Decrypt the combined commitment for (Msg1 + Msg2)
combined_r = r1 + r2  # The combined randomness
combined_msg = msg1 + msg2  # The combined message
decrypt_combined = v.decrypt(param, addCM, combined_msg, combined_r)

print("\nDecryption of combined commitment (Msg1 + Msg2):", decrypt_combined)
