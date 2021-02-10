import requests

import sys

from bs4 import BeautifulSoup

languages = ["Arabic", "German", "English", "Spanish", "French", "Hebrew", "Japanese", "Dutch", "Polish", "Portuguese", "Romanian", "Russian", "Turkish", "All"]
def welcome():
    print("Hello, you're welcome to the translator. Translator supports:")
    languages = ["Arabic", "German", "English", "Spanish", "French", "Hebrew", "Japanese", "Dutch", "Polish", "Portuguese", "Romanian", "Russian", "Turkish"]
    for i in range(len(languages)):
        print(f"{i+1}. {languages[i]}")

def lan_print(lan):
    return f"{lan} Translations:"

def examp_print(lan):
    return f"{lan} Examples:"

def translate_to_all(main_lan):
    languages.remove(main_lan)
    return languages

def open_file(word):
    file = open(f"{word}.txt", "w", encoding="utf-8")
    return file

class Translation:
    language = ""
    word = ""
    url = "https://context.reverso.net/translation/"

    def __init__(self, source_lan, translate_lan, chosen_word):
        self.source_language = source_lan
        self.translate_language = translate_lan
        self.word = chosen_word
        self.word_list = list()
        self.example_list = list()

    def exact_url(self):
        self.url = f"{self.url}{self.source_language}-{self.translate_language}/{self.word}"
        self.r = requests.get(self.url, headers={'User-Agent': 'Mozilla/5.0'})
        self.soup = BeautifulSoup(self.r.content, "html.parser")

    def access_to_website(self):
        return self.r.status_code

    def word_translation(self):
        self.words = self.soup.find_all('a', class_="translation")
        for i in self.words:
            if i.text.strip() != 'Translation':
                self.word_list.append(i.text.strip())
        return self.word_list

    def example_sentences(self):
        self.examples = self.soup.find_all('div', class_="example")
        for i in self.examples:
            self.example_list.append(i.text.strip())
        return self.example_list


#welcome()
args = sys.argv
#print("Type the number of your language:")
main_language = args[1]
#print("Type the number of a language you want to translate to or '0' to translate to all languages:")
to_language = args[2]
#print("Type the word you want to translate:")
word_choice = args[3]
try:
    counter = languages.count(to_language.capitalize())
    if counter == 0:
        raise ValueError
except ValueError:
    print(f"Sorry, the program doesn't support {to_language}")
    exit()
try:
    counter = languages.count(main_language.capitalize())
    if counter == 0:
        raise  ValueError
except ValueError:
    print(f"Sorry, the program doesn't support {main_language}")
    exit()
else:
    source_lan = main_language
    if to_language == 'all':
        languages.remove("All")
        all_lan_list = translate_to_all(source_lan.capitalize())
        file = open_file(word_choice)
        for lan in all_lan_list:
            translation_obj = Translation(source_lan.lower(), lan.lower(), word_choice)
            translation_obj.exact_url()
            try:
                translation_obj.word_translation()[0]
            except IndexError:
                print(f"Sorry, unable to find {word_choice}")
                break
            else:
                print("\n")
                print(lan_print(lan.capitalize()))
                file.write("\n\n\n" + lan_print(lan.capitalize()) + "\n")
                for i in range(1):
                    word = translation_obj.word_translation()[i]
                    print(word)
                    file.write(word)
                print("\n")
                print(examp_print(lan))
                file.write("\n\n\n" + examp_print(lan) + "\n")
                for i in range(1):
                    example = translation_obj.example_sentences()[i].replace("\n\n\n\n\n", "\n").replace("          ", "")
                    print(example)
                    file.write(example)
        file.close()
    else:
        languages.remove("All")
        translate_lan = to_language
        translation_obj = Translation(source_lan.lower(), translate_lan.lower(), word_choice)
        translation_obj.exact_url()
        try:
            translation_obj.word_translation()[0]
        except IndexError:
            print(f"Sorry, unable to find {word_choice}")
        else:
            print("\n")
            print(lan_print(translate_lan.capitalize()))
            file = open_file(word_choice)
            file.write(lan_print(translate_lan.capitalize()) + "\n")
            for i in range(5):
                word = translation_obj.word_translation()[i]
                file.write(word + "\n")
                print(word)

            print("\n")
            print(examp_print(translate_lan.capitalize()))
            file.write("\n\n" + examp_print(translate_lan.capitalize()) + "\n")
            for i in range(5):
                example = translation_obj.example_sentences()[i].replace("\n\n\n\n\n", "\n").replace("          ", "")
                print(example + "\n")
                file.write(example + "\n\n")
            file.close()
