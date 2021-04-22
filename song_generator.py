import pymorphy2
from russtress import Accent
from random import shuffle
from song_base import base, words
from stress_exceptions import exceptions, exceptions_not_normal
from stresses_base import sb
own = False


class PAR(pymorphy2.MorphAnalyzer):
    # класс на основе pymorphy2.MorphAnalyzer, исправляющий некоторые ошибки оригинала
    def __init__(self):
        super().__init__()

    def parse(self, word):
        if word in ['поляне', 'солдат'] and s_name == 'Невыносимая лёгкость бытия':
            return [super().parse(word)[1]]
        if word in ['молот', 'плесень'] and s_name == 'Всё идёт по плану':
            return [super().parse(word)[1]]
        if word == 'голоса' and s_name == 'На заре':
            return [super().parse(word)[1]]
        if word == 'глаза' and s_name == 'Моя оборона':
            return [super().parse(word)[2]]
        if word == 'капель' and s_name == 'Победа':
            return [super().parse(word)[1]]
        if word == 'постою' and s_name == 'Исповедь':
            return [super().parse(word)[1]]
        if word == 'поле' and s_name == 'Русское поле экспериментов':
            return [super().parse(word)[1]]
        if word == 'имени' and s_name == 'Звезда по имени солнце':
            return [super().parse(word)[1]]
        if word == 'шинель' and s_name == 'Бери шинель':
            return [super().parse(word)[1]]
        if word == 'дурачка' and s_name == 'Про дурачка':
            return [super().parse(word)[1]]
        if word == 'исповедь' and s_name == 'Исповедь':
            return [super().parse(word)[1]]
        if word == 'любовь' and s_name == 'Наташа':
            return [super().parse(word)[1]]
        if word == 'верша':
            return [super().parse(word)[1]]
        if word == 'мишутка':
            return [super().parse('мужчина')[0]]
        return super().parse(word)


local_dict = {}
m = PAR()
accent = Accent()
s_name = ''
rhyme = False


def mega_split(used, mark):
    # сплитит строку и отделяет знаки препинания от слов
    if mark in used:
        used_list = used.split(mark)
        used_list = [mark if x == '' else x for x in used_list]
        return used_list
    return used


def remove_consonants(wr):
    # убирает согласные из слова
    dr = ''
    for el in wr:
        if el in 'АЯОЁУЮЫИЭЕаяоёуюыиэе' or el == '\'':
            dr += el
    return dr


def stress(form):
    # возвращает ударный слог в слове
    word = form.word
    if word.lower() in exceptions_not_normal:
        return exceptions_not_normal[word.lower()]
    elif form.normal_form.lower() in exceptions:
        return exceptions[form.normal_form.lower()]
    elif word in sb:
        return sb[word]
    accented_word = accent.put_stress(word)
    if '\'' not in accented_word:
        return 1

    dr = remove_consonants(accented_word)
    sb[word] = dr.index('\'')
    return dr.index('\'')


def count_vowels(word):
    # просто считает гласные
    return len(remove_consonants(word))


def check_rhyme(w1, w2):
    # проверяет, рифмуются ли слова
    s1 = stress(m.parse(w1)[0])
    s2 = stress(m.parse(w2)[0])
    if count_vowels(w1) - s1 == count_vowels(w2) - s2:
        f1 = 'АОУЫЭаоуыэЯЁЮИЕяёюие'
        f2 = 'ЯЁЮИЕяёюиеАОУЫЭаоуыэ'
        son = 'бвгджзйлмнр'
        dul = 'кпстфхцчшщ'
        d1 = remove_consonants(w1)
        d2 = remove_consonants(w2)
        if d1[s1 - 1] == d2[s2 - 1] or f1.index(d1[s1 - 1]) == f2.index(d2[s2 - 1]):
            if w1[-1] == 'ь':
                w1 = w1[:-1]
            if w2[-1] == 'ь':
                w2 = w2[:-1]
            if w1[-1] not in f1 and w2[-1] not in f2:
                if w1[-1] in 'лрмнй' and w2[-1] not in 'лрмнй' or w2[-1] in 'лрмнй' and w1[-1] not in 'лрмнй':
                    return False
                else:
                    w1 = w1[:-1]
                    w2 = w2[:-1]
            else:
                if w1[-1] not in f1:
                    w1 = w1[:-1]
                if w2[-1] not in f2:
                    w2 = w2[:-1]
            counter = 0
            s3 = 0
            for i in range(len(w1)):
                if w1[i] in f1:
                    counter += 1
                    if counter == s1:
                        s3 = i
                        break
            s4 = 0
            for i in range(len(w2)):
                if w2[i] in f2:
                    counter += 1
                    if counter == s1:
                        s4 = i
                        break

            w1 = w1[s3:]
            w2 = w2[s4:]
            for el in f1:
                w1 = w1.replace(el, '$')
                w2 = w2.replace(el, '$')
            w1l = w1.split('$')
            w2l = w2.split('$')
            for i in range(len(w1l)):
                if w1l[i] and w2l[i]:
                    if w1l[i][-1] in son and w2l[i][-1] in dul or w2l[i][-1] in son and w1l[i][-1] in dul:
                        return False
            return True
    return False


