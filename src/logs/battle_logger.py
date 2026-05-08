def log_decision(battle, move, score=None):
    print("\n----- Decisão do bot foda -----")
    print(f"Turno: {battle.turn}")
    print(f"Bot: {battle.active_pokemon}")
    print(f"Oponente: {battle.opponent_active_pokemon}")
    print(f"Move escolhido: {move}")

    if score is not None:
        print(f"Score: {score}")

    print("--------------------------------")