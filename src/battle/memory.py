class OponnentMonMemmory:
    def __init__(self, species):
        self.species = species
        self.types = []
        self.ability = None
        self.item = None
        self.status = None
        self.moves = set()
        self.last_seen_turn = None

    def __repr__(self):
        return (
            f"OpponentMonMemory("
            f"species={self.species}, "
            f"types={self.types}, "
            f"ability={self.ability}, "
            f"moves={self.moves}, "
            f"status={self.status}, "
            f"last_seen_turn={self.last_seen_turn}"
            f")"
        )