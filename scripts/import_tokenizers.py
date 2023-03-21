# Import libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd
import importlib
import spacy
from spacy.tokenizer import Tokenizer

# Create an URL object
url = 'https://spacy.io/usage/models'
# Create object page
page = requests.get(url)

# parser-lxml = Change html to Python friendly format
# Obtain page's information
soup = BeautifulSoup(page.text, 'lxml')

table1 = soup.find('table', {'class':'table_root__ZlA_w'})

# Obtain every title of columns with tag <th>
headers = []
for i in table1.find_all('th'):
    title = i.text
    headers.append(title)

print(table1)


# Create a dataframe
mydata = pd.DataFrame(columns = headers)

# Create a for loop to fill mydata
for j in table1.find_all('tr')[1:]:
    row_data = j.find_all('td')
    row = [i.text for i in row_data]
    length = len(mydata)
    mydata.loc[length] = row

print(mydata)


modnames = mydata.Code
for language in modnames:
    package_name = f"spacy.lang.{language}"
    globals()[package_name] = importlib.import_module(package_name)


langs = {}
for index, row in mydata.iterrows():
    if row["Language"] == "Multi-language":
        continue

    full_name = row["Language"].replace(" ", "")
    code = row["Code"]

    try:
        # Import corresponding language
        exec("nlp = spacy.lang.%s.%s()" % (code, full_name))
        # Use default tokenizer for the language
        langs[code] = {"lang" : nlp, "tokenizer" : nlp.tokenizer}
        print("Added instance of %s" % (row["Language"]))
    except ImportError:
        print("Cannot import language %s" % (row["Language"]))
    except AttributeError:
        print("Error parsing name of %s to create instance" % (row["Language"]))
    except SyntaxError as e:
        print("Syntax error:", e)


for code in langs:
    tokenizer = langs[code]["tokenizer"]
    text = "this is a test."
    tokens = tokenizer(text)
    print(type(tokens))
    for token in tokens:
        print(token)

#TODO: create a dict of tokenizers, use it to parse the texts
#TODO: investigate stopword and punctuation removal

#interesting links being used:
# https://spacy.io/api/tokenizer#_title
# https://spacy.io/usage/models
# https://www.w3schools.com/tags/ref_language_codes.asp






