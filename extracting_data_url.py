from bs4 import BeautifulSoup
import requests

# page = requests.get("https://forecast.weather.gov/MapClick.php?lat=37.7772&lon=-122.4168")
# soup = BeautifulSoup(page.content, 'html.parser')
# seven_day = soup.find(id="seven-day-forecast")
# forecast_items = seven_day.find_all(class_="tombstone-container")
# tonight = forecast_items[0]
# print(tonight.prettify())

page=requests.get('https://github.com/LibrePDF/OpenPDF/blob/master/openpdf/src/main/java/com/lowagie/text/alignment/HorizontalAlignment.java')
soup = BeautifulSoup(page.content, 'html.parser')
code = soup.find('table',class_='highlight tab-size js-file-line-container js-code-nav-container js-tagsearch-file').find_all('tr',recursive=False)
text=""
for i,row in enumerate(code):
    text=text+(str(row.text))
    #text=row.find('tr').get_text()
    #print(str(i)+str(row.text))   
    #   
with open('./text.txt','w') as f:
    f.write(text)
#print(text)

