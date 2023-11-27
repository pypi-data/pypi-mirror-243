'''
Дисклеймер:
    Данный модуль носит исключительно ознакомительный характер и
    не имеет цели помешать объективной оценки знаний студента.
    Прямая задача этого модуля - хранение большинства реализаций структур данных и сортировок,
    и быстрый и удобный доступ к ним.
    Всю ответственность за недобросовестное использование модуля носит исключительно сам пользователь и только ОН.

Здарова дружище, пользуйся реализациям на здоровье
За код структур данных и сортировок поблагодарим Виталия Игоревича
За то что ты сейчас видишь это сообщение благодари своего скромного слугу - Rekzi

P.S.
1) Чтобы был хороший и красивый вывод не забудь обернуть в print()
2) Удачи на сессии ;)

P.P.S.
ПОСЛЕ ПРОЧТЕНИЯ СЖЕЧЬ!!!
'''

def get_stack():
    'Возвращает реализацию стека'
    return("""
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class Stack:
    def __init__(self):
        self.head = None

    def is_empty(self):
        return self.head is None

    def push(self, item):
        new_node = Node(item)
        new_node.next = self.head
        self.head = new_node

    def pop(self):
        if self.is_empty():
            return None
        else:
            popped_item = self.head.data
            self.head = self.head.next
            return popped_item

    def peek(self):
        if self.is_empty():
            return None
        else:
            return self.head.data

    def __str__(self):
        current = self.head
        stack_str = ""
        while current:
            stack_str += str(current.data) + " → "
            current = current.next
        return stack_str.rstrip(" → ")
    """)


def get_queue():
    'Возвращает реализацию очереди'
    return("""
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class Queue:
    def __init__(self):
        self.head = None
        self.tail = None

    def is_empty(self):
        return not bool(self.head)

    def enqueue(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node

    def dequeue(self):
        data = self.head.data
        self.head = self.head.next
        if not self.head:
            self.tail = None
        return data

    def __len__(self):
        count = 0
        current = self.head
        while current:
            count += 1
            current = current.next
        return count

    def __str__(self):
        current = self.head
        queue_str = ""
        while current:
            queue_str += " → " + str(current.data)
            current = current.next
        return queue_str.lstrip(" → ")  
    """)

def get_double_linked_list():
    'Возвращает реализацию двусвязного списка'
    return("""
class Node:
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None

class DoublyLinkedList:
    def __init__(self):
        self.head = None

    def add_node(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
        else:
            current = self.head
            while current.next is not None:
                current = current.next
            current.next = new_node
            new_node.prev = current

    def delete_node(self, data):
        if self.head is None:
            return
        elif self.head.data == data:
            if self.head.next is not None:
                self.head = self.head.next
                self.head.prev = None
            else:
                self.head = None
        else:
            current = self.head
            while current.next is not None and current.next.data != data:
                current = current.next
            if current.next is None:
                return
            else:
                current.next = current.next.next
                if current.next is not None:
                    current.next.prev = current

    def __len__(self):
        count = 0
        current = self.head
        while current:
            count += 1
            current = current.next
        return count

    def __str__(self):
        if self.head == None:
            return f"Двусвязный список пустой"
        current = self.head
        dllist_str = ""
        while current:
            dllist_str += " ⇄ " + str(current.data)
            current = current.next
        return dllist_str.lstrip(" ⇄ ")   
    """)

