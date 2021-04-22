from russtress import Accent

# Файл для тестирования ударений в тексте
accent = Accent()
while True:
    text = input()
    if text == '1':
        break
    accented_text = accent.put_stress(text)
    print(accented_text)
