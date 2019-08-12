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

camera = PiCamera()                                                                                                                                                                                            
camera.resolution = (WIDTH,HEIGHT)         

try:
    os.makedirs("resources")
except FileExistsError:
    ok = 1

sdl2.ext.init()
RESOURCES = sdl2.ext.Resources(__file__, "resources")

window = sdl2.ext.Window("Claymation", size=(WIDTH, HEIGHT))
window.show()

renderer = sdl2.ext.Renderer(window)
renderer.clear(sdl2.ext.Color(0, 0, 0))
renderer.present()

factory = sdl2.ext.SpriteFactory(renderer=renderer)
sprite = factory.create_texture_sprite(renderer,size=(WIDTH,HEIGHT))
spriterenderer = factory.create_sprite_render_system(sprite_type=sdl2.ext.sprite.TEXTURE)

textures = []
   
GPIO.setmode(GPIO.BCM)

buttons = [ 4, 17, 27, PLAY, RECORD ]
sprites = []
doit = []

def button_callback(channel):
    global doit

    if channel == RECORD:
        doit.append({"record":True})
    if channel == PLAY:
        doit.append({"play":True})

for p in buttons:
    GPIO.setup(p, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(p, GPIO.FALLING, callback=button_callback, bouncetime=600)

while True:

    if len(doit) > 0:
        x = doit.pop()
        if x != None:


            if "play" in x:
                for g in textures:
                    
                    surf = sdl2.ext.load_image(os.path.join("resources",g))
                    texture = sdl2.render.SDL_CreateTextureFromSurface(renderer.renderer,surf)
                    sprite.texture = texture
                    spriterenderer.render(sprite)
                    sdl2.render.SDL_DestroyTexture(texture)
                    sdl2.SDL_FreeSurface(surf)


            if "record" in x:

                now = datetime.now()
                fname = "%s.jpg" % now.strftime("%Y-%m-%d_%H-%M-%S")
                camera.capture(os.path.join("resources",fname),'jpeg')

                surf = sdl2.ext.load_image(os.path.join("resources",fname))
                texture = sdl2.render.SDL_CreateTextureFromSurface(renderer.renderer,surf)
                textures.append( fname )

                sprite.texture = texture
                spriterenderer.render(sprite)
                sdl2.render.SDL_DestroyTexture(texture)
                sdl2.SDL_FreeSurface(surf)

