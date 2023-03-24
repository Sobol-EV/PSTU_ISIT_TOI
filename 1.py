from math import copysign, fabs, floor, isfinite, modf, log, ceil
from collections import Counter


def float_to_bin(f: float) -> str:
    """Функция преобразования вещественного числа из 10 с.ч в 2 с.ч"""
    if not isfinite(f):
        return repr(f)  # inf nan
    sign = '-' * (copysign(1.0, f) < 0)
    frac, fint = modf(fabs(f))  # split on fractional, integer parts
    n, d = frac.as_integer_ratio()  # frac = numerator / denominator
    assert d & (d - 1) == 0  # Модульный тест
    return f'{sign}{floor(fint):b}.{n:0{d.bit_length() - 1}b}'


def sorted_dict(dict_original: dict) -> dict:
    """Функция сортировки словаря по значению"""
    sort_dict = {}
    sort_values = sorted(dict_original.values(), reverse=True)
    for i in sort_values:
        for j in dict_original.keys():
            if dict_original[j] == i:
                sort_dict[j] = dict_original[j]
    return sort_dict


def lx(Px: float) -> int:
    """Вычисляем Lx"""
    return ceil(-log(Px, 2))


def kod(bx: str, lx: int) -> str:
    """Вычисляем код для каждого символа"""
    if lx == 0:
        return '0'
    if bx.split(".")[1] == '0':
        return '0' * lx
    return bx.split(".")[1][:lx]


def beautiful_output(d: dict, step: int):
    """Функция для вывода результатов, 1-3, 5 шагов"""
    if step == 1:
        print("-----ПОДСЧЁТ СИМВОЛОВ-----")
        for i in d:
            print(f"Символ {i} встречается {d[i]}")
        print()
    if step == 2:
        print("-----ПОДСЧЁТ ЧАСТОТЫ ПОЯВЛЕНИЯ-----")
        for i in d:
            print(f"Символ {i} c частотой {d[i]}")
        print()
    if step == 3:
        print("-----СОРТИРОВКА ПО УБЫВАНИЮ-----")
        k = 1
        for i in d:
            print(f"{k} 'элемент - символ {i} c частотой {d[i]}")
            k += 1
        print()
    if step == 5:
        print("-----СПИСКИ С ГОТОВЫМИ ЗНАЧЕНИЯМИ ДЛЯ ПОСТРОЕНИЯ КОДА-----")
        for i in d:
            print(f"Для символа {i} список {d[i]}")
        print()


def generic_dict(line: str) -> dict:
    """Создаём словарь со всеми основными вычислениями по каждому символу"""
    final_dict = dict(Counter(line))
    beautiful_output(final_dict, 1)
    for i in final_dict.keys():
        final_dict[i] = final_dict[i] / len(line)
    beautiful_output(final_dict, 2)
    final_dict = sorted_dict(final_dict)
    beautiful_output(final_dict, 3)
    pre_sum = [0]
    j = 0
    for i in final_dict.values():
        j += i
        pre_sum.append(j)
    print("-----СПИСОК С ИНТЕРВАЛАМИ-----")
    print(pre_sum, "\n")
    j = 0
    k = 0
    for i in final_dict.keys():
        final_dict[i] = [final_dict[i]]
        final_dict[i].append(pre_sum[k])
        final_dict[i].append(float_to_bin(final_dict[i][-1]))
        final_dict[i].append(lx(final_dict[i][0]))
        final_dict[i].append(kod(final_dict[i][2], final_dict[i][-1]))
        j += 1
        k += 1
    beautiful_output(final_dict, 5)
    return final_dict


def generic_kod(line: str, dictionary: dict) -> str:
    """Преобразуем строку в шифр по словарю"""
    output_dict(dictionary)
    result = ""
    for i in line:
        result += dictionary[i][-1]
    print("--------------------РЕЗУЛЬТАТ--------------------")
    return result


def shannon_code(line: str) -> str:
    """Преобразуем строку в код методом Шеннона используя созданный словарь"""
    abc = generic_dict(line)
    cipher = generic_kod(line, abc)
    return cipher


def output_dict(d: dict):
    """Функция отображения кодов символов"""
    print("--------------------КОДЫ СИМВОЛОВ--------------------")
    for i in d.keys():
        print(f'Символ "{i}" - "{d[i][-1]}"')


if __name__ == '__main__':
    print("Задание № 1 Шифр Шеннона")
    source_line = input("Введите строку: ")
    print(shannon_code(source_line))