def get_circular_doubly_linked_list():
    'Возвращает циклический двусвязный список'
    return("""
class Node:
    def __init__(self, data=None):
        self.data = data
        self.prev = None
        self.next = None

class CircularDoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def append(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
            new_node.prev = self.tail
            new_node.next = self.head
        else:
            new_node.prev = self.tail
            new_node.next = self.head
            self.tail.next = new_node
            self.head.prev = new_node
            self.tail = new_node

    def prepend(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
            new_node.prev = self.tail
            new_node.next = self.head
        else:
            new_node.prev = self.tail
            new_node.next = self.head
            self.head.prev = new_node
            self.tail.next = new_node
            self.head = new_node

    def delete(self, key):
        current_node = self.head
        while current_node:
            if current_node.data == key:
                if current_node == self.head:
                    self.head = current_node.next
                    self.tail.next = self.head
                    self.head.prev = self.tail
                elif current_node == self.tail:
                    self.tail = current_node.prev
                    self.head.prev = self.tail
                    self.tail.next = self.head
                else:
                    current_node.prev.next = current_node.next
                    current_node.next.prev = current_node.prev
                return
            current_node = current_node.next

    def __len__(self):
        count = 0
        current_node = self.head
        while current_node:
            count += 1
            current_node = current_node.next
            if current_node == self.head:
                break
        return count

    def __str__(self):
        cdllist_str = ""
        current_node = self.head
        while current_node:
            cdllist_str += str(current_node.data) + " ⇄ "
            current_node = current_node.next
            if current_node == self.head:
                break
        return " ⇄ " + cdllist_str
    """)

def get_tree():
    'Возвращает реалезацию дерева'
    return (
        """
class Node:
    def __init__(self, value):
        self.value = value
        self.children = []

class Tree:
    def __init__(self):
        self.root = None

    def add_node(self, value, parent_value=None):
        node = Node(value)
        if parent_value is None:
            if self.root is not None:
                raise ValueError("У дерева уже есть корень")
            self.root = node
        else:
            parent_node = self.find_node(parent_value)
            if parent_node is None:
                raise ValueError("Родительский узел не найден")
            parent_node.children.append(node)

    def find_node(self, value):
        return self._find_node(value, self.root)

    def _find_node(self, value, node):
        if node is None:
            return None
        if node.value == value:
            return node
        for child in node.children:
            found = self._find_node(value, child)
            if found is not None:
                return found
        return None

    def __str__(self):
        return self._str_tree(self.root)

    def _str_tree(self, node, indent=0):
        result = "  " * indent + str(node.value) + "\\n"
        for child in node.children:
            result += self._str_tree(child, indent + 2)
        return result
        """
    )

def get_binary_tree():
    'Возвращает реализацию бинарного дерева'
    print(
        """
class Node:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None        

class BinaryTree:
    def __init__(self):
        self.root = None

    def insert(self, data):
        new_node = Node(data)
        if self.root is None:
            self.root = new_node
        else:
            current = self.root
            while True:
                if data < current.data:
                    if current.left is None:
                        current.left = new_node
                        break
                    else:
                        current = current.left
                else:
                    if current.right is None:
                        current.right = new_node
                        break
                    else:
                        current = current.right

    def search(self, data):
        current = self.root
        while current is not None:
            if data == current.data:
                return True
            elif data < current.data:
                current = current.left
            else:
                current = current.right
        return False

    def delete(self, data):
        if self.root is not None:
            self.root = self._delete(data, self.root)

    def _delete(self, data, node):
        if node is None:
            return node

        if data < node.data:
            node.left = self._delete(data, node.left)
        elif data > node.data:
            node.right = self._delete(data, node.right)
        else:
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left

            temp = self._find_min_node(node.right)
            node.data = temp.data
            node.right = self._delete(temp.data, node.right)

        return node

    def _find_min_node(self, node):
        while node.left is not None:
            node = node.left
        return node

    def __str__(self):
        return '\\n'.join(self._display(self.root)[0])

    def _display(self, node):
        if node.right is None and node.left is None:
            line = str(node.data)
            width = len(line)
            height = 1
            middle = width // 2
            return [line], width, height, middle

        if node.right is None:
            lines, n, p, x = self._display(node.left)
            s = str(node.data)
            u = len(s)
            first_line = (x + 1)*' ' + (n - x - 1)*'_' + s
            second_line = x*' ' + '/' + (n - x - 1 + u)*' '
            shifted_lines = [line + u*' ' for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, n + u // 2

        if node.left is None:
            lines, n, p, x = self._display(node.right)
            s = str(node.data)
            u = len(s)
            first_line = s + x*'_' + (n - x)*' '
            second_line = (u + x)*' ' + '\\' + (n - x - 1)*' '
            shifted_lines = [u*' ' + line for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, u // 2

        left, n, p, x = self._display(node.left)
        right, m, q, y = self._display(node.right)
        s = str(node.data)
        u = len(s)
        first_line = (x + 1)*' ' + (n - x - 1)*'_' + s + y*'_' + (m - y)*' '
        second_line = x*' ' + '/' + (n - x - 1 + u + y)*' ' + '\\' + (m - y - 1)*' '
        if p < q:
            left += [n*' ']*(q - p)
        elif q < p:
            right += [m*' ']*(p - q)
        zipped_lines = zip(left, right)
        lines = [first_line, second_line] + [a + u*' ' + b for a, b in zipped_lines]
        return lines, n + m + u, max(p, q) + 2, n + u // 2
        """
    )

