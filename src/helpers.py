import subprocess, requests, os

# Abbreviated function
def shell(command) : 
    subprocess.call(command, shell = True)

# Deleting the text from a file
def delete_file_data(filename):
    try : 
        with open(f"{filename}", "a") as f : 
            f.truncate(0)
    except FileNotFoundError : 
        pass

# Counting fies from a directory
def count_files_in_directory(directory):
    count = 0
    try:
        for entry in os.listdir(directory):
            path = os.path.join(directory, entry)
            if os.path.isfile(path):
                count += 1
            elif os.path.isdir(path):
               
                count += count_files_in_directory(path)
    except PermissionError:
        pass
    
    return count

# A list with all the proxy servers scraped
def proxy_server_list() :  
    with open("src/files/newestproxy.txt", "r") as f : 
        lines = [ line.rstrip() for line in f ]

    for i in range(0, 3) : 
        lines.pop(0)
    lines.pop(len(lines) - 1)

    return lines