
from colorama import Fore, Back, Style, init
import time
import os
import sys
import random
import requests
import io
import cairosvg
from PIL import Image


debug = False
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
def initializeCube():

    global frontFace, upFace, downFace, leftFace, rightFace, backFace, ColW, ColG, ColB, ColR, ColY, ColO
    ColW = Fore.WHITE + Back.BLACK + Style.BRIGHT + "██" + Style.RESET_ALL
    ColG = Fore.GREEN + Back.BLACK + Style.BRIGHT + "██" + Style.RESET_ALL
    ColB = Fore.BLUE + Back.BLACK + Style.BRIGHT + "██" + Style.RESET_ALL
    ColR = Fore.RED + Back.BLACK + Style.BRIGHT + "██" + Style.RESET_ALL
    ColY = Fore.YELLOW + Back.BLACK + Style.BRIGHT + "██" + Style.RESET_ALL
    ColO = "\033[38;5;208m" + Back.BLACK + Style.BRIGHT + "██" + "\033[0m"
    if not debug:
    
        frontFace = [[ColW, ColW], [ColW, ColW]]
        upFace    = [[ColG, ColG], [ColG, ColG]]
        downFace  = [[ColB, ColB], [ColB, ColB]]
        leftFace  = [[ColR, ColR], [ColR, ColR]]
        rightFace = [[ColO, ColO], [ColO, ColO]]
        backFace  = [[ColY, ColY], [ColY, ColY]]
    else:
    
        frontFace = [[Fore.WHITE + Back.BLACK + Style.BRIGHT + "██00" + Style.RESET_ALL , Fore.WHITE + Back.BLACK + Style.BRIGHT + "██01" + Style.RESET_ALL ],
                    [Fore.WHITE + Back.BLACK + Style.BRIGHT + "██10" + Style.RESET_ALL , Fore.WHITE + Back.BLACK + Style.BRIGHT + "██11" + Style.RESET_ALL ]]
        upFace = [[ Fore.GREEN + Back.BLACK + Style.BRIGHT + "██00" + Style.RESET_ALL , Fore.GREEN + Back.BLACK + Style.BRIGHT + "██01" + Style.RESET_ALL ],
                [ Fore.GREEN + Back.BLACK + Style.BRIGHT + "██10" + Style.RESET_ALL ,  Fore.GREEN + Back.BLACK + Style.BRIGHT + "██11" + Style.RESET_ALL ]]
        downFace = [[ Fore.BLUE + Back.BLACK + Style.BRIGHT + "██00" + Style.RESET_ALL ,  Fore.BLUE + Back.BLACK + Style.BRIGHT + "██01" + Style.RESET_ALL ],
                    [ Fore.BLUE + Back.BLACK + Style.BRIGHT + "██10" + Style.RESET_ALL ,  Fore.BLUE + Back.BLACK + Style.BRIGHT + "██11" + Style.RESET_ALL ]]
        leftFace = [[  Fore.RED + Back.BLACK + Style.BRIGHT + "██00" + Style.RESET_ALL ,  Fore.RED + Back.BLACK + Style.BRIGHT + "██01" + Style.RESET_ALL ],
                    [  Fore.RED + Back.BLACK + Style.BRIGHT + "██10" + Style.RESET_ALL ,   Fore.RED + Back.BLACK + Style.BRIGHT + "██11" + Style.RESET_ALL ]]
        rightFace = [["\033[38;5;208m" + Back.BLACK + Style.BRIGHT + "██00" + "\033[0m" , "\033[38;5;208m" + Back.BLACK + Style.BRIGHT + "██01" + "\033[0m"],
                    [ "\033[38;5;208m" + Back.BLACK + Style.BRIGHT + "██10" + "\033[0m", "\033[38;5;208m" + Back.BLACK + Style.BRIGHT + "██11" + "\033[0m"]]
        backFace = [[ Fore.YELLOW + Back.BLACK + Style.BRIGHT + "██00" + Style.RESET_ALL ,  Fore.YELLOW + Back.BLACK + Style.BRIGHT + "██01" + Style.RESET_ALL ],
                [ Fore.YELLOW + Back.BLACK + Style.BRIGHT + "██10" + Style.RESET_ALL ,  Fore.YELLOW + Back.BLACK + Style.BRIGHT + "██11" + Style.RESET_ALL ]]

