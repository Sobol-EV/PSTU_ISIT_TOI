
def quick_sort(k: list, l=None, r=None):
    if l is None:  # Q1.1
        l = 0
    if r is None:  # Q1.2
        r = len(k) - 1
    if l >= r:
        # simple_inserts(k)  # Q9
        return None
    j = hoare_split(k, l, r)  # Q2
    quick_sort(k, l, j-1)  # Q7.1
    quick_sort(k, j+1, r)  # Q7.2


def hoare_split(k: list, l: int, r: int) -> int:
    print(f"               {k}  (l={l + 1}, r={r + 1}) ")
    k_current = k[l]
    i = l + 1
    j = r
    while True:
        while i < r and k[i] < k_current:  # Q3
            i += 1
        while k[j] > k_current:  # Q4
            j -= 1
        if i >= j:  # Q5
            break
        k[i], k[j] = k[j], k[i]  # Q6
        i += 1
        j -= 1
    k[l], k[j] = k[j], k[l]
    return j  # Q8


def simple_inserts(k: list) -> list:
    """Сортировка методом простых вставок"""
    for i in range(len(k) - 1):
        j = i - 1
        key = k[i]
        while k[j] > key and j >= 0:
            k[j + 1] = k[j]
            j -= 1
        k[j + 1] = key
    return k


if __name__ == '__main__':
    print('Задание № 7 - ВАРИАНТ 7 "Быстрая сортировка Хоара"')
    m = [999, 44, 32, 61, 755, 66, 910, 111, 15, 77, 154, 519, 312, 164, 5, 7, 300]
    print(f"До сортировки: {m}")
    print("-----------------------------------------------------------------------------------------------")
    quick_sort(m)
    print("-----------------------------------------------------------------------------------------------")
    print(f"> РЕЗУЛЬТАТ РАБОТЫ СОРТИРОВКИ: {m}")
