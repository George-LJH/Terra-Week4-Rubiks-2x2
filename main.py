
from colorama import Fore, Back, Style, init
import time
import os
import sys

def getKey():
    if sys.platform == "win32":
        import msvcrt
        ch = msvcrt.getch()
        if ch in (b'\x00', b'\xe0'):
            ch = msvcrt.getch()
            key = {b'H': 'UP', b'P': 'DOWN', b'M': 'RIGHT', b'K': 'LEFT'}.get(ch, b'').decode()
        else:
            key = ch.decode(errors='ignore')
    else:
        import termios, tty
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
            if ch == '\x1b':
                ch += sys.stdin.read(2)
                key = {'\x1b[A': 'UP', '\x1b[B': 'DOWN', '\x1b[C': 'RIGHT', '\x1b[D': 'LEFT'}.get(ch, ch)
            else:
                key = ch
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)
    
    if key == '\x03':  # Ctrl+C
        raise KeyboardInterrupt
    return key

def clearConsole():
    os.system('cls' if os.name == 'nt' else 'clear')

init(autoreset=True)

frontFace = [[Fore.WHITE + Back.BLACK + Style.BRIGHT + "■" + Style.RESET_ALL , Fore.WHITE + Back.BLACK + Style.BRIGHT + "■" + Style.RESET_ALL ],
             [Fore.WHITE + Back.BLACK + Style.BRIGHT + "■" + Style.RESET_ALL , Fore.WHITE + Back.BLACK + Style.BRIGHT + "■" + Style.RESET_ALL ]]
upFace = [[ Fore.GREEN + Back.BLACK + Style.BRIGHT + "■" + Style.RESET_ALL , Fore.GREEN + Back.BLACK + Style.BRIGHT + "■" + Style.RESET_ALL ],
          [ Fore.GREEN + Back.BLACK + Style.BRIGHT + "■" + Style.RESET_ALL ,  Fore.GREEN + Back.BLACK + Style.BRIGHT + "■" + Style.RESET_ALL ]]
downFace = [[ Fore.BLUE + Back.BLACK + Style.BRIGHT + "■" + Style.RESET_ALL ,  Fore.BLUE + Back.BLACK + Style.BRIGHT + "■" + Style.RESET_ALL ],
            [ Fore.BLUE + Back.BLACK + Style.BRIGHT + "■" + Style.RESET_ALL ,  Fore.BLUE + Back.BLACK + Style.BRIGHT + "■" + Style.RESET_ALL ]]
leftFace = [[  Fore.RED + Back.BLACK + Style.BRIGHT + "■" + Style.RESET_ALL ,  Fore.RED + Back.BLACK + Style.BRIGHT + "■" + Style.RESET_ALL ],
            [  Fore.RED + Back.BLACK + Style.BRIGHT + "■" + Style.RESET_ALL ,   Fore.RED + Back.BLACK + Style.BRIGHT + "■" + Style.RESET_ALL ]]
rightFace = [["\033[38;5;208m" + Back.BLACK + Style.BRIGHT + "■" + "\033[0m" , "\033[38;5;208m" + Back.BLACK + Style.BRIGHT + "■" + "\033[0m"],
             [ "\033[38;5;208m" + Back.BLACK + Style.BRIGHT + "■" + "\033[0m", "\033[38;5;208m" + Back.BLACK + Style.BRIGHT + "■" + "\033[0m"]]
backFace = [[ Fore.YELLOW + Back.BLACK + Style.BRIGHT + "■" + Style.RESET_ALL ,  Fore.YELLOW + Back.BLACK + Style.BRIGHT + "■" + Style.RESET_ALL ],
            [ Fore.YELLOW + Back.BLACK + Style.BRIGHT + "■" + Style.RESET_ALL ,  Fore.YELLOW + Back.BLACK + Style.BRIGHT + "■" + Style.RESET_ALL ]]
# frontFace = [["⬜️","⬜️"],["⬜️","⬜️"]]
# upFace = [["🟩","🟩"],["🟩","🟩"]]
# downFace = [["🟦","🟦"],["🟦","🟦"]]
# leftFace = [["🟥","🟥"],["🟥","🟥"]]
# rightFace = [["🟧","🟧"],["🟧","🟧"]]
# backFace = [["🟨","🟨"],["🟨","🟨"]]
def R():
    global upFace, downFace, leftFace, rightFace, frontFace, backFace
    newRightFace = [[None, None],[None, None]]
    newRightFace[0][0] = rightFace[1][0]
    newRightFace[0][1] = rightFace[0][0]
    newRightFace[1][0] = rightFace[1][1]
    newRightFace[1][1] = rightFace[0][1]
    rightFace = newRightFace

    newFrontFace = [[frontFace[0][0], None], [frontFace[1][0], None]]
    newFrontFace[0][1] = downFace[0][1]
    newFrontFace[1][1] = downFace[1][1]

    newDownFace = [[downFace[0][0], None], [downFace[1][0], None]]
    newDownFace[0][1] = backFace[0][1]
    newDownFace[1][1] = backFace[1][1]

    newBackFace = [[backFace[0][0], None], [backFace[1][0], None]]
    newBackFace[0][1] = upFace[0][1]
    newBackFace[1][1] = upFace[1][1]

    newUpFace = [[upFace[0][0], None], [upFace[1][0], None]]
    newUpFace[0][1] = frontFace[0][1]
    newUpFace[1][1] = frontFace[1][1]

    
    frontFace = newFrontFace
    downFace = newDownFace
    backFace = newBackFace
    upFace = newUpFace
    rightFace = newRightFace
