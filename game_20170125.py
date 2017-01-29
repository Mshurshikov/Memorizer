# PATH
#blablabla
# Комментарий
# SublimeREPL

from tkinter import *
from random import randint, shuffle
import os

SIDE = 6
QSIDE = SIDE ** 2 // 2      # сколько чисел нужно сделать?

print('Memorizer')

# PEP-8 - рекомендации по оформлению кода




prev = None

def hide_both(btns, prev, i, j):
    # btns[i][j].configure(text=' x ') 
    # btns[prev[0]][prev[1]].configure(text=' x ') 
    btns[i][j].configure(image=faq) 
    btns[prev[0]][prev[1]].configure(image=faq) 
       

def change(btns, nums, i, j):
    global prev
    # btns[i][j].configure(text='{:>3}'.format(str(nums[SIDE * i + j])))
    btns[i][j].configure(image=images[SIDE * i + j])

    if prev:
        if nums[SIDE * i + j] != nums[SIDE * prev[0] + prev[1]]:
            pass  # хочется спрятатьff обе кнопки через таймаут
            main_window.after(1000, hide_both, btns, prev, i, j)

        prev = None    
    else:
        prev = (i, j)    


def hide_all(btns):
    for i in range(SIDE):
        for j in range(SIDE):
            # btns[i][j].configure(text=' x ')
            btns[i][j].configure(image=faq)


def show_all(btns, nums):
    for i in range(SIDE):
        for j in range(SIDE):
            # btns[i][j].configure('{:>3}'.format(str(nums[SIDE * i + j])))
            btns[i][j].configure('{:>3}'.format(str(nums[SIDE * i + j])))


# def <lambda> (args):
#     return expression

# lambda args: expression


main_window = Tk()
main_window.title('Запоминалка')
faq = PhotoImage(file='FAQ.gif')

# numbers = []
# for i in range(1, 100):
#     numbers.append(i)

files = os.listdir('gif')
shuffle(files)
files = files[0:QSIDE] * 2
shuffle(files)  

images = [PhotoImage(file=os.path.join('gif', img)) for img in files]

numbers = [x for x in range(1, 100)]
shuffle(numbers)

numbers = numbers[0:QSIDE] * 2
shuffle(numbers)  
print(numbers)

buttons = []

for i in range(SIDE):       # while
    buttons.append([])
    for j in range(SIDE):
        b = Button(main_window, 
                # text='{:>3}'.format(str(numbers[SIDE * i + j])),
                image=images[SIDE * i + j],
                font=('Courier New', 12, 'normal'),
                relief=FLAT, 
                command=lambda ii=i, jj=j: change(buttons, files, ii, jj))

        buttons[i].append(b)
        b.grid(row=i, column=j)


main_window.after(2000, hide_all, buttons)
main_window.mainloop()

# ДЗ
# Сделать Label-счетчик открыто:осталось
# Сделать игру по таймеру
# Отладить баги