def search(word, rh=False):
    # ищет похожие слова
    global local_dict
    word = word.lower()
    res = m.parse(word)
    if len(res) > 0:
        chosen = None
        for el in res:
            if 'Apro' in el.tag:
                return word
        if not chosen:
            chosen = res[0]
    else:
        chosen = res[0]
    check = (count_vowels(chosen[0]), stress(chosen))
    pos = chosen.tag.POS
    if pos not in words.keys():
        return word
    else:
        s_list = words[pos]
        shuffle(s_list)
        for el in s_list:
            ask = m.parse(el)
            one = None
            for one in ask:
                if one.tag.POS == pos:
                    break
            if pos == 'NOUN' and chosen.tag.number == 'sing':
                if chosen.tag.gender != one.tag.gender or chosen.tag.number != one.tag.number:
                    continue
            if pos == 'VERB' and chosen.tag.transitivity != one.tag.transitivity:
                continue
            two = None
            for form in one.lexeme:
                if form.tag == chosen.tag:
                    two = form
                    break
            if not two:
                continue
            if two[0] in ['рте', 'льде']:
                two = m.parse(two[0][:-1] + 'у')[0]
            if count_vowels(two[0]) == check[0] and two[0].lower() != chosen[0].lower() and \
                    two[0].lower() not in local_dict.values():
                if stress(two) == check[1]:
                    if chosen.tag.POS == 'NOUN' and chosen[0][-1] != two[0][-1] and chosen[0][-1] \
                            in 'ье' and chosen.tag.case in 'accs_loct':
                        continue
                    if rh:
                        if not check_rhyme(chosen[0], two[0]):
                            continue
                    return two[0]
        return word


def generate(song_name):
    # функция, генерирующая песню на основе другой
    global s_name
    global rhyme
    s_name = song_name
    global local_dict
    answer = []
    song = base[song_name].copy()
    song.append(song_name)
    for line in song:
        if line == '':
            answer.append('\n')
        else:
            line_list = line.split()
            for i in range(len(line_list)):
                rhyme_last = False
                if i == len(line_list) - 1 and rhyme:
                    rhyme_last = True
                line_list[i] = mega_split(line_list[i], '.')
                line_list[i] = mega_split(line_list[i], ',')
                line_list[i] = mega_split(line_list[i], '!')
                line_list[i] = mega_split(line_list[i], '?')
                line_list[i] = mega_split(line_list[i], ':')
                line_list[i] = mega_split(line_list[i], ';')
                if isinstance(line_list[i], list):
                    word = line_list[i][0]
                    if word[0].isupper():
                        cap = True
                    else:
                        cap = False
                    if word.lower() in local_dict.keys():
                        line_list[i][0] = local_dict[line_list[i][0].lower()]
                        if cap:
                            line_list[i][0] = line_list[i][0].capitalize()
                        line_list[i] = ''.join(line_list[i])
                    else:
                        if cap:
                            n_word = search(word, rh=rhyme_last).capitalize()
                        else:
                            n_word = search(word, rh=rhyme_last)
                        local_dict[line_list[i][0].lower()] = n_word.lower()
                        line_list[i][0] = n_word
                        line_list[i] = ''.join(line_list[i])
                else:
                    word = line_list[i]
                    if word[0].isupper():
                        cap = True
                    else:
                        cap = False
                    if word.lower() in local_dict.keys():
                        line_list[i] = local_dict[line_list[i].lower()]
                        if cap:
                            line_list[i] = line_list[i].capitalize()
                    else:
                        if cap:
                            n_word = search(word, rh=rhyme_last).capitalize()
                        else:
                            n_word = search(word, rh=rhyme_last)
                        local_dict[line_list[i].lower()] = n_word.lower()
                        line_list[i] = n_word

            b = ' '.join(line_list)

            answer.append(b)
    answer = [answer[-1]] + answer[:-1]
    answer[0] = answer[0] + '\n'
    local_dict = {}
    ans_str = '\n'.join(answer)
    ans_str = correct(ans_str)
    return ans_str


