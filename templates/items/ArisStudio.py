import os

import pygame


class ArisStudio(object):
    FILL = 0  # 填充模式
    ADAPT = 1  # 自适应模式
    NOT_ADJUST = 2  # 不调整模式

    def __init__(self, screen: pygame.Surface,
                 image: str | pygame.Surface | tuple[int, int, int],
                 position: tuple[int, int] = (0, 0),
                 scale: float = 1.0,
                 zoom_mode: int = FILL):
        super().__init__()
        self.screen = screen  # 屏幕
        self.image: pygame.Surface | None = None
        self.image_rect: pygame.Rect | None = None
        self.load_image(image)  # 加载图片(这个是常量)
        self.window_image = self.image.copy()  # 窗口图片
        self.position = position  # 位置
        self.scale = scale  # 缩放比例
        self.adapt_mode = zoom_mode  # 自适应模式
        # 备份默认参数
        self.default_center_position = position  # 中心位置
        self.default_scale = scale  # 缩放比例

    def load_image(self, image):
        if isinstance(image, str):
            if os.path.isfile(image):
                self.image = pygame.image.load(image)
                self.image_rect = self.image.get_rect()
            else:
                self.image = pygame.Surface((1, 1))
                self.image_rect = self.image.fill(image)
        elif isinstance(image, tuple):
            self.image = pygame.Surface((1, 1))
            self.image_rect = self.image.fill(image)
        else:
            raise TypeError('Image type error!')

    def auto_fit(self):
        """
        自动缩放图片并调整角色位置，使其适应屏幕大小
        """
        screen_width, screen_height = self.screen.get_size()
        image_width, image_height = self.image.get_size()

        # 自适应窗口比例
        limit = 1.0
        if self.adapt_mode == self.NOT_ADJUST:
            self.window_image = self.image.copy()
        else:
            if screen_width / image_width < screen_height / image_height:
                if self.adapt_mode == self.FILL:
                    limit = screen_width / image_width
                elif self.adapt_mode == self.ADAPT:
                    limit = screen_height / image_height
            else:
                if self.adapt_mode == self.FILL:
                    limit = screen_height / image_height
                elif self.adapt_mode == self.ADAPT:
                    limit = screen_width / image_width
        self.window_image = pygame.transform.scale(self.image, (
            int(image_width * limit * self.scale), int(image_height * limit * self.scale)))

        # 更新图片的位置以适应屏幕
        new_image_width, new_image_height = self.window_image.get_size()
        self.image_rect.update((screen_width - new_image_width) // 2 + self.position[0], self.position[1], 0, 0)

    def reset(self):
        """
        重置角色位置
        """
        self.position = self.default_center_position
        self.scale = self.default_scale

    def update(self, screen):
        # 屏幕更新
        self.screen = screen
        self.auto_fit()
        # 绘制图片
        self.screen.blit(self.window_image, self.image_rect)
