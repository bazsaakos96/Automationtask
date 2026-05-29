import random
import string


def random_password() -> str:
    chars = string.ascii_letters + string.digits + string.punctuation
    return "".join(random.choice(chars) for _ in range(random.randint(8, 16)))


def random_username() -> str:
    chars = string.ascii_letters + string.digits + "ÁÉÍÓÖŐÚÜŰáéíóöőúüű"
    return "".join(random.choice(chars) for _ in range(random.randint(6, 12)))
static_data=["Akos","Jelszo123"]

class TestData:


    SIGNUP_DATA = [
        (random_username(),random_password()),
        (random_username(), random_password()),
        (static_data[0], static_data[1]),

    ]

    INVALID_SIGNUP_DATA = [
        ("", "Password123!"),
        ("testuser", ""),
        ("", ""),
    ]

    BASE_URL = "https://www.demoblaze.com"
