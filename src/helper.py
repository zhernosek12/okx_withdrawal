from pathlib import Path
from typing import List


def print_logo():
    logo = '''
    ______  _____  _____   ___   _____   __   __   _____ ______ __   ________  _____  _   _  _____ 
    | ___ \|  ___||  __ \ / _ \ /  ___|  \ \ / /  /  __ \| ___ \\\ \ / /| ___ \|_   _|| | | |/  ___|
    | |_/ /| |__  | |  \// /_\ \\\ `--.    \ V /   | /  \/| |_/ / \ V / | |_/ /  | |  | | | |\ `--. 
    |  __/ |  __| | | __ |  _  | `--. \   /   \   | |    |    /   \ /  |  __/   | |  | | | | `--. \\
    | |    | |___ | |_\ \| | | |/\__/ /  / /^\ \  | \__/\| |\ \   | |  | |      | |  | |_| |/\__/ /
    \_|    \____/  \____/\_| |_/\____/   \/   \/   \____/\_| \_|  \_/  \_|      \_/   \___/ \____/ 

    '''
    print(logo)


def load_data(file_path: Path) -> List[str]:
    with file_path.open() as f:
        data = f.read().splitlines()
    return data


def fee_network(symbol, name, fees):
    networks = {
        "AVAX": {
            "Avalanche C-Chain": "Avalanche C"
        },
        "ETH": {
            "ERC20": "ERC20",
            "Base": "Base",
            "Optimism": "OPTIMISM",
            "Arbitrum One": "Arbitrum One",
            "zkSync Era": "zkSync Era",
        },
        "BNB": {
            "BSC": "BEP20",
        },
        "MATIC": {
            "Polygon": "MATIC"
        }
    }
    try:
        return networks[symbol][name]
    except Exception as e:
        return name
        #raise Exception(f"Сеть не найдена! '{symbol}' --> '{name}' ({fees})")
