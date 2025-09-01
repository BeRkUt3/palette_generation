import random
import tkinter as tk
from tkinter import ttk
from tkinter import colorchooser
from sys import maxsize
from tkinter.messagebox import showerror, showwarning, showinfo
from functools import cmp_to_key
import time

root = tk.Tk()
root.title('App')

root.geometry('800x700+600+200')
root.resizable(True, True)
root.minsize(200, 200)
root.maxsize(710, 750)


###############################################################
def clear_window():
    for i in range(0, 15):
        for el in root.grid_slaves(row=i):
            el.destroy()


def palette_generation():
    clear_window()
    root.title('Palette generation')
    #################################################################################################################
    import random
    import math

    class HSV:
        def __init__(self, h=0, s=0, v=0):
            self.h = h
            self.s = s
            self.v = v

    class RGB:
        def __init__(self, r=0, g=0, b=0):
            self.r = r
            self.g = g
            self.b = b

    global l, r
    l = -1
    r = -1
    global gamma, akcent
    akcent = RGB()
    gamma = RGB()

    def hsv2rgb(color):
        h = color.h
        s = color.s / 100.0
        v = color.v / 100.0

        c = v * s  # Чистота
        x = c * (1 - abs((h / 60) % 2 - 1))
        m = v - c

        if 0 <= h < 60:
            r, g, b = c, x, 0
        elif 60 <= h < 120:
            r, g, b = x, c, 0
        elif 120 <= h < 180:
            r, g, b = 0, c, x
        elif 180 <= h < 240:
            r, g, b = 0, x, c
        elif 240 <= h < 300:
            r, g, b = x, 0, c
        else:
            r, g, b = c, 0, x

        r = int((r + m) * 255)
        g = int((g + m) * 255)
        b = int((b + m) * 255)

        return RGB(r, g, b)

    def rgb2hex(rgba):
        hh = f"{max(0, min(255, rgba.r)):02X}"
        ee = f"{max(0, min(255, rgba.g)):02X}"
        xx = f"{max(0, min(255, rgba.b)):02X}"
        return hh + ee + xx

    def rgb2hsv(rgba):
        rr = rgba.r / 255.0
        gg = rgba.g / 255.0
        bb = rgba.b / 255.0
        cmax = max(rr, gg, bb)
        cmin = min(rr, gg, bb)
        dlt = cmax - cmin
        ans = HSV()
        ans.v = int(cmax * 100)

        if dlt == 0:
            ans.h = 0
        elif cmax == rr:
            ans.h = int(60 * (((gg - bb) / dlt) % 6.0))
        elif cmax == gg:
            ans.h = int(60 * (((bb - rr) / dlt) + 2.0))
        elif cmax == bb:
            ans.h = int(60 * (((rr - gg) / dlt) + 4.0))

        if cmax == 0:
            ans.s = 0
        else:
            ans.s = int(dlt / cmax * 100)

        return ans

    def hex2rgb(s):
        a = RGB(r=0, g=0, b=0)
        for i in range(1, 7):
            if '0' <= s[i] <= '9':
                b = ord(s[i]) - ord('0')  # '0' - '9'
            elif 'A' <= s[i] <= 'F':
                b = ord(s[i]) - ord('A') + 10  # 'A' - 'F'
            elif 'a' <= s[i] <= 'f':
                b = ord(s[i]) - ord('a') + 10  # 'a' - 'f'

            if i == 1 or i == 2:
                a.r = a.r * 16 + b
            elif i == 3 or i == 4:
                a.g = a.g * 16 + b
            elif i == 5 or i == 6:
                a.b = a.b * 16 + b

        return a

    def akcent_color(a):
        b = HSV(a.h, a.s, a.v)
        b.h = 360 - b.h
        b.s = 100 - b.s
        b.v = 100 - b.v
        b.h = random.randint(max(b.h - 15, 0), min(b.h + 15, 360))
        b.s = random.randint(max(b.s - 10, 0), min(b.s + 10, 100))
        b.v = random.randint(max(b.v - 10, 0), min(b.v + 10, 100))
        return b

    def akcent_color_inrange(a):
        b = HSV(a.h, a.s, a.v)
        b.h = random.randint(max(b.h - 15, 0), min(b.h + 15, 360))
        b.s = random.randint(max(b.s - 10, 0), min(b.h + 10, 100))
        b.v = random.randint(max(b.v - 10, 0), min(b.v + 10, 100))
        return b

    def complement_color_down(a):
        b = HSV(a.h, a.s, a.v)
        b.h = random.randint(b.h, min(b.h + 5, 360))
        b.s = random.randint(b.s, min(b.s + 10, 100))
        b.v = random.randint(max(b.v - 10, 0), b.v)
        return b

    def complement_color_up(a):
        b = HSV(a.h, a.s, a.v)
        b.h = random.randint(max(b.h - 5, 0), b.h)
        b.s = random.randint(max(b.s - 10, 0), b.s)
        b.v = random.randint(b.v, min(b.v + 10, 100))
        return b

    def mymain(n, b, d):
        global gamma, akcent
        random.seed(time.time())
        ans = []
        if b:
            ab = rgb2hsv(gamma)
            m = HSV(h=random.randint(max(ab.h - 5, 0), min(ab.h + 5, 360)),
                    s=random.randint(max(ab.s - 30, 15), min(ab.s + 30, 85)),
                    v=random.randint(15, 85))
        else:
            m = HSV(h=random.randint(0, 360), s=random.randint(15, 85), v=random.randint(15, 85))

        if not b and d:
            u = rgb2hsv(akcent)
            m = HSV(h=random.randint(*sorted([(u.h + 165) % 360, (u.h + 195) % 360])),
                    s=random.randint(15, 85),
                    v=random.randint(15, 85))

        s = m
        ud = random.randint(0, 1)
        sak = []
        for i in range(n):
            if d:
                if i % 4 == 0:
                    f = akcent_color_inrange(rgb2hsv(akcent))
                    t = "#" + rgb2hex(hsv2rgb(f))
                    sak.append(t)
                else:
                    if ud:
                        f = complement_color_up(s)
                    else:
                        f = complement_color_down(s)
                    s = f
                    t = "#" + rgb2hex(hsv2rgb(f))
                    ans.append(t)
            else:
                if ud:
                    f = complement_color_up(s)
                else:
                    f = complement_color_down(s)
                s = f
                t = "#" + rgb2hex(hsv2rgb(f))
                ans.append(t)
        ans = ans + sak
        return ans

    #################################################################################################################
    def print_colors():
        global last_row, isgamma, isakcent
        last_row += 1
        col = 0
        if not color_cnt.get().isdigit():
            showerror(title='Error!', message='The input data is incorrect')
            return 0
        amount_of_colors = int(color_cnt.get())
        if amount_of_colors < 1 or amount_of_colors > 20:
            showerror(title='Error!', message='You have exceeded the available range')
            return 0
        for i in range(last_row - 1, 2, -1):
            for widget in root.grid_slaves(row=i):
                widget.destroy()
        color_list = mymain(amount_of_colors, isgamma.get(), isakcent.get())
        for i in range(amount_of_colors):
            if col > 4:
                last_row += 1
                col = 0
            root.columnconfigure(i, minsize=col_minsize)
            current_color = color_list[i]
            text_color = rgb2hsv(hex2rgb(current_color)).v
            if text_color < 50:
                text_color = 'white'
            else:
                text_color = 'black'
            col_rgb = hex2rgb(current_color)
            can = tk.Canvas(root, bg=current_color, width=col_minsize, height=col_minsize)
            can.grid(row=last_row, column=col, stick='we')
            can.create_text(col_minsize // 2, col_minsize // 2 - 6, text=f'RGB: {col_rgb.r} {col_rgb.g} {col_rgb.b}',
                            fill=text_color)
            can.create_text(col_minsize // 2, col_minsize // 2 + 6, text='hex: ' + current_color, fill=text_color)
            col += 1

    def get_color():
        global osngamma, gamma, isgamma
        isgamma.set(True)
        osngamma = tk.colorchooser.askcolor()
        gamma = RGB(r=osngamma[0][0], g=osngamma[0][1], b=osngamma[0][2])

    def isgamma_false():
        global isgamma
        isgamma.set(False)

    def akc_true():
        global isakcent, akcent
        ak = tk.colorchooser.askcolor()
        akcent = RGB(r=ak[0][0], g=ak[0][1], b=ak[0][2])
        isakcent.set(True)

    def akc_false():
        global isakcent
        isakcent.set(False)

    ################################################################################
    tk.Label(root, text='Number of colors:').grid(row=0, column=0, stick='we')

    color_cnt = tk.Entry(root, width=15)
    color_cnt.grid(row=0, column=1)
    tk.Label(text='from 1 to 20').grid(row=0, column=2)

    col_minsize = 140
    global last_row
    last_row = 3
    global osngamma
    osngamma = (1,)

    tk.Label(root, text='Main color').grid(row=1, column=0)
    global isgamma
    isgamma = tk.BooleanVar()
    isgamma.set(False)
    ttk.Radiobutton(root, text='Yes', variable=isgamma, value=True, command=get_color).grid(row=1, column=1)
    ttk.Radiobutton(root, text='No', variable=isgamma, value=False, command=isgamma_false).grid(row=1, column=2)
    tk.Label(root, text='Accent').grid(row=2, column=0)
    global isakcent
    isakcent = tk.BooleanVar()
    isakcent.set(False)
    ttk.Radiobutton(root, text='Yes', variable=isakcent, value=True, command=akc_true).grid(row=2, column=1)
    ttk.Radiobutton(root, text='No', variable=isakcent, value=False, command=akc_false).grid(row=2, column=2)

    tk.Button(root, text='Generate', command=print_colors).grid(row=1, column=3)



if __name__ == '__main__':
    palette_generation()

    root.mainloop()