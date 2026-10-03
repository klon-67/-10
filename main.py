import tkinter as tk
import random

# =========================
# НАЛАШТУВАННЯ
# =========================

MAX_BOMB = 100

bomb = MAX_BOMB
score = 0
high_score = 0
level = 1
combo = 0
game_running = False


# =========================
# ВІКНО
# =========================

root = tk.Tk()
root.title("💣 Bomb Clicker")
root.geometry("600x700")
root.resizable(False, False)


# =========================
# ЗАГОЛОВОК
# =========================

title_label = tk.Label(
    root,
    text="💣 BOMB CLICKER 💣",
    font=("Comic Sans MS", 26, "bold")
)
title_label.pack(pady=15)


info_label = tk.Label(
    root,
    text="Натисни ENTER, щоб почати!",
    font=("Comic Sans MS", 14)
)
info_label.pack()


# =========================
# ІНФОРМАЦІЯ
# =========================

stats_frame = tk.Frame(root)
stats_frame.pack(pady=15)

fuse_label = tk.Label(
    stats_frame,
    text="Fuse: 100",
    font=("Comic Sans MS", 14)
)
fuse_label.grid(row=0, column=0, padx=15)

score_label = tk.Label(
    stats_frame,
    text="Score: 0",
    font=("Comic Sans MS", 14)
)
score_label.grid(row=0, column=1, padx=15)

level_label = tk.Label(
    stats_frame,
    text="Level: 1",
    font=("Comic Sans MS", 14)
)
level_label.grid(row=0, column=2, padx=15)


high_score_label = tk.Label(
    root,
    text="🏆 Record: 0",
    font=("Comic Sans MS", 14, "bold")
)
high_score_label.pack()


# =========================
# ПРОГРЕС-БАР
# =========================

progress = tk.Canvas(
    root,
    width=450,
    height=30,
    highlightthickness=0
)
progress.pack(pady=15)


def draw_progress():
    progress.delete("all")

    width = 450
    current_width = int(width * bomb / MAX_BOMB)

    if bomb > 60:
        color = "green"
    elif bomb > 30:
        color = "orange"
    else:
        color = "red"

    progress.create_rectangle(
        0,
        0,
        width,
        30,
        fill="lightgray"
    )

    progress.create_rectangle(
        0,
        0,
        current_width,
        30,
        fill=color
    )

    progress.create_text(
        width // 2,
        15,
        text=f"{bomb} / {MAX_BOMB}",
        font=("Arial", 12, "bold")
    )


# =========================
# КАРТИНКИ
# =========================

img_1 = tk.PhotoImage(file="bomb_1.png").subsample(3, 3)
img_2 = tk.PhotoImage(file="bomb_2.png").subsample(3, 3)
img_3 = tk.PhotoImage(file="bomb_3.png").subsample(3, 3)
img_4 = tk.PhotoImage(file="bomb_4.png").subsample(3, 3)


bomb_label = tk.Label(
    root,
    image=img_1
)
bomb_label.pack(pady=20)


# =========================
# ОНОВЛЕННЯ ЕКРАНУ
# =========================

def update_display():

    fuse_label.config(
        text=f"Fuse: {bomb}"
    )

    score_label.config(
        text=f"Score: {score}"
    )

    level_label.config(
        text=f"Level: {level}"
    )

    high_score_label.config(
        text=f"🏆 Record: {high_score}"
    )

    draw_progress()

    # Зміна картинки
    if bomb >= 80:
        bomb_label.config(image=img_1)

    elif bomb >= 50:
        bomb_label.config(image=img_2)

    elif bomb > 0:
        bomb_label.config(image=img_3)

    else:
        bomb_label.config(image=img_4)


# =========================
# ВИБУХ
# =========================

def explode():

    global game_running

    game_running = False

    bomb_label.config(image=img_4)

    info_label.config(
        text=f"💥 BANG! Твій результат: {score}"
    )

    click_button.config(
        text="🔄 НОВА ГРА",
        state="normal"
    )


# =========================
# ЗМЕНШЕННЯ БОМБИ
# =========================

def update_bomb():

    global bomb

    if not game_running:
        return

    bomb -= 1 + level

    if bomb <= 0:
        bomb = 0
        update_display()
        explode()
        return

    update_display()

    # Чим більший рівень,
    # тим швидше падає бомба
    speed = max(100, 500 - level * 30)

    root.after(speed, update_bomb)


# =========================
# ОЧКИ
# =========================

def update_score():

    global score, level

    if not game_running:
        return

    score += 1

    # Новий рівень кожні 10 очок
    new_level = score // 10 + 1

    if new_level > level:
        level = new_level
        info_label.config(
            text=f"🔥 РІВЕНЬ {level}! Бомба стала швидшою!"
        )

    update_display()

    root.after(1000, update_score)


# =========================
# КЛІК ПО БОМБІ
# =========================

def click_bomb():

    global bomb
    global score
    global combo
    global high_score

    if not game_running:
        start_game()
        return

    # Випадкова кількість заряду
    power = random.randint(2, 6)

    bomb += power

    # Комбо
    combo += 1

    # Кожні 10 кліків бонус
    if combo % 10 == 0:
        bomb += 10
        score += 5

        info_label.config(
            text="🔥 COMBO! +10 до бомби та +5 очок!"
        )

    else:
        info_label.config(
            text=f"💥 +{power} до запобіжника!"
        )

    # Максимум 100
    if bomb > MAX_BOMB:
        bomb = MAX_BOMB

    if score > high_score:
        high_score = score

    update_display()


# =========================
# ПОЧАТОК ГРИ
# =========================

def start_game(event=None):

    global bomb
    global score
    global level
    global combo
    global game_running

    bomb = MAX_BOMB
    score = 0
    level = 1
    combo = 0

    game_running = True

    click_button.config(
        text="💣 CLICK!",
        state="normal"
    )

    info_label.config(
        text="Клікай по бомбі! Не дай їй вибухнути!"
    )

    update_display()

    update_bomb()
    update_score()


# =========================
# КНОПКА
# =========================

click_button = tk.Button(
    root,
    text="💣 START!",
    width=18,
    height=2,
    font=("Comic Sans MS", 16, "bold"),
    command=click_bomb
)

click_button.pack(pady=20)


# =========================
# КЕРУВАННЯ ENTER
# =========================

root.bind("<Return>", start_game)


# =========================
# СТАРТОВИЙ ЕКРАН
# =========================

update_display()

root.mainloop()
