import pygame 
import pandas as pd
import sys
    
def main(player1_name, player2_name,bg):
    pygame.init()
    WIDTH, HEIGHT = 700, 500
    screen = pygame.display.set_mode()
    WIDTH, HEIGHT = screen.get_size()
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pong")

    bgr = pygame.image.load("static/bg"+bg+".jpg")

    # using this your ball speed will remain constant irrespective of computer
    FPS = 60

    # variables
    White = (255, 255, 255)
    Black = (0, 0, 0)
    paddle_width, paddle_height = 20, 120
    Ball_radius = 10
    Score_font = pygame.font.SysFont("comicsans", 30)
    Score_font1 = pygame.font.SysFont("comicsans", 50)
    Winning_score = 5
    score1 = 0
    score2 = 0

    # class for paddles
    class Paddle:
        COLOR = White
        Velocity = 8

        def __init__(self, x, y, width, height):
            self.x = self.original_x = x
            self.y = self.original_y = y
            self.width = width
            self.height = height

        def draw(self, win):
            pygame.draw.rect(
                win, self.COLOR, (self.x, self.y, self.width, self.height))

        def move(self, up=True):
            if up:
                self.y -= self.Velocity
            else:
                self.y += self.Velocity

        def reset(self):
            self.x = self.original_x
            self.y = self.original_y

        # class for ball


    class Ball:
        MAX_VEL = 10
        Color = White

        def __init__(self, x, y, radius):
            self.x = self.original_x = x
            self.y = self.original_y = y
            self.radius = radius
            self.x_Velocity = self.MAX_VEL
            self.y_Velocity = 0

        def draw(self, win):
            pygame.draw.circle(win, self.Color, (self.x, self.y), self.radius)

        def move(self):
            self.x += self.x_Velocity
            self.y += self.y_Velocity

        def reset(self):
            self.x = self.original_x
            self.y = self.original_y
            self.y_Velocity = 0
            self.x_Velocity *= -1

    # Draw function


    def draw(win, paddles, ball, player1, player2):
        win.blit(bgr, (0, 0))
        player1_text = Score_font.render(f"{player1_name} : {player1}", 1, White)
        player2_text = Score_font.render(f"{player2_name} : {player2}", 1, White)
        win.blit(player1_text, (WIDTH//4 - player1_text.get_width()//2, 20))
        win.blit(player2_text, (WIDTH*(3/4) - player2_text.get_width() // 2, 20))

        for paddle in paddles:
            paddle.draw(win)
        ball.draw(win)
        pygame.display.update()


    def handle_collision(ball, left_paddle, right_paddle):
        s1 = pygame.mixer.Sound('static/s1.wav')
        if ball.y + ball.radius >= HEIGHT:
            s1.play()
            ball.y_Velocity *= -1
        elif ball.y - ball.radius <= 0:
            s1.play()
            ball.y_Velocity *= -1

        if ball.x_Velocity < 0:
            if ball.y >= left_paddle.y and ball.y <= left_paddle.y + left_paddle.height:
                if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
                    s1.play()
                    ball.x_Velocity *= -1

                    middle_y = left_paddle.y + left_paddle.height/2
                    difference_in_y = middle_y - ball.y
                    reduction_factor = (left_paddle.height/2) / ball.MAX_VEL
                    y_Velocity = difference_in_y / reduction_factor
                    ball.y_Velocity = -1 * y_Velocity
        else:
            if ball.y >= right_paddle.y and ball.y <= right_paddle.y + right_paddle.height:
                if ball.x + ball.radius >= right_paddle.x:
                    s1.play()
                    ball.x_Velocity *= -1

                    middle_y = right_paddle.y + right_paddle.height / 2
                    difference_in_y = middle_y - ball.y
                    reduction_factor = (right_paddle.height / 2) / ball.MAX_VEL
                    y_Velocity = difference_in_y / reduction_factor
                    ball.y_Velocity = -1 * y_Velocity


    def handle_paddle_movement(keys, left_paddle, right_paddle):
        if keys[pygame.K_w] and left_paddle.y - left_paddle.Velocity >= 0:
            left_paddle.move(up=True)
        if keys[pygame.K_s] and left_paddle.y + left_paddle.Velocity + left_paddle.height <= HEIGHT:
            left_paddle.move(up=False)

        if keys[pygame.K_UP] and right_paddle.y - right_paddle.Velocity >= 0:
            right_paddle.move(up=True)
        if keys[pygame.K_DOWN] and right_paddle.y + right_paddle.Velocity + right_paddle.height <= HEIGHT:
            right_paddle.move(up=False)

    player1_name = player1_name.upper()
    player2_name = player2_name.upper()
    gameRun = True
    clock = pygame.time.Clock()
    left_paddle = Paddle(10, HEIGHT//2 - paddle_height //
                         2, paddle_width, paddle_height)
    right_paddle = Paddle(WIDTH - 10 - paddle_width, HEIGHT //
                          2 - paddle_height // 2, paddle_width, paddle_height)
    ball = Ball(WIDTH//2, HEIGHT//2, Ball_radius)
    player1 = 0
    player2 = 0

    while gameRun:
        clock.tick(FPS)
        draw(WIN, [left_paddle, right_paddle], ball, player1, player2)
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type==pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                gameRun = False
                break

        keys = pygame.key.get_pressed()
        handle_paddle_movement(keys, left_paddle, right_paddle)
        ball.move()
        handle_collision(ball, left_paddle, right_paddle)

        if ball.x < 0:
            player2 += 1
            ball.reset()
        elif ball.x > WIDTH:
            player1 += 1
            ball.reset()

        if player1 >= Winning_score:
            win_text = f"{player1_name} Won"
            text = Score_font1.render(win_text, 1, White)
            WIN.blit(text, (WIDTH//2 - text.get_width() //
                     2, HEIGHT//2 - text.get_height()//2))
            pygame.display.update()
            pygame.time.delay(5000)
            score1 = player1
            score2 = player2
            break
        elif player2 >= Winning_score:
            win_text = f"{player2_name} Won"
            text = Score_font1.render(win_text, 1, White)
            WIN.blit(text, (WIDTH // 2 - text.get_width() //
                     2, HEIGHT // 2 - text.get_height() // 2))
            pygame.display.update()
            pygame.time.delay(5000)
            score1 = player1
            score2 = player2
            break
    pygame.quit()

    if gameRun==True:
        # Saving different stats of the player in csv file
        d = pd.read_csv('pong_game_stat.csv')
        df1 = pd.DataFrame(d)
        lst = list(df1["Name"])
        p1p = False
        p2p = False
        total_game_played1 = 1
        total_game_played2 = 1
        games_won1 = 0
        games_won2 = 0
        games_lost1 = 0
        games_lost2 = 0
        p1_scr = 0
        p2_scr = 0
        idx1 = 0
        idx2 = 0
        for i in range(len(lst)):
            if lst[i] == player1_name:
                p1p = True
                idx1 = i
                p1_scr = df1.iloc[i]["Score"]
                total_game_played1 = df1.iloc[i]["Total_games_played"]
                total_game_played1 += 1
                games_won1 = df1.iloc[i]["Games_won"]
                games_lost1 = df1.iloc[i]["Games_lost"]
            if lst[i] == player2_name:
                p2p = True
                idx2 = i
                p2_scr = df1.iloc[i]["Score"]
                total_game_played2 = df1.iloc[i]["Total_games_played"]
                total_game_played2 += 1
                games_won2 = df1.iloc[i]["Games_won"]
                games_lost2 = df1.iloc[i]["Games_lost"]

        if p1p == True:
            df1 = df1.drop(idx1)
        if p2p == True:
            df1 = df1.drop(idx2)

        if score1 > score2:
            p1_scr += (10+score1)
            p2_scr += score2
            games_won1 += 1
            games_lost2 += 1
        else:
            p1_scr += score1
            p2_scr += (10+score2)
            games_won2 += 1
            games_lost1 += 1

        data = {
            'Name': [player1_name, player2_name],
            'Score': [p1_scr, p2_scr],
            'Total_games_played': [total_game_played1, total_game_played2],
            'Games_won': [games_won1, games_won2],
            'Games_lost': [games_lost1, games_lost2]
        }

        df2 = pd.DataFrame(data)
        df = pd.concat([df2, df1], axis=0)
        df.to_csv('pong_game_stat.csv', index=False, header=True)

if __name__ == '__main__':
    main()