

class MorseCodeTranslator:
    
    def __init__(self):
        self.MORSE_CODE_DICT = {'A':   '.-',
         'B':   '-...',
         'C':   '-.-.',
         'CH':  '----',
         'D':   '-..',
         'E':   '.',
         'F':   '..-.',
         'G':   '--.',
         'H':   '....',
         'I':   '..',
         'J':   '.---',
         'K':   '-.-',
         'L':   '.-..',
         'M':   '--',
         'N':   '-.',
         'Ñ':   '--.--',
         'O':   '---',
         'P':   '.--.',
         'Q':   '--.-',
         'R':   '.-.',
         'S':   '...',
         'T':   '-',
         'U':   '..-',
         'V':   '...-',
         'W':   '.--',
         'X':   '-..-',
         'Y':   '-.--',
         'Z':   '--..',
         '0':   '-----',
         '1':   '.----',
         '2':   '..---',
         '3':   '...--',
         '4':   '....-',
         '5':   '.....',
         '6':   '-....',
         '7':   '--...',
         '8':   '---..',
         '9':   '----.',
         '.':   '.-.-.-',
         ',':   '--..--',
         '?':   '..--..',
         '"':   '.-..-.',
         "'":   '.----.',
         '!':   '-.-.--',
         '/':   '-..-.',
         '(':   '-.--.',
         ')':   '-.--.-',
         '&':   '.-...',
         ':':   '---...',
         ';':   '-.-.-.',
         '=':   '-...-',
         '+':   '.-.-.',
         '-':   '-....-',
         '_':   '..--.-',
         'ERROR':'........'
        }


    def enconde_to_morse(self,phrase):
        morse_code = []
        for letter in phrase:
            element = letter.upper()
            if element in self.MORSE_CODE_DICT.keys():
                morse_value = self.MORSE_CODE_DICT[element]
            else:
                morse_value = ''
            morse_code.append(morse_value)
        
        return ' '.join(morse_code)
    
    def decode_morse_code(self,morse):
        morse_code = morse.split(' ')
        phrase = ''
        for element in morse_code:
            if element in self.MORSE_CODE_DICT.values():
                phrase += list(self.MORSE_CODE_DICT.keys())[list(self.MORSE_CODE_DICT.values()).index(element)]
            else:
                phrase += ' '
        return phrase

if __name__ == "__main__":
    morse = MorseCodeTranslator()
    print(morse.enconde_to_morse('hello'))
    print(morse.decode_morse_code('.... . .-.. .-.. ---'))