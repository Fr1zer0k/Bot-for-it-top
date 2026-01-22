# Основной файл бота
import os
import telebot


from commands import start_text, main_keyboard
from Schedule_report_tz1 import ScheduleReport
from Report_on_lesson_topics_tz2 import TopicsReport
from Student_Report_tz3 import StudentsReport
from Student_Attendance_Report_tz4 import StudentsAttendanceReport
from Report_on_checked_homework_assignments_tz5 import HomeworkCheckedReport
from Homework_report_tz6 import HomeworkDoneReport


TOKEN = "8019278054:AAF4T2rztALi87as6OmmEnD7fz977KF4Rg8"

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

bot = telebot.TeleBot(TOKEN)
user_files = {}   # user_id -> file_path

def send_big_message(chat_id, text):
    MAX_LEN = 4000

    if len(text) <= MAX_LEN:
        bot.send_message(chat_id, text)
        return

    for i in range(0, len(text), MAX_LEN):
        bot.send_message(chat_id, text[i:i + MAX_LEN])

@bot.message_handler(commands=["start", "menu"])
def start(message):
    user_id = message.from_user.id

    # удаляем файл если был
    if user_id in user_files:
        try:
            os.remove(user_files[user_id])
        except:
            pass
        del user_files[user_id]

    bot.send_message(message.chat.id, start_text, reply_markup=main_keyboard())


@bot.message_handler(content_types=["document"])
def handle_file(message):
    user_id = message.from_user.id

    # если был предыдущий файл — удаляем
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
    bot.send_message(message.chat.id, "📎 Файл загружен! Теперь выбери отчёт.")


@bot.message_handler(func=lambda m: True)
def handle_report(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    text = message.text

    if text == "🏠 Главное меню":
        start(message)
        return

    if user_id not in user_files:
        bot.send_message(chat_id, "Сначала отправь Excel-файл.")
        return

    file_path = user_files[user_id]

    if text == "Расписание групп":
        result = ScheduleReport(file_path)
    elif text == "Темы уроков":
        result = TopicsReport(file_path)
    elif text == "Отчет по студентам":
        result = StudentsReport(file_path)
    elif text == "Посещаемость студентов":
        result = StudentsAttendanceReport(file_path)
    elif text == "Проверенные ДЗ":
        result = HomeworkCheckedReport(file_path)
    elif text == "Сданные ДЗ":
        result = HomeworkDoneReport(file_path)
    else:
        bot.send_message(chat_id, "Не понял, выбери кнопку или /menu.")
        return

    send_big_message(chat_id, result)

bot.infinity_polling()

