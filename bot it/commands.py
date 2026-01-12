#Команды бота.
from telebot import types
start_text = ("Это бот учебной части Колледжа IT TOP\n\n"
         "Для работы бота надо загрузить excel файл и выбрать тип отчета который вы хотите видеть.")

def main_keybard():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("Рассписание групп","Тему уроков")
    kb.add("Отсчёт по студентам","Посещаемость студентов")
    kb.add("Проверенные ДЗ","Сданные ДЗ")
    return kb