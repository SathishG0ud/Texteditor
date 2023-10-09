import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import scrolledtext
from tkinter import font

class TextEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Text Editor")
        self.text_widget = scrolledtext.ScrolledText(root, wrap=tk.WORD)
        self.text_widget.pack(expand=True, fill='both')
        self.create_menu()

    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New", command=self.new_file)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="Save As", command=self.save_file_as)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.exit)

        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Cut", command=self.cut_text)
        edit_menu.add_command(label="Copy", command=self.copy_text)
        edit_menu.add_command(label="Paste", command=self.paste_text)
        edit_menu.add_separator()
        edit_menu.add_command(label="Undo", command=self.undo_text)
        edit_menu.add_command(label="Redo", command=self.redo_text)

        format_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Format", menu=format_menu)
        format_menu.add_command(label="Font", command=self.change_font)

        self.text_widget.config(undo=True)

    def new_file(self):
        self.text_widget.delete(1.0, tk.END)

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            with open(file_path, 'r') as file:
                self.text_widget.delete(1.0, tk.END)
                self.text_widget.insert(tk.END, file.read())

    def save_file(self):
        if self.text_widget.get(1.0, tk.END) == '\n':
            messagebox.showwarning("Warning", "Cannot save an empty file.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            with open(file_path, 'w') as file:
                file.write(self.text_widget.get(1.0, tk.END))

    def save_file_as(self):
        if self.text_widget.get(1.0, tk.END) == '\n':
            messagebox.showwarning("Warning", "Cannot save an empty file.")
            return

        file_path = filedialog.asksaveasfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            with open(file_path, 'w') as file:
                file.write(self.text_widget.get(1.0, tk.END))

    def cut_text(self):
        self.text_widget.event_generate("<<Cut>>")

    def copy_text(self):
        self.text_widget.event_generate("<<Copy>>")

    def paste_text(self):
        self.text_widget.event_generate("<<Paste>>")

    def undo_text(self):
        try:
            self.text_widget.edit_undo()
        except tk.TclError:
            pass

    def redo_text(self):
        try:
            self.text_widget.edit_redo()
        except tk.TclError:
            pass

    def change_font(self):
        selected_font = font.askfont(root=self.root, title="Select Font")
        if selected_font:
            self.text_widget.configure(font=selected_font)

    def exit(self):
        if messagebox.askokcancel("Exit", "Do you want to exit?"):
            self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    editor = TextEditor(root)
    root.mainloop()
