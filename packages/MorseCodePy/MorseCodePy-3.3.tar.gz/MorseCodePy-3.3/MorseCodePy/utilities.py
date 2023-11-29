# Define error messages
error_message1: str = 'Invalid symbols: Dots, dashes, and separators must be single characters!'
error_message2: str = 'Invalid characters: Use only specified dots, dashes, spaces, and separators!'
error_message3: str = 'KeyboardInterrupt: Morse code playback interrupted by user.'
warning_message1: str = 'Long delay: The specified delay is longer than recommended (1 second). Playback may be slower than expected.'


def separate_words(words: str, dot: str, dash: str, separator: str, sound_mode: bool = False) -> list[str]:
    """
    Separate a string into Morse code letters.

    :parameter words: The input string to be processed.
    :parameter dot: The symbol to represent dots.
    :parameter dash: The symbol to represent dashes.
    :parameter separator: The symbol used to separate words.
    :parameter sound_mode: A flag to include space characters when sound mode is enabled (default is False).

    :returns: A list of Morse code letters.
    """

    letters: list = []
    current_element: str = ''

    for char in words:
        if char in (dot, dash):
            current_element += char
        elif char == separator:
            if current_element:
                letters.append(current_element)
                current_element = ''
            letters.append(separator)
        elif char == ' ':
            if current_element:
                letters.append(current_element)
                current_element = ''
            if sound_mode:
                letters.append(' ')
        else:
            current_element += char

    if current_element:
        letters.append(current_element)

    return letters


def separate_letters(letters: list[str]) -> list[str]:
    """
    Separate Morse code letters into individual characters.

    :parameter letters: The input list to be processed.

    :returns: A list of individual Morse code characters.
    """

    return [char for letter in letters for char in letter]


def reversed_dictionary(dictionary: dict) -> dict:
    """
    Reverse the keys and values of a dictionary.

    :param dictionary: The input dictionary to be processed.

    :return: A dictionary with reversed keys and values.
    """

    return {value: key for key, value in dictionary.items()}
