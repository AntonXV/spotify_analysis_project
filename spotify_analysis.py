import pandas as pd
from datetime import datetime
from typing import Union, List, Dict
import json
import matplotlib.pyplot as plt


def format_date(date_row: str) -> datetime:
    '''
    Функция для приведения даты в единый формат
    ---
    * преобразует строковую дату из датафрейма в формате '(d)d month yyyy'
        или '(d)d.month.yy' в формат datetime.datetime 'yyyy-mm-dd'
    ----------
    Аргументы:
    date_row: str – строка с датой из датафрейма
    -------------------
    Функция возвращает:
    formatted_date: datetime.datetime - отформатированная дата
    '''

    date_temp: List[str] = []

    # Разбиение строковой даты на элементы в зависимости от формата.
    if '.' in date_row:
        date_temp = date_row.split('.')
    else:
        date_temp = date_row.split()

    # Приведение форматов дня и года к единому.
    if len(date_temp[0]) == 1:
        date_temp[0] = '0' + date_temp[0]
    if len(date_temp[2]) == 2:
        date_temp[2] = '20' + date_temp[2]

    # Сборка элементов даты в строку.
    date_row = ' '.join(date_temp)
    # Преобразование строковой даты в формат datetime.datetime.
    formatted_date: datetime = datetime.strptime(date_row, '%d %B %Y')

    return formatted_date


def get_sheeran_songs(df_song_artist: pd.DataFrame) -> List[str]:
    '''
    Функция для извлечения из датафрейма песен Ed Sheeran
    ---
    * извлекает из исходного датафрейма все песни,
        которые исполняет Ed Sheeran (в том числе с кем-то)
    ----------
    Аргументы:
    df_song_artist: pd.DataFrame – столбцы 'Song' и 'Artist' из датафрейма
    -------------------
    Функция возвращает:
    sheeran_songs: List[str] - список песен Ed Sheeran
    '''

    # Поиск строк в столбце 'Artist', содержащих 'Ed Sheeran',
    # выбор соответствующих строк в столбце 'Song',
    # преобразование результата в список.
    sheeran_songs: List[str] = df_song_artist.loc[
        df_song_artist['Artist'].str.contains('Ed Sheeran'), 'Song'
        ].to_list()
    return sheeran_songs


def get_oldest_songs(df_song_reldate: pd.DataFrame) -> List[str]:
    '''
    Функция для извлечения из датафрейма трех самых старых песен
    ----------
    Аргументы:
    df_song_reldate: pd.DataFrame – столбцы 'Song' и
        'Release Date' из датафрейма
    -------------------
    Функция возвращает:
    oldest_songs: List[str] - список трех самых старых песен
    '''

    # Сортировка по возрастанию по столбцу 'Release Date'.
    df_song_reldate_sorted: pd.DataFrame = df_song_reldate.sort_values(
        by='Release Date'
        )
    # Выбор столбца 'Song', отображение первых трех строк,
    # преобразование результата в список.
    oldest_songs: List[str] = df_song_reldate_sorted['Song'].head(3).to_list()
    return oldest_songs


def format_streams(streams_row: str) -> float:
    '''
    Функция для преобразования формата кол-ва прослушиваний
    ---
    * преобразует строку с кол-вом прослушиваний из датафрейма
        в число с плавающей точкой
    ----------
    Аргументы:
    streams_row: str – строка с кол-вом прослушиваний из датафрейма
    -------------------
    Функция возвращает:
    formatted_streams: float - кол-во прослушиваний в формате
        числа с плавающей точкой
    '''

    formatted_streams: float = float(streams_row.replace(',', '.'))
    return formatted_streams


def get_artists_list(artists_series: pd.Series) -> List[str]:
    '''
    Функция для получения списка уникальных исполнителей
    ----------
    Аргументы:
    artists_series: pd.Series – набор исполнителей из датафрейма,
        включая коллаборации ('x and y') и участия ('x feauturing y')
    -------------------
    Функция возвращает:
    result: List[str] - список уникальных исполнителей
    '''

    result: List[str] = []

    for artist in artists_series:
        # Замена 'feauturing' на 'and' в участиях ('x feauturing y').
        if 'featuring' in artist:
            artist = artist.replace('featuring', 'and')
        # Разделение исполнителей по 'and' и добавление их в список.
        if 'and' in artist:
            result.extend(artist.split(' and '))
        # Добавление соло-исполнителей в список.
        else:
            result.append(artist)

    # Получение списка уникальных исполнителей.
    result = list(set(result))
    return result


