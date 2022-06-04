import pygame
import numpy as np

WIN_WIDTH, WIN_HEIGHT = 1200, 800
WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Yavalath")

FPS = 30

class Hexagon:
    hexSprite = pygame.image.load('hex.png')
    p1sprite = pygame.image.load('p1.png')
    p2sprite = pygame.image.load('p2.png')
    inradius = hexSprite.get_width() // 2
    circumradius = hexSprite.get_height() // 2

    def __init__(self, r, q):
        self.r = r
        self.q = q

        self.xpos = WIN_WIDTH / 2 + self.circumradius * (np.sqrt(3) * self.q + np.sqrt(3)/2 * self.r)
        self.ypos = WIN_HEIGHT / 2 + self.circumradius * 3/2 * self.r

        self.player = 2

    def draw(self):
        # Draw from the center
        coords = (self.xpos - self.inradius, self.ypos - self.circumradius)
        WIN.blit(self.hexSprite, coords)

        if self.player == 1:
            WIN.blit(self.p1sprite, coords)
        elif self.player == 0:
            WIN.blit(self.p2sprite, coords)

def getCurrentlySelectedHex(x, y):
    x -= WIN_WIDTH / 2
    y -= WIN_HEIGHT / 2
    fracq = (np.sqrt(3)/3 * x - 1/3 * y) / Hexagon.circumradius
    fracr = (2/3 * y) / Hexagon.circumradius
    fracs = -fracq - fracr

    q,r,s = np.round((fracq,fracr,fracs))

    dq = abs(q - fracq)
    dr = abs(r - fracr)
    ds = abs(s - fracs)

    if dq > dr and dq > ds:
        q = -r-s
    elif dr > ds:
        r = -q-s
    else:
        s = -q-r

    if abs(q) > 4 or abs(r) > 4 or (q + r <= -5) or (q + r >= 5):
        q = None
        r = None
    else:
        q = int(q)
        r = int(r)

    return (q,r)

def checkGameEnd(coords, turn):
    if turn < 5:
        return 0

    # TODO Add line checker


def draw_window(map):
    WIN.fill((0,0,0))
    for subarr in map:
        for hex in subarr:
            if type(hex) is Hexagon:
                hex.draw()
    pygame.display.flip()

def main():
    run = True
    clock = pygame.time.Clock()

    # Create a 2D array in the form:
    #     # # # # . . . . .
    #     # # # . . . . . .
    #     # # . . . . . . .
    #     # . . . . . . . .
    #     . . . . . . . . .
    #     . . . . . . . . #
    #     . . . . . . . # #
    #     . . . . . . # # #
    #     . . . . . # # # #
    # Where # is None, and . corresponds to a hexagon in the grid.
    # - A row in the array corresponds to a diagonal in the hex grid.
    # - A diagonal in the array corresponds to a row in the hex grid.

    axialMap = np.zeros((9,9), dtype=object)
    for r in range(9):
        for q in range(9):
            if 4 <= r + q <= 12:
                # Offset by -4 to ensure that the center of the hex grid is (0,0)
                axialMap[r, q] = Hexagon(r - 4, q - 4)
            else:
                axialMap[r, q] = None

    turn = 1

    # Game loop
    while run:
        clock.tick(FPS)
        # Get mouse position and the coords of the currently selected hex.
        mousex, mousey = pygame.mouse.get_pos()


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                curq, curr = getCurrentlySelectedHex(mousex, mousey)
                if (curq, curr) != (None, None) and axialMap[curr + 4, curq + 4].player == 2:
                        # Turn odd: p1, even: p2
                        axialMap[curr + 4, curq + 4].player = turn & 1
                        print("Turn:", turn)
                        turn += 1

                        # TODO Check for lines here

        draw_window(axialMap)

    pygame.quit()


if __name__ == "__main__":
    main()
