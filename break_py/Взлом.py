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
    words = input_text.split()
    input_text = ' '. join(words)
    return input_text

# Функция, которая формирмирует отсортированный по частоте появления список букв
def make_sorted_alphas(text):
    counts = {letter: text.count(letter) for letter in alpha}
    sorted_counts = list(counts.values())
    sorted_counts.sort(reverse=True)
    sorted_alphas = [key for count in sorted_counts for key, value in counts.items() if count == value]
    return sorted_alphas

# Функция форирует текст на основе сопоставления букв
def make_preliminary_text(encr_text, our_alphs, alphs):
    preliminary_text = ''
    for our_txt_a in encr_text:
        for encrypted_alpha, decrypted_alpha in zip(our_alphs, alphs):
            if our_txt_a == encrypted_alpha:
                our_txt_a = decrypted_alpha
                break
        preliminary_text += our_txt_a
    return preliminary_text

# Вычисляет разницу между словами: процент одинаковых букв
def difference_between_two_words(word_one, word_two):
    same_al_count = 0
    for a1, a2 in zip(word_one, word_two):
        if a1 == a2:
            same_al_count += 1
    res_percent =  round(same_al_count / len(word_one) * 100)
    return res_percent

'''
Функция, которая распределяет слова из текста на три группы: 
1. Слова из одной буквы
2. Слова, которые есть в словаре
3. Слова, которых нет в словаре
'''
def distribute_words(fin_text, input_dict):
    one_alpha_words = []
    trusted_words = []
    untrusted_words = []
    for word_n, our_word in enumerate(fin_text):
        if len(our_word) < 2:
            one_alpha_words.append((word_n, our_word))
        elif our_word in input_dict:
            trusted_words.append((word_n, our_word))
        else:
            untrusted_words.append((word_n, our_word))
    # Сортируем, чтобы в начале шли самые длинные слова, 
    # и результаты дальнейших шагов были более точными
    untrusted_words.sort(key = lambda x: len(x[1]), reverse=True)
    return one_alpha_words, trusted_words, untrusted_words

# Функция формирует множество букв, которые точно не перепутаны
def make_trusted_letters(trstd_wrds):
    trusted_letters = set()
    for trstd_wrd in trstd_wrds:
        if len(trstd_wrd) > 7:
            trusted_letters |= set(trstd_wrd)
    return trusted_letters
    
# Функция, которая находит в словаре слова, похожие на данное
def make_same_words(untrstd_w, inp_dict, percent):
    same_words = []
    for dict_word in inp_dict:
        if len(dict_word) == len(untrstd_w):
            diff = difference_between_two_words(untrstd_w, dict_word)
            if diff >= percent:
                same_words.append((dict_word, diff))
    # Сортировка по проценту совпадающих букв, чтобы в начале были самые похожие слова
    same_words.sort(key=lambda i: i[1], reverse=True)
    return same_words

# Функция и делает список, содержащий сомнительные слова и все слова из словаря, которые на них похожи
def make_same_words_list(untrusted, in_dict, prcnt):
    almost_correct = [] # для похожих слов
    wrong = [] # для слов, для которых не найдено похожих
    for untrstd_w_n, untrstd_wrd in untrusted:
        same_ws = make_same_words(untrstd_wrd, in_dict, prcnt) # ищутся похожие
        if len(same_ws):
            almost_correct.append(((untrstd_w_n, untrstd_wrd), same_ws))
        else:
            wrong.append((untrstd_w_n, untrstd_wrd))
    return almost_correct, wrong

# Функция возвращает номера слов с их заменами, а также все пары заменяемых букв
def replacements(almst, trusted_lt):
    all_letter_replacements = []
    replacements = []
    for alm_corr, alm_corr_wrds in almst:
        for alm_corr_wrd in alm_corr_wrds:
            replacements_for_word = make_letters_replacements(alm_corr[1], alm_corr_wrd[0], trusted_lt)
            if replacements_for_word:
                replacements.append((alm_corr[0], alm_corr[1], alm_corr_wrd[0]))
                add_to_all_letters_replacements(all_letter_replacements, replacements_for_word)
                break
    return replacements, all_letter_replacements

# Добавляет замены букв в список замен, если их там ещё нет
def add_to_all_letters_replacements(all_lttr_rplcmnts, rplcmnts_fr_wrd):
    for replacement in rplcmnts_fr_wrd:
        if replacement not in all_lttr_rplcmnts:
            all_lttr_rplcmnts.append(replacement)