# def getCorners():
#     return {
#         "UFR": [upFace[1][1], frontFace[0][1], rightFace[0][0]],
#         "UFL": [upFace[1][0], leftFace[0][1],  frontFace[0][0]],
#         "UBL": [upFace[0][0], backFace[0][1],  leftFace[0][0]],
#         "UBR": [upFace[0][1], rightFace[0][1], backFace[0][0]],
#         "DFR": [downFace[0][1], rightFace[1][0], frontFace[1][1]],
#         "DFL": [downFace[0][0], frontFace[1][0], leftFace[1][1]],
#         "DBL": [downFace[1][0], leftFace[1][0],  backFace[1][1]],
#         "DBR": [downFace[1][1], backFace[1][0],  rightFace[1][1]],
#     }
def getStickerColor(providedSticker):
    sticker = str(providedSticker)
    if "37m" in sticker:
        return "W"
    elif "32m" in sticker:
        return "G"
    elif "34m" in sticker:
        return "B"
    elif "31m" in sticker:
        return "R"
    elif "33m" in sticker:
        return "Y"
    elif "38;5;208" in sticker:
        return "O"

def getUFRWhiteFace():
    if getStickerColor(upFace[1][1]) == "W":
        return "U"
    if getStickerColor(frontFace[0][1]) == "W":
        return "F"
    if getStickerColor(rightFace[0][0]) == "W":
        return "R"
def isWhiteAtDFR():
    return getStickerColor(downFace[0][1]) == "W"
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
    newDownFace[0][1] = backFace[1][0]
    newDownFace[1][1] = backFace[0][0]

    newBackFace = [[None, backFace[0][1]], [None, backFace[1][1]]]
    newBackFace[0][0] = upFace[1][1]
    newBackFace[1][0] = upFace[0][1]

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

    newUpFace = [[None, upFace[0][1]], [None, upFace[1][1]]]
    newUpFace[0][0] = backFace[1][1]
    newUpFace[1][0] = backFace[0][1]

    newBackFace = [[backFace[0][0], None], [backFace[1][0], None]]
    newBackFace[0][1] = downFace[1][0]
    newBackFace[1][1] = downFace[0][0]

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
def F():
    global upFace, downFace, leftFace, rightFace, frontFace, backFace
    newFrontFace = [[None, None], [None, None]]
    newFrontFace[0][0] = frontFace[1][0]
    newFrontFace[0][1] = frontFace[0][0]
    newFrontFace[1][0] = frontFace[1][1]
    newFrontFace[1][1] = frontFace[0][1]

    newLeftFace = [[leftFace[0][0], None], [leftFace[1][0], None]]
    newLeftFace[0][1] = downFace[0][0]
    newLeftFace[1][1] = downFace[0][1]

    newDownFace = [[None, None], [downFace[1][0], downFace[1][1]]]
    newDownFace[0][0] = rightFace[1][0]
    newDownFace[0][1] = rightFace[0][0]

    newRightFace = [[None, rightFace[0][1]], [None, rightFace[1][1]]]
    newRightFace[0][0] = upFace[1][0]
    newRightFace[1][0] = upFace[1][1]

    newUpFace = [[upFace[0][0], upFace[0][1]], [None, None]]
    newUpFace[1][0] = leftFace[1][1]
    newUpFace[1][1] = leftFace[0][1]

    frontFace = newFrontFace
    leftFace = newLeftFace
    downFace = newDownFace
    rightFace = newRightFace
    upFace = newUpFace
