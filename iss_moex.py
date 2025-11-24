import requests
from urllib import parse


def __query(method, kwargs):
    """ Отправляю запрос к ISS MOEX """
    try:
        url = f"https://iss.moex.com/iss/{str(method)}.json"
        if kwargs: url += "?" + parse.urlencode(kwargs)
#        print(f"URL: {url}")
        r = requests.get(url)
        r.encoding = 'utf-8'
        j = r.json()
        return j

    except Exception as e:
        print(f"__query() ERROR {str(e)}")
        return None


def __flatten(j: dict, blockname: str):
    """ Собираю двумерный массив (словарь) """
    return [{k: r[i] for i, k in enumerate(j[blockname]['columns'])} for r in j[blockname]['data']]


def get_list_all_name_futures():
    """Получить список ticker торгуемых в настоящий момент

        Args:
            void

        Returns:
            (list[str, ...]): список ticker торгуемых в настоящий момент
    """
    list_secid = []
    # Получить таблицу фьючерсных контрактов
    all_table = __query("engines/futures/markets/forts/securities", None)
    for cur_data in all_table['securities']['data']:
        list_secid.append(cur_data[0])
    return list_secid


def get_list_definite_futures(prefix_ftrs):
    """Получить список ticker начинающихся с указанного префикса

        Args:
            prefix_ftrs (str): префикс фьючерса для получения торгуемых ticker

        Returns:
            (list[str, ...]): список ticker торгуемых в настоящий момент начинающихся с указанного префикса
    """
    list_ftrs = []
    list_all_secid = get_list_all_name_futures()
    for secid in list_all_secid:
        if secid.lower().startswith(prefix_ftrs.lower()):
            list_ftrs.append(secid)
    return list_ftrs


def get_list_current_cny_futures():
    """Получить список ticker фьючерса CNY торгующихся в настоящий момент

            Args:
                void

            Returns:
                (list[str, ...]): список ticker фьючерса CNY торгующихся в настоящий момент
    """
    return get_list_definite_futures("CR")


def get_data_future(ticker):
    """Получить данные указанного фьючерса

        Args:
            ticker (str): тикер фьючерса для получения данных

        Returns:
            (dict{'ticker': 'str', 'minstep': 'str', 'lasttradedate': 'str'}): формат возвращаемых данных
    """
    SECID = 0
    MINSTEP = 6
    LASTTRADEDATE = 7
    data_ticker = {}

    full_data_ticker = __query(f"engines/futures/markets/forts/securities/{ticker}", None)['securities']['data']
    data_ticker['ticker'] = full_data_ticker[0][SECID]
    data_ticker['minstep'] = str(full_data_ticker[0][MINSTEP])
    data_ticker['lasttradedate'] = full_data_ticker[0][LASTTRADEDATE]
    return data_ticker


def __get_candles(market, ticker, start_date=None, finish_date=None, interval='1m'):
    """Получить данные свечей за указанный период из MOEX

        Args:
            market (str): рынок на котором торгуется запрашиваемый инструмент ('future', 'stock')
            ticker (str): тикер запрашиваемого инструмента ('CRH5', 'AFKS')
            start_date (str): Дата и время, начиная с которой необходимо начать выводить данные. Формат: ГГГГ-ММ-ДД ЧЧ:ММ:СС
            finish_date (str): Дата и время, до которой необходимо выводить данные. Формат: ГГГГ-ММ-ДД ЧЧ:ММ:СС
                               Если значение не указано, то до последней даты ведения торгов.
            interval: временной интервал свечи (1m, 5m, 10m, 60m, 1d, 1w, 1m или 1y)

        Returns:
            (list[{}]): список словарей запрошенных свечей
    """
    table_interval = {'1m': '1', '5m': '1', '10m': '10', '60m': '60', '1d': '24', '1w': '7', '1mth': '31', '1y': '4'}
    kwargs = {}
    if market == 'future':
        iss_queries = f"engines/futures/markets/forts/securities/{ticker}/candles"
    elif market == 'stock':
        iss_queries = f"engines/stock/markets/shares/securities/{ticker}/candles"
    else:
        return list()

    if start_date is not None:
        kwargs['from'] = start_date
    if finish_date is not None:
        kwargs['till'] = finish_date
    kwargs['interval'] = table_interval[interval]

    return __flatten(__query(iss_queries, kwargs), "candles")


def get_candles_futures(ticker, start_date=None, finish_date=None, interval='1m'):
    """Получить данные свечей фьючерса за указанный период из MOEX

        Args:
            ticker (str): тикер запрашиваемого инструмента ('CRH5')
            start_date (str): Дата и время, начиная с которой необходимо начать выводить данные. Формат: ГГГГ-ММ-ДД ЧЧ:ММ:СС
            finish_date (str): Дата и время, до которой необходимо выводить данные. Формат: ГГГГ-ММ-ДД ЧЧ:ММ:СС
                               Если значение не указано, то до последней даты ведения торгов.
            interval: временной интервал свечи (1m, 5m, 10m, 60m, 1d, 1w, 1m или 1y)

        Returns:
            (list[{}]): список словарей запрошенных свечей
    """
    return __get_candles('future', ticker, start_date, finish_date, interval)


def get_candles_stock(ticker, start_date=None, finish_date=None, interval='1m'):
    """Получить данные свечей акций за указанный период из MOEX

        Args:
            ticker (str): тикер запрашиваемого инструмента ('AFKS')
            start_date (str): Дата и время, начиная с которой необходимо начать выводить данные. Формат: ГГГГ-ММ-ДД ЧЧ:ММ:СС
            finish_date (str): Дата и время, до которой необходимо выводить данные. Формат: ГГГГ-ММ-ДД ЧЧ:ММ:СС
                               Если значение не указано, то до последней даты ведения торгов.
            interval: временной интервал свечи (1m, 5m, 10m, 60m, 1d, 1w, 1m или 1y)

        Returns:
            (list[{}]): список словарей запрошенных свечей
    """
    return __get_candles('stock', ticker, start_date, finish_date, interval)
