# 角色类
import threading
import time

import pygame

from templates.items.ArisStudio import ArisStudio


# 参数分别是：屏幕，图片路径，字体颜色，字体大小，字体，位置，缩放比例
class Character(ArisStudio):
    ANIMATE_JITTER = 0  # 抖动动画
    ANIMATE_SHAKE = 1  # 摇晃动画
    ANIMATE_MOVE = 2  # 移动动画
    ANIMATE_APPEAR = 3  # 出现动画
    ANIMATE_DISAPPEAR = 4  # 消失动画
    ANIMATE_DISTANCE = 5  # 距离控制动画

    APPROACH = 0  # 接近动画
    OPPOSITE = 1  # 正对动画
    RETREAT = 2  # 远离动画

    LEFT = 0  # 左
    MIDDLE_LEFT = 1  # 中左
    CENTER = 2  # 中间
    MIDDLE_RIGHT = 3  # 中右
    RIGHT = 4  # 右

    def __init__(self, screen: pygame.Surface, image: str, font_color: tuple[int, int, int] | str = (255, 255, 255),
                 font_size: int = 20, font: pygame.font.Font = "", position: tuple[float | int, float | int] = (0, 0),
                 scale: float = 1, zoom_mode: int = ArisStudio.FILL):
        super().__init__(screen, image, position, scale, zoom_mode)
        self.font_color = font_color  # 字体颜色
        self.font_size = font_size  # 字体大小
        self.font = font  # 字体
        self.active = False  # 是否活动
        # 动画参数
        self.animation_step = 10  # 动画步数
        self.target_position = position  # 目标位置
        self.target_scale = scale  # 目标位置
        self.animate_thread = None  # 动画线程
        # 备份默认参数
        self.default_animation_step = self.animation_step

    def move_to(self, position: [float | int, float | int]):
        """
        移动到指定位置
        """
        self.target_position = position

    def move_add(self, position: [float | int, float | int] = (0, 0)):
        """
        移动指定步数
        """
        self.target_position = (self.target_position[0] + position[0], self.target_position[1] + position[1])

    def scale_to(self, scale: float):
        """
        缩放到指定比例
        """
        self.target_scale = scale

    def update_position(self):
        """
        更新角色位置，实现平滑移动
        """
        # 计算当前位置和目标位置之间的差异
        dx = (self.target_position[0] - self.position[0]) / self.animation_step
        dy = (self.target_position[1] - self.position[1]) / self.animation_step

        # 根据差异调整位置
        self.position = (self.position[0] + dx, self.position[1] + dy)

        # 当接近目标位置时，停止移动
        if abs(self.position[0] - self.target_position[0]) < abs(dx) and abs(
                self.position[1] - self.target_position[1]) < abs(dy):
            self.position = self.target_position

    def update_scale(self):
        """
        更新角色缩放比例，实现平滑缩放
        """
        # 计算当前缩放比例和目标缩放比例之间的差异
        ds = (self.target_scale - self.scale) / self.animation_step

        # 根据差异调整缩放比例
        self.scale = self.scale + ds

        # 当接近目标缩放比例时，停止缩放
        if abs(self.scale - self.target_scale) < abs(ds):
            self.scale = self.target_scale

    def animation(self, mode: int, properties: int | None = None):
        """
        启动抖动动画线程
        """
        if self.animate_thread is None or not self.animate_thread.is_alive():
            if mode == self.ANIMATE_JITTER:
                self.animate_thread = threading.Thread(target=self.animate_jitter)
                self.animate_thread.start()
            elif mode == self.ANIMATE_SHAKE:
                self.animate_thread = threading.Thread(target=self.animate_shake)
                self.animate_thread.start()
            elif mode == self.ANIMATE_MOVE and properties is not None:
                self.animate_thread = threading.Thread(target=self.animate_move, args=(properties,))
                self.animate_thread.start()
            elif mode == self.ANIMATE_DISTANCE and properties is not None:
                self.animate_thread = threading.Thread(target=self.animate_distance, args=(properties,))
                self.animate_thread.start()

    def animate_jitter(self):
        """
        角色抖动动画
        """
        screen_width, screen_height = self.screen.get_size()
        self.animation_step = 3

        delay = 0.2
        for _ in range(2):  # 抖动两次
            self.move_add((0, -screen_height // 10))
            time.sleep(delay)
            self.move_add((0, screen_height // 10))
            time.sleep(delay)

    def animate_shake(self):
        """
        角色摇晃动画
        """
        screen_width, screen_height = self.screen.get_size()
        self.animation_step = 2

        delay = 0.1  # 延迟
        self.move_add((-screen_width // 60, 0))
        time.sleep(delay)
        self.move_add((screen_width // 30, 0))
        time.sleep(delay)
        self.move_add((-screen_width // 30, 0))
        time.sleep(delay)
        self.move_add((screen_width // 30, 0))
        time.sleep(delay)
        self.move_add((-screen_width // 60, 0))
        time.sleep(delay)

    def animate_move(self, location: int):
        """
        角色摇晃动画
        """
        screen_width, screen_height = self.screen.get_size()
        self.animation_step = 6

        delay = 0  # 延迟
        if location == self.LEFT:
            position_x = -screen_width // 2.8 + self.default_center_position[0]
            self.move_to((position_x, self.position[1]))
            time.sleep(delay)
        elif location == self.MIDDLE_LEFT:
            position_x = -screen_width // 5.6 + self.default_center_position[0]
            self.move_to((position_x, self.position[1]))
            time.sleep(delay)
        elif location == self.CENTER:
            position_x = self.default_center_position[0]
            self.move_to((position_x, self.position[1]))
            time.sleep(delay)
        elif location == self.MIDDLE_RIGHT:
            position_x = screen_width // 5.6 + self.default_center_position[0]
            self.move_to((position_x, self.position[1]))
            time.sleep(delay)
        elif location == self.RIGHT:
            position_x = screen_width // 2.8 + self.default_center_position[0]
            self.move_to((position_x, self.position[1]))
            time.sleep(delay)

    """
    distance: 距离控制
    @:param distance: 距离
    APPROACH = 0  # 接近动画
    OPPOSITE = 1  # 正对动画
    RETREAT = 2  # 远离动画
    """
    def animate_distance(self, distance: int):
        self.animation_step = 4
        delay = 0  # 延迟
        if distance == self.APPROACH:
            scale = self.default_scale * 1.4
            self.scale_to(scale)
            self.move_to((self.default_center_position[0], self.default_center_position[1]))
            time.sleep(delay)
        elif distance == self.OPPOSITE:
            scale = self.default_scale
            self.scale_to(scale)
            time.sleep(delay)
        elif distance == self.RETREAT:
            scale = self.default_scale * 0.8
            self.scale_to(scale)
            time.sleep(delay)

    def character_inactivate(self):
        """
        设置图片灰度
        """
        self.active = False

    def reset(self):
        self.position = self.default_center_position
        self.scale = self.default_scale
        self.animation_step = self.default_animation_step

    def update(self, screen, zoom_mode=ArisStudio.FILL):
        # 屏幕更新
        self.screen = screen
        self.auto_fit()
        self.update_position()
        self.update_scale()
        # 绘制图片
        self.screen.blit(self.window_image, self.image_rect)
