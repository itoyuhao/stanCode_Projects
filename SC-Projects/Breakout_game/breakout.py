"""
stanCode Breakout Project
Adapted from Eric Roberts's Breakout by
Sonja Johnson-Yu, Kylie Jue, Nick Bowman,
and Jerry Liao.

Creator Name: Kevin Chen
"""

from breakoutgraphics import BreakoutGraphics
from campy.gui.events.timer import pause

FRAME_RATE = 1000 / 120  # 120 frames per second
NUM_LIVES = 3			 # Number of attempts


def main():
    graphics = BreakoutGraphics()

    lives = NUM_LIVES
    # Add animation loop here!
    if lives > 0 and graphics.mouse_switch:
        while True:
            # When there's no brick, end the game and show the final score
            if graphics.there_is_no_brick():
                graphics.window.remove(graphics.ball)
                graphics.window.remove(graphics.score_board)
                pause(1000)
                graphics.congrats()
                graphics.show_score(graphics.get_score())
                break
            # When the ball's out of the window
            if graphics.ball.y >= graphics.window.height:
                lives -= 1
                # If there's lives remained, reset the ball and turn the mouse switch on
                if lives > 0:
                    graphics.reset_ball()
                    graphics.mouse_switch = True
                # If there's no lives left, end the game and show the final score
                else:
                    graphics.remove_all()
                    graphics.window.remove(graphics.score_board)
                    pause(1000)
                    graphics.game_over()
                    graphics.show_score(graphics.get_score())
                    break
            # Update animation
            ball_vx = graphics.get_vx()
            ball_vy = graphics.get_vy()
            graphics.ball.move(ball_vx, ball_vy)
            # Check
            if graphics.ball.x <= 0 or graphics.ball.x + graphics.ball.width >= graphics.window.width:
                graphics.set_vx(-ball_vx)
            if graphics.ball.y <= 0:
                graphics.set_vy(-ball_vy)
            # When the ball hit something (except for the wall)
            if graphics.is_ball_collision() is not None:
                an_object = graphics.is_ball_collision()
                # If the ball hits the paddle
                if an_object is graphics.paddle:
                    # To avoid from stuck in the paddle (set the ball on the paddle)
                    if graphics.ball.y + graphics.ball.height >= an_object.y:
                        graphics.ball.y = graphics.paddle.y - graphics.ball.height

                    # Bouncing up
                    graphics.set_vy(-ball_vy)

                    # vx changes with the position ball hit the paddle
                    if graphics.ball.x + graphics.ball.width/2 < graphics.paddle.x + graphics.paddle.width/4:
                        graphics.set_vx(ball_vx-2)
                    if graphics.paddle.x + graphics.paddle.width/4 <= graphics.ball.x + graphics.ball.width/2 \
                            < graphics.paddle.x + graphics.paddle.width/2:
                        graphics.set_vx(ball_vx-1)
                    if graphics.paddle.x + graphics.paddle.width/2 <= graphics.ball.x + graphics.ball.width/2 \
                            < graphics.paddle.x + graphics.paddle.width*3/4:
                        graphics.set_vx(ball_vx+1)
                    if graphics.paddle.x + graphics.paddle.width*3/4 <= graphics.ball.x + graphics.ball.width/2:
                        graphics.set_vx(ball_vx+2)

                else:
                    # When the ball hits the bricks
                    if an_object is not graphics.score_board:
                        # Changing color of the ball
                        graphics.ball.color = an_object.fill_color
                        graphics.ball.fill_color = an_object.fill_color

                        # Bounce
                        graphics.set_vy(-ball_vy)
                        # Remove the bricks
                        graphics.window.remove(an_object)
                        # Get 100 scores (updating the score board)
                        graphics.set_score(100)
                        graphics.score_board_update(graphics.get_score())
                    # When the ball hits the 'score board' (try it, haha)
                    else:
                        # Bounce
                        graphics.set_vy(-ball_vy*1.5)
                        # Double scores and speed up (updating the score board)
                        graphics.set_score(graphics.get_score())
                        graphics.score_board_update(graphics.get_score())

            # Pause
            pause(FRAME_RATE)


if __name__ == '__main__':
    main()