def get_binary_heap():
    'Возвращает реализацию двоичной кучи'
    print(
        """
import math

class BinaryHeap:
    def __init__(self):
        self.heapList = [0]
        self.currentSize = 0

    def percUp(self, i):
        while i // 2 > 0:
            if self.heapList[i] < self.heapList[i // 2]:
                tmp = self.heapList[i // 2]
                self.heapList[i // 2] = self.heapList[i]
                self.heapList[i] = tmp
            i //= 2

    def insert(self, k):
        self.heapList.append(k)
        self.currentSize = self.currentSize + 1
        self.percUp(self.currentSize)

    def percDown(self, i):
        while (i * 2) <= self.currentSize:
            mc = self.minChild(i)
            if self.heapList[i] > self.heapList[mc]:
                tmp = self.heapList[i]
                self.heapList[i] = self.heapList[mc]
                self.heapList[mc] = tmp
            i = mc

    def minChild(self, i):
        if i * 2 + 1 > self.currentSize:
            return i * 2
        else:
            if self.heapList[i*2] < self.heapList[i*2+1]:
                return i * 2
            else:
                return i * 2 + 1

    def delMin(self):
        retval = self.heapList[1]
        self.heapList[1] = self.heapList[self.currentSize]
        self.currentSize = self.currentSize - 1
        self.heapList.pop()
        self.percDown(1)
        return retval

    def buildHeap(self, alist):
        i = len(alist) // 2
        self.currentSize = len(alist)
        self.heapList = [0] + alist[:]
        while (i > 0):
            self.percDown(i)
            i -= 1

    def __str__(self):
        if not self.currentSize:
            return f'Двоичная куча пуста'
        else:
            heap_str = ""
            height = int(math.log(self.currentSize, 2)) + 1
            for i in range(0, height):
                for j in range(2**i, min(2**(i+1), self.currentSize+1)):
                    heap_str += str(self.heapList[j]) + " "
                heap_str += "\\n"
            return heap_str.strip()
        """
    )

def get_priority_queue():
    '''Возвращает реализацию класса очереди с приоритетом
    Для реализации очереди с приоритетами на основе вышеописанного класса binary_heap'''
    print(
        """
class PriorityQueue:
    def __init__(self):
        self.heap = BinaryHeap()

    def enqueue(self, item, priority):
        self.heap.insert((priority, item))

    def dequeue(self):
        return self.heap.delMin()[1]

    def __str__(self):
        return self.heap.__str__()
        """
    )