def B():
    global upFace, downFace, leftFace, rightFace, frontFace, backFace
    newBackFace = [[None, None], [None, None]]
    newBackFace[0][0] = backFace[1][0]
    newBackFace[0][1] = backFace[0][0]
    newBackFace[1][0] = backFace[1][1]
    newBackFace[1][1] = backFace[0][1]

    newUpFace = [[None, None], [upFace[1][0], upFace[1][1]]]
    newUpFace[0][0] = rightFace[0][1]
    newUpFace[0][1] = rightFace[1][1]

    newRightFace = [[rightFace[0][0], None], [rightFace[1][0], None]]
    newRightFace[0][1] = downFace[1][1]
    newRightFace[1][1] = downFace[1][0]

    newDownFace = [[downFace[0][0], downFace[0][1]], [None, None]]
    newDownFace[1][0] = leftFace[0][0]
    newDownFace[1][1] = leftFace[1][0]

    newLeftFace = [[None, leftFace[0][1]], [None, leftFace[1][1]]]
    newLeftFace[0][0] = upFace[0][1]
    newLeftFace[1][0] = upFace[0][0]

    backFace = newBackFace
    upFace = newUpFace
    downFace = newDownFace
    leftFace = newLeftFace
    rightFace = newRightFace

def D():
    R()
    L()
    L()
    L()
    F()
    L()
    R()
    R()
    R()
def printCube():
    global upFace, downFace, leftFace, rightFace, frontFace, backFace
    indent = "      "
    print(f"{indent}{upFace[0][0]}┃{upFace[0][1]}")
    print("      ━━╋━━")
    print(f"{indent}{upFace[1][0]}┃{upFace[1][1]}\n")
    print(f"{leftFace[0][0]}┃{leftFace[0][1]}┃{frontFace[0][0]}┃{frontFace[0][1]}┃{rightFace[0][0]}┃{rightFace[0][1]}")
    print("━━╋━━╋━━╋━━╋━━╋━━")
    print(f"{leftFace[1][0]}┃{leftFace[1][1]}┃{frontFace[1][0]}┃{frontFace[1][1]}┃{rightFace[1][0]}┃{rightFace[1][1]}\n")
    print(f"{indent}{downFace[0][0]}┃{downFace[0][1]}")
    print("      ━━╋━━")
    print(f"{indent}{downFace[1][0]}┃{downFace[1][1]}\n")
    print(f"{indent}{backFace[1][1]}┃{backFace[1][0]}")
    print("      ━━╋━━")
    print(f"{indent}{backFace[0][1]}┃{backFace[0][0]}")

def insertUFRToDFR():
    face = getUFRWhiteFace()
    if face == "R":
        movement("R")
        movement("U")
        movement("r")
    elif face == "F":
        movement("f")
        movement("u")
        movement("F")
    elif face == "U":
        movement("R")
        movement("U")
        movement("U")
        movement("r")
        movement("u")
        movement("R")
        movement("U")
        movement("r")


