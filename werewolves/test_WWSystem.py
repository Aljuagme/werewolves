import pytest
from werewolves import views  # dont go import * !
from django.contrib.sessions.middleware import SessionMiddleware  # to work with sessions in RequestFactory
from werewolves.WWManagementSystem import *
from django.test import RequestFactory


# Tests for python class "WWManagementSystem" in WWManagementSystem.py
def test_add_player():
    """tests if a Player object is created and assigned in the WWMSystem"""
    # setup
    w = WWManagementSystem()
    name = "Steve"

    # method
    w.add_player(name)

    # actual test
    assert name in [player.name for player in w.players]


def test_get_player_by_name():
    """tests if the returned object has the correct name"""
    # setup
    w = WWManagementSystem()
    name = "Steve"

    # method
    w.add_player(name)

    # test
    assert w.get_player_by_name(name).name == name


def test_assign_role():
    """tests if assigned role is correct"""
    # setup
    w = WWManagementSystem()
    name = "Steve"
    w.add_player(name)
    role = "villager"

    # method
    w.assign_role(name, role)

    # test
    assert w.get_player_by_name(name).role == role


def test_assign_lover():
    """tests if player object gets gets lover attribute set to True"""
    # setup
    w = WWManagementSystem()
    name = "Steve"
    w.add_player(name)

    # method
    w.assign_lover(name)

    # test
    assert w.get_player_by_name(name).lover is True

def test_make_suggestions():
    """tests if it return the correct suggestion"""
    # setup
    w = WWManagementSystem()
    assert w.make_suggestions(5) == {"werewolves": 1, "whitewerewolf": 1, "seer": 0, "hunter": 1, "witch": 1, "amor": 0}
    assert w.make_suggestions(6) == {"werewolves": 1, "whitewerewolf": 1, "seer": 0, "hunter": 1, "witch": 1, "amor": 0}
    assert w.make_suggestions(7) == {"werewolves": 1, "whitewerewolf": 1, "seer": 0, "hunter": 1, "witch": 1, "amor": 0}
    assert w.make_suggestions(8) == {"werewolves": 2, "whitewerewolf": 1, "seer": 1, "hunter": 1, "witch": 1, "amor": 0}
    assert w.make_suggestions(10) == {"werewolves": 3, "whitewerewolf": 1, "seer": 1, "hunter": 1, "witch": 1, "amor": 1}
    assert w.make_suggestions(14) == {"werewolves": 5, "whitewerewolf": 1, "seer": 1, "hunter": 1, "witch": 1, "amor": 1}


# Tests for function with request parameter in WWManagementSystem.py

def test_get_player():
    """tests if player names are assigned in the WWManagementSystem from post request"""
    # setup
    w = WWManagementSystem()
    player_list = ["Thomas", "Steve", "Alvaro"]
    factory = RequestFactory()
    path = "/werewolves/setup"
    r = factory.post(path, {"players": player_list})

    # method
    get_player(r, w)

    # test
    system_players = [player.name for player in w.players]
    assert player_list == system_players


def test_check_role_numbers():
    """tests if role numbers from the post request are checked correctly"""
    # setup

    w1 = WWManagementSystem()
    w2 = WWManagementSystem()
    player_list1 = ["Thomas", "Steve", "Alvaro"]  # player list with acceptable length
    player_list2 = ["Thomas"]  # player list with unacceptable length
    role_numbers_request = {"csrfmiddlewaretoken": "some_csrfmiddlewaretoken", "werewolf": 2, "whitewerewolf": "",
                            "villager": 1}
    no_roles_numbers_request = {"csrfmiddlewaretoken": "some_csrfmiddlewaretoken", "werewolf": "", "whitewerewolf": "",
                                "villager": ""}
    no_werewolves_roles_numbers_request = {"csrfmiddlewaretoken": "some_csrfmiddlewaretoken", "werewolf": "",
                                           "whitewerewolf": "", "villager": ""}
    for player in player_list1:  # Assign good list
        w1.add_player(player)
    for player in player_list2:  # Assign bad list
        w2.add_player(player)

    path = "/werewolves/setup_night"
    factory = RequestFactory()
    r = factory.post(path, role_numbers_request)
    r_no_roles = factory.post(path, no_roles_numbers_request)
    r_no_werewolves = factory.post(path, no_werewolves_roles_numbers_request)
    # method and test
    assert check_role_numbers(r, w1) is True
    assert check_role_numbers(r, w2) is False
    assert check_role_numbers(r_no_roles, w1) is False
    assert check_role_numbers(r_no_roles, w2) is False
    assert check_role_numbers(r_no_werewolves, w1) is False
    assert check_role_numbers(r_no_werewolves, w2) is False


def test_get_role_numbers():
    """tests if the role numbers get assigned in the class WWManagementSystem"""
    # setup
    w = WWManagementSystem()
    role_numbers_request = {"csrfmiddlewaretoken": "some_csrfmiddlewaretoken", "werewolf": 2, "seer": 1, "witch": 1,
                            "villager": 1}
    role_numbers = {"werewolf": 2, "seer": 1, "witch": 1, "villager": 1}

    path = "/werewolves/setup_night"
    factory = RequestFactory()
    r = factory.post(path, role_numbers_request)

    # method
    get_role_numbers(r, w)

    # test
    assert role_numbers == w.roleNumbers


def test_get_players_without_any_role():
    """tests if every Player object in the returned list of players has no role (role==None)"""
    # setup
    players_with_role = [Player("Satan", role="whitewerewolf"), Player("Deepkan", role="werewolf"),
                         Player("Steve", role="seer")]
    players_without_role = [Player("Thomas"), Player("Alvaro")]

    # method and test
    assert (players_with_role == get_players_without_any_role(players_with_role)) is False
    assert (players_without_role == get_players_without_any_role(players_without_role)) is True


