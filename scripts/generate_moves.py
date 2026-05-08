import re
from pathlib import Path
from urllib.request import urlopen


SHOWDOWN_MOVES_URL = (
    "https://raw.githubusercontent.com/smogon/pokemon-showdown/master/data/moves.ts"
)

OUTPUT_PATH = Path("src/data/moves.py")


def normalize_move_id(raw_id: str) -> str:
    return raw_id.lower().replace("-", "").replace(" ", "").replace("'", "")


def main():
    print("Baixando moves.ts do Pokémon Showdown...")

    with urlopen(SHOWDOWN_MOVES_URL) as response:
        content = response.read().decode("utf-8")

    pattern = re.compile(
        r'["\']?([a-zA-Z0-9]+)["\']?\s*:\s*\{.*?type:\s*["\'](\w+)["\']',
        re.DOTALL,
    )

    moves = {}

    for move_id, move_type in pattern.findall(content):
        moves[normalize_move_id(move_id)] = move_type.upper()

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with OUTPUT_PATH.open("w", encoding="utf-8") as file:
        file.write("# Arquivo gerado automaticamente por scripts/generate_moves.py\n\n")
        file.write("MOVE_TYPES = {\n")

        for move_id in sorted(moves):
            file.write(f'    "{move_id}": "{moves[move_id]}",\n')

        file.write("}\n")

    print(f"Gerado: {OUTPUT_PATH}")
    print(f"Total de moves: {len(moves)}")


if __name__ == "__main__":
    main()