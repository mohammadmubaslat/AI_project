



from tkinter import *
import numpy as np
import random
import pygame
import sys
import math



my_tk = Tk()
my_tk.title("Connect 4 game")
my_tk.geometry("750x500")

img = PhotoImage(file="game_photo.png")
label = Label(  my_tk,image=img)
label.place(x=0, y=0)


def friend_button_fun():
    newWindow = Toplevel(my_tk)
    newWindow.geometry("750x500")
    Label(newWindow, image=img).pack()





def computer_button_fun():
    newWindow2 = Toplevel(my_tk)
    newWindow2.geometry("750x500")
    Label(newWindow2, image=img).pack()

    easy_button = Button(newWindow2, text='Easy',height=2 , width=20 )
    easy_button.pack()
    easy_button.place(x=290, y=220)

    med_button = Button(newWindow2, text='Medium',height=2 , width=20 )
    med_button.pack()
    med_button.place(x=290, y=290)

    hard_button = Button(newWindow2, text='Hard', height=2, width=20 )
    hard_button.pack()
    hard_button.place(x=290, y=360)


friend_button = Button(my_tk, text='Play with friend',height=2 , width=30, command= friend_button_fun)
friend_button.pack()
friend_button.place(x=290, y=250)


computer_button = Button(my_tk, text='Play with computer',height=2 , width=30, command=computer_button_fun)
computer_button.pack()
computer_button.place(x=290, y=350)




my_tk.mainloop()


