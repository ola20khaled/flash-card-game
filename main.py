from tkinter import *
import pandas as pd
import random

BACKGROUND_COLOR = "#B1DDC6"
to_learn = {}
current_card = {}

#Start with the german words then make another file for the words to be learned
try:
    data = pd.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pd.read_csv('data/german_words.csv')
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient='records')


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)  #so after 3 seconds it doesn't flip automatically
    current_card = random.choice(to_learn)
    front_card_canvas.itemconfig(card_title, text="German", fill="Black")
    front_card_canvas.itemconfig(card_word, text=current_card['German'], fill="Black")  #we change the canvas
    front_card_canvas.itemconfig(front_card_image, image=front_image)
    flip_timer = window.after(3000, func=back_card)  #set new timer


#Flip the card
def back_card():
    front_card_canvas.itemconfig(front_card_image, image=back_image)
    front_card_canvas.itemconfig(card_word, text=current_card["English"], fill="White")
    front_card_canvas.itemconfig(card_title, text="English", fill="White")


#When pressing right
def is_known():
    to_learn.remove(current_card)
    data = pd.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv", index=False)
    next_card()


#UI SETUP
window = Tk()
window.title("Flash Card")
window.config(bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=back_card)

front_card_canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
front_image = PhotoImage(file="images/card_front.png")
front_card_image = front_card_canvas.create_image(400, 263, image=front_image)
card_title = front_card_canvas.create_text(400, 150, text="German", font=("Arial", 40, "italic"))
card_word = front_card_canvas.create_text(400, 263, text="Wort", font=("Arial", 60, "bold"))
front_card_canvas.grid(row=0, column=0, columnspan=2, padx=50, pady=50)

back_image = PhotoImage(file="images/card_back.png")


right_image = PhotoImage(file='images/right.png')
right_button = Button(image=right_image, highlightthickness=0, command=is_known)
right_button.grid(row=1, column=1)

wrong_image = PhotoImage(file='images/wrong.png')
wrong_button = Button(image=wrong_image, highlightthickness=0, command=next_card)
wrong_button.grid(row=1, column=0)

next_card()

window.mainloop()