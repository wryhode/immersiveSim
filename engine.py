import pygame
from pygame.locals import *
pygame.init()

def char_to_cp437(char):
    try:
        char = str(char)
        i = ord(char.encode('cp437', errors='replace'))
    except UnicodeEncodeError:
        print(f"{char} cannot be converted. Please replace it")
        return 0
    
    return i

class TerminalWindow():
    class TickerText():
        def __init__(self,x,y,string,tick_delay,clip_size,reset_rest):
            self.x = x
            self.scroll = 0
            self.y = y
            self.string = string
            self.tick_delay = tick_delay
            self.reset_rest = reset_rest
            self.tick_counter = -reset_rest
            self.clip_size = clip_size

        def update(self):
            self.tick_counter += 1
            if self.tick_counter >= self.tick_delay:
                if len(self.string) > self.clip_size:
                    self.scroll += 1
                self.tick_counter = 0
                if self.scroll > len(self.string):
                    self.scroll = 0
                    self.tick_counter = -self.reset_rest

    def __init__(self,resolution):
        self.tileset = pygame.image.load("./tileset.png")
        self.resolution = resolution
        self.terminal_size = [80,24]
        self.tile_size = [9,17]
        self.tileset_width = 16
        self.tileset_height = 16
        self.char_step = self.resolution[0] / self.terminal_size[0], self.resolution[1] / self.terminal_size[1]
        self.window = pygame.display.set_mode(self.resolution)
        self.clock = pygame.time.Clock()

    def draw_character(self,x,y,c):
        ci = char_to_cp437(c)
        cx = (ci % self.tileset_width) * self.tile_size[0]
        cy = int(ci / self.tileset_width) * self.tile_size[1]
        self.window.blit(self.tileset,[x*self.char_step[0],y*self.char_step[1]],[cx,cy,self.tile_size[0],self.tile_size[1]])

    def draw_string(self,x,y,stri):
        for i,c in enumerate(stri):
            self.draw_character(x+i,y,c)

    def draw_string_vertical(self,x,y,stri):
        for i,c in enumerate(stri):
            self.draw_character(x,y+i,c)

    def draw_string_clipped(self,x,y,stri,clip_size):
        for i,c in enumerate(stri):
            if i > clip_size:
                return
            self.draw_character(x+i,y,c)

    def draw_ticker(self,ticker):
        self.draw_string_clipped(ticker.x,ticker.y,ticker.string[ticker.scroll:len(ticker.string)],ticker.clip_size)

    def draw_menu_box(self,x,y,w,h):
        string_horiz = "═"*w
        string_vertical = "║"*(h+1)
        
        self.draw_string(x+1,y,string_horiz)
        self.draw_string(x+1,y+h+1,string_horiz)
        self.draw_string_vertical(x,y,string_vertical)
        self.draw_string_vertical(x+w+1,y,string_vertical)
        self.draw_character(x,y,"╔")
        self.draw_character(x+w+1,y,"╗")
        self.draw_character(x,y+h+1,"╚")
        self.draw_character(x+w+1,y+h+1,"╝")

    def update(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return False
        
        return True

    def draw(self):
        pygame.display.update()
        self.clock.tick(60)