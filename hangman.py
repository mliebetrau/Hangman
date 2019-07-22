######################################################
## File Name: hangman.py                            ##
## Description: Simple Python Game                  ##
######################################################
import pygame
import random

pygame.init()
winHeight = 480
winWidth = 700
win = pygame.display.set_mode((winWidth, winHeight))

#---------------------------------------#
# initialize global variables/constants #
#---------------------------------------#
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (102, 255, 255)

btnFont = pygame.font.SysFont("arial", 20)
guessFont = pygame.font.SysFont("arial", 24)
endFont = pygame.font.SysFont("arial", 45)
word = ''
buttons = []
guessed = []
hangmanPictures = [pygame.image.load("hangman0.png"), pygame.image.load("hangman1.png"), pygame.image.load("hangman2.png"), pygame.image.load("hangman3.png"), pygame.image.load("hangman4.png"),
                   pygame.image.load("hangman5.png"), pygame.image.load("hangman6.png")]

limbs = 0

def redrawGameWindow():
    global guessed
    global hangmanPictures
    global limbs

    win.fill(GREEN)

    #----- Buttons -----#
    for i in range(len(buttons)):
        if buttons[i][4]:
            pygame.draw.circle(win, BLACK, (int(buttons[i][1]), int(buttons[i][2])), int(buttons[i][3]))
            pygame.draw.circle(win, buttons[i][0], (int(buttons[i][1]), int(buttons[i][2])), int(buttons[i][3]) - 2)
            label = btnFont.render(chr(buttons[i][5]), 1, BLACK)
            win.blit(label, (buttons[i][1] - (label.get_width() / 2), buttons[i][2] - (label.get_height() / 2)))

    spaced = spacedOut(word, guessed)
    firstLabel = guessFont.render(spaced, 1, BLACK)
    rectangle = firstLabel.get_rect()
    length = rectangle[2]

    win.blit(firstLabel, (winWidth / 2 - length / 2, 400))

    picture = hangmanPictures[limbs]
    win.blit(picture, (winWidth / 2 - picture.get_width() / 2 + 20, 150))
    pygame.display.update()

def randomWord():
    file = open('words.txt')
    f = file.readlines()
    rand = random.randrange(0, len(f) - 1)

    return f[rand][:-1]

def hang(guess):
    global word
    if guess.lower() not in word.lower():
        return True
    else:
        return False

def spacedOut(word, guessed = []):
    spacedWord = ''
    guessedLetters = guessed

    for x in range(len(word)):
        if word[x] != ' ':
            spacedWord += '_ '
            for i in range(len(guessedLetters)):
                if word[x].upper() == guessedLetters[i]:
                    spacedWord = spacedWord[:-2]
                    spacedWord += word[x].upper() + ' '
        elif word[x] == ' ':
            spacedWord += ' '
    return spacedWord

def buttonHit(x, y):
    for i in range(len(buttons)):
        if x < buttons[i][1] + 20 and x > buttons[i][1] - 20:
            if y < buttons[i][2] + 20 and y > buttons[i][2] - 20:
                return buttons[i][5]
    return None

def end(winner = False):
    global limbs
    lostText = 'You Lost, press any key to play again...'
    winText = 'Winner! Press any key to play again...'

    redrawGameWindow()
    pygame.time.delay(1000)
    win.fill(GREEN)

    if winner == True:
        label = endFont.render(winText, 1, BLACK)
    else:
        label = endFont.render(lostText, 1, BLACK)

    wordText = endFont.render(word.upper(), 1, BLACK)
    wordWas = endFont.render('The phrase was: ', 1, BLACK)

    win.blit(wordText, (winWidth / 2 - wordText.get_width() / 2, 295))
    win.blit(wordWas, (winWidth / 2 - wordWas.get_width() / 2, 245))
    win.blit(label, (winWidth / 2 - label.get_width() / 2, 140))

    pygame.display.update()
    again = True
    while again:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                again = False
    reset()

def reset():
    global limbs
    global guessed
    global buttons
    global word

    for i in range(len(buttons)):
        buttons[i][4] = True

    limbs = 0
    guessed = []
    word = randomWord()


#----- Setup Buttons -----#
increase = round(winWidth / 13)

for i in range(26):
    if i < 13:
        y = 40
        x = 25 + (increase * i)
    else:
        x = 25 + (increase * (i - 13))
        y = 85

    buttons.append([LIGHT_BLUE, x, y, 20, True, 65 + i])
    # color, x_pos, y_pos, radius, visible, character

word = randomWord()
inPlay = True

while inPlay:
    redrawGameWindow()
    pygame.time.delay(10)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            inPlay = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                inPlay = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            clickPosition = pygame.mouse.get_pos()
            letter = buttonHit(clickPosition[0], clickPosition[1])
            if letter != None:
                guessed.append(chr(letter))
                buttons[letter - 65][4] = False
                if hang(chr(letter)):
                    if limbs != 5:
                        limbs += 1
                    else:
                        end()
                else:
                    print(spacedOut(word, guessed))
                    if spacedOut(word, guessed).count('_') == 0:
                        end(True)

pygame.quit()