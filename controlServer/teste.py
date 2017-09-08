# from Crypto.Cipher import AES

# obj1 = AES.new('This is a key123', AES.MODE_CBC, 'This is an IV456')
# message = 'The answer is no'
# ciphertext = obj1.encrypt(message)
# print(ciphertext)
# obj2 = AES.new('This is a key123', AES.MODE_CBC, 'This is an IV456')
# print(obj2.decrypt(message))


from cryptography.fernet import Fernet
# Put this somewhere safe!
key = Fernet.generate_key()
print(key)

f = Fernet(key)
token = f.encrypt(b"A really secret message. Not for prying eyes.")
print(token)

print(f.decrypt(token))