import requests
import bs4


response = requests.get('https://www.netflix.com/ar/title/70143836')

soup = bs4.BeautifulSoup(response.text, 'html.parser')


def info():
    print("Titulo:", soup.h1.text)
    print("Fecha de publicacion:", soup.find("span", {"data-uia": "item-year"}).text)
    print("Edad minima recomendada:", soup.find("span", {"class": "maturity-number"}).text)
    print("Cantidad de temporadas:", soup.find("span", {"class": "test_dur_str"}).text)
    print("Genero:", soup.find("a", {"data-uia": "item-genre"}).text)
    print("Sinopsis:", soup.find("div", {"data-uia": "title-info-synopsis"}).text)
    print("Protagonistas:", soup.find("span", {"data-uia": "info-starring"}).text)
    if soup.find("span", {"data-uia": "info-creators"}) is not None:
        print("Creado por:", soup.find("span", {"data-uia": "info-creators"}).text)
    else:
        pass
    if soup.find("div", {"data-uia": "hook-text"}) is not None:
        print("Info:", soup.find("div", {"data-uia": "hook-text"}).text)
    else:
        pass


# Crea una lista con el valor que contiene el tag
def list_maker(elem_list):
    values = [val.text for val in elem_list]
    value_list = []
    for item in range(len(elem_list)):
        value_list.append(values[item])
    return value_list


# Crea un mapa dependiendo de 2 listas
def map_generator(elem_list, second_list):
    my_map = {}
    for chapter in range(len(elem_list)):
        my_map[elem_list[chapter]] = second_list[chapter]
    return my_map


def separator_map(elem_list, second_list):
    values = elem_list
    values_2 = second_list
    chapter_list = []
    for elem in range(len(elem_list)):
        chapter_list.append({"capitulos": map_generator(values[elem], values_2[elem])})

    return chapter_list


def object_list(first_list, second_list, third_list):
    general_list = []
    if len(first_list) == len(second_list):
        for number in range(len(second_list)):
            general_list.append([{first_list[number]: second_list[number]}, third_list[number]])

    else:
        general_list.append([{"Temporada 1": second_list[0]}, third_list[0]])


    return general_list


def season_list(tag, key, value, second_tag):
    season_select = soup.find(tag, {key: value})
    season_option_list = season_select.find_all(second_tag)
    return list_maker(season_option_list)


# Seleccionamos todas las sinopsis
def synopsis_list(tag, key, value, second_tag, second_key, second_value):
    seasons_and_episodes_list_container = soup.find(tag, {key: value})
    season_synopsis_list = seasons_and_episodes_list_container.find_all(second_tag, {second_key: second_value})
    return list_maker(season_synopsis_list)


def chapter_syn_list(tag, key, value, second_tag, second_key, second_value, third_tag, third_key, third_value):
    chapter_syn_list = soup.find_all(tag, {key: value})
    synopsis_list = []
    title_list = []
    for season in range(len(chapter_syn_list)):
        synopsis_list.append(list_maker(chapter_syn_list[season].find_all(third_tag, {third_key: third_value})))
        title_list.append(list_maker(chapter_syn_list[season].find_all(second_tag, {second_key: second_value})))

    return separator_map(synopsis_list, title_list)


info()
print(object_list(season_list("select", "id", "undefined-select", "option"),
                  synopsis_list("div", "id", "seasons-and-episodes-list-container", "p", "data-uia", "season-synopsis"),
                  chapter_syn_list("div", "class", "episodes-container", "p", "data-uia", "episode-synopsis", "h3",
                                   "data-uia", "episode-title")))
