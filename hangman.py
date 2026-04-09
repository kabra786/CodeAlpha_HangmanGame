import tkinter as tk
import random

# ================= WORDS =================
levels = {
    1: ["cat", "dog", "sun"],
    2: ["book", "tree", "milk"],
    3: ["apple", "chair", "house"],
    4: ["python", "mouse", "table"],
    5: ["window", "school", "orange"],
    6: ["laptop", "keyboard", "monitor"],
    7: ["developer", "hangman", "project"],
    8: ["algorithm", "database", "network"],
    9: ["programming", "framework", "variable"],
    10: ["artificial", "intelligence", "application"]
}

level = 1
lives = 6
score = 0
word = ""
guessed = []

# ================= WINDOW =================
window = tk.Tk()
window.title("🎮 Hangman Game")
window.geometry("1100x1100")
window.config(bg="#fffbeb")

# ================= EFFECTS =================
def flash(color):
    original = window.cget("bg")
    window.config(bg=color)
    window.after(150, lambda: window.config(bg=original))

def button_glow(btn):
    original = btn.cget("bg")
    btn.config(bg="#22c55e")
    window.after(120, lambda: btn.config(bg=original))

# ================= CANVAS =================
canvas = tk.Canvas(window, width=1000, height=350, bg="#fffbeb", highlightthickness=0)
canvas.pack()

particles = []

def create_confetti():
    colors = ["#ff4d6d", "#ffd60a", "#38bdf8", "#22c55e", "#f97316"]
    for _ in range(60):
        particles.append([
            random.randint(200, 800),
            50,
            random.uniform(-3, 3),
            random.uniform(2, 6),
            random.choice(colors)
        ])

def animate_confetti():
    canvas.delete("confetti")
    for p in particles:
        x, y, dx, dy, color = p
        canvas.create_oval(x, y, x+8, y+8, fill=color, outline="", tags="confetti")
        p[0] += dx
        p[1] += dy
        p[3] += 0.3
    if particles:
        window.after(40, animate_confetti)

# ================= HANGMAN =================
def draw_hangman():
    canvas.delete("hangman")

    canvas.create_line(50, 300, 200, 300, width=4, tags="hangman")
    canvas.create_line(100, 300, 100, 50, width=4, tags="hangman")
    canvas.create_line(100, 50, 200, 50, width=4, tags="hangman")
    canvas.create_line(200, 50, 200, 90, width=4, tags="hangman")

    if lives <= 5:
        canvas.create_oval(170, 90, 230, 150, width=3, tags="hangman")
    if lives <= 4:
        canvas.create_line(200, 150, 200, 230, width=3, tags="hangman")
    if lives <= 3:
        canvas.create_line(200, 170, 160, 200, width=3, tags="hangman")
    if lives <= 2:
        canvas.create_line(200, 170, 240, 200, width=3, tags="hangman")
    if lives <= 1:
        canvas.create_line(200, 230, 170, 280, width=3, tags="hangman")
    if lives == 0:
        canvas.create_line(200, 230, 230, 280, width=3, tags="hangman")

# ================= PROGRESS =================
progress_canvas = tk.Canvas(window, width=350, height=20, bg="#ddd", highlightthickness=0)
progress_canvas.pack(pady=10)

def update_progress():
    progress_canvas.delete("all")
    width = (level / 10) * 350
    progress_canvas.create_rectangle(0, 0, width, 20, fill="#22c55e")

# ================= GAME =================
def new_word():
    global word, guessed
    word = random.choice(levels[level])
    guessed = []
    update()

def update():
    display = "  ".join([l if l in guessed else "_" for l in word])

    word_label.config(text=display)
    lives_label.config(text=f"❤️ Lives: {lives}")
    score_label.config(text=f"🏆 Score: {score}")
    level_label.config(text=f"🎯 Level: {level}/10")

    update_progress()
    draw_hangman()

    if "_" not in display:
        win()

    if lives == 0:
        lose()

# ================= GUESS =================
def guess(letter, btn):
    global lives, score

    button_glow(btn)

    if letter in guessed:
        return

    guessed.append(letter)

    if letter not in word:
        lives -= 1
    else:
        score += 10

    update()

# ================= WIN / LOSE =================
def win():
    global level

    flash("#a7f3d0")
    create_confetti()
    animate_confetti()

    result_label.config(text="🎉 LEVEL COMPLETE!", fg="#16a34a")
    window.after(1500, next_level)

def lose():
    flash("#fecaca")
    result_label.config(text=f"💀 GAME OVER! Word: {word}", fg="#dc2626")

# ================= NEXT LEVEL =================
def next_level():
    global level, lives

    if level < 10:
        level += 1
        lives = 6
        new_word()
        result_label.config(text="")
    else:
        result_label.config(text="🏆 YOU COMPLETED ALL LEVELS!", fg="#22c55e")

# ================= RESTART =================
def restart():
    global level, lives, score

    level = 1
    lives = 6
    score = 0

    flash("#fde68a")
    new_word()
    result_label.config(text="")

# ================= UI =================
tk.Label(window, text="🎮 HANGMAN GAME",
         font=("Arial", 30, "bold"),
         bg="#fffbeb", fg="#2563eb").pack(pady=10)

level_label = tk.Label(window, text="", font=("Arial", 14),
                       bg="#fffbeb", fg="#f59e0b")
level_label.pack()

word_label = tk.Label(window, text="", font=("Courier", 36, "bold"),
                      bg="#fffbeb", fg="#dc2626")
word_label.pack(pady=10)

lives_label = tk.Label(window, text="", font=("Arial", 14),
                       bg="#fffbeb", fg="#1d4ed8")
lives_label.pack()

score_label = tk.Label(window, text="", font=("Arial", 14),
                       bg="#fffbeb", fg="#16a34a")
score_label.pack()

result_label = tk.Label(window, text="", font=("Arial", 18, "bold"),
                        bg="#fffbeb")
result_label.pack(pady=10)

# ================= BUTTONS =================
frame = tk.Frame(window, bg="#fffbeb")
frame.pack(pady=5)

alphabet = "abcdefghijklmnopqrstuvwxyz"

# split into 2 rows
row1 = alphabet[:13]   # A–M
row2 = alphabet[13:]   # N–Z

buttons = []

# Row 1
for col, letter in enumerate(row1):
    btn = tk.Button(frame, text=letter.upper(),
                    width=4, height=2,
                    bg="#fcd34d", fg="black",
                    activebackground="#34d399")

    btn.grid(row=0, column=col, padx=3, pady=5)
    btn.config(command=lambda l=letter, b=btn: guess(l, b))
    buttons.append(btn)

# Row 2
for col, letter in enumerate(row2):
    btn = tk.Button(frame, text=letter.upper(),
                    width=4, height=2,
                    bg="#fcd34d", fg="black",
                    activebackground="#34d399")

    btn.grid(row=1, column=col, padx=3, pady=5)
    btn.config(command=lambda l=letter, b=btn: guess(l, b))
    buttons.append(btn)

# ================= CONTROL =================
tk.Button(window, text="🔄 Restart",
          font=("Arial", 12, "bold"),
          bg="#22c55e", command=restart).pack(pady=10)

# ================= START =================
new_word()
window.mainloop()