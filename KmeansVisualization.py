import pygame
from random import randint
import math
from sklearn.cluster import KMeans

def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0]) * (p1[0] - p2[0]) + (p1[1] - p2[1]) * (p1[1] - p2[1]))

pygame.init() # init all operation of pygame

screen = pygame.display.set_mode((1200, 700)) # weidth and height of screen

icon = pygame.image.load('kmeans.png') # path of image 

pygame.display.set_icon(icon) # set icon for program

pygame.display.set_caption("Kmeans Algorithm Visualization") # set caption for program

running = True

clock = pygame.time.Clock() # create FPS

White = (255, 255, 255)
colorOfBackground = (210, 184, 180)
Black = (0, 0, 0)
BackgroundPanel = (249, 255, 230)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (147, 153, 35)
PURPLE = (255, 0, 255)
SKY = (0, 255, 255)
ORANGE = (255, 125, 25)
GRAPE = (100, 25, 125)
GRASS = (55, 155, 65)

COLORS = [RED, GREEN, BLUE, YELLOW, PURPLE, SKY, ORANGE, GRAPE, GRASS] 

font = pygame.font.SysFont('Fira Code', 40)
fontSmall = pygame.font.SysFont('Fira Code', 20)
textPlus = font.render('+', True, White)
textMinus = font.render('-', True, White)
textRun = font.render("Run", True, White)
textAlgorithm = font.render("Algorithm", True, White)
textReset = font.render("Reset", True, White)
textRandom = font.render("Random", True, White)
K = 0
error = 0
points = []
clusters = []
labels = []
while running:
    clock.tick(60) # set FPS = 60
    screen.fill(colorOfBackground) # set color background
    mouseX, mouseY = pygame.mouse.get_pos()
    # Draw interface
    # Draw panel
    
    pygame.draw.rect(screen, Black, (50, 50, 700, 500))
    pygame.draw.rect(screen, BackgroundPanel, (55, 55, 690, 490))

    # K button plus (+)
    pygame.draw.rect(screen, Black, (850, 50, 50, 50))
    screen.blit(textPlus, (860, 47))

    # K button minus (-)
    pygame.draw.rect(screen, Black, (950, 50, 50, 50))
    screen.blit(textMinus, (960, 47))

    # K value
    textK = font.render("K = " + str(K), True, Black)
    screen.blit(textK, (1050, 50))

    # run button
    pygame.draw.rect(screen, Black, (850,150,150,50)) 
    screen.blit(textRun, (890, 147))

    # algorithm button
    pygame.draw.rect(screen, Black, (850, 450, 240, 50))
    screen.blit(textAlgorithm, (850, 450))
    
    # Random button 
    pygame.draw.rect(screen, Black, (850, 350, 150, 50))
    screen.blit(textRandom, (850, 350))

    # Reset button
    pygame.draw.rect(screen, Black, (850, 550, 150, 50))
    screen.blit(textReset, (850, 550))

    # Draw mouse position when mouse is in panel
    if 50 < mouseX < 750 and 50 < mouseY < 550:
        textMouse = fontSmall.render("(" + str(mouseX - 50) + "," + str(mouseY - 50) + ")", True, Black)
        screen.blit(textMouse, (mouseX + 10, mouseY))
    # End interface
    # exit program
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            # create point on panel
            if 50 < mouseX < 750 and 50 < mouseY < 550:
                labels = []
                point = [mouseX - 50, mouseY - 50]
                points.append(point)
            # Change K button (+)
            if 850 < mouseX < 900 and 50 < mouseY < 100:
                if K < 8:
                    K = K + 1
                print("press +")

            if 950 < mouseX < 1000 and 50 < mouseY < 100:
                K = K - 1
                print("press -")

            if 850 < mouseX < 1000 and 150 < mouseY < 200:
                labels = []
                if clusters == []:
                    continue
                # assign points to closest clusters
                for p in points:
                    distanceToCluster = []
                    for c in clusters:
                        dis = distance(p, c)
                        distanceToCluster.append(dis)
                    if distanceToCluster != []:
                        minDistance = min(distanceToCluster)
                        label = distanceToCluster.index(minDistance)
                        labels.append(label)
                # Update clusters
                for i in range(K):
                    sumX = 0
                    sumY = 0
                    count = 0
                    for j in range(len(points)):
                        if labels[j] == i:
                            sumX += points[j][0]
                            sumY += points[j][1]
                            count += 1
                    if count != 0:
                        newClusterX = sumX / count
                        newClusterY = sumY / count
                        clusters[i] = [newClusterX, newClusterY]
                print("run button pressed")

            if 850 < mouseX < 1000 and 450 < mouseY < 550:
                try:
                    kmeans = KMeans(n_clusters=K).fit(points)
                    labels = kmeans.predict(points)
                    clusters = kmeans.cluster_centers_
                except:
                    print("error")
                print("Algorithm button pressed")

            if 850 < mouseX < 1000 and 350 < mouseY < 400:
                clusters = []
                labels = []
                for i in range(K):
                    randomPoint = [randint(0, 700), randint(0, 500)]
                    clusters.append(randomPoint)
                print("Random button pressed")

            if 850 < mouseX < 1000 and 550 < mouseY < 600:
                labels = []
                points = []
                clusters = []
                error = 0
                K = 0
                print("Reset button pressed")
    # Draw cluster
    for i in range(len(clusters)):
        pygame.draw.circle(screen, COLORS[i], (int(clusters[i][0]) + 50, int(clusters[i][1]) + 50), 10)
    # Draw point
    for i in range(len(points)):
        pygame.draw.circle(screen, Black, (points[i][0] + 50, points[i][1] + 50), 6)
        if len(labels) == 0:
            pygame.draw.circle(screen, White, (points[i][0] + 50, points[i][1] + 50), 5)
        else:
            pygame.draw.circle(screen, COLORS[labels[i]], (points[i][0] + 50, points[i][1] + 50), 5)
    # Caculate and draw error
    error = 0
    if len(clusters) > 0 and len(labels) > 0:
        for i in range(len(points)):
            error += distance(points[i], clusters[labels[i]])
    textError = font.render("Error = " + str(int(error)), True, Black)
    screen.blit(textError, (850, 250))
    pygame.display.flip()

pygame.quit()
