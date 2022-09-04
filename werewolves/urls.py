from django.urls import path

from . import views

app_name = "werewolves"

urlpatterns = [
    path("", views.index, name="index"),

    path("day", views.day, name="day"),

    path("setup", views.setup, name="setup"),

    path("setup_night", views.setup_night, name="setup_night"),

    path("setup_night_werewolves", views.setup_night_werewolves, name="setup_night_werewolves"),

    path("setup_night_white_werewolf", views.setup_night_white_werewolf, name="setup_night_white_werewolf"),

    path("setup_night_seer", views.setup_night_seer, name="setup_night_seer"),

    path("setup_night_witch", views.setup_night_witch, name="setup_night_witch"),

    path("setup_night_hunter", views.setup_night_hunter, name="setup_night_hunter"),

    path("setup_night_amor", views.setup_night_amor, name="setup_night_amor"),

    path("night", views.night, name="night"),

    path("end_game", views.end_game, name="end_game"),

    path("seer_skill", views.seer_skill, name="seer_skill"),

    path("werewolves_skill", views.werewolves_skill, name="werewolves_skill"),

    path("sleep_walking", views.sleep_walking, name="sleep_walking"),

    path("white_skill", views.white_skill, name="white_skill"),

    path("witch_skill", views.witch_skill, name="witch_skill"),

    path("sleep_1", views.sleep_1, name="sleep_1"),

    path("sleep_accident", views.sleep_accident, name="sleep_accident"),

]