def get_artist_streams(df_st_art: pd.DataFrame) -> Dict[str, float]:
    '''
    Функция для извлечения из датафрейма данных о прослушиваниях
    ---
    * извлекает из исходного датафрейма данные о суммарных прослушиваниях
        для каждого уникального исполнителя: все исполнители
        в коллаборациях ('x and y') и участиях ('x featuring y')
        считаются уникальными, и прослушивания засчитываются
        каждому исполнителю в полном объеме
    ----------
    Аргументы:
    df_st_art: pd.DataFrame – столбцы 'Streams (Billions)' и
        'Artist' из датафрейма
    -------------------
    Функция возвращает:
    artist_streams_dict_sorted: Dict[str, float] - словарь вида
        [исполнитель: кол-во_прослушиваний]
    '''

    # Создание копии датафрейма для последующих преобразований.
    df_copy = df_st_art.copy()

    # Преобразование формата кол-ва прослушиваний.
    df_copy['Streams (Billions)'] = df_copy['Streams (Billions)'].apply(
        format_streams
        )

    # Получение списка уникальных исполнителей.
    artists_list: List[str] = get_artists_list(df_copy['Artist'])

    # Создание словаря[исполнитель: кол-во_прослушиваний].
    artist_streams_dict: Dict[str, float] = {}
    for artist in artists_list:
        # Поиск строк в столбце 'Artist', содержащих текущий artist,
        # выбор соответствующих строк в столбце 'Streams (Billions)',
        # суммирование кол-ва прослушиваний.
        total_streams: float = df_copy.loc[
            df_copy['Artist'].str.contains(artist), 'Streams (Billions)'
            ].sum()
        # Округление кол-ва прослушиваний и запись значения в словарь
        # по ключу исполнителя.
        artist_streams_dict[artist] = round(total_streams, 3)

    # Сортировка словаря по исполнителям.
    artist_streams_dict_sorted: Dict[str, float] = {}
    sorted_keys: List[str] = sorted(artist_streams_dict.keys())
    for key in sorted_keys:
        artist_streams_dict_sorted[key] = artist_streams_dict[key]

    return artist_streams_dict_sorted


def build_hist(df_hist: pd.DataFrame):
    '''
    Функция для построения гистограммы
    ---
    * строит гистограмму зависимости количества популярых песен
         от года выпуска
    ----------
    Аргументы:
    df_hist: pd.DataFrame – датафрейм
    '''

    # Создание столбца 'Release Year', содержащего год релиза песни.
    df_hist['Release Year'] = df_hist['Release Date'].apply(
        lambda date: date.year
        )
    # Группировка по столбцу 'Release Year' с подсчетом кол-ва песен.
    df_hist = df_hist.groupby('Release Year').agg('Song').count().reset_index()
    # Сортировка по возрастанию по столбцу 'Release Year'.
    df_hist.sort_values(by='Release Year', inplace=True)
    # Преобразование datetime-значений в столбце 'Release Year'
    # в строковые для последующего корректного построения гистограммы.
    df_hist['Release Year'] = df_hist['Release Year'].apply(
        lambda year: str(year)
        )

    # Построение гистограммы.
    plt.figure(figsize=(8, 6))
    plt.bar(df_hist['Release Year'], df_hist['Song'],
            color='#1DB954', edgecolor='black')

    plt.xticks(rotation=90)
    plt.yticks(range(0, max(df_hist['Song']) + 1, 1))
    plt.grid(axis='y', alpha=0.3)

    plt.title(
        'Кол-во популярных песен в Spotify в зависимости от года выпуска',
        color='black', fontweight='bold'
        )
    plt.xlabel('Год выпуска')
    plt.ylabel('Кол-во популярных песен')

    plt.tight_layout()
    plt.savefig('spotify_songs_by_year.png')


def main():
    # Считывание датасета в pandas.DataFrame
    df = pd.read_csv('spotify_songs_top_100.csv')

    # Преобразование формата даты в соответствующем столбце датафрейма.
    df['Release Date'] = df['Release Date'].apply(format_date)

    # Анализ данных датафрейма.
    var_alias = Dict[str, Union[List[str], Dict[str, float]]]
    analysis_results: var_alias = {}
    # Результаты записываются в итоговую переменную-словарь.
    analysis_results['Ed Sheeran songs'] = get_sheeran_songs(
        df[['Song', 'Artist']]
        )
    analysis_results['3 oldest songs'] = get_oldest_songs(
        df[['Song', 'Release Date']]
        )
    analysis_results['Artists total streams (Billions)'] = get_artist_streams(
        df[['Streams (Billions)', 'Artist']]
        )

    # Запись результатов анализа в json-файл.
    with open('spotify_analysis_results.json', 'w') as file:
        json.dump(analysis_results, file, indent=4)

    # Создание гистограммы.
    build_hist(df)

    print('Analysis completed')


if __name__ == '__main__':
    main()
