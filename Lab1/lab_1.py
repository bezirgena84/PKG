import tkinter as tk
from tkinter import colorchooser, messagebox
import colorsys

# Функции преобразования
def rgb_to_cmyk(r, g, b):
    if (r == 0) and (g == 0) and (b == 0):
        return (0, 0, 0, 1)
    c = 1 - (r / 255)
    m = 1 - (g / 255)
    y = 1 - (b / 255)
    k = min(c, m, y)
    c = (c - k) / (1 - k) if k < 1 else 0
    m = (m - k) / (1 - k) if k < 1 else 0
    y = (y - k) / (1 - k) if k < 1 else 0
    return (c, m, y, k)

def cmyk_to_rgb(c, m, y, k):
    r = 255 * (1 - c) * (1 - k)
    g = 255 * (1 - m) * (1 - k)
    b = 255 * (1 - y) * (1 - k)
    return int(r), int(g), int(b)

def rgb_to_hls(r, g, b):
    r, g, b = r / 255.0, g / 255.0, b / 255.0
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    return h * 360, l * 100, s * 100

def hls_to_rgb(h, l, s):
    h, l, s = h / 360.0, l / 100.0, s / 100.0
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    return int(r * 255), int(g * 255), int(b * 255)

# Обновление цветов
def update_colors(event=None):
    try:
        r = int(entry_r.get())
        g = int(entry_g.get())
        b = int(entry_b.get())

        if any(c < 0 or c > 255 for c in (r, g, b)):
            raise ValueError("RGB values must be between 0 and 255.")

        # Обновление цвета фона
        color_display.config(bg=f'#{r:02x}{g:02x}{b:02x}')

        # Обновление CMYK
        c, m, y, k = rgb_to_cmyk(r, g, b)
        entry_c.delete(0, tk.END)
        entry_c.insert(0, f"{c * 100:.2f}")
        entry_m.delete(0, tk.END)
        entry_m.insert(0, f"{m * 100:.2f}")
        entry_y_cmyk.delete(0, tk.END)
        entry_y_cmyk.insert(0, f"{y * 100:.2f}")
        entry_k.delete(0, tk.END)
        entry_k.insert(0, f"{k * 100:.2f}")

        # Обновление HLS
        h, l, s = rgb_to_hls(r, g, b)
        entry_h.delete(0, tk.END)
        entry_h.insert(0, f"{h:.2f}")
        entry_l.delete(0, tk.END)
        entry_l.insert(0, f"{l:.2f}")
        entry_s.delete(0, tk.END)
        entry_s.insert(0, f"{s:.2f}")

        # Обновление ползунков
        r_scale.set(r)
        g_scale.set(g)
        b_scale.set(b)
        c_scale.set(c * 100)
        m_scale.set(m * 100)
        y_cmyk_scale.set(y * 100)
        k_scale.set(k * 100)
        h_scale.set(h)
        l_scale.set(l)
        s_scale.set(s)

    except ValueError as e:
        messagebox.showerror("Ошибка", str(e))

# Функция для обновления всех значений из ползунков
def scale_update(val):
    try:
        # Получение значений из ползунков
        r = r_scale.get()
        g = g_scale.get()
        b = b_scale.get()

        c = c_scale.get() / 100
        m = m_scale.get() / 100
        y = y_cmyk_scale.get() / 100
        k = k_scale.get() / 100

        h = h_scale.get()
        l = l_scale.get()
        s = s_scale.get()

        # Проверка, откуда идет обновление
        if val in ['r', 'g', 'b']:
            entry_r.delete(0, tk.END)
            entry_r.insert(0, r)
            entry_g.delete(0, tk.END)
            entry_g.insert(0, g)
            entry_b.delete(0, tk.END)
            entry_b.insert(0, b)
            update_colors()
        elif val in ['c', 'm', 'y', 'k']:
            update_rgb_from_cmyk()
        elif val in ['h', 'l', 's']:
            update_rgb_from_hls()
    except ValueError:
        messagebox.showerror("Ошибка", "Некорректное значение.")

# Обновление RGB из CMYK
def update_rgb_from_cmyk(event=None):
    try:
        c = c_scale.get() / 100
        m = m_scale.get() / 100
        y = y_cmyk_scale.get() / 100
        k = k_scale.get() / 100

        r, g, b = cmyk_to_rgb(c, m, y, k)

        entry_r.delete(0, tk.END)
        entry_r.insert(0, r)
        entry_g.delete(0, tk.END)
        entry_g.insert(0, g)
        entry_b.delete(0, tk.END)
        entry_b.insert(0, b)

        update_colors()

    except ValueError as e:
        messagebox.showerror("Ошибка", str(e))

