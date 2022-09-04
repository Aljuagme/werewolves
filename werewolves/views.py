from django.shortcuts import render
from werewolves.WWManagementSystem import *
from django.shortcuts import redirect

from django.http import HttpResponseRedirect
from django.urls import reverse


# Instance of WWManagementSystem class
w = WWManagementSystem()
recent_players = []

# Global variables needed during the game
people_alive = list(w.players)
seer_list = []
werewolves_victim = []
turn = 0


# Create your views here.

# Display index page
def index(request,):
    return render(request, "werewolves/index.html")


# Check if we reach an end-game point
def end_game(request):
    # Check if the condition for the lovers is fulfill
    if lovers_win(people_alive):
        return render(request, "werewolves/lovers_win.html", )

    # Check if the condition for the white werewolf is fulfill
    elif whitewerewolf_win(people_alive):
        return render(request, "werewolves/whitewerewolf_win.html", )

    # Check if the condition for the villagers is fulfill
    elif villagers_win(people_alive):
        return render(request, "werewolves/villagers_win.html", )

    # Check if the condition for the werewolves is fulfill
    elif werewolves_win(people_alive):
        return render(request, "werewolves/werewolves_win.html", )

# display setup page
def setup(request, testing_session=False):
    global recent_players, people_alive
    args = {"players": recent_players}
    args["min_players"] = [1, 2, 3, 4, 5]
    recent_players = []
    # condition for testing
    if testing_session:
        args = {"players": request.session["players"]}
    # if there are no players stored from the last game
    if "players" not in request.session:
        # create the key,value
        request.session["players"] = []
    # if the "load recent players" button is clicked
    if request.method == "POST" and "load_players" in request.POST:
        # assign the players form the session to recent_players
        recent_players = request.session["players"]
        return HttpResponseRedirect(reverse("werewolves:setup"))
    # if the "start setup night" button is clicked
    if request.method == "POST" and "players" in request.POST:
        # check if the amount of players exceeds the maximum
        if len(request.POST.getlist("players")) > 20:
            return HttpResponseRedirect(reverse("werewolves:setup"))
        # checks if there are duplicate values
        if get_player(request, wwSystem=w):
            people_alive = list(w.players)
            # save the players in the session for next use
            request.session["players"] = request.POST.getlist("players")
            return HttpResponseRedirect(reverse("werewolves:setup_night"))
        else:
            HttpResponseRedirect(reverse("werewolves:setup"))
    return render(request, "werewolves/setup.html", args)

