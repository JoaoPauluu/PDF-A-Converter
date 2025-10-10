import customtkinter as ctk
from tkinterdnd2 import TkinterDnD, DND_ALL

class Tk(ctk.CTk, TkinterDnD.DnDWrapper):
    def __init__(self, fg_color = None, **kwargs):
        super().__init__(fg_color, **kwargs)


class StartPage(Tk):
    def __init__(self, fg_color=None, **kwargs):
        super().__init__(fg_color, **kwargs)

        self.title("Conversor PDF-A/2b")
        self.geometry("300x200")
        self.resizable(False, False)

        label = ctk.CTkLabel(self, text="Conversor PDF-A/2b")
        by = ctk.CTkLabel(self, text="Feito por: João Paulo Gasperi")

        bulk_button = ctk.CTkButton(self, text="Converter em Massa", command=self.open_bulk)
        dnd_button = ctk.CTkButton(self, text="Arrastar e soltar", command=self.open_dnd)

        label.grid(row=0, column=0, pady=10)
        by.grid(row=1, column=0, pady=10)
        bulk_button.grid(row=2, column=0, pady=10)
        dnd_button.grid(row=3, column=0, pady=10)

        self.grid_columnconfigure(0, weight=1)

    def open_bulk(self):
        pass
    def open_dnd(self):
        dnd = DragAndDrop(self)
        pass



class DragAndDrop(ctk.CTkToplevel):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.title = "Arrastar e Soltar"




def main():
    app = StartPage()

    app.mainloop()
    pass



if __name__ == "__main__":
    main()