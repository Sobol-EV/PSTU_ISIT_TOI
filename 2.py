from math import copysign, fabs, floor, isfinite, modf, log, ceil
from collections import Counter


def li(Pi: float) -> int:
    """Высчитываем Li - количество разрядов после запятой"""
    return ceil(-log(Pi/2, 2))


def float_to_bin(f: float) -> str:
    """Функция преобразования вещественного числа из 10 с.ч в 2 с.ч"""
    if not isfinite(f):
        return repr(f)  # inf nan
    sign = '-' * (copysign(1.0, f) < 0)
    frac, fint = modf(fabs(f))  # split on fractional, integer parts
    n, d = frac.as_integer_ratio()  # frac = numerator / denominator
    assert d & (d - 1) == 0  # Модульный тест
    return f'{sign}{floor(fint):b}.{n:0{d.bit_length() - 1}b}'


def kod(Qi: str, L: int) -> str:
    """Определяем код буквы"""
    return Qi.split(".")[1][:L]


def beautiful_output(d: dict, step: int):
    """Функция для вывода результатов, 1-2, 4 шагов"""
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
    if step == 4:
        print("-----СПИСКИ С ГОТОВЫМИ ЗНАЧЕНИЯМИ ДЛЯ ПОСТРОЕНИЯ КОДА-----")
        for i in d:
            print(f"Для символа {i} список {d[i]}")
        print()


def generic_dict(line: str) -> dict:
    """Создаём словарь со всеми основными вычислениями"""
    final_dict = dict(Counter(line))
    beautiful_output(final_dict, 1)
    k = 0
    for i in final_dict.keys():
        if k == 0:
            index_0 = i
        final_dict[i] = final_dict[i] / len(line)
        k += 1
    beautiful_output(final_dict, 2)
    qi = 0
    pre_sum = [final_dict[index_0]/2]
    prev_pi = 0
    for pi in final_dict.values():
        if prev_pi != 0:
            qi += prev_pi
            pre_sum.append(qi + pi / 2)
        prev_pi = pi
    print("-----СПИСОК С ИНТЕРВАЛАМИ-----")
    print(pre_sum, "\n")
    k = 0
    for i in final_dict.keys():
        final_dict[i] = [final_dict[i]]
        final_dict[i].append(pre_sum[k])
        final_dict[i].append(li(final_dict[i][0]))
        final_dict[i].append(float_to_bin(final_dict[i][1]))
        final_dict[i].append(kod(final_dict[i][-1], final_dict[i][-2]))
        k += 1
    beautiful_output(final_dict, 4)
    return final_dict


def gilbert_mur(line: str) -> str:
    """Преобразуем строку в код методом Гилберта-Мура используя созданный словарь"""
    abc = generic_dict(line)
    output_dict(abc)
    result = ""
    for i in line:
        result += abc[i][-1]
    print("--------------------РЕЗУЛЬТАТ--------------------")
    return result


def output_dict(d: dict):
    """Функция отображения кодов символов"""
    print("--------------------КОДЫ СИМВОЛОВ--------------------")
    for i in d.keys():
        print(f'Символ "{i}" - "{d[i][-1]}"')
    print()


if __name__ == '__main__':
    print("Задание № 2 Шифр Гилберта-Мура")
    Source_line = input("Введите строку:")
    print(gilbert_mur(Source_line))