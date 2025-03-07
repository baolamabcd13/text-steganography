import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import streamlit as st
from collections import Counter

class StegAnalyzer:
    def __init__(self):
        pass
    
    def analyze_text_changes(self, original_text, stego_text):
        """Phân tích sự thay đổi giữa văn bản gốc và văn bản đã ẩn thông tin"""
        results = {}
        
        # Tính toán độ dài
        results["original_length"] = len(original_text)
        results["stego_length"] = len(stego_text)
        results["length_difference"] = len(stego_text) - len(original_text)
        
        # Tính số ký tự khác nhau
        diff_chars = sum(1 for a, b in zip(original_text[:min(len(original_text), len(stego_text))], 
                                          stego_text[:min(len(original_text), len(stego_text))]) if a != b)
        results["different_chars"] = diff_chars
        
        # Tính tỷ lệ thay đổi
        if len(original_text) > 0:
            results["change_ratio"] = diff_chars / len(original_text)
        else:
            results["change_ratio"] = 0
        
        return results
    
    def analyze_zero_width(self, stego_text):
        """Phân tích các ký tự zero-width trong văn bản"""
        results = {}
        
        # Đếm số ký tự zero-width
        zwsp_count = stego_text.count('\u200B')  # Zero-width space
        zwj_count = stego_text.count('\u200D')   # Zero-width joiner
        zwnj_count = stego_text.count('\u200C')  # Zero-width non-joiner
        
        results["zwsp_count"] = zwsp_count
        results["zwj_count"] = zwj_count
        results["zwnj_count"] = zwnj_count
        results["total_zero_width"] = zwsp_count + zwj_count + zwnj_count
        
        # Tính tỷ lệ ký tự zero-width
        if len(stego_text) > 0:
            results["zero_width_ratio"] = results["total_zero_width"] / len(stego_text)
        else:
            results["zero_width_ratio"] = 0
        
        return results
    
    def analyze_unicode(self, stego_text, similar_chars_dict):
        """Phân tích các ký tự Unicode đặc biệt trong văn bản"""
        results = {}
        
        # Đếm số ký tự Unicode đặc biệt
        reverse_similar = {v: k for k, v in similar_chars_dict.items()}
        homoglyph_count = sum(1 for char in stego_text if char in reverse_similar)
        
        results["homoglyph_count"] = homoglyph_count
        
        # Tính tỷ lệ ký tự Unicode đặc biệt
        if len(stego_text) > 0:
            results["homoglyph_ratio"] = homoglyph_count / len(stego_text)
        else:
            results["homoglyph_ratio"] = 0
        
        return results
    
    def analyze_morse(self, stego_text):
        """Phân tích văn bản chứa mã Morse ẩn"""
        results = {}
        
        # Phân tích độ dài từ
        words = stego_text.split()
        if not words:
            results["short_words"] = 0
            results["long_words"] = 0
            results["short_long_ratio"] = 0
            return results
        
        # Đếm số từ ngắn (1-3 ký tự) và từ dài (4+ ký tự)
        short_words = sum(1 for word in words if len(word.strip('.,;:!?')) <= 3)
        long_words = sum(1 for word in words if len(word.strip('.,;:!?')) > 3)
        
        results["short_words"] = short_words
        results["long_words"] = long_words
        results["total_words"] = len(words)
        
        # Tính tỷ lệ từ ngắn/dài
        if len(words) > 0:
            results["short_words_ratio"] = short_words / len(words)
            results["long_words_ratio"] = long_words / len(words)
        else:
            results["short_words_ratio"] = 0
            results["long_words_ratio"] = 0
        
        # Tính tỷ lệ từ ngắn/dài (thông thường khoảng 0.5 nếu phân bố đều)
        if long_words > 0:
            results["short_long_ratio"] = short_words / long_words
        else:
            results["short_long_ratio"] = 0
        
        return results
    
    def calculate_entropy(self, text):
        """Tính entropy của văn bản (độ đo tính ngẫu nhiên)"""
        if not text:
            return 0
        
        # Đếm tần suất xuất hiện của mỗi ký tự
        counter = Counter(text)
        frequencies = np.array(list(counter.values())) / len(text)
        
        # Tính entropy
        entropy = -np.sum(frequencies * np.log2(frequencies))
        return entropy
    
    def plot_char_distribution(self, original_text, stego_text, top_n=10):
        """Tạo biểu đồ phân bố ký tự cho văn bản gốc và văn bản đã ẩn"""
        if not original_text or not stego_text:
            return None
        
        # Đếm tần suất xuất hiện của các ký tự
        original_counter = Counter(original_text)
        stego_counter = Counter(stego_text)
        
        # Lấy top_n ký tự phổ biến nhất từ cả hai văn bản
        top_chars = set()
        for char, _ in original_counter.most_common(top_n):
            top_chars.add(char)
        for char, _ in stego_counter.most_common(top_n):
            top_chars.add(char)
        
        # Tạo DataFrame cho biểu đồ
        data = []
        for char in top_chars:
            data.append({
                'Ký tự': char if char.isprintable() else f'U+{ord(char):04X}',
                'Số lượng': original_counter.get(char, 0),
                'Loại': 'Văn bản gốc'
            })
            data.append({
                'Ký tự': char if char.isprintable() else f'U+{ord(char):04X}',
                'Số lượng': stego_counter.get(char, 0),
                'Loại': 'Văn bản đã ẩn'
            })
        
        df = pd.DataFrame(data)
        
        # Tạo biểu đồ
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Nhóm theo loại và vẽ biểu đồ
        original_df = df[df['Loại'] == 'Văn bản gốc'].sort_values('Số lượng', ascending=False)
        stego_df = df[df['Loại'] == 'Văn bản đã ẩn'].sort_values('Số lượng', ascending=False)
        
        x = np.arange(len(top_chars))
        width = 0.35
        
        ax.bar(x - width/2, original_df['Số lượng'], width, label='Văn bản gốc')
        ax.bar(x + width/2, stego_df['Số lượng'], width, label='Văn bản đã ẩn')
        
        ax.set_xlabel('Ký tự')
        ax.set_ylabel('Số lượng')
        ax.set_title('So sánh phân bố ký tự')
        ax.set_xticks(x)
        ax.set_xticklabels(original_df['Ký tự'])
        ax.legend()
        
        plt.tight_layout()
        return fig
    
    def detect_steganography(self, text):
        """Phát hiện dấu hiệu của steganography trong văn bản"""
        results = {}
        
        # Kiểm tra Zero-width characters
        zwsp_count = text.count('\u200B')  # Zero-width space
        zwj_count = text.count('\u200D')   # Zero-width joiner
        zwnj_count = text.count('\u200C')  # Zero-width non-joiner
        
        results["has_zero_width"] = (zwsp_count + zwj_count + zwnj_count) > 0
        results["zero_width_count"] = zwsp_count + zwj_count + zwnj_count
        
        # Kiểm tra Unicode homoglyphs (cần danh sách homoglyphs)
        # Đây chỉ là kiểm tra cơ bản, cần cung cấp danh sách đầy đủ để kiểm tra chính xác
        suspicious_ranges = [
            (0x0370, 0x03FF),  # Greek and Coptic
            (0x0400, 0x04FF),  # Cyrillic
            (0x2000, 0x206F)   # General Punctuation (contains zero-width chars)
        ]
        
        homoglyph_count = 0
        for char in text:
            code_point = ord(char)
            for start, end in suspicious_ranges:
                if start <= code_point <= end:
                    homoglyph_count += 1
                    break
        
        results["suspicious_homoglyphs"] = homoglyph_count > 0
        results["homoglyph_count"] = homoglyph_count
        
        # Kiểm tra phân bố từ ngắn/dài bất thường (cho Morse)
        words = text.split()
        if words:
            short_words = sum(1 for word in words if len(word.strip('.,;:!?')) <= 3)
            long_words = sum(1 for word in words if len(word.strip('.,;:!?')) > 3)
            
            short_ratio = short_words / len(words) if len(words) > 0 else 0
            long_ratio = long_words / len(words) if len(words) > 0 else 0
            
            # Phân bố từ ngắn/dài bất thường (thường khoảng 0.5-0.6 cho văn bản tiếng Anh thông thường)
            results["unusual_word_distribution"] = abs(short_ratio - 0.55) > 0.2
            results["short_word_ratio"] = short_ratio
        else:
            results["unusual_word_distribution"] = False
            results["short_word_ratio"] = 0
        
        # Tính entropy
        entropy = self.calculate_entropy(text)
        results["entropy"] = entropy
        
        # Entropy cao bất thường có thể là dấu hiệu của steganography
        results["unusual_entropy"] = entropy > 4.5  # Ngưỡng này cần điều chỉnh dựa trên thử nghiệm
        
        # Kết luận tổng thể
        results["steganography_detected"] = (
            results["has_zero_width"] or 
            results["suspicious_homoglyphs"] or 
            results["unusual_word_distribution"] or
            results["unusual_entropy"]
        )
        
        return results