import customtkinter as ctk
from tkinter import filedialog
from PIL import Image
import os

# Set theme and color
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# screen
root = ctk.CTk()
root.title("WebP to JPG Converter")
root.geometry("400x300")
root.resizable(0, 0)

def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("WebP files", "*.webp")])
    if file_path:
        convert_to_jpg(file_path)

def convert_to_jpg(webp_path):
    try:
        image = Image.open(webp_path)
        jpg_path = os.path.splitext(webp_path)[0] + ".jpg"
        image.save(jpg_path, "JPEG")
        status_label.configure(text="Conversion successful!", text_color="green")
    except Exception as e:
        status_label.configure(text="Error during conversion!", text_color="red")

frame = ctk.CTkFrame(root)
frame.pack(pady=20, padx=20, fill="both", expand=True)

select_button = ctk.CTkButton(frame, text="Select WebP File", command=select_file)
select_button.pack(pady=20)

status_label = ctk.CTkLabel(frame, text="")
status_label.pack(pady=10)

root.mainloop()