import bcrypt

# pwd = 'rodrigo'.encode('utf-8')
# hash =bcrypt.hashpw(pwd, bcrypt.gensalt(10))
# print(hash)

res = bcrypt.checkpw(b'liy', b'$2b$10$r/.uXxAqIPhZabqOU0AQAudvUwxgKXJHcWsKDTH1bwxyVuLw64NFG')

print(res)