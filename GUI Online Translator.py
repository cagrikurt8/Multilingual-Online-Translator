from tkinter import *
from tkinter.ttk import Combobox
import requests
from bs4 import BeautifulSoup
import pandas as pd
import seaborn as sbn
import matplotlib.pyplot as plt

# Altta web scraping yapmak için kullanacağım dillerin listesini depoladım
languages = ["Arabic", "German", "English", "Spanish", "French", "Hebrew", "Japanese", "Dutch", "Polish", "Portuguese", "Romanian", "Russian", "Turkish", "Chinese"]


def target_languages():
    """
    Grafiksel arayüzde target language seçeneklerinde gözükmesi için languages listesine
    'All' seçeneğini ekleyen ve kopyasını döndüren bir fonksiyon
    :return: Tüm dilleri ve 'All' seçeneğini içeren bir liste
    """
    lan_list = languages
    lan_list.append("All")
    return lan_list


class Translation:
    """
    Web scraping yaparak toplamda 14 dil destekleyen bir online çeviri programı
    Bir dilden bir dile veya bir dilden diğer 13 dile çeviri yapmayı sağlar
    """
    url = "https://context.reverso.net/translation/"  # Çeviri için web scraping yapılacak site

    def __init__(self, source_lan, translate_lan, chosen_word):
        """
        Çeviri programının constructorı verilen çeviri dili, çevrilecek dil ve kelimeyi alarak bu parametreleri
        web scraping yapılacak sitenin URL'inde uygun yerlere yerleştirip verileri çeker
        :param source_lan: kaynak dil
        :param translate_lan: çevrilecek dil
        :param chosen_word: çevrilecek kelime
        """
        self.source_language = source_lan  # Kaynak dil
        self.translate_language = translate_lan  # Çevrilecek dil
        self.word = chosen_word  # Çevrilecek kelime
        self.word_list = list()  # Çevrilen kelimeleri depolayacak liste
        self.example_list = list()  # Örnek cümleleri depolayacak liste
        self.url = f"{self.url}{self.source_language}-{self.translate_language}/{self.word}"  # Verilen kaynak ve hedef dile göre web scraping için kullanılacak URL
        self.r = requests.get(self.url, headers={'User-Agent': 'Mozilla/5.0'})  # Web scraping için URL e bağlantı sağlayan request
        self.soup = BeautifulSoup(self.r.content, "html.parser")  # Web scraping ile veri çekmek için BeautifulSoup objesi

    def access_to_website(self):
        """Siteye erişimin başarılı olup olmadığını görmek için bir fonksiyon, başarılı ise status code 200 döndürür"""
        return self.r.status_code

    def word_translation(self):
        """
        Verilen kaynak dil, çevrilecek dil ve kelimeyi dikkate alarak kelime çevirilerini döndürür
        :return: Çevrilen kelimelerin listesini döndürür
        """
        words = self.soup.find_all('a', class_="translation")  # Kaynak sitede kelime çevirileri html kodunda 'a' tag i ile girilmişti. Onları çekmek için 'a' tagi ile ve class larını girerek arama yapıyoruz
        for i in range(6):  # Çevrilen kelimelerden ilk 5ini almak için döngü, ilk gelen veri Translation olduğu için range 6
            try:
                if words[i].text.strip() != 'Translation':
                    self.word_list.append(words[i].text.strip())  # Çevrilen kelimeler listede depolanıyor
            except IndexError:  # 'All' seçeneği seçildiğinde listeden tüm diller hem 'all' ı hem de kaynak dilin kendisini içerir. Bu durum programın akışına zarar vermesin diye o kısımlarda continue ile döngü devam eder
                continue
        return self.word_list

    def example_sentences(self):
        """
        Verilen kaynak dil, çevrilecek dil ve kelimeyi dikkate alarak o kelimeyi içeren örnek cümleler döndürür
        :return: Kelimeyi içeren örnek cümleler döndürür
        """
        examples = self.soup.find_all('div', class_="example")  # Kaynak siteden 'div' tagi ile örnek cümleleri çeker
        for i in range(5):  # Örnek cümlelerden ilk 5 tanesi çekilir
            try:
                self.example_list.append(examples[i].text.strip().replace("\n\n\n\n", ""))
            except IndexError:  # # 'All' seçeneği seçildiğinde listeden tüm diller hem 'all' ı hem de kaynak dilin kendisini içerir. Bu durum programın akışına zarar vermesin diye o kısımlarda continue ile döngü devam eder
                continue
        return self.example_list


