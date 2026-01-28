#команды бота
from telebot import types

start_text = (
    "Добро пожаловать.\n"
    "Этот бот предназначен для генерации отчетов по Excel файлам.\n\n"
    "1. Отправьте файл Excel.\n"
    "2. Выберите тип отчета.\n"
    "3. Для возврата в меню используйте /menu."
)
def main_keyboard():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row("Расписание групп", "Темы уроков")
    kb.row("Отчет по студентам", "Посещаемость студентов")
    kb.row("Проверенные ДЗ", "Сданные ДЗ")
    kb.row("Главное меню")
    return kb
