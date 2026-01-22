#команды бота
from telebot import types


start_text = (
    "Привет! \n"
    "Я бот для отчётов по Excel.\n\n"
    "1 - Отправь мне файл .xls / .xlsx\n"
    "2 - Нажми кнопку с нужным отчётом.\n"
    "3 - Команда /menu — вернуться в начало"
)

def main_keyboard():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row("Расписание групп", "Темы уроков")
    kb.row("Отчет по студентам", "Посещаемость студентов")
    kb.row("Проверенные ДЗ", "Сданные ДЗ")
    kb.row("Главное меню")
    return kb
