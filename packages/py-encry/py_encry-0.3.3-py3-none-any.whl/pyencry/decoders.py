import math

def decode_rail_fence_cipher(message, rails):
    message_size = len(message)
    fence = { rails: 0 for rails in range(rails) }
    for n in range(rails):
        k = (2 * (rails - 1)) - (n * 2)
        m = n * 2
        message_length = message_size - n
        i = 0
        Up = False
        if n == 0:
            fence[n] = math.ceil(message_length / k)
            continue
        if n == rails - 1:
            fence[n] = math.ceil(message_size / m)
            continue
        for _ in range(message_length):
            if (Up and i % k == 0) or (not Up and i % m == 0):
                i = 0
                fence[n] += 1
                Up = not Up
            i += 1
    fences = {}
    for n in range(rails):
        fences[n] = message[:fence[n]]
        message = message[fence[n]:]
    result = ""
    rail = 0
    down = True
    for n in range(message_size):
        result += fences[rail][0]
        fences[rail] = fences[rail][1:]
        if down:
            rail += 1
        else:
            rail -= 1
        if rail % (rails - 1) == 0 :
            down = not down
    return result
