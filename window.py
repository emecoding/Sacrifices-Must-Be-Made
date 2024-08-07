import pygame



class Window:
    def __init__(self, width: int, height: int, title: str):
        self.__mWidth: int = width
        self.__mHeight: int = height

        self.__mTitle: str = title

        self.__pgWindow: pygame.Surface = None

        self.__mShouldClose: bool = False

        self.__mBackgroundColor: tuple = (0, 0, 0)

    def initialize(self):
        self.__pgWindow = pygame.display.set_mode((self.__mWidth, self.__mHeight))
        if self.__pgWindow == None: print("Window initialization failed...")
        pygame.display.set_caption(self.__mTitle)

    def should_close(self) -> bool: return self.__mShouldClose

    def window_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__mShouldClose = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.__mShouldClose = True

    def update_caption(self, caption: str):
        pygame.display.set_caption(f"{self.__mTitle} - {caption}")

    def fill(self): self.__pgWindow.fill(self.__mBackgroundColor)

    def set_background_color(self, color: tuple): self.__mBackgroundColor = color

    def set_window_should_close(self, value: bool): self.__mShouldClose = value

    def update(self): pygame.display.update()

    def destroy(self):
        pygame.quit()

    def surface(self): return self.__pgWindow

    def width(self): return self.__mWidth
    def height(self): return self.__mHeight


WINDOW: Window = None



