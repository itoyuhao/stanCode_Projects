"""
stanCode Breakout Project
Adapted from Eric Roberts's Breakout by
Sonja Johnson-Yu, Kylie Jue, Nick Bowman,
and Jerry Liao

Name: Kevin Chen
"""
from campy.graphics.gwindow import GWindow
from campy.graphics.gobjects import GOval, GRect, GLabel
from campy.gui.events.mouse import onmouseclicked, onmousemoved
from campy.gui.events.timer import pause
import random

BRICK_SPACING = 5  # Space between bricks (in pixels). This space is used for horizontal and vertical spacing.
BRICK_WIDTH = 40  # Height of a brick (in pixels).
BRICK_HEIGHT = 15  # Height of a brick (in pixels).
BRICK_ROWS = 10  # Number of rows of bricks.
BRICK_COLS = 10  # Number of columns of bricks.
BRICK_OFFSET = 50  # Vertical offset of the topmost brick from the window top (in pixels).
BALL_RADIUS = 10  # Radius of the ball (in pixels).
PADDLE_WIDTH = 75  # Width of the paddle (in pixels).
PADDLE_HEIGHT = 15  # Height of the paddle (in pixels).
PADDLE_OFFSET = 50  # Vertical offset of the paddle from the window bottom (in pixels).

INITIAL_Y_SPEED = 7  # Initial vertical speed for the ball.
MAX_X_SPEED = 5  # Maximum initial horizontal speed for the ball.


