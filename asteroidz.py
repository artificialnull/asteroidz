#Asteroidz by 
creatorName = "Ishan Kamat"
#mainSound = raw_input("Please provide the filename of the main theme.\nMake sure it is either in the .ogg or .mp3 format\nLeave blank to use default: ")
#menuSound = raw_input("\nNow for the menu theme. Same rules apply: ")
mainSound = "asteroidz_theme.wav"
menuSound = ""
import pygame
from random import randint, choice, random
from time import sleep, time
import thread
pygame.init()

pygame.mouse.set_visible(False)
info = pygame.display.Info()
sW = info.current_w
sH = info.current_h
def text(text, size=16, color=(255,255,255), font=None):
	fontRatio = 1
	if font != None:
		if font == "mono":
			textfont = pygame.font.Font(fontsPath + "asteroidz-mono.ttf", int(size * fontRatio))
		else:
			textfont = pygame.font.SysFont(font, size)
	else:
		textfont = pygame.font.Font(fontsPath + "asteroidz.ttf", int(size * fontRatio))
	return textfont.render(text, False, color)

##Music Functions
def loadMusic(filename):
	pygame.mixer.music.load(filename)
def playMusic(loops = 0, start=0.0):
	pygame.mixer.music.play(loops, start)
def stopMusic():
	pygame.mixer.music.stop()
def pauseMusic():
	pygame.mixer.music.pause()
def unpauseMusic():
	pygame.mixer.music.unpause()
def fadeoutMusic(millis):
	pygame.mixer.music.fadeout(millis)
def changeVolume(percent):
	realValue = float(percent) / 100
	log(realValue)
	pygame.mixer.music.set_volume(realValue)
##/Music Functions

loadImage = pygame.image.load
whiteRGB = (255,255,255)
blackRGB = (0,0,0)
def centerX(thing):
	width = thing.get_width()
	return (sW - width) / 2

whiteCK = pygame.Color(255, 255, 255)
blackCK = pygame.Color(0, 0, 0)
##Settings
imagePath = "./resources/image/"
textsPath = "./resources/texts/"
fontsPath = "./resources/fonts/"
soundPath = "./resources/sound/"
logPath = "./logs/"
startLogTime = time()
soundSetting = 1
colorKeySetting = 1
backgroundColorKey = 0 ### Depends on $colorKeySetting.
frameLimitSetting = 1
fullScreenSetting = 1
fullResolutionSetting = 0
fancyAnimationSetting = 1
healthCheatSetting = 0
multiColorLoadingBar = 0
showLoadingStuff = 1
convertImages = 1 ### Changes them into fast format. 
logSetting = 0 ### Records things and stores them in log file(s).
useArtificialIntelligence = 0
maxStars = 500
starThread = 0
shipChoice = ("N","T")[0] ### This doesn't work anymore!
if frameLimitSetting:
	frameLimit = 60
if not fullResolutionSetting:
	sW = 1366
	sH = 768
if healthCheatSetting:
	healthCheatValue = 24
maxLogLength = 500 * 1000
continueText = text("press BACKSPACE to go back", 14)
creatorText = text("Created by " + creatorName, 10)
##/Settings

print "\nUsing..."
if mainSound == "":
	mainSound = soundPath + "heatwave.mp3"
if menuSound == "":
	menuSound = soundPath + "spacebattle.mp3"

if "./" not in mainSound:
	mainSound = "./" + mainSound
if "./" not in menuSound:
	menuSound = "./" + menuSound

print mainSound
print menuSound
sleep(0.3)

maxShipDeviation = sW / 100
#maxShipDeviation = 0
toLog = ""
clock = pygame.time.Clock()
logFileName = str(startLogTime)
logFileName_append = 1
shipChange = 10

heartCount = 0
rockCount = 0
junkCount = 0
#pygame.HWSURFACE
#pygame.FULLSCREEN
s = pygame.display.set_mode(
	(sW,sH), 
	pygame.FULLSCREEN if fullScreenSetting else 0
)
def log(text):
	global toLog
	if logSetting:
		logTime = float(int(float(time() - startLogTime) * 100)) / 100.0 
		toLog += str(logTime) + " " * (5 - len(str(logTime))) + ": " + str(text) + "\n"

def quitGame():
	log("Entering endMenu")
	endMenu()
	log("QUITTING!")
	log(rockCount)
	log(heartCount)
	log(junkCount)
	print rockCount
	print heartCount
	print junkCount
	writeLogFile()
	raise SystemExit

def writeLogFile():
	global toLog
	global logFileName_append
	logFile = open(logPath + "game_" + logFileName + "_" + str(logFileName_append) + ".txt", "w")
	logFile.write(toLog)
	logFile.close()
	toLog = ""
	logFileName_append += 1

starRects = []
starColors = [(120, 120, 255), (255, 60, 60), (250, 200, 100), (200, 200, 200)]
chances = [1, 1, 5, 4]
newStarColors = []
for starColor in starColors:
	newList = [starColor] * chances[starColors.index(starColor)]
	newStarColors = newStarColors + newList
