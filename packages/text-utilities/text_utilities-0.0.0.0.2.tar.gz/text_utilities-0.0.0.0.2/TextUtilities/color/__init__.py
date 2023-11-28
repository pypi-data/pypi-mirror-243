class rgbtext():
    """The rgbtext class is used to represent and manipulate text with RGB color values."""

    def __init__(self, text=0, red=0, green=0, blue=0, reset=True) -> str:
        self.text = text
        self.red = red
        self.green = green
        self.blue = blue

    def __str__(self):
        textretrun = "[38;2;{0};{1};{2}m{3}".format(
            self.red, self.green, self.blue, self.text)
        if self.reset:
            textretrun = textretrun + "[37m"
        return textretrun
