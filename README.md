# Ứng dụng Ẩn Văn bản trong Văn bản

Ứng dụng ẩn văn bản trong văn bản (Text-in-Text Steganography) sử dụng các phương pháp khác nhau để ẩn thông điệp bí mật trong văn bản thông thường.

## Tính năng

- **Zero-width Characters**: Sử dụng các ký tự không hiển thị như zero-width space, zero-width joiner để mã hóa thông điệp bí mật.
- **Mã Morse Ẩn**: Sử dụng từ ngắn để biểu diễn dấu chấm (.) và từ dài để biểu diễn gạch ngang (-) trong mã Morse.
- **Unicode Steganography**: Sử dụng các ký tự Unicode đặc biệt (homoglyphs) trông giống với ký tự thông thường nhưng có mã Unicode khác nhau.
- **Bảo vệ bằng mật khẩu**: Mã hóa thông điệp bí mật bằng mật khẩu trước khi ẩn, tăng cường bảo mật.

## Cài đặt

```bash
git clone https://github.com/baolamabcd13/text-steganography.git
cd text-steganography
pip install -r requirements.txt
```

## Chạy ứng dụng

```bash
streamlit run app.py
```

## Tác giả

Nguyễn Hoàng Bảo Lâm | 2111111032
