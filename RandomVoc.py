import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import random
import argparse
from datetime import date
import unicodedata

parser = argparse.ArgumentParser(description="Change la langue ou ajoute ton dictionnaire")
parser.add_argument("-f", "--file", type=str, help="Enter the path to the file [default : ita.txt]")
parser.add_argument("-a", "--add", action="store_true",  help="Ajoute ton vocabulaire, Aucun argument")
parser.add_argument("-l", "--lang", type=str, help="Choisis entre lang2:lang1 ou l'inverse | lang2 = trouver lang2 [lang2, lang1, random]")
parser.add_argument("-d", "--difficulty", type=str, help="hard/medium/easy/EZ]")
parser.add_argument("-i", "--increase", action="store_true", help="Ajoute de la difficulté et augmente de la vitesse au fur est a mesure")
parser.add_argument("-c", "--cc", action="store_true", help=argparse.SUPPRESS)
args = parser.parse_args()

pygame.init()
WIDTH, HEIGHT = 1920, 1080
SCREEN = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("ASTEROID GAME")
FAIL, SUCCESS = 0, 0

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def answer(nb = False):
    if nb:
        print(bcolors.OKGREEN + "Bonne réponse" + bcolors.ENDC)
    else:
        print(bcolors.FAIL + "Mauvaise réponse" + bcolors.ENDC)
    print("\n")

def moveLocation(file_path, path, line_nb):
    line_nb -= 1
    with open(file_path, "r") as file:
        lines = file.readlines()
    with open(file_path, 'w') as fp:
        for number, line in enumerate(lines):
            if number is not line_nb:
                fp.write(line)
            else:
                with open(path, "a") as f:
                    f.write(line)

def lineInFile(pathStr):
    if os.path.isfile(pathStr):
        count = 0
        f = open(pathStr, "r")
        for line in f:
            if line != "\n":
                count += 1
        f.close()
        return count
    else:
        print("No such file at the path")
        return 0

def readFile(pathStr):
    if (not os.path.isfile(pathStr)):
        print("Specified path doesn't exists")
        exit()
    try:
        rdm = random.randint(1, lineInFile(pathStr))
        f = open(pathStr, "r")
        strLines = f.readlines()
        strFormat = strLines[rdm - 1].rstrip("\n").split(":")
        f.close()
        return strFormat[0], strFormat[1], rdm
    except:
        print("No line in this file")
    return None, None, None

def checkLangxd(pathFile, checkLang = "lang1"):
    if (checkLang == "lang1"):
        result, motATrouver, lineNb = readFile(pathFile)
    elif (checkLang == "lang2"):
        motATrouver, result, lineNb = readFile(pathFile)
    elif (checkLang == "random"):
        rdm = random.randint(1, 2)
        if (rdm % 2 == 0):
            result, motATrouver, lineNb = readFile(pathFile)
        else:
            motATrouver, result, lineNb = readFile(pathFile)
    return motATrouver, result, lineNb

def questions(pathFile, tries, failNb, checkLang = "lang1"):
    tries -= 1
    while (tries >= 0):
        motATrouver, result, lineNb = checkLangxd(pathFile, checkLang)
        print("Question : " + motATrouver)
        checkAnswer = input("Réponse : ")
        if (checkAnswer == "GetMeOutSenpai"):
            input("Press any key to get out")
            exit()
        elif (checkAnswer != result):
            moveLocation(pathFile,f"Fail{failNb}.txt", lineNb)
            answer()
        elif (checkAnswer == result):
            moveLocation(pathFile, "Success.txt", lineNb)
            answer(True)
        tries -= 1
    return 1

def cleanup_folder():
    counter = 0
    date_today = date.today().strftime("%H_%m_%d_%y")
    if (not os.path.isdir(date_today)):
        os.mkdir(date_today)
    for file in os.listdir(os.getcwd()):
        if file.lower().endswith(".txt"):
            new_file = str(f"{file.rsplit('.')[0]}_{counter}.{file.rsplit('.')[1]}")
            counter += 1
            os.rename(file, f"{date_today}/{new_file}")

def add_to_txt(filePath):
    if (os.path.isfile(filePath)):
        add_to_existing = input("Ajouter au fichier existant [[Y]yes/[N]no] : ").lower()
        if (add_to_existing == "no" or add_to_existing == "n"):
            cleanup_folder()
    else:
        clean_foler = input("Clean the folder ? (Remove everything and add it to another folder) [yes/no] : ").lower()
        if (clean_foler == "yes" or clean_foler == "y"):
            cleanup_folder()
    f = open(filePath, "a")
    while True:
        get_ita = input("Entre le mot : ")
        get_fra = input("Entre la sa traduction : ")
        if (get_ita == "EXIT()" or get_fra == "EXIT()"):
            f.close()
            return
        f.write(f"{get_ita}:{get_fra}\n")

def base(file_path, argv = "lang1"):
    numberOfLine = lineInFile(file_path)
    if numberOfLine:
        failNb = 0
        finish = questions(file_path,numberOfLine, failNb, argv)
        if (finish >= 1):
            while (finish >= 1):
                questions(f"Fail{failNb}.txt", numberOfLine, failNb, argv)
                failNb += 1

