import hashlib
pw = "qwerty_1"
h = hashlib.sha256(pw.encode()).hexdigest()
print(f"Password: {pw}")
print(f"Hash: {h}")
