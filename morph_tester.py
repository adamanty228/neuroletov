import pymorphy2

# функция, чтобы тестировать pymorphy2 и не только

morph = pymorphy2.MorphAnalyzer()
print(morph.parse('любовь'))

