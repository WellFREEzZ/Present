import curses
import pygame
import settings
import os
from converter import ArtConverter


# define the menu function
def menu(title, classes, color='white'):
    # define the curses wrapper
    def character(stdscr, ):
        attributes = {}
        # stuff i copied from the internet that i'll put in the right format later
        icol = {
            1: 'red',
            2: 'green',
            3: 'yellow',
            4: 'blue',
            5: 'magenta',
            6: 'cyan',
            7: 'white'
        }
        # put the stuff in the right format
        col = {v: k for k, v in icol.items()}

        # declare the background color

        bc = curses.COLOR_BLACK

        # make the 'normal' format
        curses.init_pair(1, 7, bc)
        attributes['normal'] = curses.color_pair(1)

        # make the 'highlighted' format
        curses.init_pair(2, col[color], bc)
        attributes['highlighted'] = curses.color_pair(2)

        # handle the menu
        c = 0
        option = 0
        while c != 10:

            stdscr.erase()  # clear the screen (you can erase this if you want)

            # add the title
            stdscr.addstr(f"{title}\n", curses.color_pair(1))

            # add the options
            for i in range(len(classes)):
                # handle the colors
                if i == option:
                    attr = attributes['highlighted']
                else:
                    attr = attributes['normal']

                # actually add the options

                stdscr.addstr(f'> ', attr)
                stdscr.addstr(f'{classes[i]}' + '\n', attr)
            c = stdscr.getch()

            # handle the arrow keys
            if c == curses.KEY_UP and option > 0:
                option -= 1
            elif c == curses.KEY_DOWN and option < len(classes) - 1:
                option += 1
        return option

    return curses.wrapper(character)


cur_menu = 0
cur_file = None
cur_param = None

menus = {
    0: ['ОСНОВНОЕ МЕНЮ:', ['Выбрать файл', 'Настройки', 'Выход']],
    1: ['lol', ['<=']],
    2: ['lol', ['<=']],
    3: ['lol', ['<=']],
    4: ['lol', ['<=']],
}


def main_loop():
    global cur_menu, cur_file
    while True:
        file_name = '' if cur_file is None else f'{settings.files[cur_file]}:'
        menu_head = f'[{cur_param}]{menus[cur_menu][0]} {file_name}' if cur_param is not None else f'{menus[cur_menu][0]} {file_name}'

        result = menu(menu_head, menus[cur_menu][1], 'blue')

        if cur_menu == 0:
            if result == 0:
                l_files = ['<=']
                l_files.extend([f for f in settings.files.values()])
                menus.update({1: ['ВЫБЕРИТЕ ФАЙЛ:', l_files]})
                cur_menu +=1
            elif result == 1:
                cur_menu = 2
                menus.update({2: ['НАСТРОЙКИ:', [
                    '<=',
                    f'Размер шрифта {settings.font_size}',
                    f'Количество чёрного {settings.threshold}'
                ]]})
            else:
                os.system('cls')
                break

        elif cur_menu == 1:
            if result == 0:
                cur_menu = 0
            else:
                cur_file = result
                cur_menu = 0
                try:
                    ArtConverter(name=settings.files[cur_file], font_size=settings.font_size, threshold=settings.threshold).run()
                except pygame.error:
                    pass
                cur_file = None

        elif cur_menu == 2:
            if result == 0:
                cur_menu = 0
            elif result == 1:
                menus.update({3: [f'РАЗМЕР ШРИФТА: {settings.font_size}\n(Чем меньше, тем детальнее, но меньше FPS)',
                                  ['<=', '+', '-']]})
                cur_menu += 1
            elif result == 2:
                menus.update({4: [f'КОЛ-ВО ЧЁРНОГО: {settings.threshold}\n(Чем меньше, тем больше символов, меньше FPS, но больше деталей)',
                                  ['<=', '+', '-']]})
                cur_menu += 2

        elif cur_menu == 3:
            if result == 0:
                menus.update({2: ['НАСТРОЙКИ:', [
                    '<=',
                    f'Размер шрифта {settings.font_size}',
                    f'Количество чёрного {settings.threshold}'
                ]]})
                cur_menu -= 1
            else:
                if result == 1:
                    if settings.font_size <= 40:
                        settings.font_size += 1
                elif result == 2:
                    if settings.font_size > 5:
                        settings.font_size -= 1
                with open(settings.datafile, 'w') as f:
                    f.write(f'{settings.font_size}|{settings.threshold}')
                menus.update({3: [f'РАЗМЕР ШРИФТА: {settings.font_size}\n(Чем меньше, тем детальнее, но меньше FPS)',
                                  ['<=', '+', '-']]})
        elif cur_menu == 4:
            if result == 0:
                menus.update({2: ['НАСТРОЙКИ:', [
                    '<=',
                    f'Размер шрифта {settings.font_size}',
                    f'Количество чёрного {settings.threshold}'
                ]]})
                cur_menu -= 2
            else:
                if result == 1:
                    if settings.threshold < 15:
                        settings.threshold += 1
                elif result == 2:
                    if settings.threshold > -15:
                        settings.threshold -= 1
                with open(settings.datafile, 'w') as f:
                    f.write(f'{settings.font_size}|{settings.threshold}')
                menus.update({4: [
                    f'КОЛ-ВО ЧЁРНОГО: {settings.threshold}\n(Чем меньше, тем больше символов, меньше FPS, но больше деталей)',
                    ['<=', '+', '-']]})


if __name__ == '__main__':
    main_loop()
