import sys
import json
import pygame

from Config import SystemConfig
from items.UI import UI
from items.Image import Image
from items.Scene import Scene
from items.Character import Character
from templates.items.NanamiStudio import NanamiStudio

# ======================================== game initialization ========================================
# 初始化pygame
pygame.init()
pygame.font.init()

# 设置窗口
# 设置游戏分辨率
window_width, window_height = SystemConfig.window_width, SystemConfig.window_height
window_width_copy, window_height_copy = window_width, window_height
window_scale = window_height / window_width
with open('resource/config.json', 'r') as config:
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN) if json.load(config)[
        'fullscreen'] else pygame.display.set_mode((window_width, window_height), pygame.RESIZABLE)
# 设置窗口大小
# scaled_surface = pygame.transform.scale(screen, (SystemConfig.window_width, SystemConfig.window_height))
pygame.display.set_caption(title=SystemConfig.title)
pygame.display.set_icon(pygame.image.load(SystemConfig.icon))

# ======================================== constants variables initialization ========================================
# 定义颜色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (100, 100, 100)

character = Character(screen, 'assets/images/azusa_happy.png', font_color='#9775fa', position=(-70, -65), scale=2, zoom_mode=NanamiStudio.FILL)
scene = Scene(screen, 'assets/images/scene.png', position=(0, 0), scale=1, zoom_mode=NanamiStudio.ADAPT)
ui = UI(screen, '#eebefa', position=(0, 0), scale=0.24, alpha=155, alignment=UI.BOTTOM)


def keyboard_event(event: pygame.event.Event):
    if event.key == pygame.K_a:  # 自动模式
        print('A key pressed')
    elif event.key == pygame.K_s:  # 保存
        print('S key pressed')
    elif event.key == pygame.K_l:  # 加载
        print('L key pressed')
    elif event.key == pygame.K_ESCAPE or event.key == pygame.K_TAB:  # 系统栏目
        print('Escape or Tab key pressed')
    elif event.key == pygame.K_RETURN and (event.mod & pygame.KMOD_ALT):  # 全屏模式
        global screen
        with open('resource/config.json', 'r') as config:
            json_data = json.load(config)
            fullscreen = json_data['fullscreen']
            fullscreen = not fullscreen
        if fullscreen:
            screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            screen = pygame.display.set_mode((0, 0), pygame.WINDOWMOVED)
            screen = pygame.display.set_mode((SystemConfig.window_width, SystemConfig.window_height), pygame.RESIZABLE)
        with open('resource/config.json', 'w') as config:
            json_data['fullscreen'] = fullscreen
            json.dump(json_data, config)


number = 3
def next_event():
    # ==================== test ====================
    if character.active:
        character.image = pygame.image.load('assets/images/azusa_happy.png')
        # character.move_to((-270, 0))
    else:
        character.image = pygame.image.load('assets/images/azusa_normal.png')
        # character.move_to((130, 0))
    global number
    character.animation(Character.ANIMATE_DISTANCE, number % 3)
    print(f"number: {number % 3}")
    number += 1
    character.active = not character.active


def mouse_event(event: pygame.event.Event):
    if event.type == pygame.MOUSEBUTTONDOWN:
        # 获取鼠标点击的位置
        mouse_x, mouse_y = event.pos
        print(f'Mouse clicked at position ({mouse_x}, {mouse_y})')

        if event.button == 1:  # 鼠标左键
            # 左键单击
            print('Left mouse button pressed')
            next_event()
        elif event.button == 3:  # 鼠标右键
            # 隐藏UI
            print('Right mouse button pressed')
        elif event.button == 4:  # 鼠标滚轮向上滚动
            # 展示历史记录
            print('Mouse wheel scrolled up, show history')
        elif event.button == 5:  # 鼠标滚轮向下滚动
            # 快速翻页
            print('Mouse wheel scrolled down')
        elif event.button == 2:  # 鼠标中键
            # 没啥用
            print('Middle mouse button pressed')


def refresh_screen():
    scene.update(screen)  # 场景重新渲染
    character.update(screen)  # 角色重新渲染
    ui.update(screen, message="和我在一起吧！小狐老师！", fontcolor=character.font_color, fontsize='100%')  # UI重新渲染


def run():
    global screen
    screen.fill(WHITE)
    # 游戏循环
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                keyboard_event(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_event(event)
            elif event.type == pygame.WINDOWRESIZED and SystemConfig.window_aspect_ratio_lock:
                screen_width, screen_height = screen.get_size()
                # 计算缩放比例
                scale = min(screen_width / window_width_copy, screen_height / window_height_copy)
                # 根据缩放比例调整屏幕尺寸
                new_width = int(window_width_copy * scale)
                new_height = int(window_height_copy * scale)
                # 设置新的屏幕模式
                screen = pygame.display.set_mode((new_width, new_height), pygame.RESIZABLE)

        refresh_screen()  # 重新渲染
        pygame.display.flip()
        pygame.time.Clock().tick(60)

    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    run()
