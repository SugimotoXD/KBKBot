import pandas as pd
import os

def compare_excel_files(file1, file2):
    # Загрузка данных из файлов Excel
    df1 = pd.read_excel(file1)
    df2 = pd.read_excel(file2)

    # Сравнение данных
    changes = []
    for column in df2.columns[1:]:
        if not df1[column].equals(df2[column]):
            changes.append(column)

    if not changes:
        result = "Изменений нет"
    else:
        result = f"Расписание изменилось. Для групп: {', '.join(changes)}"

    return result

# Получение двух последних файлов Excel в директории
directory = 'C:/Users/Sugimoto/PycharmProjects/KBKBot/Excel'
files = os.listdir(directory)
excel_files = [file for file in files if file.endswith('.xlsx') or file.endswith('.xls')]
excel_files.sort(key=lambda x: os.path.getmtime(os.path.join(directory, x)), reverse=True)
recent_files = excel_files[:2]

def proof():
    # Проверка изменений в последних двух файлах
    if len(recent_files) == 2:
        file1 = os.path.join(directory, recent_files[0])
        file2 = os.path.join(directory, recent_files[1])
        result = compare_excel_files(file1, file2)
        return result
    else:
        return "Недостаточно файлов для сравнения"

output = proof()

# Отправка сообщения через телеграм-бот
if output == "Изменений нет":
    # Отправить сообщение "Изменений нет" через телеграм-бота
    pass
else:
    # Отправить сообщение с результатом через телеграм-бота
    pass
