from app.Interf import run_app
from app.RSA import RSA


def main():
# main.py

    # rsa = RSA(bit=64, c=False, st=False)  # Начните с малого для теста
    # rsa.test_keys()  # Должно вывести "✅ Ключи работают корректно!"

    # message = "Hello"
    # encrypted = rsa.encrypt(message)
    # decrypted = rsa.decrypt(encrypted)
    # print(f"Original: {message}")
    # print(f"Original: {encrypted}")
    # print(f"Decrypted: {decrypted}")

    run_app()

if __name__ == "__main__":
    main()