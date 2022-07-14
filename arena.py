from master import Master
from pokemon import Pokemon
import ascii_magic
from colorizer import *
import time
from pyfiglet import figlet_format

class Arena():
    def __init__(self):
        self.master1=None
        self.master2=None
    
    def welcome(self):
        clear_screen()
        print('\n'*5)
        logo=ascii_magic.from_url("https://res.cloudinary.com/cae67/image/upload/v1657497449/pokemon_mdjxb5.png")
        ascii_magic.to_terminal(logo)
        print('\n'*2)
        input_yellow('\t\t\t\t\t\t--PRESS ENTER TO START--')

    def collect_team(self, master):
        while len(master.pokemon) < Master.MAX_TEAM_SIZE:
            print(Fore.BLUE if master.id%2==0 else Fore.YELLOW, Style.BRIGHT, end="")
            clear_screen()
            poke_name = input(f"{master.name} What pokemon do you want to find?: ").title()
            if poke_name.lower()=="remove":
                poke_name = input(f"{master.name} What pokemon do you want to release?: ").title()

                if master.release(poke_name):
                    print(f'You have released {poke_name}')
                    time.sleep(2)
                else:
                    print(f'you haven\'t caught that pokemon!')
                    time.sleep(2)
                continue
            poke=Pokemon()
            if not poke.create_from_name(poke_name):
                print(f"{poke_name} is too elusive try another Pokemon")
                time.sleep(2)
                continue
            clear_screen()
            print(f"{master.name} found {poke_name}")
            print(Style.RESET_ALL, end='')
            poke.display()
            print_red(poke.display_stats())
            if master.id%2==0:
                catchem = input_blue(f"Would you like to Catch {poke_name}? (Y/N) ")
            else:
                catchem = input_yellow(f"Would you like to Catch {poke_name}? (Y/N) ")

            if catchem and catchem[0].lower()=='y':
                clear_screen()
                print_red(master.catch(poke))
                time.sleep(2)
                clear_screen()


    def battle_loop(self):
        while self.master1.pokemon and self.master2.pokemon:
            self.battle()
            clear_screen()

            # Find the dead
            player_1_dead=list(filter(lambda p: p.hit_points <= 0, self.master1.pokemon))
            player_2_dead=list(filter(lambda p: p.hit_points <= 0, self.master2.pokemon))

            # Death Notices
            if player_1_dead or player_2_dead:
                print_red(figlet_format("The Fallen", font = "chunky"))

            if player_1_dead:
                print_yellow(figlet_format("PLAYER 1", font="speed"))
                for poke in player_1_dead:
                    print_yellow(f"{poke.name} has been defeated")

            if player_2_dead:
                print_blue(figlet_format("PLAYER 2", font="speed"))
                for poke in player_2_dead:
                    print_blue(f"{poke.name} has been defeated")

            # Kill the pokemon by saving the survivors
            self.master1.pokemon = list(filter(lambda p: p.hit_points > 0, self.master1.pokemon))
            self.master2.pokemon = list(filter(lambda p: p.hit_points > 0, self.master2.pokemon))


            # Hp Balances of Remaing pokemon
            if self.master1.pokemon or self.master2.pokemon:
                print_red(figlet_format("Remaining", font="chunky"))

            if self.master1.pokemon:
                print_yellow(figlet_format("Player 1", font="speed"))
                for poke in self.master1.pokemon:
                    print_yellow(f"{poke.name} has {poke.hit_points} life remaining")
            
            if self.master2.pokemon:
                print_blue(figlet_format("Player 2", font="speed"))
                for poke in self.master2.pokemon:
                    print_blue(f"{poke.name} has {poke.hit_points} life remaining")
            
            if self.master1.pokemon and self.master2.pokemon:
                input_red("\t\t\t\t\t --Press Enter For the Next Round--")
            else:
                input_green("\t\t\t\t\t --Press Enter--")

                if not self.master1.pokemon:
                    clear_screen()
                    print_red(figlet_format(f"{self.master2.name} Claims Victory", font="poison"))
                
                if not self.master2.pokemon:
                    clear_screen()
                    print_red(figlet_format(f"{self.master1.name} Claims Victory", font="poison"))
                
            

    def battle(self):
        master2_index = len(self.master2.pokemon)-1
        for index in range(len(self.master1.pokemon)):
            if master2_index >=0 and self.master1.pokemon[index].hit_points > 0 \
                and self.master2.pokemon[master2_index].hit_points > 0:
                clear_screen()
                start_hp_p1=self.master1.pokemon[index].hit_points
                start_hp_p2=self.master2.pokemon[master2_index].hit_points

                self.master1.pokemon[index].attack(self.master2.pokemon[master2_index])

                # Make stuff happen 

                #player1 OG HP
                self.master1.pokemon[index].display()
                print_yellow(figlet_format(f'\tHP {start_hp_p1}', font="doom"))
                time.sleep(2)
                clear_screen()

                #player2 OG HP
                self.master2.pokemon[master2_index].display()
                print_blue(figlet_format(f'\tHP {start_hp_p2}', font="doom"))
                time.sleep(2)
                clear_screen()

                #flash balls
                logo = ascii_magic.from_url('https://res.cloudinary.com/cae67/image/upload/v1657666237/pokeball_closed_kqdsgd.png')
                ascii_magic.to_terminal(logo)
                time.sleep(1)
                clear_screen()
                logo = ascii_magic.from_url('https://res.cloudinary.com/cae67/image/upload/w_1000,ar_1:1,c_fill,g_auto,e_art:hokusai/v1657666100/pokeballopen_rtossk.png')
                ascii_magic.to_terminal(logo)
                time.sleep(1)
                clear_screen()

                # Display both pokemon with damage taken
                damage_taken_p1 = int(self.master1.pokemon[index].hit_points - start_hp_p1)
                damage_taken_p2 = int(self.master2.pokemon[master2_index].hit_points - start_hp_p2)
                
                self.master1.pokemon[index].display(cols=40)
                print_yellow(figlet_format(str(damage_taken_p1) if damage_taken_p1 else 'invincible' , font="doom"))
                
                self.master2.pokemon[master2_index].display(cols=40)
                print_blue(figlet_format(str(damage_taken_p2) if damage_taken_p2 else 'invincible' , font="doom"))
                time.sleep(2)
            master2_index-=1
            


    # Player 1 I want in Yellow
    # Player 2 I want in Blue
    def main(self):
        self.welcome()
        player1 = input_yellow("Player 1 Enter Your Name: ").title()
        player2 = input_blue("Player 2 Enter Your Name: ").title()
        self.master1=Master(player1, 1)
        self.master2=Master(player2, 2)

        print_yellow(f"""
{self.master1.name} Capture Your Team
You will get to capture up to {Master.MAX_TEAM_SIZE} Pokemon
If you change your mind you can type Remove to choose a pokemon to release
        """)
        time.sleep(3)
        self.collect_team(self.master1)


        print_blue(f"""
{self.master2.name} Capture Your Team
You will get to capture up to {Master.MAX_TEAM_SIZE} Pokemon
If you change your mind you can type Remove to choose a pokemon to release
        """)
        time.sleep(3)
        self.collect_team(self.master2)

        clear_screen()
        print_yellow(figlet_format(f"{self.master1.name} Entering the Arena", font="speed"))
        self.master1.show_team()
        time.sleep(3)

        clear_screen()
        print_blue(figlet_format(f"{self.master2.name} Entering the Arena", font="speed"))
        self.master2.show_team()
        time.sleep(3)

        self.battle_loop()

    