class GUI:
    """
    Çeviri programı ile birlikte çalışarak grafiksel arayüz oluşturmamızı sağlayan class
    """
    def __init__(self, window):
        """
        Verilen bir tkinkter window parametresi üzerinde çeşitli grafiksel arayüz objeleri oluşturan constructor
        Kaynak dil, hedef dil ve kelime için labeller oluşturur
        Kaynak dil ve hedef dil için seçim yapmamızı sağlayan bir liste(Combobox) ekler
        Kelime girişi yapmamız için bir Entry widget ı ekler
        Çeviri işlemini başlatmamız için de bir buton ekler
        :param window: Grafiksel objeler oluşturulacak window
        """
        self.main_language = str()  # Kaynak dil
        self.target_language = str()  # Hedef dil
        self.word = str()  # Çevrilecek kelime

        self.welcome = Label(window, text="Welcome to Online Translator")  # Programın en üstündeki hoş geldiniz label ı
        self.welcome.place(x=300, y=20)  # welcome label ının konum parametreleri

        self.main_language_label = Label(window, text="Main Language")  # Kaynak dil label
        self.main_language_label.place(x=70, y=70)  # Kaynak dil label konum parametreleri

        self.language_list_box = Combobox(window, values=languages)  # Kaynak dil seçim listesi
        self.language_list_box.place(x=50, y=100)  # Kaynak dil seçim listesi konum parametreleri

        self.word_label = Label(window, text="Word")  # Çevrilecek dil label
        self.word_label.place(x=340, y=70)  # Çevrilecek dil label konum parametresi

        self.word_entry = Entry()  # Çevrilecek dil için metin Entry widget
        self.word_entry.place(x=300, y=100)  # Metin Entry widget konum parametreleri

        self.to_language_label = Label(window, text="Target Language")  # Hedef dil seçim label
        self.to_language_label.place(x=570, y=70)  # Hedef dil label konum parametreleri

        self.target_language_box = Combobox(window, values=target_languages())  # Hedef dil seçim listesi
        self.target_language_box.place(x=550, y=100)  # Hedef dil seçim listesi konum parametreleri

        self.translate_button = Button(text="Translate", bg="#03fccf", command=self.translate)  # Çeviri butonu
        self.translate_button.place(x=340, y=150)  # Çeviri butonu konum parametreleri

        self.translations_canvas = Canvas(window, bg="white", scrollregion=(0, 0, 500, 2500))  # Çevirilerin sunulacağı metin alanı
        self.translations_canvas.place(x=30, y=200, width=750, height=400)  # Metin alanının konumu ve boyutları

        self.scrollY = Scrollbar(self.translations_canvas, orient=VERTICAL)  # Metin alanı için kaydırma barı
        self.scrollY.pack(fill="y", side=RIGHT)  # Scrollbar ın konumu ve yönü
        self.scrollY.config(command=self.translations_canvas.yview)  # Scrollbar ın işlevi
        self.translations_canvas.config(yscrollcommand=self.scrollY.set)  # Metin alanı ile scrollbar entegresi

        self.translations = Label(self.translations_canvas, bg="white")

    def translate(self):
        """
        Translation class ı ile seçilen kaynak dil, hedef dil ve girilen kelime bağlamında etkileşime girer ve
        Translation class ından kelime ile cümle çevirilerini alıp grafiksel arayüzde gösterilmek üzere ekler
        :return: Çevrilen kelimeleri ve örnek cümleleri döndürür
        """
        self.main_language = self.language_list_box.get().lower()  # Seçilen kaynak dil
        self.target_language = self.target_language_box.get().lower()  # Seçilen hedef dil
        self.word = self.word_entry.get()  # Girilen kelime
        words = str()
        sample_sentences = str()

        if self.target_language == "all":  # Eğer seçilen hedef dil 'All' ise listedeki tüm dillere olan çeviriler yapılacak
            self.translations_canvas.create_window(250, 1270, window=self.translations)  # Çeviri alanı boyut düzenlemesi
            for language in languages:  # Dil listesindeki tüm dillere çeviriler yapılıp depolanacak ve çeviri alanına eklenecek
                online_translator = Translation(self.main_language, language.lower(), self.word)
                word_list = online_translator.word_translation()
                sentence_list = online_translator.example_sentences()

                try:
                    words += f"\t\t\t\t{language} Translation\n\t\t\t\t" + word_list[0] + "\n\n\n\n"
                except IndexError:
                    continue
                try:
                    sample_sentences += f"\t\t\t\t{language} Examples\n\t\t\t\t" + sentence_list[0] + "\n\n\n\n"
                except IndexError:
                    continue

        else:  # Eğer hedef dil spesifik bir dil ile bu koşul gerçekleşecek
            self.translations_canvas.create_window(250, 360, window=self.translations)  # Çeviri alanı boyut düzenlemesi
            online_translator = Translation(self.main_language, self.target_language, self.word)  # Girilen parametrelere göre çeviri objesi
            word_list = online_translator.word_translation()  # Kelime listesi
            sentence_list = online_translator.example_sentences()  # Örnek cümle listesi

            for i in range(5):
                if i == 4:
                    words += "\t\t\t\t" + word_list[i]
                else:
                    words += "\t\t\t\t" + word_list[i] + "\n\n"

            for i in range(5):
                if i == 4:
                    sample_sentences += "\t\t\t\t" + sentence_list[i]
                else:
                    sample_sentences += "\t\t\t\t" + sentence_list[i] + "\n\n\n\n"

        translations = f"\t\t\t\tWords\n\n\n\n{words}\n\n\n\n\t\t\t\tSample Sentences\n\n\n\n{sample_sentences}"  # Çeviri alanına eklenecek son string
        self.translations.configure(text=translations)  # Çeviri alanındaki metne parametre olarak çeviriler veriliyor
        language_plot(self.main_language)  # Kaynak dildeki en yaygın 10 kelime grafiği ve dataframe