class BreakoutGraphics:
    # Constructor
    def __init__(self, ball_radius=BALL_RADIUS, paddle_width=PADDLE_WIDTH,
                 paddle_height=PADDLE_HEIGHT, paddle_offset=PADDLE_OFFSET,
                 brick_rows=BRICK_ROWS, brick_cols=BRICK_COLS,
                 brick_width=BRICK_WIDTH, brick_height=BRICK_HEIGHT,
                 brick_offset=BRICK_OFFSET, brick_spacing=BRICK_SPACING,
                 title='Breakout'):

        # Create a graphical window, with some extra space
        window_width = brick_cols * (brick_width + brick_spacing) - brick_spacing
        window_height = brick_offset + 3 * (brick_rows * (brick_height + brick_spacing) - brick_spacing)
        self.window = GWindow(width=window_width, height=window_height, title=title)

        # Play pilot animation
        self.pilot()

        # After the pilot, start the game
        # Create a paddle
        self.paddle_offset = paddle_offset
        self.paddle = GRect(paddle_width, paddle_height)
        self.paddle.filled = True
        self.paddle.fill_color = 'black'
        self.paddle.color = 'black'
        self.window.add(self.paddle, x=(self.window.width - self.paddle.width) / 2,
                        y=(self.window.height - paddle_offset))

        # Draw bricks
        self.brick_width = brick_width
        self.brick_height = brick_height
        self.brick_offset = brick_offset
        self.brick_spacing = brick_spacing
        self.brick_rows = brick_rows
        self.brick_cols = brick_cols
        for i in range(self.brick_rows):
            for j in range(self.brick_cols):
                self.brick = GRect(brick_width, brick_height)
                self.brick.filled = True
                if i // 2 == 0:
                    self.brick.fill_color = 'salmon'
                    self.brick.color = 'salmon'
                elif i // 2 == 1:
                    self.brick.fill_color = 'gold'
                    self.brick.color = 'gold'
                elif i // 2 == 2:
                    self.brick.fill_color = 'lightskyblue'
                    self.brick.color = 'lightskyblue'
                elif i // 2 == 3:
                    self.brick.fill_color = 'cornflowerblue'
                    self.brick.color = 'cornflowerblue'
                else:
                    self.brick.fill_color = 'royalblue'
                    self.brick.color = 'royalblue'
                self.window.add(self.brick, x=(j * (brick_width + brick_spacing)),
                                y=(brick_offset + i * (brick_height + brick_spacing)))

        # Center a filled ball in the graphical window
        self.radius = ball_radius
        self.ball = GOval(self.radius * 2, self.radius * 2)
        self.ball.filled = True
        self.ball.fill_color = 'black'
        self.ball.color = 'black'
        self.window.add(self.ball, x=(self.window.width - self.ball.width) / 2,
                        y=(self.window.height - self.ball.height) / 2)

        # Default initial velocity for the ball
        self.__dx = 0
        self.__dy = 0

        # Initialize our mouse listeners
        onmouseclicked(self.starter)
        onmousemoved(self.paddle_control)
        self.mouse_switch = True

        # Show the score board
        self.__score = 0
        self.score_board = GLabel('Score: ' + str(self.__score))
        self.score_board.font = 'Courier-10'
        self.window.add(self.score_board, 0, 20)

    # Methods in this class
    # Paddle controller
    def paddle_control(self, m):
        self.paddle.x = m.x - self.paddle.width / 2
        if self.paddle.x <= 0:
            self.paddle.x = 0
        elif self.paddle.x + self.paddle.width >= self.window.width:
            self.paddle.x = self.window.width - self.paddle.width

    # Reset the ball to the initial position
    def reset_ball(self):
        self.__dx = 0
        self.__dy = 0
        self.ball.fill_color = 'black'
        self.ball.color = 'black'
        self.window.add(self.ball, x=(self.window.width - self.ball.width) / 2,
                        y=(self.window.height - self.ball.height) / 2)
        self.mouse_switch = True

    # Give the ball initial speed to start
    def set_initial_velocity(self):
        self.__dx = random.randint(1, MAX_X_SPEED)
        self.__dy = INITIAL_Y_SPEED
        if random.random() > 0.5:
            self.__dx *= -1

    # V(x) getter
    def get_vx(self):
        return self.__dx

    # V(y) getter
    def get_vy(self):
        return self.__dy

    # V(x) setter
    def set_vx(self, new_vx):
        self.__dx = new_vx

    # V(y) setter
    def set_vy(self, new_vy):
        self.__dy = new_vy

    # Score getter
    def get_score(self):
        return self.__score

    # Score setter
    def set_score(self, add_score):
        self.__score += add_score

    # Function for starting the game (used for onmouseclicked)
    def starter(self, m):
        if self.mouse_switch is True:
            self.set_initial_velocity()
            self.mouse_switch = False

    # Method for detect if the ball hit something
    def is_ball_collision(self):
        for i in range(2):
            for j in range(2):
                ball_x = self.ball.x + 2 * i * self.radius
                ball_y = self.ball.y + 2 * j * self.radius
                maybe_object = self.window.get_object_at(ball_x, ball_y)
                if maybe_object is not None:
                    return maybe_object

    # Method for detect if there's remained bricks
    def there_is_no_brick(self):
        for i in range(BRICK_ROWS):
            for j in range(BRICK_COLS):
                maybe_brick = self.window.get_object_at(x=(j * (self.brick_width + self.brick_spacing)),
                                                        y=(self.brick_offset + i * (self.brick_height +
                                                                                    self.brick_spacing)))
                if maybe_brick is not None:
                    return False
        return True

    # Method for remove all the object on the window
    def remove_all(self):
        for i in range(self.brick_rows):
            for j in range(self.brick_cols):
                maybe_object = self.window.get_object_at(x=(j * (self.brick_width + self.brick_spacing)),
                                                         y=(self.brick_offset + i * (self.brick_height
                                                                                     + self.brick_spacing)))
                if maybe_object is not None:
                    self.window.remove(maybe_object)
        self.window.remove(self.paddle)

    # Method for game over (no lives left)
    def game_over(self):
        game_over = GLabel('Game Over')
        game_over.color = 'tomato'
        game_over.font = 'Courier-30-bold'
        self.window.add(game_over, x=(self.window.width - game_over.width) / 2, y=self.window.height / 2)

    # Method for settlement
    def congrats(self):
        label_win = GLabel('Congratulations!')
        label_win.color = 'navy'
        label_win.font = 'Courier-30-bold'
        self.window.add(label_win, x=(self.window.width - label_win.width) / 2, y=self.window.height / 2)

    # Method for final score display
    def show_score(self, score):
        score_label = GLabel('Your Final Score: ' + str(score))
        score_label.font = 'Courier-15'
        self.window.add(score_label, x=(self.window.width - score_label.width) / 2, y=self.window.height / 2 + 60)

    # Method for updating the score during the game
    def score_board_update(self, score):
        self.score_board.text = 'Score: ' + str(score)

    # Method for the pilot animation
    def pilot(self):
        # Instructions
        line_1 = GLabel('Welcome to my Breakout Game!')
        line_1.font = 'Courier-12-bold'
        line_2 = GLabel('Your mission is to get the highest score.')
        line_2.font = 'Courier-12-bold'
        line_3 = GLabel('No matter how you get it >.^')
        line_3.font = 'Courier-12-bold'
        self.window.add(line_1, x=(self.window.width - line_1.width) / 2, y=self.window.height - 40)
        self.window.add(line_2, x=(self.window.width - line_2.width) / 2, y=self.window.height - 20)
        self.window.add(line_3, x=(self.window.width - line_3.width) / 2, y=self.window.height)
        # Animation
        while True:
            # Update
            line_1.move(0, -5)
            line_2.move(0, -5)
            line_3.move(0, -5)
            # Check
            if line_1.y <= self.window.height / 2:
                break
            # Pause
            pause(100)
        pause(1000)
        self.window.remove(line_1)
        self.window.remove(line_2)
        self.window.remove(line_3)
        pause(1000)