def get_hash_table_chain():
    'Возвращает реализацию хеш-таблицы методом цепочек'
    print(
        """
class HashTable:
    def __init__(self, size):
        self.size = size
        self.table = [[] for _ in range(self.size)]

    def hash_function(self, key):
        return hash(key) % self.size

    def insert(self, key, value):
        slot = self.hash_function(key)
        for pair in self.table[slot]:
            if pair[0] == key:
                pair[1] = value
                return
        self.table[slot].append([key, value])

    def find(self, key):
        slot = self.hash_function(key)
        for pair in self.table[slot]:
            if pair[0] == key:
                return pair[1]
        return None
        """
    )

def get_hash_table_open():
    'Возвращает реализацию хеш-таблицы методом открытой адресации'
    print(
        """
class HashTable:
    def __init__(self, size):
        self.size = size
        self.table = [None] * size

    def hash_function(self, key):
        return hash(key) % self.size

    def insert(self, key, value):
        index = self.hash_function(key)
        while self.table[index]:
            if self.table[index][0] == key:
                break
            index = (index + 1) % self.size
        self.table[index] = (key, value)

    def find(self, key):
        index = self.hash_function(key)
        while self.table[index]:
            if self.table[index][0] == key:
                return self.table[index][1]
            index = (index + 1) % self.size
        return None
        """
    )

def get_binary_search():
    'Возвращает реализацию бинарного поиска'
    print(
        """
def binary_search(arr, x):
    low = 0
    high = len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == x:
            return mid
        elif arr[mid] < x:
            low = mid + 1
        else:
            high = mid - 1
    return -1
        """
    )

def get_bubble_sort():
    'Возвращает реализацию сортировки пузырьком'
    print(
        """
def bubble_sort(arr, reverse=False):
    n = len(arr)
    for i in range(n):
        for j in range(n - i - 1):
            if not reverse:
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
            else:
                if arr[j] < arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr
        """
    )

def get_cocktail_sort():
    'Возвращает реализацию шейкерной сортировки'
    print(
        """
def cocktail_sort(arr, reverse=False):
    n = len(arr)
    start = 0
    end = n - 1
    swapped = True
    while swapped:
        swapped = False
        for i in range(start, end):
            if (not reverse and arr[i] > arr[i + 1]) or (reverse and arr[i] < arr[i + 1]):
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                swapped = True
        if not swapped:
            break
        swapped = False
        end = end - 1
        for i in range(end - 1, start - 1, -1):
            if (not reverse and arr[i] > arr[i + 1]) or (reverse and arr[i] < arr[i + 1]):
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                swapped = True
        start = start + 1
    return arr
        """
    )

def get_comb_sort():
    'Возвращает реализацию сортировки расческой'
    print(
        """
def comb_sort(arr, reverse=False):
    n = len(arr)
    gap = n
    shrink = 1.3
    swapped = True
    while swapped:
        gap = int(gap/shrink)
        if gap < 1:
            gap = 1
        i = 0
        swapped = False
        while i+gap < n:
            if (not reverse and arr[i] > arr[i+gap]) or (reverse and arr[i] < arr[i+gap]):
                arr[i], arr[i+gap] = arr[i+gap], arr[i]
                swapped = True
            i += 1
    return arr
        """
    )

def get_selection_sort():
    'Возвращает реализацию алгоритма сортировки выбором'
    print(
        """
ef selection_sort(arr, reverse=False):
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if reverse:
                if arr[j] > arr[min_idx]:
                    min_idx = j
            else:
                if arr[j] < arr[min_idx]:
                    min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr
        """
    )

def get_insertion_sort():
    'Возвращает реализацию алгоритма сортировки вставки'
    print(
        """
def insertion_sort(arr, reverse=False):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and ((not reverse and arr[j] > key) or (reverse and arr[j] < key)):
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr
        """
    )

def get_quick_sort():
    'Возвращает реализацию алгоритма быстрой сортировки'
    print(
        """
def quick_sort(arr, reverse=False):
    if len(arr) <= 1:
        return arr
    else:
        pivot = arr[0]
        left = []
        right = []
        for i in range(1, len(arr)):
            if arr[i] < pivot:
                left.append(arr[i])
            else:
                right.append(arr[i])
        if reverse:
            return quick_sort(right, reverse=True) + [pivot] + quick_sort(left, reverse=True)
        else:
            return quick_sort(left) + [pivot] + quick_sort(right)
        """
    )