def movement(move):
    global debug
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
    elif move == "F":
        F()
    elif move == "f":
        F()
        F()
        F()
    elif move == "B":
        B()
    elif move == "b":
        B()
        B()
        B()
    elif move == "D":
        D()
    elif move == "d":
        D()
        D()
        D()
    elif move == "{":
        debug = not debug
        initializeCube()
    elif move == "S":
        initializeCube()
        scrambleSize = int(input("What is the scramble size?"))
        scramble = []
        for i in range(0,scrambleSize):
            scramble.append(random.choice(["R","r","L","l","U","u","F","f", "B", "b", "D", "d"]))
        for move in scramble:
            movement(move)
    elif move == "1":
        solveCube()
    elif move == "2":
        def c(face, r, c):
            return getStickerColor(face[r][c])
        
        print("      U")
        print(f"    {c(upFace,0,0)} {c(upFace,0,1)}")
        print(f"    {c(upFace,1,0)} {c(upFace,1,1)}")
        print()
        print("L        F        R        B")
        print(f"{c(leftFace,0,0)} {c(leftFace,0,1)}   {c(frontFace,0,0)} {c(frontFace,0,1)}   {c(rightFace,0,0)} {c(rightFace,0,1)}   {c(backFace,0,0)} {c(backFace,0,1)}")
        print(f"{c(leftFace,1,0)} {c(leftFace,1,1)}   {c(frontFace,1,0)} {c(frontFace,1,1)}   {c(rightFace,1,0)} {c(rightFace,1,1)}   {c(backFace,1,0)} {c(backFace,1,1)}")
        print()
        print("      D")
        print(f"    {c(downFace,0,0)} {c(downFace,0,1)}")
        print(f"    {c(downFace,1,0)} {c(downFace,1,1)}")
    elif move == "3":
        print(checkSune())
    elif move == "4":
        print(f"BACKFACE00{backFace[0][0]} BACKFACE01{backFace[0][1]} BACKFACE10{backFace[1][0]} BACKFACE11{backFace[1][1]}")
    elif move == "5":
        print(cubeSolved())
    elif move == "6":
        print(checkDiag())
    elif move == "7":
        print(checkOppOpp())
    elif move == "8":
        print(checkAdjAdj())
    elif move == "9":
        print(topSolved())
    elif move == "0":
        print(bottomSolved())
    elif move == "!":
        print(checkAdjOpp())
    elif move == "UP":
        movement("R")
        movement("l")
    elif move == "DOWN":
        movement("r")
        movement("L")
    elif move == "LEFT":
        movement("U")
        movement("d")
    elif move == "RIGHT":
        movement("u")
        movement("D")
    else:
        print(f"Command {move} not recognized")


def bringWhiteToUFR():
    for _ in range(4):
        if getUFRWhiteFace():
            return True
        movement("U")
    return False