def test_normal_werewolf():
    """tests if the "werewolf"-alive check is correct"""
    # setup
    players1 = [Player("Thomas", "werewolf"), Player("Steve", "seer"), Player("Alvaro", "villager")]
    players2 = [Player("Thomas", "whitewerewolf"), Player("Steve", "villager"), Player("Alvaro", "villager")]

    # method and test
    assert normal_werewolf(players1) is True
    assert normal_werewolf(players2) is False


def test_white_alive():
    """tests if the "whitewerewolf"-alive check is correct"""
    # setup
    players1 = [Player("Thomas", "werewolf"), Player("Steve", "seer"), Player("Alvaro", "villager")]
    players2 = [Player("Thomas", "whitewerewolf"), Player("Steve", "villager"), Player("Alvaro", "villager")]

    # method and test
    assert white_alive(players1) is False
    assert white_alive(players2) is True


def test_seer_alive():
    """tests if the "seer"-alive check is correct"""
    # setup
    players1 = [Player("Thomas", "werewolf"), Player("Steve", "seer"), Player("Alvaro", "villager")]
    players2 = [Player("Thomas", "whitewerewolf"), Player("Steve", "villager"), Player("Alvaro", "villager")]

    # method and test
    assert seer_alive(players1) is True
    assert seer_alive(players2) is False


def test_witch_alive():
    """tests if the "witch"-alive check is correct"""
    # setup
    players1 = [Player("Thomas", "werewolf"), Player("Steve", "witch"), Player("Alvaro", "villager")]
    witch = players1[1]
    players2 = [Player("Thomas", "whitewerewolf"), Player("Steve", "villager"), Player("Alvaro", "villager")]

    # method and test
    assert witch_alive(players1) == witch
    assert witch_alive(players2) is False


def test_villager_alive():
    """tests if the "villager"-alive check is correct"""
    # setup
    players1 = [Player("Thomas", "werewolf"), Player("Steve", "seer"), Player("Alvaro", "villager")]
    players2 = [Player("Thomas", "whitewerewolf"), Player("Steve", "villager"), Player("Alvaro", "villager")]
    players3 = [Player("Thomas", "whitewerewolf"), Player("Steve", "witch"), Player("Alvaro", "seer")]

    # method and test
    assert len(villagers_alive(players1)) == 1
    assert len(villagers_alive(players2)) == 2
    assert villagers_alive(players3) is False


def test_kill():
    """tests if player with given id in the list of players gets it's "player.dead = True" and removed from the list"""
    # setup
    Player.id = 0
    players = [Player("Thomas"), Player("Poseidon"), Player("Steve"), Player("Alvaro"), Player("Bernhard")]
    players_length = len(players)
    victim = players[2]

    # method
    return_value = kill(players, victim=victim.id)

    # test
    assert return_value == victim
    assert len(players) == players_length - 1
    assert victim not in players
    assert kill(players, victim=999999) is None
    assert kill(players, victim="999999") is None


def test_lovers_skill():
    """tests if a player with "player.lover == True" is killed"""
    # setup
    Player.id = 0
    p1 = Player("Maria", "villager")
    p1.lover = True
    p2 = Player("Matt", "villager")
    p2.lover = True
    p2.dead = True
    players_alive = []
    players_alive.append(p1)
    players_alive.append(Player("Thomas", "villager"))
    players_alive.append(Player("Alvaro", "villager"))
    # method
    lovers_skill(players_alive, killed=p2)

    # test
    assert p1 not in players_alive
    assert p1.dead is True

def test_lovers_win():
    """tests if the return value is correct"""
    # setup
    p1 = Player("Thomas")
    p1.lover = True
    p2 = Player("Alvaro")
    p2.lover = True
    players_1 = [p1, p2]
    players_2 = [p1, p2, Player("Steve")]
    players_3 = [Player("Poseidon"), Player("Satan")]
    # method and test
    assert lovers_win(players_1) is True
    assert lovers_win(players_2) is False
    assert lovers_win(players_3) is False

def test_whitewerewolf_win():
    """tests if the return value is correct"""
    # setup
    players_1 = [Player("Poseidon"), Player("Satan", "whitewerewolf")]
    players_2 = [Player("Poseidon"), Player("Satan")]
    players_3 = [Player("Poseidon"), Player("Satan"), Player("Thomas", "whitewerewolf")]
    players_4 = [Player("Poseidon"), Player("Satan"), Player("Thomas")]
    # method and test
    assert whitewerewolf_win(players_1) is True
    assert whitewerewolf_win(players_2) is False
    assert whitewerewolf_win(players_3) is False
    assert whitewerewolf_win(players_4) is False

def test_villager_win():
    """tests if the return value is correct"""
    # setup
    players_1 = [Player("Poseidon", "villager"), Player("Satan", "whitewerewolf")]
    players_2 = [Player("Poseidon", "villager"), Player("Satan", "werewolf")]
    players_3 = [Player("Poseidon", "villager"), Player("Thomas", "villager")]
    players_4 = [Player("Poseidon"), Player("Satan"), Player("Thomas")]
    # method and test
    assert villagers_win(players_1) is False
    assert villagers_win(players_2) is False
    assert villagers_win(players_3) is True
    assert villagers_win(players_4) is True