# Обновление RGB из HLS
def update_rgb_from_hls(event=None):
    try:
        h = h_scale.get()
        l = l_scale.get()
        s = s_scale.get()

        r, g, b = hls_to_rgb(h, l, s)

        entry_r.delete(0, tk.END)
        entry_r.insert(0, r)
        entry_g.delete(0, tk.END)
        entry_g.insert(0, g)
        entry_b.delete(0, tk.END)
        entry_b.insert(0, b)

        update_colors()

    except ValueError as e:
        messagebox.showerror("Ошибка", str(e))

# Создание интерфейса
root = tk.Tk()
root.title("Color Converter")
root.geometry("600x800")
root.resizable(False, False)

# Поля для RGB
tk.Label(root, text="R:").grid(row=0, column=0)
entry_r = tk.Entry(root)
entry_r.grid(row=0, column=1)
r_scale = tk.Scale(root, from_=0, to=255, orient=tk.HORIZONTAL, command=lambda _: scale_update('r'))
r_scale.grid(row=0, column=2)

tk.Label(root, text="G:").grid(row=1, column=0)
entry_g = tk.Entry(root)
entry_g.grid(row=1, column=1)
g_scale = tk.Scale(root, from_=0, to=255, orient=tk.HORIZONTAL, command=lambda _: scale_update('g'))
g_scale.grid(row=1, column=2)

tk.Label(root, text="B:").grid(row=2, column=0)
entry_b = tk.Entry(root)
entry_b.grid(row=2, column=1)
b_scale = tk.Scale(root, from_=0, to=255, orient=tk.HORIZONTAL, command=lambda _: scale_update('b'))
b_scale.grid(row=2, column=2)

# Поля для CMYK
tk.Label(root, text="C:").grid(row=3, column=0)
entry_c = tk.Entry(root)
entry_c.grid(row=3, column=1)
c_scale = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, command=lambda _: scale_update('c'))
c_scale.grid(row=3, column=2)

tk.Label(root, text="M:").grid(row=4, column=0)
entry_m = tk.Entry(root)
entry_m.grid(row=4, column=1)
m_scale = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, command=lambda _: scale_update('m'))
m_scale.grid(row=4, column=2)

tk.Label(root, text="Y:").grid(row=5, column=0)
entry_y_cmyk = tk.Entry(root)
entry_y_cmyk.grid(row=5, column=1)
y_cmyk_scale = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, command=lambda _: scale_update('y'))
y_cmyk_scale.grid(row=5, column=2)

tk.Label(root, text="K:").grid(row=6, column=0)
entry_k = tk.Entry(root)
entry_k.grid(row=6, column=1)
k_scale = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, command=lambda _: scale_update('k'))
k_scale.grid(row=6, column=2)

# Поля для HLS
tk.Label(root, text="H:").grid(row=7, column=0)
entry_h = tk.Entry(root)
entry_h.grid(row=7, column=1)
h_scale = tk.Scale(root, from_=0, to=360, orient=tk.HORIZONTAL, command=lambda _: scale_update('h'))
h_scale.grid(row=7, column=2)

tk.Label(root, text="L:").grid(row=8, column=0)
entry_l = tk.Entry(root)
entry_l.grid(row=8, column=1)
l_scale = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, command=lambda _: scale_update('l'))
l_scale.grid(row=8, column=2)

tk.Label(root, text="S:").grid(row=9, column=0)
entry_s = tk.Entry(root)
entry_s.grid(row=9, column=1)
s_scale = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, command=lambda _: scale_update('s'))
s_scale.grid(row=9, column=2)

# Отображение цвета
color_display = tk.Frame(root, width=400, height=100, bg="#ffffff")
color_display.grid(row=10, columnspan=3, pady=10)

# Привязка событий
for entry in [entry_r, entry_g, entry_b]:
    entry.bind("<KeyRelease>", update_colors)

for entry in [entry_c, entry_m, entry_y_cmyk, entry_k]:
    entry.bind("<KeyRelease>", update_rgb_from_cmyk)

for entry in [entry_h, entry_l, entry_s]:
    entry.bind("<KeyRelease>", update_rgb_from_hls)

root.mainloop()
