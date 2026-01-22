# 2 тех-задание - Неправельные темы уроков
import pandas as pd

def TopicsReport(file_path: str) -> str:
    df = pd.read_excel(file_path)

    if "Тема урока" not in df.columns:
        return "В файле нет колонки 'Тема урока'."

    bad = []

    for value in df["Тема урока"]:
        if pd.isna(value):
            continue

        text = str(value).strip()

        if text.lower().startswith("урок"):
            if "тема:" not in text.lower():
                bad.append(text)
            continue

        bad.append(text)

    if not bad:
        return "Все темы оформлены правильно!"

    msg = "⚠ Темы, которые НЕ соответствуют формату 'Урок _. Тема: _':\n\n"
    for t in bad:
        msg += f"- {t}\n"

    return msg