# display setup_night page
def setup_night(request, testing=False):
    # checks if the request is type POST
    if request.method == "POST" and "werewolf" in request.POST:
        # checks and gets role numbers
        if check_role_numbers(request, wwSystem=w):
            get_role_numbers(request, wwSystem=w)
            return HttpResponseRedirect(reverse("werewolves:setup_night_werewolves"))
        else:
            return HttpResponseRedirect(reverse("werewolves:setup_night"))
    args = {"players": w.players}
    max_werewolves = len(args["players"])

    global turn, werewolves_victim, seer_list, people_alive
    turn = 0
    werewolves_victim = []
    seer_list = []
    people_alive = list(w.players)

    if max_werewolves % 2 == 0:
        max_werewolves = (max_werewolves // 2) - 1
    else:
        max_werewolves = max_werewolves // 2
    args["max_werewolves"] = max_werewolves
    # stores the suggestion in args
    suggestions = w.make_suggestions(len(args["players"]))
    for key, value in suggestions.items():
        args[key] = value
    if testing:
        # list of players for testing
        args = {"players": [Player("Thomas"), Player("Alvaro"), Player("Steve"), Player("Poseidon")]}
    return render(request, "werewolves/setup_night/setup_night.html", args)


# display setup_night_seer page
def setup_night_seer(request, testing=(False,None)): # testing[0]->enable testing, testing[1]-> pass role numbers
    role = "seer"
    # assigns a seer if there is one
    if request.method == "POST":
        data = request.POST.getlist(role)
        for name in data:
            w.assign_role(name, role)
        return HttpResponseRedirect(reverse("werewolves:setup_night_witch"))
    if testing[0]:
        w.roleNumbers = testing[1]
    # if there is no seer, redirect to the next page
    if w.roleNumbers[role] < 1:
        return HttpResponseRedirect(reverse("werewolves:setup_night_witch"))
    # arguments passed to render the html
    args = {"players": get_players_without_any_role(w.players)}
    return render(request, "werewolves/setup_night/setup_night_seer.html", args)


# display setup_night_werewolves page
def setup_night_werewolves(request, testing=(False, None)):
    role = "werewolf"
    # assigns werewolves
    if request.method == "POST":
        data = request.POST.getlist(role)
        for name in data:
            w.assign_role(name, role)
        return HttpResponseRedirect(reverse("werewolves:setup_night_white_werewolf"))
    if testing[0]:
        w.roleNumbers = testing[1]
    # if there are no werewolves, redirect to the next page
    if w.roleNumbers[role] < 1:
        return HttpResponseRedirect(reverse("werewolves:setup_night_white_werewolf"))
    # arguments passed to render the html
    args = {"nr_werewolves": list(range(1, w.roleNumbers[role]+1)),
            "players": get_players_without_any_role(w.players)}
    return render(request, "werewolves/setup_night/setup_night_werewolves.html", args)


# display setup_night_white_werewolf page
def setup_night_white_werewolf(request,testing=(False,None)):
    role = "whitewerewolf"
    # assigns the white werewolf if there is one
    if request.method == "POST":
        data = request.POST.getlist(role)
        for name in data:
            w.assign_role(name, role)
        return HttpResponseRedirect(reverse("werewolves:setup_night_seer"))
    if testing[0]:
        w.roleNumbers = testing[1]
    # if there is no whitewerewolf, redirect to the next page
    if w.roleNumbers[role] < 1:
        return HttpResponseRedirect(reverse("werewolves:setup_night_seer"))
    # arguments passed to render the html
    args = {"players": get_players_without_any_role(w.players)}
    return render(request, "werewolves/setup_night/setup_night_white_werewolf.html", args)

# display setup_night_witch page
def setup_night_witch(request,testing=(False,None)):
    role = "witch"
    # assigns the witch if there is one
    if request.method == "POST":
        data = request.POST.getlist(role)
        for name in data:
            w.assign_role(name, role)
        return HttpResponseRedirect(reverse("werewolves:setup_night_hunter"))
    if testing[0]:
        w.roleNumbers = testing[1]
    # if there is no witch, redirect to the next page
    if w.roleNumbers[role] < 1:
        return HttpResponseRedirect(reverse("werewolves:setup_night_hunter"))
    # arguments passed to render the html
    args = {"players": get_players_without_any_role(w.players)}
    return render(request, "werewolves/setup_night/setup_night_witch.html", args)

# display setup_night_hunter page
def setup_night_hunter(request, testing=(False,None)):
    role = "hunter"
    # assigns the hunter if there is one
    if request.method == "POST":
        data = request.POST.getlist(role)
        for name in data:
            w.assign_role(name, role)
        return HttpResponseRedirect(reverse("werewolves:setup_night_amor"))
    if testing[0]:
        w.roleNumbers = testing[1]
    # if there is no hunter, redirect to the next page
    if w.roleNumbers[role] < 1:
        return HttpResponseRedirect(reverse("werewolves:setup_night_amor"))
    # arguments passed to render the html
    args = {"players": get_players_without_any_role(w.players)}
    return render(request, "werewolves/setup_night/setup_night_hunter.html", args)

# display setup_night_amor page
def setup_night_amor(request, testing=(False,None)):
    role = "amor"
    if request.method == "POST":
        data1 = request.POST.getlist(role)
        for name in data1:
            # assigns the amor
            w.assign_role(name, role)
        data2 = request.POST.getlist("lover")
        # assigns both lovers
        for name in data2:
            w.assign_lover(name)
        # assign every player without a role the role "villager"
        for player in get_players_without_any_role(w.players):
            w.assign_role(player.name, "villager")
        return HttpResponseRedirect(reverse("werewolves:night"))
    if testing[0]:
        w.roleNumbers = testing[1]
    # if there is no amor, redirect to the next page
    if w.roleNumbers[role] < 1:
        for player in get_players_without_any_role(w.players):
            w.assign_role(player.name, "villager")
        return HttpResponseRedirect(reverse("werewolves:night"))
    # arguments to render the html
    args = {"players_without_role": get_players_without_any_role(w.players), "players": w.players}
    return render(request, "werewolves/setup_night/setup_night_amor.html", args)


# Start of the day, main point of the game.
def day(request, testing=(False, None)):
    global werewolves_victim
    if testing[0]:
        global people_alive
        people_alive = testing[1][0]
        werewolves_victim = testing[1][1]
    # If we reach this point with a GET request (no input given)
    if request.method == "GET":
        # If there were victims during the night, kill them
        if len(werewolves_victim) > 0:
            for v in werewolves_victim:
                killed = kill(people_alive, str(v.id))

                if killed:

                    # If the victim was the hunter, return the page where he can use his skill
                    if killed.role == "hunter":
                        werewolves_victim.remove(v)

                        # If the hunter was a lover, kill the lover as well
                        if killed.lover:
                            lovers_skill(people_alive, killed)

                        return render(request, "werewolves/hunter.html", {"players": people_alive,
                                                                          "werewolves_victim": werewolves_victim})

                    # Else if the victim is a lover, trigger the lovers' skill
                    elif killed.lover:
                        werewolves_victim.remove(v)
                        other_lover = lovers_skill(people_alive, killed)

                        if other_lover.role == "hunter":
                            return render(request, "werewolves/hunter.html", {"players": people_alive,
                                                                              "werewolves_victim": werewolves_victim})

                    # If the victim is not a hunter or a lover, just kill it normally
                    if killed.role != "hunter" and not killed.lover:
                        werewolves_victim.remove(v)

                    # After you will the first victim, redirect in order to proceed with the next victim if exists
                    return HttpResponseRedirect(reverse("werewolves:day"))

                else:
                    try:
                        werewolves_victim.remove(v)
                    except AttributeError:
                        print("There is no victim with this features")
                    finally:
                        return HttpResponseRedirect(reverse("werewolves:day"))


        # After all the victims from the night are killed, check if end-game point has been reached.
        if end_game(request):
            return end_game(request)

        # If not more victims, and not end-game point reached, just display the main page of the game.
        return render(request, "werewolves/day.html", {"players": w.players})

    # If we reach this point with a POST request (input given)
    else:
        # Retrieve that input
        chosen = request.POST.get("victim")

        # Check that input is not None
        if chosen:
            # If there is a victim, kill it, and check for special roles such as hunter or lovers
            killed = kill(people_alive, chosen)
            if killed.role == "hunter":
                # If the hunter was a lover, kill the lover as well
                if killed.lover:
                    lovers_skill(people_alive, killed)
                return render(request, "werewolves/hunter.html", {"players": people_alive,
                                                                  "werewolves_victim": werewolves_victim})

            if killed.lover:
                other_lover = lovers_skill(people_alive, killed)
                if other_lover.role == "hunter":
                    return render(request, "werewolves/hunter.html", {"players": people_alive,
                                                                      "werewolves_victim": werewolves_victim})

            # Once you kill the victim of the day, redirect to the same page in order to see who died.
            return HttpResponseRedirect(reverse("werewolves:day"))

        # If for some reason the input is None, just redirect to the main page.
        else:
            return redirect("werewolves:day")


# Entering the night
def night(request, testing=(False, None)):
    if testing[0]:
        global people_alive
        people_alive = testing[1]
    # Check if there are villagers or the seer alive, in order to go through the states of the night.
    villagers = villagers_alive(people_alive)
    seer = seer_alive(people_alive)

    # If the seer is alive, then go to his night-turn
    try:
        if seer:
            return render(request, "werewolves/night_seer.html",
                          {"players": people_alive, "seer_list": seer_list,
                           "villager": villagers, "len_villagers": len(villagers)})
    except TypeError:
        if seer:
            return render(request, "werewolves/night_seer.html",
                          {"players": people_alive, "seer_list": seer_list,
                           "villager": villagers})

    # If the seer is not alive, go directly to the sleepwalking face just if there are villagers left
    if villagers:
        if len(villagers) > 1:
            return render(request, "werewolves/sleepwalking.html",
                        {"players": people_alive, "villagers": len(villagers)})
        else:
            return HttpResponseRedirect(reverse("werewolves:werewolves_skill"))

    # Else, werewolves-night (If there are no werewolves, the end-game condition would have been reached already)
    else:
        return HttpResponseRedirect(reverse("werewolves:werewolves_skill"))


# Entering Seer night
def seer_skill(request, testing=(False, None)):
    if testing[0]:
        global people_alive, seer_list
        people_alive = testing[1][0]
        seer_list = testing[1][1]
    # If the seer already checked the role of a player
    chosen = request.POST.get("reveal")

    # Just append it to his list and display it
    if chosen:
        for p in people_alive:
            if p.id == int(chosen):
                seer_list.append(p)

        # Redirect to night, in order to redirect from there to the seer again, in order to see the role of the player
        return HttpResponseRedirect(reverse("werewolves:night"))

    # If the seer didn't check yet, just display his page.
    else:
        return redirect("werewolves:night")


# Entering the sleepwalking phase
def sleep_walking(request, testing=(False, None)):
    if testing[0]:
        global people_alive
        people_alive = testing[1]
    # We get here always as a GET request
    if request.method == "GET":
        # Get me the list of the villagers alive, so we can help the moderator with the total nº of villagers alive.
        villagers = villagers_alive(people_alive)

        # Check if there are more than 1 villager in order to go to sleepwalking phase
        if len(villagers) > 1:
            return render(request, "werewolves/sleepwalking.html",
                      {"players": people_alive, "villagers": len(villagers)})
        else:
            return HttpResponseRedirect(reverse("werewolves:night"))



# Entering sleepwalking if just one villager raised hand
def sleep_1(request, testing=(False, None)):
    if testing[0]:
        global people_alive
        people_alive = testing[1]
    # Is not a seer, different players can get to see a role, therefore we want to start setting the variable to None
    saw = None

    # If the request is GET, just display the names of the players alive
    if request.method == "GET":
        return render(request, "werewolves/sleep_1.html",
                      {"players": people_alive})

    # If request is POST
    else:
        # Get me the player you want to see
        chosen = request.POST.get("reveal")

        # If the chose is valid
        if chosen:
            for p in people_alive:
                if p.id == int(chosen):
                    saw = p

        # Display again the page showing me the role of the chosen player
        return render(request, "werewolves/sleep_1.html",
                      {"players": people_alive, "saw": saw})


# Entering the sleep-accident phase is all villagers raised the hand
def sleep_accident(request, testing=(False, None)):
    global werewolves_victim
    accident_list = []

    if testing[0]:
        global people_alive
        people_alive = testing[1][0]
        accident_list = testing[1][1]
        werewolves_victim = testing[1][2]
    # We need random in order to kill a villager randomly
    import random

    # Kill the villager randomly and added to the accident list
    for p in people_alive:
        if p.role == "villager":
            accident_list.append(p)
    victim = random.choice(accident_list)

    # Add it also to the list of victims during the night

    werewolves_victim.append(victim)

    # Render the page, showing me who died in a terrible accident.
    return render(request, "werewolves/sleep_accident.html",
                  {"victim": victim})


# Entering the werewolves phase
def werewolves_skill(request, testing=(False, None)):
    if testing[0]:
        global people_alive
        people_alive = testing[1]
    # Check if there are whitewerewolf, witch and normal werewolves, to know which one is the next phase of the night
    white = white_alive(people_alive)
    witch = witch_alive(people_alive)
    werewolves = normal_werewolf(people_alive)

    # We want to keep track of the turns for the whitewerewolf
    global turn

    # We get here always as a GET request.
    if request.method == "GET":
        turn += 1   # Sum 1 each turn
        # Render the werewolves page
        return render(request, "werewolves/night_werewolves.html",
                      {"players": people_alive, "white": white, "witch": witch,
                       "turn": turn, "werewolf": werewolves})


# Entering the whitewerewolf phase
def white_skill(request, testing=(False, None)):
    if testing[0]:
        global people_alive, werewolves_victim
        people_alive = testing[1][0]
        werewolves_victim = testing[1][1]
    # Chek if witch to know if we should go/skip the witch's turn
    witch = witch_alive(people_alive)

    # If we reach this by GET request.
    if request.method == "GET":
        return render(request, "werewolves/night_white.html",
                      {"players": people_alive, "witch": witch})

    # Reaching by POST request
    else:
        # Retrieve the victim from the werewolves
        victim = request.POST.get("victim")

        # If there is a victim, added to the list of victims during the night
        if victim:
            for p in people_alive:
                if p.id == int(victim):
                    target = p
                    if target not in werewolves_victim:
                        werewolves_victim.append(target)
                    # Once you added the victim, display the actual whitewerewolf page (GET request)
                    return HttpResponseRedirect(reverse("werewolves:white_skill"))
        return redirect("werewolves:white_skill")


# Entering the witch phase
def witch_skill(request, testing=(False, None)):
    if testing[0]:
        global people_alive, werewolves_victim
        people_alive = testing[1][0]
        werewolves_victim = testing[1][1]
    # Get the object of the player witch
    witch = witch_alive(people_alive)

    # If the witch is alive
    if witch:
        # If the witch does not have potions, her skills can not be use
        if not (witch.death_potion or witch.health_potion):

            # Kill the werewolves victim and go to day
            victim = request.POST.get("victim")
            if victim:
                for p in people_alive:
                    if p.id == int(victim):
                        if p not in werewolves_victim:
                            target = p
                            werewolves_victim.append(target)
                        break

            # Go to main page
            return redirect("werewolves:day")

    # If the witch is dead
    else:
        # Go to main page
        return redirect("werewolves:day")

# If the witch is alive and has potions

    # Check if we are receiving the skill of the heal potion
    if request.POST.get("heal"):
        heal = request.POST.get("heal")
        # Go and delete the player-selected from the night-victims-list so he does not get kill
        for v in werewolves_victim:
            if v.id == int(heal):
                werewolves_victim.remove(v)
                witch.health_potion = False
                # Redirect to the same page
                return HttpResponseRedirect(reverse("werewolves:witch_skill"))

    # Check if we are receiving the skill of the dead potion
    elif request.POST.get("die"):
        die = request.POST.get("die")
        # Go and add the player-selected to the night-victims-list
        for p in people_alive:
            if p.id == int(die):
                target = p
                werewolves_victim.append(target)
                witch.death_potion = False
                # Redirect to the same page
                return HttpResponseRedirect(reverse("werewolves:witch_skill"))

    # If witch, and potions, display the page showing the victims.
    if request.method == "GET":
        return render(request, "werewolves/night_witch.html",
                      {"players": people_alive, "victims": werewolves_victim,
                       "witch": witch, "len_victims": len(werewolves_victim)})

    # Add the victim from the previous page
    else:
        victim = request.POST.get("victim")
        if victim:
            for p in people_alive:
                if p.id == int(victim):
                    if p not in werewolves_victim:
                        target = p
                        werewolves_victim.append(target)
                    break

        return HttpResponseRedirect(reverse("werewolves:witch_skill"))
