# =====================================================================
# TASK 4: LANGUAGE LEARNING APP  (beginner-friendly version)
# =====================================================================
# What this app does:
#   - Choose a language (Spanish, French, German) and a category
#     (Daily Lesson, Vocabulary, Phrases, Grammar).
#   - LEARN tab: flashcards with the translation and how to pronounce it.
#   - QUIZ tab: a multiple-choice quiz (10 questions).
#   - PROGRESS tab: your past quiz scores, saved in a text file.
#
# How to run:   python language_app.py
# (Run it from inside this folder so the save file is created here.)
# =====================================================================


# ---------------------------------------------------------------------
# 1. IMPORTS
# ---------------------------------------------------------------------
import os                                # to check if a file exists
import random                            # shuffling and random choices
import tkinter as tk                     # windows and buttons
from tkinter import ttk                  # tabs, drop-down lists, progress bar
from datetime import date                # today's date


# ---------------------------------------------------------------------
# 2. THE LESSON DATA
# ---------------------------------------------------------------------
# Layout:  LESSONS[language][category]  gives a list of cards.
# Each card is a tuple (a list that cannot change) with 3 items:
#     position 0 = English word
#     position 1 = translation
#     position 2 = pronunciation (CAPITAL letters = the stressed part)
#
# Example: LESSONS["Spanish"]["Vocabulary"][0]  is  ("Hello", "Hola", "OH-lah")
#
LESSONS = {
    "Spanish": {
        "Vocabulary": [
            ("Hello", "Hola", "OH-lah"),
            ("Thank you", "Gracias", "GRAH-see-ahs"),
            ("Water", "Agua", "AH-gwah"),
            ("Food", "Comida", "koh-MEE-dah"),
            ("House", "Casa", "KAH-sah"),
            ("Friend", "Amigo", "ah-MEE-goh"),
            ("Book", "Libro", "LEE-broh"),
            ("Cat", "Gato", "GAH-toh"),
            ("Please", "Por favor", "por fah-VOR"),
            ("Goodbye", "Adiós", "ah-dee-OHS"),
        ],
        "Phrases": [
            ("How are you?", "¿Cómo estás?", "KOH-moh ehs-TAHS"),
            ("My name is...", "Me llamo...", "meh YAH-moh"),
            ("I don't understand", "No entiendo", "noh ehn-tee-EHN-doh"),
            ("Where is the bathroom?", "¿Dónde está el baño?", "DOHN-deh ehs-TAH el BAH-nyoh"),
            ("How much does it cost?", "¿Cuánto cuesta?", "KWAHN-toh KWEHS-tah"),
            ("I would like water", "Quiero agua", "kee-EH-roh AH-gwah"),
            ("Good morning", "Buenos días", "BWEH-nohs DEE-ahs"),
            ("Nice to meet you", "Mucho gusto", "MOO-choh GOOS-toh"),
        ],
        "Grammar": [
            ("I am", "Yo soy", "yoh soy"),
            ("You are (informal)", "Tú eres", "too EH-rehs"),
            ("He / She is", "Él / Ella es", "el / EH-yah ehs"),
            ("We are", "Nosotros somos", "noh-SOH-trohs SOH-mohs"),
            ("I have", "Yo tengo", "yoh TEHN-goh"),
            ("I want", "Yo quiero", "yoh kee-EH-roh"),
            ("I eat", "Yo como", "yoh KOH-moh"),
            ("The (masculine)", "El", "el"),
            ("The (feminine)", "La", "lah"),
        ],
    },
    "French": {
        "Vocabulary": [
            ("Hello", "Bonjour", "bohn-ZHOOR"),
            ("Thank you", "Merci", "mehr-SEE"),
            ("Water", "Eau", "oh"),
            ("Food", "Nourriture", "noo-ree-TUUR"),
            ("House", "Maison", "meh-ZOHN"),
            ("Friend", "Ami", "ah-MEE"),
            ("Book", "Livre", "LEE-vruh"),
            ("Cat", "Chat", "shah"),
            ("Please", "S'il vous plaît", "seel voo PLEH"),
            ("Goodbye", "Au revoir", "oh ruh-VWAHR"),
        ],
        "Phrases": [
            ("How are you?", "Comment allez-vous ?", "koh-mohn tah-lay VOO"),
            ("My name is...", "Je m'appelle...", "zhuh mah-PEL"),
            ("I don't understand", "Je ne comprends pas", "zhuh nuh kohm-PRAHN pah"),
            ("Where is the bathroom?", "Où sont les toilettes ?", "oo sohn lay twah-LET"),
            ("How much is it?", "Combien ça coûte ?", "kohm-BYAN sah KOOT"),
            ("I would like water", "Je voudrais de l'eau", "zhuh voo-DREH duh LOH"),
            ("Good evening", "Bonsoir", "bohn-SWAHR"),
            ("Nice to meet you", "Enchanté", "ahn-shahn-TAY"),
        ],
        "Grammar": [
            ("I am", "Je suis", "zhuh SWEE"),
            ("You are", "Tu es", "too EH"),
            ("He is", "Il est", "eel EH"),
            ("We are", "Nous sommes", "noo SOHM"),
            ("I have", "J'ai", "zhay"),
            ("I want", "Je veux", "zhuh VUH"),
            ("I eat", "Je mange", "zhuh MAHNZH"),
            ("The (masculine)", "Le", "luh"),
            ("The (feminine)", "La", "lah"),
        ],
    },
    "German": {
        "Vocabulary": [
            ("Hello", "Hallo", "HAH-loh"),
            ("Thank you", "Danke", "DAHN-kuh"),
            ("Water", "Wasser", "VAH-ser"),
            ("Food", "Essen", "ESS-en"),
            ("House", "Haus", "hows"),
            ("Friend", "Freund", "froynd"),
            ("Book", "Buch", "bookh"),
            ("Cat", "Katze", "KAHT-seh"),
            ("Please", "Bitte", "BIT-teh"),
            ("Goodbye", "Auf Wiedersehen", "owf VEE-der-zay-en"),
        ],
        "Phrases": [
            ("How are you?", "Wie geht's?", "vee GAYTS"),
            ("My name is...", "Ich heiße...", "ikh HY-seh"),
            ("I don't understand", "Ich verstehe nicht", "ikh fer-SHTAY-eh nikht"),
            ("Where is the bathroom?", "Wo ist die Toilette?", "voh ist dee toy-LET-teh"),
            ("How much does it cost?", "Was kostet das?", "vahs KOS-tet dahs"),
            ("I would like water", "Ich möchte Wasser", "ikh MERKH-teh VAH-ser"),
            ("Good morning", "Guten Morgen", "GOO-ten MOR-gen"),
            ("Nice to meet you", "Freut mich", "froyt mikh"),
        ],
        "Grammar": [
            ("I am", "Ich bin", "ikh bin"),
            ("You are", "Du bist", "doo bist"),
            ("He is", "Er ist", "air ist"),
            ("We are", "Wir sind", "veer zint"),
            ("I have", "Ich habe", "ikh HAH-beh"),
            ("I want", "Ich will", "ikh vil"),
            ("I eat", "Ich esse", "ikh ESS-eh"),
            ("The (masculine)", "Der", "dair"),
            ("The (feminine)", "Die", "dee"),
        ],
    },
}


