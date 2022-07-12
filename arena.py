from master import Master
from pokemon import Pokemon
import ascii_magic
import os
from pyfiglet import figlet_format
from colorama import Fore
from colorama import Style
from colorama import init
import time



# Death - poison



class Arena:
    #init for colorama to fixed windows wierdness
    init()
    @staticmethod
    def clear_screen():
        os.system('cls' if os.name == 'nt' else 'clear')

    def __init__(self):
        self.master1=None
        self.master2=None
    
    def welcome(self):

        Arena.clear_screen()
        print('\n'*5)
        logo=ascii_magic.from_url('https://res.cloudinary.com/cae67/image/upload/v1657497449/pokemon_mdjxb5.png')
        ascii_magic.to_terminal(logo)
        print('\n'*2)
        print(Fore.YELLOW, Style.BRIGHT, end="" )     
        input('\t\t\t\t\t\t--PRESS ENTER TO START--')


    def collect_team(self,master):
        print(Fore.BLUE if master.id%2==0 else Fore.YELLOW, Style.BRIGHT, end="")
        while len(master.pokemon)<Master.MAX_TEAM_SIZE:
            Arena.clear_screen()
            poke_name=input(f"{master.name} What pokemon do you want to find?:  ").title()
            if poke_name.lower()=="remove":
                poke_name=input(f"{master.name} What pokemon do you want to release?:").lower()
                if master.release(poke_name):
                    print(f'You have release {poke_name}')
                    time.sleep(2)
                else:
                    print(f'You haven\'t caught that pokemon!')
                    time.sleep(2)
                continue
            poke=Pokemon()
            if not poke.create_from_name(poke_name):
                print(f"{poke_name} is too elusive try another pokemon")
                time.sleep(2)
                continue
            Arena.clear_screen()
            print(f"{master.name} found {poke_name}")
            print(Style.RESET_ALL, end='')
            poke.display()

            print(Fore.RED, Style.BRIGHT,poke.display_stats(), Style.RESET_ALL, end="")

            print(Fore.BLUE if master.id%2==0 else Fore.YELLOW, Style.BRIGHT, end="")
            catchem=input(f"Would you like to Catch {poke_name}? (Y/N) ")
            if catchem[0].lower()=='y':
                print(master.catch(poke))
        print(Style.RESET_ALL, end='')

    def battle(self):
        master2_index=len(self.master2.pokemon)-1
        for index in range(len(self.master1.pokemon)):
            if master2_index>0 and self.master1.pokemon[index].hit_points > 0 and self.master2.pokemon[master2_index].hit_points > 0:
                self.master1.pokemon[index].attack(self.master2.pokemon[index])
            master2_index-=1


    def battle_loop(self):
        Arena.clear_screen()
        self.master1.pokemon=list(filter(lambda pokemon: pokemon.hit_points>0, self.master1.pokemon))
        self.master2.pokemon=list(filter(lambda pokemon: pokemon.hit_points>0, self.master2.pokemon))
        while self.master1.pokemon and self.master2.pokemon:
            self.battle()
            print(Fore.RED, Style.BRIGHT, end="")
            if list(filter(lambda p: p.hit_points<0 ,self.master1.pokemon)) and list(filter(lambda p: p.hit_points<0 ,self.master2.pokemon)):
                print(figlet_format("RESULT", font="univers"))

            print(Style.RESET_ALL, end='')

            # Death Notices
            print(Fore.YELLOW, Style.BRIGHT, end="")
            if list(filter(lambda p: p.hit_points<0 ,self.master2.pokemon)):
                print(figlet_format("PLAYER 1", font="speed"))

            for poke in self.master1.pokemon:
                if poke.hit_points < 0:
                    print(f"{poke.name} has been defeated")

            print(Style.RESET_ALL, end='')
            print(Fore.BLUE, Style.BRIGHT, end="")

            if list(filter(lambda p: p.hit_points<0 ,self.master2.pokemon)):
                print(figlet_format("PLAYER 2",font="speed"))

            for poke in self.master2.pokemon:
                if poke.hit_points < 0:
                    print(f"{poke.name} has been defeated")

            print(Style.RESET_ALL, end='')
            self.master1.pokemon=list(filter(lambda pokemon: pokemon.hit_points>0, self.master1.pokemon))
            self.master2.pokemon=list(filter(lambda pokemon: pokemon.hit_points>0, self.master2.pokemon))

            # HP Balances
            print(Fore.RED, Style.BRIGHT, end="")
            if self.master1.pokemon or self.master2.pokemon:
                print(figlet_format("Poke in Battle" ,font="univers"))
            print(Style.RESET_ALL, end='')

            print(Fore.YELLOW, Style.BRIGHT, end="")
            if self.master1.pokemon:
                print(figlet_format("PLAYER 1",font="speed"))
            for poke in self.master1.pokemon:
                print(f"{poke.name} has {poke.hit_points} life remaining")

            print(Style.RESET_ALL, end='')

            print(Fore.BLUE, Style.BRIGHT, end="")
            if self.master2.pokemon:
                print(figlet_format("PLAYER 2",font="speed"))

            for poke in self.master2.pokemon:
                print(f"{poke.name} has {poke.hit_points} life remaining")
            print(Style.RESET_ALL, end='')

            input("\t\t\t\t --Press Enter For the Next Round--")

        if len(self.master1.pokemon)>0:
            time.sleep(3)
            Arena.clear_screen()
            print(Fore.YELLOW, Style.BRIGHT, end="")
            print(figlet_format(f"{self.master1.name} Claims Victory",font="poison"))
            print(Style.RESET_ALL, end='')

        if len(self.master2.pokemon)>0:
            time.sleep(3)
            Arena.clear_screen()
            print(Fore.BLUE, Style.BRIGHT, end="")
            print(figlet_format(f"{self.master2.name} Claims Victory",font="poison"))
            print(Style.RESET_ALL, end='')

    def main(self):
        self.welcome()
        print(Fore.YELLOW, Style.BRIGHT, end="")
        player1=input("Player 1 Enter your name: ").title()
        print(Style.RESET_ALL, end='')
        print(Fore.BLUE, Style.BRIGHT, end="")
        player2=input("Player 2 Enter your name: ").title()
        print(Style.RESET_ALL, end='')
        self.master1=Master(player1,1)
        self.master2=Master(player2,2)
        print(Fore.YELLOW, Style.BRIGHT, end="")

        print(f"""
{self.master1.name} Capture Your Team
You will get to capture up to 5 Pokemon
If you change your mind you can Type Remove to choose a pokemon to remove
        """)
        print(Style.RESET_ALL, end='')
        self.collect_team(self.master1)

        print(Fore.YELLOW, Style.BRIGHT, end="")
        print(f"""
{self.master2.name} Capture Your Team
You will get to capture up to 5 Pokemon
If you change your mind you can Type Remove to choose a pokemon to remove
        """)
        print(Style.RESET_ALL, end='')
        self.collect_team(self.master2)

        
        Arena.clear_screen()
        print(Fore.BLUE, Style.BRIGHT, end="")
        print(figlet_format(f"{self.master1.name} Entering the Arena", font="speed"))
        print(Style.RESET_ALL, end='')
        self.master1.show_team()
        time.sleep(3)
        
        Arena.clear_screen()
        print(Fore.BLUE, Style.BRIGHT, end="")
        print(figlet_format(f"{self.master2.name} Entering the Arena", font="speed"))
        print(Style.RESET_ALL, end='')
        self.master2.show_team()
        time.sleep(3)


        self.battle_loop()

        

if __name__=="__main__":
    Arena().main()


            




