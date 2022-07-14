class Master:
    MAX_TEAM_SIZE=3

    def __init__(self, name, id):
        self.name=name
        self.id=id
        self.pokemon=[]
        self.crit_chance = .125
        self.crit_bonus = 100

    def catch(self, poke):
        if len(self.pokemon)>=Master.MAX_TEAM_SIZE:
            return "You have too many Pokemon"
        if poke.id in [p.id for p in self.pokemon]:
            return f"You have Already caught {poke.name}"
        poke.master=self
        self.pokemon.append(poke)
        return f"You caught {poke.name}!"
    

    def release(self, name):
        self.pokemon=list(filter(lambda poke: poke.name!=name,self.pokemon))
        return True

    def show_team(self):
        for poke in self.pokemon:
            poke.display(30)

    

