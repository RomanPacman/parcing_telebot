import requests
from bs4 import BeautifulSoup
from .data import FlatInfo
from .settings import Realt_by, HEADERS
import re
import PySimpleGUI as sg
from datetime import datetime
from . import db_client


def save_flat(flat):
    db_client.insert_flat_realt(flat)


def get_page_content(url, parcer_name='html.parser'):
    resp = requests.get(url, headers=HEADERS)
    html = BeautifulSoup(resp.content, parcer_name)
    return html


def get_last_page(url):
    list_pages = get_page_content(url).find('select', class_='form-control').find_all('option')[-1].text
    return int(list_pages) - 1


def get_all_flats_links(url, page_from=0, page_to=1):
    flat_links = []
    while page_from < page_to:
        sg.one_line_progress_meter('Получение данных', page_from + 1, page_to)
        html = get_page_content(f'{url}?page={page_from}')
        all_cards = html.find_all('div', class_="teaser-tile teaser-tile-right")
        for link in all_cards:
            flat_links.append(link.find('a', href=True, class_='teaser-title')['href'])
        page_from += 1
    return flat_links


def get_flats_cards_in_page(url):
    page = get_page_content(url)
    all_cards = page.find_all('div', class_='listing-item')
    return all_cards


def get_info_from_card(card):
    link = card.find('div', class_='teaser-tile-left').find('a', class_='image')['href']
    raw_price = card.find('div', class_='desc-mini-bottom').find('strong')
    if raw_price is not None:
        price = int(re.sub('[^0-9]', '', raw_price.text.strip()))
    else:
        price = 0
    title = card.find('div', class_='desc').find('a').text.strip()
    description = card.find('div', class_='info-text info-more').text.strip()
    try:
        date = card.find('div', class_='info-mini').find_all('span')[-2].text.strip()
        date = datetime.strptime(date, '%d.%m.%Y')
    except:
        date = datetime.now()
    preview = card.find('div', class_='teaser-tile-left').find('img')['src']
    floor = re.sub('[^0-9/]', '',
                   card.find('div', class_='info-large').find_all('span', class_=None)[2].text.strip())
    room = int(re.sub('[^0-9]', '',
                      card.find('div', class_='info-large').find_all('span', class_=None)[0].text.strip()))
    apartment_area = re.sub('\s\D\d', '',
                            card.find('div', class_='info-large').find_all('span', class_=None)[
                                1].text.strip())
    address = card.find('div', class_='location color-graydark').text.strip()
    views = int(card.find('div', class_='info-mini').find('span', class_='views').text.strip())
    flat = FlatInfo(link=link,
                    reference=Realt_by.urls,
                    price=price,
                    title=title,
                    description=description,
                    date=date,
                    preview=preview,
                    floor=floor,
                    room=room,
                    apartment_area=apartment_area,
                    phone='Не опознан',
                    address=address,
                    views=views
                    )
    return flat




def get_new_or_old_flat(card, only_new=True):
    try:
        link = card.find('div', class_='teaser-tile-left').find('a', class_='image')['href']
        if only_new:
            if link not in db_client.select_links():
                return get_info_from_card(card)
            else:
                pass
        else:
            return get_info_from_card(card)
    except:
        pass


def get_flats(url, first_page=0, last_page=1, only_new=True):
    numbers = 0
    flats = []
    while first_page < last_page:
        sg.one_line_progress_meter(f'Сохранение страниц', first_page + 1, last_page)
        for card in get_flats_cards_in_page(f'{url}?page={first_page}'):
            if get_new_or_old_flat(card, only_new=only_new) is not None:
                flats.append(get_new_or_old_flat(card, only_new=only_new))
                save_flat(flats[-1])
                numbers += 1
        first_page += 1
    return numbers, flats
