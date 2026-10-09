# =====================================================================
# TASK 1: FLASHCARD QUIZ APP  (beginner-friendly version)
# =====================================================================
# What this app does:
#   - Shows a question. Click "Show Answer" to see the answer.
#   - "Next" and "Previous" buttons move between cards.
#   - You can Add, Edit and Delete flashcards.
#   - Cards are saved in a file so they are still there next time.
#
# How to run:   python flashcard_app.py
# (Run it from inside this folder so the save file is created here.)
#
# HOW THIS FILE IS ORGANISED (read it from top to bottom):
#   1. Imports
#   2. Variables the app remembers
#   3. Functions (saving, loading, showing cards, buttons)
#   4. Building the window
#   5. Starting the app
# =====================================================================


# ---------------------------------------------------------------------
# 1. IMPORTS
# ---------------------------------------------------------------------
# An "import" lets us use code that someone else already wrote.

import json                              # lets us save a list into a text file and read it back
import tkinter as tk                     # tkinter makes windows and buttons. "as tk" = short nickname
from tkinter import messagebox           # small pop-up boxes (like "Are you sure?")
from tkinter import simpledialog         # small pop-up box where the user types something


# ---------------------------------------------------------------------
# 2. VARIABLES THE APP REMEMBERS
# ---------------------------------------------------------------------

FILE_NAME = "flashcards.json"    # the file where cards are saved

cards = []                       # a LIST that will hold all our cards
                                 # each card is a DICTIONARY like {"question": "...", "answer": "..."}

card_index = 0                   # which card we are looking at (0 = the first card)
answer_showing = False           # False = we see the question, True = we see the answer


# ---------------------------------------------------------------------
# 3. FUNCTIONS
# ---------------------------------------------------------------------
# A function is a named block of code. We write it once and can run it
# many times by using its name.

def make_starter_cards():
    """Gives us a few example cards the very first time."""
    starter = []
    starter.append({"question": "What keyword makes a function in Python?", "answer": "def"})
    starter.append({"question": "Is a tuple changeable (mutable)?", "answer": "No, a tuple is immutable"})
    starter.append({"question": "What does len([1, 2, 3]) give?", "answer": "3"})
    starter.append({"question": "Which symbol starts a comment?", "answer": "#"})
    return starter                       # "return" sends the result back to whoever called the function


def load_cards():
    """Read the cards from the file. If there is no file yet, use the starter cards."""
    global cards
    # "global" tells Python: I want to CHANGE the variable "cards" that lives at the top of the file.
    # (If we skip this line, Python would create a new, separate variable inside the function.)

    try:
        file = open(FILE_NAME, "r", encoding="utf-8")    # open the file for reading ("r")
        cards = json.load(file)                          # turn the text in the file into a Python list
        file.close()                                     # always close a file when you are done
    except (FileNotFoundError, json.JSONDecodeError):
        # "try / except" = try this code, and if an error happens, do the except part instead.
        # FileNotFoundError = the file does not exist yet.
        # JSONDecodeError  = the file exists but its content is broken.
        cards = make_starter_cards()


def save_cards():
    """Write the cards into the file so they are not lost."""
    file = open(FILE_NAME, "w", encoding="utf-8")        # "w" = write (replaces the old content)
    json.dump(cards, file, indent=2)                     # turn the list into text and write it
    file.close()


def show_card():
    """Update what the window displays. We call this after EVERY change."""

    # Case 1: there are no cards at all
    if len(cards) == 0:                                  # len() = how many items are in the list
        counter_label.config(text="No cards")            # .config() changes a widget's settings
        side_label.config(text="EMPTY DECK")
        text_label.config(text="Click Add to create your first flashcard.")
        show_button.config(text="Show Answer")
        return                                           # stop the function here

    # Case 2: there is at least one card
    card = cards[card_index]                             # get the current card (a dictionary)

    # We add 1 because humans count from 1, but Python counts from 0.
    # str() turns a number into text so we can join it with other text using +
    counter_label.config(text="Card " + str(card_index + 1) + " of " + str(len(cards)))

    if answer_showing == True:
        side_label.config(text="ANSWER", fg="green")
        text_label.config(text=card["answer"])           # card["answer"] reads the "answer" from the dictionary
        show_button.config(text="Hide Answer")
    else:
        side_label.config(text="QUESTION", fg="blue")
        text_label.config(text=card["question"])
        show_button.config(text="Show Answer")


def toggle_answer():
    """Called when the user clicks 'Show Answer' / 'Hide Answer'."""
    global answer_showing
    if len(cards) == 0:
        return
    if answer_showing == True:
        answer_showing = False
    else:
        answer_showing = True
    show_card()


def next_card():
    """Go to the next card. After the last card, go back to the first."""
    global card_index, answer_showing
    if len(cards) == 0:
        return
    card_index = card_index + 1              # move forward by one
    if card_index >= len(cards):             # did we go past the last card?
        card_index = 0                       # then start again from the first
    answer_showing = False                   # always show the question side first
    show_card()


def previous_card():
    """Go to the previous card. Before the first card, go to the last."""
    global card_index, answer_showing
    if len(cards) == 0:
        return
    card_index = card_index - 1              # move back by one
    if card_index < 0:                       # did we go before the first card?
        card_index = len(cards) - 1          # then jump to the last card
    answer_showing = False
    show_card()


