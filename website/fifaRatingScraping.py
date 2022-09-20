# Import packages
from bs4 import BeautifulSoup
import requests

rating = '0'

# A method to get the price of the cheapest player with a particular rating by web scraping from a FIFA database
# Input: An string representing a particular rating
# Output: An integer corresponding to the cheapest price found for the input rating
def getCheapest(inputRating):

    # Sets the search to players with the rating based on the input
    set_rating(inputRating)

    # Gets the URL of players with the appropriate rating based on the input
    url = 'https://www.futwiz.com/en/fifa22/players?page=0&order=bin&s=asc&minprice=150&minrating={}&maxrating={}' \
        .format(inputRating, inputRating)
    html_text = requests.get(url).text

    # Organizes the html source code using BeautifulSoup
    soup = BeautifulSoup(html_text, 'lxml')

    # Find the source code responsible for the columns that contains the data of the first player listed
    # corresponding to the cheapest player for that particular rating
    tag = soup.find("tr", {"class": "table-row"})

    counter = 0
    lowestPrice = 0
    for td_tag in tag.find_all('td'):
        if counter == 4:
            lowestPrice = td_tag.text
            break
        else:
            td_tag.nextSibling
            counter = counter + 1

    # Format the string values into int
    # Remove white spaces from the string
    lowestPrice = lowestPrice.replace(' ', '')

    # Replace 'K' as in thousand with '000'
    lowestPrice = lowestPrice.replace('K', '000')

    # Replace 'M' as in million with '000000'
    lowestPrice = lowestPrice.replace('M', '000000')

    # Replace '.', which has become redundant after the previous two steps, with ''
    if lowestPrice.__contains__('.'):
        lowestPrice = lowestPrice[:-2]
        lowestPrice = lowestPrice.replace('.', '')

    # Convert the string into int
    lowestPrice = int(lowestPrice)
    return lowestPrice

def set_rating(inputRating2):

    # Condition if input type is int
    if isinstance(inputRating2, int):
        if (inputRating2 < 47) or (inputRating2 > 99):
            raise ValueError("Rating input should be between 47 and 99 based on the ratings in FIFA 22!")
        rating = str(inputRating2)

    else:
        raise ValueError("Rating input should be of type int")
