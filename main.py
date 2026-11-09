
from colorama import Fore, Back, Style, init
import time


init(autoreset=True)

frontFace = [[Fore.WHITE + Back.BLACK + Style.BRIGHT + "■" + Style.RESET_ALL , Fore.WHITE + Back.BLACK + Style.BRIGHT + "■" + Style.RESET_ALL ],
             [Fore.WHITE + Back.BLACK + Style.BRIGHT + "■" + Style.RESET_ALL , Fore.WHITE + Back.BLACK + Style.BRIGHT + "■" + Style.RESET_ALL ]]
upFace = [[ Fore.GREEN + Back.BLACK + Style.BRIGHT + "G" + Style.RESET_ALL , Fore.GREEN + Back.BLACK + Style.BRIGHT + "G" + Style.RESET_ALL ],
          [ Fore.GREEN + Back.BLACK + Style.BRIGHT + "G" + Style.RESET_ALL ,  Fore.GREEN + Back.BLACK + Style.BRIGHT + "G" + Style.RESET_ALL ]]
downFace = [[ Fore.BLUE + Back.BLACK + Style.BRIGHT + "B" + Style.RESET_ALL ,  Fore.BLUE + Back.BLACK + Style.BRIGHT + "B" + Style.RESET_ALL ],
            [ Fore.BLUE + Back.BLACK + Style.BRIGHT + "B" + Style.RESET_ALL ,  Fore.BLUE + Back.BLACK + Style.BRIGHT + "B" + Style.RESET_ALL ]]
leftFace = [[  Fore.RED + Back.BLACK + Style.BRIGHT + "R" + Style.RESET_ALL ,  Fore.RED + Back.BLACK + Style.BRIGHT + "R" + Style.RESET_ALL ],
            [  Fore.RED + Back.BLACK + Style.BRIGHT + "R" + Style.RESET_ALL ,   Fore.RED + Back.BLACK + Style.BRIGHT + "R" + Style.RESET_ALL ]]
rightFace = [["\033[38;5;208m" + Back.BLACK + Style.BRIGHT + "O" + "\033[0m" , "\033[38;5;208m" + Back.BLACK + Style.BRIGHT + "O" + "\033[0m"],
             [ "\033[38;5;208m" + Back.BLACK + Style.BRIGHT + "O" + "\033[0m", "\033[38;5;208m" + Back.BLACK + Style.BRIGHT + "O" + "\033[0m"]]
backFace = [[ Fore.YELLOW + Back.BLACK + Style.BRIGHT + "Y" + Style.RESET_ALL ,  Fore.YELLOW + Back.BLACK + Style.BRIGHT + "Y" + Style.RESET_ALL ],
            [ Fore.YELLOW + Back.BLACK + Style.BRIGHT + "Y" + Style.RESET_ALL ,  Fore.YELLOW + Back.BLACK + Style.BRIGHT + "Y" + Style.RESET_ALL ]]
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
def printCube():
    global upFace, downFace, leftFace, rightFace, frontFace, backFace
    indent = "    "
    print(f"{indent}{upFace[0][0]} {upFace[0][1]}")
    print(f"{indent}{upFace[1][0]} {upFace[1][1]}")
    print(f"{leftFace[0][0]} {leftFace[0][1]} {frontFace[0][0]} {frontFace[0][1]} {rightFace[0][0]} {rightFace[0][1]}")
    print(f"{leftFace[1][0]} {leftFace[1][1]} {frontFace[1][0]} {frontFace[1][1]} {rightFace[1][0]} {rightFace[1][1]}")

printCube()
R()
printCube()

