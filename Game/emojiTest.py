# Source - https://stackoverflow.com/q
# Posted by Iago Beuller, modified by community. See post 'Timeline' for change history
# Retrieved 2025-11-08, License - CC BY-SA 3.0

# -*- coding: UTF-8 -*-

import pygame

pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()
done = False
white = (255, 255, 255)
black = (0, 0, 0)
pygame.font.init()
font = pygame.font.SysFont("freesansbold", 32)
font_color = (255,255,255, 255)
font_background = (0,0,0,0)

text_string = "level 1 → level 2"
fonts = pygame.sysfont.get_fonts()
fontSearchChoice = ("emoji", "andale mono", "arial")[-1]
#TODO: MAYBE look and see if other fonts display the right-arrow emoji more aesthetically (preview different fonts with `Font Book` on Mac
if fontSearchChoice == "emoji":
    emojis = [font for font in fonts if "emoji" in font]
    print(f"emoji fonts = {emojis}")
elif fontSearchChoice == "andale mono":
    andaleOrMono = [font for font in fonts if "andale" in font.lower() or "mono" in font.lower()]
    print(f"Andale Mono fonts = {andaleOrMono}")
elif fontSearchChoice == "arial":
    arial = [font for font in fonts if "arial" in font.lower()]
    print(f"Arial fonts = {arial}")

print(f"font.size(text_string) = {font.size(text_string)}")
text = font.render(text_string, True, black, white)#, fgcolor=font_color, size=0)
image_size = list(text.get_size())
text_image = pygame.Surface(image_size)
text_image.fill(font_background)
pygame.display.flip()
text_image.blit(text, (0,0))

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            done = True

    screen.fill((0, 0, 0))
    screen.blit(text_image,
        (320 - text.get_width() // 2, 240 - text.get_height() // 2))
    pygame.display.flip()
    clock.tick(60)