# ---------------------------------------------------------------------
# 3. SETTINGS AND VARIABLES THE APP REMEMBERS
# ---------------------------------------------------------------------
DAILY_LESSON = "Daily Lesson (5 items)"      # the name of the special daily category
PROGRESS_FILE = "progress.txt"               # quiz scores are saved in this text file
BUTTON_GREY = "#d9d9d9"

# --- Learn tab ---
learn_cards = []                 # the cards being studied right now
learn_index = 0                  # which card we are looking at
translation_showing = False      # False = hidden, True = shown

# --- Quiz tab ---
quiz_questions = []              # the list of quiz questions
quiz_index = 0                   # which question we are on
quiz_score = 0                   # how many answers are correct so far
question_answered = False        # has the user answered the current question?


# ---------------------------------------------------------------------
# 4. FUNCTIONS THAT WORK WITH THE DATA (no windows here)
# ---------------------------------------------------------------------

def get_all_items(language):
    """Return ALL cards of a language (Vocabulary + Phrases + Grammar together)."""
    items = []
    categories = LESSONS[language]                   # a dictionary: {"Vocabulary": [...], "Phrases": [...], ...}
    for category_name in categories:                 # looping over a dictionary gives its keys
        for card in categories[category_name]:
            items.append(card)
    return items