def solveCube():
    def doMove(m):
        movement(m)
        clearConsole()
        # printCube()
        buildCubeFaces()
        time.sleep(0.1)
    if not cubeSolved():
        if not (getStickerColor(downFace[0][0]) == getStickerColor(downFace[0][1]) == getStickerColor(frontFace[1][0]) == getStickerColor(rightFace[1][0]) == getStickerColor(backFace[1][0]) == getStickerColor(leftFace[1][1]) == "W"):
            for _ in range(4):
                dfr_corner = [downFace[0][1], rightFace[1][0], frontFace[1][1]]
                white_on_bottom = getStickerColor(dfr_corner[0]) == "W"
                white_on_side = any(getStickerColor(s) == "W" for s in dfr_corner[1:])
                
                if white_on_side:
                    doMove("R"); doMove("U"); doMove("r")
                elif white_on_bottom:
                    doMove("D")
                    continue
                
                if not bringWhiteToUFR():
                    doMove("R"); doMove("U"); doMove("r")
                    bringWhiteToUFR()
                
                # insertUFRToDFR does multiple moves - expand it:
                face = getUFRWhiteFace()
                if face == "R":
                    doMove("R"); doMove("U"); doMove("r")
                elif face == "F":
                    doMove("f"); doMove("u"); doMove("F")
                elif face == "U":
                    doMove("R"); doMove("U"); doMove("U"); doMove("r")
                    doMove("u"); doMove("R"); doMove("U"); doMove("r")
                
                doMove("D")

        clearConsole()
        if not (getStickerColor(upFace[0][0]) == getStickerColor(upFace[0][1]) == getStickerColor(upFace[1][0]) == getStickerColor(upFace[1][1]) == "Y"):
            for _ in range(4):
                if checkAntisune():
                    doMove("R"); doMove("u"); doMove("u"); doMove("r"); doMove("u"); doMove("R"); doMove("u"); doMove("r")
                    # clearConsole()
                elif checkSune():
                    doMove("R"); doMove("U"); doMove("r"); doMove("U"); doMove("R"); doMove("U"); doMove("U"); doMove("r")
                    # clearConsole()
                elif checkCar():
                    doMove("R"); doMove("R"); doMove("U"); doMove("U"); doMove("R"); doMove("U"); doMove("U"); doMove("R"); doMove("R")
                elif checkBlinker():
                    doMove("R"); doMove("U"); doMove("U"); doMove("R"); doMove("R"); doMove("u"); doMove("R"); doMove("R"); doMove("u"); doMove("R"); doMove("R"); doMove("U"); doMove("U"); doMove("R")
                    print(checkSune())
                elif checkBowtie():
                    doMove("F"); doMove("r"); doMove("f"); doMove("R"); doMove("U"); doMove("R"); doMove("u"); doMove("r");
                elif checkChameleon():
                    doMove("R"); doMove("U"); doMove("r"); doMove("u"); doMove("r"); doMove("F"); doMove("R"); doMove("f");
                elif checkHeadlights():
                    doMove("F"); doMove("R"); doMove("U"); doMove("r"); doMove("u"); doMove("f");
                else:
                    doMove("U")
                clearConsole()
        done = False
        for i in range(4):
            for j in range(4):
                if checkAdj():
                    doMove("r"); doMove("F"); doMove("R"); doMove("f"); doMove("R"); doMove("U"); doMove("U"); doMove("r"); doMove("U"); doMove("R"); doMove("U"); doMove("U"); doMove("r");
                    done = True
                    break
                elif checkDiag():
                    doMove("R"); doMove("u"); doMove("r"); doMove("u"); doMove("F"); doMove("F"); doMove("u"); doMove("R"); doMove("U"); doMove("r"); doMove("U"); doMove("F"); doMove("F");
                    # movement("R"); movement("u"); movement("r"); movement("u"); movement("F"); movement("F"); movement("u"); movement("R"); movement("U"); movement("r"); movement("U"); movement("F"); movement("F");
                    done = True
                    break
                elif checkOppOpp():
                    doMove("R"); doMove("R"); doMove("F"); doMove("F"); doMove("R"); doMove("R");
                    done = True
                    break
                elif checkAdjAdj():
                    doMove("R"); doMove("R"); doMove("u"); doMove("B"); doMove("B"); doMove("U"); doMove("U"); doMove("R"); doMove("R"); doMove("u"); doMove("R"); doMove("R");
                    done = True
                    break
                elif checkAdjOpp():
                    doMove("R"); doMove("u"); doMove("R"); doMove("F"); doMove("F"); doMove("r"); doMove("U"); doMove("r")
                    done = True
                    break
                elif checkOppAdj():
                    doMove("r"); doMove("D"); doMove("r"); doMove("F"); doMove("F"); doMove("R"); doMove("d"); doMove("R")
                    done = True
                    break
                else:
                    doMove("D")
        
                # clearConsole()
            if done:
                break
            else:
                doMove("U")


    while not cubeSolved():
        doMove("U")
    clearConsole()

        

def getSVG(frontFaceStr, upFaceStr, rightFaceStr):
    url = f"https://rubik-render.leoganpro.net/v1/cube/isometric/2x2x2/{frontFaceStr}-{upFaceStr}-{rightFaceStr}"
    response = requests.get(url)
    if response.status_code == 200:
        SVGdat= response.text
        renderCube(SVGdat)
    
    
