from classes.game import Person, bcolors
from classes.magic import spell
from classes.inventory import Item
import random

# Create Black Magic

Fire = spell("Fire", 25, 600, "black")
Thunder = spell("Thunder", 25, 600, "black")
Blizzard = spell("Blizzard", 25, 600, "black")
Meteor = spell("Meteor", 40, 1200, "black")
Quake = spell("Quake", 14, 140, "black")

# Create White Damage

Cure = spell("Cure", 25, 650, "white")
Cura = spell("Cura", 30, 1500, "white")
Cureen = spell("Cureen", 50, 6000, "white")

# Create some items
Potion = Item("Potion", "potion", "heals 50 HP", 50)
Highpotion = Item("Highpotion", "potion", "heals 100 HP", 100)
Superpotion = Item("Super Potion", "potion", "Heals 1200 HP", 1200)
elixer = Item("Elixer", "elixer", "Fully restores HP,Mp of one party member", 1000)
highelixer = Item("Megaelixer", "elixer", "Fully restores Party's HP and MP", 2000)

Grenade = Item("Grenade", "Attack", "deals 500 damage", 500)

# instantiate People
player_spells = [Fire, Thunder, Blizzard, Meteor, Cure, Cura]
enemy_spells = [Fire, Meteor, Cure]
player_items = [{"Item": Potion, "quantity": 15}, {"Item": Highpotion, "quantity": 5},
                {"Item": Superpotion, "quantity": 5}, {"Item": elixer, "quantity": 5},
                {"Item": highelixer, "quantity": 5}, {"Item": Grenade, "quantity": 5}]
player1 = Person("Amar: ", 3260, 132, 300, 34, player_spells, player_items)
player2 = Person("Akbar:  ", 4160, 190, 315, 34, player_spells, player_items)
player3 = Person("Anthony: ", 3890, 170, 288, 34, player_spells, player_items)

enemy1 = Person("Shakaal ", 1200, 130, 560, 325, enemy_spells, [])
enemy2 = Person("Magnum ", 11200, 700, 520, 25, enemy_spells, [])
enemy3 = Person("Demogorgen ", 1200, 130, 560, 325, enemy_spells, [])

players = [player1, player2, player3]
enemies = [enemy1, enemy2, enemy3]
running = True
i = 0
print(bcolors.FAIL + bcolors.BOLD + "An ENEMY Attacks!" + bcolors.ENDC)

while running:

    print("=================")
    print("\n\n")
    print("Names:                       HP                                    MP")
    for player in players:
        player.get_stats()

    print("\n")
    for enemy in enemies:
        enemy.get_enemy_stats()

    for player in players:

        player.choose_action()
        choice = input("    Choose Action: ")
        index = int(choice) - 1
        if index == 0:
            dmg = player.generate_damage()
            enemy = player.choose_target(enemies)
            enemies[enemy].take_damage(dmg)
            print("You are attacked " + enemies[enemy].name.replace(" ", "") + " for ", dmg, "points of damage.")

            if enemies[enemy].get_hp() == 0:
                print(enemies[enemy].name + " has died.")
                del enemies[enemy]



        elif index == 1:
            player.choose_magic()
            magic_choice = int(input("    Choose Magic ")) - 1

            if magic_choice == -1:
                continue

            spell = player.magic[magic_choice]
            magic_dmg = spell.generate_damage()

            current_mp = player.get_mp()

            if spell.cost > current_mp:
                print(bcolors.FAIL + "\nNot Enough MP\n" + bcolors.ENDC)
                continue
            player.reduce_mp(spell.cost)

            if spell.type == "white":
                player.heal(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + "heals for", str(magic_dmg), "HP " + bcolors.ENDC)
            elif spell.type == "black":
                enemy = player.choose_target(enemies)
                enemies[enemy].take_damage(magic_dmg)

                print(bcolors.OKBLUE + "\n" + spell.name + " deals", str(magic_dmg),
                      "points of damage to " + enemies[enemy].name.replace(" ", "") + bcolors.ENDC)

                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].name.replace(" ", "") + " has died.")
                    del enemies[enemy]

        elif index == 2:
            player.choose_items()
            Item_choice = int(input("    Choose item: ")) - 1

            if Item_choice == -1:
                continue

            Item = player.items[Item_choice]["Item"]
            if player.items[Item_choice]["quantity"] == 0:
                print(bcolors.FAIL + "\n" + "None Left......" + bcolors.ENDC)
                continue

            player.items[Item_choice]["quantity"] -= 1

            if Item.type == "potion":
                player.heal(Item.prop)
                print(bcolors.OKGREEN + "\n" + Item.name + "heals for ", str(Item.prop), "HP" + bcolors.ENDC)
            elif Item.type == "elixer":
                if Item.name == "Megaelixer":
                    for i in players:
                        i.hp = i.maxhp
                        i.mp = i.maxmp
                else:
                    player.hp = player.maxhp
                    player.mp = player.maxmp
                print(bcolors.OKGREEN + "\n" + Item.name + " Fully Restores HP/MP" + bcolors.ENDC)
            elif Item.type == "attack":
                enemy = player.choose_target(enemies)
                enemies[enemy].take_damage(Item.prop)
                print(bcolors.FAIL + "\n" + Item.name + "deals", str(Item.prop),
                      "points of damage to" + enemies[enemy].name.replace(" ", "") + bcolors.ENDC)

                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].name + " has died.")
                    del enemies[enemy]
    # Check if Battle is over
    defeated_enemies = 0

    defeated_players = 0

    for enemy in enemies:
        if enemy.get_hp() == 0:
            defeated_enemies += 1

    for player in players:

        if player.get_hp() == 0:
            defeated_players += 1
    # Check if Player won
    if defeated_enemies == 2:
        print(bcolors.OKGREEN + "You win!" + bcolors.ENDC)
        running = False
    # Check if Enemy won
    elif defeated_players == 2:
        print(bcolors.FAIL + "Your Enemies have defeated you!" + bcolors.ENDC)
        running = False
    print(" ")
    # Enemy won
    for enemy in enemies:
        enemy_choice = random.randrange(0, 2)
        if enemy_choice == 0:
            # Choose Attack
            target = random.randrange(0, 3)
            enemy_dmg = enemy.generate_damage()

            players[target].take_damage(enemy_dmg)
            print(enemy.name.replace(" ", "") + " attacks " + players[target].name.replace(" ", "") + "for", enemy_dmg)

        elif enemy_choice == 1:
            spell, magic_dmg = enemy.choose_enemy_spell()
            enemy.reduce_mp(spell.cost)

            if spell.type == "white":
                enemy.heal(magic_dmg)
                print(bcolors.OKBLUE + spell.name + " heals " + enemy.name + "for", str(magic_dmg), "HP " + bcolors.ENDC)
            elif spell.type == "black":
                target = random.randrange(0, 3)
                players[target].take_damage(magic_dmg)

                print(bcolors.OKBLUE + "\n" + enemy.name.replace(" ", "") + "'s  " + spell.name + " deals", str(magic_dmg),
                      "points of damage to " + players[target].name.replace(" ", "") + bcolors.ENDC)

                if players[target].get_hp() == 0:
                    print(players[target].name.replace(" ", "") + " has died.")
                    del players[target]
            # print("Enemy chose", spell, "damage is", magic_dmg)
