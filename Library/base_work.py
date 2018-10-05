# -*- coding: utf-8 -*-
"""
Модуль, содержащий функции для работы с базой данных
"""


def search(query: list, base: dict):
    """
    Входные данные: список критериев в следующем порядке [Country, (Population, Знак), (Area, Знак), Capital, Language,
    Currency], где Знак - >, >=, <, <=, =, Интервал; словарь - база данных
    Выходные данные: список ключей для словаря, содержащий подходящие записи (может быть пустым)
    Данная функция, выполняя поиск по каждому критерию из списка, составляет список подходящих элементов для вывода в
    окне поиска
    """
    keys = []
    for e in base:
        if query[0].lower() in e.lower():
            if query[1][0] == '=':
                if base[e]['Population'] != int(query[1][1]):
                    continue  # здесь и далее continue выполняется при несоответствии хотя бы одного из условий
            elif query[1][0] == '>':
                if base[e]['Population'] <= int(query[1][1]):
                    continue
            elif query[1][0] == '>=':
                if base[e]['Population'] < int(query[1][1]):
                    continue
            elif query[1][0] == '<':
                if base[e]['Population'] >= int(query[1][1]):
                    continue
            elif query[1][0] == '<=':
                if base[e]['Population'] > int(query[1][1]):
                    continue
            elif query[1][0] == 'Интервал':
                minimum, maximum = query[1][1].split()
                if not (minimum <= base[e]['Population'] <= maximum):
                    continue

            if query[2][0] == '=':
                if base[e]['Area'] != int(query[2][1]):
                    continue  # здесь и далее continue выполняется при несоответствии хотя бы одного из условий
            elif query[2][0] == '>':
                if base[e]['Area'] <= int(query[2][1]):
                    continue
            elif query[2][0] == '>=':
                if base[e]['Area'] < int(query[2][1]):
                    continue
            elif query[2][0] == '<':
                if base[e]['Area'] >= int(query[2][1]):
                    continue
            elif query[2][0] == '<=':
                if base[e]['Area'] > int(query[2][1]):
                    continue
            elif query[2][0] == 'Интервал':
                minimum, maximum = query[2][1].split()
                if not (minimum <= base[e]['Area'] <= maximum):
                    continue

            if query[3].lower() not in base[e]['Capital'].lower():
                continue
            if query[4].lower() not in base[e]['Language'].lower():
                continue
            if query[5].lower() not in base[e]['Currency'].lower():
                continue

            keys.append(e)

    return keys


def local_copy(base):
    """
    Входные данные: объект базы данных
    Выходные данные: локальная копия базы данных для редактирования
    Получает считанную с диска базу данных, создает и возвращает копию
    """
    dic = {}
    for key in base:
        dic[key] = base[key]
    return dic


def save_copy(copy, base):
    """
    Входные данные: локальная копия бд, объект, в который будет записана бд и сохранена на диск
    Выходные данные: пересохраненный объект, содержащий бд
    Сохраняет локальную копию в объект БД для сохранения на диске
    """
    base.clear()
    for key in copy:
        base[key] = copy[key]
    return base


def total(keys: list, base: dict):
    """
    Входные данные: список ключей, база данных
    Выходные данные: текст отчета
    Функция получает на вход список ключей, по которым надо составить отчет, и базу данных. Высчитывает количество
    записей, средние значения и выборочные дисперсии
    """
    total_count = len(keys)
    avg_popul = 0
    avg_area = 0
    mean_popul = 0
    mean_area = 0
    count_list = ''
    for k in keys:
        cname, popul, area, capital = k, base[k]['Population'], base[k]['Area'], base[k]['Capital']
        lang, cur = base[k]['Language'], base[k]['Currency']
        count_list += '{};{};{};{};{};{}\n'.format(cname, popul, area, capital, lang, cur)
        avg_popul += int(popul)
        avg_area += int(area)
        mean_popul += int(popul) ** 2
        mean_area += int(area) ** 2
    avg_popul /= total_count
    avg_area /= total_count
    mean_popul /= total_count
    mean_area /= total_count
    disp_popul = mean_popul - avg_popul ** 2
    disp_area = mean_area - avg_area ** 2
    text = 'Всего стран: {}\nСреднее население: {}\nВыборочная дисперсия населения: {}\nСредняя площадь: {}\n' \
           'Выборочная дисперсия площади: {}' \
           '\nСтрана;Население;Площадь;Столица;Язык;Валюта\n{}'.format(total_count, avg_popul, disp_popul, avg_area,
                                                                       disp_area, count_list)
    return text
