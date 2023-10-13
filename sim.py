import engine
import character
from random import randint,choice
import string

display = engine.TerminalWindow([800,320])
display.colorable = True
ticker = display.TickerText(9,4,"Hello, world!123456789123456789",10,20,30)

t = 0
while display.update():
    display.window.fill([0,0,0])

    ticker.update()

    display.fg_color = engine.pygame.Color([255,255,255])
    display.draw_string(0,0,display.clock.get_fps())

    display.draw_ticker(ticker)
    display.bg_color = engine.pygame.Color([255,0,0])
    display.fg_color = engine.pygame.Color([0,255,0])

    t += 1
    display.draw()