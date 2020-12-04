import os
import sys
import requests
from bs4 import BeautifulSoup


class Translator:
    AVAILABLE_LANGUAGE = ['All',
                          'Arabic',
                          'German',
                          'English',
                          'Spanish',
                          'French',
                          'Hebrew',
                          'Japanese',
                          'Dutch',
                          'Polish',
                          'Portuguese',
                          'Romanian',
                          'Russian',
                          'Turkish']
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/86.0.4240.193 "
                      "Safari/537.36"}
    URL = "https://context.reverso.net/translation/"

    def __init__(self):
        self.translations_list = []
        self.examples_list = []
        self.url_list = []
        self.user_input_lang1 = ""
        self.user_input_lang2 = ""
        self.translations = ""
        self.examples = ""
        self.input_word = ""

    def parse_arguments(self):
        args = sys.argv
        if len(args) != 4:
            print("Must be four arguments <python><file_name.py><your_lang><lang_to_translate><word>")
        elif args[1].capitalize() not in self.AVAILABLE_LANGUAGE:
            print(f"Sorry, the program doesn't support {args[1]}")
            exit()
        elif args[2].capitalize() not in self.AVAILABLE_LANGUAGE:
            print(f"Sorry, the program doesn't support {args[2]}")
            exit()
        else:
            self.user_input_lang1 = args[1]
            self.user_input_lang2 = args[2]
            self.input_word = args[3]

    def main(self):
        self.parse_arguments()
        if self.user_input_lang1 and self.user_input_lang2 and self.input_word:
            self.get_translations()
        else:
            self.input_by_terminal()
            self.get_translations()

    def input_by_terminal(self):
        print('''Hello, you're welcome to the translator. Translator supports: 
        1. Arabic
        2. German
        3. English
        4. Spanish
        5. French
        6. Hebrew
        7. Japanese
        8. Dutch
        9. Polish
        10. Portuguese
        11. Romanian
        12. Russian
        13. Turkish
        Type the number of your language:''')

        self.user_input_lang1 = self.user_input_lang()
        print("Type the number of a language you want to translate to "
              "or '0' to translate to all languages:")
        self.user_input_lang2 = self.user_input_lang()
        print("Type the word you want to translate:")
        self.input_word = self.user_input_word()

    def get_translations(self):
        self.make_all_urls_list()
        if self.user_input_lang2 == "all":
            self.save_to_file()
            self.read_from_file()
        else:
            self.parse_url(self.make_url(self.user_input_lang2.lower()))
            f = open(f"{self.input_word}.txt", "a", encoding="utf-8")
            f.write(f"{self.user_input_lang2.capitalize()} Translations:\n")
            for i in range(5):
                f.write(f"{self.translations[i].get_text().strip()} \n")

            f.write(f"\n{self.user_input_lang2.capitalize()} Example:\n")
            j = 0
            while j <= 9:
                f.write(self.examples[j].get_text().strip() + "\n")
                j += 1
                f.write(self.examples[j].get_text().strip() + "\n\n")
                j += 1
            f.close()
            self.read_from_file()

    def make_all_urls_list(self):
        try:
            for i in self.AVAILABLE_LANGUAGE:
                if i != self.user_input_lang1.capitalize():
                    self.url_list.append(self.make_url(i.lower()))
            return self.url_list.pop(0)
        except AttributeError:
            print("AttributeError:")
            exit()

    def save_to_file(self):
        f = open(f"{self.input_word}.txt", "a", encoding="utf-8")
        x = 1
        for i in self.url_list:
            self.parse_url(i)
            if self.AVAILABLE_LANGUAGE[x] == self.user_input_lang1.capitalize():
                x += 1
            f.write(self.AVAILABLE_LANGUAGE[x].capitalize() + " Translations:\n")
            f.write(self.translations[0].get_text().strip() + "\n\n")
            f.write(self.AVAILABLE_LANGUAGE[x].capitalize() + " Example:\n")
            f.write(self.examples[0].get_text().strip() + "\n")
            f.write(self.examples[1].get_text().strip() + "\n\n")
            x += 1
        f.close()

    def read_from_file(self):
        f = open(f"{self.input_word}.txt", encoding="utf-8")
        for line in f:
            print(line, end="")
        f.close()
        os.remove(f"{self.input_word}.txt")

    def make_url(self, lang_to_translate):
        url = self.URL + self.user_input_lang1 + "-" + lang_to_translate + "/" + self.input_word
        return url

    def parse_url(self, url):
        self.make_translation_list()
        self.make_examples_list()
        # TODO exeptions
        try:
            r = requests.get(url, headers=self.HEADERS)
            r.raise_for_status()
        except requests.exceptions.HTTPError:
            print(f"Sorry, unable to find {self.input_word}")
            exit()
        except requests.exceptions.ConnectionError:
            print("Something wrong with your internet connection")
            exit()

        soup = BeautifulSoup(r.content, 'html.parser')
        self.translations = soup.select("#translations-content a.translation")
        self.examples = soup.select("#examples-content span.text")

    def make_translation_list(self):
        for i in self.translations:
            self.translations_list.append(i.get_text().strip())
        return self.translations_list

    def make_examples_list(self):
        for i in self.examples:
            self.examples_list.append(i.get_text().strip())
        for i in range(len(self.examples_list)):
            if i % 2 != 0:
                self.examples_list[i] += "\n"
        return self.examples_list

    def user_input_lang(self):
        try:
            user_input = int(input(">"))
            if user_input < 0 or user_input > 13:
                raise Exception
            lang_numb = 0
            while lang_numb <= 13:
                if user_input == lang_numb:
                    lang = self.AVAILABLE_LANGUAGE[lang_numb].lower()
                    return lang
                lang_numb += 1
        except Exception:
            print(f"Sorry, the program doesn't support {user_input}")
            exit(print("Exiting......"))

    def user_input_word(self):
        word = input(">")
        return word.lower()


translate = Translator()
translate.main()
