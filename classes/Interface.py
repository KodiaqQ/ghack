from tkinter import *
from tkinter.filedialog import askopenfilename


class Interface:
    def __init__(self):
        self.root = Tk()
        self.filepath = ''

    def load_file(self, text):
        self.filepath = askopenfilename(initialdir="/", title=text,
                                        filetypes=(("Excel File", "*.xls"), ("All Files", "*.*")))
        return self.filepath
