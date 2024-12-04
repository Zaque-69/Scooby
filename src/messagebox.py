from tkinter import * 
from tkinter import messagebox
import sys

def info_messagebox(title, message) : 
    messagebox.showinfo(title = title , message = message)

def error_messagebox(title, message) : 
    messagebox.showerror(title = title , message = message)
