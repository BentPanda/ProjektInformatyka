import hashlib
import os

def insecure_hash(password):
    hash_object = hashlib.md5()
    hash_object.update(password.encode('utf-8'))
    return hash_object.hexdigest()

def insecure_temp_file():
    temp_path = "/tmp/insecure_temp_file.txt"
    with open(temp_path, 'w') as temp_file:
        temp_file.write("Some sensitive data.")
    return temp_path

def execute_command(command):
    os.system(command)
if __name__ == "__main__":
    user_password = 'jakies_haslo'
    print("Insecure MD5 Hash:", insecure_hash(user_password))

    temp_file_path = insecure_temp_file()
    print("Insecure Temp File Created At:", temp_file_path)

    user_command = 'echo Hello World'
    execute_command(user_command)
