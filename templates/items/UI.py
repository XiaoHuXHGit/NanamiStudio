import pygame

from templates.items.NanamiStudio import NanamiStudio


class UI(NanamiStudio):
    """
    This class represents the UI of the game.
    @param screen: The pygame screen object.
    """
    TOP = 0
    CENTER = 1
    BOTTOM = 2

    def __init__(self, screen, image, position: tuple[int, int] = (0, 0), scale: float = 1, blur_radius: int = 10,
                 alpha: int = 255, alignment: int = BOTTOM):
        super().__init__(screen, image, position, scale)
        self.alpha = alpha
        self.alignment = alignment
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
        gradient_surface.set_colorkey((color.r, color.g, color.b, self.alpha))
        start_color = (color.r, color.g, color.b, 0)  # 完全透明
        end_color = (color.r, color.g, color.b, self.alpha)  # 完全不透明
        height = gradient_surface.get_height()

        gradient_start = 1 / 6 * height
        # 处理渐变部分
        for y in range(int(gradient_start)):
            # 计算当前行的透明度
            alpha = int(start_color[3] + (end_color[3] - start_color[3]) * (1 - (1 - y / gradient_start) ** 2))
            # 设置当前行的颜色
            color = (start_color[0], start_color[1], start_color[2], alpha)
            # 填充当前行
            pygame.draw.line(gradient_surface, color, (0, y), (gradient_surface.get_width(), y))
            # 处理完全不透明部分
            pygame.draw.rect(gradient_surface, end_color,
                             (0, int(gradient_start), gradient_surface.get_width(), height - int(gradient_start)))
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
        vertical_position = screen_height - new_image_height
        if self.alignment == self.TOP:
            vertical_position = 0
        elif self.alignment == self.CENTER:
            vertical_position = (screen_height - new_image_height) // 2
        elif self.alignment == self.BOTTOM:
            vertical_position = vertical_position
        self.image_rect.update(self.position[0], vertical_position + self.position[1], 0, 0)

    def message(self, message, fontcolor, fontsize, fontname):
        """
        这个方法用于在屏幕上显示文字。
        :param message: 要显示的文字。
        :param fontcolor: 文字颜色。
        :param fontsize: 文字大小。
        :param fontname: 字体名称。
        :return: 处理后的 pygame 图像对象。
        """
        # 加载字体
        font = pygame.font.Font(fontname, fontsize)
        # 绘制文字
        text_surface = font.render(message, True, fontcolor)
        text_rect = text_surface.get_rect()
        return text_surface, text_rect

    def update(self, screen, message=None, fontcolor=(0, 0, 0), fontsize=50,
               fontname=r"assets\fonts\微软雅黑.ttf"):
        # 屏幕更新
        self.screen = screen
        self.auto_fit()
        # 绘制图片
        self.screen.blit(self.window_image, self.image_rect)
        # 绘制文字
        if message is not None:
            self.screen.blit(*self.message(message, fontcolor, fontsize, fontname))
