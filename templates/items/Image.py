from templates.items.NanamiStudio import NanamiStudio


class Image(NanamiStudio):
    def __init__(self, screen, src, position, scale):
        super().__init__(screen, src, position, scale)
