import requests
from bs4 import BeautifulSoup
import json, csv


datas = []
# Afficher le status code pour vérifier la connexion
# print(response.status_code)

# Afficher le contenu du site
# print(response.text)

page = 1
next_page = True
# Pagination
while next_page:
    url = f"https://quotes.toscrape.com/page/{page}/"
    print(url)

    response = requests.get(url)

    if response.status_code == 200:
        html_doc = response.text
        soup = BeautifulSoup(html_doc, 'html.parser')
        li_next = soup.find('li', {'class': "next"})
        print(page)

        # print(soup)
        # En cas de propriete de la balise on definit une dico dans l'argument
        # eg. soup.find('div', {'class':container})
        # h1 = soup.find('h1')
        # a = h1.find('a')

        # a.text permet d'accéder au contenu de la balise
        # print(a.text)
        html_doc = response.text
        soup = BeautifulSoup(html_doc, 'html.parser')

        quotes = soup.findAll('div', {'class': "quote"})
        # print(len(quotes))

        for quote in quotes:
            # print(quote)
            # print("======"*2)
            data = {}
            text = quote.find('span', {'class': "text"})

            author = quote.find('small', {'class': "author"})
            tags = quote.findAll('a', {'class': "tag"})
            tag_value = ""
            for tag in tags:
                # Concatenation - alignement sur ligne
                tag_value += " " + tag.text

            # Creation du dictionnaire avec les données
            data['text'] = text.text
            data['author'] = author.text
            data['tags'] = tag_value

            # Mise à jour du tableau avec les données du dictionnaire
            datas.append(data)

        # print(json.dumps(datas, indent=4, ensure_ascii=False))
    else:
        print("Scraping fail")

    # Contrôle pour arrêter la boucle
    if li_next:
        page += 1
    else:
        next_page = False


# Fichier Csv - Enregistrement
if datas:
    with open("quotes.csv", "w", newline='', encoding='utf-8') as csvfile:
        fieldnames = ['text', 'author', 'tags']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for data in datas:
            writer.writerow(data)