def test_werewolves_win():
    """tests if the return value is correct"""
    # setup
    players_1 = [Player("Poseidon", "villager"), Player("Satan", "whitewerewolf"), Player("P1", "werewolf")]
    players_2 = [Player("Poseidon", "villager"), Player("Satan", "villager"), Player("P1", "werewolf")]
    players_3 = [Player("Satan", "whitewerewolf"), Player("P1", "werewolf")]
    players_4 = [Player("Poseidon", "hunter"), Player("Satan", "witch")]
    players_5 = [Player("Satan", "villager"), Player("P1", "werewolf")]
    # method and test
    assert werewolves_win(players_1) is False
    assert werewolves_win(players_2) is False
    assert werewolves_win(players_3) is True
    assert werewolves_win(players_4) is False
    assert werewolves_win(players_5) is True

def test_index():
    """tests if the index page gets rendered correctly"""
    # setup
    path = "/werewolves/index"
    factory = RequestFactory()
    r = factory.get(path)
    # method
    response = views.index(r)
    # test
    assert response.status_code == 200
    assert b"THE WEREWOLVES OF MILLER" in response.content
    assert b"Enter the forest..." in response.content


@pytest.mark.django_db
def test_setup():
    """"tests all post requests in setup()"""
    # setup to use sessions in get tests
    middleware = SessionMiddleware()

    # setup with empty request.session["players"]
    path = "/werewolves/setup"
    factory = RequestFactory()
    r_get_1 = factory.get(path)
    middleware.process_request(r_get_1)
    # method
    get_response_1 = views.setup(r_get_1)
    # test standard get request (no players in sessions)
    assert r_get_1.session["players"] == []
    assert get_response_1.status_code == 200
    assert b"Load recent players" in get_response_1.content

    # setup with NON-empty request.session["players"]
    r_get_2 = factory.get(path)
    middleware.process_request(r_get_2)
    to_be_loaded_players = ["Thomas", "Alvaro", "Steve"]
    r_get_2.session["players"] = to_be_loaded_players
    # method
    get_response_2 = views.setup(r_get_2, testing_session=True)
    # test
    assert r_get_2.session["players"] == to_be_loaded_players
    assert get_response_2.status_code == 200
    for player in to_be_loaded_players:
        assert bytearray(f"{player}", "utf-8") in get_response_2.content
    assert b"Load recent players" in get_response_2.content

    # setup to test post with "load_players" key
    data_load_players = {"load_players": ""}
    r_post_1 = factory.post(path, data_load_players)
    middleware.process_request(r_post_1)
    # method
    post_return_1 = views.setup(r_post_1)
    # test
    assert post_return_1.status_code == 302
    assert post_return_1.url == path

    # setup to test post with "players" key
    user_input_players_1 = ["Poseidon", "Satan", "God", "Gzuz", "Alvaro", "Thomas", "Steve"]
    user_input_players_2 = []
    for i in range(30):
        user_input_players_2.append(f"player_{i}")
    data_players = {"players"}
    post_return_path_1 = "/werewolves/setup_night"
    r_post_2 = factory.post(path, {"players": user_input_players_1})
    middleware.process_request(r_post_2)
    r_post_3 = factory.post(path, {"players": user_input_players_2})
    middleware.process_request(r_post_3)
    # method
    post_return_2 = views.setup(r_post_2)
    post_return_3 = views.setup(r_post_3)
    # test
    # test r_post_2
    assert r_post_2.session["players"] == user_input_players_1
    assert post_return_2.status_code == 302
    assert post_return_2.url == post_return_path_1
    # test r_post_3
    assert r_post_3.session["players"] == []
    assert post_return_3.status_code == 302
    assert post_return_3.url == path


def test_setup_night():
    """tests if the get and post request works correctly (get roles, do recommendation,...)"""
    # setup to test standard get request
    path = "/werewolves/setup_night"
    factory = RequestFactory()
    r_get = factory.get(path)
    # method
    get_response = views.setup_night(r_get, testing=True)
    # test
    assert get_response.status_code == 200
    assert b"Number of players: 4" in get_response.content  # 4 test players are passed if "testing=True"

    # setup to test post request
    response_path = "/werewolves/setup_night_werewolves"
    role_number_1 = {"werewolf": "1",
                     "whitewerewolf": "",
                     "seer": "1",
                     "witch": "",
                     "hunter": "",
                     "amor": "",
                     "villager": "", }
    role_number_2 = {"werewolf": "2",
                     "whitewerewolf": "",
                     "seer": "1",
                     "witch": "1",
                     "hunter": "1",
                     "amor": "",
                     "villager": "5", }
    r_post_1 = factory.post(path, role_number_1)
    r_post_2 = factory.post(path, role_number_2)
    # method
    post_return_1 = views.setup_night(r_post_1, testing=True)
    post_return_2 = views.setup_night(r_post_2, testing=True)
    # test
    assert post_return_1.status_code == 302
    assert post_return_1.url == response_path
    assert post_return_2.status_code == 302
    assert post_return_2.url == path


def test_setup_night_seer():
    """tests get and post requests and responses"""
    # setup to test standard get request
    factory = RequestFactory()
    path = "/werewolves/setup_night_seer"
    response_path = "/werewolves/setup_night_witch"
    role_number_1 = {"werewolf": 1,
                     "whitewerewolf": 0,
                     "seer": 1,
                     "witch": 0,
                     "hunter": 0,
                     "amor": 0,
                     "villager": 0}
    role_number_2 = {"werewolf": 1,
                     "whitewerewolf": 0,
                     "seer": 0,
                     "witch": 0,
                     "hunter": 0,
                     "amor": 0,
                     "villager": 0}
    r_get = factory.get(path)
    # method
    get_response_1 = views.setup_night_seer(r_get, testing=(True, role_number_1))
    get_response_2 = views.setup_night_seer(r_get, testing=(True, role_number_2))
    # test
    assert get_response_1.status_code == 200
    assert b"Seer:" in get_response_1.content
    assert get_response_2.status_code == 302
    assert get_response_2.url == response_path

    # setup to test post request
    post_request_data = {'csrfmiddlewaretoken': ['sCfG40WamMX23fVPLx2HYOhLdod93WBYB19tvCkl3qM13kvf3p4QPpWXhwl3pOsE'],
                         'seer': ['Steve']}
    r_post = factory.post(path, post_request_data)
    # method
    post_response = views.setup_night_seer(r_post)
    # test
    assert post_response.status_code == 302
    assert post_response.url == response_path


