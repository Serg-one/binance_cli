import json
import logging
import math
import os
import threading
import time
from dotenv import load_dotenv
from datetime import timedelta, datetime

from binance_api import Binance

logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.INFO,
                    # level=logging.DEBUG,
                    )
load_dotenv()
bot1 = Binance(
    API_KEY=os.getenv("API_KEY1"),
    API_SECRET=os.getenv('API_SECRET1'))

bot2 = Binance(
    API_KEY=os.getenv('API_KEY2'),
    API_SECRET=os.getenv('API_SECRET2'))

settings1 = dict(
    symbol='BTCUSDT',  # Пара для отслеживания
    strategy="Short",  # Стратегия - Long (повышение), Short (понижение)
    stop_loss_perc=0.5,  # % оставания от цены
    stop_loss_fixed=0,  # Изначальный stop-loss, можно установить руками нужную сумму, потом бот подтянет.
    # Можно указать 0, тогда бот высчитает, возьмет текущую цену и применит к ней процент
    amount=0.0015,  # Кол-во монет, которое планируем продать (в случае Long) или купить (в случае Short)
    # Если указываем Long, то альты для продажи (Например, продать 0.1 ETH в паре ETHBTC)
    # Если Short, то кол-во, на которое покупать, например купить на 0.1 BTC по паре ETHBTC
    working_time=30,  # Время работы в минутах до принудительного закрытия сделки
    no_profit_flag=True,  # Настройка закрывать ли убыточные сделки
    refund_flag=False,  # True, если запустили обратную сделку для возврата убытков
    start_rate=0,  # Начальный курс для обратной сделки (которую запускаем в случае убыточности в обратную сторону)
    multiplier_loss=3,  # Коэффициент увеличения объема сделки при запуске в обратную сторону, при убыточности
    coefficient=0.75,  # Коэффициент увеличения объема на каждом шаге для обратной сделки
    grid_step=1,  # Шаг в процентах для сетки графика, при котором увеличиваем объем на coefficient
    count_fails=0,  # Кол-во убыточных попыток
)

settings2 = dict(
    symbol='EOSUSDT',  # Пара для отслеживания
    strategy="Long",  # Стратегия - Long (повышение), Short (понижение)
    stop_loss_perc=0.5,  # % оставания от цены
    stop_loss_fixed=0,  # Изначальный stop-loss, можно установить руками нужную сумму, потом бот подтянет.
    # Можно указать 0, тогда бот высчитает, возьмет текущую цену и применит к ней процент
    amount=0.0015,  # Кол-во монет, которое планируем продать (в случае Long) или купить (в случае Short)
    # Если указываем Long, то альты для продажи (Например, продать 0.1 ETH в паре ETHBTC)
    # Если Short, то кол-во, на которое покупать, например купить на 0.1 BTC по паре ETHBTC
    working_time=30,  # Время работы в минутах до принудительного закрытия сделки
    no_profit_flag=True,  # Настройка закрывать ли убыточные сделки
    refund_flag=False,  # True, если запустили обратную сделку для возврата убытков
    start_rate=0,  # Начальный курс для обратной сделки (которую запускаем в случае убыточности в обратную сторону)
    multiplier_loss=3,  # Коэффициент увеличения объема сделки при запуске в обратную сторону, при убыточности
    coefficient=0.75,  # Коэффициент увеличения объема на каждом шаге для обратной сделки
    grid_step=1,  # Шаг в процентах для сетки графика, при котором увеличиваем объем на coefficient
    count_fails=0,  # Кол-во убыточных попыток
)

settings3 = dict(
    symbol='BNBUSDT',  # Пара для отслеживания
    strategy="Long",  # Стратегия - Long (повышение), Short (понижение)
    stop_loss_perc=0.5,  # % оставания от цены
    stop_loss_fixed=0,  # Изначальный stop-loss, можно установить руками нужную сумму, потом бот подтянет.
    # Можно указать 0, тогда бот высчитает, возьмет текущую цену и применит к ней процент
    amount=0.0015,  # Кол-во монет, которое планируем продать (в случае Long) или купить (в случае Short)
    # Если указываем Long, то альты для продажи (Например, продать 0.1 ETH в паре ETHBTC)
    # Если Short, то кол-во, на которое покупать, например купить на 0.1 BTC по паре ETHBTC
    working_time=30,  # Время работы в минутах до принудительного закрытия сделки
    no_profit_flag=True,  # Настройка закрывать ли убыточные сделки
    refund_flag=False,  # True, если запустили обратную сделку для возврата убытков
    start_rate=0,  # Начальный курс для обратной сделки (которую запускаем в случае убыточности в обратную сторону)
    multiplier_loss=3,  # Коэффициент увеличения объема сделки при запуске в обратную сторону, при убыточности
    coefficient=0.75,  # Коэффициент увеличения объема на каждом шаге для обратной сделки
    grid_step=1,  # Шаг в процентах для сетки графика, при котором увеличиваем объем на coefficient
    count_fails=0,  # Кол-во убыточных попыток
)

