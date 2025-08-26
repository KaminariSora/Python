import base64

def text_to_ascii_base64_reverse(text: str) -> str:
    # 1) แปลงเป็น ASCII codes
    ascii_codes = [ord(c) for c in text]
    
    # 2) รวมเป็น string ตัวเลข
    ascii_str = " ".join(str(code) for code in ascii_codes)
    
    # 3) Encode Base64
    ascii_base64 = base64.b64encode(ascii_str.encode()).decode()
    
    # 4) Reverse ตัวอักษร Base64
    reversed_b64 = ascii_base64[::-1]
    
    return reversed_b64


def reverse_base64_to_text(reversed_b64: str) -> str:
    # 1) Reverse กลับมาก่อน
    normal_b64 = reversed_b64[::-1]
    
    # 2) Decode Base64 → ASCII string
    decoded_ascii_str = base64.b64decode(normal_b64).decode()
    
    # 3) ASCII string → Text
    decoded_text = "".join(chr(int(n)) for n in decoded_ascii_str.split())
    
    return decoded_text


# ------------------- ทดลองใช้งาน -------------------
original = "You're probably not the person I've heard right?"

encoded = text_to_ascii_base64_reverse(original)
print("Encoded (Reversed Base64):", encoded)

decoded = reverse_base64_to_text(encoded)
print("Decoded Text:", decoded)
