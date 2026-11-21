import base64

def xor_decrypt(data, key):
    return bytes([b ^ ord(key[i % len(key)]) for i, b in enumerate(data)])

def decode_part(encoded, key):
    decoded_bytes = base64.b64decode(encoded)
    return xor_decrypt(decoded_bytes, key).decode("utf-8", errors="ignore")

# Given values
part1 = base64.b64decode("QlU=").decode()  # "BU"
part2 = decode_part("Snp3PQ==", "kp")
part3 = decode_part("LiQ=", "kp")

final_string = (part1 + part2 + part3).upper()

print(f"💥 Type this to win: {final_string}")
