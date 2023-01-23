# Алфавит 
alpha = [chr(letter + 97) for letter in range(26)] 
alphabet = alpha + [' ']

# Функция, которая оставляет в тексте только буквы и пробелы
def handle_text(input_text):
    input_text = input_text.lower()
    trantab = str.maketrans("-—", '  ')
    input_text = input_text.translate(trantab)
    input_text = ' '. join(input_text.split())
    input_text = ''.join([char for char in input_text if char in alphabet])
    input_text = ' '. join(input_text.split())
    return input_text

# Функция, зашифровывающая текст
def encrypt(text, kword, k):
    key_list = list(kword)
    # Список с переставленными символами алфавита
    rearranged = key_list + [lttr for lttr in alpha if lttr not in key_list]
    rearranged = rearranged[-k:] + rearranged[:-k]
    encrypted_text = ''
    # Буквы шифруются в цикле
    for alpha_char in text:
        for true_alpha, crypted_alpha in zip(alpha, rearranged):
            if alpha_char == true_alpha:
                alpha_char = crypted_alpha
                break
        encrypted_text += alpha_char
    return encrypted_text

# Функция, расшифровывающая текст
def decrypt(txt, kwrd, k_n):
    key_lst = list(kwrd)
    # Список с переставленными символами алфавита
    rearranged = key_lst + [ltr for ltr in alpha if ltr not in key_lst]
    rearranged = rearranged[-k_n:] + rearranged[:-k_n]
    decrypted_text = ''
    # Буквы расшифровываются в цикле
    for alpha_chr in txt:
        for cr_alpha, tr_alpha in zip(rearranged, alpha):
            if alpha_chr == cr_alpha:
                alpha_chr = tr_alpha
                break
        decrypted_text += alpha_chr
    return decrypted_text

print('Программа шифрования шифрования – дешифрования методом Цезаря с ключевым словом для английского языка')

while True:
    # Пользовательский ввод
    print('''
Что вы хотите сделать? 
1 -> зашифровать
2 -> расшифровать
3 -> выход ''')
    operation = input()
    if operation not in ['1', '2', '3']:
        print('Введите, пожалуйста, цифру 1 или 2')
        continue
    elif operation == '3':
        input('До свидания!')
        break
    path = input('Введите путь к файлу: ')
    keyword = input('Введите ключевое слово: ')
    keyword = keyword.lower()
    if any(letter not in alpha for letter in keyword):
        print('Вы ввели некорректное слово, пожалуйста, попробуйте ещё раз')
        continue
    else:
        new_word = ''
        for l in keyword:
            if l not in new_word:
                new_word += l
        keyword = new_word
        print(keyword)
    k_str = input('Введите число k: ')
    
    try:
        k = int(k_str)
    except:
       print('Вы ввели некорректное число, пожалуйста, попробуйте ещё раз')
       continue
    
    if k > 25 or k < 0:
        print('Вы ввели некорректное число, пожалуйста, попробуйте ещё раз')
        continue
    
    # Пытаемся открыть файл, если получается, то зашифрвываем или расшифровываем
    try:
        file = open(path, encoding='utf-8')
    except IOError:
        print('Какие - то проблемы с файлом. Пожалуйста, попробуйте ещё раз')
        continue
    else:
        with file:
            text_to_crypt = handle_text(file.read())
        if operation == '1':
            encrypted = encrypt(text_to_crypt, keyword, k)
            if encrypted:
                print("\nФайл успешно зашифрован\n")
                filename = input('Введите имя файла, в который записать результат: ')
                
                try:
                    f = open(filename, 'w')
                except IOError:
                    print('Ошибка')
                else:
                    with f:
                        f.write(encrypted)
                    print('Файл записан')
            else:
               print("\nОшибка. Попробуйте ещё раз")
        else:
            decrypted = decrypt(text_to_crypt, keyword, k)
            if decrypted:
                print("\nФайл успешно расшифрован")
                
                # Запись в файл
                filename = input('Введите имя файла, в который записать результат: ')
                
                try:
                    f = open(filename, 'w')
                except IOError:
                    print('Ошибка')
                else:
                    with f:
                        f.write(decrypted)
                    print('Файл записан')
            else:
               print("\nОшибка. Попробуйте ещё раз")


