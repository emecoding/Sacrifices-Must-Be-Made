import pygame

SPRITES_PATH: str = "resources/sprites/"

def load_sprite_sheet(path: str, sprite_width: int, sprite_height: int, amount_of_sprites: int, flip_frames_horizontally: bool = False, flip_frames_vertically: bool = False) -> list:
    sprites: list = []
    full_path: str = SPRITES_PATH + path
    sprite_sheet: pygame.Surface = __open_image(full_path)

    sprites_on_x: int = int(sprite_sheet.get_width()/sprite_width)
    sprites_on_y: int = int(sprite_sheet.get_height()/sprite_height)


    for y in range(0, sprites_on_y):
        for x in range(0, sprites_on_x):
            rect: pygame.Rect = pygame.Rect(x*sprite_width, y*sprite_height, sprite_width, sprite_height)
            sprite: pygame.Surface = pygame.Surface(rect.size).convert()
            sprite.blit(sprite_sheet, (0, 0), rect)

            sprite = pygame.transform.flip(sprite, flip_frames_horizontally, flip_frames_vertically)

            color_key: tuple = sprite.get_at((0, 0))
            sprite.set_colorkey(color_key)

            sprites.append(sprite)

            if amount_of_sprites != None:
                if len(sprites) >= amount_of_sprites:
                    return sprites

    print(f"Something might have failed with {full_path}")
    return sprites

def get_sprites_from_index_A_to_index_B(index_A: int, index_B: int, sprite_sheet: list) -> list:
    sprites: list = []
    for i in range(index_A, index_B+1):
        sprites.append(sprite_sheet[i])
    return sprites

def load_image(path: str, size: list) -> pygame.Surface:
    image = pygame.image.load(path)
    image = pygame.transform.scale(image, size)
    return image

def __open_image(path: str) -> pygame.Surface:
    try:
        return pygame.image.load(path).convert()
    except pygame.error as message:
        print(f"Failed to load image {path}")
        print(message)
        return None