starColors = newStarColors
def genStars(anywhere=False):
	global starRects
	while len(starRects) < maxStars:
		color = choice(starColors)
		size = randint(100, 400)
		posX = sW + 10
		if anywhere:
			posX = randint(0, sW)
		posY = randint(0, sH)
		speed = float(size) / 200.0
		size = size / 100.0
		starRects.append([color, size, posX, posY, speed])
def loadStars():
	global starRects
	newStars = []
	for thing in starRects:
		color, size, posX, posY, speed = thing
		pygame.draw.rect(s, color, pygame.Rect(posX, posY, size, size))
		#pygame.display.flip()
		posX -= speed
		if posX > (0-size):
			newStars.append([color, size, posX, posY, speed])
	starRects = newStars
def clearStars():
	pass
##Start Menu
def startMenu():
###Gameplay Explanation
	def gamePlayExplanation():
		s.fill(blackRGB)
		loadStars()
		log("In gamePlayExplanation")
####Controls
		controls = ""
		controlFile = open(textsPath + "controls.txt")
		for line in controlFile.read().split("\n"):
			action, key = line.split("|")
			controls += action + ": " + (" " * (15 - len(action))) + key + "\n"
		controlTexts = []
		controlFontSize = 18
		for line in controls.split("\n"):
			controlTexts.append(text(line, controlFontSize, font="mono"))
		controlYCoord = 200
		for controlText in controlTexts:
			s.blit(controlText, (100, controlYCoord))
			controlYCoord += controlFontSize + 5
####/Controls

####Gameplay
		gameplayLines = []
		gameplayFontSize = 30
		gameplayFile = open(textsPath + "gameplay.txt")
		for line in gameplayFile.read().split("\n"):
			gameplayLines.append(text(line, gameplayFontSize))
		gameplayYCoord = controlYCoord + 75
		for gameplayLine in gameplayLines:
			s.blit(gameplayLine, ((sW - gameplayLine.get_width()) / 2, gameplayYCoord))
			gameplayYCoord += gameplayFontSize
####/Gameplay

		titleText = text("CONTROLS + GAMEPLAY", 50)
		s.blit(titleText, ((sW - titleText.get_width()) / 2, 50))
		s.blit(continueText, (sW - continueText.get_width() - 20, sH - continueText.get_height() - 20))
		pygame.display.flip()
		continued = False
		while not continued:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					raise SystemExit
				elif event.type == pygame.KEYDOWN: 
					if event.key == pygame.K_BACKSPACE:
						continued = True
						s.fill(blackRGB)
						return 1
					elif event.key == pygame.K_ESCAPE:
						raise SystemExit
###/Gameplay Explanation

###Play the Game
	def playTheGame():
		log("playTheGame has run")
		return 0
###/Play the Game

###About the Game
	def aboutGame():

		log("In aboutGame")
		aboutFile = open(textsPath + "about.txt")
		aboutList = aboutFile.read().split("\n")
		aboutListTexts = []
		aboutFontSize = 40
		for aboutLine in aboutList:
			aboutListTexts.append(text(aboutLine.format(creatorName), aboutFontSize))
		startPosition = aboutFontSize * 3
		topBlockHeight = startPosition
		firstPixel = startPosition
		lastPixel = firstPixel + len(aboutList) * aboutFontSize
		scrollSpeedFactor = 0.15
		while lastPixel > 0.9 * topBlockHeight:
			#clock.tick(120)
			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						raise SystemExit
					elif event.key == pygame.K_BACKSPACE:
						return 2
				elif event.type == pygame.QUIT:
					raise SystemExit
			log(str(firstPixel) + ", " + str(lastPixel))
			aboutCount = 0
			s.fill(blackRGB)
			loadStars()
			for aboutText in aboutListTexts:
				s.blit(aboutText, ((sW - aboutText.get_width()) / 2, aboutFontSize * aboutCount + firstPixel))
				aboutCount += 1
			firstPixel -= scrollSpeedFactor
			lastPixel -= scrollSpeedFactor
			pygame.draw.rect(s, blackRGB, pygame.Rect(0,0, sW, topBlockHeight))
			pygame.draw.rect(s, blackRGB, pygame.Rect(0, sH - topBlockHeight, sW, topBlockHeight))
			s.blit(continueText, (sW - continueText.get_width() - 20, sH - continueText.get_height() - 20))
			pygame.display.flip()
		return 2

