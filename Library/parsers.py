def validate_interval_entry(text):
    """
    Входные данные: строка текста, которую необходимо проверить
    Выходные данные: True - если строка соотвествует условию, иначе False
    Проверяет, состоит ли строка из двух натуральных чисел, разделенных пробеломб при чем первое число меньше второго
    Пустая строка допустима
    """
    if text == '':
        return True
    elems = text.split()
    if len(elems) != 2:  # проверка, что чисел ровно два
        return False
    try:  # попытка преобразовать строки в числа. в случае exception - введено не число
        n1, n2 = map(int, text.split())
        f1, f2 = map(float, text.split())
        if f1 != n1 or f2 != n2:  # проверка, что число целое
            return False
        if (n1 < 0 or n2 < 0) or (n1 >= n2):  # проверка, что первое число меньше второго
            return False
    except ValueError:
        return False
    return True


def validate_singlenum_entry(text):
    """
    Входные данные: строка текста, которую необходимо проверить
    Выходные данные: True - если строка соотвествует условию, иначе False
    Проверяет, состоит ли строка из натурального числа. Пустая строка допустима
    """
    if text == '':
        return True
    try:
        n = int(text)
        if n <= 0:
            return False
    except ValueError:
        return False
    return True
