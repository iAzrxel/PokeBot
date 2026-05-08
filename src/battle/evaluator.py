from src.data.moves import MOVE_TYPES
from poke_env.battle.pokemon_type import PokemonType

HEALING_MOVES = {
    "recover",
    "softboiled",
    "roost",
    "synthesis",
    "slackoff",
    "morningsun",
    "moonlight",
}

CLERIC_MOVES = {
    "healbell",
    "aromatherapy",
}

DISRUPTION_MOVES = {
    "encore",
    "taunt",
    "roar",
    "whirlwind",
    "dragontail",
    "circlethrow",
    "haze",
    "clearsmog",
}

PRIORITY_MOVES = {
    "aquajet",
    "jetpunch",
    "suckerpunch",
    "extremespeed",
    "iceshard",
    "bulletpunch",
    "machpunch",
    "vacuumwave",
    "shadowshard",
    "quickattack",
}

def estimate_damage(attacker, defender, move):
    if move.base_power is None:
        return 0
    
    score = move.base_power

    if move.type in attacker.types:
        score *= 1.5

    multiplier = defender.damage_multiplier(move)
    score *= multiplier

    return score

def team_has_status(battle):
    for pokemon in battle.team.values():
        if pokemon.status is not None:
            return True

    return False

def total_positive_boosts(pokemon):
    if not pokemon.boosts:
        return 0

    return sum(value for value in pokemon.boosts.values() if value > 0)


def opponent_is_boosted(pokemon):
    return total_positive_boosts(pokemon) > 0

def evaluate_move(attacker, defender, move, battle):
    move_id = move.id

    if move_id in HEALING_MOVES:
        if attacker.current_hp_fraction <= 0.5:
            return 80

        return -10

    if move_id in CLERIC_MOVES:
        if team_has_status(battle):
            return 70

        return -10
    
    if move_id in DISRUPTION_MOVES:
        total_boosts = total_positive_boosts(defender)

        if total_boosts >= 2:
            return 250

        if total_boosts > 0:
            return 120
        
        return -10

    score = estimate_damage(attacker, defender, move)

    estimated_hp_percent_damage = score / 3

    if estimated_hp_percent_damage >= defender.current_hp_fraction * 100:
        score += 500

    if attacker.current_hp_fraction <= 0.25:
        if move_id in PRIORITY_MOVES:
            score += 120

        if estimated_hp_percent_damage >= defender.current_hp_fraction * 100:
            score += 250

    return score

def evaluate_switch_by_opponent_types(pokemon, opponent):
    multipliers = []

    for opponent_type in opponent.types:
        multiplier = pokemon.damage_multiplier(opponent_type)
        multipliers.append(multiplier)

    if not multipliers:
        return 100
    
    worst_multiplier = max(multipliers)

    if worst_multiplier == 0:
        return 350

    return 100 / worst_multiplier


def evaluate_switch_by_known_moves(pokemon, opponent_memory):
    if not opponent_memory:
        return 0
    
    if not opponent_memory.moves:
        return 0
    
    total_score = 0

    for move_id in opponent_memory.moves:

        move_type = MOVE_TYPES.get(move_id)

        if not move_type:
            continue

        pokemon_type = PokemonType[move_type]

        multiplier = pokemon.damage_multiplier(pokemon_type)

        if multiplier == 0:
            total_score += 120

        elif multiplier == 0.25:
            total_score += 80

        elif multiplier == 0.5:
            total_score += 40

        elif multiplier == 1:
            total_score += 0

        elif multiplier == 2:
            total_score -= 160

        elif multiplier == 4:
            total_score -= 320

    return total_score

def evaluate_switch(pokemon, opponent, opponent_memory = None):
    type_score = evaluate_switch_by_opponent_types(pokemon, opponent)

    memory_score = evaluate_switch_by_known_moves(pokemon, opponent_memory)

    return type_score + memory_score