###/About the Game

	log("Started")
	if soundSetting:
		loadMusic(menuSound)
		playMusic(-1)
		log("Playing music")
	logoImage = loadImage(imagePath + "logo.png").convert()
	#logoImage.set_colorkey(blackCK)
	logoResizeFactor = 15
	logoImage = pygame.transform.scale(logoImage, (logoImage.get_width() * logoResizeFactor, 
		logoImage.get_height() * logoResizeFactor))
	menuChoices = [
		"Start",
		"Gameplay",
		"Credits",
	]
	menuChoicesTexts = []
	menuChoiceFontSize = 40
	for menuChoice in menuChoices:
		menuChoicesTexts.append(text(menuChoice, menuChoiceFontSize))

	unBroken = True
	selectorPoint_1 = (sW / 3, sH / 2 + (0.75 * menuChoiceFontSize))
	selectorPoint_2 = (sW / 3, sH / 2 + (0.25 * menuChoiceFontSize))
	selectorPoint_3 = (sW / 3 + (0.5 * menuChoiceFontSize), sH / 2 + (0.5 * menuChoiceFontSize))

	selectionNumber = 0

	menuChoiceKey = {
		0: playTheGame,
		1: gamePlayExplanation,
		2: aboutGame
	}
	genStars(True)

	while unBroken:
		selectorPoints = [
			selectorPoint_1,
			selectorPoint_2,
			selectorPoint_3
		]
		s.fill(blackRGB)
		s.blit(logoImage, ((sW - logoImage.get_width()) / 2, 50))
		selector = pygame.draw.polygon(s, whiteRGB, selectorPoints)
		genStars()
		loadStars()
		choicesDisplayed = 0
		for menuChoicesText in menuChoicesTexts:
			s.blit(menuChoicesText, ((sW - menuChoicesText.get_width()) / 2, (sH / 2) + (menuChoiceFontSize * choicesDisplayed)))
			choicesDisplayed += 1
		pygame.display.update()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pass
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					raise SystemExit
				elif event.key == pygame.K_UP and selectorPoint_2[1] >= sH / 2 + menuChoiceFontSize and selectionNumber != 0:
					selectionNumber -= 1
					selectorPoint_1 = (selectorPoint_1[0], selectorPoint_1[1] - menuChoiceFontSize)
					selectorPoint_2 = (selectorPoint_2[0], selectorPoint_2[1] - menuChoiceFontSize)
					selectorPoint_3 = (selectorPoint_3[0], selectorPoint_3[1] - menuChoiceFontSize)
				elif (event.key == pygame.K_DOWN and selectorPoint_1[1] < (sH / 2) + len(menuChoices) * menuChoiceFontSize and
						selectionNumber != choicesDisplayed - 1):
					selectorPoint_1 = (selectorPoint_1[0], selectorPoint_1[1] + menuChoiceFontSize)
					selectorPoint_2 = (selectorPoint_2[0], selectorPoint_2[1] + menuChoiceFontSize)
					selectorPoint_3 = (selectorPoint_3[0], selectorPoint_3[1] + menuChoiceFontSize)
					selectionNumber += 1
				elif event.key == pygame.K_RETURN:
					unBroken = menuChoiceKey[selectionNumber]()
					#print unBroken
					if unBroken == 2:
						genStars(True)
						unBroken = 1
##/Start Menu

##End Menu
def endMenu():
	finalScore = score
	totalTime = time() - startPlayTime
	totalTime = float(int(totalTime * 100)) / 100.0
	finalScoreHeader = text("Final Score:", 40)
	finalScoreText = text(str(finalScore), 40)
	totalTimeHeader = text("Total Time:", 40)
	totalTimeText = text(str(totalTime) + " seconds", 40)
	gameOverHeader = text("GAME OVER", 120)
	statsHeader = text("Stats:", 50)
	enterText = text("press ENTER to continue")
	collisionsHeader = text("Collisions:", 40)
	enterX = sW - enterText.get_width() - 20
	enterY = sH - enterText.get_height() - 20
	enterRect = pygame.Rect(enterX, enterY, enterText.get_width(), enterText.get_height())
	s.fill(blackRGB)
	loadStars()
	stopMusic()
	s.blit(gameOverHeader, (centerX(gameOverHeader), 20))
	s.blit(statsHeader, (centerX(statsHeader), sH / 2.1))
	prevY = sH / 2.1 + statsHeader.get_height()
	s.blit(finalScoreHeader, (centerX(finalScoreHeader), prevY + 20))
	prevY = prevY + 20 + finalScoreHeader.get_height()
	s.blit(finalScoreText, (centerX(finalScoreText), prevY + 20))
	prevY = prevY + 20 + finalScoreText.get_height()
	s.blit(totalTimeHeader, (centerX(totalTimeHeader), prevY + 30))
	prevY = prevY + 30 + totalTimeHeader.get_height()
	s.blit(totalTimeText, (centerX(totalTimeText), prevY + 20))
	prevY = prevY + 20 + totalTimeText.get_height()
	broken = False
	badSound.play()
	while not broken:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				return 1
			elif event.type == pygame.KEYDOWN:
				if event.key in [pygame.K_ESCAPE , pygame.K_RETURN]:
					return 1
		pygame.draw.rect(s, blackRGB, enterRect)
		pygame.display.flip()

		sleep(0.5)
		
		s.blit(enterText, (enterX, enterY))
		pygame.display.flip()

		sleep(0.5)

		clock.tick(fps)
##/End Menu

startMenu()

if showLoadingStuff:
	musicFadeOutTimeMs = 2000
else:
	musicFadeOutTimeMs = 100
fadeoutMusic(musicFadeOutTimeMs)
log("Music fading out")

##Loading

