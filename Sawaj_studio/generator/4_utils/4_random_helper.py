"""
🎲 Random Helper
"""
import random
import string


def random_string(length=8):
    chars = string.ascii_letters + string.digits
    return "".join(random.choices(chars, k=length))


def random_choice(items):
    return random.choice(items) if items else None


def random_int(min_val, max_val):
    return random.randint(min_val, max_val)


def shuffle_list(items):
    items = list(items)
    random.shuffle(items)
    return items