def manipulate(request):
    # Функция для взаимодействия с пользователем
    global own
    global rhyme
    if own:
        own = False
        custom = request.split('\n')
        custom_name = custom[0]
        custom = custom[1:]
        base[custom_name] = custom
        answer = generate(custom_name)
        del base[custom_name]
        return answer
    rhyme = False
    request = request.capitalize()
    rsl = request.split()
    if rsl[0].lower() in ['р', 'рифма']:
        rhyme = True
        request = ' '.join(rsl[1:]).capitalize()
    if request in ['Пой революция', 'Пой, революция']:
        request = 'Пой, революция!'

    if request in base.keys():
        return generate(request)

    if request.lower() in ['помощь', 'инструкция', 'п', 'и']:
        return '- введите название песни для генерации\n- введите "список" или "список песен",' \
               ' чтобы получить список песен\n' \
               '- букву слово "рифма" перед названием песни\n' \
               'Функция рифмы еще мало изучена, ' \
               'потому что от нее получали больше ошибок, чем информации\n' \
               '- Слово "оригинал" или "ориг" перед названием песни, чтобы получить оригинал песни\n' \
               '- "Свой" или "свой текст", чтобы сгенерировать бред на основе своего текста'
    if request.lower() in ['свой', 'свой текст', 'своя', 'своя песня']:
        own = True
        return 'Введите текст своей песни, и я сгенерирую бред. Названием будет первая строчка. ' \
               'Непроверенный текст, скорее всего, сгенерируется с большим количеством ошибок.'
    if request.lower() in ['с', 'список', 'список песен']:
        lll = sorted(list(base.keys()))
        return '- ' + '\n- '.join(lll)
    if rsl[0].lower() in ['о', 'оригинал', 'ориг']:
        request = ' '.join(rsl[1:]).capitalize()
        if request in base.keys():
            answer_list = [request, '']
            for el in base[request]:
                answer_list.append(el)
            answer = '\n'.join(answer_list)
            return correct(answer)
        return 'Такой песни у нас нет. Проверьте, не заменили ли вы "ё" на "е"?'
    request = request.lower()
    for el in ['привет', 'прив', 'здравстуй', 'хай']:
        if el in request:
            return 'И тебе привет!'
    return 'Такой песни у нас нет. Проверьте, не заменили ли вы "ё" на "е"?'


def correct(text):
    # Корректор и цензор одновременно
    ws_list = {'проливный': 'проливной', 'хмельный': 'хмельной', 'жоп': 'ж**', 'говн': 'г***', 'мужчина': 'мишутка'}
    for el in ws_list:
        text = text.replace(el, ws_list[el])
        text = text.replace(el.capitalize(), ws_list[el].capitalize())
    return text


def extend(n):
    # заполняет sb новыми значениями
    global s_name
    for i in range(n):
        for el in base.keys():
            s_name = el
            print(generate(el))
            print()

    print('sb =', sb)


def main():
    # тут можно тестировать функции
    # extend(10)
    print(stress(m.parse('хитрого')[0]))
    print(stress(m.parse('сухого')[0]))
    # print(stress(m.parse('пусто')[0]))
    # print(stress(m.parse('крылечка')[0]))
    #
    # print(m.parse('постою'))
    # print(check_rhyme('снег', 'стол'))
    # print(manipulate('Исповедь'))
    pass


if __name__ == "__main__":
    main()