###Loading Setup
loadingBarY = sH / 2 - 10
loadingBarMax = 200
currentLoadingLength = 0
loadingSegments = 10
loadingOffset = loadingBarMax / loadingSegments
loadingBarX = sW / 2 - loadingBarMax / 2
creatorText = text("Created by " + creatorName, 10)
def loadMore(delay=10, loadingText="", endDelay=0.1):
	global currentLoadingLength

	if not showLoadingStuff:
		return 1
	delay = float(delay) / 1000
	for x in range(0, loadingOffset):
		loadingBar = pygame.Rect(loadingBarX, loadingBarY, currentLoadingLength, 10)
		barColor = (randint(63, 255),randint(63, 255),randint(63, 255)) if multiColorLoadingBar else (255,255,255)
		pygame.draw.rect(s, barColor, loadingBar)
		currentLoadingLength += 1
		loadingHint = text(loadingText, 20)
		loadingBarTextX = (sW - loadingHint.get_width()) / 2
		s.blit(loadingHint, (loadingBarTextX, loadingBarY - 50))
		s.blit(creatorText, (sW - creatorText.get_width() - 2, sH - creatorText.get_height() - 2))
		pygame.display.flip()
		s.fill(blackRGB)
		#loadStars()
		log(currentLoadingLength)

		sleep(delay / 2)
	sleep(endDelay / 5)
	log(loadingText)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			raise SystemExit
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				raise SystemExit
###/Loading Setup

shootSound = pygame.mixer.Sound(soundPath + 'shoot.wav')
destroySound = pygame.mixer.Sound(soundPath + 'destroy.wav')
goodSound = pygame.mixer.Sound(soundPath + 'good.wav')
thumpSound = pygame.mixer.Sound(soundPath + 'thump.wav')
badSound = pygame.mixer.Sound(soundPath + 'bad2.wav')
alarmSound = pygame.mixer.Sound(soundPath + 'alarm.wav')

loadMore(10, "Launch...")

background = loadImage(imagePath + "background.png")
background = pygame.transform.scale(background, (sW, sH))
loadMore(20, "Orbital Insertion...")

shipX = 100
shipY = sH / 2
ship = loadImage(imagePath + "spaceship" + shipChoice + ".png")
hull = loadImage(imagePath + "hull.png")
wingUp = loadImage(imagePath + "wingu.png")
wingDown = loadImage(imagePath + "wingd.png")
rockBasis1 = loadImage(imagePath + "rock1.png")
rockBasis2 = loadImage(imagePath + "rock2.png")
rockBasis3 = loadImage(imagePath + "rock3.png")
rockBases = [rockBasis1, rockBasis2, rockBasis3]
heartRock = loadImage(imagePath + "healthrock.png")
explosion = loadImage(imagePath + "explosion.png")
bullet = loadImage(imagePath + "bullet.png")
spaceJunk1 = loadImage(imagePath + "spacejunk1.png")
spaceJunks = [spaceJunk1]
#back1 = loadImage(imagePath + "starsheet1.png").convert()
#back2 = loadImage(imagePath + "starsheet2.png").convert()
#back3 = loadImage(imagePath + "starsheet3.png").convert()
#back1.set_colorkey(blackCK)
#back2.set_colorkey(blackCK)
#back3.set_colorkey(blackCK)
#backs = [back1, back2, back3]
#back1X = 0
#back2X = 0
#back3X = 0
#back1Rate = 10
#back2Rate = 5
#back3Rate = 2
bullet = pygame.transform.scale(bullet, (10,5))
if convertImages:
	background = background.convert()
	heartRock = heartRock.convert()
	explosion = explosion.convert()
	ship = ship.convert()
	bullet = bullet.convert()
	hull = hull.convert()
	wingUp = wingUp.convert()
	wingDown = wingDown.convert()
	rockBasesIndex = 0
	for rockBasis in rockBases:
		rockBases[rockBasesIndex] = rockBasis.convert()
		rockBasesIndex += 1
	junkIndex = 0
	for junk in spaceJunks:
		spaceJunks[junkIndex] = junk.convert()
		junkIndex += 1
loadMore(25, "Burning to Escape...")

whites = ["N"]
if colorKeySetting:
	shipColorKey = whiteCK if shipChoice in whites else blackCK
	ship.set_colorkey(shipColorKey) 
	hull.set_colorkey(shipColorKey)
	wingUp.set_colorkey(shipColorKey)
	wingDown.set_colorkey(shipColorKey)
	heartRock.set_colorkey(whiteCK)
	explosion.set_colorkey(blackCK)
	bullet.set_colorkey(whiteCK)
	for rockBasis in rockBases:
		rockBasis.set_colorkey(whiteCK)
	for junk in spaceJunks:
		junk.set_colorkey(whiteCK)
	if backgroundColorKey: background.set_colorkey(whiteCK)

loadMore(40, "Hibernating...", 0.3)
wingUpOffset = (32, -10)
wingDownOffset = (23, 20)
wUMask = pygame.mask.from_surface(wingUp)
hullMask = pygame.mask.from_surface(hull)
wDMask = pygame.mask.from_surface(wingDown)
rocks = {
}
# rock: (positionX, positionY, movementSpeed, angle, rotationSpeed, rockHealth)
	# DO NOT INCLUDE HEARTS!
otherThings = {
}
# thing: (positionX, positionY, movementSpeed, identifier)
	# Can include hearts and stuff.
maxRocks = 1
maxThings = 3
score = 0
health = 100
shot = False
fps = 0
fullHealthBarLength = sW * 0.4
doShoot = False
doUp = False
doDown = False
loadMore(5, "Resuming...")
jitterTuple = [None, None]

