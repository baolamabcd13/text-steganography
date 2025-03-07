class UnicodeSteg:
    def __init__(self):
        # Sử dụng các ký tự Unicode đặc biệt để ẩn thông tin
        # Homoglyphs: các ký tự trông giống nhau nhưng có mã Unicode khác nhau
        self.normal_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
        self.similar_chars = {
            'A': 'Α', 'B': 'Β', 'C': 'Ϲ', 'E': 'Ε', 'H': 'Η', 'I': 'Ι', 'J': 'Ј', 
            'K': 'Κ', 'M': 'Μ', 'N': 'Ν', 'O': 'Ο', 'P': 'Ρ', 'S': 'Ѕ', 'T': 'Τ', 
            'X': 'Χ', 'Y': 'Υ', 'Z': 'Ζ',
            'a': 'а', 'c': 'с', 'e': 'е', 'i': 'і', 'j': 'ј', 'o': 'о', 'p': 'р', 
            's': 'ѕ', 'x': 'х', 'y': 'у'
        }
        
        # Đảo ngược bảng để decode
        self.reverse_similar = {v: k for k, v in self.similar_chars.items()}

    def text_to_binary(self, text):
        """Chuyển đổi văn bản thành chuỗi nhị phân"""
        binary = ''.join(format(ord(char), '08b') for char in text)
        return binary
    
    def binary_to_text(self, binary):
        """Chuyển đổi chuỗi nhị phân thành văn bản"""
        text = ''
        for i in range(0, len(binary), 8):
            if i + 8 <= len(binary):
                byte = binary[i:i+8]
                text += chr(int(byte, 2))
        return text

    def hide(self, cover_text, secret_message):
        """Ẩn thông điệp bí mật sử dụng homoglyphs Unicode"""
        binary_secret = self.text_to_binary(secret_message)
        bit_index = 0
        steganographic_text = ''
        
        for char in cover_text:
            if char in self.similar_chars and bit_index < len(binary_secret):
                # Nếu ký tự có thể thay thế và còn bit để ẩn
                if binary_secret[bit_index] == '1':
                    # Sử dụng homoglyph nếu bit là 1
                    steganographic_text += self.similar_chars[char]
                else:
                    # Giữ nguyên ký tự nếu bit là 0
                    steganographic_text += char
                bit_index += 1
            else:
                steganographic_text += char
        
        # Kiểm tra xem đã ẩn hết thông điệp chưa
        if bit_index < len(binary_secret):
            return "Văn bản gốc quá ngắn để ẩn toàn bộ thông điệp"
        
        return steganographic_text

    def extract(self, steganographic_text):
        """Trích xuất thông điệp bí mật từ văn bản sử dụng homoglyphs Unicode"""
        binary = ''
        
        for char in steganographic_text:
            if char in self.reverse_similar:
                # Nếu tìm thấy homoglyph, bit là 1
                binary += '1'
            elif char in self.similar_chars:
                # Nếu tìm thấy ký tự gốc có thể thay thế, bit là 0
                binary += '0'
        
        # Cắt binary thành các byte và chuyển đổi thành văn bản
        # Tìm số byte hoàn chỉnh
        num_bytes = len(binary) // 8
        binary = binary[:num_bytes * 8]
        
        return self.binary_to_text(binary)