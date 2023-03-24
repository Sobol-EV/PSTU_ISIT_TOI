from collections import Counter
from math import copysign, fabs, floor, isfinite, modf, log, ceil
from ast import literal_eval


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
            print(f"{k} элемент - символ {i} c частотой {d[i]}")
            k += 1
        print()
    if step == 4:
        print("-----НАЙДЁМ ТОЧКИ НА ОТРЕЗКЕ ОТ 0 ДО 1-----")
        k = 1
        for i in d:
            print(f"{k} '- {d[i]}")
            k += 1
        print()
    if step == 5:
        print("-----НАЙДЁМ ОТРЕЗКИ И ДЛИНУ-----")
        for i in d:
            print(f"{i} - [{d[i][1]}: {d[i][0]}], длина: {d[i][0] - d[i][1]}")
        print()


def float_to_bin(f: float) -> str:
    """Функция преобразования вещественного числа из 10 с.ч в 2 с.ч"""
    if not isfinite(f):
        return repr(f)  # inf nan
    sign = '-' * (copysign(1.0, f) < 0)
    frac, fint = modf(fabs(f))  # split on fractional, integer parts
    n, d = frac.as_integer_ratio()  # frac = numerator / denominator
    assert d & (d - 1) == 0  # Модульный тест
    return f'{sign}{floor(fint):b}.{n:0{d.bit_length() - 1}b}'


def bin_to_float(binary):
    """Функция преобразования вещественного числа из 2 с.ч в 10 с.ч"""
    m = [list(tuple(i)) for i in binary.split(".")]
    result = 0
    for i in range(len(m)):
        if i == 0:
            for j in range(len(m[i])):
                m[i][j] = int(m[i][j]) * 2 ** (len(m[i]) - j - 1)
            result += sum(m[i])
        if i == 1:
            for j in range(len(m[i])):
                m[i][j] = int(m[i][j]) / 2 ** (j + 1)
            result += sum(m[i])
    return result


def sorted_dict(dict_original: dict) -> dict:
    """Функция сортировки словаря по ключу"""
    sort_dict = dict(sorted(dict_original.items(), key=lambda x: x[0]))
    beautiful_output(sort_dict, 3)
    return sort_dict


def new_value(lo: float, ho: float, rh: float, rl: float) -> tuple:
    """Функция расчёта границ"""
    new_low_value = lo + (ho - lo) * rl
    new_high_value = lo + (ho - lo) * rh
    print(f"СДВИНУЛИСЬ ГРАНИЦЫ [{new_low_value}:{new_high_value}]")
    return new_low_value, new_high_value


def generic_dict(line: str) -> dict:
    """Создаём словарь c вероятностями по символу"""
    final_dict = dict(Counter(line))
    beautiful_output(final_dict, 1)
    for i in final_dict.keys():
        final_dict[i] = final_dict[i] / len(line)
    beautiful_output(final_dict, 2)
    return final_dict


def create_section(d: dict) -> dict:
    """Функция для нахождения точек на отрезке от 0 до 1"""
    s = 0
    for i in d.keys():
        s += d[i]
        d[i] = s
    beautiful_output(d, 4)
    return d


def computation_result(line: str, d: dict) -> float:
    """Функция отвечающая за арифметическое кодирование"""
    lo = 0
    ho = 1
    print("-----АРИФМЕТИЧЕСКОЕ КОДИРОВАНИЕ-----")
    for i in list(line):
        lo, ho = new_value(lo, ho, d[i][0], d[i][1])
    print("G=", ho - lo)
    return (lo + ho) / 2, ho - lo


def encoding(line: str) -> tuple:
    """Функция кодирования"""
    result = generic_dict(line)
    result = sorted_dict(result)
    section = create_section(result)
    k = 0
    for i in section.keys():
        section[i] = [section[i]]
        section[i].append(k)
        k = section[i][0]
    beautiful_output(section, 5)
    result, n = computation_result(line, section)
    n = ceil(-log(n, 2) + 1)
    print(f"F+G/2={result}, ^-logG + 1^={n}")
    return float_to_bin(result)[2:n+2], section


def decoding(enc_value: float, length: int, d: dict) -> str:
    """Функция декодирования"""
    print("-----ДЕКОДИРОВАНИЕ-----")
    enc_value = bin_to_float("0." + enc_value)
    result = ""
    k = 1
    for _ in range(length):
        for i in d.keys():
            if (enc_value >= d[i][1]) and (enc_value <= d[i][0]):
                print(f"Итерация ({k}) - {enc_value} > {d[i][1]} и {enc_value} < {d[i][0]}")
                k += 1
                result += i
                enc_value = (enc_value - d[i][1]) / (d[i][0] - d[i][1])
                print("Значение:", enc_value)
                print("Расшифровано:", result)
                print("-------------------------")
                break
    return result


if __name__ == '__main__':
    print("Задание № 4 Арифметическое кодирование")
    source_line = input("Введите строку: ")
    encoding_value, dictionary = encoding(source_line)
    print("--------------------РЕЗУЛЬТАТ КОДИРОВАНИЯ--------------------")
    print("Закодированное значение: ", encoding_value, "\n")
    length_line = len(source_line)
    decoding_value = decoding(encoding_value, length_line, dictionary)
    print("--------------------РЕЗУЛЬТАТ ДЕКОДИРОВАНИЯ--------------------")
    print("Расшифрованное значение: ", decoding_value, "\n")
