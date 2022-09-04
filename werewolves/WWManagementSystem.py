class WWManagementSystem:
    def __init__(self):
        self.players = []
        self.setupNight = None
        self.roleNumbers = {} # dict: e.g. {"werewolf" : 5, "amor": 1,...}

    # adds a Player object with a given name to the list of players
    def add_player(self, name):
        player = Player(name)
        self.players.append(player)

    # return a Player object with the given name from the list
    def get_player_by_name(self, name):
        for player in self.players:
            if player.name == name:
                return player

    # assign a role and the image path to a Player object with a given name in the player list
    def assign_role(self, player_name, role):
        for player in self.players:
            if player.name == player_name:
                player.role = role
                player.imgPath = f"images/{player.role}.jpg"
                if role == "witch":
                    player.death_potion = True
                    player.health_potion = True

    # sets the attribute of the Player to true
    def assign_lover(self, player_name):
        for player in self.players:
            if player.name == player_name:
                player.lover = True

    # returns a suggestion based of the number of people playing
    def make_suggestions(self, n):
        suggestions = {"werewolves": 1, "whitewerewolf": 1, "seer": 0, "hunter": 1, "witch": 1, "amor": 0}
        for i in range(7, n + 1, 1):
            if i % 2 == 0:
                suggestions["werewolves"] += 1
            if i == 8:
                suggestions["seer"] += 1
            elif i == 10:
                suggestions["amor"] += 1
        return suggestions


class Player:
    id = 0
    def __init__(self, name, role=None):
        self.id = Player.id
        self.name = name
        self.role = role
        self.dead = False
        self.imgPath = None
        self.lover = False
        self.health_potion = None
        self.death_potion = None
        Player.id += 1


# Check if there are normal werewolves alive (used as filter to enter whitewerewolf phase)
def normal_werewolf(people_alive, ):
    # checks if there is a player object with the role "werewolf" in a given list
    for nw in people_alive:
        if nw.role == "werewolf":
            return True
    return False


# Check if there is a white werewolf alive (used as filter to enter whitewerewolf phase)
def white_alive(people_alive):
    # checks if there is a player object with the role "whitewerewolf" in a given list
    for ww in people_alive:
        if ww.role == "whitewerewolf":
            return True
    return False


# Check if there is a seer alive (used as filter to enter seer phase)
def seer_alive(people_alive):
    for s in people_alive:
        if s.role == "seer":
            return True
    return False


# Check if there is a witch alive (used as filter to enter witch phase)
def witch_alive(people_alive):
    for w in people_alive:
        if w.role == "witch":
            return w
    return False


# Check if there are villagers alive (used as filter ot enter sleepwalking phase)
def villagers_alive(people_alive):
    villagers = []
    for v in people_alive:
        if v.role == "villager":
            villagers.append(v)
    if len(villagers) > 0:
        return villagers
    return False


# Method to recreate the kill function
def kill(people_alive, victim):
    # Argument victim is given from the value we retrieve from the web
    if victim:
        # Find the victim, set that player.dead = True, and remove it from the people_alive list
        for player in people_alive:
            if player.id == int(victim):
                player.dead = True
                people_alive.remove(player)
                return player


# Check if the killed person is a lover, if yes, kill the lover as well
def lovers_skill(people_alive, killed):
    # killed = Player object
    for player in people_alive:
        if player.lover and killed.id != player.id:
            kill(people_alive, str(player.id))
            return player


# Check if lovers win condition is reached, if yes, the game is over.
def lovers_win(people_alive):
    if len(people_alive) == 2:
        if people_alive[0].lover and people_alive[1].lover:
            return True
    return False


# Check if whitewerewolf wins condition is reached, if yes, the game is over.
def whitewerewolf_win(people_alive):
    for p in people_alive:
        if p.role == "whitewerewolf":
            if len(people_alive) < 3:
                return True
    return False


# Check if villagers win condition is reached, if yes, the game is over.
def villagers_win(people_alive):
    for p in people_alive:
        if p.role == "werewolf" or p.role == "whitewerewolf":
            return False

    return True


# Check if werewolves win condition is reached, if yes, the game is over.
def werewolves_win(people_alive):
    roles = ["seer", "witch", "amor", "hunter", "villager"]

    if len(people_alive) == 2:
        for p in people_alive:
            if p.role == "werewolf":
                return True

    for w in people_alive:
        if w.role in roles:
            return False

    return True


# Functions for setup
# assigns players from a list in the post request to a WWManagementSystem
def get_player(request, wwSystem):
    request_players = request.POST.getlist("players")
    # set() != len() so we do not have any duplicates
    if len(set(request_players)) != len(request_players):
        return False
    wwSystem.players = []
    for player in request_players:
        if player.strip() != "":
            wwSystem.add_player(player)
    Player.id = 0 # class attribute gets set to 0
    return True

# check if the role_numbers in the post request are correct
def check_role_numbers(request, wwSystem):
    data = dict(request.POST.lists())
    count = 0
    for key, value in data.items():
        if key == 'csrfmiddlewaretoken':
            continue
        try:
            count += int(value[0])
        except:
            continue
    # if there are no werewolves or whitewerewolves return False
    if data["werewolf"][0] == "":
        if data["whitewerewolf"][0] == "":
            return False
    # if there are no roles at all return False
    if count == 0:
        return False
    elif count <= len(wwSystem.players):
        return True
    # if there are more roles than players
    else:
        return False

# get the role numbers and store them in a dict in a WWManagementSystem class
def get_role_numbers(request, wwSystem):
    # assigns key and value to the WWManagementSystem object attribute
    wwSystem.roleNumbers = {}
    data = dict(request.POST.lists()) # get post data
    for key, value in data.items():
        if key == 'csrfmiddlewaretoken':
            continue
        try:
            wwSystem.roleNumbers[key] = int(value[0])
        except:
            wwSystem.roleNumbers[key] = 0

# returns a list of players without any role from a given list of Player objects
def get_players_without_any_role(player_list):
    players_without_any_role = []
    for player in player_list:
        if isinstance(player, Player):
            if player.role is None or player.role == "":
                players_without_any_role.append(player)
    return players_without_any_role
