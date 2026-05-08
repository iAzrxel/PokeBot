import asyncio

from poke_env import AccountConfiguration, ShowdownServerConfiguration

from src.bot.config import (
    BOT_USERNAME,
    BOT_PASSWORD,
    TARGET_USERNAME,
    BATTLE_FORMAT,
    validate_config
)
from src.bot.player import PokeBot
from src.strategy.max_power import MaxPowerStrategy

async def main():
    validate_config()

    bot = PokeBot(
        strategy=MaxPowerStrategy(),
        account_configuration =AccountConfiguration(
            BOT_USERNAME,
            BOT_PASSWORD
        ),
        server_configuration=ShowdownServerConfiguration,
        battle_format=BATTLE_FORMAT
    )

    print(f'Bot conectado como {BOT_USERNAME}')
    print(f'Aguardando desafio em {BATTLE_FORMAT}...')

    await bot.accept_challenges(
        TARGET_USERNAME,
        n_challenges=1
    )

if __name__ == "__main__":
    asyncio.run(main())