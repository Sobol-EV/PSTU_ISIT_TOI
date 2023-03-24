from math import log2


def add_check_zero(line: str) -> str:
    """Функция добавляет контрольные биты"""
    for i in range(int(log2(len(line)))+1):
        line = line[:2 ** i - 1] + "0" + line[2 ** i - 1:]
    return line


def create_line(length: int, k: int) -> str:
    """Функция создаёт строку, начиная с n значения, чередует X и O по n раз"""
    s = ""
    flag = 0
    for i in range(k-1):
        s += "O"
    while len(s) < length:
        for i in range(k):
            if len(s) < length:
                if flag % 2 == 0:
                    s += "X"
                else:
                    s += "O"
            else:
                break
        flag += 1
    return s


def create_matrix(m: list) -> list:
    """Функция создаёт список из строк, который будет использоваться как матрица"""
    for i in range(int(log2(len(m[0])))+1):
        m.append(create_line(len(m[0]), 2**i))
    return m


def output_matrix(m: list):
    """Вспомогательная функция для вывода матрицы"""
    for i in m:
        print(i)
    print()


def check_value_control(matrix: list) -> str:
    """Функция сравнивает значения в матрице и проставляет контрольные биты"""
    sum_one = {}
    for i in range(int(log2(len(matrix[0])))+1):
        sum_one[2**i] = 0
    for i in range(1, len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == "X" and matrix[0][j] == "1":
                sum_one[2**(i-1)] = sum_one[2**(i-1)] + 1
    for i in sum_one.keys():
        if sum_one[i] % 2 == 1:
            matrix[0] = matrix[0][:i-1] + "1" + matrix[0][i:]
    print("-----ПРОСТАВИМ КОНТРОЛЬНЫЕ БИТЫ>-----")
    print("|| |   |       |")
    print(matrix[0], "\n")
    return matrix[0]


def add_insign_zeros(line: str) -> str:
    """Функция дополняет хначения незначимыми контрольными битами 0, до размера 16 бит- 1 символ"""
    while len(line) < 16:
        line = "0" + line
    return line


def encoding(line: str) -> str:
    """Основная функция для кодирования методом Хэмминга"""
    print("-----КОДИРОВАНИЕ-----\n")
    print("ПЕРЕВЕДЁМ СИМВОЛЫ В ACSII КОДЫ, КОДЫ ПЕРЕВЕДЁМ В ДВОИЧНУЮ СИСТЕМУ")
    print("ДВОИЧНУЮ ЗАПИСЬ ДОПОЛНИМ НЕЗНАЧАЩИМИ НУЛЯМИ до 16-БИТ")
    line = list(map(lambda x: add_insign_zeros("0" + bin(ord(x)).split("b")[1]), list(line)))
    print("СПИСОК СО ЗНАЧЕНИЯМИ: ", line, "\n")
    final_encoding = ""
    for i in range(len(line)):
        bit_16 = line[i]
        bit_16 = [add_check_zero(bit_16)]
        print(f"-({i + 1})-ДОБАВИМ КОНТРОЛЬНЫЕ БИТЫ-----")
        print("|| |   |       |")
        print(bit_16[0], "\n")
        mtx_16bit = create_matrix(bit_16)
        print("-----СОЗДАДИМ МАТРИЦУ-----")
        output_matrix(mtx_16bit)
        print()
        final_encoding += check_value_control(mtx_16bit)
    return final_encoding


def replace_with_null(line: str) -> str:
    """Функция обнуляет контрольные биты"""
    for i in range(int(log2(len(line)))+1):
        line = line[:2**i - 1] + "0" + line[2**i:]
    return line


def delete_control_value(line: str) -> str:
    """Функция удаляет контрольные биты"""
    for i in range(int(log2(len(line)))+1):
        line = line[:2**i - (i + 1)] + line[2**i - i:]
    return line


def comparison_control_bits(line1: str, line2: str, i_help: int) -> bool:
    """Функция сравнивает контрольные биты в строках"""
    flag = True
    i_err = None
    m_2i = []
    for i in range(int(log2(len(line1)))+1):
        m_2i.append(i)
        if line1[2**i-1] != line2[2**i-1]:
            flag = False
    print("-----СРАВНИМ КОНТРОЛЬНЫЕ БИТЫ-----")
    print(line1)
    print("|| |   |       |")
    print(line2)
    for i in range(len(line2)):
        flg1 = 0
        for j in m_2i:
            if 2**j == (i+1):
                flg1 = 1
        if (flg1 == 0) and (line1[i] != line2[i]):
            print("------------------> НЕКОРРЕКТНЫЙ БИТ: ", i_help*21 + (i+1))
    print("ИТОГ: ", flag, "\n")
    return flag


def decoding(new_line: str) -> str:
    """Основная функция декодирования методом Хэмминга, также позволяет исправить одну ошибку на 16 бит информации"""
    print("-----ДЕКОДИРОВАНИЕ-----")
    count_16bit = len(new_line) // 21
    print("Количество символов для декодирования: ", count_16bit)
    border = 0
    final_decoding = ""
    for i in range(count_16bit):
        line = new_line[border:border + 21]
        print(f"-({i + 1})-СИМВОЛ-----")
        print(line, "\n")
        border += 21
        original_line = replace_with_null(line)
        print(f"ОБНУЛЯЕМ КОНТРОЛЬНЫЕ БИТЫ")
        print(original_line, "\n")
        matrix = create_matrix([original_line])
        print(f"-----СОЗДАЁМ МАТРИЦУ-----")
        output_matrix(matrix)
        original_line = check_value_control(matrix)
        i_old = i
        if comparison_control_bits(line, original_line, i):
            original_line = delete_control_value(original_line)
            print("-----УДАЛЯЕМ КОНТРОЛЬНЫЕ ЗНАЧЕНИЯ-----")
            print(original_line, "\n")
            final_decoding += chr(int(original_line, 2))
            print("-----РАСШИФРОВАННАЯ ЧАСТЬ-----")
            print(final_decoding, "\n")
        else:
            sum_err = 0
            print("------ОБНАРУЖЕНА ОШИБКА-----")
            for i in range(int(log2(len(original_line)))+1):
                print(f"{original_line[2 ** i - 1]} != {line[2 ** i - 1]}")
                if original_line[2 ** i - 1] != line[2 ** i - 1]:
                    sum_err += 2 ** i
            repl = "1" if original_line[sum_err - 1] == "0" else "0"
            original_line = original_line[:sum_err - 1] + repl + original_line[sum_err:]
            original_line = replace_with_null(original_line)
            matrix = create_matrix([original_line])
            original_line = check_value_control(matrix)
            if comparison_control_bits(line, original_line, i_old):
                original_line = delete_control_value(original_line)
                final_decoding += chr(int(original_line, 2))
            else:
                print(original_line)
                print("Восстановить данные не удалось, больше 2 ошибок на 16 бит информации")
                exit()
    return final_decoding


if __name__ == '__main__':
    print("Задание № 5 Код Хэмминга")
    source_line = input("Введите строку:")
    encoding_value = encoding(source_line)
    print("--------------------РЕЗУЛЬТАТ--------------------")
    print("Закодированное значение: ", encoding_value, "\n")
    decoding_value = decoding("110000010000010101110100000000000011001111010000010001001100001")
    print("--------------------РЕЗУЛЬТАТ--------------------")
    print("Расшифрованное значение: ", decoding_value, "\n")















