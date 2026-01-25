# Основной файл бота
import os
import telebot
from telebot import types

from commands import start_text, main_keyboard
from Schedule_report_tz1 import ScheduleReport
from Report_on_lesson_topics_tz2 import get_bad_topics
from Student_Report_tz3 import StudentsReport
from Student_Attendance_Report_tz4 import StudentsAttendanceReport
from Report_on_checked_homework_assignments_tz5 import HomeworkCheckedReport
from Homework_report_tz6 import HomeworkDoneReport

TOKEN = "8019278054:AAF4T2rztALi87as6OmmEnD7fz977KF4Rg8"

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

bot = telebot.TeleBot(TOKEN)

user_files = {}
user_topics = {}
user_indexes = {}
user_state = {}

dz5_state = {}
dz5_data = {}
dz5_last_period = {}

CHUNK = 4000


def send_long(chat_id, msg):
    if len(msg) <= 4000:
        bot.send_message(chat_id, msg)
        return
    for i in range(0, len(msg), 4000):
        bot.send_message(chat_id, msg[i:i+4000])


# =============== ТЗ2 Темы уроков ===============

def send_topics_chunk(chat_id, user_id):
    topics = user_topics[user_id]
    index = user_indexes[user_id]
    text = ""

    while index < len(topics) and (len(text) + len(topics[index]) < CHUNK):
        text += "- " + topics[index] + "\n"
        index += 1

    bot.send_message(chat_id, text)
    user_indexes[user_id] = index

    if index < len(topics):
        kb = types.InlineKeyboardMarkup()
        kb.add(
            types.InlineKeyboardButton("Дальше", callback_data="topics_next"),
            types.InlineKeyboardButton("Все сразу", callback_data="topics_all")
        )
        bot.send_message(chat_id, f"Показано {index} из {len(topics)} строк.", reply_markup=kb)
    else:
        bot.send_message(chat_id, "Больше тем нет.")


@bot.callback_query_handler(func=lambda call: call.data == "topics_next")
def callback_topics_next(call):
    bot.answer_callback_query(call.id)
    send_topics_chunk(call.message.chat.id, call.from_user.id)


@bot.callback_query_handler(func=lambda call: call.data == "topics_all")
def callback_topics_all(call):
    bot.answer_callback_query(call.id)
    topics = user_topics[call.from_user.id]
    text = ""
    for t in topics:
        line = "- " + t + "\n"
        if len(text) + len(line) >= CHUNK:
            bot.send_message(call.message.chat.id, text)
            text = ""
        text += line
    if text:
        bot.send_message(call.message.chat.id, text)
    bot.send_message(call.message.chat.id, "Больше тем нет.")


# =============== ТЗ5 Проверенные ДЗ ===============

@bot.callback_query_handler(func=lambda call: call.data in ["dz5_70", "dz5_custom"])
def callback_dz5(call):
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    bot.answer_callback_query(call.id)

    if user_id not in user_files:
        bot.send_message(chat_id, "Сначала загрузите Excel файл.")
        return

    if call.data == "dz5_70":
        dz5_data[user_id] = {"percent": 70}
        dz5_state[user_id] = "select_period"
        select_period(chat_id)
        return

    if call.data == "dz5_custom":
        dz5_state[user_id] = "input_percent"
        bot.send_message(chat_id, "Введите процент (0-100):")
        return


@bot.callback_query_handler(func=lambda call: call.data in ["dz5_month", "dz5_week"])
def callback_dz5_period(call):
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    bot.answer_callback_query(call.id)

    if user_id not in dz5_data:
        bot.send_message(chat_id, "Ошибка: нет процента.")
        return

    period = "month" if call.data == "dz5_month" else "week"
    percent = dz5_data[user_id]["percent"]
    file_path = user_files[user_id]

    dz5_last_period[user_id] = period

    msg = HomeworkCheckedReport(file_path, period, percent)

    kb = types.InlineKeyboardMarkup()
    if period == "month":
        kb.add(types.InlineKeyboardButton("Посмотреть за неделю", callback_data="dz5_switch_week"))
    else:
        kb.add(types.InlineKeyboardButton("Посмотреть за месяц", callback_data="dz5_switch_month"))

    bot.send_message(chat_id, msg, reply_markup=kb)


