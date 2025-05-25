from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image
import img2pdf
import os

#screen
root = Tk()
root.title("Png/Pdf Dönüştrücü")
root.geometry("400x300")
root.resizable(0, 0)

def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("png files", "*.png")])
    if file_path:
        convert_to_pdf(file_path)

def convert_to_pdf(webp_path):
    try:
        image = Image.open(webp_path)
        if image.mode == 'RGBA':
            image = image.convert('RGB')
        temp_path = os.path.splitext(webp_path)[0] + "_temp.jpg"
        image.save(temp_path, "JPEG")
        pdf_path = os.path.splitext(webp_path)[0] + ".pdf"
        with open(pdf_path, "wb") as f:
            f.write(img2pdf.convert(temp_path))
        os.remove(temp_path)
        messagebox.showinfo("Başarılı", "Dönüştürme başarılı!")
    except Exception as e:
        messagebox.showerror("Hata", f"Dönüştürme sırasında hata oluştu: {str(e)}")
        print(f"Hata detayı: {str(e)}")

frame = Frame(root)
frame.pack(pady=20, padx=20, fill="both", expand=True)

select_button = Button(frame, text="Png Dosyasını Seçin", command=select_file)
select_button.pack(pady=20)

bildirim= Label(frame, text="Dönüştürülen dosya aynı klasöre kaydedilir .", wraplength=300,fg="#666666").pack(pady=10)

status_label = Label(frame, text="")
status_label.pack(pady=10)

root.mainloop()