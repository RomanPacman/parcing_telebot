HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
       ' Chrome/86.0.4240.185 YaBrowser/20.11.2.78 Yowser/2.5 Safari/537.36', 'accept': '*/*'}



class ReferenceSite:
    def __init__(self, urls):
        self.urls = urls

Realt_by = ReferenceSite('https://realt.by/sale/flats/')
Domovita_by = ReferenceSite('https://domovita.by/minsk/houses/sale')



