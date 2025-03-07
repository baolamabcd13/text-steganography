class MorseSteg:
    def __init__(self):
        # Bảng mã Morse
        self.morse_code_dict = {
            'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 
            'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..', 
            'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.', 
            'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 
            'Y': '-.--', 'Z': '--..', '1': '.----', '2': '..---', '3': '...--', 
            '4': '....-', '5': '.....', '6': '-....', '7': '--...', '8': '---..', 
            '9': '----.', '0': '-----', ' ': '/'
        }
        
        # Đảo ngược bảng mã Morse để decode
        self.reverse_morse_dict = {v: k for k, v in self.morse_code_dict.items()}
        
        # Từ ngắn (1-3 ký tự) và từ dài (4+ ký tự) để biểu diễn dấu chấm và gạch ngang
        self.short_words = []
        self.long_words = []

    def load_word_lists(self, short_words_file=None, long_words_file=None):
        """Tải danh sách từ ngắn và từ dài từ file"""
        if short_words_file:
            with open(short_words_file, 'r', encoding='utf-8') as f:
                self.short_words = [line.strip() for line in f]
        else:
            # Danh sách mặc định các từ ngắn
            self.short_words = ["a", "an", "at", "as", "by", "he", "hi", "in", "is", "it", 
                               "me", "my", "no", "of", "on", "or", "so", "to", "up", "us", "we"]
        
        if long_words_file:
            with open(long_words_file, 'r', encoding='utf-8') as f:
                self.long_words = [line.strip() for line in f]
        else:
            # Danh sách mặc định các từ dài
            self.long_words = ["about", "above", "across", "actually", "although", "always",
                              "america", "another", "because", "between", "business", "company",
                              "consider", "different", "important", "information", "something"]
    
    def text_to_morse(self, text):
        """Chuyển đổi văn bản thành mã Morse"""
        morse = []
        for char in text.upper():
            if char in self.morse_code_dict:
                morse.append(self.morse_code_dict[char])
        return ' '.join(morse)
    
    def morse_to_text(self, morse):
        """Chuyển đổi mã Morse thành văn bản"""
        text = ''
        morse_chars = morse.split(' ')
        for char in morse_chars:
            if char in self.reverse_morse_dict:
                text += self.reverse_morse_dict[char]
        return text
    
    def hide(self, secret_message):
        """Ẩn thông điệp bí mật sử dụng từ ngắn/dài để biểu diễn mã Morse"""
        if not self.short_words or not self.long_words:
            self.load_word_lists()
        
        morse = self.text_to_morse(secret_message)
        
        import random
        steganographic_text = []
        
        for symbol in morse:
            if symbol == '.':
                steganographic_text.append(random.choice(self.short_words))
            elif symbol == '-':
                steganographic_text.append(random.choice(self.long_words))
            elif symbol == ' ':
                steganographic_text.append(',')
            elif symbol == '/':
                steganographic_text.append('.')
        
        return ' '.join(steganographic_text)
    
    def extract(self, steganographic_text):
        """Trích xuất thông điệp bí mật từ văn bản sử dụng từ ngắn/dài"""
        if not self.short_words or not self.long_words:
            self.load_word_lists()
        
        words = steganographic_text.replace('.', ' . ').replace(',', ' , ').split()
        
        morse = ''
        for word in words:
            if word == ',':
                morse += ' '
            elif word == '.':
                morse += '/ '
            elif len(word.strip('.,;:!?')) <= 3:
                morse += '.'
            else:
                morse += '-'
        
        return self.morse_to_text(morse)