import asyncio
import random
import time
import ccxt

from loguru import logger
from pathlib import Path

from src.helper import load_data, print_logo
from src.config import config


async def run():
    try:
        print_logo()

        okx_account = ccxt.okx({
            'apiKey': config.okx_key,
            'secret': config.okx_secret,
            'password': config.okx_password
        })

        root_path = Path(__file__).resolve().parent.parent
        wallets_path = root_path / "wallets.txt"

        wallets = load_data(wallets_path)

        if config.shuffle:
            random.shuffle(wallets)

        logger.info("Начинаем вывод с OKX")
        for address in wallets:
            amount = round(random.uniform(
                config.amount_withdraw.from_value,
                config.amount_withdraw.to_value
            ), 7)

            logger.info(f"Выводим: {amount} {config.symbol} в сети {config.network} на {address}")

            fees = okx_account.fetch_deposit_withdraw_fees([config.symbol])
            fee = float(str(fees["ETH"]["networks"][config.network]["withdraw"]["fee"]))

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

    except Exception as e:
        logger.error("Ошибка: " + str(e))


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
