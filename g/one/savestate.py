from pyglet.resource import get_settings_path

from g.one.game_pickler import GamePickler, GameUnpickler


def get_filename(statenum):
    return get_settings_path("g-one") + "/save_" + str(statenum) + ".p"


def get_state_info(statenum):
    filename = get_filename(statenum)
    try:
        with open(filename, 'rb') as f:
            return GameUnpickler(f, None).load()
    except Exception:
        return None


def save_state(statenum, game):
    filename = get_filename(statenum)
    with open(filename, 'wb') as f:
        pickler = GamePickler(f)
        game_info = str(len(game.players))
        game_info += " player, "
        if game.earth:
            game_info += "Earthlings, "
        else:
            game_info += "Aliens, "
        game_info += "Level 1, "
        game_info += ["Normal", "Hard"][game.difficulty]
        pickler.dump(game_info)
        pickler.dump(game)


def load_state(statenum, window):
    filename = get_filename(statenum)
    with open(filename, 'rb') as f:
        pickler = GameUnpickler(f, window)
        pickler.load()
        return pickler.load()