def L():
    global upFace, downFace, leftFace, rightFace, frontFace, backFace
    
    newLeftFace = [[None, None], [None, None]]
    newLeftFace[0][0] = leftFace[1][0]
    newLeftFace[1][0] = leftFace[1][1]
    newLeftFace[1][1] = leftFace[0][1]
    newLeftFace[0][1] = leftFace[0][0]
    leftFace = newLeftFace

    newFrontFace = [[None, frontFace[0][1]], [None, frontFace[1][1]]]
    newFrontFace[0][0] = upFace[0][0]
    newFrontFace[1][0] = upFace[1][0]

    newUpFace = [[None,upFace[0][1]], [None,upFace[1][1]]]
    newUpFace[0][0] = backFace[0][0]
    newUpFace[1][0] = backFace[1][0]

    newBackFace = [[None, backFace[0][1]], [None, backFace[1][1]]]
    newBackFace[0][0] = downFace[0][0]
    newBackFace[1][0] = downFace[1][0]

    newDownFace = [[None, downFace[0][1]], [None, downFace[1][1]]]
    newDownFace[0][0] = frontFace[0][0]
    newDownFace[1][0] = frontFace[1][0]

    frontFace = newFrontFace
    downFace = newDownFace
    backFace = newBackFace
    upFace = newUpFace
    leftFace = newLeftFace
def U():
    global upFace, downFace, leftFace, rightFace, frontFace, backFace
    
    newUpFace = [[None, None], [None, None]]
    newUpFace[0][0] = upFace[1][0]
    newUpFace[0][1] = upFace[0][0]
    newUpFace[1][1] = upFace[0][1]
    newUpFace[1][0] = upFace[1][1]

    newFrontFace = [[None, None], [frontFace[1][0], frontFace[1][1]]]
    newFrontFace[0][0] = rightFace[0][0]
    newFrontFace[0][1] = rightFace[0][1]

    newRightFace = [[None, None], [rightFace[1][0], rightFace[1][1]]]
    newRightFace[0][0] = backFace[0][0]
    newRightFace[0][1] = backFace[0][1]

    newBackFace = [[None, None], [backFace[1][0], backFace[1][1]]]
    newBackFace[0][0] = leftFace[0][0]
    newBackFace[0][1] = leftFace[0][1]

    newLeftFace = [[None, None], [leftFace[1][0], leftFace[1][1]]]
    newLeftFace[0][0] = frontFace[0][0]
    newLeftFace[0][1] = frontFace[0][1]


    upFace = newUpFace
    frontFace = newFrontFace
    leftFace = newLeftFace
    rightFace = newRightFace
    backFace = newBackFace



def printCube():
    global upFace, downFace, leftFace, rightFace, frontFace, backFace
    indent = "    "
    print(f"{indent}{upFace[0][0]} {upFace[0][1]}")
    print(f"{indent}{upFace[1][0]} {upFace[1][1]}\n")
    print(f"{leftFace[0][0]} {leftFace[0][1]} {frontFace[0][0]} {frontFace[0][1]} {rightFace[0][0]} {rightFace[0][1]}")
    print(f"{leftFace[1][0]} {leftFace[1][1]} {frontFace[1][0]} {frontFace[1][1]} {rightFace[1][0]} {rightFace[1][1]}\n")
    print(f"{indent}{downFace[0][0]} {downFace[0][1]}")
    print(f"{indent}{downFace[1][0]} {downFace[1][1]}\n")
    print(f"{indent}{backFace[0][0]} {backFace[0][1]}")
    print(f"{indent}{backFace[1][0]} {backFace[1][1]}")

clearConsole()
while True:
    printCube()
    move = getKey()
    clearConsole()
    if move == "R":
        R()
    elif move == "r":
        R()
        R()
        R()
    elif move == "L":
        L()
    elif move == "l":
        L()
        L()
        L()
    elif move == "U":
        U()
    elif move == "u":
        U()
        U()
        U()
    else:
        print(f"Command {move} not recognized")