def test_setup_night_werewolves():
    """tests get and post requests and responses"""
    # setup for standard get request
    factory = RequestFactory()
    path = "/werewolves/setup_night_werewolves"
    response_path = "/werewolves/setup_night_white_werewolf"
    role_number_1 = {"werewolf": 1,
                     "whitewerewolf": 0,
                     "seer": 1,
                     "witch": 0,
                     "hunter": 0,
                     "amor": 0,
                     "villager": 0}
    role_number_2 = {"werewolf": 0,
                     "whitewerewolf": 1,
                     "seer": 0,
                     "witch": 0,
                     "hunter": 0,
                     "amor": 0,
                     "villager": 0}
    r_get = factory.get(path)
    # method
    get_response_1 = views.setup_night_werewolves(r_get, testing=(True, role_number_1))
    get_response_2 = views.setup_night_werewolves(r_get, testing=(True, role_number_2))
    # test
    assert get_response_1.status_code == 200
    assert b"Werewolves:" in get_response_1.content
    assert get_response_2.status_code == 302
    assert get_response_2.url == response_path

    # setup to test post request
    post_request_data = {'csrfmiddlewaretoken': ['sCfG40WamMX23fVPLx2HYOhLdod93WBYB19tvCkl3qM13kvf3p4QPpWXhwl3pOsE'],
                         'werewolf': ['Steve']}
    r_post = factory.post(path, post_request_data)
    # method
    post_response = views.setup_night_werewolves(r_post)
    # test
    assert post_response.status_code == 302
    assert post_response.url == response_path


def test_setup_night_white_werewolf():
    """tests get and post requests and responses"""
    # setup for standard get request
    factory = RequestFactory()
    path = "/werewolves/setup_night_white_werewolf"
    response_path = "/werewolves/setup_night_seer"
    role_number_1 = {"werewolf": 0,
                     "whitewerewolf": 1,
                     "seer": 1,
                     "witch": 0,
                     "hunter": 0,
                     "amor": 0,
                     "villager": 0}
    role_number_2 = {"werewolf": 1,
                     "whitewerewolf": 0,
                     "seer": 0,
                     "witch": 0,
                     "hunter": 0,
                     "amor": 0,
                     "villager": 0}
    r_get = factory.get(path)
    # method
    get_response_1 = views.setup_night_white_werewolf(r_get, testing=(True, role_number_1))
    get_response_2 = views.setup_night_white_werewolf(r_get, testing=(True, role_number_2))
    # test
    assert get_response_1.status_code == 200
    assert b"White Werewolf:" in get_response_1.content
    assert get_response_2.status_code == 302
    assert get_response_2.url == response_path

    # setup to test post request
    post_request_data = {'csrfmiddlewaretoken': ['sCfG40WamMX23fVPLx2HYOhLdod93WBYB19tvCkl3qM13kvf3p4QPpWXhwl3pOsE'],
                         'whitewerewolf': ['Steve']}
    r_post = factory.post(path, post_request_data)
    # method
    post_response = views.setup_night_white_werewolf(r_post)
    # test
    assert post_response.status_code == 302
    assert post_response.url == response_path


def test_setup_night_witch():
    """tests get and post requests and responses"""
    # setup for standard get request
    factory = RequestFactory()
    path = "/werewolves/setup_night_witch"
    response_path = "/werewolves/setup_night_hunter"
    role_number_1 = {"werewolf": 0,
                     "whitewerewolf": 1,
                     "seer": 1,
                     "witch": 1,
                     "hunter": 0,
                     "amor": 0,
                     "villager": 0}
    role_number_2 = {"werewolf": 1,
                     "whitewerewolf": 0,
                     "seer": 0,
                     "witch": 0,
                     "hunter": 0,
                     "amor": 0,
                     "villager": 0}
    r_get = factory.get(path)
    # method
    get_response_1 = views.setup_night_witch(r_get, testing=(True, role_number_1))
    get_response_2 = views.setup_night_witch(r_get, testing=(True, role_number_2))
    # test
    assert get_response_1.status_code == 200
    assert b"Witch:" in get_response_1.content
    assert get_response_2.status_code == 302
    assert get_response_2.url == response_path

    # setup to test post request
    post_request_data = {'csrfmiddlewaretoken': ['sCfG40WamMX23fVPLx2HYOhLdod93WBYB19tvCkl3qM13kvf3p4QPpWXhwl3pOsE'],
                         'witch': ['Steve']}
    r_post = factory.post(path, post_request_data)
    # method
    post_response = views.setup_night_witch(r_post)
    # test
    assert post_response.status_code == 302
    assert post_response.url == response_path


