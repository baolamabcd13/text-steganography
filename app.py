import streamlit as st
import pyperclip
import matplotlib.pyplot as plt
from src.zero_width_steg import ZeroWidthSteg
from src.morse_steg import MorseSteg
from src.unicode_steg import UnicodeSteg
from src.encryption import Encryptor
from src.analyzer import StegAnalyzer  # Import module phân tích mới

# Khởi tạo các phương pháp steganography, encryptor và analyzer
zero_width_steg = ZeroWidthSteg()
morse_steg = MorseSteg()
unicode_steg = UnicodeSteg()
encryptor = Encryptor()
analyzer = StegAnalyzer()  # Khởi tạo analyzer

# Thiết lập trang
st.set_page_config(
    page_title="Ứng dụng Ẩn Văn bản trong Văn bản",
    page_icon="🔒",
    layout="wide"
)

# Hàm sao chép văn bản vào clipboard
def copy_to_clipboard(text):
    pyperclip.copy(text)
    st.success("Đã sao chép vào clipboard!")

# Tiêu đề ứng dụng
st.title("Ứng dụng Ẩn Văn bản trong Văn bản")
st.markdown("---")

# Tạo tabs cho các phương pháp khác nhau và tab phân tích
tab1, tab2, tab3, tab4 = st.tabs(["Zero-width Characters", "Mã Morse Ẩn", "Unicode Steganography", "Phân tích"])

# Tab 1: Zero-width Characters
with tab1:
    st.header("Phương pháp Zero-width Characters")
    
    # Tạo 2 cột cho ẩn và trích xuất
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Ẩn thông điệp")
        
        cover_text = st.text_area("Văn bản gốc:", height=150, key="zw_cover")
        secret_text = st.text_area("Thông điệp bí mật:", height=100, key="zw_secret")
        
        # Thêm tùy chọn mật khẩu
        use_password = st.checkbox("Sử dụng mật khẩu bảo vệ", key="zw_use_password")
        password = ""
        if use_password:
            password = st.text_input("Nhập mật khẩu:", type="password", key="zw_password")
        
        # Tạo hai cột cho nút ẩn thông điệp và nút sao chép
        hide_col1, hide_col2 = st.columns([1, 1])
        
        with hide_col1:
            hide_button = st.button("Ẩn thông điệp", key="zw_hide_btn")
        
        # Xử lý khi nhấn nút ẩn thông điệp
        if hide_button:
            if not cover_text or not secret_text:
                st.error("Vui lòng nhập cả văn bản gốc và thông điệp bí mật")
            elif use_password and not password:
                st.error("Vui lòng nhập mật khẩu")
            else:
                try:
                    # Mã hóa thông điệp nếu sử dụng mật khẩu
                    message_to_hide = secret_text
                    if use_password:
                        message_to_hide = encryptor.encrypt(secret_text, password)
                    
                    result = zero_width_steg.hide(cover_text, message_to_hide)
                    st.session_state.zw_result = result
                    st.text_area("Kết quả:", value=result, height=150, key="zw_result_area")
                    st.success("Đã ẩn thông điệp thành công!")
                except Exception as e:
                    st.error(f"Đã xảy ra lỗi: {str(e)}")
        
        # Hiển thị nút sao chép nếu đã có kết quả
        with hide_col2:
            if 'zw_result' in st.session_state:
                if st.button("Sao chép kết quả", key="zw_copy_btn"):
                    copy_to_clipboard(st.session_state.zw_result)
    
    with col2:
        st.subheader("Trích xuất thông điệp")
        
        stego_text = st.text_area("Văn bản chứa thông điệp ẩn:", height=150, key="zw_stego")
        
        # Thêm tùy chọn mật khẩu cho giải mã
        is_encrypted = st.checkbox("Thông điệp được bảo vệ bằng mật khẩu", key="zw_is_encrypted")
        decrypt_password = ""
        if is_encrypted:
            decrypt_password = st.text_input("Nhập mật khẩu để giải mã:", type="password", key="zw_decrypt_password")
        
        # Tạo hai cột cho nút trích xuất và nút sao chép
        extract_col1, extract_col2 = st.columns([1, 1])
        
        with extract_col1:
            extract_button = st.button("Trích xuất thông điệp", key="zw_extract_btn")
        
        # Xử lý khi nhấn nút trích xuất
        if extract_button:
            if not stego_text:
                st.error("Vui lòng nhập văn bản chứa thông điệp ẩn")
            elif is_encrypted and not decrypt_password:
                st.error("Vui lòng nhập mật khẩu để giải mã")
            else:
                try:
                    extracted_message = zero_width_steg.extract(stego_text)
                    
                    # Giải mã nếu thông điệp được mã hóa
                    if is_encrypted:
                        try:
                            extracted_message = encryptor.decrypt(extracted_message, decrypt_password)
                        except ValueError:
                            st.error("Mật khẩu không đúng hoặc thông điệp không được mã hóa")
                            extracted_message = "Lỗi giải mã: Mật khẩu không đúng hoặc thông điệp không được mã hóa"
                    
                    st.session_state.zw_extracted = extracted_message
                    st.text_area("Thông điệp được trích xuất:", value=extracted_message, height=100, key="zw_extracted_area")
                    st.success("Đã trích xuất thông điệp thành công!")
                except Exception as e:
                    st.error(f"Đã xảy ra lỗi: {str(e)}")
        
        # Hiển thị nút sao chép nếu đã có kết quả trích xuất
        with extract_col2:
            if 'zw_extracted' in st.session_state:
                if st.button("Sao chép kết quả", key="zw_copy_extract_btn"):
                    copy_to_clipboard(st.session_state.zw_extracted)