def get_shell_sort():
    'Возвращает реализацию алгоритма сортировки Шелла'
    print(
        """
def shell_sort(arr, reverse=False):
    gap = len(arr) // 2
    while gap > 0:
        for i in range(gap, len(arr)):
            temp = arr[i]
            j = i
            while j >= gap and ((not reverse and arr[j - gap] > temp) or (reverse and arr[j - gap] < temp)):
                arr[j] = arr[j - gap]
                j -= gap
            arr[j] = temp
        gap //= 2
    return arr
        """
    )

def get_merge_sort():
    'Возвращает реализацию алгоритма сортировки слиянием'
    print(
        """
def merge_sort(arr, reverse=False):
    if len(arr) <= 1:
        return arr
    
    mid = len(arr) // 2
    left_half = arr[:mid]
    right_half = arr[mid:]
    
    left_half = merge_sort(left_half, reverse=reverse)
    right_half = merge_sort(right_half, reverse=reverse)
    
    return merge(left_half, right_half, reverse=reverse)

# вспомогательная функция для алгоритма сортировки слиянием
def merge(left_half, right_half, reverse=False):
    result = []
    i = 0
    j = 0
    
    while i < len(left_half) and j < len(right_half):
        if not reverse:
            if left_half[i] <= right_half[j]:
                result.append(left_half[i])
                i += 1
            else:
                result.append(right_half[j])
                j += 1
        elif reverse:
            if left_half[i] >= right_half[j]:
                result.append(left_half[i])
                i += 1
            else:
                result.append(right_half[j])
                j += 1
            
    result += left_half[i:]
    result += right_half[j:]
    
    return result
        """
    )