def test_setup_night_hunter():
    """tests get and post requests and responses"""
    # setup for standard get request
    factory = RequestFactory()
    path = "/werewolves/setup_night_hunter"
    response_path = "/werewolves/setup_night_amor"
    role_number_1 = {"werewolf": 0,
                     "whitewerewolf": 1,
                     "seer": 1,
                     "witch": 0,
                     "hunter": 1,
                     "amor": 0,
                     "villager": 0}
    role_number_2 = {"werewolf": 1,
                     "whitewerewolf": 0,
                     "seer": 0,
                     "witch": 0,
                     "hunter": 0,
                     "amor": 0,
                     "villager": 0}
    r_get = factory.get(path)
    # method
    get_response_1 = views.setup_night_hunter(r_get, testing=(True, role_number_1))
    get_response_2 = views.setup_night_hunter(r_get, testing=(True, role_number_2))
    # test
    assert get_response_1.status_code == 200
    assert b"Hunter:" in get_response_1.content
    assert get_response_2.status_code == 302
    assert get_response_2.url == response_path

    # setup to test post request
    post_request_data = {'csrfmiddlewaretoken': ['sCfG40WamMX23fVPLx2HYOhLdod93WBYB19tvCkl3qM13kvf3p4QPpWXhwl3pOsE'],
                         'hunter': ['Steve']}
    r_post = factory.post(path, post_request_data)
    # method
    post_response = views.setup_night_hunter(r_post)
    # test
    assert post_response.status_code == 302
    assert post_response.url == response_path


def test_setup_night_amor():
    """tests get and post requests and responses"""
    # setup for standard get request
    factory = RequestFactory()
    path = "/werewolves/setup_night_amor"
    response_path = "/werewolves/night"
    role_number_1 = {"werewolf": 0,
                     "whitewerewolf": 1,
                     "seer": 1,
                     "witch": 0,
                     "hunter": 1,
                     "amor": 1,
                     "villager": 0}
    role_number_2 = {"werewolf": 1,
                     "whitewerewolf": 0,
                     "seer": 0,
                     "witch": 0,
                     "hunter": 0,
                     "amor": 0,
                     "villager": 0}
    r_get = factory.get(path)
    # method
    get_response_1 = views.setup_night_amor(r_get, testing=(True, role_number_1))
    get_response_2 = views.setup_night_amor(r_get, testing=(True, role_number_2))
    # test
    assert get_response_1.status_code == 200
    assert b"Amor:" in get_response_1.content
    assert get_response_2.status_code == 302
    assert get_response_2.url == response_path

    # setup to test post request
    post_request_data = {'csrfmiddlewaretoken': ['sCfG40WamMX23fVPLx2HYOhLdod93WBYB19tvCkl3qM13kvf3p4QPpWXhwl3pOsE'],
                         'amor': ['Satan']}
    r_post = factory.post(path, post_request_data)
    # method
    post_response = views.setup_night_amor(r_post)
    # test
    assert post_response.status_code == 302
    assert post_response.url == response_path


