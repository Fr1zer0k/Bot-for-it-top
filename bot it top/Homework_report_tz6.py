# 6 тех-задание - зданые дз
import pandas as pd

def HomeworkDoneReport(file_path: str) -> str:
    df = pd.read_excel(file_path)

    if "FIO" not in df.columns:
        return " В файле нет колонки 'FIO'. Открой файл 'Отчет по студентам'."

    if "Percentage Homework" not in df.columns:
        return " В файле нет колонки 'Percentage Homework'."

    df["Percentage Homework"] = (
        df["Percentage Homework"]
        .astype(str)
        .str.replace("%", "", regex=False)
    )

    df["Percentage Homework"] = pd.to_numeric(df["Percentage Homework"], errors="coerce")

    bad = df[df["Percentage Homework"] < 70]

    if bad.empty:
        return " Все студенты сдали больше 70% ДЗ!"

    msg = "📂 Студенты с процентом выполнения ДЗ ниже 70%:\n\n"
    for _, row in bad.iterrows():
        msg += f"- {row['FIO']} — {row['Percentage Homework']}%\n"
    return msg
