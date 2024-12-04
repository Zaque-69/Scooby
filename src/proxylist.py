import requests
from bs4 import BeautifulSoup

from helpers import delete_file_data
from messagebox import error_messagebox

def main() : 

    #The proxies are scraped from : 
    try : 
        proxy = requests.get("https://free-proxy-list.net/")
        soup = BeautifulSoup(proxy.content, "html.parser")

        #Deleting the old proxies
        delete_file_data("src/files/newestproxy.txt")

        #Scraping the IPs
        for i in soup.findAll("textarea", attrs = { "class" : "form-control" }) : 
            with open("src/files/newestproxy.txt", "a") as f :
                f.write(str(i))

    except requests.exceptions.RequestException : 
        error_messagebox("Error", "The proxy serverc cannot be scraped!")

if __name__ == "__main__" : 
    main()