def dispExplosions():
	global toExplode

	explosionIndexCounter = 0
	for rockInfo in toExplode:
		newExplosion = pygame.transform.scale(explosion, (rockInfo[2], rockInfo[3]))
		newExplosion = pygame.transform.rotate(newExplosion, randint(0, 359))
		s.blit(newExplosion, (rockInfo[0], rockInfo[1]))
		log(toExplode[explosionIndexCounter])
		if rockInfo[4] < 1:
			toExplode.pop(explosionIndexCounter)
		else:
			toExplode[explosionIndexCounter] = [rockInfo[0], 
				rockInfo[1], 
				rockInfo[2], 
				rockInfo[3], 
				rockInfo[4] - 1
			]
			explosionIndexCounter += 1
loadMore(5, "Entering Asteroid Belt...")
aiMultiplyYChange = 0
wingUpDestroyed = False
wingDownDestroyed = False
def loadRocks():
	global rocks, maxRocks
	global health
	global score
	global toExplode
	global shotX, shotY, shot
	global rockCount
	global wingUpDestroyed, wingDownDestroyed

	someIntersection = False
	for rock in rocks.keys():
		oldRock = rock
		markForDelete = False
		positionX, positionY, movementSpeed, angle, rotationSpeed, rockHealth = rocks[rock]
		positionX -= movementSpeed[0]
		positionY -= movementSpeed[1]
		if fancyAnimationSetting:
			rock = pygame.transform.rotate(rock, angle)
		newPosX = int(positionX) - int(0.5 * rock.get_height())
		newPosY = int(positionY) - int(0.5 * rock.get_height())
		log(rock)
		log(str(newPosX) + ", " + str(newPosY))
		rockMask = pygame.mask.from_surface(rock)
		angle += rotationSpeed
		rockHealthText = text(str(rockHealth), 12, (255,0,0))
		s.blit(rock, (newPosX, newPosY))
		s.blit(rockHealthText, (positionX - int(0.5 * rockHealthText.get_width()), 
			positionY - int(0.5 * rockHealthText.get_height())))
		collisionCheck = checkShipCollision(rockMask, newPosX, newPosY)
		if collisionCheck == 1:
			rockDamage = (
				float((rock.get_width() * 0.2) 
					+ (rotationSpeed * 0.9) 
					+ (movementSpeed[0] * 0.5)
					+ (movementSpeed[1] * 0.5)) 
				+ rockHealth
				) * 0.75
			health -= rockDamage
			rockCount += 1
			if health < 0:
				quitGame()
			markForDelete = True
		elif collisionCheck == 2:
			wingUpDestroyed = True
			markForDelete = True
		elif collisionCheck == 3:
			wingDownDestroyed = True
			markForDelete = True
		#elif rockMask.overlap(wUMask, ())
		elif rockMask.overlap(bulletMask, (shotX - newPosX,shotY - newPosY)):
			rockHealth -= 5
			if rockHealth < 1:
				markForDelete = True
				score += 1
			else:
				if soundSetting:
					thumpSound.play()
					#print "wowowowo"
					#print newPosX, newPosY, shotX, shotY
			shot = False
			s.blit(bullet, (-1000, -1000))
			shotX = -1000
			shotY = -1000
		if markForDelete:
			if soundSetting:
				destroySound.play()
				#print "WODMWOADMSOKA"
			del rocks[oldRock]
			toExplode.append([newPosX, newPosY, rock.get_width(), rock.get_height(), randint(7,11)])
		else:
			rocks[oldRock] = (positionX, positionY, movementSpeed, angle, rotationSpeed, rockHealth)
		markForDelete = False
	
loadMore(20, "Circularizing...")

def makeRocks():
	global rocks

	intHealthFrac = int(health / 10.0)
	if intHealthFrac < 2:
		intHealthFrac = 2
	while len(rocks.keys()) < maxRocks:
		newSize = randint(30, 120)
		rockBasis = choice(rockBases)
		rock = pygame.transform.scale(rockBasis, (newSize, newSize))
		positionX = sW + randint(10, 200) + newSize
		positionY = randint(0, sH - int(0.5 * newSize))
		if randint(0, 1):
			vertSpeed = random()
			if vertSpeed > 0.5:
				vertSpeed = 0.5
		else:
			vertSpeed = (0.0 - random())
			if vertSpeed < -0.5:
				vertSpeed = -0.5
		movementSpeed = [randint(4, int(17 - (newSize * 0.1))), vertSpeed]
		angle = randint(0,359)
		rotationSpeed = randint(-10,10)
		rockHealth = randint(
			int(newSize * 0.1),
			int(newSize * 0.125)
			)
		#positionY = sH - 200
		#movementSpeed = [4, -0.7]
		if rock not in rocks.keys():
			rocks[rock] = (positionX, positionY, movementSpeed, angle, rotationSpeed, rockHealth)
			log(rocks[rock])
loadMore(15, "Locating Asteroids...")

def deleteRocks():
	global rocks

	for rock in rocks.keys():
		if rocks[rock][0] + rock.get_width() < -10:
			del rocks[rock]
		else:
			yTop = rocks[rock][1] - rock.get_height()
			yBot = rocks[rock][1] + rock.get_height()
			if yBot < 0 or yTop > sH :
				del rocks[rock]
		rock = [999999]

