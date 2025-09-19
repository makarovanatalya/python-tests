import random

from faker import Faker

faker = Faker()


class RandomData:
    @staticmethod
    def get_username() -> str:
        return ''.join(faker.random_letters(length=random.randint(3, 15)))

    @staticmethod
    def get_password() -> str:
        upper_letters = [letter.upper() for letter in faker.random_letters(length=3)]
        lower_letters = [letter.lower() for letter in faker.random_letters(length=3)]
        digits = [faker.random_digit() for _ in range(3)]
        special = [random.choice('!@#$%^&=+')]    # ()*-. are not special symbols
        password = [str(letter) for letter in upper_letters + lower_letters + digits + special]
        random.shuffle(password)
        return ''.join(password)