def renderCube(svg_string: str, width: int = 50):
    # Convert SVG to PNG in memory
    png_bytes = cairosvg.svg2png(bytestring=svg_string.encode("utf-8"))
    img = Image.open(io.BytesIO(png_bytes)).convert("RGBA")

    # Calculate proportional height (must be even for half-block pairing)
    aspect_ratio = img.height / img.width
    height = int(width * aspect_ratio)
    if height % 2 != 0:
        height += 1

    img = img.resize((width, height), Image.Resampling.LANCZOS)
    pixels = img.load()

    # Render two vertical pixels per terminal character using '▀'
    for y in range(0, height, 2):
        line = []
        for x in range(width):
            r1, g1, b1, a1 = pixels[x, y]
            r2, g2, b2, a2 = pixels[x, y + 1]

            if a1 < 128 and a2 < 128:
                line.append(" ")
            elif a1 < 128:
                # Top transparent, bottom colored
                line.append(f"\033[38;2;{r2};{g2};{b2}m▄\033[0m")
            elif a2 < 128:
                # Top colored, bottom transparent
                line.append(f"\033[38;2;{r1};{g1};{b1}m▀\033[0m")
            else:
                # Top is foreground (▀), bottom is background
                line.append(
                    f"\033[38;2;{r1};{g1};{b1}m\033[48;2;{r2};{g2};{b2}m▀\033[0m"
                )
        print("".join(line))

def getFaceColor(face, row, col):
    return getStickerColor(face[row][col])

def buildCubeFaces():
    global frontFace, upFace, rightFace
    frontFaceStr = getFaceColor(frontFace, 0, 0) + getFaceColor(frontFace, 0, 1) + getFaceColor(frontFace, 1, 0) + getFaceColor(frontFace, 1, 1)
    upFaceStr = getFaceColor(upFace, 1, 0) + getFaceColor(upFace, 0, 0) + getFaceColor(upFace, 1, 1) + getFaceColor(upFace, 0, 1)
    rightFaceStr = getFaceColor(rightFace, 0, 0) + getFaceColor(rightFace, 0, 1) + getFaceColor(rightFace, 1, 0) + getFaceColor(rightFace, 1, 1)
    # print(f"Front Face: {frontFaceStr}, Up Face: {upFaceStr}, Right Face: {rightFaceStr}")
    # printCube()
    getSVG(frontFaceStr, upFaceStr, rightFaceStr)
def checkAntisune():
    top_correct = (
        getStickerColor(upFace[0][1]) == "Y" and
        getStickerColor(upFace[0][0]) != "Y" and
        getStickerColor(upFace[1][1]) != "Y" and
        getStickerColor(upFace[1][0]) != "Y"
    )
    # print(upFace[0][0], upFace[0][1], "\n", upFace[1][0], upFace[1][1])
    # print(top_correct)
    
    sides_correct = (
        getStickerColor(frontFace[0][0]) == "Y" and
        getStickerColor(rightFace[0][0]) == "Y" and
        getStickerColor(leftFace[0][0]) == "Y"
    )
    # print(getStickerColor(frontFace[0][0]), getStickerColor(rightFace[0][0]), getStickerColor(backFace[0][0]))
    # print(sides_correct)
    return top_correct and sides_correct
def checkSune():
    topCorrect = (
        getStickerColor(upFace[1][0]) == "Y" and
        getStickerColor(upFace[1][1]) != "Y" and
        getStickerColor(upFace[0][0]) != "Y" and
        getStickerColor(upFace[0][1]) != "Y"
    )
    # print(getStickerColor(upFace[1][0]))
    # print(f"UPFACE00{upFace[0][0]} UPFACE01{upFace[0][1]} UPFACE10{upFace[1][0]} UPFACE11{upFace[1][1]}")
    # print(f"TOP CORRECT: {topCorrect}")
    sidesCorrect = (
        getStickerColor(backFace[0][1]) == "Y" and
        getStickerColor(rightFace[0][1]) == "Y" and
        getStickerColor(frontFace[0][1]) == "Y"
    )
    # print(f"BACKFACE00{backFace[0][0]} BACKFACE01{backFace[0][1]} BACKFACE10{backFace[1][0]} BACKFACE11{backFace[1][1]}")
    # print(f"RIGHTFACE00{rightFace[0][0]} RIGHTFACE01{rightFace[0][1]} RIGHTFACE10{rightFace[1][0]} RIGHTFACE11{rightFace[1][1]}")
    # print(f"LEFTFACE00{leftFace[0][0]} LEFTFACE01{leftFace[0][1]} LEFTFACE10{leftFace[1][0]} LEFTFACE11{leftFace[1][1]}")
    # print(f"BACKFACE01{backFace[0][1]} RIGHTFACE01{rightFace[0][1]} \nLEFTFACE01{leftFace[0][1]} LEFTFACE11{leftFace[1][1]} LEFTFACE10{leftFace[1][0]} LEFTFACE00{leftFace[0][0]}")
    # print(f"SIDES CORRECT: {sidesCorrect}")
    # input("Press Enter to continue...")
    return topCorrect and sidesCorrect
