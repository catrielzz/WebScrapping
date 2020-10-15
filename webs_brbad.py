import requests
import bs4

response = requests.get('https://www.netflix.com/ar/title/70143836')

soup = bs4.BeautifulSoup(response.text, 'html.parser')
print("Titulo:", soup.h1.text)
print("Fecha de publicacion:", soup.find("span", {"data-uia": "item-year"}).text)
print("Edad minima recomendada:", soup.find("span", {"class": "maturity-number"}).text)
print("Cantidad de temporadas:", soup.find("span", {"class": "test_dur_str"}).text)
print("Genero:", soup.find("a", {"data-uia": "item-genre"}).text)
print("Sinopsis:", soup.find("div", {"data-uia": "title-info-synopsis"}).text)
print("Protagonistas:", soup.find("span", {"data-uia": "info-starring"}).text)
print("Creado por:", soup.find("span", {"data-uia": "info-creators"}).text)
print("Info:", soup.find("div", {"data-uia": "hook-text"}).text)


def list_maker(elem_list):
    values = [val.text for val in elem_list]
    value_list = []
    for item in range(len(elem_list)):
        value_list.append(values[item])
    return value_list


def map_generator(elem_list, second_list):
    my_map = {}
    for chapter in range(len(elem_list)):
        my_map[elem_list[chapter]] = second_list[chapter]
    return my_map


def separator_map(elem_list, second_list):
    values = elem_list
    values_2 = second_list

    season_one_titles = values[0:7]
    season_two_titles = values[8:21]
    season_three_titles = values[22:35]
    season_four_titles = values[36: 49]
    season_five_titles = values[50: 66]

    season_one_synapsis = values_2[0:7]
    season_two_synapsis = values_2[8:21]
    season_three_synapsis = values_2[22:35]
    season_four_synapsis = values_2[36: 49]
    season_five_synapsis = values_2[50: 66]

    chapter_list = [{"capitulos": map_generator(season_one_titles, season_one_synapsis)},
                    {"capitulos": map_generator(season_two_titles, season_two_synapsis)},
                    {"capitulos": map_generator(season_three_titles, season_three_synapsis)},
                    {"capitulos": map_generator(season_four_titles, season_four_synapsis)},
                    {"capitulos": map_generator(season_five_titles, season_five_synapsis)}]

    return chapter_list


def object_list(first_list, second_list, third_list):
    season_1 = [{first_list[0]: second_list[0]}, third_list[0]]
    season_2 = [{first_list[1]: second_list[1]}, third_list[1]]
    season_3 = [{first_list[2]: second_list[2]}, third_list[2]]
    season_4 = [{first_list[3]: second_list[3]}, third_list[3]]
    season_5 = [{first_list[4]: second_list[4]}, third_list[4]]

    general_list = [season_1, season_2, season_3, season_4, season_5]
    return general_list


# Seleccionamos titulos de las temporadas
season_select = soup.find("select", {"id": "undefined-select"})
season_option_list = season_select.find_all("option")
season_list = list_maker(season_option_list)


# Seleccionamos todas las synopsis
seasons_and_episodes_list_container = soup.find("div", {"id": "seasons-and-episodes-list-container"})
season_synopsis_list = seasons_and_episodes_list_container.find_all("p", {"data-uia": "season-synopsis"})
synopsis_list = list_maker(season_synopsis_list)


# Seleccionamos todos los capitulos
episode_name_list = seasons_and_episodes_list_container.find_all("h3", {"data-uia": "episode-title"})
episode_list = list_maker(episode_name_list)


# Seleccionamos todas las sinapsis
episode_synapsis_name_list = seasons_and_episodes_list_container.find_all("p", {"data-uia": "episode-synopsis"})
episode_synapsis_list = list_maker(episode_synapsis_name_list)


# Mapa de episodios y synapsis
chapters_list = separator_map(episode_list, episode_synapsis_list)

print(object_list(season_list, synopsis_list, chapters_list))

