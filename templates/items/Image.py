from templates.items.ArisStudio import ArisStudio


class Image(ArisStudio):
    def __init__(self, screen, src, position, scale):
        super().__init__(screen, src, position, scale)
