#!/usr/bin/python3

import os
from datetime import datetime
from picamera import PiCamera
import RPi.GPIO as GPIO
import time
import sys
import sdl2
import sdl2.ext
import time
import glob

# Display size
WIDTH = 1280
HEIGHT = 720

# Button numbers
RECORD = 5
PLAY = 22

sdl2.ext.init()
RESOURCES = sdl2.ext.Resources(__file__, "resources")

window = sdl2.ext.Window("Claymation", size=(WIDTH, HEIGHT))
window.show()

renderer = sdl2.ext.Renderer(window)
factory = sdl2.ext.SpriteFactory(renderer=renderer)
sprite = factory.create_texture_sprite(renderer,size=(WIDTH,HEIGHT))
spriterenderer = factory.create_sprite_render_system(sprite_type=sdl2.ext.sprite.TEXTURE)

textures = []
   
camera = PiCamera()
camera.resolution = (1280,720)
GPIO.setmode(GPIO.BCM)

buttons = [ 4, 17, 27, PLAY, RECORD ]
sprites = []
doit = []

def button_callback(channel):
    global doit

    if channel == RECORD:
        now = datetime.now()
        fname = "%s.jpg" % now.strftime("%Y-%m-%d_%H-%M-%S")
        camera.capture(os.path.join("resources",fname),'jpeg')
        doit.append({"img":fname})

    if channel == PLAY:
        doit.append({"play":True})

for p in buttons:
    GPIO.setup(p, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(p, GPIO.FALLING, callback=button_callback, bouncetime=600)

while True:

    if len(doit) > 0:
        x = doit.pop()
        if x != None:

            if "img" in x:
                textures.append( sdl2.render.SDL_CreateTextureFromSurface(renderer.renderer,sdl2.ext.load_image(os.path.join("resources",x["img"]))))
                sprite.texture = textures[len(textures)-1]
                spriterenderer.render(sprite)

            if "play" in x:
                for g in textures:
                    sprite.texture = g
                    spriterenderer.render(sprite)
                    time.sleep(0.04)