def get_cards(language, category):
    """Return the cards for the chosen language and category."""
    if category == DAILY_LESSON:
        items = get_all_items(language)
        # random.seed() with today's date makes the "random" shuffle come out the SAME
        # all day, so the daily lesson stays the same until tomorrow.
        random.seed(date.today().isoformat() + language)
        random.shuffle(items)                        # mix the list
        random.seed()                                # go back to truly random for everything else
        return items[0:5]                            # items[0:5] = the first 5 items

    items = []
    for card in LESSONS[language][category]:         # make a copy of the list
        items.append(card)
    return items


def make_quiz(language, category):
    """Build a list of quiz questions. Each question is a dictionary with:
       "prompt"  - the English word to translate
       "answer"  - the correct translation
       "options" - 4 choices (1 correct + 3 wrong), shuffled"""
    items = get_cards(language, category)
    random.shuffle(items)                            # random question order

    number_of_questions = len(items)
    if number_of_questions > 10:
        number_of_questions = 10                     # maximum 10 questions

    # Collect every translation in this language. We use them as WRONG answers.
    all_translations = []
    for card in get_all_items(language):
        all_translations.append(card[1])

    questions = []
    for i in range(number_of_questions):
        card = items[i]
        correct = card[1]

        options = [correct]                          # start with the right answer
        while len(options) < 4:                      # add wrong answers until we have 4 options
            wrong = random.choice(all_translations)
            if wrong not in options:                 # "not in" avoids duplicates
                options.append(wrong)
        random.shuffle(options)                      # so the right answer is not always first

        question = {"prompt": card[0], "answer": correct, "options": options}
        questions.append(question)

    return questions


def save_result(language, category, score, total):
    """Add one line to the progress file. We use the | symbol to separate the pieces."""
    file = open(PROGRESS_FILE, "a", encoding="utf-8")        # "a" = append (add to the end)
    line = date.today().isoformat() + "|" + language + "|" + category + "|" + str(score) + "|" + str(total)
    file.write(line + "\n")                                  # \n = start a new line
    file.close()


def load_results():
    """Read all saved results. Returns a list of lists, newest first."""
    results = []
    if os.path.exists(PROGRESS_FILE) == False:               # no file yet = no results
        return results

    file = open(PROGRESS_FILE, "r", encoding="utf-8")
    lines = file.readlines()                                 # a list with one item per line
    file.close()

    for line in lines:
        line = line.strip()                                  # remove the new-line at the end
        if line != "":
            pieces = line.split("|")                         # "a|b|c" becomes ["a", "b", "c"]
            results.append(pieces)

    results.reverse()                                        # newest first
    return results


# ---------------------------------------------------------------------
# 5. FUNCTIONS FOR THE LEARN TAB
# ---------------------------------------------------------------------

def show_learn_card():
    """Show the current flashcard."""
    card = learn_cards[learn_index]
    english = card[0]
    translation = card[1]
    pronunciation = card[2]

    learn_counter.config(text=category_box.get() + "  -  Card " + str(learn_index + 1) +
                              " of " + str(len(learn_cards)))
    english_label.config(text=english)

    if translation_showing == True:
        translation_label.config(text=translation)
        pron_label.config(text="Say it: " + pronunciation)
        reveal_button.config(text="Hide Translation")
    else:
        translation_label.config(text="?")
        pron_label.config(text="")
        reveal_button.config(text="Show Translation")


