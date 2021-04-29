from tkinter import *
from tkinter.ttk import Combobox
import requests
from bs4 import BeautifulSoup

languages = ["Arabic", "German", "English", "Spanish", "French", "Hebrew", "Japanese", "Dutch", "Polish", "Portuguese", "Romanian", "Russian", "Turkish"]


def target_languages():
    lan_list = languages
    lan_list.append("All")
    return lan_list


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
            self.example_list.append(i.text.strip().replace("\n\n\n\n\n", "\n").replace("          ", ""))
        return self.example_list


class GUI:

    def __init__(self, window):
        self.main_language = str()
        self.target_language = str()
        self.word = str()

        self.welcome = Label(window, text="Welcome to Online Translator")
        self.welcome.place(x=300, y=20)

        self.main_language_label = Label(window, text="Main Language")
        self.main_language_label.place(x=70, y=70)

        self.language_list_box = Combobox(window, values=languages)
        self.language_list_box.place(x=50, y=100)

        self.word_label = Label(window, text="Word")
        self.word_label.place(x=340, y=70)

        self.word_entry = Entry()
        self.word_entry.place(x=300, y=100)

        self.to_language_label = Label(window, text="Target Language")
        self.to_language_label.place(x=570, y=70)

        self.target_language_box = Combobox(window, values=target_languages())
        self.target_language_box.place(x=550, y=100)

        self.translate_button = Button(text="Translate", bg="#03fccf", command=self.translate)
        self.translate_button.place(x=340, y=150)

        self.translations_canvas = Canvas(window, bg="white", scrollregion=(0, 0, 500, 1500))
        self.translations_canvas.place(x=70, y=200, width=700, height=400)

        self.scrollY = Scrollbar(self.translations_canvas, orient=VERTICAL)
        self.scrollY.pack(fill="y", side=RIGHT)
        self.scrollY.config(command=self.translations_canvas.yview)
        self.translations_canvas.config(yscrollcommand=self.scrollY.set)

        self.translations = Label(self.translations_canvas, bg="white")

    def translate(self):
        self.main_language = self.language_list_box.get().lower()
        self.target_language = self.target_language_box.get().lower()
        self.word = self.word_entry.get()
        words = str()
        sample_sentences = str()

        if self.target_language == "all":
            self.translations_canvas.create_window(250, 700, window=self.translations)
            for language in languages:
                online_translator = Translation(self.main_language, language.lower(), self.word)
                online_translator.exact_url()
                word_list = online_translator.word_translation()
                sentence_list = online_translator.example_sentences()

                try:
                    words += f"{language} Translation\n" + word_list[0] + "\n\n"
                except IndexError:
                    print()
                try:
                    sample_sentences += f"{language} Examples\n" + sentence_list[0] +"\n\n"
                except IndexError:
                    print()

        else:
            self.translations_canvas.create_window(250, 250, window=self.translations)
            online_translator = Translation(self.main_language, self.target_language, self.word)
            online_translator.exact_url()
            word_list = online_translator.word_translation()
            sentence_list = online_translator.example_sentences()

            for i in range(5):
                if i == 4:
                    words += word_list[i]
                else:
                    words += word_list[i] + "\n\n"

            for i in range(5):
                if i == 4:
                    sample_sentences += sentence_list[i]
                else:
                    sample_sentences += sentence_list[i] +"\n\n"

        translations = f"\t\t\t\tWords\n\n{words}\n\n\t\t\t\tSample Sentences\n\n{sample_sentences}"
        self.translations.configure(text=translations)


win = Tk()
myGUI = GUI(win)
win.title('Online Translator')
win.geometry("800x600+350+100")
win.config(bg="#ff944d")
win.mainloop()
