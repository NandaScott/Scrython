import scrython
import requests
import time

IMAGE_PATH = './' # You can replace this with whatever path

def get_set_code():
    all_sets = scrython.sets.Sets()
    for i, set_object in enumerate(all_sets.data()):
        print(i, all_sets.data(i, "name"))

    choice = int(input("Select your set by number: "))

    code = all_sets.data(choice, "code")

    return code

def save_image(path, url, name):
    response = requests.get(url)

    with open('{}{}.png'.format(path, name), 'wb') as f:
        f.write(response.content)

def get_all_pages(set_code):
    page_count = 1
    all_data = []
    while True:
        time.sleep(0.5)
        page = scrython.cards.Search(q='e:{}'.format(set_code), page=page_count)
        all_data = all_data + page.data()
        page_count += 1
        if not page.has_more():
            break

    return all_data

def get_all_cards(card_array):
    card_list = []
    for card in card_array:
        time.sleep(0.5)
        id_ = card['id']
        card = scrython.cards.Id(id=id_)
        card_list.append(card)

    return card_list

code = get_set_code()
card_list = get_all_pages(code)
card_list_objects = get_all_cards(card_list)

for card in card_list_objects:
    time.sleep(0.1)
    save_image(IMAGE_PATH, card.image_uris(0, 'normal'), card.name())