import customtkinter, json, os, random, re, requests, subprocess, webbrowser

from tkinter import *
from threading import Thread
from bs4 import BeautifulSoup  
from urllib.parse import urljoin

from helpers import shell, count_files_in_directory, proxy_server_list
from messagebox import error_messagebox
from subdirectories import request_range_of_subdirectories

class scooby:
    def __init__(self, master):
        self.master = master
        
        # Labels
        Label(master, bg="#363047", text="Web Scraping", font=(14), fg="white").place(x = 150, y = 30)
        Label(master, text="Please insert your link:", bg="#363047", fg="white").place(x = 50, y = 70)
        Label(master, bg="#363047", text = "").pack()
        Label(master, text="Status Code :", bg="#363047", fg="white").place(x = 665, y = 155)
        Label(master, bg="#363047", text="© 2023 Z4que ALL RIGHTS RESERVED", fg="white").place(x=20, y=390)
        Label(master, bg="#363047", text="URLs Found", fg="white", font=(14)).place(x=500, y = 30)
        Label(master, bg="#363047", text="Hidden Pages", fg="white", font=(14)).place(x=140, y = 230)
        Label(master, bg="#363047", text="Proxy Info", fg="white", font=(14)).place(x=510, y = 230)
        Label(master, bg="#363047", text="E-mails Found", fg="white", font=(14)).place(x=715, y=30)
        Label(master, bg="#363047", text="User Agent", fg="white", font=(14)).place(x=700, y=230)
        Label(master, bg="#363047", text="Servers", fg="white", font=(14)).place(x=950, y=30)

        # Entries 
        self.inputtxt = customtkinter.CTkEntry(master, placeholder_text="https://www.example.com/", width=270, height=25, border_width=2, corner_radius=5, fg_color = "#0E0C12", text_color = "white",border_color="#000")
        self.name = customtkinter.CTkEntry(master, placeholder_text="Name (optional)", width=270, height=25, border_width=2, corner_radius=5, fg_color = "#0E0C12", text_color = "white", border_color="#000")
        self.search = customtkinter.CTkEntry(master, placeholder_text="Search", width=270, height=25, border_width=2, corner_radius=5, fg_color = "#0E0C12", text_color = "white",border_color="#000")
        self.statuscode = customtkinter.CTkEntry(master, placeholder_text="XXX", width=100, height=25, border_width=2, corner_radius=5, fg_color = "#191621", text_color = "#80C148", border_color="#0E0C12")
        self.totalFiles = customtkinter.CTkEntry(master, width=190, height=25, border_width=2, corner_radius=5, fg_color = "#191621", text_color = "#968BC4", border_color="#0E0C12") 

        self.choseYourIp = customtkinter.CTkEntry(master, placeholder_text="0.0.0.0:PORT", width=130, height=25, border_width=2, corner_radius=5, fg_color = "#0E0C12", text_color = "#D69044", border_color="#000")
        self.currentIp = customtkinter.CTkEntry(master, placeholder_text="Your IP", width=190, height=25, border_width=2, corner_radius=5, fg_color = "#191621", text_color = "#D69044", border_color="#0E0C12")
        self.changedIp = customtkinter.CTkEntry(master, placeholder_text="Changed IP", width=190, height=25, border_width=2, corner_radius=5, fg_color = "#191621", text_color = "#D69044", border_color="#0E0C12") 

        self.inputtxt.place(x = 50, y = 100)
        self.name.place(x = 50, y = 140)
        self.search.place(x = 50, y = 180)
        self.statuscode.place(x = 755, y = 155)
        self.totalFiles.place(x = 445, y = 180) 

        self.choseYourIp.place(x = 445, y = 267)
        self.changedIp.place(x = 445, y = 307)
        self.currentIp.place(x = 445, y = 347) 

        # Buttons
        customtkinter.CTkButton(master, width=60, height=60, text="Run", fg_color="#574E73", hover_color="#706494", text_color="black", border_width=1, corner_radius=5, border_color="#4B4363", command = self.main).place(x = 350, y = 100)
        customtkinter.CTkButton(master, width=60, height=40, text="Find", fg_color="#574E73", hover_color="#706494", text_color="black", border_width=1, corner_radius=5, border_color="#4B4363", command = self.thread_request_subdirectories).place(x = 350, y = 270)
        customtkinter.CTkButton(master, width=60, height=40, text="Reload", fg_color="#574E73", hover_color="#706494", text_color="black", border_width=1, corner_radius=5, border_color="#4B4363", command = self.refresh).place(x = 350, y = 330)
        customtkinter.CTkButton(master, width=60, height=30, text="Search", fg_color="#574E73", hover_color="#706494", text_color="black", border_width=1, corner_radius=5, border_color="#4B4363", command = self.search_on_web).place(x = 350, y = 177.5)
        customtkinter.CTkButton(master, width=30, height=30, text="Servers", fg_color="#574E73", hover_color="#706494", text_color="black", border_width=1, corner_radius=5, border_color="#4B4363", command = self.insert_proxy_servers).place(x = 585, y = 263.5)

        # Text areas
        self.output = customtkinter.CTkTextbox(master , width=270, height=100, border_width=2, corner_radius=5, fg_color = "#191621", text_color = "#8D8B93", border_color="#0E0C12")
        self.domains = customtkinter.CTkTextbox(master, width=190, height=80, border_width=2, corner_radius=5, fg_color = "#191621", text_color = "#E7CF50", border_color="#0E0C12")
        self.afis = customtkinter.CTkTextbox(master , width=190, height=100, border_width=2, corner_radius=5, fg_color = "#191621", text_color = "#D0669F", border_color="#0E0C12")
        self.EntryUserAgent = customtkinter.CTkEntry(master, placeholder_text="Your User Agent (optional)", width=190, height=25, border_width=2, corner_radius=5, fg_color = "#191621", text_color = "#D0669F", border_color="#0E0C12")
        self.userAgent = customtkinter.CTkTextbox(master, width=190, height=70, border_width=2, corner_radius=5, fg_color = "#191621", text_color = "#74CFC1", border_color="#0E0C12")
        self.payload = customtkinter.CTkTextbox(master, width=190, height = 300, border_width=2, corner_radius=5, fg_color = "#191621", text_color = "#74CFC1", border_color="#0E0C12")

        self.output.place(x = 50, y = 270)
        self.afis.place(x = 445, y = 70)
        self.domains.place(x = 665, y = 70)
        self.EntryUserAgent.place(x = 665, y = 265)
        self.userAgent.place(x = 665, y = 300)
        self.payload.place(x = 890, y = 70)

    # Function to clear the Textboxes
    def clear_text_boxes(self) : 
        self.currentIp.delete(0, 'end')
        self.changedIp.delete(0, 'end')
        self.statuscode.delete(0, 'end')
        self.totalFiles.delete(0, 'end')

        self.userAgent.delete('1.0', END)
        self.domains.delete('1.0', END)
        self.output.delete('1.0', END)
        self.afis.delete("1.0", END)

    # Function to validate URL
    def search_on_web(self):
        return webbrowser.open_new(str(self.search.get()))

    # Function to re-write the output
    def refresh(self):
        self.output.delete("1.0", END)
        for j in open("src/files/hiddenaddress.txt", "r"): 
            self.output.insert(END, j)

    # Obtaining a the name to the folder where we will move the files
    def folder_name(self) : 
        address = ""
        domain = ""
        INPUT = self.inputtxt.get()
        NAME = self.name.get()

        # Getting the domain name
        if len(NAME) == 0:
            if "https://www." in INPUT : domain = INPUT.replace(INPUT[:12], "")
            if "http://www." in INPUT: domain = INPUT.replace(INPUT[:8], "")
            for char in domain :
                if char == "." : 
                    break
                address += char
        else: 
            # If the field for "NAME is completed", we get that name
            address = NAME
            return address + "_folder"

    # Creating the folder to move the files
    def create_scraped_files_folder(self) : 
        PATH = self.folder_name()
        try : 
            if os.path.exists(PATH) : 
                if os.path.isdir(PATH): 
                    shell(f"rm -rf {PATH}")
                else : 
                    shell(f"rm {PATH}")

        except TypeError as e : 
            error_messagebox("Error!", e)

        os.mkdir(PATH)

    # Moving the files in your created folder
    def move_files_to_your_folder(self) : 
        elementsToMove = [
            "hypertext_files", 
            "script_files", 
            "media_files",
            "html.html"
            ]

        for path in os.listdir() : 
            for e in elementsToMove : 
                if path == e : 
                    shell(f"mv {path} {self.folder_name()}")

    # Chosing between 2 IPs to scrap the files
    def get_valid_ip_to_scrap(self) : 
        if (self.choseYourIp.get()) : 
            return self.choseYourIp.get()
        else :  
            return ""

    def ip_data(proxy_server) : 
        try : 
            public_ip = requests.get("https://ipinfo.io/json")
            self.currentIp.insert(END, str(public_ip.json()["ip"]))

        except requests.exceptions.RequestException as e : 
            error_messagebox("Error", e)

        try : 
            changed_ip = requests.get("https://ipinfo.io/json", 
            proxies = {
                "http" : proxy_server, 
                "https" : proxy_server
                }
            )
            self.currentIp.insert(END, str(changed_ip.json()["ip"]))

        except requests.exceptions.RequestException as e : 
            error_messagebox("Error", e)

    def get_valid_user_agent_to_scrap(self) : 
        INPUT = self.inputtxt.get()
        user_agent = ""

        if (self.EntryUserAgent.get()) : 
            user_agent = self.EntryUserAgent.get()
        else :  
            user_agent = random.choice(
                open('src/files/useragent.txt').readlines()
                ).split('\n')[0]

        return user_agent

    # Function to scarp the elements from the page, like scripts, images, etc.
    def request(self, var, source, elements, user_agent, proxy_server): 
        INPUT = str(self.inputtxt.get())
        try : 
            request = requests.get(INPUT, 
                headers = {
                    "User-Agent" : user_agent 
                }, 
                proxies = {
                    "http" : f"{proxy_server}", 
                    "https" : f"{proxy_server}"
                }
            )
            self.statuscode.insert(END, str(request.status_code) + ' ')
            soup = BeautifulSoup( request.content, "html.parser" )
            if not os.path.exists(elements): 
                os.mkdir(elements)

            for i in soup.find_all(var):
                try : 
                    name = os.path.basename(i[source])           
                    url = urljoin(INPUT, i.get(source))
                    path = os.path.join(elements, name)
                    self.afis.insert(END, "URL FOUNFD : " + str(url) + "\n" + "\n", )
                
                    if not os.path.isfile(path):
                        with open(path, 'wb') as file:
                            filebin = requests.Session().get(url)
                            file.write(filebin.content)
                except : 
                    pass

        except requests.exceptions.RequestException as e : 
            return error_messagebox("Error!", e)
            
    # Function to scrap the HTML code
    def request_html(self, user_agent, proxy_server) :
        INPUT = self.inputtxt.get() 
        try : 
            request = requests.get(INPUT, 
                    headers = {
                        "User-Agent" : user_agent 
                    }, 
                    proxies = {
                        "http" : f"{proxy_server}", 
                        "https" : f"{proxy_server}"
                    }
                )
            soup = BeautifulSoup(request.content, "html.parser")

            with open("html.html", "a", encoding = 'utf-8') as f: 
                f.write(str(request.text))

        except requests.exceptions.RequestException as e: 
            return error_messagebox("Error!", e)

    # REGEX to fint the emails in the page
    def request_find_emails(self, user_agent, proxy_server ):        
        INPUT = self.inputtxt.get()
        try : 
            request = requests.get(INPUT, 
                headers = {
                        "User-Agent" : user_agent 
                    }, 
                    proxies = {
                        "http" : f"{proxy_server}", 
                        "https" : f"{proxy_server}"
                    }
                )
            soup = BeautifulSoup(request.content, "html.parser")

            with open("html.html", "a", encoding = 'utf-8') as f: 
                f.write(str(request.text))

            email_regex = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}')
            emails = email_regex.findall(soup.prettify())
            emails += email_regex.findall(soup.text)

            for j in set(emails)  : 
                self.domains.insert(END, str(j) + "\n")

        except requests.exceptions.RequestException as e: 
            return error_messagebox("Error!", e)

    # Function to get a list with some subdirectories of the main URL
    def request_subdirectories(self):
        INPUT = str(self.inputtxt.get())
        self.output.delete("1.0", END)
        number = 0 
        
        for i in range(4):
            # Making 4 threads to find faster the subdirectories, especially when you use a proxy server
            Thread(target = request_range_of_subdirectories(INPUT, number,  number + 10)).start()
            number += 10
   
   # Making a thread so you don't have to wait for all the requests ( GUI is freezed )
    def thread_request_subdirectories(self): 
        Thread(target = self.request_subdirectories).start()

    # Here are all the "requests" functions from behind
    def requests_start(self) : 
        INPUT = str(self.inputtxt.get())
        user_agent = self.get_valid_user_agent_to_scrap()
        proxy_server = self.get_valid_ip_to_scrap()

        self.userAgent.insert(END, user_agent)

        scraping_config = [
                {"var": tag, "source": "src", "elements": "media_files"}
                for tag in ["img", "video", "iframe", "source", "audio"]
            ] + [
                {"var": tag, "source": "href", "elements": "hypertext_files"}
                for tag in ["a", "link", "area", "base"]
            ] + [
                {"var": "script", "source": "src", "elements": "script_files"},
                {"var": "img", "source": "data-src", "elements": "media_files"}
            ]

        for config in scraping_config:
            self.request(
                var = config["var"],
                source = config["source"],
                elements = config["elements"],
                user_agent = user_agent,
                proxy_server = proxy_server,
            )

        # Call to scrap the HTML
        self.request_html(
            user_agent = user_agent, 
            proxy_server = proxy_server
            )
       
        # Call to scrap the e-mails
        self.request_find_emails(
            user_agent = user_agent, 
            proxy_server = proxy_server
            )

        # Call to insert the IPs
        self.ip_data(
            proxy_server = proxy_server
        )

    # Function to insert the proxy servers scraped
    def insert_proxy_servers(self) : 
        list = proxy_server_list()
        for server in list : 
            self.payload.insert(END, str(server) + '\n')

    # Inserting some text in text boxes
    def insert_text(self) : 
        self.totalFiles.insert(END, f"Total files downloaded : {count_files_in_directory(self.folder_name())}")

    # The main function
    def main(self):
        self.clear_text_boxes()
        self.create_scraped_files_folder()
        self.refresh()
        self.requests_start()
        self.refresh()
        self.move_files_to_your_folder()
        self.insert_text()

if __name__ == "__main__": 
    root = Tk()
    root.geometry("1110x420")
    root.configure(bg="#363047")
    root.config(cursor = "top_left_arrow")
    root.resizable(False, False)
    root.title("Web Scraping")
    scooby(root)
    root.mainloop()
