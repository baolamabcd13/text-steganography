class ZeroWidthSteg:
    def __init__(self):
        # Định nghĩa các ký tự zero-width
        self.zwsp = '\u200B'  # Zero-width space (bit 0)
        self.zwj = '\u200D'   # Zero-width joiner (bit 1)
        self.zwnj = '\u200C'  # Zero-width non-joiner (delimiter)

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
        """Ẩn thông điệp bí mật vào văn bản"""
        if not cover_text or not secret_message:
            return "Văn bản gốc và thông điệp bí mật không được để trống"
        
        binary_secret = self.text_to_binary(secret_message)
        
        # Thêm delimiter vào đầu và cuối để dễ dàng trích xuất
        steganographic_text = cover_text[0]
        steganographic_text += self.zwnj  # Bắt đầu thông điệp bí mật
        
        # Chèn các ký tự zero-width để biểu diễn thông điệp bí mật
        for bit in binary_secret:
            if bit == '0':
                steganographic_text += self.zwsp
            else:
                steganographic_text += self.zwj
        
        steganographic_text += self.zwnj  # Kết thúc thông điệp bí mật
        steganographic_text += cover_text[1:]
        
        return steganographic_text

    def extract(self, steganographic_text):
        """Trích xuất thông điệp bí mật từ văn bản"""
        if not steganographic_text:
            return "Văn bản không được để trống"
        
        # Tìm vị trí của các delimiter
        parts = steganographic_text.split(self.zwnj)
        if len(parts) < 3:
            return "Không tìm thấy thông điệp bí mật"
        
        # Phần giữa hai delimiter chứa thông điệp bí mật
        hidden_part = parts[1]
        
        binary = ''
        for char in hidden_part:
            if char == self.zwsp:
                binary += '0'
            elif char == self.zwj:
                binary += '1'
        
        # Chuyển đổi nhị phân thành văn bản
        return self.binary_to_text(binary)