junkCounter = 0

def makeThings():
	global otherThings
	global junkCounter

	#healthIntFrac = int(health) * 10
	#if healthIntFrac < 2: healthIntFrac = 2
	junkRandHealth = (100 - int(health)) * 50
	junkRandHealth = 2 if junkRandHealth < 2 else junkRandHealth
	#log(healthIntFrac)
	log(junkRandHealth)
	if len(otherThings.keys()) < maxThings:
		if health != 100 and randint(1, 300) == 1 and heartRock not in otherThings.keys():
			thing = heartRock
			positionX = sW + heartRock.get_width() + randint(50, 250)
			positionY = randint(0, sH - heartRock.get_height())
			while shipY <= positionY <= shipY + ship.get_height():
				positionY = randint(0, sH - heartRock.get_height())
			movementSpeed = 10
			identifier = "001"
			otherThings[thing] = (positionX, positionY, movementSpeed, identifier)
		if health > 25 and randint(1, junkRandHealth) == 1:
			if junkCounter == 0:
				angle = randint(-45, 45)
				spaceJunk = choice(spaceJunks)
				spaceJunk = pygame.transform.rotate(spaceJunk, angle)
				positionX = sW + spaceJunk.get_width() + randint(10, 20)
				positionY = randint(0, sH - spaceJunk.get_height())
				movementSpeed = 15
				identifier = "002"
				otherThings[spaceJunk] = (positionX, positionY, movementSpeed, identifier)
				junkCounter = 1

def loadThings():
	global otherThings
	global health
	global toExplode
	global junkCounter
	global junkCount, heartCount
	global wingUpDestroyed, wingDownDestroyed

	for thing in otherThings.keys():
		positionX, positionY, movementSpeed, identifier = otherThings[thing]
		positionX -= movementSpeed
		#newPosX = positionX - int(0.5 * thing.get_width())
		#newPosY = positionY - int(0.5 * thing.get_height())
		thingMask = pygame.mask.from_surface(thing)
		s.blit(thing, (positionX, positionY))
		collisionCheck = checkShipCollision(thingMask, positionX, positionY)
		if collisionCheck != 0:
			if identifier == "001":
				health = 100
				heartCount += 1
				if soundSetting:
					goodSound.play()
			if identifier == "002":
				health -= randint(15, 25)
				if health < 0:
					quitGame()
				junkCount += 1
				if soundSetting:
					destroySound.play()
					junkCounter = 0
					toExplode.append([positionX, positionY, thing.get_width(), thing.get_height(), randint(2,4)])
			del otherThings[thing]
		else:
			otherThings[thing] = (positionX, positionY, movementSpeed, identifier)

def deleteThings():
	global otherThings
	global junkCounter

	for thing in otherThings.keys():
		if otherThings[thing][0] + thing.get_width() < -10:
			if otherThings[thing][3] == "002":
				junkCounter = 0
			del otherThings[thing]
		thing = [99999]

##AI
aiMultiplier = 1
def artificialIntelligence():
	global doUp, doDown, doShoot, aiMultiplier

	oldAM = aiMultiplier
	shipHeight = int(ship.get_height() * 1.25)
	print shipHeight, "SHIP_HEIGHT"
	#print shipHeight
	midShip = shipY + int(0.5 * shipHeight)
	shipFromTop = shipY
	shipFromBottom = sH - midShip
	lowestX = sW
	rockDexes = []
	badDexes = []
	for rock in rocks.keys():
		positionX, positionY, movementSpeed, angle, rotationSpeed, rockHealth = rocks[rock]
		newPosY = positionY - int(0.5 * rock.get_height())
		newPosY = int(newPosY)
		newShipY = int(shipY) + wingUpOffset[1]
		if positionX < lowestX and positionX > 0:
			rockDexes = []
			for pix in range(newPosY, newPosY + rock.get_height()):
				rockDexes.append(pix)
			oldDB = badDexes
			badDexes = []
			for pix in range(newShipY, newShipY + shipHeight):
				if pix in rockDexes:
					badDexes.append(pix - newShipY)
			if badDexes != []:
				lowestX = positionX
			else:
				badDexes = oldDB

	print lowestX, shipY + (4 * ship.get_width())
	if len(badDexes) > 0 and lowestX < newShipY + (4 * ship.get_width()):
		print "DANGER AHEAD!"
		topPixel = badDexes[0]
		bottomPixel = badDexes[-1]
		print topPixel, bottomPixel
		fromTop = topPixel
		fromBottom = shipHeight - bottomPixel - 1
		print fromTop, fromBottom, "TB"
		if fromTop != 0 or fromBottom != 0:
			print "NOT TOO BIG"
			if fromTop > fromBottom:
				print 1
				if shipFromTop >= (10 * aiMultiplier):
					aiMultiplier = 1
					print 1.1
					doUp = True
					doDown = False
				else:
					aiMultiplier += 1
					print 1.2
					doDown = True
					doUp = False
			elif fromTop < fromBottom:
				print 2
				if shipFromBottom < shipHeight + (10 * aiMultiplier):
					aiMultiplier = 1
					print 2.1
					doUp = True
					doDown = False
				else:
					aiMultiplier += 1
					print 2.2
					doDown = True
					doUp = False
			else:
				print 3
				if shipFromTop < shipFromBottom:
					print 3.1
					doUp = False
					doDown = True
				elif shipFromTop > shipFromBottom:
					print 3.1
					doUp = True
					doDown = False
		else:
			print "BIG ROCK AHEAD"
			topOfRock = rockDexes[0]
			bottomOfRock = rockDexes[-1]
			fromTop = topOfRock - shipY
			fromBottom = bottomOfRock - shipY - shipHeight
			print fromTop, fromBottom
			if fromTop > fromBottom:
				print 1
				if shipFromTop >= 10:
					print 1.1
					doUp = True
					doDown = False
				else:
					print 1.2
					doDown = True
					doUp = False
			elif fromTop < fromBottom:
				print 2
				if shipFromBottom < shipHeight + 10:
					print 2.1
					doUp = True
					doDown = False
				else:
					print 2.2
					doDown = True
					doUp = False
			else:
				print 3
				if shipFromTop < shipFromBottom:
					print 3.1
					doUp = False
					doDown = True
				elif shipFromTop > shipFromBottom:
					print 3.1
					doUp = True
					doDown = False
	elif len(badDexes) > 0 and lowestX >= shipY + (2 * ship.get_width()):
		doShoot = True
		#pass
	else:
		pass		

	if oldAM == aiMultiplier:
		aiMultiplier = 1		
