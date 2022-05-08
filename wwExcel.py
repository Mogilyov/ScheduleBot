from config import days_of_week
import datetime
import xlrd


current_date = datetime.datetime.today()
year = int(current_date.strftime("%Y"))
month = int(current_date.strftime("%m"))
day = int(current_date.strftime("%u"))



def course_by_group(group):
    group_number = int(group[4])
    course = (year - group_number) % 10 + 1 * (month > 7)
    return course


def file_name(group, month_, year_):
    s = "excels/"
    s += str(course_by_group(group)) + "-kurs-"
    if month_ > 7:
        s += "osen-" + str(year_) + "_" + str(year_ + 1) + ".xls"
    else:
        s += "vesna-" + str(year_ - 1) + "_" + str(year_) + ".xls"
    return s


def para_info(group, time):


    # определяем имя файла и открываем его
    file = file_name(group, month, year)
    book = xlrd.open_workbook(file, formatting_info=True)
    sheet = book.sheet_by_index(0)

    day_rowx_down = sheet.nrows
    day_rowx_up = 0
    para_rowx = -1
    group_colx = -1
    group_rowx = -1

    # находим строку с группами
    for rowx in range(sheet.nrows):
        if sheet.cell_value(rowx, 0) == "Дни":
            group_rowx = rowx
    # находим ряд, в котором находится необходимая группа
    for colx in range(sheet.ncols):
        if sheet.cell_value(group_rowx, colx) == group:
            group_colx = colx
    # если группу не нашли, отправляем ошибку
    if group_colx == -1 or group_rowx == -1:
        return ["bad"]

    # находим нужный день недели
    for rowx in range(sheet.nrows):
        if sheet.cell_value(rowx, 0) == days_of_week[day]:
            day_rowx_up = rowx
        elif day != 6 and sheet.cell_value(rowx, 0) == days_of_week[day + 1]:
            day_rowx_down = rowx
    # находим нужное время
    for rowx in range(day_rowx_up, day_rowx_down):
        if sheet.cell_value(rowx, 1) == time:
            para_rowx = rowx

    # берём значение из ячейки
    a = sheet.cell_value(para_rowx, group_colx).split('/')

    # обновляем значение из ячейки, если ячейки были объеденины
    for cringe in sheet.merged_cells:
        y1, y2, x1, x2 = cringe
        if x1 <= group_colx < x2 and y1 <= para_rowx < y2:
            a = sheet.cell_value(y1, x1).split('/')
    return a