def language_plot(language):
    """
    Seçilen kaynak dili baz alarak o dilde en çok kullanılan kelimeler listesinden ilk 10 kelimeyi bir siteden
    web scraping yöntemi ile çeker ve bunları bir dataframe e ekler. Sonrasında da bu kelimeleri yaygınlık derecelerine
    göre bir barplot ile sunar
    :param language: En çok kullanılan kelimelerin seçileceği dil
    """
    link = f"https://1000mostcommonwords.com/1000-most-common-{language}-words/"  # En yaygın kelimeler için kaynak URL
    r = requests.get(link, headers={'User-Agent': 'Mozilla/5.0'})  # URL e bağlanmak için request
    soup = BeautifulSoup(r.content, "html.parser")  # Veri çekmek için BeautifulSoup objesi

    data = soup.find_all('td')  # Kelimelerin depolandığı 'td' tagi ile web scraping
    words = list()
    if language == "english":
        for i in range(5, 33, 3):
            words.append(data[i].text)
    else:
        for i in range(4, 32, 3):
            words.append(data[i].text)
    dframe = pd.DataFrame(data=words, columns=[f"{language.capitalize()} Words"])  # Kelime DataFrame
    dframe["Frequency"] = [i for i in range(10, 0, -1)]
    sbn.barplot(x=dframe[f"{language.capitalize()} Words"], y=dframe["Frequency"])  # Kelime grafiği
    plt.title(f"Most Common 10 {language.capitalize()} Words")
    plt.show()
    print(dframe)


win = Tk()  # Tkinter Window u
myGUI = GUI(win)  # GUI class'ının işlem yapacağı window parametre olarak verilip obje oluşturuluyor
win.title('Online Translator')  # Grafik arayüzünün pencere title ı
win.geometry("800x600+350+100")  # Grafik arayüzünün başlangıç boyutları ve konumu
win.config(bg="#ff944d")  # Grafik arayüzünün arkaplan rengi
win.mainloop()  # Grafik arayüzünün program çalıştığı sürece girdiğimiz verilere ve buton aksiyonlarına tepki vermesi için mainloop döngü
