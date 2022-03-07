import pyperclip as pc
from turtle import width
import pandas as pd
import tkinter as tk
from tkinter import *
from tkinter import messagebox

# setting the screen
root = tk.Tk()
root.title("Phonetic Translator")
root.configure(background='#F4F4F4')
ws = root.winfo_screenwidth() # width of the screen
hs = root.winfo_screenheight() # height of the screen
# calculate x and y coordinates for the Tk root window
w = 790 # width of the screen
h = 400 # height of the screen
x = (ws/2) - (w/2) # position coordinates of the Tk window
y = (hs/2) - (h/2) # position coordinates of the Tk window
root.geometry('%dx%d+%d+%d' % (w, h, x, y))

text_to_be_translated = []
pronunciations_result = []
translated_text_label = tk.StringVar()
translated_text_label.set("")

def update_translated_text():
    global translated_text_label
    translated_text_label.set(result)

data = pd.DataFrame()

def read_data():
    global data
    data = pd.read_excel(r'C:\Users\Fred\Desktop\Frederico\6 python_dev\pronunciation translator\all_words.xlsx')#, encoding='utf-8')
read_data()

# Label requesting the text to translate
label_get_text = Label(root, text="Type to get the pronunciation", font=("Tahoma", 16), background='#F4F4F4',fg='#181818')
label_get_text.grid(row=0, column=0, columnspan=2, padx=10, pady=0)

# Label do not use punctiation marks
label_notice = Label(root, text="Please do not use punctuation marks", font=("Tahoma",11), background='#F4F4F4',fg='#F71B1B')
label_notice.place(x = 5, y = 30, width = 280, height = 40)

# Label for the translated text
label_translated = Label(root, text="Here is the pronunciation", font=("Tahoma", 16), background='#F4F4F4',fg='#004D0F')
label_translated.grid(row=0, column=10, columnspan=2, padx=100, pady=0)

# Setting the entry box for the wanted text
text_to_translate = Text(root, font=("Arial", 14))
text_to_translate.place(x = 10, y = 70, width = 380, height = 280)

# Setting the entry box for the wanted text
text_translated = Label(root, font=("Arial", 12), textvariable = translated_text_label, anchor="nw", borderwidth=2, relief="groove")
text_translated.place(x = 400, y = 70, width = 380, height = 280)

# Button for submit text to translation
btn_submit = Button(root, text="Submit", command=lambda: pronunciation(text_to_translate.get("1.0", "end-1c")), font=("Tahoma", 14), background='#D2D2D2',fg='#181818')
btn_submit.place(x = 10, y = 360, width = 100, height = 30)

# Button for deleting the input text
btn_clear = Button(root, text="Clear", command=lambda: clear_input_text(text_to_translate.get("1.0", "end-1c")), font=("Tahoma", 14), background='#F9E4E4',fg='#400000')
btn_clear.place(x = 290, y = 360, width = 100, height = 30)

# Button for copying translated text to clipboard
btn_copy_translated = Button(root, text="Copy", command=lambda: copy_clipboard(clipboard_text), font=("Tahoma", 14), background='#D2D2D2',fg='#181818')
btn_copy_translated.place(x = 680, y = 360, width = 100, height = 30)

# functions to get the pronunciation of the text
def pronunciation(input):
    global result, clipboard_text
    input = input.upper().split()
    result = []
    punctuation = [",",".",";","/",":","?","!","-","_","(",")","[","]","{","}","'","|","<",">","=","+","*","&","^","%","$","#","@","~","`","1","2","3","4","5","6","7","8","9","0"," "]
    [messagebox.showinfo("Info", "Please don't use any punctuation marks") for i in input if i in punctuation]
    for term in input:
        try:
            pronunciation = data.loc[data['word'] == term, 'Simplified'].values[0]
        except IndexError:
            messagebox.showinfo("Info", f"Sorry, we don't have the pronunciation for {term}. \n Please check the spelling and try again.")
        result.append(pronunciation.upper())
    result = "  ".join(result)
    clipboard_text = result
    if len(result) > 50:
        result = (result[:40]+"\n"+result[40:80]+"\n"+result[80:120]+"\n"+result[120:])
        update_translated_text()
    else:
        update_translated_text()

# function for getting the text from the input text
def get_text():
    return text_to_translate.get("1.0", "end-1c")

# Function for clearing input text - Applies in the btn_clear
def clear_input_text(input_text):
    global text_to_translate, result
    text_to_translate.delete("1.0", END)
    text_translated['Text'] = ""

# Function for copyin the translated text to clipboard - Applies in the btn_copy_translated
def copy_clipboard(output_text):
    pc.copy(output_text)
    messagebox.showinfo("Info", "Your text has been copied to the clipboard")
   
root.mainloop()