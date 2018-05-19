from game_states import GameStates
from render_functions import RenderOrder
from game_messages import Message


def kill_player(player, colors):
    player.char = "%"
    player.color = colors.get("dark_red")

    return Message("It's a sad thing that your adventures have ended here!", colors.get("red")), GameStates.PLAYER_DEAD


def kill_monster(monster, colors):
    death_message = Message("{0} falls!".format(monster.name.capitalize()), colors.get("orange"))

    monster.char = '%'
    monster.color = colors.get('dark_red')
    monster.blocks = False
    monster.fighter = None
    monster.ai = None
    monster.name = 'remains of ' + monster.name
    monster.render_order = RenderOrder.CORPSE

    return death_message
