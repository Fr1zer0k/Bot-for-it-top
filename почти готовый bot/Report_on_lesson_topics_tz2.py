# 2 тех-задание - Неправельные темы уроков
import pandas as pd

def get_bad_topics(file_path: str):
    df = pd.read_excel(file_path)
#проверяем есть ли те колонки которые нам нужны
    if "Тема урока" not in df.columns:
        return [], "В файле нет колонки 'Тема урока'."

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
        return [], "Все темы оформлены правильно."

    return bad, ""
