#Brendan Burke, bmb3wm, CS 1111
#if the gamebox.from_image commands don't function on the testing computers (they work on mine)
#they (and references to them) can all be deleted, and the bird can be replaced with the commented from_text bird
import random
import pygame
import gamebox
camera = gamebox.Camera(800,600)

score = 0
game_on = False
wallspeed = 3

ticker = 0
a = random.randint(0,251)
b = random.randint(0,251)
walls = [
    gamebox.from_color(800, a, "green", 50, 2*a),
    gamebox.from_color(800, 600, "green", 50, 1000-4*a),
    gamebox.from_color(1400,b,"green",50,2*b),
    gamebox.from_color(1400, 600, "green", 50, 1000-4*b),
]
#Randomly generates the first two sets of obstacles, the random determines where the opening will be
#The pillars are between 0 and 500 pixels tall, leaving a 100 pixel opening
sun = gamebox.from_image(100,40,"https://static.giantbomb.com/uploads/square_medium/12/126726/1774729-sppbanzaibill.png")
sun.scale_by(.75)
cloud1 = gamebox.from_image(random.randint(0,800),random.randint(0,600),"http://pixelartmaker.com/art/4ca4553e5b770fc.png")
cloud1.scale_by(.75)
cloud2 = gamebox.from_image(random.randint(0,800),random.randint(0,600),"http://pixelartmaker.com/art/4ca4553e5b770fc.png")
cloud2.scale_by(.5)
cloud3 = cloud1.copy_at(random.randint(0,800),random.randint(0,600))
cloud3.scale_by(.75)
ground = gamebox.from_color(400,600,"blue",1000,20)
water = gamebox.from_image(400,612,"https://i.imgur.com/9jg63i0.png")
#sun, clouds, and water, are background images, clouds randomly placed
#True to the original, the assets are blatantly taken from Mario
#ground is the deathbox for if the bird flies too low

#bird = gamebox.from_text(30, 400, "bird", 40, "purple")
bird = gamebox.from_image(25,400,"https://i.imgur.com/4gFfOMe.png")
bird.size = [50,30]
#Created the bird, sprite is taken from the original game
def tick(keys):
    """"Has all of the game actions
    Draw puts sprites/characters on the screen
    makes the bird jump when space is pushed
    makes the player lose when he or she hits a wall, the ground, or tries to fly over the walls
    adds a point whenever they pass the walls"""
    global game_on
    global score
    global wallspeed
    camera.clear("skyblue")
    camera.draw(sun)
    camera.draw(cloud2)
    camera.draw(cloud3)
    camera.draw(cloud1) #Makes the largest cloud the top layer of background
    if game_on: #moves background objects for a parallax effect
        cloud1.x -= 1
        cloud2.x -= .5
        cloud3.x -= .75
        sun.x -= .01
    if cloud1.x <= -100:
        cloud1.center = [1000, random.randint(0,600)]
    if cloud2.x <= -75:
        cloud2.center = [900, random.randint(0,600)]
    if cloud3.x <= -75:
        cloud3.center = [950, random.randint(0,600)]

    if pygame.K_SPACE in keys: #begins the game
        game_on = True


    if game_on:
        bird.speedy += 0.25 #acceleration of gravity
    if pygame.K_SPACE in keys: #lift force of flapping
        bird.speedy -= 7.5
    else: #moves the bird
        bird.move_speed()
    for wall in walls: #draws walls
        camera.draw(wall)
    to_delete = []
    if game_on: #moves walls
        for wall in walls:
            wall.x -= wallspeed
            if bird.touches(wall): #gameover if player hits the wall
                camera.draw(gamebox.from_text(400,300,"You lose, try to not lose next time",50,"red",bold=True))
                camera.draw(gamebox.from_text(400, 200, "Press ESC to exit", 50, "black", italic=True))
                gamebox.pause()
            elif wall.x < -20: #increments score when the player gets through the obstacle
                score += 0.5
                if score%5 == 0: #makes the game more difficult every 5 points
                    wallspeed += 1
                to_delete.append(wall)
            elif bird.y < 0 and wall.x < bird.x: #gameover if player tries to fly over obstacles
                camera.draw(gamebox.from_text(400,300,"Like Icarus, you flew too close to the sun",40,"orange",True))
                camera.draw(gamebox.from_text(400, 200, "Press ESC to burn up", 50, "black", italic=True))
                gamebox.pause()
        for wall in to_delete:
            if wall in walls:
                walls.remove(wall)
    if len(walls) == 2: #adds another set of obstacles once one disappears
        randnumb = random.randint(0,251)
        new_top = gamebox.from_color(1180,randnumb,"green",50,2*randnumb)
        new_bot = gamebox.from_color(1180,600,'green',50,1000-4*randnumb)
        walls.append(new_top)
        walls.append(new_bot)

    camera.draw(ground)
    camera.draw(bird)
    camera.draw(water)
    if bird.touches(ground): #gameover if player goes under the water
        camera.draw(gamebox.from_text(400,300,"You have drowned, birds cannot swim",50,"black",True))
        camera.draw(gamebox.from_text(400,200,"Press ESC to exit",50,"red",italic=True))
        gamebox.pause()
    camera.draw(gamebox.from_text(400, 50, str(int(score)), 50, "black", bold=True))
    if not game_on: #instructions to begin the game
        camera.draw(gamebox.from_text(400, 100, "BIRD GAME 2k18", 50, "white", bold=True))
        camera.draw(gamebox.from_text(400,250,"Press Space to Start",50,"purple",bold=True))
        camera.draw(gamebox.from_text(400, 300, "(Space is also jump)", 20, "red", bold=True))
        camera.draw(gamebox.from_text(400, 350, "Press ESC to Exit", 50, "black", bold=True))

    camera.display()
    keys.clear()


ticks_per_second = 60
gamebox.timer_loop(ticks_per_second, tick)