def toggle_translation():
    global translation_showing
    if translation_showing == True:
        translation_showing = False
    else:
        translation_showing = True
    show_learn_card()


def next_learn_card():
    global learn_index, translation_showing
    learn_index = learn_index + 1
    if learn_index >= len(learn_cards):
        learn_index = 0                      # after the last card, go to the first
    translation_showing = False
    show_learn_card()


def previous_learn_card():
    global learn_index, translation_showing
    learn_index = learn_index - 1
    if learn_index < 0:
        learn_index = len(learn_cards) - 1   # before the first card, go to the last
    translation_showing = False
    show_learn_card()


# ---------------------------------------------------------------------
# 6. FUNCTIONS FOR THE QUIZ TAB
# ---------------------------------------------------------------------

def reset_quiz():
    """Put the quiz tab back to its 'ready to start' state."""
    global quiz_questions, quiz_index, quiz_score, question_answered
    quiz_questions = []
    quiz_index = 0
    quiz_score = 0
    question_answered = False

    quiz_status.config(text=language_box.get() + "  -  " + category_box.get())
    quiz_question_label.config(text="Ready to test yourself?")
    feedback_label.config(text="")
    for button in option_buttons:                            # a loop over the 4 answer buttons
        button.config(text="", state="disabled", bg=BUTTON_GREY)
    quiz_main_button.config(text="Start Quiz", state="normal")


def show_question():
    """Show the current question and its 4 options."""
    global question_answered
    question_answered = False
    question = quiz_questions[quiz_index]

    quiz_status.config(text="Question " + str(quiz_index + 1) + " of " + str(len(quiz_questions)) +
                            "     Score: " + str(quiz_score))
    quiz_question_label.config(text="How do you say:  " + question["prompt"] + " ?")
    feedback_label.config(text="")

    for i in range(4):                                       # i = 0, 1, 2, 3
        option_buttons[i].config(text=question["options"][i], state="normal", bg=BUTTON_GREY)

    quiz_main_button.config(state="disabled")                # the user must answer first


def check_answer(number):
    """Runs when an answer button is clicked. 'number' is the button (0, 1, 2 or 3)."""
    global quiz_score, question_answered
    if question_answered == True:                            # ignore a second click
        return
    question_answered = True

    question = quiz_questions[quiz_index]
    chosen = question["options"][number]                     # the text of the clicked button

    if chosen == question["answer"]:
        quiz_score = quiz_score + 1
        feedback_label.config(text="Correct!", fg="green")
    else:
        feedback_label.config(text="Not quite. The answer is: " + question["answer"], fg="red")

    # Colour the buttons: green = right answer, red = the wrong one the user clicked
    for i in range(4):
        option_text = question["options"][i]
        if option_text == question["answer"]:
            option_buttons[i].config(bg="#86efac")
        elif option_text == chosen:
            option_buttons[i].config(bg="#fca5a5")
        option_buttons[i].config(state="disabled")

    # The big button now lets us continue
    if quiz_index == len(quiz_questions) - 1:
        quiz_main_button.config(text="Finish", state="normal")
    else:
        quiz_main_button.config(text="Next Question", state="normal")


# One tiny function per answer button. Each one calls check_answer with its own number.
def click_option_0():
    check_answer(0)

def click_option_1():
    check_answer(1)

def click_option_2():
    check_answer(2)

def click_option_3():
    check_answer(3)


def quiz_main_click():
    """The big button: starts the quiz, or moves to the next question, or finishes."""
    global quiz_questions, quiz_index, quiz_score

    if len(quiz_questions) == 0:                             # no quiz running -> start one
        quiz_questions = make_quiz(language_box.get(), category_box.get())
        quiz_index = 0
        quiz_score = 0
        show_question()
    elif question_answered == True:                          # the question was answered -> go on
        quiz_index = quiz_index + 1
        if quiz_index >= len(quiz_questions):
            finish_quiz()
        else:
            show_question()