def test_day():
    """tests if get and post requests and responses work correctly"""
    # GET REQUESTS
    # setup for standard get request (victim is no hunter and no lover)
    Player.id = 0
    path = "/werewolves/day"
    factory = RequestFactory()
    response_path = "/werewolves/hunter"
    p1 = Player("Thomas")
    people_alive = [p1, Player("Alvaro"), Player("Steve")]
    werewolves_victim = [p1]
    r_get_1 = factory.get(path)
    # method
    get_response_1 = views.day(r_get_1, testing=(True, [people_alive, werewolves_victim]))
    # test
    assert p1 not in werewolves_victim
    assert p1 not in people_alive
    assert get_response_1.status_code == 302
    assert get_response_1.url == path

    # setup for get request where killed player is hunter (no lovers)
    Player.id = 0
    p1 = Player("Thomas", "hunter")
    people_alive = [p1, Player("Alvaro"), Player("Steve")]
    werewolves_victim = [p1]
    # method
    get_response_2 = views.day(r_get_1, testing=(True, [people_alive, werewolves_victim]))
    # test
    assert p1 not in people_alive
    assert p1 not in werewolves_victim
    assert get_response_2.status_code == 200
    assert b"Hunter, you may take one with you" in get_response_2.content

    # setup for get request where killed player is lover (no hunter)
    Player.id = 0
    p1 = Player("Thomas", "villager")
    p1.lover = True
    p2 = Player("Poseidon", "villager")
    p2.lover = True
    people_alive = [p1, p2, Player("Alvaro", "villager"), Player("Steve", "villager")]
    werewolves_victim = [p1]
    # method
    get_response_3 = views.day(r_get_1, testing=(True, [people_alive, werewolves_victim]))
    # test
    assert p1 not in people_alive
    assert p1 not in werewolves_victim
    assert p2 not in people_alive
    assert p2 not in werewolves_victim
    assert get_response_3.status_code == 302
    assert get_response_3.url == path

    # setup for get request where killed player is lover and the other lover is a hunter
    Player.id = 0
    p1 = Player("Thomas", "villager")
    p1.lover = True
    p2 = Player("Poseidon", "hunter")
    p2.lover = True
    people_alive = [p1, p2, Player("Alvaro", "villager"), Player("Steve", "villager")]
    werewolves_victim = [p1]
    # method
    get_response_4 = views.day(r_get_1, testing=(True, [people_alive, werewolves_victim]))
    # test
    assert p1 not in people_alive
    assert p1 not in werewolves_victim
    assert p2 not in people_alive
    assert p2 not in werewolves_victim
    assert get_response_4.status_code == 200
    assert b"Hunter, you may take one with you" in get_response_4.content

    # setup for get request where killed player is both a hunter and lover
    Player.id = 0
    p1 = Player("Thomas", "hunter")
    p1.lover = True
    p2 = Player("Poseidon", "villager")
    p2.lover = True
    people_alive = [p1, p2, Player("Alvaro", "villager"), Player("Steve", "villager")]
    werewolves_victim = [p1]
    # method
    get_response_5 = views.day(r_get_1, testing=(True, [people_alive, werewolves_victim]))
    # test
    assert p1 not in people_alive
    assert p1 not in werewolves_victim
    assert p2 not in people_alive
    assert p2 not in werewolves_victim
    assert get_response_5.status_code == 200
    assert b"Hunter, you may take one with you" in get_response_5.content

    # POST REQUESTS
    # setup for standard post request without input
    r_post_1 = factory.post(path, {"chosen": ""})
    # method
    post_response_1 = views.day(r_post_1)
    # test
    assert post_response_1.status_code == 302
    assert post_response_1.url == path

    # setup for post request with "chosen" (victim)
    Player.id = 0
    chosen = {"victim": "1"}
    people_alive = [Player("Poseidon", "villager"), Player("Thomas", "villager"), Player("Alvaro", "villager"),
                    Player("Steve", "villager")]
    r_post_2 = factory.post(path, chosen)
    for player in people_alive:
        if player.id == int(chosen["victim"]):
            chosen_player = player
    # method
    post_response_2 = views.day(r_post_2, testing=(True, [people_alive, None]))
    # test
    assert post_response_2.status_code == 302
    assert post_response_2.url == path
    assert chosen_player not in people_alive

    # setup for post request with "chosen" (victim) with role hunter
    Player.id = 0
    chosen = {"victim": "1"}
    people_alive = [Player("Poseidon", "villager"), Player("Thomas", "hunter"), Player("Alvaro", "villager"),
                    Player("Steve", "villager")]
    r_post_3 = factory.post(path, chosen)
    for player in people_alive:
        if player.id == int(chosen["victim"]):
            chosen_player = player
    # method
    post_response_3 = views.day(r_post_3, testing=(True, [people_alive, None]))
    # test
    assert post_response_3.status_code == 200
    assert b"Hunter, you may take one with you" in post_response_3.content
    assert chosen_player not in people_alive

    # setup for post request with "chosen" (victim) with both role hunter and attribute lover
    Player.id = 0
    chosen = {"victim": "4"}
    people_alive = [Player("Poseidon", "villager"), Player("Thomas", "villager"), Player("Alvaro", "villager"),
                    Player("Steve", "villager")]
    p1 = Player("Satan", "hunter")
    p1.lover = True
    p2 = Player("Satan", "seer")
    p2.lover = True
    people_alive.append(p1)
    people_alive.append(p2)
    r_post_4 = factory.post(path, chosen)
    for player in people_alive:
        if player.id == int(chosen["victim"]):
            chosen_player = player
    # method
    post_response_4 = views.day(r_post_4, testing=(True, [people_alive, None]))
    # test
    assert post_response_4.status_code == 200
    assert b"Hunter, you may take one with you" in post_response_4.content
    assert chosen_player not in people_alive
    assert p2 not in people_alive

    # setup for post request with "chosen" (victim) with lover attribute
    Player.id = 0
    chosen = {"victim": "4"}
    people_alive = [Player("Poseidon", "villager"), Player("Thomas", "villager"), Player("Alvaro", "villager"),
                    Player("Steve", "villager")]
    p1 = Player("Satan", "villager")
    p1.lover = True
    p2 = Player("Satan", "seer")
    p2.lover = True
    people_alive.append(p1)
    people_alive.append(p2)
    r_post_5 = factory.post(path, chosen)
    for player in people_alive:
        if player.id == int(chosen["victim"]):
            chosen_player = player
    # method
    post_response_5 = views.day(r_post_5, testing=(True, [people_alive, None]))
    # test
    assert post_response_5.status_code == 302
    assert post_response_5.url == path
    assert p1 not in people_alive
    assert p2 not in people_alive

    # setup for post request with "chosen" (victim) with lover attribute and other lover is also a hunter
    Player.id = 0
    chosen = {"victim": "4"}
    people_alive = [Player("Poseidon", "villager"), Player("Thomas", "villager"), Player("Alvaro", "villager"),
                    Player("Steve", "villager")]
    p1 = Player("Satan", "villager")
    p1.lover = True
    p2 = Player("Satan", "hunter")
    p2.lover = True
    people_alive.append(p1)
    people_alive.append(p2)
    r_post_6 = factory.post(path, chosen)
    for player in people_alive:
        if player.id == int(chosen["victim"]):
            chosen_player = player
    # method
    post_response_6 = views.day(r_post_6, testing=(True, [people_alive, None]))
    # test
    assert post_response_6.status_code == 200
    assert b"Hunter, you may take one with you" in post_response_6.content
    assert p1 not in people_alive
    assert p2 not in people_alive


def test_night():
    """tests if get and post requests and responses work correctly"""
    # GET REQUESTS
    # setup for get request where seer is alive
    Player.id = 0
    path = "/werewolves/night"
    factory = RequestFactory()
    people_alive = [Player("Poseidon", "seer"), Player("Thomas", "villager"), Player("Alvaro", "villager"),
                    Player("Steve", "villager")]
    r_get = factory.get(path)
    # method
    get_response_1 = views.night(r_get, testing=(True, people_alive))
    # test
    assert get_response_1.status_code == 200
    assert b"Reveal identity" in get_response_1.content

    # setup for get request where seer is dead and at least one villager alive
    Player.id = 0
    path = "/werewolves/night"
    factory = RequestFactory()
    people_alive = [Player("Poseidon", "werewolf"), Player("Thomas", "villager"), Player("Alvaro", "villager"),
                    Player("Steve", "villager")]
    r_get = factory.get(path)
    # method
    get_response_2 = views.night(r_get, testing=(True, people_alive))
    # test
    assert get_response_2.status_code == 200
    assert b"How many sleepwalkers?" in get_response_2.content

    # setup for get request where seer is dead and at least one villager alive
    Player.id = 0
    path = "/werewolves/night"
    response_path = "/werewolves/werewolves_skill"
    factory = RequestFactory()
    people_alive = [Player("Poseidon", "werewolf"), Player("Thomas", "witch"), Player("Alvaro", "hunter"),
                    Player("Steve", "villager")]
    r_get = factory.get(path)
    # method
    get_response_3 = views.night(r_get, testing=(True, people_alive))
    # test
    assert get_response_3.status_code == 302
    assert get_response_3.url == response_path


