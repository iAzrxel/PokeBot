from poke_env import Player
from src.battle.memory import OponnentMonMemmory

class PokeBot(Player):
    def __init__(self, strategy, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.strategy = strategy
        self.last_switches_species = None
        self.opponent_memory = {}

    def update_opponent_memory(self, battle):
        for pokemon in battle.opponent_team.values():
            species = pokemon.species

            if species not in self.opponent_memory:
                self.opponent_memory[species] = OponnentMonMemmory(species)

            memory = self.opponent_memory[species]

            memory.types = pokemon.types
            memory.ability = pokemon.ability
            memory.item = pokemon.item
            memory.status = pokemon.status
            memory.last_seen_turn = battle.turn

            if pokemon.moves:
                for move_id in pokemon.moves.keys():
                    memory.moves.add(move_id)
        
    def print_opponent_memory(self):
        print("\n----- MEMÓRIA DO OPONENTE -----")

        for species, memory in self.opponent_memory.items():
                print(
                    f"{species} | "
                    f"types = {memory.types} | "
                    f"ability = {memory.ability} | "
                    f"item = {memory.item} | "
                    f"moves = {list(memory.moves)} | "
                    f"status = {memory.status} | "
                    f"last seen = {memory.last_seen_turn} | "
                )

        print("---------------------------------\n")

    def choose_move(self, battle):
        self.update_opponent_memory(battle)
        self.print_opponent_memory()

        return self.strategy.choose(self, battle)