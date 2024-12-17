import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image, ImageTk

# Основной класс приложения
class ImageProcessorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Processing App")
        self.root.geometry("800x600")

        self.image = None
        self.processed_image = None

        # Интерфейс
        self.setup_ui()

    def setup_ui(self):
        # Кнопка загрузки изображения
        self.load_button = tk.Button(self.root, text="Load Image", command=self.load_image)
        self.load_button.pack(pady=10)

        # Канва для отображения изображений
        self.image_canvas = tk.Canvas(self.root, width=500, height=400, bg="gray")
        self.image_canvas.pack(pady=10)

        # Кнопки обработки изображений
        self.filter_button = tk.Button(self.root, text="Apply Low-Pass Filter", command=self.apply_low_pass_filter)
        self.filter_button.pack(pady=5)

        self.histogram_button = tk.Button(self.root, text="Show Histogram", command=self.show_histogram)
        self.histogram_button.pack(pady=5)

        self.equalize_histogram_button = tk.Button(self.root, text="Equalize Histogram", command=self.equalize_histogram)
        self.equalize_histogram_button.pack(pady=5)

        self.contrast_button = tk.Button(self.root, text="Apply Linear Contrast", command=self.apply_linear_contrast)
        self.contrast_button.pack(pady=5)

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.png *.jpeg *.bmp")])
        if file_path:
            self.image = cv2.imread(file_path, cv2.IMREAD_COLOR)
            self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
            self.display_image(self.image)

    def display_image(self, image):
        image = Image.fromarray(image)
        image = image.resize((500, 400), Image.ANTIALIAS)
        image_tk = ImageTk.PhotoImage(image)
        self.image_canvas.image_tk = image_tk
        self.image_canvas.create_image(250, 200, image=image_tk)

    def apply_low_pass_filter(self):
        if self.image is None:
            messagebox.showerror("Error", "No image loaded.")
            return
        kernel = np.ones((5, 5), np.float32) / 25
        self.processed_image = cv2.filter2D(self.image, -1, kernel)
        self.display_image(self.processed_image)

    def show_histogram(self):
        if self.image is None:
            messagebox.showerror("Error", "No image loaded.")
            return

        img_gray = cv2.cvtColor(self.image, cv2.COLOR_RGB2GRAY)
        plt.figure("Histogram")
        plt.hist(img_gray.ravel(), 256, [0, 256])
        plt.title("Histogram")
        plt.xlabel("Pixel Intensity")
        plt.ylabel("Frequency")
        plt.show()

    def equalize_histogram(self):
        if self.image is None:
            messagebox.showerror("Error", "No image loaded.")
            return

        img_gray = cv2.cvtColor(self.image, cv2.COLOR_RGB2GRAY)
        equalized = cv2.equalizeHist(img_gray)
        self.processed_image = cv2.cvtColor(equalized, cv2.COLOR_GRAY2RGB)
        self.display_image(self.processed_image)

    def apply_linear_contrast(self):
        if self.image is None:
            messagebox.showerror("Error", "No image loaded.")
            return

        alpha = 1.5  # коэффициент усиления контраста
        beta = 20    # добавляемая яркость

        self.processed_image = cv2.convertScaleAbs(self.image, alpha=alpha, beta=beta)
        self.display_image(self.processed_image)

# Запуск приложения
if __name__ == "__main__":
    root = tk.Tk()
    app = ImageProcessorApp(root)
    root.mainloop()
