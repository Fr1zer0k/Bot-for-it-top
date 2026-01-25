# 3 тех-задание - средняя оценка дз и клсная работа
import pandas as pd

def StudentsReport(file_path: str) -> str:
    df = pd.read_excel(file_path)

    # Проверяем нужные колонки
    for col in ("FIO", "Homework", "Classroom"):
        if col not in df.columns:
            return f"В файле нет колонки '{col}'. Проверь, что это 'Отчет по студентам.xls'."

    result = df[(df["Homework"] == 1) & (df["Classroom"] < 3)]

    if result.empty:
        return "✅ Нет студентов с Homework = 1 и Classroom < 3."

    msg = "👥 Студенты с низкими оценками (Homework = 1 и Classroom < 3):\n\n"
    for _, row in result.iterrows():
        msg += f"- {row['FIO']}\n"

    return msg