def get_sorting():
    'Возвращает пользовательский класс sorting'
    print(
        """
import time

class Sorting:

    # простая обменная сортировка
    @staticmethod
    def bubble_sort(arr, reverse=False):
        n = len(arr)
        for i in range(n):
            for j in range(n - i - 1):
                if not reverse:
                    if arr[j] > arr[j + 1]:
                        arr[j], arr[j + 1] = arr[j + 1], arr[j]
                else:
                    if arr[j] < arr[j + 1]:
                        arr[j], arr[j + 1] = arr[j + 1], arr[j]
        return arr

    # шейкерная сортировка
    @staticmethod
    def cocktail_sort(arr, reverse=False):
        n = len(arr)
        start = 0
        end = n - 1
        swapped = True
        while swapped:
            swapped = False
            for i in range(start, end):
                if (not reverse and arr[i] > arr[i + 1]) or (reverse and arr[i] < arr[i + 1]):
                    arr[i], arr[i + 1] = arr[i + 1], arr[i]
                    swapped = True
            if not swapped:
                break
            swapped = False
            end = end - 1
            for i in range(end - 1, start - 1, -1):
                if (not reverse and arr[i] > arr[i + 1]) or (reverse and arr[i] < arr[i + 1]):
                    arr[i], arr[i + 1] = arr[i + 1], arr[i]
                    swapped = True
            start = start + 1
        return arr

    # сортировка расчёской
    @staticmethod
    def comb_sort(arr, reverse=False):
        n = len(arr)
        gap = n
        shrink = 1.3
        swapped = True
        while swapped:
            gap = int(gap/shrink)
            if gap < 1:
                gap = 1
            i = 0
            swapped = False
            while i+gap < n:
                if (not reverse and arr[i] > arr[i+gap]) or (reverse and arr[i] < arr[i+gap]):
                    arr[i], arr[i+gap] = arr[i+gap], arr[i]
                    swapped = True
                i += 1
        return arr

    # сортировка выбором
    @staticmethod
    def selection_sort(arr, reverse=False):
        n = len(arr)
        for i in range(n):
            min_idx = i
            for j in range(i + 1, n):
                if reverse:
                    if arr[j] > arr[min_idx]:
                        min_idx = j
                else:
                    if arr[j] < arr[min_idx]:
                        min_idx = j
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
        return arr

    # сортировка включением
    @staticmethod
    def insertion_sort(arr, reverse=False):
        for i in range(1, len(arr)):
            key = arr[i]
            j = i - 1
            while j >= 0 and ((not reverse and arr[j] > key) or (reverse and arr[j] < key)):
                arr[j + 1] = arr[j]
                j -= 1
            arr[j + 1] = key
        return arr

    # быстрая сортировка
    @staticmethod
    def quick_sort(arr, reverse=False):
        if len(arr) <= 1:
            return arr
        else:
            pivot = arr[0]
            left = []
            right = []
            for i in range(1, len(arr)):
                if arr[i] < pivot:
                    left.append(arr[i])
                else:
                    right.append(arr[i])
            if reverse:
                return Sorting.quick_sort(right, reverse=True) + [pivot] + Sorting.quick_sort(left, reverse=True)
            else:
                return Sorting.quick_sort(left) + [pivot] + Sorting.quick_sort(right)

    # сортировка Шелла
    @staticmethod
    def shell_sort(arr, reverse=False):
        gap = len(arr) // 2
        while gap > 0:
            for i in range(gap, len(arr)):
                temp = arr[i]
                j = i
                while j >= gap and ((not reverse and arr[j - gap] > temp) or (reverse and arr[j - gap] < temp)):
                    arr[j] = arr[j - gap]
                    j -= gap
                arr[j] = temp
            gap //= 2
        return arr

    # сортировка слиянием
    @staticmethod
    def merge_sort(arr, reverse=False):
        if len(arr) <= 1:
            return arr
        
        mid = len(arr) // 2
        left_half = arr[:mid]
        right_half = arr[mid:]
        
        left_half = Sorting.merge_sort(left_half, reverse=reverse)
        right_half = Sorting.merge_sort(right_half, reverse=reverse)
        
        return Sorting.merge(left_half, right_half, reverse=reverse)

    # вспомогательная функция для сортировки слиянием
    @staticmethod
    def merge(left_half, right_half, reverse=False):
        result = []
        i = 0
        j = 0
        while i < len(left_half) and j < len(right_half):
            if not reverse:
                if left_half[i] <= right_half[j]:
                    result.append(left_half[i])
                    i += 1
                else:
                    result.append(right_half[j])
                    j += 1
            elif reverse:
                if left_half[i] >= right_half[j]:
                    result.append(left_half[i])
                    i += 1
                else:
                    result.append(right_half[j])
                    j += 1
        result += left_half[i:]
        result += right_half[j:]
        return result

    # декоратор, вычисляющий время выполнения функции и выводящий его на экран
    def measure_time(func):
        def wrapper(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            end = time.time()            
            print(f"\\nВремя выполнения {tuple(kwargs.items())[0][1]}_sort: {end - start:.6f} сек.")
            return result
        return wrapper

    @staticmethod
    @measure_time
    def sort(arr, method='bubble', reverse=False):
        if method == 'bubble':
            return Sorting.bubble_sort(arr, reverse)
        elif method == 'cocktail':
            return Sorting.cocktail_sort(arr, reverse)
        elif method == 'comb':
            return Sorting.comb_sort(arr, reverse)
        elif method == 'selection':
            return Sorting.selection_sort(arr, reverse)
        elif method == 'insertion':
            return Sorting.insertion_sort(arr, reverse)
        elif method == 'quick':
            return Sorting.quick_sort(arr, reverse)
        elif method == 'shell':
            return Sorting.shell_sort(arr, reverse)
        elif method == 'merge':
            return Sorting.merge_sort(arr, reverse)
        """
    )