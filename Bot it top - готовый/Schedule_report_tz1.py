# 1 тех-задание - полное рассписание на неделю
import pandas as pd

def ScheduleReport(file_path: str) -> str:
    df = pd.read_excel(file_path)
    subjects = {}
# есть ли те колонки которые нам нужны
    for col in df.columns:
        if "Время" in str(col):
            continue

        for value in df[col]:
            if pd.isna(value):
                continue

            text = str(value)
            if "Предмет:" in text:
                part = text.split("Предмет:", 1)[1]
                part = part.split("Группа:")[0]
                subject = part.strip()

                if subject:
                    subjects[subject] = subjects.get(subject, 0) + 1

    if not subjects:
        return "В файле не найдены предметы (строки с 'Предмет:')."

    msg = "Отчёт по расписанию (кол-во пар по дисциплинам):\n\n"
    for name, count in subjects.items():
        msg += f"- {name} — {count} пар\n"

    return msg
