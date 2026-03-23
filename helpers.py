import pygame


def draw_shading_for_rect(top_color, rect, surface, shading_W = 2,
                            left_color = None, right_color = None, bottom_color = None):
    '''
    draw custom shading for spesicif rectangel
    '''
    # top
    pygame.draw.line(surface, top_color, (rect.x, rect.y),
                        (rect.x + rect.width, rect.y), shading_W)
    # left
    if left_color is None:
        left_color = top_color
    pygame.draw.line(surface, left_color, (rect.x, rect.y),
                        (rect.x, rect.y + rect.height), shading_W)
    # right
    if right_color is None:
        right_color = top_color
    pygame.draw.line(surface, right_color, (rect.x + rect.width, rect.y),
                        (rect.x + rect.width, rect.y + rect.height), shading_W)
    # bottom
    if bottom_color is None:
        bottom_color = right_color
    pygame.draw.line(surface, bottom_color, (rect.x, rect.y + rect.height),
                        (rect.x + rect.width, rect.y + rect.height), shading_W)
