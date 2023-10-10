import pygame
from json import loads
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
            self.auto_scroll = True

        def update(self):
            self.tick_counter += 1
            if self.tick_counter >= self.tick_delay:
                if self.auto_scroll and len(self.string) > self.clip_size:
                    self.scroll += 1
                self.tick_counter = 0
                if self.scroll > len(self.string):
                    self.scroll = 0
                    self.tick_counter = -self.reset_rest # Give rest time when scroll wraps

    def __init__(self,resolution):
        self.resolution = resolution
        self.tileset_settings_file = open("./tileset.json")
        self.tileset_settings = loads(self.tileset_settings_file.read())
        self.tileset_settings_file.close()
        self.terminal_size = self.tileset_settings["terminal_size"]
        self.tileset_scaling = self.tileset_settings["scaling"]
        self.tile_size = [self.tileset_settings["tile_size"][0]*self.tileset_scaling[0],self.tileset_settings["tile_size"][1]*self.tileset_scaling[1]]
        self.tileset_width = self.tileset_settings["tileset_size"][0]
        self.tileset_height = self.tileset_settings["tileset_size"][1]
        self.colorable = self.tileset_settings["colorable"] # This will usually be on when using text graphics
        self.fg_color = pygame.Color([255,255,255])
        self.bg_color = pygame.Color([0,0,0])
        self.prev_fg_color = self.fg_color
        self.prev_bg_color = self.bg_color
        self.tileset = pygame.image.load("./tileset.png")
        self.tileset = pygame.transform.scale_by(self.tileset,self.tileset_scaling)
        if self.colorable:
            self.tileset.set_colorkey([0,0,0])
            self.colored_tileset = self.tileset.copy()
        self.char_step = (self.resolution[0] / self.terminal_size[0]) * self.tileset_scaling[0], (self.resolution[1] / self.terminal_size[1]) * self.tileset_scaling[0]
        self.window = pygame.display.set_mode(self.resolution)
        self.clock = pygame.time.Clock()

    def draw_character(self,x,y,c):
        ci = char_to_cp437(c)
        cx = (ci % self.tileset_width) * self.tile_size[0]
        cy = int(ci / self.tileset_width) * self.tile_size[1]
        if self.colorable and self.fg_color != self.prev_fg_color or self.bg_color != self.prev_bg_color:
            self.colored_tileset = self.tileset.copy()
            self.colored_tileset.fill(self.bg_color,special_flags=pygame.BLEND_RGBA_MAX)
            self.colored_tileset.fill(self.fg_color,special_flags=pygame.BLEND_RGBA_MIN)
            self.prev_bg_color = self.bg_color
            self.prev_fg_color = self.fg_color
        self.window.blit(self.colored_tileset,[x*self.char_step[0],y*self.char_step[1]],[cx,cy,self.tile_size[0],self.tile_size[1]])

    def draw_string(self,x,y,stri):
        stri = str(stri)
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