def test_seer_skill():
    """tests if get and post requests and responses work correctly"""
    # REQUESTS
    # setup for post request where seer does not choose someone
    Player.id = 0
    path = "/werewolves/seer_skill"
    response_path = "/werewolves/night"
    factory = RequestFactory()
    chosen = {"reveal": ""}
    r_post_1 = factory.post(path, chosen)
    # method
    post_response_1 = views.seer_skill(r_post_1)
    # test
    assert post_response_1.status_code == 302
    assert post_response_1.url == response_path

    # setup for post request where seer chooses someone
    Player.id = 0
    seer_list = []
    people_alive = [Player("Poseidon", "werewolf"), Player("Thomas", "witch"), Player("Alvaro", "hunter"),
                    Player("Steve", "amor")]
    p1 = Player("Satan", "whitewerewolf")
    people_alive.append(p1)
    chosen = {"reveal": str(p1.id)}
    r_post_2 = factory.post(path, chosen)
    # method
    post_response_2 = views.seer_skill(r_post_2, testing=(True, (people_alive, seer_list)))
    # test
    assert p1 in seer_list
    assert post_response_2.status_code == 302
    assert post_response_2.url == response_path


def test_sleep_walking():
    """tests if the get request and response work correctly"""
    # REQUESTS
    # setup for get request with more than 1 villager
    Player.id = 0
    factory = RequestFactory()
    path = "/werewolves/sleep_walking"
    people_alive = [Player("Poseidon", "werewolf"), Player("Thomas", "villager"), Player("Alvaro", "villager"),
                    Player("Steve", "amor")]
    r_get = factory.get(path)
    # method
    get_response_1 = views.sleep_walking(r_get, testing=(True, people_alive))
    # test
    assert get_response_1.status_code == 200
    assert b"How many sleepwalkers?" in get_response_1.content

    # setup for get request with <= 1 villager
    response_path = "/werewolves/night"
    people_alive = [Player("Poseidon", "werewolf"), Player("Thomas", "hunter"), Player("Alvaro", "villager"),
                    Player("Steve", "amor")]
    r_get = factory.get(path)
    # method
    get_response_2 = views.sleep_walking(r_get, testing=(True, people_alive))
    # test
    assert get_response_2.status_code == 302
    assert get_response_2.url == response_path


def test_sleep_1():
    """tests if get and post requests and responses work correctly"""
    # GET REQUESTS
    # setup for standard get
    Player.id = 0
    factory = RequestFactory()
    path = "/werewolves/sleep_1"
    r_get = factory.get(path)
    # method
    get_response = views.sleep_1(r_get)
    # test
    assert get_response.status_code == 200
    assert b"Sleep Walking" not in get_response.content
    assert b"Reveal identity" in get_response.content

    # POST REQUESTS
    # setup for post request with id of player to reveal
    Player.id = 0
    people_alive = [Player("Poseidon", "werewolf"), Player("Thomas", "villager"), Player("Alvaro", "villager"),
                    Player("Steve", "amor")]
    p1 = Player("Satan", "werewolf")
    people_alive.append(p1)
    chosen = {"reveal": str(p1.id)}
    r_post = factory.post(path, chosen)
    # method
    post_response = views.sleep_1(r_post, testing=(True, people_alive))
    # test
    assert post_response.status_code == 200
    assert b"Sleep Walking" not in post_response.content
    assert b"Reveal identity" in post_response.content


def test_sleep_accident():
    """tests if get requests and responses work correctly"""
    # GET REQUESTS
    # setup for standard get request
    Player.id = 0
    factory = RequestFactory()
    path = "/werewolves/sleep_accident"
    r_get = factory.get(path)
    people_alive = [Player("Poseidon", "werewolf"), Player("Thomas", "villager"), Player("Alvaro", "villager"),
                    Player("Steve", "villager")]
    accident_list = []
    werewolves_victim = []
    # method
    get_response = views.sleep_accident(r_get, testing=(True, (people_alive, accident_list, werewolves_victim)))
    # test
    assert len(accident_list) > 0
    assert len(werewolves_victim) > 0
    assert get_response.status_code == 200
    assert b"has died in a terrible accident" in get_response.content


def test_werewolves_skill():
    """tests if get request and response work correctly"""
    # GET REQUESTS
    # setup for standard get request
    Player.id = 0
    factory = RequestFactory()
    path = "/werewolves/werewolves_skill"
    r_get = factory.get(path)
    people_alive = [Player("Poseidon", "werewolf"), Player("Thomas", "villager"), Player("Alvaro", "villager"),
                    Player("Steve", "villager"), Player("Satan", "witch"), Player("Deepak", "whitewerewolf")]
    # method
    get_response = views.werewolves_skill(r_get, testing=(True, people_alive))
    # test
    assert get_response.status_code == 200
    assert b"Werewolves choose the victim" in get_response.content


