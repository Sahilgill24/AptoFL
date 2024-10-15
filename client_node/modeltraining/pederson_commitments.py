import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa

def generate_large_prime(bit_length):
    # Generate a large prime number
    return rsa.generate_private_key(public_exponent=65537, key_size=bit_length, backend=default_backend()).private_numbers().p

class Verifier:
    def setup(self, security):
        p = generate_large_prime(security)
        q = generate_large_prime(security * 2)
        g = os.urandom(32)  # Generate g as random bytes
        s = os.urandom(32)  # Secret value as random bytes
        h = pow(int.from_bytes(g, 'big'), int.from_bytes(s, 'big'), q)

        param = (p, q, g, h)
        return param

    def open(self, param, c, x, *r):
        result = "False"
        q, g, h = param[1], param[2], param[3]

        # Convert randomness from bytes to integers
        sum_r = sum(int.from_bytes(r_i, 'big') for r_i in r)
        res = (pow(int.from_bytes(g, 'big'), x, q) * pow(h, sum_r, q)) % q

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
        q, g, h = param[1], param[2], param[3]
        return (c, x, r)

class Prover:
    def commit(self, param, x):
        q, g, h = param[1], param[2], param[3]
        r = os.urandom(32)
        c = (pow(int.from_bytes(g, 'big'), x, q) * pow(h, int.from_bytes(r, 'big'), q)) % q
        return c, r

# Security parameter and messages
security = 1024
msg1 = 7804
msg2 = 1254

# Initialize verifier and prover
v = Verifier()
p = Prover()

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
combined_r = int.from_bytes(r1, 'big') + int.from_bytes(r2, 'big')  # The combined randomness
combined_msg = msg1 + msg2  # The combined message
decrypt_combined = v.decrypt(param, addCM, combined_msg, combined_r)

print("\nDecryption of combined commitment (Msg1 + Msg2):", decrypt_combined)
