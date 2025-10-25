import os
from PIL import Image
import customtkinter as ctk
from tkinter import filedialog, messagebox

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class ImageSplitterApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Image Splitter - Full Spread to Halves")
        self.geometry("600x350")
        self.resizable(False, False)

        # Variables
        self.input_folder = ctk.StringVar()
        self.output_folder = ctk.StringVar()

        # UI
        self.create_widgets()

    def create_widgets(self):
        ctk.CTkLabel(self, text="📁 Select Input Folder (Full Spread Images)", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(20, 5))
        input_frame = ctk.CTkFrame(self)
        input_frame.pack(padx=20, pady=5, fill="x")
        ctk.CTkEntry(input_frame, textvariable=self.input_folder, width=400).pack(side="left", padx=5, pady=10)
        ctk.CTkButton(input_frame, text="Browse", width=80, command=self.select_input_folder).pack(side="right", padx=5)

        ctk.CTkLabel(self, text="📂 Select Output Folder", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(15, 5))
        output_frame = ctk.CTkFrame(self)
        output_frame.pack(padx=20, pady=5, fill="x")
        ctk.CTkEntry(output_frame, textvariable=self.output_folder, width=400).pack(side="left", padx=5, pady=10)
        ctk.CTkButton(output_frame, text="Browse", width=80, command=self.select_output_folder).pack(side="right", padx=5)

        ctk.CTkButton(self, text="Split Images", width=200, height=40, command=self.split_images).pack(pady=30)
        self.progress_label = ctk.CTkLabel(self, text="")
        self.progress_label.pack(pady=5)

    def select_input_folder(self):
        folder = filedialog.askdirectory(title="Select Input Folder")
        if folder:
            self.input_folder.set(folder)

    def select_output_folder(self):
        folder = filedialog.askdirectory(title="Select Output Folder")
        if folder:
            self.output_folder.set(folder)

    def split_images(self):
        in_folder = self.input_folder.get().strip()
        out_folder = self.output_folder.get().strip()

        if not in_folder or not os.path.isdir(in_folder):
            messagebox.showerror("Error", "Please select a valid input folder.")
            return
        if not out_folder or not os.path.isdir(out_folder):
            messagebox.showerror("Error", "Please select a valid output folder.")
            return

        images = [f for f in os.listdir(in_folder) if f.lower().endswith((".jpg", ".jpeg", ".png", ".bmp", ".tiff"))]
        if not images:
            messagebox.showinfo("No Images", "No image files found in the input folder.")
            return

        self.progress_label.configure(text="Processing images...")
        self.update()

        count = 0
        for img_name in images:
            try:
                img_path = os.path.join(in_folder, img_name)
                img = Image.open(img_path)
                w, h = img.size

                mid = w // 2
                left_half = img.crop((0, 0, mid, h))
                right_half = img.crop((mid, 0, w, h))

                base, ext = os.path.splitext(img_name)
                left_half.save(os.path.join(out_folder, f"{base}_left{ext}"), quality=100)
                right_half.save(os.path.join(out_folder, f"{base}_right{ext}"), quality=100)
                count += 1

            except Exception as e:
                print(f"❌ Error processing {img_name}: {e}")

        self.progress_label.configure(text=f"✅ Done! {count} images processed.")
        messagebox.showinfo("Completed", f"{count} images successfully split.")

if __name__ == "__main__":
    app = ImageSplitterApp()
    app.mainloop()