settings4 = dict(
    symbol='ADAUSDT',  # Пара для отслеживания
    strategy="Short",  # Стратегия - Long (повышение), Short (понижение)
    stop_loss_perc=0.5,  # % оставания от цены
    stop_loss_fixed=0,  # Изначальный stop-loss, можно установить руками нужную сумму, потом бот подтянет.
    # Можно указать 0, тогда бот высчитает, возьмет текущую цену и применит к ней процент
    amount=0.0015,  # Кол-во монет, которое планируем продать (в случае Long) или купить (в случае Short)
    # Если указываем Long, то альты для продажи (Например, продать 0.1 ETH в паре ETHBTC)
    # Если Short, то кол-во, на которое покупать, например купить на 0.1 BTC по паре ETHBTC
    working_time=30,  # Время работы в минутах до принудительного закрытия сделки
    no_profit_flag=True,  # Настройка закрывать ли убыточные сделки
    refund_flag=False,  # True, если запустили обратную сделку для возврата убытков
    start_rate=0,  # Начальный курс для обратной сделки (которую запускаем в случае убыточности в обратную сторону)
    multiplier_loss=3,  # Коэффициент увеличения объема сделки при запуске в обратную сторону, при убыточности
    coefficient=0.75,  # Коэффициент увеличения объема на каждом шаге для обратной сделки
    grid_step=1,  # Шаг в процентах для сетки графика, при котором увеличиваем объем на coefficient
    count_fails=0,  # Кол-во убыточных попыток
)


def set_timer(minutes: int):
    """ Устанавливаем таймер до закрытия сделки """
    timer = datetime.now() + timedelta(minutes=minutes)
    return timer


def rates_market_info(init_settings: dict, bot):
    """ Получаем текущие курсы по паре """
    current_rates = bot.futuresDepth(symbol=init_settings['symbol'], limit=5)
    bid = float(current_rates['bids'][0][0])
    ask = float(current_rates['asks'][0][0])
    return bid, ask


def refunding_try(current_settings: dict, start_rate: float):
    """ Меняем настройки для сделки в обратную сторону, согласно стратегии """
    new_settings = current_settings
    new_settings['amount'] = current_settings['amount'] * current_settings['multiplier_loss']
    new_settings['start_rate'] = start_rate
    new_settings['strategy'] = 'Short' if current_settings['strategy'] == "Long" else "Short"
    new_settings['refund_flag'] = True

    logging.info(f"Сделка по {new_settings['symbol']} убыточна. "
                 f"Запускаем сделку в обратную сторону: {datetime.now()}")

    timer = set_timer(new_settings['working_time'])
    logging.info("Обновляем таймер")

    new_settings['count_fails'] += 1
    logging.info(f"Количество убыточных сделок: {new_settings['count_fails']}")

    return new_settings, timer


def grid_step_set(amount: float, coefficient: float, start_rate: float, grid_step: float):
    """Увеличиваем объем сделки на коэффициент для шага"""
    amount += amount * coefficient
    start_rate += (start_rate * grid_step / 100)

    logging.info(f"Новый объем установлен {amount}")
    logging.info(f"Установлен новый шаг {start_rate}")
    return amount, start_rate


def create_order(side: str, settings: dict, bot: Binance):
    """ Создание ордера на основе текущего шага стратегии"""
    return bot.futuresCreateOrder(symbol=settings['symbol'],
                                  recvWindow=15000,
                                  side=side,
                                  type='MARKET',
                                  quantity=settings['amount'])


def write_to_file(file_for_data, data1, data2):
    """ Пишем данные для анализа в файл"""
    with open(file_for_data, "a+") as f:
        tick_time = datetime.now().strftime("%H:%M:%S")
        json.dump((tick_time, data1, data2), f)