def test_white_skill():
    """tests if get and post requests and responses work correctly"""
    # GET REQUESTS
    # setup for standard get request
    Player.id = 0
    factory = RequestFactory()
    path = "/werewolves/white_skill"
    r_get = factory.get(path)
    people_alive = [Player("Poseidon", "werewolf"), Player("Thomas", "villager"), Player("Alvaro", "villager"),
                    Player("Steve", "villager"), Player("Satan", "witch"), Player("Deepak", "whitewerewolf")]
    werewolves_victim = []
    # method
    get_response = views.white_skill(r_get, testing=(True, (people_alive, werewolves_victim)))
    # test
    assert get_response.status_code == 200
    assert b"White Werewolf may choose a victim" in get_response.content

    # POST REQUESTS
    # setup for post request
    Player.id = 0
    people_alive = [Player("Poseidon", "werewolf"), Player("Thomas", "villager"), Player("Alvaro", "villager"),
                     Player("Steve", "villager"), Player("Satan", "witch"), Player("Deepak", "whitewerewolf")]
    p1 = Player("Zeus", "villager")
    people_alive.append(p1)
    werewolves_victim = []
    chosen = {"victim": str(p1.id)}
    r_post = factory.post(path, chosen)
    # method
    post_response = views.white_skill(r_post, testing=(True, (people_alive, werewolves_victim)))
    # test
    assert post_response.status_code == 302
    assert p1 in werewolves_victim
    assert post_response.url == path


def test_witch_skill():
    """tests if get and post requests and responses work correctly"""
    # GET REQUESTS
    # setup for standard get request, witch has potion(s)
    factory = RequestFactory()
    path = "/werewolves/witch_skill"
    respone_path = "/werewolves/day"
    Player.id = 0
    people_alive = [Player("Poseidon", "werewolf"), Player("Thomas", "villager"), Player("Alvaro", "villager"),
                     Player("Steve", "villager"), Player("Deepak", "whitewerewolf")]
    p1 = Player("Satan", "witch")
    p1.death_potion = True
    p1.health_potion = True
    people_alive.append(p1)
    werewolves_victim = []
    r_get = factory.get(path)
    # method
    get_response_1 = views.witch_skill(r_get, testing=(True, (people_alive, werewolves_victim)))
    # test
    assert get_response_1.status_code == 200
    assert b"Witch sees all the victims" in get_response_1.content

    # setup for standard get request, witch has no potions
    Player.id = 0
    people_alive = [Player("Poseidon", "werewolf"), Player("Thomas", "villager"), Player("Alvaro", "villager"),
                     Player("Steve", "villager"), Player("Deepak", "whitewerewolf")]
    p1 = Player("Satan", "witch")
    p1.death_potion = False
    p1.health_potion = False
    people_alive.append(p1)
    werewolves_victim = []
    r_get = factory.get(path)
    # method
    get_response_2 = views.witch_skill(r_get, testing=(True, (people_alive, werewolves_victim)))
    # test
    assert get_response_2.status_code == 302
    assert get_response_2.url == respone_path

    # setup for standard get request, witch is dead
    Player.id = 0
    people_alive = [Player("Poseidon", "werewolf"), Player("Thomas", "villager"), Player("Alvaro", "villager"),
                    Player("Steve", "villager"), Player("Deepak", "whitewerewolf")]
    werewolves_victim = []
    r_get = factory.get(path)
    # method
    get_response_3 = views.witch_skill(r_get, testing=(True, (people_alive, werewolves_victim)))
    # test
    assert get_response_3.status_code == 302
    assert get_response_3.url == respone_path

    # POST REQUESTS
    # setup for post request where player gets healed
    Player.id = 0
    people_alive = [Player("Poseidon", "werewolf"), Player("Thomas", "villager"),
                    Player("Steve", "villager"), Player("Deepak", "whitewerewolf")]
    p1 = Player("Alvaro", "villager")
    p2 = Player("Deepak", "witch")
    p2.health_potion = True
    p2.death_potion = True
    people_alive.append(p2)
    werewolves_victim = [p1]
    chosen = {"heal": str(p1.id)}
    r_post_1 = factory.post(path, chosen)
    # method
    post_response_1 = views.witch_skill(r_post_1, testing=(True, (people_alive, werewolves_victim)))
    # test
    assert p2.health_potion is False
    assert p1 not in werewolves_victim
    assert post_response_1.status_code == 302
    assert post_response_1.url == path

    # setup for post request where player gets the death potion
    Player.id = 0
    people_alive = [Player("Poseidon", "werewolf"), Player("Thomas", "villager"),
                    Player("Steve", "villager"), Player("Deepak", "whitewerewolf")]
    p1 = Player("Alvaro", "villager")
    p2 = Player("Deepak", "witch")
    p2.health_potion = True
    p2.death_potion = True
    people_alive.append(p2)
    people_alive.append(p1)
    werewolves_victim = []
    chosen = {"die": str(p1.id)}
    r_post_2 = factory.post(path, chosen)
    # method
    post_response_2 = views.witch_skill(r_post_2, testing=(True, (people_alive, werewolves_victim)))
    # test
    assert p2.death_potion is False
    assert p1 in werewolves_victim
    assert post_response_2.status_code == 302
    assert post_response_2.url == path

    # setup for post request where the victim of the previous page is also shown
    Player.id = 0
    people_alive = [Player("Poseidon", "werewolf"), Player("Thomas", "villager"),
                    Player("Steve", "villager"), Player("Deepak", "whitewerewolf")]
    p1 = Player("Alvaro", "villager")
    p2 = Player("Deepak", "witch")
    p2.health_potion = True
    p2.death_potion = True
    people_alive.append(p2)
    people_alive.append(p1)
    werewolves_victim = []
    chosen = {"victim": str(p1.id)}
    r_post_3 = factory.post(path, chosen)
    # method
    post_response_3 = views.witch_skill(r_post_3, testing=(True, (people_alive, werewolves_victim)))
    # test
    assert p1 in werewolves_victim
    assert post_response_3.status_code == 302
    assert post_response_3.url == path





