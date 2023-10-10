import engine
import character

display = engine.TerminalWindow([800,640])

ticker = display.TickerText(6,1,"Hello, world!123456789123456789",10,20,30)

while display.update():
    display.window.fill([0,0,0])

    ticker.update()

    display.draw_string(1,1,"News:")
    display.draw_ticker(ticker)

    display.draw_menu_box(0,0,25,1)


    display.draw()