def checkCar():
    sideCorrect = (
        getStickerColor(frontFace[0][0]) == "Y" and
        getStickerColor(frontFace[0][1]) == "Y" and
        getStickerColor(backFace[0][1]) == "Y" and
        getStickerColor(backFace[0][0]) == "Y"
        )
    return sideCorrect
def checkBlinker():
    sideCorrect = (
        getStickerColor(leftFace[0][0]) == "Y" and
        getStickerColor(leftFace[0][1]) == "Y" and
        getStickerColor(frontFace[0][1]) == "Y" and
        getStickerColor(backFace[0][0]) == "Y"
    )
    return sideCorrect
def checkBowtie():
    upCorrect = (
        getStickerColor(upFace[0][0]) == "Y" and
        getStickerColor(upFace[1][1]) == "Y")
    sideCorrect = (
        getStickerColor(frontFace[0][0]) == "Y" and
        getStickerColor(rightFace[0][1]) == "Y"
    )

    return upCorrect and sideCorrect
def checkChameleon():
    upCorrect = (
        getStickerColor(upFace[0][1]) == "Y" and
        getStickerColor(upFace[1][1]) == "Y"
    )
    sideCorrect = (
        getStickerColor(frontFace[0][0]) == "Y" and
        getStickerColor(backFace[0][1]) == "Y"
    )
    return upCorrect and sideCorrect
def checkHeadlights():
    upCorrect = (
        getStickerColor(upFace[0][1]) == "Y" and
        getStickerColor(upFace[1][1]) == "Y"
    )
    sideCorrect = (
        getStickerColor(leftFace[0][0]) == "Y" and
        getStickerColor(leftFace[0][1]) == "Y"
    )
    return upCorrect and sideCorrect
def checkAdj():
    bottomCorrect = (
        getStickerColor(frontFace[1][0]) == getStickerColor(frontFace[1][1]) and 
        getStickerColor(backFace[1][0]) == getStickerColor(backFace[1][1]) and
        getStickerColor(rightFace[1][0]) == getStickerColor(rightFace[1][1]) and
        getStickerColor(leftFace[1][0]) == getStickerColor(leftFace[1][1])
    )
    # print(
    #     getStickerColor(frontFace[1][0]) == getStickerColor(frontFace[1][1]) and 
    #     getStickerColor(backFace[1][0]) == getStickerColor(backFace[1][1]) and
    #     getStickerColor(rightFace[1][0]) == getStickerColor(rightFace[1][1]) and
    #     getStickerColor(leftFace[1][0]) == getStickerColor(leftFace[1][1])
    # )
    topCorrect = (
        getStickerColor(leftFace[0][0]) == getStickerColor(leftFace[0][1])
    )
    # print(
    #     getStickerColor(leftFace[0][0]) == getStickerColor(leftFace[0][1])
    # )
    # input("Press Enter to continue..."  )
    return bottomCorrect and topCorrect
