# -*- coding: utf-8 -*-

import subprocess
from othello_py import *
import tkinter
import datetime
from random import randint

offset_y = 10
offset_x = 10
rect_size = 60
circle_offset = 3

ai_exe = subprocess.Popen('./egaroucid.exe'.split(), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)

ai_player = 0
depth = 10
final_depth = 16
record = ''
vals = []


o = None
legal_buttons = []

app = tkinter.Tk()
app.geometry('1000x700')
app.title('Egaroucid4 アプリバージョン')
canvas = tkinter.Canvas(app, width=1000, height = 700)
pixel_virtual = tkinter.PhotoImage(width=1, height=1)

def on_closing():
    global ai_exe
    ai_exe.kill()
    app.destroy()

app.protocol("WM_DELETE_WINDOW", on_closing)

for y in range(hw):
    for x in range(hw):
        canvas.create_rectangle(offset_x + rect_size * x, offset_y + rect_size * y, offset_x + rect_size * (x + 1), offset_y + rect_size * (y + 1), outline='black', width=2, fill='#16a085')

stone_str = tkinter.StringVar()
stone_str.set('*● 2 - 2 ○ ')
stone_label = tkinter.Label(canvas, textvariable=stone_str, font=('', 50))
stone_label.place(x=250, y=600, anchor=tkinter.CENTER)

val_str = tkinter.StringVar()
val_str.set('0')
val_label = tkinter.Label(canvas, textvariable=val_str, font=('', 20))
#val_label.place(x=10, y=650)

def start():
    global o, record, vals, ai_player
    record = ''
    ai_player = randint(0, 1)
    vals = [-1000 for _ in range(60)]
    o = othello()
    o.check_legal()
    show_grid()

start_button = tkinter.Button(canvas, text='対局開始', command=start)
start_button.place(x=600, y=10)

def end_game():
    with open('records.csv', 'a') as f:
        f.write(str(datetime.datetime.now()) + ',' + ('0' if ai_player == 1 else '1') + ',' + str(depth) + ',' + str(final_depth) + ',' + str(o.n_stones[1 - ai_player] - o.n_stones[ai_player]) + ',' + str(o.n_stones[0]) + ',' + str(o.n_stones[1]) + ',' + record)
        for elem in vals:
            f.write(',' + str(elem))
        f.write('\n')

def translate_coord(y, x):
    return chr(ord('a') + x) + str(y + 1)

def ai():
    global clicked, record
    grid_str = str(ai_player) + '\n' + str(depth) + '\n' + str(final_depth) + '\n'
    for i in range(hw):
        for j in range(hw):
            grid_str += '0' if o.grid[i][j] == 0 else '1' if o.grid[i][j] == 1 else '.'
        grid_str += '\n'
    #print(grid_str)
    ai_exe.stdin.write(grid_str.encode('utf-8'))
    ai_exe.stdin.flush()
    y, x, val = [float(elem) for elem in ai_exe.stdout.readline().decode().split()]
    y = int(y)
    x = int(x)
    vals[sum(o.n_stones) - 4] = val
    val_str.set(str(val))
    record += translate_coord(y, x)
    print(y, x)
    clicked = True
    o.move(y, x)
    if not o.check_legal():
        o.player = 1 - o.player
        if not o.check_legal():
            o.print_info()
            o.player = -1
            end_game()
            print('end')
    s = ''
    if o.player == 0:
        s += '*'
    else:
        s += ' '
    s += '● '
    s += str(o.n_stones[0])
    s += ' - '
    s += str(o.n_stones[1])
    s += ' ○'
    if o.player == 1:
        s += '*'
    else:
        s += ' '
    stone_str.set(s)
    #o.print_info()
    show_grid()

def get_coord(event):
    global clicked, record
    y = int(event.widget.cget('text')[0])
    x = int(event.widget.cget('text')[2])
    record += translate_coord(y, x)
    print(y, x)
    clicked = True
    o.move(y, x)
    if not o.check_legal():
        o.player = 1 - o.player
        if not o.check_legal():
            o.print_info()
            o.player = -1
            end_game()
            print('end')
    s = ''
    if o.player == 0:
        s += '*'
    else:
        s += ' '
    s += '● '
    s += str(o.n_stones[0])
    s += ' - '
    s += str(o.n_stones[1])
    s += ' ○'
    if o.player == 1:
        s += '*'
    else:
        s += ' '
    stone_str.set(s)
    #o.print_info()
    show_grid()

def show_grid():
    global clicked, legal_buttons
    for button in legal_buttons:
        button.place_forget()
    legal_buttons = []
    for y in range(hw):
        for x in range(hw):
            try:
                canvas.delete(str(y) + '_' + str(x))
            except:
                pass
            if o.grid[y][x] == vacant:
                continue
            color = ''
            if o.grid[y][x] == black:
                color = 'black'
            elif o.grid[y][x] == white:
                color = 'white'
            elif o.grid[y][x] == legal:
                if o.player != ai_player:
                    color = '#3498db'
                    legal_buttons.append(tkinter.Button(canvas, image=pixel_virtual, width=rect_size - circle_offset * 2, height=rect_size - circle_offset * 2, bg=color, text=str(y) + '_' + str(x)))
                    legal_buttons[-1].bind('<ButtonPress>', get_coord)
                    legal_buttons[-1].place(y=offset_y + rect_size * y, x=offset_x + rect_size * x)
                continue
            canvas.create_oval(offset_x + rect_size * x + circle_offset, offset_y + rect_size * y + circle_offset, offset_x + rect_size * (x + 1) - circle_offset, offset_y + rect_size * (y + 1) - circle_offset, width=0, fill=color, tag=str(y) + '_' + str(x))
    if o.player == ai_player:
        app.after(10, ai)

canvas.place(y=0, x=0)
app.mainloop()
