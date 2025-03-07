import streamlit as st
import pyperclip
from src.zero_width_steg import ZeroWidthSteg
from src.morse_steg import MorseSteg
from src.unicode_steg import UnicodeSteg
from src.encryption import Encryptor

# Khởi tạo các phương pháp steganography và encryptor
zero_width_steg = ZeroWidthSteg()
morse_steg = MorseSteg()
unicode_steg = UnicodeSteg()
encryptor = Encryptor()

# Thiết lập trang
st.set_page_config(
    page_title="Ứng dụng Ẩn Văn bản trong Văn bản",
    page_icon="🔒",
    layout="wide"
)

# Tiêu đề ứng dụng
st.title("Ứng dụng Ẩn Văn bản trong Văn bản")
st.markdown("---")

# Tạo tabs cho các phương pháp khác nhau
tab1, tab2, tab3 = st.tabs(["Zero-width Characters", "Mã Morse Ẩn", "Unicode Steganography"])

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
        
        if st.button("Ẩn thông điệp", key="zw_hide_btn"):
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
                    
                    if st.button("Sao chép kết quả", key="zw_copy_btn"):
                        pyperclip.copy(result)
                        st.success("Đã sao chép vào clipboard!")
                except Exception as e:
                    st.error(f"Đã xảy ra lỗi: {str(e)}")
    
    with col2:
        st.subheader("Trích xuất thông điệp")
        
        stego_text = st.text_area("Văn bản chứa thông điệp ẩn:", height=150, key="zw_stego")
        
        # Thêm tùy chọn mật khẩu cho giải mã
        is_encrypted = st.checkbox("Thông điệp được bảo vệ bằng mật khẩu", key="zw_is_encrypted")
        decrypt_password = ""
        if is_encrypted:
            decrypt_password = st.text_input("Nhập mật khẩu để giải mã:", type="password", key="zw_decrypt_password")
        
        if st.button("Trích xuất thông điệp", key="zw_extract_btn"):
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
                    
                    st.text_area("Thông điệp được trích xuất:", value=extracted_message, height=100, key="zw_extracted")
                    st.success("Đã trích xuất thông điệp thành công!")
                    
                    if st.button("Sao chép kết quả", key="zw_copy_extract_btn"):
                        pyperclip.copy(extracted_message)
                        st.success("Đã sao chép vào clipboard!")
                except Exception as e:
                    st.error(f"Đã xảy ra lỗi: {str(e)}")

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
        
        if st.button("Tạo văn bản ẩn", key="morse_hide_btn"):
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
                    st.text_area("Kết quả (văn bản chứa mã Morse ẩn):", value=result, height=150, key="morse_result")
                    st.success("Đã tạo văn bản ẩn thành công!")
                    
                    if st.button("Sao chép kết quả", key="morse_copy_btn"):
                        pyperclip.copy(result)
                        st.success("Đã sao chép vào clipboard!")
                except Exception as e:
                    st.error(f"Đã xảy ra lỗi: {str(e)}")
    
    with col2:
        st.subheader("Trích xuất thông điệp từ Mã Morse ẩn")
        
        morse_stego = st.text_area("Văn bản chứa mã Morse ẩn:", height=150, key="morse_stego")
        
        # Thêm tùy chọn mật khẩu cho giải mã
        morse_is_encrypted = st.checkbox("Thông điệp được bảo vệ bằng mật khẩu", key="morse_is_encrypted")
        morse_decrypt_password = ""
        if morse_is_encrypted:
            morse_decrypt_password = st.text_input("Nhập mật khẩu để giải mã:", type="password", key="morse_decrypt_password")
        
        if st.button("Trích xuất thông điệp", key="morse_extract_btn"):
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
                    
                    st.text_area("Thông điệp được trích xuất:", value=extracted_message, height=100, key="morse_extracted")
                    st.success("Đã trích xuất thông điệp thành công!")
                    
                    if st.button("Sao chép kết quả", key="morse_copy_extract_btn"):
                        pyperclip.copy(extracted_message)
                        st.success("Đã sao chép vào clipboard!")
                except Exception as e:
                    st.error(f"Đã xảy ra lỗi: {str(e)}")

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
        
        if st.button("Ẩn thông điệp", key="unicode_hide_btn"):
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
                    st.text_area("Kết quả:", value=result, height=150, key="unicode_result")
                    st.success("Đã ẩn thông điệp thành công!")
                    
                    if st.button("Sao chép kết quả", key="unicode_copy_btn"):
                        pyperclip.copy(result)
                        st.success("Đã sao chép vào clipboard!")
                except Exception as e:
                    st.error(f"Đã xảy ra lỗi: {str(e)}")
    
    with col2:
        st.subheader("Trích xuất thông điệp từ Unicode")
        
        unicode_stego = st.text_area("Văn bản chứa thông điệp ẩn:", height=150, key="unicode_stego")
        
        # Thêm tùy chọn mật khẩu cho giải mã
        unicode_is_encrypted = st.checkbox("Thông điệp được bảo vệ bằng mật khẩu", key="unicode_is_encrypted")
        unicode_decrypt_password = ""
        if unicode_is_encrypted:
            unicode_decrypt_password = st.text_input("Nhập mật khẩu để giải mã:", type="password", key="unicode_decrypt_password")
        
        if st.button("Trích xuất thông điệp", key="unicode_extract_btn"):
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
                    
                    st.text_area("Thông điệp được trích xuất:", value=extracted_message, height=100, key="unicode_extracted")
                    st.success("Đã trích xuất thông điệp thành công!")
                    
                    if st.button("Sao chép kết quả", key="unicode_copy_extract_btn"):
                        pyperclip.copy(extracted_message)
                        st.success("Đã sao chép vào clipboard!")
                except Exception as e:
                    st.error(f"Đã xảy ra lỗi: {str(e)}")

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