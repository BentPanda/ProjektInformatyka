import os
import subprocess

def example_assert():
    assert False, "This is an assert statement."

def example_eval():
    eval("os.system('ls')")

def example_subprocess():
    subprocess.Popen('ls -la', shell=True)

def example_tempfile():
    import tempfile
    f = tempfile.NamedTemporaryFile(delete=False)
    f.write(b'Temporary file content.')
    f.close()

def example_pickle():
    import pickle
    data = {'key': 'value'}
    with open('data.pickle', 'wb') as f:
        pickle.dump(data, f)

def example_requests():
    import requests
    requests.get('https://example.com', verify=False)

def example_hashlib():
    import hashlib
    password = 'password123'
    hashlib.md5(password.encode('utf-8')).hexdigest()
