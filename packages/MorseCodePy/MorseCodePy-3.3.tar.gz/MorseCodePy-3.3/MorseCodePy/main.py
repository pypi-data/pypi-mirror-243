import logging
from time import sleep

from .audio_manager import AudioManager
from .codes import encodes, decodes, Language
from .utilities import *

# Setup logging
logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.WARNING)


def encode(string: str, language: Language, dot: str = '.', dash: str = '-', separator: str = '/',
           error: str = '*') -> str:
    """
    Encodes your string into Morse code.

    :parameter string: The input string to be encoded.
    :parameter language: The language to use for encoding (e.g., Language.english, Language.french, Language.numbers).
    :parameter dot: The symbol to represent dots.
    :parameter dash: The symbol to represent dashes.
    :parameter separator: The symbol used to separate words.
    :parameter error: The symbol to represent errors when a character is not found in the dictionary.

    :returns: The Morse code representation of the input string.
    """

    # Error handling: Ensure that dot, dash, and separator have only one symbol
    if any(len(symbol) != 1 for symbol in (dot, dash, separator)):
        logging.error(error_message1)
        return error_message1

    # Translating string into Morse code
    code: str = str()  # New string that will hold the translated text
    string = string.lower()  # Convert the input string to lowercase for consistent encoding

    char: int = 0
    while char != len(string):
        if string[char] == 'c' and string[char + 1] == 'h':
            code += '1111'.replace('1', dash) + ' '
            char += 1
        elif string[char] == ' ':
            code += separator + ' '
        elif string[char] in encodes[language]:
            morse_code = encodes[language][string[char]]
            code += morse_code.replace('0', dot).replace('1', dash) + ' '
        elif string[char] in encodes[Language.numbers] and language != Language.special:
            morse_code = encodes[Language.numbers][string[char]]
            code += morse_code.replace('0', dot).replace('1', dash) + ' '
        elif string[char] in encodes[Language.special] and language != Language.numbers:
            morse_code = encodes[Language.special][string[char]]
            code += morse_code.replace('0', dot).replace('1', dash) + ' '
        else:
            code += error + ' '

        char += 1

    return code.rstrip()


def decode(code: str, language: Language, dot: str = '.', dash: str = '-', separator: str = '/',
           error: str = '*') -> str:
    """
    Decode Morse code into a string.

    :parameter code: The input Morse code string to be decoded.
    :parameter language: The language to use for decoding (e.g., Language.russian, Language.spanish, Language.special).
    :parameter dot: The symbol used to represent dots.
    :parameter dash: The symbol used to represent dashes.
    :parameter separator: The symbol used to separate words.
    :parameter error: The symbol to represent errors when an unknown Morse code sequence is encountered.

    :returns: The decoded string.
    """

    # Error Handling: Ensure that dot, dash, and separator have only one symbol
    if any(len(symbol) != 1 for symbol in (dot, dash, separator)):
        logging.error(error_message1)
        return error_message1

    # Error Handling: Ensure that the input string contains only valid Morse code symbols
    if any(char not in dot + dash + separator + ' ' + '\n' for char in code):
        logging.error(error_message2)
        return error_message2

    # Separating String: Split the input Morse code into letters and separators
    letters: list[str] = separate_words(code, dot, dash, separator)

    # Translating Morse Code into normal text
    string: str = ''

    # Create dictionaries to map Morse code to characters for the selected language
    reversed_codes: dict = reversed_dictionary(decodes[language])
    reversed_numbers_dictionary: dict = reversed_dictionary(decodes[Language.numbers])
    reversed_special_dictionary: dict = reversed_dictionary(decodes[Language.special])

    # Create a mapping dictionary to translate Morse code symbols to '0' and '1'
    mapping: dict[str: str] = {dot: '0', dash: '1'}

    for letter in letters:
        # Translate Morse code symbols to '0' and '1'
        letter = str().join(mapping.get(char, char) for char in letter)

        if letter == '1111' and language in {Language.english, Language.spanish, Language.french}:
            string += 'ch'
        elif letter == separator:
            string += ' '
        elif letter == '\n':
            string += '\n'
        elif letter in reversed_codes:
            string += reversed_codes[letter]
        elif letter in reversed_numbers_dictionary and language != Language.special:
            string += reversed_numbers_dictionary[letter]
        elif letter in reversed_special_dictionary and language != Language.numbers:
            string += reversed_special_dictionary[letter]
        else:
            string += error

    return string


def chart(dot: str = '·', dash: str = '-') -> None:
    """
    Print Morse code chart in the console.

    :parameter dot: The symbol to represent dots in the chart.
    :parameter dash: The symbol to represent dashes in the chart.

    :returns: None
    """

    print('Morse Code Chart\n')
    print('-' * 15)

    # Iterate through the language codes and their corresponding characters
    for language, codes in encodes.items():
        print()
        print(language.name.capitalize())

        # Print characters and their Morse code representations
        for char, code in codes.items():
            if code not in ('\n', ' '):
                code = code.replace('0', dot).replace('1', dash)
                print(f'{char:<5} {code:<15}')

        print()
        print('-' * 15)


def play(code: str, delay: float = 0.4, dot: str = '.', dash: str = '-', separator: str = '/') -> None:
    """
    Play Morse code sound.

    :parameter code: The Morse code string to play.
    :parameter delay: The delay in seconds between each Morse code symbol (default is 0.4).
    :parameter dot: Symbol representing a dot (default is '.').
    :parameter dash: Symbol representing a dash (default is '-').
    :parameter separator: Symbol representing a separator (default is '/').

    :returns: None
    """

    # Ensure that delay has only 2 numbers after the comma
    delay = round(delay, 2)

    # Error Handling: Ensure that dot, dash, and separator have only one symbol
    if any(len(symbol) != 1 for symbol in (dot, dash, separator)):
        logging.error(error_message1)
        return error_message1

    # Error Handling: Ensure that the input string contains only valid Morse code symbols
    if any(char not in dot + dash + separator + ' ' + '\n' for char in code):
        logging.error(error_message2)
        return error_message2

    if delay > 1.0:
        logging.warning(warning_message1)

    # Separate the string into individual Morse code characters
    characters: list[str] = separate_letters(separate_words(code, dot, dash, separator, sound_mode=True))

    try:
        audio_manager = AudioManager()  # Initialize audio manager

        # Play Morse code
        for character in characters:
            match character:
                case '.':
                    audio_manager.play_dot()
                    sleep(delay / 2.0)
                case '-':
                    audio_manager.play_dash()
                    sleep(delay)
                case ' ':
                    sleep(delay * 1.8)
                case '/':
                    sleep(delay * 2.0)
    except KeyboardInterrupt:
        logging.error(error_message3)
