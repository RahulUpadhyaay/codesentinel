from app.core.security import hash_password, verify_password, create_access_token, decode_access_token

# 1. Test Password Hashing
raw_pass = "MySecretPassword123"
hashed = hash_password(raw_pass)

print("🔑 Raw Password:", raw_pass)
print("🔒 Hashed Password:", hashed)
print("✅ Password Matches?", verify_password(raw_pass, hashed))
print("❌ Wrong Password Matches?", verify_password("WrongPass", hashed))

print("\n-----------------------------------\n")

# 2. Test JWT Token Generation
token_payload = {"sub": "user_id_101", "email": "rahul@codesentinel.ai"}
token = create_access_token(data=token_payload)

print("🎟️ Generated JWT Token:\n", token)

# 3. Test JWT Decoding
decoded_data = decode_access_token(token)
print("\n🔓 Decoded Token Payload:\n", decoded_data)