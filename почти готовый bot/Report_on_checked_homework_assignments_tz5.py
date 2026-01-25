# 5 тех-задание - проверенные дз
import pandas as pd

def HomeworkCheckedReport(file_path: str, period: str, percent_limit: float):
    df = pd.read_excel(file_path)

    if "ФИО преподавателя" not in df.columns:
        return "В файле нет колонки 'ФИО преподавателя'."

#убираем первую строку
    df = df.iloc[1:].copy()


    if period == "month":
        received_col = "Unnamed: 4"
        checked_col  = "Unnamed: 5"
        period_name = "за месяц"
    elif period == "week":
        received_col = "Unnamed: 9"
        checked_col  = "Unnamed: 10"
        period_name = "за неделю"
    else:
        return "Ошибка: неизвестный период."

    df["received"] = pd.to_numeric(df[received_col], errors="coerce")
    df["checked"]  = pd.to_numeric(df[checked_col], errors="coerce")

    df = df[df["received"] > 0]

    if df.empty:
        return f"Нет данных по полученному ДЗ ({period_name})."

    df["percent"] = df["checked"] / df["received"] * 100

    bad = df[df["percent"] < percent_limit]

    if bad.empty:
        return f"Нет преподавателей с проверкой ДЗ ниже {percent_limit}% ({period_name})."

    msg = f"Преподаватели с проверкой ДЗ ниже {percent_limit}% ({period_name}):\n\n"
    for _, row in bad.iterrows():
        msg += f"- {row['ФИО преподавателя']}: {int(row['checked'])} из {int(row['received'])} ({row['percent']:.1f}%)\n"

    return msg
