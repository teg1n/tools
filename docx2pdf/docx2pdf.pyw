from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
import os
import sys
from docx2pdf import convert

class DummyStream:
    def write(self, x): pass
    def flush(self): pass

sys.stdout = DummyStream()
sys.stderr = DummyStream()

def select_file():
    file_path = filedialog.askopenfilename(
        title="Select a DOCX file",
        filetypes=[("DOCX files", "*.docx"), ("All files", "*.*")]
    )
    if file_path:
        entry.delete(0, END)
        entry.insert(0, file_path)

def convert_to_pdf():
    file_path = entry.get()
    if not file_path:
        messagebox.showerror("Error", "Please select a DOCX file.")
        return

    if not file_path.lower().endswith('.docx'):
        messagebox.showerror("Error", "Selected file must be a DOCX file.")
        return

    try:
        progress_window = Toplevel(root)
        progress_window.title("Converting...")
        progress_window.geometry("300x150")
        progress_window.transient(root) 
        progress_window.grab_set()  

        progress_frame = Frame(progress_window, padx=20, pady=20)
        progress_frame.pack(expand=True)

        Label(progress_frame, text="Converting document...").pack(pady=10)
        progress_bar = ttk.Progressbar(progress_frame, mode="indeterminate")
        progress_bar.pack(pady=10)
        progress_bar.start()

        progress_window.update()

        output_path = file_path.rsplit('.', 1)[0] + '.pdf'
        convert(file_path)


        progress_window.destroy()

        if os.path.exists(output_path):
            messagebox.showinfo("Success", f"PDF saved as:\n{output_path}")
        else:
            raise Exception("PDF file was not created")
    except Exception as e:
        try:
            progress_window.destroy()
        except:
            pass
        if "Word.Application.Quit" not in str(e):
            messagebox.showerror("Error", f"Conversion failed: {str(e)}")

def create_gui():
    global root
    root = Tk()
    root.title("DOCX to PDF Converter")
    root.geometry("400x200")  
    root.resizable(False, False)  

    frame = Frame(root, padx=20, pady=20)
    frame.pack(expand=True)

    global entry
    entry = Entry(frame, width=50)
    entry.pack(pady=10)

    Button(frame, text="Select DOCX File", command=select_file,
           width=20).pack(pady=5)
    Button(frame, text="Convert to PDF", command=convert_to_pdf,
           width=20).pack(pady=5)

    root.mainloop()

create_gui()