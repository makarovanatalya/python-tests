import random

from faker import Faker

faker = Faker()


class RandomData:
    @staticmethod
    def get_random_int(start: int, end: int) -> int:
        return random.randrange(start, end)

    @staticmethod
    def get_random_float(start: float, end: float):
        return random.uniform(start, end)

    @staticmethod
    def get_random_special_symbol():
        return random.choice('!@#$%^&=+')  # ()*-. are not considered ad special symbols

    @staticmethod
    def get_username() -> str:
        return ''.join(faker.random_letters(length=random.randint(3, 15)))

    @staticmethod
    def get_password() -> str:
        upper_letters = [letter.upper() for letter in faker.random_letters(length=3)]
        lower_letters = [letter.lower() for letter in faker.random_letters(length=3)]
        digits = [faker.random_digit() for _ in range(3)]
        special = [RandomData.get_random_special_symbol()]    # ()*-. are not special symbols
        password = [str(letter) for letter in upper_letters + lower_letters + digits + special]
        random.shuffle(password)
        return ''.join(password)

    @staticmethod
    def get_faker(language="en_US") -> Faker:
        return Faker(language)
