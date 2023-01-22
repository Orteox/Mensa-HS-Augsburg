from PyPDF2 import PdfReader
import requests
import os
import re


def main():
    url = "https://www.hs-augsburg.de/Service/Mensa-und-Cafeteria.html"
    html = requests.get(url).text
    html = html.split("hyphenate tinymce-content")[2]
    html = html.split('a href="')[1]
    html = html.split('" target')[0]
    r = requests.get(html)
    open('mensa.pdf', 'wb').write(r.content)
    reader = PdfReader("mensa.pdf")
    text = reader.pages[0].extract_text() + "\n"

    one = text.split("Tellergericht I ")[1].split("Tellergericht")[0]
    one = re.split(r"\d+,\d+\d+ € \| \d+,\d+\d+ € \| \d+,\d+\d+ €", one)
    del (one[-1])

    two = text.split("Tellergericht\nII")[1].split("Beilagen")[0]
    two = re.split(r"\d+,\d+\d+ € \| \d+,\d+\d+ € \| \d+,\d+\d+ €", two)
    del (two[-1])

    weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

    for i in range(len(one)):
        print(weekdays[i] + ":\n" + re.sub(r'\(\d+(\s*,\s*\d+)+\)', ' ', one[i]) + "\n" +
              re.sub(r'\(\d+(\s*,\s*\d+)+\)', ' ', two[i] + "-" * 30))
    os.remove("mensa.pdf")


if __name__ == '__main__':
    main()