# Tab 2: Mã Morse Ẩn
with tab2:
    st.header("Phương pháp Mã Morse Ẩn")
    
    # Tạo 2 cột cho ẩn và trích xuất
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Ẩn thông điệp bằng Mã Morse")
        
        morse_secret = st.text_area("Thông điệp bí mật:", height=100, key="morse_secret")
        
        # Thêm tùy chọn mật khẩu
        morse_use_password = st.checkbox("Sử dụng mật khẩu bảo vệ", key="morse_use_password")
        morse_password = ""
        if morse_use_password:
            morse_password = st.text_input("Nhập mật khẩu:", type="password", key="morse_password")
        
        # Tạo hai cột cho nút tạo văn bản ẩn và nút sao chép
        morse_hide_col1, morse_hide_col2 = st.columns([1, 1])
        
        with morse_hide_col1:
            morse_hide_button = st.button("Tạo văn bản ẩn", key="morse_hide_btn")
        
        # Xử lý khi nhấn nút tạo văn bản ẩn
        if morse_hide_button:
            if not morse_secret:
                st.error("Vui lòng nhập thông điệp bí mật")
            elif morse_use_password and not morse_password:
                st.error("Vui lòng nhập mật khẩu")
            else:
                try:
                    # Mã hóa thông điệp nếu sử dụng mật khẩu
                    message_to_hide = morse_secret
                    if morse_use_password:
                        message_to_hide = encryptor.encrypt(morse_secret, morse_password)
                    
                    morse_steg.load_word_lists()  # Đảm bảo danh sách từ được tải
                    result = morse_steg.hide(message_to_hide)
                    st.session_state.morse_result = result
                    st.text_area("Kết quả (văn bản chứa mã Morse ẩn):", value=result, height=150, key="morse_result_area")
                    st.success("Đã tạo văn bản ẩn thành công!")
                except Exception as e:
                    st.error(f"Đã xảy ra lỗi: {str(e)}")
        
        # Hiển thị nút sao chép nếu đã có kết quả
        with morse_hide_col2:
            if 'morse_result' in st.session_state:
                if st.button("Sao chép kết quả", key="morse_copy_btn"):
                    copy_to_clipboard(st.session_state.morse_result)
    
    with col2:
        st.subheader("Trích xuất thông điệp từ Mã Morse ẩn")
        
        morse_stego = st.text_area("Văn bản chứa mã Morse ẩn:", height=150, key="morse_stego")
        
        # Thêm tùy chọn mật khẩu cho giải mã
        morse_is_encrypted = st.checkbox("Thông điệp được bảo vệ bằng mật khẩu", key="morse_is_encrypted")
        morse_decrypt_password = ""
        if morse_is_encrypted:
            morse_decrypt_password = st.text_input("Nhập mật khẩu để giải mã:", type="password", key="morse_decrypt_password")
        
        # Tạo hai cột cho nút trích xuất và nút sao chép
        morse_extract_col1, morse_extract_col2 = st.columns([1, 1])
        
        with morse_extract_col1:
            morse_extract_button = st.button("Trích xuất thông điệp", key="morse_extract_btn")
        
        # Xử lý khi nhấn nút trích xuất
        if morse_extract_button:
            if not morse_stego:
                st.error("Vui lòng nhập văn bản chứa mã Morse ẩn")
            elif morse_is_encrypted and not morse_decrypt_password:
                st.error("Vui lòng nhập mật khẩu để giải mã")
            else:
                try:
                    morse_steg.load_word_lists()  # Đảm bảo danh sách từ được tải
                    extracted_message = morse_steg.extract(morse_stego)
                    
                    # Giải mã nếu thông điệp được mã hóa
                    if morse_is_encrypted:
                        try:
                            extracted_message = encryptor.decrypt(extracted_message, morse_decrypt_password)
                        except ValueError:
                            st.error("Mật khẩu không đúng hoặc thông điệp không được mã hóa")
                            extracted_message = "Lỗi giải mã: Mật khẩu không đúng hoặc thông điệp không được mã hóa"
                    
                    st.session_state.morse_extracted = extracted_message
                    st.text_area("Thông điệp được trích xuất:", value=extracted_message, height=100, key="morse_extracted_area")
                    st.success("Đã trích xuất thông điệp thành công!")
                except Exception as e:
                    st.error(f"Đã xảy ra lỗi: {str(e)}")
        
        # Hiển thị nút sao chép nếu đã có kết quả trích xuất
        with morse_extract_col2:
            if 'morse_extracted' in st.session_state:
                if st.button("Sao chép kết quả", key="morse_copy_extract_btn"):
                    copy_to_clipboard(st.session_state.morse_extracted)

