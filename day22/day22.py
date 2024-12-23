import math

with open("day22/input.txt", "r") as f:
    secrets = [int(line.strip()) for line in f.readlines()]

print(secrets)

res = []

for secret in secrets:
    n_generations = 2000
    while(n_generations>0):
        # step 1:
        secret = ((secret * 64) ^ secret) % 16777216
        
        # step 2:
        secret = ((math.floor(secret / 32)) ^ secret) % 16777216

        # step 3:
        secret = ((secret * 2048) ^ secret) % 16777216

        n_generations -= 1
    
    res.append(secret)

print(res)
print(sum(res))