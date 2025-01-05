import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import Progressbar
from PIL import Image
from tkhtmlview import HTMLLabel
import base64
import tempfile

class ExifCleanerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("EXIF Yok Edici 3000")
        self.root.geometry("400x390")
        self.icon_data = """
Program simgesinin BASE64 verisi
        """
        self.icon_path = self.extract_icon()
        try:
            self.root.iconbitmap(self.icon_path)
        except tk.TclError:
            messagebox.showwarning("Uyarı", "Program simgesi yüklenemedi.")
        self.files = []
        self.output_folder = ""
        self.setup_ui()

    def extract_icon(self):
        try:
            temp_dir = tempfile.gettempdir()
            icon_path = os.path.join(temp_dir, "simge.ico")
            with open(icon_path, "wb") as icon_file:
                icon_file.write(base64.b64decode(self.icon_data))
            return icon_path
        except Exception as e:
            print(f"Program simgesi çıkarılırken hata oluştu: {e}")
            return ""

    def setup_ui(self):
        self.top_frame = tk.Frame(self.root)
        self.top_frame.pack(fill=tk.X, pady=10)
        self.btn_add_files = tk.Button(self.top_frame, text="Görsel Ekle", command=self.add_files)
        self.btn_add_files.pack(side=tk.LEFT, padx=5)
        self.btn_select_output = tk.Button(self.top_frame, text="Çıktı Klasörü Seç", command=self.select_output_folder)
        self.btn_select_output.pack(side=tk.LEFT, padx=5)
        self.output_folder_label = tk.Label(self.top_frame, text="", anchor="w")
        self.output_folder_label.pack(side=tk.LEFT, padx=10)
        self.file_list_frame = tk.Frame(self.root, bg="white", height=200)
        self.file_list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.scrollbar = tk.Scrollbar(self.file_list_frame, orient=tk.VERTICAL)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.file_listbox = tk.Canvas(self.file_list_frame, bg="white", yscrollcommand=self.scrollbar.set, height=200)
        self.file_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.config(command=self.file_listbox.yview)
        self.inner_frame = tk.Frame(self.file_listbox, bg="white")
        self.inner_frame_id = self.file_listbox.create_window((0, 0), window=self.inner_frame, anchor="nw")
        self.inner_frame.bind("<Configure>", self.resize_canvas)
        self.file_listbox.bind("<Configure>", self.resize_inner_frame)
        self.file_listbox.bind_all("<MouseWheel>", self.on_mouse_wheel)
        self.progress_frame = tk.Frame(self.root)
        self.progress_frame.pack(pady=10)
        self.progress_bar = Progressbar(self.progress_frame, orient="horizontal", length=400, mode="determinate")
        self.progress_bar.pack()
        self.progress_label = tk.Label(self.progress_frame, text="")
        self.progress_label.pack()
        self.bottom_frame = tk.Frame(self.root)
        self.bottom_frame.pack(fill=tk.X, pady=10)
        self.btn_clean_exif = tk.Button(self.bottom_frame, text="Arındır", command=self.clean_exif)
        self.btn_clean_exif.pack(side=tk.LEFT, padx=5)
        self.btn_clean_exif.place(relx=0.5, rely=0.5, anchor="center")
        self.info_button = tk.Button(self.bottom_frame, text="h", command=self.show_info)
        self.info_button.pack(side=tk.RIGHT, padx=5)
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def resize_canvas(self, event):
        self.file_listbox.configure(scrollregion=self.file_listbox.bbox("all"))

    def resize_inner_frame(self, event):
        canvas_width = event.width
        self.file_listbox.itemconfig(self.inner_frame_id, width=canvas_width)

    def on_mouse_wheel(self, event):
        self.file_listbox.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def add_files(self):
        file_paths = filedialog.askopenfilenames(
            filetypes=[
                ("Görüntü Dosyaları", "*.jpg;*.jpeg;*.png;*.gif;*.bmp;*.tiff"),
                ("Tüm Dosyalar", "*.*"),
            ]
        )
        for file_path in file_paths:
            if file_path not in self.files:
                self.files.append(file_path)
                self.add_file_row(file_path)

    def add_file_row(self, file_path):
        row_frame = tk.Frame(self.inner_frame, bg="white")
        row_frame.pack(fill=tk.X, pady=2)
        remove_button = tk.Button(row_frame, text="-", command=lambda: self.remove_file(row_frame, file_path))
        remove_button.pack(side=tk.LEFT, padx=5)
        file_label = tk.Label(row_frame, text=file_path, anchor="w", bg="white")
        file_label.pack(side=tk.LEFT, fill=tk.X, expand=True)

    def remove_file(self, row_frame, file_path):
        row_frame.destroy()
        if file_path in self.files:
            self.files.remove(file_path)

    def select_output_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.output_folder = folder_path
            self.output_folder_label.config(text=f"{folder_path}")

    def clean_exif(self):
        if not self.files:
            messagebox.showwarning("Uyarı", "Hedef saptanmadı.")
            return
        self.progress_bar["maximum"] = len(self.files)
        self.progress_bar["value"] = 0
        self.progress_label.config(text="EXIF bilgileri yok ediliyor...")
        success_count = 0
        error_count = 0
        for index, file_path in enumerate(self.files):
            try:
                img = Image.open(file_path)
                if "exif" in img.info:
                    img_without_exif = Image.new(img.mode, img.size)
                    img_without_exif.putdata(list(img.getdata()))
                    output_file_path = os.path.join(self.output_folder, os.path.basename(file_path)) if self.output_folder else file_path
                    img_without_exif.save(output_file_path, "jpeg")
                else:
                    output_file_path = os.path.join(self.output_folder, os.path.basename(file_path)) if self.output_folder else file_path
                    img.save(output_file_path)
                success_count += 1
            except Exception as e:
                error_count += 1
                print(f"Hata: {file_path} -> {e}")
            self.progress_bar["value"] = index + 1
            self.root.update_idletasks()
        if error_count > 0:
            self.progress_label.config(
                text=f"{success_count} görselin EXIF bilgisi yok edildi. {error_count} görsel kaçtı."
            )
        else:
            self.progress_label.config(
                text=f"{success_count} görselin EXIF bilgisi yok edildi."
            )

    def show_info(self):
        about_window = tk.Toplevel(self.root)
        about_window.title("Hakkında")
        about_window.geometry("400x200")
        html_content = """
        <p style="font-family: TkDefaultFont; font-size: 12px; color: #000000; line-height: 1.5;">
            Bu programcık BMP, GIF, JPG, PNG ve TIFF dosyalarını EXIF üstverilerinden arındırır.
        </p>
        <p style="font-family: TkDefaultFont; font-size: 12px; color: #000000; line-height: 1.5;">
            Farklı bir çıktı klasörü seçilmezse üstveriden arındırılan görsel özgün görselin üzerine yazılır.
        </p>
        <p style="font-family: TkDefaultFont; font-size: 12px; color: #000000; line-height: 1.5;">
            Geliştirici: <a href="https://github.com/tyyaman55" style="color: #1a73e8; text-decoration: none; font-weight: bold;">tyyaman</a>
            <span style="font-size: 9px;"> (Cyberdyne Systems noobie researcher)</span>
        </p>
        """
        html_label = HTMLLabel(about_window, html=html_content)
        html_label.pack(padx=10, pady=10, fill="both", expand=True)
        close_button = tk.Button(about_window, text="Kapat", command=about_window.destroy)
        close_button.pack(pady=10)
    
    def on_close(self):
        if self.icon_path and os.path.exists(self.icon_path):
            try:
                os.remove(self.icon_path)
            except Exception as e:
                print(f"Geçici program simgesi silinirken hata oluştu: {e}")
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ExifCleanerApp(root)
    root.mainloop()