# Находит все различия в буквах для двух слов, 
# если эти буквы являются недоверенными
def make_letters_replacements(word1, word2, trusted_ltr):
    letters_replacements = []
    for letter1, letter2 in zip(word1, word2):
        if letter1 != letter2:
            if letter1 in trusted_ltr or letter2 in trusted_ltr:
                return
            elif (letter1, letter2) not in letters_replacements:
                letters_replacements.append((letter1, letter2))
    return letters_replacements

# Для поданного на вход слова функция формирует его замену в тексте, 
# используя информацию о заменах букв
def make_same_word(wrd, lt_rplcmnts):
    new_word = ''
    for l in wrd:
        for lt_r in lt_rplcmnts:
            if l == lt_r[0]:
                l = lt_r[1]
                break
        new_word += l
    return new_word

# Функция, которая формирует окончательную версию текста
def make_final_text(input_preliminary, input_dictionary, percnt):
    final_text = input_preliminary.split()
    '''
    Списки:
    1. Слова из одной буквы
    2. Слова, найденные в словаре
    3. Слова, не найденные в словаре
    '''
    one_a, trusted_w, untrusted_w = distribute_words(final_text, input_dictionary)
    # 'Доверенные' буквы
    trusted_l = make_trusted_letters(dict(trusted_w).values())
    # Списки для слов, для которых нашлись похожие слова 
    # и для слов, для которых не нашлись
    almost, wrng = make_same_words_list(untrusted_w, input_dictionary, percnt)
    # Список со словами, которые надо заменить и с парами заменяемых букв
    rplcmnts, lttr_rplcmnts = replacements(almost, trusted_l)
    
    # Производим замену слов, для которых есть похожие в словаре
    for rplcmnt in rplcmnts:
        final_text[rplcmnt[0]] = rplcmnt[2]
    
    # Для слов, для которых похожих не найдено, просто заменяем буквы,
    # используя информацию об уже заменённых ранее буквах
    for wrng_wrd in wrng:
        final_text[wrng_wrd[0]] = make_same_word(wrng_wrd[1], lttr_rplcmnts)
    
    # Если слово состоит из одной буквы, и эта буква была ранее заменена, 
    # то это слово заменяется на соответствующую букву
    for o_a in one_a:
        for lttr_rplcmnt in lttr_rplcmnts:
            if o_a[1] == lttr_rplcmnt[0]:
                final_text[o_a[0]] = lttr_rplcmnt[1]
                break
    
    # Запись промежуточных данных алгоритма
    with open('log.txt', 'w') as log:
        print(trusted_l, file=log)
        print(lttr_rplcmnts, file=log)
        print(file=log)
        for a in almost:
            print(a, file=log)
        print(file=log)
        for rpl in rplcmnts:
            print(rpl, file=log)
        
    return ' '.join(final_text)
    

# Берём слова из словаря
with open("Dictionary.txt") as d_f:
    dictionary = d_f.read().split()

# Буквы, отсортированные по частоте
with open("sorted_alphas.txt") as s_f:
    alphas = s_f.read().split()

print("Взлом методом частотного анализа\n")

while True:
    print('Нажмите e чтобы выйти, или любую другую клавишу, чтобы продолжить')
    if input() == 'e':
        break
    
    path_to_file = input("Введите путь к файлу: ")
    
    # Пытаемся открыть файл  
    try:
        file = open(path_to_file, encoding='utf-8')
    except IOError:
        print('Какие - то проблемы с файлом. Пожалуйста, попробуйте ещё раз')
        continue
    else:
        with file:
            our_text = handle_text(file.read())
        # Если получилось, расшифровываем
        our_alphas = make_sorted_alphas(our_text)
        # Создаём и записываем предварительный вариант текста
        preliminary = make_preliminary_text(our_text, our_alphas, alphas)
        with open("preliminary.txt", 'w') as prelim_f:
            prelim_f.write(preliminary)
        # Создаём финальную версию текста, на основе анализа словаря
        final_result = make_final_text(preliminary, dictionary, 65)
        
        # Запись в файл
        f_name = input("Готово! Введите имя файла, в который записать результат: ")
        
        try:
            f = open(f_name, 'w')
        except IOError:
            print('Ошибка')
        else:
            with f:
                f.write(final_result)
            print('Файл записан')
            
            
            