# 4 тех-задание - посещаемость
import pandas as pd

def StudentsAttendanceReport(file_path: str) -> str:
    df = pd.read_excel(file_path)

    if "ФИО преподавателя" not in df.columns or "Средняя посещаемость" not in df.columns:
        return "Файл не похож на 'Посещаемость по преподавателям.xlsx'."


    df = df[df["ФИО преподавателя"].notna()].copy()


    df["percent"] = (
        df["Средняя посещаемость"]
        .astype(str)
        .str.replace("%", "", regex=False)
        .str.replace(",", ".", regex=False)
    )
    df["percent"] = pd.to_numeric(df["percent"], errors="coerce")

    bad = df[df["percent"] < 40]

    if bad.empty:
        return " Нет преподавателей с посещаемостью ниже 40%."

    msg = " Преподаватели с посещаемостью ниже 40%:\n\n"
    for _, row in bad.iterrows():
        msg += f"- {row['ФИО преподавателя']} — {row['percent']}%\n"

    return msg
