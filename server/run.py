import threading
import os

def start_thread1():
    os.system("gunicorn server:app")
    

def start_thread2():
    os.system("python discordbot_only.py")
    


if __name__ == '__main__':
    
    thread1 = threading.Thread(target=start_thread1, args=[])
    thread1.start()

    thread2 = threading.Thread(target=start_thread2, args=[])
    thread2.start()