def trade(init_settings: dict, file: str, bot: Binance, number: int):
    """Запускаем процесс трейлинга (по сути торгов) с заданными параметрами"""

    multiplier = -1 if init_settings['strategy'] == "Long" else 1

    # Получаем настройки пар с биржи
    symbols = bot.futuresExchangeInfo()['symbols']
    step_sizes = {symbol['symbol']: symbol for symbol in symbols}
    for symbol in symbols:
        for f in symbol['filters']:
            if f['filterType'] == 'LOT_SIZE':
                step_sizes[symbol['symbol']] = float(f['stepSize'])

    start_rate_bid, start_rate_ask = rates_market_info(init_settings, bot)

    timer = set_timer(init_settings['working_time'])

    while timer > datetime.now():
        try:
            bid, ask = rates_market_info(init_settings, bot)

            # Если играем на повышение, то ориентируемся на цены, по которым продают, иначе на цены, по которым покупают
            curr_rate = bid if init_settings['strategy'] == "Long" else ask

            # Если цена больше или равна установленному шагу и обратная сделка в процессе, доливаем с указанным
            # коэффициентом
            if init_settings['refund_flag'] and curr_rate >= init_settings['start_rate'] + \
                    (init_settings['start_rate'] * init_settings['grid_step'] / 100):
                init_settings['amount'], init_settings['start_rate'] = \
                    grid_step_set(init_settings['amount'], init_settings['coefficient'],
                                  init_settings['start_rate'], init_settings['grid_step'])

            if init_settings['stop_loss_fixed'] == 0:
                init_settings['stop_loss_fixed'] = (curr_rate / 100) * (
                        init_settings['stop_loss_perc'] * multiplier + 100)

            logging.info(
                f"Bot#{number}: Текущие курсы {init_settings['symbol']} bid {bid:0.8f}, ask {ask:0.8f}, выбрана {curr_rate:0.8f} "
                f"stop_loss {init_settings['stop_loss_fixed']:0.8f}")

            # Считаем, каким был бы stop-loss, если применить к нему %
            curr_rate_applied = (curr_rate / 100) * (init_settings['stop_loss_perc'] * multiplier + 100)

            if init_settings['strategy'] == "Long":
                # Выбрана стратегия Long, пытаемся продать монеты как можно выгоднее
                write_to_file(file, f"{curr_rate:0.8f}", f"{init_settings['stop_loss_fixed']:0.8f}")
                if curr_rate > init_settings['stop_loss_fixed']:
                    logging.info(f"Bot#{number}: Текущая цена выше цены Stop-Loss")
                    if curr_rate_applied > init_settings['stop_loss_fixed']:
                        logging.info(f"Bot#{number}: Пора изменять stop-loss, новое значение {curr_rate_applied:0.8f}")
                        init_settings['stop_loss_fixed'] = curr_rate_applied
                else:
                    # Текущая цена ниже или равна stop loss, продажа по рынку
                    profit_check = start_rate_bid - curr_rate - (curr_rate * 0.0002)
                    if profit_check > 0 or (profit_check <= 0 and init_settings['no_profit_flag']):
                        res = create_order("SELL", init_settings, bot)
                        logging.info(f'Bot#{number}: Результат создания ордера', res)
                        if 'orderId' in res:
                            # Создание ордера прошло успешно, выход
                            logging.info(f"Bot#{number}: Сделка по паре {res['symbol']} {init_settings['strategy']} "
                                         f"успешно закрыта по цене {res['price']}")
                            init_settings['count_fails'] = 0
                            break
                    else:
                        # Запускаем сделку в обратную сторону, согласно стратегии
                        init_settings, timer = refunding_try(init_settings, curr_rate)

            else:
                write_to_file(file, f"{curr_rate:0.8f}", f"{init_settings['stop_loss_fixed']:0.8f}")
                # Выбрана стратегия Short, пытаемся купить монеты как можно выгоднее
                if curr_rate < init_settings['stop_loss_fixed']:
                    logging.info(f"Bot#{number}: Текущая цена ниже stop-loss")
                    if curr_rate_applied < init_settings['stop_loss_fixed']:
                        logging.info(f"Bot#{number}: Пора изменять stop-loss, новое значение {curr_rate_applied:0.8f}")
                        init_settings['stop_loss_fixed'] = curr_rate_applied
                else:
                    # Цена поднялась выше Stop-Loss, Покупка по рынку
                    quantity = math.floor(
                        (init_settings['amount'] / curr_rate) * (1 / step_sizes[init_settings['symbol']])) / (
                                       1 / step_sizes[init_settings['symbol']])
                    logging.info(f"Bot#{number}: Цена поднялась выше Stop-Loss, Покупка по рынку, "
                                 f"кол-во монет {quantity:0.8f}")
                    profit_check = start_rate_ask - curr_rate - (curr_rate * 0.0002)
                    if profit_check > 0 or (profit_check <= 0 and init_settings['no_profit_flag']):
                        res = create_order("BUY", init_settings, bot)
                        logging.info(f"Bot#{number}: Результат создания ордера", res)
                        if 'orderId' in res:
                            # Создание ордера прошло успешно, выход
                            logging.info(f"Bot#{number}: Сделка по паре {res['symbol']} {init_settings['strategy']} "
                                         f"успешно закрыта по цене {res['price']}")
                            init_settings['count_fails'] = 0
                            break
                    else:
                        # Запускаем сделку в обратную сторону, согласно стратегии
                        init_settings, timer = refunding_try(init_settings, curr_rate)

        except Exception as e:
            logging.error(e)
        time.sleep(0.5)


if __name__ == "__main__":
    settings = [settings1, settings2, settings3, settings4]
    threads = []
    bots = [bot1, bot2]
    bot = bots[0]

    for i in range(len(settings)):
        file_name = f"data{i+1}.json"
        t = threading.Thread(target=trade, args=(settings[i], file_name, bot, i+1))
        t.start()
        threads.append(t)
        bot = bots[1] if bot == bots[0] else bots[0]

    for i in range(len(threads)):
        threads[i].join()
