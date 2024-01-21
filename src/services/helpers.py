from random import choice, randint
from string import ascii_letters, ascii_lowercase, ascii_uppercase, printable, digits, punctuation


class RandomStringCreator:
    def __init__(self, length, add_special_char=False, add_big_letter=False):
        self.length: int = length
        self.__basic_set = ascii_letters + digits
        self.add_special_char: bool = add_special_char
        self.add_big_letter: bool = add_big_letter
        self.separation_char: str | None = None
        self.separation_indexes: tuple[int] | tuple = ()

    def change_basic_set(self, set_name):
        match set_name:
            case 'small letters':
                self.__basic_set = ascii_lowercase
            case 'letters':
                self.__basic_set = ascii_letters
            case 'numeric':
                self.__basic_set = digits
            case 'alphanumeric':
                self.__basic_set = ascii_letters + digits
            case 'all despite whitespace':
                self.__basic_set = ascii_letters + digits
            case 'all printable':
                self.__basic_set = printable
            case _:
                raise Exception('Invalid set name')

    def create_string(self) -> str:
        characters_list = [choice(self.__basic_set) for _ in range(self.length)]
        if self.add_special_char is True:
            string_length = len(characters_list)
            characters_index = randint(0, string_length - 1)
            characters_list[characters_index] = choice(punctuation)
        if self.add_big_letter is True:
            string_length = len(characters_list)
            characters_index = randint(0, string_length - 1)
            characters_list[characters_index] = choice(ascii_uppercase)
        if self.separation_char is not None:
            for index in self.separation_indexes:
                characters_list.insert(index, self.separation_char)
        random_string = ''.join(characters_list)
        return random_string
