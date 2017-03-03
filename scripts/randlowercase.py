import random
import string


def tamper_payload(payload):
    chars = list(payload)
    print chars
    tampered = []
    print tampered
    nums = range(0, len(payload))
    print nums
    for i, c in enumerate(chars):
        print c
        if c == " ":
            print c
            pass
        elif c in string.uppercase and i == random.choice(nums):
            print c, i
            tampered.append(c.lower())
        else:
            print tampered
            tampered.append(c)

    return ''.join(tampered)



print tamper_payload("SELECT * FROM *")
print tamper_payload("SELECT table AND * FROM *")