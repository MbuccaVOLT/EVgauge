from matplotlib.pyplot import fill
from numpy import angle
import pygame
import pygame.gfxdraw
import math
import serial

hw_sensor = serial.Serial(port='/dev/ttyUSB0', baudrate=115200, timeout=1, write_timeout=1)
class Gauge:
    def __init__(self, screen, FONT, x_cord, y_cord, thickness, radius, start_angle, stop_angle, circle_colour, glow=True):
        self.screen = screen
        self.Font = FONT
        self.x_cord = x_cord
        self.y_cord = y_cord
        self.thickness = thickness
        self.radius = radius
        self.start_angle = start_angle
        self.stop_angle = stop_angle
        self.circle_colour = circle_colour
        self.glow = glow


    def draw(self, percent):
        # start_angle=45,
        # stop_angle=135,
        angle_path = self.stop_angle-self.start_angle
        fill_angle = int(percent*angle_path/100)
        per=percent
        if percent > 100:
            percent = 100
        if per <=40:
            per=0
        if per > 100:
            per = 100
        ac = [int(per*255/100),int(per*255/100),int(0), 255]
        for indexi in range(len(ac)):
            if ac[indexi] < 0:
                ac[indexi] = 0
            if ac[indexi] > 255:
                ac[indexi] = 255
        # print(ac)

        pertext = self.Font.render(str(percent) + " Kmh", True, ac)
        pertext_rect = pertext.get_rect(center=(int(self.x_cord), int(self.y_cord)))
        self.screen.blit(pertext, pertext_rect)

        for i in range(0, self.thickness):

            pygame.gfxdraw.arc(screen, int(self.x_cord), int(self.y_cord), self.radius - i, self.start_angle, fill_angle+ self.start_angle, self.circle_colour)
            pygame.gfxdraw.arc(screen, int(self.x_cord), int(self.y_cord), self.radius - i, self.start_angle, fill_angle + self.start_angle, ac)

        # if percent < 4:
        #     return

        if self.glow:
            for i in range(0,15):
                ac [3] = int(150 - i*10)
                pygame.gfxdraw.arc(screen, int(self.x_cord), int(self.y_cord), self.radius + i, self.start_angle,  fill_angle + self.start_angle, ac)

            for i in range(0,15):
                ac [3] = int(150 - i*10)
                pygame.gfxdraw.arc(screen, int(self.x_cord), int(self.y_cord), self.radius -self.thickness - i, self.start_angle, fill_angle + self.start_angle, ac)

            angle_r = math.radians(fill_angle- self.start_angle)
            lx,ly = int((self.radius-self.thickness/2)*math.cos(angle_r)), int( (self.radius-self.thickness/2)*math.sin(angle_r))
            ac[3] = 255
            lx = int(lx+self.x_cord)
            ly = int(ly + self.y_cord)

            pygame.draw.circle(self.screen,ac,(lx,ly),int(self.thickness/2),0)


            for i in range(0,10):
                ac [3] = int(150 - i*15)
                pygame.gfxdraw.arc(screen, int(lx), int(ly), (self.thickness//2)+i , self.start_angle, fill_angle - self.start_angle, ac)
                # pygame.gfxdraw.arc(screen, int(lx), int(ly), (self.thickness//2)+i , fill_angle  self.start_angle, fill_angle - self.start_angle, ac)
                # pygame.gfxdraw.arc(screen, int(lx), int(ly), (self.thickness//2)+i , fill_angle -225-10, fill_angle - 225-180-10, ac)

if __name__ == '__main__':
    bg_c = (56, 56, 56)
    circle_c = (55, 77, 91)
    val=''
    values=''
    pygame.init()
    width, height = (1366/2, 800/2)
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)


    pygame.display.set_caption('Wahaj Gauge Pygame')


    fps = 30
    # FONT = pygame.font.SysFont('Segoe UI', 100)
    FONT_ = pygame.font.Font("./NFS_by_JLTV.ttf", 50)

    speed = Gauge(
        screen=screen,
        FONT=FONT_,
        x_cord=width ,
        y_cord=height,
        thickness=30,
        radius=200,
        start_angle=200,
        stop_angle=340,
        circle_colour=circle_c,
        glow=False)
    acel= Gauge(
        screen=screen,
        FONT=FONT_,
        x_cord=width,
        y_cord=height,
        thickness=15,
        radius=180,
        start_angle=0,
        stop_angle=80,
        circle_colour=circle_c,
        glow=False)
    battery= Gauge(
        screen=screen,
        FONT=FONT_,
        x_cord=width ,
        y_cord=height,
        thickness=20,
        radius=200,
        start_angle=100,
        stop_angle=160,
        circle_colour=circle_c,
        glow=False)

    percentage = 0
    while True:

        while val!="\n":
            val=hw_sensor.read().decode("utf-8")
            values += val
        try:
            number=int(values.strip('\r\n'))
            number=(number*100/710)  #93
            values=''
            val=''
        except:
                pass
        screen.fill(bg_c)
        speed.draw(percent=int(number))
        acel.draw(percent=int(number))
        battery.draw(percent=int(number))
        pygame.draw.circle(screen, (255,255,255), (int(width), int(height)), 210, 12)
        pygame.draw.circle(screen, (55, 77, 91), (int(width), int(height)), 220, 12)
        pygame.display.update()
        clock.tick(fps)