def finish_quiz():
    """Show the final score and save it."""
    global quiz_questions
    total = len(quiz_questions)
    save_result(language_box.get(), category_box.get(), quiz_score, total)

    percent = quiz_score / total * 100
    if percent >= 80:
        message = "Excellent!"
    elif percent >= 50:
        message = "Good effort!"
    else:
        message = "Keep practising!"

    quiz_status.config(text="Quiz complete")
    quiz_question_label.config(text="You scored " + str(quiz_score) + " / " + str(total) +
                                    "  (" + str(int(percent)) + "%)")
    feedback_label.config(text=message, fg="#d97706")
    for button in option_buttons:
        button.config(text="", state="disabled")

    quiz_questions = []                                      # empty = the next click starts a NEW quiz
    quiz_main_button.config(text="Try Again", state="normal")
    refresh_progress()


# ---------------------------------------------------------------------
# 7. FUNCTIONS FOR THE PROGRESS TAB
# ---------------------------------------------------------------------

def refresh_progress():
    """Read the saved results and show them."""
    results = load_results()
    history_list.delete(0, tk.END)                           # clear the list

    total_score = 0
    total_questions = 0
    for result in results:                                   # result = [date, language, category, score, total]
        line = result[0] + "   " + result[1] + "   " + result[2] + "   " + result[3] + "/" + result[4]
        history_list.insert(tk.END, line)
        total_score = total_score + int(result[3])           # int() turns the text "7" into the number 7
        total_questions = total_questions + int(result[4])

    if len(results) == 0:
        summary_label.config(text="No quizzes yet. Try the Quiz tab!")
        accuracy_bar["value"] = 0
    else:
        accuracy = total_score / total_questions * 100
        summary_label.config(text=str(len(results)) + " quizzes   -   overall accuracy " + str(int(accuracy)) + "%")
        accuracy_bar["value"] = accuracy


# ---------------------------------------------------------------------
# 8. FUNCTIONS FOR THE TOP BAR AND TABS
# ---------------------------------------------------------------------

def selection_changed(event=None):
    """Runs when the user picks a different language or category."""
    global learn_cards, learn_index, translation_showing
    learn_cards = get_cards(language_box.get(), category_box.get())
    learn_index = 0
    translation_showing = False
    show_learn_card()
    reset_quiz()


def tab_changed(event):
    refresh_progress()


# ---------------------------------------------------------------------
# 9. BUILDING THE WINDOW
# ---------------------------------------------------------------------
root = tk.Tk()
root.title("Language Learning App")
root.geometry("640x580")
root.configure(bg="#fffbeb")

# ---------- Top bar: language + category ----------
top_bar = tk.Frame(root, bg="#fffbeb")
top_bar.pack(fill="x", padx=15, pady=10)

tk.Label(top_bar, text="Language:", bg="#fffbeb", font=("Arial", 11, "bold")).pack(side="left")
language_box = ttk.Combobox(top_bar, values=["Spanish", "French", "German"], state="readonly", width=10)
language_box.set("Spanish")
language_box.pack(side="left", padx=(5, 20))

tk.Label(top_bar, text="Category:", bg="#fffbeb", font=("Arial", 11, "bold")).pack(side="left")
category_box = ttk.Combobox(top_bar, values=[DAILY_LESSON, "Vocabulary", "Phrases", "Grammar"],
                            state="readonly", width=22)
category_box.set(DAILY_LESSON)
category_box.pack(side="left", padx=5)

language_box.bind("<<ComboboxSelected>>", selection_changed)
category_box.bind("<<ComboboxSelected>>", selection_changed)

# ---------- The three tabs ----------
tabs = ttk.Notebook(root)
tabs.pack(fill="both", expand=True, padx=15, pady=10)

learn_tab = tk.Frame(tabs, bg="#fffbeb")
quiz_tab = tk.Frame(tabs, bg="#fffbeb")
progress_tab = tk.Frame(tabs, bg="#fffbeb")
tabs.add(learn_tab, text="  Learn  ")
tabs.add(quiz_tab, text="  Quiz  ")
tabs.add(progress_tab, text="  Progress  ")