# Tab 3: Unicode Steganography
with tab3:
    st.header("Phương pháp Unicode Steganography")
    
    # Tạo 2 cột cho ẩn và trích xuất
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Ẩn thông điệp bằng Unicode")
        
        unicode_cover = st.text_area("Văn bản gốc:", height=150, key="unicode_cover")
        unicode_secret = st.text_area("Thông điệp bí mật:", height=100, key="unicode_secret")
        
        # Thêm tùy chọn mật khẩu
        unicode_use_password = st.checkbox("Sử dụng mật khẩu bảo vệ", key="unicode_use_password")
        unicode_password = ""
        if unicode_use_password:
            unicode_password = st.text_input("Nhập mật khẩu:", type="password", key="unicode_password")
        
        # Tạo hai cột cho nút ẩn thông điệp và nút sao chép
        unicode_hide_col1, unicode_hide_col2 = st.columns([1, 1])
        
        with unicode_hide_col1:
            unicode_hide_button = st.button("Ẩn thông điệp", key="unicode_hide_btn")
        
        # Xử lý khi nhấn nút ẩn thông điệp
        if unicode_hide_button:
            if not unicode_cover or not unicode_secret:
                st.error("Vui lòng nhập cả văn bản gốc và thông điệp bí mật")
            elif unicode_use_password and not unicode_password:
                st.error("Vui lòng nhập mật khẩu")
            else:
                try:
                    # Mã hóa thông điệp nếu sử dụng mật khẩu
                    message_to_hide = unicode_secret
                    if unicode_use_password:
                        message_to_hide = encryptor.encrypt(unicode_secret, unicode_password)
                    
                    result = unicode_steg.hide(unicode_cover, message_to_hide)
                    st.session_state.unicode_result = result
                    st.text_area("Kết quả:", value=result, height=150, key="unicode_result_area")
                    st.success("Đã ẩn thông điệp thành công!")
                except Exception as e:
                    st.error(f"Đã xảy ra lỗi: {str(e)}")
        
        # Hiển thị nút sao chép nếu đã có kết quả
        with unicode_hide_col2:
            if 'unicode_result' in st.session_state:
                if st.button("Sao chép kết quả", key="unicode_copy_btn"):
                    copy_to_clipboard(st.session_state.unicode_result)
    
    with col2:
        st.subheader("Trích xuất thông điệp từ Unicode")
        
        unicode_stego = st.text_area("Văn bản chứa thông điệp ẩn:", height=150, key="unicode_stego")
        
        # Thêm tùy chọn mật khẩu cho giải mã
        unicode_is_encrypted = st.checkbox("Thông điệp được bảo vệ bằng mật khẩu", key="unicode_is_encrypted")
        unicode_decrypt_password = ""
        if unicode_is_encrypted:
            unicode_decrypt_password = st.text_input("Nhập mật khẩu để giải mã:", type="password", key="unicode_decrypt_password")
        
        # Tạo hai cột cho nút trích xuất và nút sao chép
        unicode_extract_col1, unicode_extract_col2 = st.columns([1, 1])
        
        with unicode_extract_col1:
            unicode_extract_button = st.button("Trích xuất thông điệp", key="unicode_extract_btn")
        
        # Xử lý khi nhấn nút trích xuất
        if unicode_extract_button:
            if not unicode_stego:
                st.error("Vui lòng nhập văn bản chứa thông điệp ẩn")
            elif unicode_is_encrypted and not unicode_decrypt_password:
                st.error("Vui lòng nhập mật khẩu để giải mã")
            else:
                try:
                    extracted_message = unicode_steg.extract(unicode_stego)
                    
                    # Giải mã nếu thông điệp được mã hóa
                    if unicode_is_encrypted:
                        try:
                            extracted_message = encryptor.decrypt(extracted_message, unicode_decrypt_password)
                        except ValueError:
                            st.error("Mật khẩu không đúng hoặc thông điệp không được mã hóa")
                            extracted_message = "Lỗi giải mã: Mật khẩu không đúng hoặc thông điệp không được mã hóa"
                    
                    st.session_state.unicode_extracted = extracted_message
                    st.text_area("Thông điệp được trích xuất:", value=extracted_message, height=100, key="unicode_extracted_area")
                    st.success("Đã trích xuất thông điệp thành công!")
                except Exception as e:
                    st.error(f"Đã xảy ra lỗi: {str(e)}")
        
        # Hiển thị nút sao chép nếu đã có kết quả trích xuất
        with unicode_extract_col2:
            if 'unicode_extracted' in st.session_state:
                if st.button("Sao chép kết quả", key="unicode_copy_extract_btn"):
                    copy_to_clipboard(st.session_state.unicode_extracted)

