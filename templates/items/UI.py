import pygame
from PIL import Image, ImageFilter

from templates.items.ArisStudio import ArisStudio


class UI(ArisStudio):
    """
    This class represents the UI of the game.
    @param screen: The pygame screen object.
    """
    TOP = 0
    CENTER = 1
    BOTTOM = 2

    def __init__(self, screen, image, position: tuple[int, int] = (0, 0), scale: float = 1, blur_radius: int = 10):
        super().__init__(screen, image, position, scale)
        self.blur_radius = blur_radius
        self.resolution_adjust()
        self.blur_top()

    def resolution_adjust(self):
        """
        This method returns the resolution of the screen.
        """
        self.image = pygame.transform.scale(self.image, (self.screen.get_width(), self.screen.get_height() // 2.4))

    def blur_top(self):
        """
        这个方法对图像的顶部进行羽化处理。
        :return: 处理后的 pygame 图像对象。
        """
        # 将pygame Surface对象转换为字符串
        # 创建一个Surface对象
        gradient_surface = pygame.Surface((200, 400)).convert_alpha()
        color = self.image.get_at((1, 1))
        # 设置Surface的背景颜色为透明
        gradient_surface.set_colorkey(color)  # 使用洋红色作为透明色
        start_color = (color.r, color.g, color.b, 0)  # 完全透明
        end_color = color  # 完全不透明
        height = gradient_surface.get_height()
        for y in range(height):
            # 计算当前行的透明度
            alpha = int(start_color[3] + (end_color[3] - start_color[3]) * y / height)
            # 设置当前行的颜色
            color = (start_color[0], start_color[1], start_color[2], alpha)
            # 填充当前行
            pygame.draw.line(gradient_surface, color, (0, y), (gradient_surface.get_width(), y))
        self.image = gradient_surface
        self.window_image = gradient_surface

    def auto_fit(self):
        """
        This method adjusts the image to fit the screen.
        """
        screen_width, screen_height = self.screen.get_size()
        image_width, image_height = self.image.get_size()

        self.window_image = pygame.transform.scale(self.image, (
            int(screen_width), int(screen_height * self.scale)))

        # 更新图片的位置以适应屏幕
        new_image_width, new_image_height = self.window_image.get_size()
        self.image_rect.update((screen_width - new_image_width) // 2 + self.position[0], self.position[1], 0, 0)

    def update(self, screen):
        # 屏幕更新
        self.screen = screen
        self.auto_fit()
        # 绘制图片
        self.screen.blit(self.window_image, self.image_rect)