class COLOR():
    white = (255, 255, 255)
    black = (0, 0, 0)
    red = (138, 3, 3)
    green = (46, 139, 87)
    light_sky = (141,182,205)

class TextBox(object):
    def __init__(self, text:str, x:int, y:int):
        self.text = text
        self.x = x
        self.y = y
        self.font_text = pygame.font.SysFont("ヒラキノ角コシックw2", 30)

    def display_text(self):
        textsurface = self.font_text.render(self.text, True, COLOR.white)
        SCREEN.blit(textsurface,(self.x, self.y))

class ScreenChanger():
    def __init__(self, text, screen_color, speed, path):
        self.text = text
        self.x = (WIDTH / 2) - 50
        self.y = (HEIGHT / 2) - 25
        self.screen_color = screen_color
        self.speed = speed
        self.path = path

    def change_screen(self):
        text = TextBox(self.text, self.x, self.y)
        running = True
        while running:
            for event in pygame.event.get():
                if (event.type == pygame.QUIT):
                    exit()
                elif (event.type == pygame.KEYDOWN):
                    if (event.key == pygame.K_ESCAPE):
                        exit()
            SCREEN.fill(self.screen_color)
            text.display_text()
            pygame.display.update()
            pygame.time.delay(800)
            base_game(self.speed, self.path)

def enemies(text, rdm, ycoord, xcoord = (WIDTH / 2)):
    text = TextBox(text, xcoord - 50, ycoord)
    if (rdm % 2 == 0):
        icon = pygame.image.load("assets/asteroid_1.png").convert_alpha()
        icon = pygame.transform.scale(icon, (80, 80))
    else:
        icon = pygame.image.load("assets/asteroid_2.png").convert_alpha()
        icon = pygame.transform.scale(icon, (70, 100))
    pygame.display.set_icon(icon)
    SCREEN.blit(icon, (xcoord - 40, ycoord - 20))
    text.display_text()

def all_kind_of_text(*arg):
    arg

def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    only_ascii = nfkd_form.encode('ASCII', 'ignore')
    return only_ascii

add_speed = 0
def base_game(game_speed, file_path):
    global FAIL, SUCCESS, add_speed
    margin_down = 100
    if (args.increase):
        add_speed += 0.05
    motATrouver, result, lineNb = readFile(file_path)
    if (not motATrouver and not result and not lineNb):
        exit()
    x, y= random.randint(50, (WIDTH - (len(motATrouver) * 15))), -10
    placement = [(WIDTH / 2), (HEIGHT - margin_down), (WIDTH / 2), (HEIGHT - margin_down) + 3]
    user_input, stored_input = "", ""
    background_image = pygame.image.load("assets/background_1.jpg").convert_alpha()
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

    text_lose, screen_lose = TextBox(f"Fail : {str(FAIL)}", 10, 10), ScreenChanger("You LOSE", COLOR.red, game_speed, file_path)
    text_win, screen_win = TextBox(f"Win : {str(SUCCESS)}", (WIDTH - (len(str(SUCCESS)) * 30) - 70), 13), ScreenChanger("You WIN", COLOR.green, game_speed, file_path)
    input_rect = pygame.Rect(50, (placement[1] + 25), (WIDTH - 100), 45)
    if (args.cc):
        print(result)
    while True:
        SCREEN.blit(background_image, (0, 0))
        user_answer = TextBox(user_input, input_rect.x + 10, input_rect.y + 10)
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                exit()
            if (event.type == pygame.KEYDOWN):
                if (event.key == pygame.K_ESCAPE):
                    exit()
                else:
                    if (event.key == pygame.K_RETURN):
                        stored_input = user_input
                        if (remove_accents(stored_input) == remove_accents(result) and y < placement[1]):
                            SUCCESS += 1
                            #moveLocation(file_path, "success.txt", lineNb)
                            screen_win.change_screen()
                        else:
                            FAIL += 1
                            #moveLocation(file_path, "Fail.txt", lineNb)
                            screen_lose.change_screen()
                    elif (event.key == pygame.K_BACKSPACE):
                        user_input = user_input[:-1]
                    else:
                        user_input += event.unicode
        enemies(motATrouver, x, y, x)
        all_kind_of_text(user_answer.display_text(), text_win.display_text(), text_lose.display_text())
        if (y >= placement[1]):
            FAIL += 1
            #moveLocation(file_path, "Fail.txt", lineNb)
            screen_lose.change_screen()
        pygame.draw.rect(SCREEN, COLOR.light_sky, input_rect, 3)
        pygame.draw.line(SCREEN, COLOR.white, (placement[0], placement[1]), (placement[2], placement[3]), (WIDTH - 50))
        pygame.time.delay(game_speed)
        y += ((HEIGHT - margin_down + 10) / 500) + add_speed
        pygame.display.update()

def main():
    game_speed = 25
    file_path = "ita.txt"
    if (args.file):
        file_path = args.file
    if (args.add):
       add_to_txt(file_path)
       exit()
    if (args.lang):
        base(file_path, args.lang)
        exit()
    else:
        if (args.difficulty == "hard"):       game_speed = 15
        elif (args.difficulty == "medium"):   game_speed = 25
        elif (args.difficulty == "easy"):     game_speed = 35
        elif (args.difficulty == "EZ"):       game_speed = 5
        base_game(game_speed, file_path)

if __name__ == "__main__":
    main()