def add_card():
    """Ask the user for a question and an answer, then add a new card."""
    global card_index, answer_showing

    # askstring shows a small box. It gives back the typed text, or None if the user pressed Cancel.
    question = simpledialog.askstring("Add Flashcard", "Type the QUESTION:", parent=root)
    if question is None:                     # user pressed Cancel
        return
    question = question.strip()              # .strip() removes extra spaces at the start and end
    if question == "":                       # user typed nothing
        return

    answer = simpledialog.askstring("Add Flashcard", "Type the ANSWER:", parent=root)
    if answer is None:
        return
    answer = answer.strip()
    if answer == "":
        return

    new_card = {"question": question, "answer": answer}   # make a new dictionary
    cards.append(new_card)                                # .append() adds it to the END of the list
    card_index = len(cards) - 1                           # jump to the new card (the last one)
    answer_showing = False
    save_cards()
    show_card()


def edit_card():
    """Change the question and answer of the card we are looking at."""
    global answer_showing
    if len(cards) == 0:
        return

    card = cards[card_index]
    # initialvalue puts the old text in the box so the user can change it
    question = simpledialog.askstring("Edit Flashcard", "Change the QUESTION:",
                                      initialvalue=card["question"], parent=root)
    if question is None:
        return
    question = question.strip()
    if question == "":
        return

    answer = simpledialog.askstring("Edit Flashcard", "Change the ANSWER:",
                                    initialvalue=card["answer"], parent=root)
    if answer is None:
        return
    answer = answer.strip()
    if answer == "":
        return

    card["question"] = question               # replace the old text with the new text
    card["answer"] = answer
    answer_showing = False
    save_cards()
    show_card()


def delete_card():
    """Delete the card we are looking at (after asking 'are you sure?')."""
    global card_index, answer_showing
    if len(cards) == 0:
        return

    sure = messagebox.askyesno("Delete", "Delete this flashcard?", parent=root)   # True if user clicks Yes
    if sure == False:
        return

    cards.pop(card_index)                     # .pop(position) removes the item at that position

    # After deleting, our position might be past the end of the list. Fix it:
    if card_index >= len(cards):
        card_index = len(cards) - 1
    if card_index < 0:                        # happens when the list becomes empty
        card_index = 0

    answer_showing = False
    save_cards()
    show_card()


# Keyboard shortcuts need a function that accepts one input called "event".
# (tkinter sends it automatically, we just don't use it.)
def key_next(event):
    next_card()

def key_previous(event):
    previous_card()

def key_flip(event):
    toggle_answer()


# ---------------------------------------------------------------------
# 4. BUILDING THE WINDOW
# ---------------------------------------------------------------------
# Everything below runs once, from top to bottom, when the program starts.

root = tk.Tk()                               # create the main window
root.title("Flashcard Quiz App")             # text at the top of the window
root.geometry("600x460")                     # width x height in pixels
root.configure(bg="#f4f6f8")                 # background colour

# A Label is a piece of text. .pack() puts it in the window.
counter_label = tk.Label(root, text="", bg="#f4f6f8", font=("Arial", 11, "bold"))
counter_label.pack(pady=10)                  # pady = empty space above and below

# A Frame is a box. We use it as the "card".
card_frame = tk.Frame(root, bg="white", highlightthickness=2, highlightbackground="#cccccc")
card_frame.pack(padx=30, pady=5, fill="both", expand=True)   # fill + expand = use all the free space

side_label = tk.Label(card_frame, text="QUESTION", bg="white", fg="blue", font=("Arial", 11, "bold"))
side_label.pack(pady=10)

# wraplength = when the text is longer than 480 pixels, continue on the next line
text_label = tk.Label(card_frame, text="", bg="white", font=("Arial", 18), wraplength=480)
text_label.pack(expand=True)

# A Button runs a function when clicked. command=toggle_answer (no brackets!)
show_button = tk.Button(root, text="Show Answer", font=("Arial", 12, "bold"), command=toggle_answer)
show_button.pack(pady=8)

# A second frame to put two buttons side by side
nav_frame = tk.Frame(root, bg="#f4f6f8")
nav_frame.pack()
tk.Button(nav_frame, text="< Previous", width=12, command=previous_card).pack(side="left", padx=5)
tk.Button(nav_frame, text="Next >", width=12, command=next_card).pack(side="left", padx=5)

# A third frame for Add / Edit / Delete
manage_frame = tk.Frame(root, bg="#f4f6f8")
manage_frame.pack(pady=10)
tk.Button(manage_frame, text="Add", width=10, command=add_card).pack(side="left", padx=5)
tk.Button(manage_frame, text="Edit", width=10, command=edit_card).pack(side="left", padx=5)
tk.Button(manage_frame, text="Delete", width=10, command=delete_card).pack(side="left", padx=5)

# Keyboard shortcuts: arrow keys and the space bar
root.bind("<Right>", key_next)
root.bind("<Left>", key_previous)
root.bind("<space>", key_flip)

# Load the saved cards and show the first one
load_cards()
show_card()


# ---------------------------------------------------------------------
# 5. STARTING THE APP
# ---------------------------------------------------------------------
# This "if" is true only when you run THIS file directly.
if __name__ == "__main__":
    root.mainloop()      # keeps the window open and waits for clicks until you close it
