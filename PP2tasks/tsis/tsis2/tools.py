import pygame

def draw_shape(surface, color, start, end, shape_type, width):
    x1, y1 = start
    x2, y2 = end
    
    rect = pygame.Rect(min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1))

    if shape_type == 'rect':
        pygame.draw.rect(surface, color, rect, width)
        
    elif shape_type == 'square':
        side = max(rect.width, rect.height)
        square_rect = pygame.Rect(
            x1 if x1 < x2 else x1 - side,
            y1 if y1 < y2 else y1 - side,
            side, side
        )
        pygame.draw.rect(surface, color, square_rect, width)
        
    elif shape_type == 'circle':
        radius = max(rect.width, rect.height) // 2
        center = (min(x1, x2) + radius, min(y1, y2) + radius)
        if radius > 0:
            pygame.draw.circle(surface, color, center, radius, width)
            
    elif shape_type == 'right_tri':
        points = [(x1, y1), (x1, y2), (x2, y2)]
        if len(set(points)) > 2:
            pygame.draw.polygon(surface, color, points, width)
            
    elif shape_type == 'eq_tri':
        mid_x = (x1 + x2) // 2
        points = [(mid_x, y1), (x1, y2), (x2, y2)]
        if len(set(points)) > 2:
            pygame.draw.polygon(surface, color, points, width)
            
    elif shape_type == 'rhombus':
        mid_x, mid_y = (x1 + x2) // 2, (y1 + y2) // 2
        points = [(mid_x, y1), (x2, mid_y), (mid_x, y2), (x1, mid_y)]
        if len(set(points)) > 2:
            pygame.draw.polygon(surface, color, points, width)


def flood_fill(surface, position, fill_color):
    fill_color_mapped = surface.map_rgb(fill_color)
    x, y = position
    width, height = surface.get_size()
    
    pixel_array = pygame.PixelArray(surface)
    target_color_mapped = pixel_array[x, y]

    if target_color_mapped == fill_color_mapped:
        pixel_array.close()
        return

    stack = [(x, y)]
    while stack:
        cx, cy = stack.pop()
        
        if 0 <= cx < width and 0 <= cy < height:
            if pixel_array[cx, cy] == target_color_mapped:
                pixel_array[cx, cy] = fill_color_mapped
                
                stack.append((cx - 1, cy))
                stack.append((cx + 1, cy))
                stack.append((cx, cy - 1))
                stack.append((cx, cy + 1))
                
    pixel_array.close()