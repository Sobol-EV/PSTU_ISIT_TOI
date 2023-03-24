from collections import Counter


class Node(object):
    """Класс узла"""
    def __init__(self, name=None, value=None):
        self.name = name
        self.value = value
        self.lchild = None
        self.rchild = None


class HuffmanTree(object):
    """Класс создающий дерево и словарь с значениями кодов"""
    def __init__(self, char_weights):
        """Конструктор класса создающий дерево от корня вверх"""
        def out_leaf(l: list, step: int):
            """Функция вывода созданных узлов"""
            if step == 1:
                print("-----СОЗДАНИЕ УЗЛОВ-----")
            if step == 2:
                print("-----ОТСОРТИРУЕМ УЗЛЫ ПО УБЫВАНИЮ-----")
            if step == 3:
                print("-----УБЕРАЕМ 2 УБИРАЕМ ДВА УЗЛА С НАИМЕНЬШЕЙ СУММОЙ-----")
                print("         ДОБАВЛЯЕМ НОВЫЙ УЗЕЛ С ДВУМЯ РОДИТЕЛЯМИ")
            for _ in l:
                print("Узел: ", _.name)
                print("Значение: ", _.value)
                print("Родитель слева: ", _.lchild)
                print("Родитель справа: ", _.rchild)
                print("-----------------------")
        self.Leaf = [Node(k, v) for k, v in char_weights.items()]
        out_leaf(self.Leaf, 1)
        while len(self.Leaf) != 1:
            self.Leaf.sort(key=lambda node: node.value, reverse=True)
            out_leaf(self.Leaf, 2)
            n = Node(value=(self.Leaf[-1].value + self.Leaf[-2].value))
            n.lchild = self.Leaf.pop(-1)
            n.rchild = self.Leaf.pop(-1)
            self.Leaf.append(n)
            out_leaf(self.Leaf, 3)

        self.root = self.Leaf[0]
        self.Buffer = list(range(10))
        self.final_dict = {}

    def hu_generate(self, tree, length):
        """Функция рекурсивно проходит по узлам и создает коды символов, сохраняет их в словарь"""
        node = tree
        if not node:  # Если нет узла, завершаем рекурсию
            return
        elif node.name:  # Ecли дошли до основания, записываем код узла
            kod = ""
            for i in range(length):
                kod += str(self.Buffer[i])
            self.final_dict[node.name] = kod
            return
        self.Buffer[length] = 1
        self.hu_generate(node.lchild, length + 1)
        self.Buffer[length] = 0
        self.hu_generate(node.rchild, length + 1)

    def get_code(self):
        """Вспомогательная функция для генерации словаря с кодами"""
        self.hu_generate(self.root, 0)


def output_dict(d: dict):
    """Функция отображения кодов символов"""
    print("--------------------КОДЫ СИМВОЛОВ--------------------")
    for i in d.keys():
        print(f'Символ "{i}" - "{d[i]}"')
    print()


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


if __name__ == '__main__':
    print("Задание № 3 Код Хаффмана")
    source_line = input("Введите строку: ")
    final_dict = dict(Counter(source_line))
    beautiful_output(final_dict, 1)
    for i in final_dict.keys():
        final_dict[i] = final_dict[i] / len(source_line)
    beautiful_output(final_dict, 2)
    tree = HuffmanTree(final_dict)
    tree.get_code()
    output_dict(tree.final_dict)
    result = ""
    for i in source_line:
        result += tree.final_dict[i]
    print("--------------------РЕЗУЛЬТАТ--------------------")
    print(result)


