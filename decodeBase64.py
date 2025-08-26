import base64

def base64_to_text(b64_string: str) -> str:
    # ถอดรหัส base64 กลับเป็นข้อความปกติ
    decoded_text = base64.b64decode(b64_string).decode("utf-8", errors="ignore")
    return decoded_text

encrypt_text = "EyU2rsrTMSlqOCYtJiY6bCMnMz4vOTAlPC9jKiU4Yy4vIy0raishIC9qNyNqLiYvJS4mbCczYyEvOTAtLS9tbB4iIiIhajojP2o1KTgzYyE/KSttagstKGozJj9maioqajMsOWopIiJqPjE5JjNjKC8pLCgvajckIzlvbDomJi05L2M7OCM3KWozLDk4ajMpJGotLScvYy4/PmM/IiMlOGovIi8iai8pPj4mPmosLD49KzEoaig6bDkjO2I="

# ------------------- ทดลองใช้งาน -------------------
# encoded = base64.b64encode(encrypt_text).decode()
# print("Base64:", encoded)

decoded = base64_to_text(encrypt_text)
print("Decoded:", decoded)