@bot.callback_query_handler(func=lambda call: call.data in ["dz5_switch_week", "dz5_switch_month"])
def callback_dz5_switch(call):
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    bot.answer_callback_query(call.id)

    if user_id not in dz5_data or user_id not in dz5_last_period:
        bot.send_message(chat_id, "Сначала выберите фильтр.")
        return

    percent = dz5_data[user_id]["percent"]
    file_path = user_files[user_id]

    if call.data == "dz5_switch_week":
        period = "week"
    else:
        period = "month"

    dz5_last_period[user_id] = period

    msg = HomeworkCheckedReport(file_path, period, percent)

    kb = types.InlineKeyboardMarkup()
    if period == "month":
        kb.add(types.InlineKeyboardButton("Посмотреть за неделю", callback_data="dz5_switch_week"))
    else:
        kb.add(types.InlineKeyboardButton("Посмотреть за месяц", callback_data="dz5_switch_month"))

    bot.send_message(chat_id, msg, reply_markup=kb)


def select_period(chat_id):
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("За месяц", callback_data="dz5_month"))
    kb.add(types.InlineKeyboardButton("За неделю", callback_data="dz5_week"))
    bot.send_message(chat_id, "Выберите период:", reply_markup=kb)


# =============== Команды ===============

@bot.message_handler(commands=["start", "menu"])
def start(message):
    user_id = message.from_user.id

    if user_id in user_files:
        try:
            os.remove(user_files[user_id])
        except:
            pass
        del user_files[user_id]

    bot.send_message(message.chat.id, start_text, reply_markup=main_keyboard())


# =============== Приём файла ===============

@bot.message_handler(content_types=["document"])
def handle_file(message):
    user_id = message.from_user.id

    if user_id in user_files:
        try:
            os.remove(user_files[user_id])
        except:
            pass
        del user_files[user_id]

    file_info = bot.get_file(message.document.file_id)
    data = bot.download_file(file_info.file_path)

    path = os.path.join(UPLOAD_DIR, message.document.file_name)
    with open(path, "wb") as f:
        f.write(data)

    user_files[user_id] = path
    bot.send_message(message.chat.id, "Файл загружен. Теперь выберите отчёт.")


# =============== Обработка текста ===============

@bot.message_handler(func=lambda m: True)
def handle_report(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    text = message.text

    # ввод процента ТЗ5
    if user_id in dz5_state and dz5_state[user_id] == "input_percent":
        try:
            value = float(text)
            if not (0 <= value <= 100):
                bot.send_message(chat_id, "Введите число от 0 до 100.")
                return
        except:
            bot.send_message(chat_id, "Введите число, например: 55")
            return

        dz5_data[user_id] = {"percent": value}
        dz5_state[user_id] = "select_period"
        select_period(chat_id)
        return

    if text == "Главное меню":
        start(message)
        return

    if user_id not in user_files:
        bot.send_message(chat_id, "Сначала отправьте Excel файл.")
        return

    file_path = user_files[user_id]

    if text == "Расписание групп":
        send_long(chat_id, ScheduleReport(file_path))

    elif text == "Темы уроков":
        topics, msg = get_bad_topics(file_path)
        if msg:
            bot.send_message(chat_id, msg)
            return
        user_topics[user_id] = topics
        user_indexes[user_id] = 0
        send_topics_chunk(chat_id, user_id)

    elif text == "Отчет по студентам":
        send_long(chat_id, StudentsReport(file_path))

    elif text == "Посещаемость студентов":
        msg = StudentsAttendanceReport(file_path, 40)
        send_long(chat_id, msg)

    elif text == "Проверенные ДЗ":
        kb = types.InlineKeyboardMarkup()
        kb.add(types.InlineKeyboardButton("Меньше 70%", callback_data="dz5_70"))
        kb.add(types.InlineKeyboardButton("Ввести свой %", callback_data="dz5_custom"))
        bot.send_message(chat_id, "Выберите фильтр:", reply_markup=kb)

    elif text == "Сданные ДЗ":
        send_long(chat_id, HomeworkDoneReport(file_path))

    else:
        bot.send_message(chat_id, "Не понял. Выберите кнопку или /menu.")


bot.infinity_polling()
