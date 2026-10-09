# =====================================================================
# TASK 2: RANDOM QUOTE GENERATOR  (beginner-friendly version)
# =====================================================================
# What this app does:
#   - Shows a random quote when the app opens.
#   - The "New Quote" button shows a DIFFERENT quote each time.
#   - Shows the quote text and the author's name.
#   - Bonus: a "Copy" button that copies the quote.
#
# How to run:   python quote_generator.py
# =====================================================================


# ---------------------------------------------------------------------
# 1. IMPORTS
# ---------------------------------------------------------------------
import random                    # gives us tools for random numbers
import tkinter as tk             # tkinter makes windows and buttons


# ---------------------------------------------------------------------
# 2. OUR DATA: a list of quotes
# ---------------------------------------------------------------------
# Each quote is a small list with 2 items:
#   position 0 = the quote text
#   position 1 = the author
# The big list "quotes" holds all of these small lists.

quotes = [
    ["The only way to do great work is to love what you do.", "Steve Jobs"],
    ["It always seems impossible until it's done.", "Nelson Mandela"],
    ["The journey of a thousand miles begins with a single step.", "Lao Tzu"],
    ["Whether you think you can, or you think you can't, you're right.", "Henry Ford"],
    ["Well done is better than well said.", "Benjamin Franklin"],
    ["The best way to predict the future is to invent it.", "Alan Kay"],
    ["Talk is cheap. Show me the code.", "Linus Torvalds"],
    ["Premature optimization is the root of all evil.", "Donald Knuth"],
    ["First, solve the problem. Then, write the code.", "John Johnson"],
    ["Make it work, make it right, make it fast.", "Kent Beck"],
    ["Programs must be written for people to read, and only incidentally for machines to execute.", "Harold Abelson"],
    ["We are what we repeatedly do. Excellence, then, is not an act, but a habit.", "Will Durant"],
    ["Genius is one percent inspiration and ninety-nine percent perspiration.", "Thomas Edison"],
    ["Imagination is more important than knowledge.", "Albert Einstein"],
    ["The unexamined life is not worth living.", "Socrates"],
    ["Fall seven times, stand up eight.", "Japanese Proverb"],
    ["Do or do not. There is no try.", "Yoda"],
]

# We remember the position of the quote on the screen right now.
# -1 means "nothing is shown yet" (positions in a list start at 0, so -1 is never a real quote).
last_index = -1


# ---------------------------------------------------------------------
# 3. FUNCTIONS
# ---------------------------------------------------------------------

def new_quote():
    """Pick a random quote (different from the last one) and show it."""
    global last_index
    # "global" means: change the variable at the top of the file, not a new one inside the function.

    # random.randint(0, 5) gives a random whole number from 0 to 5 (both included).
    # The last position in our list is len(quotes) - 1.
    index = random.randint(0, len(quotes) - 1)

    # If we picked the same quote as last time, keep picking until it is different.
    while index == last_index:
        index = random.randint(0, len(quotes) - 1)

    last_index = index                   # remember this choice for next time

    quote = quotes[index]                # one small list: [text, author]
    text = quote[0]                      # position 0 = text
    author = quote[1]                    # position 1 = author

    quote_label.config(text=text)                  # .config() changes what a label shows
    author_label.config(text="- " + author)        # + joins two pieces of text together


def copy_quote():
    """Copy the quote on the screen to the clipboard (so you can paste it somewhere)."""
    text = quote_label.cget("text")      # .cget() reads a setting from a widget
    author = author_label.cget("text")
    root.clipboard_clear()                           # empty the clipboard
    root.clipboard_append(text + " " + author)       # put our text on the clipboard
    root.update()                                    # make sure it really gets saved


def key_pressed(event):
    """Runs when Enter or Space is pressed. (tkinter always sends an 'event', we ignore it.)"""
    new_quote()


# ---------------------------------------------------------------------
# 4. BUILDING THE WINDOW
# ---------------------------------------------------------------------
root = tk.Tk()                           # create the main window
root.title("Random Quote Generator")
root.geometry("640x420")
root.configure(bg="#0f172a")             # dark blue background

# A Frame is a box that holds other things. This one is the "panel" for the quote.
panel = tk.Frame(root, bg="#1e293b")
panel.pack(padx=30, pady=30, fill="both", expand=True)

# A big decorative quotation mark
tk.Label(panel, text="“", bg="#1e293b", fg="#38bdf8", font=("Georgia", 60, "bold")).pack(anchor="w", padx=20)

# The quote text. wraplength makes long quotes continue on the next line.
quote_label = tk.Label(panel, text="", bg="#1e293b", fg="white",
                       font=("Georgia", 20, "italic"), wraplength=520, justify="left")
quote_label.pack(padx=30, anchor="w")

# The author's name, on the right side
author_label = tk.Label(panel, text="", bg="#1e293b", fg="#94a3b8", font=("Arial", 14))
author_label.pack(padx=30, pady=15, anchor="e")

# A row with two buttons
button_row = tk.Frame(root, bg="#0f172a")
button_row.pack(pady=(0, 25))

tk.Button(button_row, text="New Quote", font=("Arial", 13, "bold"), width=12,
          command=new_quote).pack(side="left", padx=8)
tk.Button(button_row, text="Copy", font=("Arial", 13), width=8,
          command=copy_quote).pack(side="left", padx=8)

# Keyboard shortcuts
root.bind("<Return>", key_pressed)       # Enter key
root.bind("<space>", key_pressed)        # Space bar

# Show the first quote as soon as the app opens
new_quote()


# ---------------------------------------------------------------------
# 5. STARTING THE APP
# ---------------------------------------------------------------------
if __name__ == "__main__":
    root.mainloop()          # keep the window open until the user closes it
