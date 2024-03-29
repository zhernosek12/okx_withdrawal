import asyncio
import random
import time
import ccxt

from loguru import logger
from pathlib import Path

from src.helper import load_data, print_logo, fee_network
from src.config import load_config


async def run(filename: str):
    print_logo()

    config = load_config(filename)

    okx_account = ccxt.okx({
        'apiKey': config.okx_key,
        'secret': config.okx_secret,
        'password': config.okx_password
    })

    root_path = Path(__file__).resolve().parent.parent
    wallets_path = root_path / config.filename

    wallets = load_data(wallets_path)

    if config.shuffle:
        random.shuffle(wallets)

    logger.info("Начинаем вывод с OKX")

    for data in wallets:
        if data == "":
            continue

        amount = round(random.uniform(
            config.amount_withdraw.from_value,
            config.amount_withdraw.to_value
        ), 7)

        datas = data.split(";")
        if len(datas) == 2:
            address = datas[0]
            amount = round(float(datas[1]), 7)
        else:
            address = datas[0]

        while True:
            try:
                fees = okx_account.fetch_deposit_withdraw_fees([config.symbol])
                fee_network_name = fee_network(config.symbol, config.network, fees)
                fee = float(str(fees[config.symbol]["networks"][fee_network_name]["withdraw"]["fee"]))
            except Exception as e:
                logger.info(f"Ошибка при получении комисси за вывод, берем значение из файла конфига")
                fee = float(config.withdraw_fee)

            try:
                logger.info(f"Выводим: {amount} {config.symbol} в сети {config.network} на {address}")
                logger.info(f"Комиссия за вывод в сети {config.network} составляет {fee} {config.symbol}")

                sleep_after_withdraw = random.randint(
                    config.sleep_after_withdraw.from_value,
                    config.sleep_after_withdraw.to_value
                )

                okx_account.withdraw(config.symbol, amount + fee, address,
                                     params={'fee': fee, 'chain': config.symbol + "-" + config.network,
                                             'pwd': config.okx_password})

                logger.success(f"Успешно {address} | {amount} {config.symbol} в сети {config.network}.")

                logger.info(f"Ждем {sleep_after_withdraw} сек.")
                time.sleep(sleep_after_withdraw)

                break

            except Exception as e:
                logger.error("Ошибка: " + str(e))
                time.sleep(30)

    logger.info("Завершили вывод с OKX")


def main(filename: str):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(filename))