def checkDiag():
    bottomCorrect = (
        getStickerColor(frontFace[1][0]) == getStickerColor(frontFace[1][1]) and 
        getStickerColor(backFace[1][0]) == getStickerColor(backFace[1][1]) and
        getStickerColor(rightFace[1][0]) == getStickerColor(rightFace[1][1]) and
        getStickerColor(leftFace[1][0]) == getStickerColor(leftFace[1][1])
    )
    topCorrect = (
        getStickerColor(frontFace[0][0]) != getStickerColor(frontFace[0][1]) and
        getStickerColor(backFace[0][0]) != getStickerColor(backFace[0][1]) and
        getStickerColor(rightFace[0][0]) != getStickerColor(rightFace[0][1]) and
        getStickerColor(leftFace[0][0]) != getStickerColor(leftFace[0][1])
    )
    return bottomCorrect and topCorrect
def checkOppOpp():
    topCorrect = (
        getStickerColor(frontFace[0][0]) != getStickerColor(frontFace[0][1]) and
        getStickerColor(backFace[0][0]) != getStickerColor(backFace[0][1]) and
        getStickerColor(rightFace[0][0]) != getStickerColor(rightFace[0][1]) and
        getStickerColor(leftFace[0][0]) != getStickerColor(leftFace[0][1])
    )
    bottomCorrect = (
        getStickerColor(frontFace[1][0]) != getStickerColor(frontFace[1][1]) and
        getStickerColor(backFace[1][0]) != getStickerColor(backFace[1][1]) and
        getStickerColor(rightFace[1][0]) != getStickerColor(rightFace[1][1]) and
        getStickerColor(leftFace[1][0]) != getStickerColor(leftFace[1][1])
    )
    return topCorrect and bottomCorrect
def checkAdjAdj():
    topCorrect = (
        getStickerColor(backFace[0][0]) == getStickerColor(backFace[0][1])
    )
    bottomCorrect = (
        getStickerColor(backFace[1][0]) == getStickerColor(backFace[1][1])
    )
    return bottomCorrect and topCorrect
def checkAdjOpp():
    topCorrect = (
        getStickerColor(frontFace[0][0]) == getStickerColor(frontFace[0][1])
    )
    bottomCorrect = not bottomSolved()
    return bottomCorrect and topCorrect
def checkOppAdj():
    bottomCorrect = (
        getStickerColor(frontFace[1][0]) == getStickerColor(frontFace[1][1])
    )
    topCorrect = not topSolved()
    return bottomCorrect and topCorrect

def cubeSolved():
    return (
        getStickerColor(upFace[0][0]) == getStickerColor(upFace[0][1]) == getStickerColor(upFace[1][0]) == getStickerColor(upFace[1][1]) and
        getStickerColor(downFace[0][0]) == getStickerColor(downFace[0][1]) == getStickerColor(downFace[1][0]) == getStickerColor(downFace[1][1]) and
        getStickerColor(leftFace[0][0]) == getStickerColor(leftFace[0][1]) == getStickerColor(leftFace[1][0]) == getStickerColor(leftFace[1][1]) and
        getStickerColor(rightFace[0][0]) == getStickerColor(rightFace[0][1]) == getStickerColor(rightFace[1][0]) == getStickerColor(rightFace[1][1])
    )
def bottomSolved():
    return (
        getStickerColor(frontFace[1][0]) == getStickerColor(frontFace[1][1]) and
        getStickerColor(backFace[1][0]) == getStickerColor(backFace[1][1]) and
        getStickerColor(rightFace[1][0]) == getStickerColor(rightFace[1][1]) and
        getStickerColor(leftFace[1][0]) == getStickerColor(leftFace[1][1])
    )
def topSolved():
    return (
        getStickerColor(frontFace[0][0]) == getStickerColor(frontFace[0][1]) and
        getStickerColor(backFace[0][0]) == getStickerColor(backFace[0][1]) and
        getStickerColor(rightFace[0][0]) == getStickerColor(rightFace[0][1]) and
        getStickerColor(leftFace[0][0]) == getStickerColor(leftFace[0][1])
    )
clearConsole()
initializeCube()
while True:
    # printCube()
    buildCubeFaces()
    move = getKey()
    clearConsole()
    movement(move)