from song_base import base, words
import pymorphy2

morph = pymorphy2.MorphAnalyzer()


# Файл для работы с текстом, возвращает словарь песен и словарь слов
def remove_extra(string, param='commas'):
    new_string = ''
    if param == 'commas':
        for el in string:
            if el not in ',.?!:;':
                new_string += el
            else:
                new_string += ' '
    if param == 'apostrophe':
        for el in string:
            if el != '\'':
                new_string += el
    return new_string


while True:
    print('Введите название:')
    name = input()
    if name == '1':
        break
    text_list = []
    print('А теперь текст:')
    while True:
        line = input()
        if line == '1':
            break
        else:
            text_list.append(line)

    line = remove_extra(line)
    for line in text_list:
        line_list = line.split()
        for word in line_list:
            result = morph.parse(word)
            first_check = result[0][1].POS
            if first_check:
                if first_check not in 'PREP_CONJ_PRCL_INTJ':
                    biggest = result[0].score
                    for desc in result:
                        if desc.score + 0.00001 < biggest:
                            break
                        res = desc[1]
                        pos = res.POS
                        normal = desc.normal_form
                        if pos in words.keys():
                            if pos == 'ADJF' or pos == 'ADJS':
                                if normal not in words['ADJF']:
                                    words['ADJF'].append(normal)
                                if normal not in words['ADJS']:
                                    words['ADJS'].append(normal)
                            elif pos == 'PRTF' or pos == 'PRTS' or pos == 'VERB' or pos == 'GRND':
                                if normal not in words['PRTF']:
                                    words['PRTF'].append(normal)
                                if normal not in words['PRTS']:
                                    words['PRTS'].append(normal)
                                if normal not in words['VERB']:
                                    words['VERB'].append(normal)
                                if normal not in words['GRND']:
                                    words['GRND'].append(normal)
                            else:
                                if normal not in words[pos]:
                                    words[pos].append(normal)
    base[name] = text_list

for el in words:
    words[el] = sorted(words[el])

print(f"base = {base}\n"
      f"words = {words}")
