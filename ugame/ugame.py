import random
from microbit import *


class Entity:
    """
    `Entity` is the base class for everything that will be drawn to the screen.
    """

    def __init__(self, x_position, y_position):
        self.position = x_position, y_position

    def update_position(self, x_position, y_position):
        """
        `update_position` updates the entity's position based on the input
        coordinates.
        """
        self.position = x_position, y_position


class Obstacle(Entity):
    """
    `Obstacle` stores all information that is related to the obstacles the
    player needs to avoid during the game.
    """


class Player(Entity):
    """
    `Player` stores all information that is related to the current player.
    """

    def __init__(self, x_position, y_position, lives):
        super().__init__(x_position=x_position, y_position=y_position)
        self.lives = lives


class Game:
    """
    `Game` is a basic game framework for the BBC micro:bit, aimed for simplicity instead
    of performance.
    """

    def __init__(self):
        self.obstacle = None
        self.player = Player(x_position=0, y_position=2, lives=3)
        self.score = 0

    def update(self):
        """
        `update` is called at the end of the game's main loop to update the
        game's state.
        """
        if not self.obstacle:
            # If no obstacle is drawn to the screen, throw a coin to determine
            # if one is created.
            create = random.choice((0, 1))

            if create:
                # If a new obstacle is created, throw a dice to determine its
                # y coordinate. The x coordinate is always fixed to 4, the right
                # screen border.
                y_position = random.choice(range(5))

                self.obstacle = Obstacle(x_position=4, y_position=y_position)

    def draw(self):
        """
        `draw` is called at the beginning of the game's main loop to draw the
        game's current state to the screen.
        """
        display.show(self._compute_screen_buffer())

    def run(self):
        """
        `run` is called to start the game's main loop and hence starts the
        game itself.
        """

        while True:
            self.draw()
            self.update()

    def _compute_screen_buffer(self):
        """
        `_compute_screen_buffer` computes the current screen, based on the positions
        of `Player` and `Obstacle`.
        """
        screen_buffer = ["0" for _ in range(25)]

        # For each entity in the game, add it to the global position bytearray.
        for entity in (self.player, self.obstacle):
            if entity:
                x_pos, y_pos = entity.position

                if x_pos < 0 or x_pos > 4 or y_pos < 0 or y_pos > 4:
                    raise ValueError

                screen_buffer[x_pos + 5 * y_pos] = "9"

        screen = (
            "".join(screen_buffer[0:5])
            + ":"
            + "".join(screen_buffer[5:10])
            + ":"
            + "".join(screen_buffer[10:15])
            + ":"
            + "".join(screen_buffer[15:20])
            + ":"
            + "".join(screen_buffer[20:25])
        )

        return Image(screen)


GAME = Game()
GAME.run()
