import threading
from subprocess import Popen
from sys import platform

import app.buttons.exec.python as python_code
import app.buttons.exec.batch as batch_code


threads = []


def python(message):
    global threads
    
    if "type:uploaded_file" in message:
        message = message.replace("C:\\fakepath\\", "").replace("/exec ", "").replace("type:uploaded_file", "").strip()
        if all(
            substring not in message
            for substring in [
                ":",
                "static/files/uploaded/",
                "static\\files\\uploaded\\",
            ]
        ):
            # if it is stored directly in static/files/uploaded and not in C:\example
            python_file = f"static/files/uploaded/{message}"
            print(message)
            print(python_file)
            
            threads.append(threading.Thread(target=python_code.execute, args=(python_file,), daemon=True))
            threads[-1].start()
            
    elif "type:file_path" in message:
        python_file = message.replace("/exec ", "").replace("type:file_path", "").strip()
        
        threads.append(threading.Thread(target=python_code.execute, args=(python_file,), daemon=True))
        threads[-1].start()
        
    else:
        exec(message.replace("/exec", "").replace("type:single_line", "").strip())


def batch(message):
    if platform != 'win32':
        return
    
    if "type:uploaded_file" in message:
        message = message.replace("C:\\fakepath\\", "").replace("/batch ", "").replace("type:uploaded_file", "").strip()
        if all(
            substring not in message
            for substring in [
                ":",
                "static/files/uploaded/",
                "static\\files\\uploaded\\",
            ]
        ):
            # if it is stored directly in static/files/uploaded and not in C:\example
            batch_file = f"static/files/uploaded/{message}"
            print(message)
            print(batch_file)
            
            threads.append(threading.Thread(target=batch_code.execute, args=(batch_file,), daemon=True))
            threads[-1].start()
            
    elif "type:file_path" in message:
        batch_file = message.replace("/batch ", "").replace("type:file_path", "").strip()
        
        threads.append(threading.Thread(target=batch_code.execute, args=(batch_file,), daemon=True))
        threads[-1].start()
        
    else:
        Popen(message.replace("/batch", "", 1).strip(), shell=True)