# Tab 4: Phân tích
with tab4:
    st.header("Phân tích Steganography")
    
    analysis_type = st.radio(
        "Chọn loại phân tích:",
        ["So sánh văn bản", "Phát hiện Steganography"]
    )
    
    if analysis_type == "So sánh văn bản":
        st.subheader("So sánh văn bản gốc và văn bản đã ẩn thông tin")
        
        col1, col2 = st.columns(2)
        
        with col1:
            original_text = st.text_area("Văn bản gốc:", height=150, key="analysis_original")
        
        with col2:
            stego_text = st.text_area("Văn bản đã ẩn thông tin:", height=150, key="analysis_stego")
        
        steg_method = st.selectbox(
            "Phương pháp ẩn thông tin được sử dụng:",
            ["Zero-width Characters", "Mã Morse Ẩn", "Unicode Steganography"]
        )
        
        if st.button("Phân tích", key="analyze_btn"):
            if not original_text or not stego_text:
                st.error("Vui lòng nhập cả văn bản gốc và văn bản đã ẩn thông tin")
            else:
                # Phân tích chung
                general_results = analyzer.analyze_text_changes(original_text, stego_text)
                
                # Phân tích cụ thể theo phương pháp
                specific_results = {}
                if steg_method == "Zero-width Characters":
                    specific_results = analyzer.analyze_zero_width(stego_text)
                elif steg_method == "Mã Morse Ẩn":
                    specific_results = analyzer.analyze_morse(stego_text)
                elif steg_method == "Unicode Steganography":
                    specific_results = analyzer.analyze_unicode(stego_text, unicode_steg.similar_chars)
                
                # Tính entropy
                original_entropy = analyzer.calculate_entropy(original_text)
                stego_entropy = analyzer.calculate_entropy(stego_text)
                
                # Hiển thị kết quả
                st.subheader("Kết quả phân tích")
                
                # Tạo 3 cột để hiển thị kết quả
                res_col1, res_col2, res_col3 = st.columns(3)
                
                with res_col1:
                    st.write("**Thông tin cơ bản:**")
                    st.write(f"- Độ dài văn bản gốc: {general_results['original_length']} ký tự")
                    st.write(f"- Độ dài văn bản đã ẩn: {general_results['stego_length']} ký tự")
                    st.write(f"- Chênh lệch độ dài: {general_results['length_difference']} ký tự")
                    st.write(f"- Số ký tự khác nhau: {general_results['different_chars']}")
                    st.write(f"- Tỷ lệ thay đổi: {general_results['change_ratio']:.2%}")
                
                with res_col2:
                    st.write("**Thông tin entropy:**")
                    st.write(f"- Entropy văn bản gốc: {original_entropy:.4f}")
                    st.write(f"- Entropy văn bản đã ẩn: {stego_entropy:.4f}")
                    st.write(f"- Chênh lệch entropy: {stego_entropy - original_entropy:.4f}")
                
                with res_col3:
                    st.write("**Thông tin cụ thể:**")
                    if steg_method == "Zero-width Characters":
                        st.write(f"- Số ký tự zero-width space: {specific_results['zwsp_count']}")
                        st.write(f"- Số ký tự zero-width joiner: {specific_results['zwj_count']}")
                        st.write(f"- Số ký tự zero-width non-joiner: {specific_results['zwnj_count']}")
                        st.write(f"- Tổng số ký tự zero-width: {specific_results['total_zero_width']}")
                        st.write(f"- Tỷ lệ ký tự zero-width: {specific_results['zero_width_ratio']:.2%}")
                    
                    elif steg_method == "Mã Morse Ẩn":
                        st.write(f"- Số từ ngắn (1-3 ký tự): {specific_results['short_words']}")
                        st.write(f"- Số từ dài (4+ ký tự): {specific_results['long_words']}")
                        st.write(f"- Tổng số từ: {specific_results['total_words']}")
                        st.write(f"- Tỷ lệ từ ngắn: {specific_results['short_words_ratio']:.2%}")
                        st.write(f"- Tỷ lệ từ dài: {specific_results['long_words_ratio']:.2%}")
                        st.write(f"- Tỷ lệ từ ngắn/dài: {specific_results['short_long_ratio']:.2f}")
                    
                    elif steg_method == "Unicode Steganography":
                        st.write(f"- Số ký tự Unicode đặc biệt: {specific_results['homoglyph_count']}")
                        st.write(f"- Tỷ lệ ký tự Unicode đặc biệt: {specific_results['homoglyph_ratio']:.2%}")
                
                # Hiển thị biểu đồ phân bố ký tự
                st.subheader("Biểu đồ phân bố ký tự")
                fig = analyzer.plot_char_distribution(original_text, stego_text)
                if fig:
                    st.pyplot(fig)
                else:
                    st.info("Không thể tạo biểu đồ phân bố ký tự")
                
                # Đánh giá bảo mật
                st.subheader("Đánh giá bảo mật")
                
                # Đánh giá khả năng phát hiện
                if steg_method == "Zero-width Characters":
                    detectability = "Thấp (khó phát hiện bằng mắt thường)"
                    robustness = "Trung bình (có thể bị mất khi sao chép qua một số nền tảng)"
                    capacity = "Cao (8 bit cho mỗi ký tự ẩn)"
                elif steg_method == "Mã Morse Ẩn":
                    detectability = "Trung bình (có thể phát hiện nếu phân tích kỹ)"
                    robustness = "Cao (không bị mất khi sao chép)"
                    capacity = "Thấp (khoảng 1-2 bit cho mỗi từ)"
                elif steg_method == "Unicode Steganography":
                    detectability = "Trung bình (có thể phát hiện nếu phân tích kỹ)"
                    robustness = "Cao (không bị mất khi sao chép)"
                    capacity = "Trung bình (1 bit cho mỗi ký tự có thể thay thế)"
                
                security_col1, security_col2 = st.columns(2)
                
                with security_col1:
                    st.write("**Đánh giá phương pháp:**")
                    st.write(f"- Khả năng phát hiện: {detectability}")
                    st.write(f"- Tính bền vững: {robustness}")
                    st.write(f"- Dung lượng ẩn: {capacity}")
                
                with security_col2:
                    st.write("**Khuyến nghị bảo mật:**")
                    if steg_method == "Zero-width Characters":
                        st.write("- Sử dụng mật khẩu để bảo vệ thông điệp")
                        st.write("- Hạn chế độ dài thông điệp để giảm số lượng ký tự zero-width")
                        st.write("- Cẩn thận khi sao chép qua các nền tảng khác nhau")
                    elif steg_method == "Mã Morse Ẩn":
                        st.write("- Sử dụng mật khẩu để bảo vệ thông điệp")
                        st.write("- Cố gắng duy trì tỷ lệ từ ngắn/dài tự nhiên")
                        st.write("- Tránh các thông điệp quá dài do dung lượng ẩn thấp")
                    elif steg_method == "Unicode Steganography":
                        st.write("- Sử dụng mật khẩu để bảo vệ thông điệp")
                        st.write("- Chọn văn bản gốc có nhiều ký tự có thể thay thế")
                        st.write("- Hạn chế độ dài thông điệp để giảm số lượng ký tự thay thế")
    
    else:  # Phát hiện Steganography
        st.subheader("Phát hiện dấu hiệu Steganography trong văn bản")
        
        suspect_text = st.text_area("Nhập văn bản cần kiểm tra:", height=200, key="detect_text")
        
        if st.button("Kiểm tra", key="detect_btn"):
            if not suspect_text:
                st.error("Vui lòng nhập văn bản cần kiểm tra")
            else:
                # Phát hiện dấu hiệu steganography
                detection_results = analyzer.detect_steganography(suspect_text)
                
                # Hiển thị kết quả
                st.subheader("Kết quả kiểm tra")
                
                # Hiển thị kết luận tổng thể
                if detection_results["steganography_detected"]:
                    st.error("⚠️ Phát hiện dấu hiệu của steganography trong văn bản!")
                else:
                    st.success("✅ Không phát hiện dấu hiệu rõ ràng của steganography.")
                
                # Hiển thị chi tiết
                st.write("**Chi tiết kiểm tra:**")
                
                detect_col1, detect_col2 = st.columns(2)
                
                with detect_col1:
                    st.write("**Dấu hiệu Zero-width Characters:**")
                    if detection_results["has_zero_width"]:
                        st.write("❌ Phát hiện ký tự zero-width")
                        st.write(f"- Số lượng: {detection_results['zero_width_count']}")
                    else:
                        st.write("✅ Không phát hiện ký tự zero-width")
                    
                    st.write("**Dấu hiệu Unicode đặc biệt:**")
                    if detection_results["suspicious_homoglyphs"]:
                        st.write("❌ Phát hiện ký tự Unicode đáng ngờ")
                        st.write(f"- Số lượng: {detection_results['homoglyph_count']}")
                    else:
                        st.write("✅ Không phát hiện ký tự Unicode đáng ngờ")
                
                with detect_col2:
                    st.write("**Phân bố từ ngắn/dài:**")
                    if detection_results["unusual_word_distribution"]:
                        st.write("❌ Phân bố từ ngắn/dài bất thường")
                        st.write(f"- Tỷ lệ từ ngắn: {detection_results['short_word_ratio']:.2%}")
                    else:
                        st.write("✅ Phân bố từ ngắn/dài bình thường")
                        st.write(f"- Tỷ lệ từ ngắn: {detection_results['short_word_ratio']:.2%}")
                    
                    st.write("**Entropy:**")
                    if detection_results["unusual_entropy"]:
                        st.write("❌ Entropy bất thường")
                        st.write(f"- Giá trị: {detection_results['entropy']:.4f}")
                    else:
                        st.write("✅ Entropy bình thường")
                        st.write(f"- Giá trị: {detection_results['entropy']:.4f}")
                
                # Thêm khuyến nghị
                st.subheader("Khuyến nghị")
                if detection_results["steganography_detected"]:
                    st.write("""
                    Văn bản có dấu hiệu chứa thông tin ẩn. Bạn có thể thử:
                    - Kiểm tra các ký tự zero-width bằng cách sao chép văn bản vào trình soạn thảo có hỗ trợ hiển thị ký tự đặc biệt
                    - Sử dụng chức năng trích xuất của ứng dụng này để thử các phương pháp khác nhau
                    - Nếu nghi ngờ có mật khẩu bảo vệ, bạn cần biết mật khẩu để trích xuất thông điệp
                    """)
                else:
                    st.write("""
                    Không phát hiện dấu hiệu rõ ràng của steganography trong văn bản. Tuy nhiên, lưu ý rằng:
                    - Một số phương pháp steganography tinh vi có thể không bị phát hiện bởi các kiểm tra cơ bản
                    - Nếu thông điệp được mã hóa bằng mật khẩu, việc phát hiện sẽ khó khăn hơn
                    - Bạn vẫn có thể thử các phương pháp trích xuất khác nhau nếu nghi ngờ
                    """)

# Thêm thông tin về ứng dụng
st.markdown("---")
st.markdown("""
### Giới thiệu về các phương pháp ẩn văn bản

1. **Zero-width Characters**: Sử dụng các ký tự không hiển thị như zero-width space, zero-width joiner để mã hóa thông điệp bí mật.

2. **Mã Morse Ẩn**: Sử dụng từ ngắn để biểu diễn dấu chấm (.) và từ dài để biểu diễn gạch ngang (-) trong mã Morse.

3. **Unicode Steganography**: Sử dụng các ký tự Unicode đặc biệt (homoglyphs) trông giống với ký tự thông thường nhưng có mã Unicode khác nhau.

### Bảo mật thông điệp

Ứng dụng hỗ trợ mã hóa thông điệp bằng mật khẩu trước khi ẩn, giúp tăng cường bảo mật cho thông điệp bí mật. Ngay cả khi thông điệp bị phát hiện, người không có mật khẩu vẫn không thể đọc được nội dung.
""")

# Footer
st.markdown("---")
st.markdown("© 2025 - Ứng dụng Ẩn Văn bản trong Văn bản | Đồ án môn An toàn Bảo mật Thông tin | Nguyễn Hoàng Bảo Lâm | 2111111032")