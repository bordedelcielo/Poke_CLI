import requests
import random
import ascii_magic
from functools import reduce

class Pokemon:
    def __init__(self):
        self.name=''
        self.id=-1
        self.hit_points=-1
        self.attack_points=-1
        self.defense_points=-1
        self.types=[]
        self.image=''
        self.master=None
    
    def create_from_name(self, name):
        response=requests.get(f'https://pokeapi.co/api/v2/pokemon/{name.lower()}')
        if not response.ok:
            return False
        data = response.json()

        self.id = data["id"]
        self.name = data['name']
        self.hit_points = data["stats"][0]["base_stat"]
        self.attack_points = data["stats"][1]["base_stat"]
        self.defense_points = data["stats"][2]["base_stat"]
        self.types=[ability['ability']['name'] for ability in data['abilities']]
        self.image=data["sprites"]["other"]["home"]["front_default"]

        return True
    
    def attack(self, pokemon):
        attacking_power_self = self.attack_points - pokemon.defense_points*.5 
        attacking_power_pokemon = pokemon.attack_points-self.defense_points*.5 
        if attacking_power_self <= 0:
            self.hit_points=0
        if attacking_power_pokemon <= 0:
            pokemon.hit_points=0
        while self.hit_points>0 and pokemon.hit_points>0:
            chance_self=random.choice([True if n < self.master.crit_chance*1000 
                else False for n in range(1000)])
            chance_pokemon=random.choice([True if n < pokemon.master.crit_chance*1000 
                else False for n in range(1000)])
            # Attacker Starts battler
            pokemon.hit_points-=int(attacking_power_self) if not chance_self \
                else int(attacking_power_self*((self.master.crit_bonus/100)+1))
            self.hit_points-=int(attacking_power_pokemon) if not chance_pokemon \
                else int(attacking_power_pokemon*((pokemon.master.crit_bonus/100)+1))
        
    def display(self, cols=100):
        poke_img = ascii_magic.from_url(self.image, columns=cols)
        ascii_magic.to_terminal(poke_img)

    def display_stats(self):
        return f"""
Name:\t\t{self.name}
Hit Points:\t{self.hit_points}
Attack Points:\t{self.attack_points}
Defense Points:\t{self.defense_points}
Types: \t\t {reduce(lambda x,y: x+" "+y, self.types)}
        """