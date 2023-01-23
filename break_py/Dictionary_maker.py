# Алфавит
alpha = [chr(letter + 97) for letter in range(26)]
alphabet = alpha + [' ']

def handle_text(input_text):
    input_text = input_text.lower()
    trantab = str.maketrans("-—", '  ')
    input_text = input_text.translate(trantab)
    input_text = ' '. join(input_text.split())
    input_text = ''.join([char for char in input_text if char in alphabet])
    words = input_text.split()
    input_text = ' '. join(words)
    return input_text

def get_handled_text_from_file(file_path):
    with open(file_path, encoding='utf-8') as file_text:
        text_lines = file_text.read()
    return handle_text(text_lines) 

def make_dictionary(txt):
    no_duplicates = list(set(txt.split()))
    no_duplicates.sort()
    with open("Dictionary.txt", 'w') as d_file:
        for w in no_duplicates:
            d_file.write(w + '\n')

def make_dictionary_from_file(file_path):
    dict_text = get_handled_text_from_file(file_path)
    make_dictionary(dict_text)
    
# Функция, которая формирмирует отсортированный по частоте появления список букв
def make_sorted_alphas(text):
    counts = {letter: text.count(letter) for letter in alpha}
    sorted_counts = list(counts.values())
    sorted_counts.sort(reverse=True)
    sorted_alphas = [key for count in sorted_counts for key, value in counts.items() if count == value]
    return sorted_alphas
    
def make_sorted_alphas_sample(text_for):
    to_write = make_sorted_alphas(text_for)
    with open("sorted_alphas.txt", 'w') as s_file:
        for a in to_write:
            s_file.write(a + '\n')
            
make_dictionary_from_file('Dictionary_text.txt')