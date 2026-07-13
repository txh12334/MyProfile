import random
import time
import os
from pynput.keyboard import Key, Listener

# 游戏配置
WIDTH = 30
HEIGHT = 15
snake = [(HEIGHT // 2, WIDTH // 2)]
food = None
dx, dy = 1, 0  # 初始向右
score = 0
game_over = False

# 生成食物
def create_food():
    while True:
        y = random.randint(1, HEIGHT - 2)
        x = random.randint(1, WIDTH - 2)
        if (y, x) not in snake:
            return (y, x)

food = create_food()

# 键盘监听
def on_press(key):
    global dx, dy, game_over
    if game_over:
        return
    # 禁止反向掉头
    if key == Key.up and dy != 1:
        dx, dy = 0, -1
    elif key == Key.down and dy != -1:
        dx, dy = 0, 1
    elif key == Key.left and dx != 1:
        dx, dy = -1, 0
    elif key == Key.right and dx != -1:
        dx, dy = 1, 0
    elif key == Key.esc:
        game_over = True

# 启动键盘监听（后台不阻塞游戏）
listener = Listener(on_press=on_press)
listener.start()

# 主游戏循环
try:
    while not game_over:
        os.system("cls")  # Windows清屏
        # 计算蛇头新坐标
        head_y, head_x = snake[0]
        new_x = head_x + dx
        new_y = head_y + dy

        # 撞墙判定
        if new_x < 1 or new_x >= WIDTH - 1 or new_y < 1 or new_y >= HEIGHT - 1:
            game_over = True
            break
        # 撞自己判定
        if (new_y, new_x) in snake:
            game_over = True
            break

        # 移动蛇
        snake.insert(0, (new_y, new_x))
        # 吃到食物
        if (new_y, new_x) == food:
            score += 10
            food = create_food()
        else:
            snake.pop()

        # 绘制顶部信息栏
        print(f"===== 贪吃蛇 | 得分：{score} | ESC退出 =====")
        # 逐行绘制游戏区域，白色■做边框
        for y in range(HEIGHT):
            line = ""
            for x in range(WIDTH):
                # 上下左右边框：白色方块
                if y == 0 or y == HEIGHT - 1 or x == 0 or x == WIDTH - 1:
                    line += "■"
                elif (y, x) == snake[0]:
                    line += "◆"  # 蛇头
                elif (y, x) in snake[1:]:
                    line += "□"  # 蛇身
                elif (y, x) == food:
                    line += "●"  # 食物
                else:
                    line += " "
            print(line)
        time.sleep(0.12)

    # 游戏结束画面
    os.system("cls")
    print("=========================================")
    print(f"        游戏结束！得分：{score}")
    print("=========================================")
    input("\n按回车键关闭窗口...")

finally:
    listener.stop()