import math

def dot(v1, v2):
    return sum(x * y for x, y in zip(v1, v2))

def magnitude(v):
    return math.sqrt(sum(x ** 2 for x in v))

def cosine(list1, list2):
    if len(list1) != len(list2):
        raise ValueError("Both lists must have the same length")

    dot_value = dot(list1, list2)
    mag1 = magnitude(list1)
    mag2 = magnitude(list2)

    if mag1 == 0 or mag2 == 0:
        return 0  # Avoid division by zero

    return dot / (mag1 * mag2)