from threading import Thread
from src.helpers import shell, delete_file_data

def thread1():  
    shell("python src/scraping.py")

def main() :
    delete_file_data("src/files/newestproxy.txt")
    delete_file_data("src/files/validproxy.txt")
    delete_file_data("src/files/hiddenaddress.txt")

    Thread(target = thread1).start()
    shell("python src/proxylist.py")

if __name__ == "__main__" : 
    main()