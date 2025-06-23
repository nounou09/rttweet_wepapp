import telebot
import json
import random
from telebot.types import (
    InlineKeyboardMarkup, InlineKeyboardButton,
    WebAppInfo, ReplyKeyboardMarkup, KeyboardButton
)

BOT_TOKEN = 'ضع_توكن_البوت_هنا'
bot = telebot.TeleBot(BOT_TOKEN)

# تحميل الأسئلة
with open("questions.json", "r", encoding="utf-8") as f:
    all_questions = json.load(f)

user_states = {}
scores = {}

def save_scores():
    with open("scores.json", "w", encoding="utf-8") as f:
        json.dump(scores, f, ensure_ascii=False, indent=2)

def load_scores():
    global scores
    try:
        with open("scores.json", "r", encoding="utf-8") as f:
            scores = json.load(f)
    except:
        scores = {}

def get_question(user_id):
    state = user_states[user_id]
    difficulty = "easy"
    if state["score"] >= 15:
        difficulty = "expert"
    elif state["score"] >= 10:
        difficulty = "hard"
    elif state["score"] >= 5:
        difficulty = "medium"

    questions = [q for q in all_questions if q["difficulty"] == difficulty]
    if state["category"] != "random":
        questions = [q for q in questions if q["category"] == state["category"]]
    question = random.choice(questions)
    state["current_question"] = question
    return question

def ask_continue(user_id):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🔁 نعم", callback_data="continue_yes"),
               InlineKeyboardButton("🛑 لا", callback_data="continue_no"))
    bot.send_message(user_id, "هل تريد الاستمرار؟", reply_markup=markup)

def send_question(user_id):
    q = get_question(user_id)
    markup = InlineKeyboardMarkup()
    options = q["options"]
    random.shuffle(options)
    for opt in options:
        markup.add(InlineKeyboardButton(opt, callback_data="ans_" + opt))
    bot.send_message(user_id, f'❓ *{q["question"]}*', parse_mode="Markdown", reply_markup=markup)

@bot.message_handler(commands=["start"])
def start(msg):
    user_id = msg.chat.id
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🎲 أسئلة عشوائية", callback_data="cat_random"))
    markup.add(InlineKeyboardButton("📂 اختيار فئة", callback_data="choose_category"))
    bot.send_message(user_id, "🎮 اختر طريقة اللعب:", reply_markup=markup)

@bot.message_handler(commands=["menu"])
def show_menu(msg):
    markup = ReplyKeyboardMarkup(resize