# ---------- Learn tab ----------
learn_counter = tk.Label(learn_tab, text="", bg="#fffbeb", font=("Arial", 10, "bold"))
learn_counter.pack(pady=10)

card_frame = tk.Frame(learn_tab, bg="white", highlightthickness=2, highlightbackground="#fcd34d")
card_frame.pack(fill="both", expand=True, padx=20, pady=5)

tk.Label(card_frame, text="ENGLISH", bg="white", fg="gray", font=("Arial", 9, "bold")).pack(pady=(12, 0))
english_label = tk.Label(card_frame, text="", bg="white", font=("Arial", 22, "bold"), wraplength=480)
english_label.pack(pady=(0, 15))
translation_label = tk.Label(card_frame, text="", bg="white", fg="#d97706", font=("Arial", 24, "bold"), wraplength=480)
translation_label.pack(pady=5)
pron_label = tk.Label(card_frame, text="", bg="white", fg="#57534e", font=("Arial", 14, "italic"), wraplength=480)
pron_label.pack()

reveal_button = tk.Button(learn_tab, text="Show Translation", font=("Arial", 12, "bold"), command=toggle_translation)
reveal_button.pack(pady=8)

learn_nav = tk.Frame(learn_tab, bg="#fffbeb")
learn_nav.pack(pady=(0, 10))
tk.Button(learn_nav, text="< Previous", width=12, command=previous_learn_card).pack(side="left", padx=5)
tk.Button(learn_nav, text="Next >", width=12, command=next_learn_card).pack(side="left", padx=5)

# ---------- Quiz tab ----------
quiz_status = tk.Label(quiz_tab, text="", bg="#fffbeb", font=("Arial", 10, "bold"))
quiz_status.pack(pady=10)

quiz_question_label = tk.Label(quiz_tab, text="", bg="#fffbeb", font=("Arial", 18, "bold"), wraplength=520)
quiz_question_label.pack(pady=10)

# Make the 4 answer buttons and keep them together in one list
option_buttons = []
button_0 = tk.Button(quiz_tab, width=34, font=("Arial", 12), command=click_option_0)
button_1 = tk.Button(quiz_tab, width=34, font=("Arial", 12), command=click_option_1)
button_2 = tk.Button(quiz_tab, width=34, font=("Arial", 12), command=click_option_2)
button_3 = tk.Button(quiz_tab, width=34, font=("Arial", 12), command=click_option_3)
option_buttons.append(button_0)
option_buttons.append(button_1)
option_buttons.append(button_2)
option_buttons.append(button_3)
for button in option_buttons:
    button.pack(pady=3)

feedback_label = tk.Label(quiz_tab, text="", bg="#fffbeb", font=("Arial", 12, "bold"))
feedback_label.pack(pady=8)

quiz_main_button = tk.Button(quiz_tab, text="Start Quiz", font=("Arial", 12, "bold"), command=quiz_main_click)
quiz_main_button.pack(pady=5)

# ---------- Progress tab ----------
summary_label = tk.Label(progress_tab, text="", bg="#fffbeb", font=("Arial", 13, "bold"))
summary_label.pack(pady=(15, 5))
accuracy_bar = ttk.Progressbar(progress_tab, maximum=100, length=360)
accuracy_bar.pack(pady=(0, 10))
tk.Label(progress_tab, text="Date   Language   Category   Score", bg="#fffbeb", fg="gray").pack(anchor="w", padx=15)
history_list = tk.Listbox(progress_tab, height=12, font=("Courier", 10))
history_list.pack(fill="both", expand=True, padx=15, pady=5)

tabs.bind("<<NotebookTabChanged>>", tab_changed)

# Load the first set of cards and the saved progress
selection_changed()
refresh_progress()


# ---------------------------------------------------------------------
# 10. STARTING THE APP
# ---------------------------------------------------------------------
if __name__ == "__main__":
    root.mainloop()
