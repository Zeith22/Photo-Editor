import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image
from tkinter import ttk
import os
import shutil
import time
import requests

window = tk.Tk()
window.geometry("1280x720")
window.title("Неймовірний фото-редактор")

image_list = []
filtered_image_list = []

image_frame = tk.Frame(window)
image_frame.pack(side="right", fill="both", expand=True)

image_label = tk.Label(image_frame)
image_label.pack(side="top", padx=10, pady=10)

info_frame = tk.Frame(window)
info_frame.pack(side="left", anchor="nw", padx=10, pady=10)

combo_box = ttk.Combobox(window, state="readonly")
combo_box.pack(side="bottom", pady=10)

images_folder = "images"
if not os.path.exists(images_folder):
    os.makedirs(images_folder)
image_files = [os.path.join(images_folder, file) for file in os.listdir(images_folder) if file.endswith((".jpg", ".jpeg", ".png"))]
image_list.extend(image_files)



def show_image(image_path):
    image = Image.open(image_path)
    image = image.resize((800, 600))
    image_tk = ImageTk.PhotoImage(image)
    global image_label
    if 'image_label' in globals():
        image_label.configure(image=image_tk)
        image_label.image = image_tk
    else:
        image_label = tk.Label(window, image=image_tk)
        image_label.image = image_tk
        image_label.pack(side="right")
    update_image_info(image_path)

def update_image_info(image_path):
    for label in info_frame.winfo_children():
        label.destroy()
    file_label = tk.Label(info_frame, text="Світлина: " + os.path.basename(image_path))
    file_label.pack(anchor="w")
    size_bytes = os.path.getsize(image_path)
    size_mb = size_bytes / (1024 * 1024)
    size_label = tk.Label(info_frame, text="Розмір: {:.2f} MB".format(size_mb))
    size_label.pack(anchor="w")
    resolution_label = tk.Label(info_frame, text="Якість: " + str(Image.open(image_path).size))
    resolution_label.pack(anchor="w")

def select_image():
    file_path = filedialog.askopenfilename(title="Оберіть світлину", filetypes=(("Image Files", "*.jpg;*.jpeg;*.png"), ("All Files", "*.*")))
    if file_path:
        image_name = os.path.basename(file_path)
        image_list.append(image_name)
        shutil.copy(file_path, os.path.join('images'))
        combo_box['values'] = tuple(image_list)
        show_image(file_path)

def combo_box_selection(event):
    selected_image_name = combo_box.get()
    selected_image_path = os.path.join("images", selected_image_name)
    show_image(selected_image_path)
combo_box.bind("<<ComboboxSelected>>", combo_box_selection)

def select_image_web():
    url_window = tk.Toplevel(window)
    url_window.geometry("480x144")
    url_window.title("Введіть посилання на світлину")
    
    def download_image():
        url = url_entry.get()
        response = requests.get(url)
        images_folder = "images"
        if not os.path.exists(images_folder):
            os.makedirs(images_folder)
        filename = f"{int(time.time())}.jpg"
        file_path = os.path.join("images", filename)
        with open(file_path, "wb") as file:
            file.write(response.content)
        image_list.append(file_path)
        show_image(file_path)
        url_window.destroy()
        
    url_label = tk.Label(url_window, text="Введіть посилання на світлину: ")
    url_label.pack()
    url_entry = tk.Entry(url_window, width=50)
    url_entry.pack()
    
    download_button = tk.Button(url_window, text="Завантажити", command=download_image)
    download_button.pack()

def update_combo_box():
    combo_box['values'] = [os.path.basename(image_path) for image_path in image_list]
    
menu_bar = tk.Menu(window)
window.config(menu=menu_bar)
file_menu = tk.Menu(menu_bar, tearoff=False)
menu_bar.add_cascade(label="Робота зі світлинами", menu=file_menu)
file_menu.add_command(label="Обрати світлину з комп'ютера", command=select_image)
file_menu.add_command(label="Обрати світлину з інтернету", command=select_image_web)
    
update_combo_box()
window.mainloop()