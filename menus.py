import tdl
import textwrap

def menu(con, root, header, options, width, screen_width, screen_height):
    if len(options) > 26: raise ValueError("Cannot have a menu with more than 26 options.")

    header_wrapped = textwrap.wrap(header, width)
    header_height = len(header_wrapped)
    height = len(options) + header_height

    # off-screen console to represent menu window
    window = tdl.Console(width, height)

    # print header
    window.draw_rect(0, 0, width, height, None, fg=(255, 255, 255), bg=None)
    for i, line in enumerate(header_wrapped):
        window.draw_str(0, 0 + i, header_wrapped[i])

    y = header_height
    letter_index = ord("a")
    for option_text in options:
        text = "(" + chr(letter_index) + ") " + option_text
        window.draw_str(0, y, text, bg=None)
        y += 1
        letter_index += 1

    # blit the contents of "window" to root console
    x = screen_width // 2 - width // 2
    y = screen_height // 2 - width // 2
    root.blit(window, x, y, width, height, 0, 0)


def inventory_menu(con, root, header, inventory, inventory_width, screen_width, screen_height):
    # show a menu with each inventory item as an option
    if len(inventory.items) == 0:
        options = ["You're not carrying anything."]
    else:
        options = [item.name for item in inventory.items]

    menu(con, root, header, options, inventory_width, screen_width, screen_height)