##/AI				
def checkShipCollision(mask, posX, posY):
	if mask.overlap(hullMask, (shipX - posX,int(shipY) - posY)):
		return 1
	elif mask.overlap(wUMask, (int(wingUpCoords[0]) - posX, int(wingUpCoords[1]) - posY)) and wingUpDestroyed == False:
		return 2
	elif mask.overlap(wDMask, (int(wingDownCoords[0]) - posX, int(wingDownCoords[1]) - posY)) and wingDownDestroyed == False:
		return 3
	else:
		return 0

loadMore(5, "Engaging Gun...")

oldH = 1
oldFPS = 1
oldSR = 1
healthBar = 0
fps = 0
score = 0
lastShotCounter = 0
firstShotCounter = 0
currentShipDeviation = 0
direction = randint(-1,1)
while direction == 0:
	direction = randint(-1,1)
loadMore(5, "Ready to go!", 0.5)
toExplode = []
##/Loading

if soundSetting:
	loadMusic(mainSound)
	playMusic(-1)
	changeVolume(100)
s.blit(bullet, (-1000, -1000))
shotX = -1000
shotY = -1000
#defaultBulletRect = pygame.Rect(-100, -100, 10, 5)
#bulletRect = defaultBulletRect
startPlayTime = time()
startMaxRocks = 3
bulletMask = pygame.mask.from_surface(bullet)
shipMask = pygame.mask.from_surface(ship)
wingUpCoords = (0,0)
wingDownCoords = (0,0)



