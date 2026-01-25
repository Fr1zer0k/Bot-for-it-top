# 4 тех-задание - посещаемость
import pandas as pd

def StudentsAttendanceReport(file_path: str, percent: float = 40):
    df = pd.read_excel(file_path)

#роверяем есть ли те колонки которые нам нужны
    if "ФИО преподавателя" not in df.columns or "Средняя посещаемость" not in df.columns:
        return "Файл не содержит колонок 'ФИО преподавателя' и 'Средняя посещаемость'."

    df = df[df["ФИО преподавателя"].notna()].copy()

    df["percent"] = (
        df["Средняя посещаемость"]
        .astype(str)
        .str.replace("%", "", regex=False)
        .str.replace(",", ".", regex=False)
    )
    df["percent"] = pd.to_numeric(df["percent"], errors="coerce")

    # фильтр по переданному проценту
    result = df[df["percent"] < percent]


    if result.empty:
        return f"Нет преподавателей с посещаемостью ниже {percent}%."

    msg = f"Преподаватели с посещаемостью ниже {percent}%:\n\n"
    for _, row in result.iterrows():
        msg += f"- {row['ФИО преподавателя']} — {row['percent']}%\n"

    return msg


