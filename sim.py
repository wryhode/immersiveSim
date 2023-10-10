import engine
import character

display = engine.TerminalWindow([800,640])
display.colorable = True
ticker = display.TickerText(9,4,"Hello, world!123456789123456789",10,20,30)

while display.update():
    display.window.fill([0,0,0])

    ticker.update()

    display.fg_color = engine.pygame.Color([255,255,255])
    display.draw_string(0,0,display.clock.get_fps())

    display.fg_color = engine.pygame.Color([255,0,0])
    display.draw_string(4,4,"News:")
    display.draw_ticker(ticker)

    display.fg_color = engine.pygame.Color([0,0,255])
    display.draw_menu_box(3,3,25,1)

    display.fg_color = engine.pygame.Color([255,255,255])
    for y in range(display.terminal_size[1]):
        display.draw_string(display.terminal_size[0]-2,y,y)

    display.draw()