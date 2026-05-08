from src.strategy.base import Strategy
from src.logs.battle_logger import log_decision
from src.battle.evaluator import evaluate_move, evaluate_switch


class MaxPowerStrategy(Strategy):
    def choose(self, player, battle):
        attacker = battle.active_pokemon
        defender = battle.opponent_active_pokemon

        opponent_memory = player.opponent_memory.get(defender.species)

        if battle.force_switch:
            print("FORCE SWITCH DETECTADO")

            best_switch = None
            best_switch_score = -1

            for pokemon in battle.available_switches:
                current_switch_score = evaluate_switch(
                    pokemon,
                    defender,
                    opponent_memory
                )

                if pokemon.species == player.last_switches_species:
                    current_switch_score -= 75

                print(
                    f"{pokemon.species} | "
                    f"switch_score = {current_switch_score}"
                )

                if current_switch_score > best_switch_score:
                    best_switch_score = current_switch_score
                    best_switch = pokemon

            if best_switch:
                player.last_switches_species = attacker.species

                print(f"BOT DECIDIU TROCAR PARA {best_switch.species}")
                return player.create_order(best_switch)

            return player.choose_random_move(battle)

        best_move = None
        attack_score = -1

        if battle.available_moves:
            for move in battle.available_moves:
                score = evaluate_move(
                    attacker,
                    defender,
                    move,
                    battle
                )

                print(
                    f"{move.id} | "
                    f"power = {move.base_power} "
                    f"score = {score}"
                )

                if score > attack_score:
                    attack_score = score
                    best_move = move

        best_switch = None
        switch_score = -1

        if battle.available_switches:
            print("\n----- AVALIANDO TROCAS -----")

            for pokemon in battle.available_switches:
                current_switch_score = evaluate_switch(
                    pokemon,
                    defender,
                    opponent_memory
                )

                if pokemon.species == player.last_switches_species:
                    current_switch_score -= 75

                print(
                    f"{pokemon.species} | "
                    f"switch_score = {current_switch_score}"
                )

                if current_switch_score > switch_score:
                    switch_score = current_switch_score
                    best_switch = pokemon

            print("-----------------------")

        SHOULD_SWITCH_MARGIN = 30

        if (
            best_switch
            and switch_score > attack_score + SHOULD_SWITCH_MARGIN
        ):
            player.last_switches_species = attacker.species

            print(
                f"BOT DECIDIU TROCAR PARA {best_switch.species} | "
                f"switch_score = {switch_score} "
                f"attack_score = {attack_score}"
            )
            print("---------------------------")

            return player.create_order(best_switch)

        if best_move:
            log_decision(
                battle=battle,
                move=best_move,
                score=attack_score
            )

            print(f"BOT DECIDIU ATACAR COM {best_move.id}")
            print(f"attack_score = {attack_score}")
            print(f"switch_score = {switch_score}")
            print(best_move.type)
            print(defender.ability)
            print("-------------------------------")

            return player.create_order(best_move)

        print("BOT NÃO ENCONTROU AÇÃO VÁLIDA, USANDO RANDOM")
        return player.choose_random_move(battle)