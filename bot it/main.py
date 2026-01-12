#Основной файл с реализацией.
import os
import telebot
from commands import start_text, main_keybard

#from Schedule_report_tz1 import ScheduleReport
##from Student_Report_tz3 import StudentsReport
#from Student_Attendance_Report_tz4 import StudentsAttendanceReport
#from Report_on_checked_homework_assignments_tz5 import HomeworkCheckedReport
#from Homework_report_tz6 import HomeworkDoneReport

TOKEN = ""
UPLOAD_DIR = "uploads"

bot = telebot.TeleBot(TOKEN)
os.makedirs(UPLOAD_DIR, exist_ok=True)

user_state = {}

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, start_text, reply_markup=main_keybard())

@bot.message_handler(content_types=["document"])
def handle_file(message):
    file_info = bot.get_file(message.document.file_id)
    data = bot.download_file(file_info.file_path)

    path = os.path.join(UPLOAD_DIR, message.document.file_name)
    with open(path, "wb") as f:
        f.write(data)

    user_state[message.from_user.id] = {"file": path}
    bot.send_message(message.chat.id, "📎 Файл загружен. Выберите отчет.")

@bot.message_handler(func=lambda m: m.text.isdigit())
def handle_percent(message):
    user_state[message.from_user.id]["percent"] = int(message.text)

@bot.message_handler(func=lambda m: True)
def handle_report(message):
    state = user_state.get(message.from_user.id)
    if not state:
        return

    file_path = state["file"]
    percent = state.get("percent", 70)

    if message.text == "📅 Расписание групп":
        ScheduleReport(file_path)

    elif message.text == "📘 Темы уроков":
        TopicsReport(file_path)

    elif message.text == "👥 Отчет по студентам":
        StudentsReport(file_path)

    elif message.text == "📊 Посещаемость студентов":
        bot.send_message(message.chat.id, "Введите процент:")
        StudentsAttendanceReport(file_path, percent)

    elif message.text == "📝 Проверенные ДЗ":
        HomeworkCheckedReport(file_path, percent, "Месяц")

    elif message.text == "✅ Сданные ДЗ":
        HomeworkDoneReport(file_path, percent)

    else:
        return

    bot.send_message(message.chat.id)
bot.infinity_polling()