firstRun = True
genStars(True)
alarmLength = alarmSound.get_length()
alarmLastPlayed = time()
while True:
	#print pygame.mixer.music.get_volume()
	totalTime = time() - startPlayTime
	if health <= 25 and time() - alarmLastPlayed >= alarmLength:
		#print time() - alarmLastPlayed
		#print alarmLength
		alarmLastPlayed = time()
		alarmSound.play()

	maxRocks = int(totalTime / 60) + startMaxRocks
	if maxRocks > 15:
		maxRocks = 15

	if healthCheatSetting: health = healthCheatValue

	if fancyAnimationSetting:
		oldShipDeviation = currentShipDeviation
		currentShipDeviation = oldShipDeviation + direction
		if (currentShipDeviation > maxShipDeviation 
			or currentShipDeviation < (0 - maxShipDeviation)):
			if direction == -1:
				direction = 1
			elif direction == 1:
				direction = -1
	
	healthColor = (255 * (100 - health) * 0.01, 255 * health * 0.01, 0)
	if oldH != health:
		#healthText = text("Health: " + healthBar, 20, healthColor)
		healthBar = pygame.Rect((sW - fullHealthBarLength) / 2, 20, int(fullHealthBarLength * (float(health) / 100)), 20)
		healthString = str(float(health))
		while len(healthString) > 5:
			healthString = str(float(int(health * 10) / 10))
		while len(healthString) < 5:
			healthString += "0"
		healthString += "/100"
		healthText = text(healthString, 20, whiteRGB)
	if oldFPS != fps:
		fpsText = text("FPS: " + str(fps), 12)
	if oldSR != score:
		scoreText = text("Score: " + str(score), 24)
	oldSR = score
	oldFPS = fps
	oldH = health
	#shipRect = pygame.draw.rect(
	#	s, 
	#	blackRGB, 
	#	pygame.Rect(
	#		shipX + 10, 
	#		shipY + 10, 
	#		ship.get_width() - 10, 
	#		ship.get_height() - 10
	#		)
	#	)
	
	makeRocks()
	deleteRocks()
	makeThings()
	deleteThings()
	s.fill(blackRGB)
	if fancyAnimationSetting:
		genStars()
		if starThread:
			thread.start_new_thread(loadStars, ())
		else:
			loadStars()
	else:
		s.blit(background, (0,0))

	s.blit(scoreText, (10,10))
	pygame.draw.rect(s, healthColor, healthBar)
	s.blit(healthText, ((sW - healthText.get_width()) / 2, 21))
	s.blit(fpsText, (sW - fpsText.get_width() - 10, 10))
	loadRocks()
	loadThings()

	if useArtificialIntelligence:
		artificialIntelligence()

	if fancyAnimationSetting:
		dispExplosions()
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			raise SystemExit
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_p:
				startPauseTime = time()
				pauseTextHead = text("Paused", 50)
				log("Paused")
				pauseTextSub = text("press P to unpause", 20)
				timeText = text(str(float(int(totalTime * 100)) / 100))
				pauseMusic()
				s.fill(blackRGB)
				s.blit(pauseTextHead, 
					((sW - pauseTextHead.get_width()) / 2,
						sH / 3
						)
					)
				s.blit(pauseTextSub,
					((sW - pauseTextSub.get_width()) / 2,
						sH / 3 + pauseTextHead.get_height() + 20
						)
					)
				s.blit(timeText,
					(sW - timeText.get_width() - 20,
						sH - timeText.get_height() - 20
						)
					)
				pygame.display.flip()
				paused = True
				while paused:
					for event in pygame.event.get():
						if event.type == pygame.QUIT:
							quitGame()
						elif event.type == pygame.KEYDOWN:
							if event.key == pygame.K_p:
								paused = False
								unpauseMusic()
								log("Unpaused")
								endPauseTime = time()
								diffPT = endPauseTime - startPauseTime
								#print time() - startPlayTime
								startPlayTime += diffPT
								#print diffPT
							elif event.key == pygame.K_ESCAPE:
								raise SystemExit
	keys = pygame.key.get_pressed()
	if keys[pygame.K_ESCAPE]:
		print time() - startPlayTime

		raise SystemExit
	if keys[pygame.K_RETURN] or keys[pygame.K_SPACE] or doShoot:
		doShoot = False
		if shot == False and lastShotCounter < 1:
			log("Shot")
			if soundSetting:
				shootSound.play()
			shot = True
			shotX = shipX + 90
			shotY = int(shipY) + 20
			lastShotCounter = 30
			firstShotCounter = lastShotCounter
			log(str(shotX) + ", " + str(shotY))

	if (keys[pygame.K_DOWN] or doDown) and (shipY + wingDownOffset[1] + hull.get_height() < sH):
		shipY += shipChange
		if not wingDownDestroyed:
			doDown = False
		if wingDownDestroyed:
			shipY -= int(0.7 * shipChange)
		#print shipY
		log("Moved down")
	if (keys[pygame.K_UP] or doUp) and (shipY + wingUpOffset[1] > 0):
		shipY -= shipChange
		if not wingUpDestroyed:
			doUp = False
		if wingUpDestroyed:
			shipY += int(0.7 * shipChange)
		#print shipY
		log("Moved up")
	#s.blit(ship, (shipX + currentShipDeviation, shipY))
	wingUpCoords = (shipX + currentShipDeviation + wingUpOffset[0], shipY + wingUpOffset[1])
	wingDownCoords = (shipX + currentShipDeviation + wingDownOffset[0], shipY + wingDownOffset[1])
	s.blit(hull, (shipX + currentShipDeviation, shipY))
	if wingUpDestroyed:
		shipY += 0.4
	else:
		s.blit(wingUp, wingUpCoords)
	if wingDownDestroyed:
		shipY -= 0.4
	else:
		s.blit(wingDown, wingDownCoords)
	if shipY + wingUpOffset[1] < 0:
		shipY = (0 - wingUpOffset[1])
	elif shipY + wingDownOffset[1] + hull.get_height() > sH:
		shipY = (sH - wingDownOffset[1] - hull.get_height())
	if shot:
		#bulletRect = pygame.Rect(shotX, shotY, 10, 5)
		s.blit(bullet, (shotX, shotY))
		shotX += 10
		if shotX > sW:
			shot = False
	else:
		s.blit(bullet, (-1000, -1000))
		shotX = -1000
		shotY = -1000
		#bulletRect = defaultBulletRect
	clock.tick(frameLimit) if frameLimitSetting else clock.tick(9001)
	fps = clock.get_fps()
	fps = float(int(fps * 100)) / 100.0
	if lastShotCounter > 0 or shot: 
		lastShotCounterPercentage = (float(firstShotCounter) - float(lastShotCounter)) / float(firstShotCounter)
		maxShotRectLength = sW / 5.0
		shotCounterRect = pygame.Rect(
			(sW - maxShotRectLength) / 2,
			sH - 30,
			int(maxShotRectLength * lastShotCounterPercentage),
			5
			)
		shotCounterBarColor = (255,0,0) if shot else whiteRGB
		pygame.draw.rect(s, shotCounterBarColor, shotCounterRect)
		if lastShotCounter > 0:
			lastShotCounter -= 1
	pygame.display.update()
	
	#print maxRocks
	#print "---"
	if len(toLog) > maxLogLength:
		log("Starting new log file")
		log("Current size: " + str(len(toLog)) + " bytes")
		writeLogFile()
