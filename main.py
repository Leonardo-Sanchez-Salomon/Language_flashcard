from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
selected = {}
unknown = {}
# - - - - - PANDAS - - - - - *
try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    data = pandas.read_csv("data/french_words.csv")
    unknown = data.to_dict(orient="records")
else:
    unknown = data.to_dict(orient="records")
print(unknown)


# * - - - - - FUNCTIONS - - - - - *

def learn_random_word():
    global selected, timer
    window.after_cancel(timer)
    selected = random.choice(unknown)
    rand_word_learn = selected["French"]
    canvas.itemconfig(face, image=card_front)
    canvas.itemconfig(title, text="French", fill="black")
    canvas.itemconfig(word, text=rand_word_learn, fill="black")
    timer = window.after(3000, func=known_rand_word)


def known_rand_word():
    rand_word = selected["English"]
    canvas.itemconfig(face, image=card_back)
    canvas.itemconfig(title, text="English", fill="white")
    canvas.itemconfig(word, text=rand_word, fill="white")


def is_known():
    unknown.remove(selected)
    print(len(unknown))
    data = pandas.DataFrame(unknown)
    data.to_csv("data/words_to_learn.csv", index=False)
    learn_random_word()


# * - - - - - WINDOW - - - - - *

window = Tk()
window.title("Flashy the cards")
window.config(bg=BACKGROUND_COLOR, pady=50, padx=50)
timer = window.after(3000, func=known_rand_word)

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)

# * - - - - - IMAGES - - - - - *

card_front = PhotoImage(file="images/card_front.png")
card_back = PhotoImage(file="images/card_back.png")
correct = PhotoImage(file="images/right.png")
incorrect = PhotoImage(file="images/wrong.png")

# * - - - - - BUTTONS - - - - - *

right = Button(image=correct, highlightthickness=0, borderwidth=0, command=is_known)
wrong = Button(image=incorrect, highlightthickness=0, borderwidth=0, command=learn_random_word)

# * - - - - - MAIN - - - - - *

face = canvas.create_image(400, 263, image=card_back)
title = canvas.create_text(400, 150, text="Title", font=("Ariel", 40, "italic"))
word = canvas.create_text(400, 263, text="Word", font=("Ariel", 60, "bold"))
canvas.grid(row=0, column=0, columnspan=2)
right.grid(row=1, column=1)
wrong.grid(row=1, column=0)

learn_random_word()

window.mainloop()
