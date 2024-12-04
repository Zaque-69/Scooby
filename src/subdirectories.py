import requests
from messagebox import error_messagebox

# List with the most common subdirectories
def common_subdirectories_list() : 
    list = []
    for i in open("src/files/common.txt"):
        list.append(i.strip())

    return list

# Request the subdirectory
def request_range_of_subdirectories(f, start, end):
    list = common_subdirectories_list()
    for line in list[start:end]:
        try : 
            response = requests.get(f + line.strip())
            if response:
                try:
                    with open("src/files/hiddenaddress.txt", "a") as file:
                        file.write(f + line.strip())
                        file.write("\n")
                except : pass
        except requests.exceptions.RequestException as e : 
            error_messagebox("Error!", e)