#!/usr/bin/env python2

import pygame as pg
import pygame.gfxdraw as gfxdraw
import numpy

from random import randint, random
from math import sin, cos, pi
from sys import exit

import cStringIO
import base64

firefly_image_string = """
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
/fUPyJa4Z4dsi2cAAAAASUVORK5CYII="""
firefly_image = base64.decodestring(firefly_image_string)
firefly_image = cStringIO.StringIO(firefly_image)
firefly_image = pg.image.load(firefly_image)
 
SHOWING = 'showing'
FLYING = 'flying'

def blend_alpha(surface, factor):
    source = pg.surfarray.pixels_alpha(surface)
    source_float = source.astype(float)
    source_float *= factor
    result = source_float.astype('uint8')
    numpy.copyto(source, result)
    del source
    del source_float

def interrect(rect1, rect2):
    if not rect1.colliderect(rect2):
        return pg.Rect(0, 0, 0, 0)
    left = rect2.left if rect2.left > rect1.left else rect1.left
    top = rect2.top if rect2.top > rect1.top else rect1.top
    right = rect2.right if rect2.right < rect1.right else rect1.right
    bottom = rect2.bottom if rect2.bottom < rect1.bottom else rect1.bottom

    size = right - left, bottom - top
    result = pg.Rect((left, top), size)
    return result

class Firefly(pg.sprite.Sprite):
    def __init__(self, initpos):
        pg.sprite.Sprite.__init__(self)
        self.radiu = randint(10, 50)
        self.color = pg.Color(0, 255, 0)
        speed = float(self.radiu - 9)/15

        self.image_static = pg.transform.scale(firefly_image, (self.radiu*2+1, self.radiu*2+1))
        self.image = self.image_static.copy()
        self.rect = self.image.get_rect()
        self.x, self.y = self.rect.center = initpos

        self.speed = speed*cos(random()*2*pi), speed*sin(random()*2*pi)

        self.state = SHOWING
        self.timer = 0
        
    def update(self, time):
        if self.timer > 2000:
            self.state = FLYING

        if self.state is SHOWING:
            self.image = self.image_static.copy()
            blend_alpha(self.image, self.timer/2000.0)

        self.x += self.speed[0]*time/15
        self.y += self.speed[1]*time/15
        self.rect.center = map(int, (self.x, self.y))

        self.timer += time

def main():
    pg.init()

    bgcolor = (0, 0, 0)

    info = pg.display.Info()
    winsize = width, height = info.current_w, info.current_h
    screen = pg.display.set_mode((winsize), pg.FULLSCREEN|pg.HWSURFACE)

    pg.display.set_caption('Firefly')
    globals()['firefly_image'] = firefly_image.convert_alpha()
    pg.display.set_icon(firefly_image)
    
    try:
        bgimg_raw = pg.image.load("background.jpg")
        bgimg = pg.transform.scale(bgimg_raw, winsize)
        bgimg_back = bgimg.copy()
        del bgimg_raw
    except pg.error:
        bgimg = None

    if bgimg:
        screen.blit(bgimg, (0, 0))
    else:
        screen.fill(bgcolor)
    pg.display.flip()

    group = pg.sprite.OrderedUpdates()
    clock = pg.time.Clock()
    timer = 0

    font = pg.sysfont.SysFont('monospace', 20)
    font_rect = pg.Rect((0, 0), font.size('fps: 00.00'))
    showfps = False
    fontclear = False
    def on_screen(sprite):
        return screen.get_rect().colliderect(sprite.rect)
    if bgimg:
        def clear_callback(surf, rect):
            redraw_rect = interrect(surf.get_rect(), rect)
            redraw_img = bgimg.subsurface(redraw_rect)
            surf.blit(redraw_img, redraw_rect)
    else:
        def clear_callback(surf, rect):
            pg.draw.rect(surf, bgcolor, rect)

    while 1:
        time_passed = clock.tick(60)
        for event in pg.event.get():
            if event.type is pg.QUIT:
                exit()
            if event.type is pg.KEYDOWN:
                if event.key is pg.K_ESCAPE:
                    exit()
                elif event.key is pg.K_s:
                    showfps = not showfps
                    fps_update = True

        if timer > 300:
            initpos = randint(0, width), randint(0, height)
            group.add(Firefly(initpos))
            timer = 0
        else:
            timer += time_passed
        group.clear(screen, clear_callback)
        group.update(time_passed)

        for firefly in group.sprites():
            if not on_screen(firefly):
                firefly.kill()
        updates = group.draw(screen)
        if showfps:
            clear_callback(screen, font_rect)
            fontsurf = font.render('fps: {:.2f}'.format(clock.get_fps()), True, (255, 255, 255))
            screen.blit(fontsurf, fontsurf.get_rect())
            del fontsurf
            updates.append(font_rect)
            fontclear = True
        elif fontclear:
            fontclear = False
            clear_callback(screen, font_rect)
            updates.append(font_rect)
        pg.display.update(updates)

if __name__ == '__main__':
    main()
