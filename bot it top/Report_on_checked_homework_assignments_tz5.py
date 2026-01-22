# 5 тех-задание - проверенные дз
import pandas as pd

def HomeworkCheckedReport(file_path: str) -> str:
    df = pd.read_excel(file_path)

    if "ФИО преподавателя" not in df.columns:
        return "В файле нет колонки 'ФИО преподавателя'."

    df = df.iloc[1:].copy()

    df["received"] = pd.to_numeric(df["Unnamed: 4"], errors="coerce")  # Получено
    df["checked"] = pd.to_numeric(df["Unnamed: 5"], errors="coerce")   # Проверено

    # оставляем только тех, у кого что-то получено
    df = df[df["received"] > 0]

    if df.empty:
        return "В файле нет данных по полученным ДЗ."

    df["percent"] = df["checked"] / df["received"] * 100

    bad = df[df["percent"] < 70]

    if bad.empty:
        return " Нет преподавателей с проверкой ДЗ ниже 70% (за месяц)."

    msg = " Преподаватели с проверкой ДЗ ниже 70% (за месяц):\n\n"
    for _, row in bad.iterrows():
        name = row["ФИО преподавателя"]
        received = int(row["received"])
        checked = int(row["checked"])
        percent = row["percent"]
        msg += f"- {name}: проверено {checked} из {received} ({percent:.1f}%)\n"

    return msg
