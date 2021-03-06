from game_messages import Message
from components.ai import ConfusedMonster


def heal(*args, **kwargs):
    entity = args[0]
    colors = args[1]
    amount = kwargs.get("amount")

    results = []

    if entity.fighter.hp == entity.fighter.max_hp:
        results.append({"consumed": False, "message": Message("That might make you TOO healthy.",
                                                              colors.get("yellow"))})
    else:
        entity.fighter.heal(amount)
        results.append({"consumed": True, "message": Message("You feel healthier already!", colors.get("green"))})

    return results


def xpboost(*args, **kwargs):
    entity = args[0]
    colors = args[1]
    amount = kwargs.get("amount")

    results = []

    entity.level.add_xp(amount)
    results.append({"consumed": True, "message": Message("You crush the pearl and swallow the powder with a swig from your canteen. You feel accomplished!",
                                                         colors.get("silver"))})

    return results


def seeker_bolt(*args, **kwargs):
    # autotargets the nearest enemy and blasts it for heavy damage
    caster = args[0]
    colors = args[1]
    entities = kwargs.get("entities")
    game_map = kwargs.get("game_map")
    damage = kwargs.get("damage")
    maximum_range = kwargs.get("maximum_range")

    results = []

    target = None
    closest_distance = maximum_range + 1

    for entity in entities:
        if entity.fighter and entity != caster and game_map.fov[entity.x, entity.y]:
            distance = caster.distance_to(entity)

            if distance < closest_distance:
                target = entity
                closest_distance = distance

    if target:
        results.append({"consumed": True, "target": target, "message": Message("A crackling beam sears from the orb toward the {0}, dealing {1} damage!".format(target.name, damage))})
        results.extend(target.fighter.take_damage(damage))
    else:
        results.append({"consumed": False, "target": None, "message": Message("No hostiles within range.", colors.get("red"))})

    return results


def flame_grenade(*args, **kwargs):
    # throw a grenade that causes fire damage in a radius
    colors = args[1]
    entities =kwargs.get("entities")
    game_map = kwargs.get("game_map")
    damage = kwargs.get("damage")
    radius = kwargs.get("radius")
    target_x = kwargs.get("target_x")
    target_y = kwargs.get("target_y")

    results= []

    if not game_map.fov[target_x, target_y]:
        results.append({"consumed": False, "message": Message("You can't aim where you can't see!",
                                                              colors.get("yellow"))})
        return results

    results.append({"consumed": True,
                    "message": Message("The grenade explodes, immolating everything within {0} squares!".format(radius),
                                       colors.get("orange"))})

    for entity in entities:
        if entity.distance(target_x, target_y) <= radius and entity.fighter:
            results.append({"message": Message("The {0} is burned for {1} damage!".format(entity.name, damage),
                                               colors.get("orange"))})
            results.extend(entity.fighter.take_damage(damage))

    return results


def confuse(*args, **kwargs):
    # confuses enemy causing them to move randomly
    #todo: reskin
    colors = args[1]

    entities = kwargs.get("entities")
    game_map = kwargs.get("game_map")
    target_x = kwargs.get("target_x")
    target_y = kwargs.get("target_y")

    results = []

    if not game_map.fov[target_x, target_y]:
        results.append({"consumed": False, "message": Message("You can't aim where you can't see!",
                                                              colors.get("yellow"))})
        return results

    for entity in entities:
        if entity.x == target_x and entity.y == target_y and entity.ai:
            confused_ai = ConfusedMonster(entity.ai, 6)

            confused_ai.owner = entity
            entity.ai = confused_ai

            results.append({"consumed": True,
                            "message": Message("The {0}'s senses are disrupted and they begin to stumble around!".format(entity.name),
                                               colors.get("light_green"))})
            break
    else:
        results.append({"consumed": False, "message": Message("There's no target here!", colors.get("yellow"))})

    return results