import random
from PIL import Image, ImageDraw

# Settings
image_size = (2000, 600)

background_color = (255, 220, 197, 255)
level1_color = (200, 71, 61, 255)
level2_color = (140, 48, 53, 255)
level3_color = (126, 36, 46, 255)
level4_color = (82, 7, 51, 255)
level5_color = (44, 25, 55, 255)
sun_color = (255, 254, 255, 255)
bird_color = (20, 10, 18, 255)
# End Settings

im = Image.new('RGBA', image_size, background_color)
draw = ImageDraw.Draw(im)

def draw_a_mountainrange(width_variation, height_variation, horizon, color, count):
    for _ in range(1, count):
        # Generate a point-up equilateral triangle
        width = random.randrange(*width_variation)
        height = random.randrange(*height_variation)

        start_offset = image_size[0] // 4
        start = random.randrange(-start_offset, image_size[0]+start_offset)

        draw.polygon([
            (start, horizon),
            (start+width/2, horizon-height),
            (start+width, horizon)
            ], fill=color)

def draw_a_sun(radius_variation, height_variation, color):
    radius = random.randrange(*radius_variation)
    height = random.randrange(*height_variation)

    center = (image_size[0]/2, height)

    draw.ellipse([
        (center[0] - radius, center[1] - radius),
        (center[0] + radius, center[1] + radius),
        ], fill=color)

def draw_a_trunk(center_x, horizon, trunk_width, height, color):
    draw.polygon([
        (center_x- (trunk_width/2), horizon),
        (center_x- (trunk_width/4), horizon-height),
        (center_x+ (trunk_width/4), horizon-height),
        (center_x+ (trunk_width/2), horizon)
        ], fill=color)

def draw_a_branch(center_x, horizon, this_branch_width, this_branch_height, this_branch_offset, color):
    draw.polygon([
        (center_x - (this_branch_width/2), horizon-this_branch_offset),
        (center_x, horizon-this_branch_offset-this_branch_height),
        (center_x + (this_branch_width/2), horizon-this_branch_offset),
        ], fill=color)

def split_distribute(iterable, count):
    items = list(iterable)
    #print(size, count, len(items), items)

    if len(items) < count:
        items += [items[-1]] * count

    size = int(len(items) / count)
    return [ items[i] for i in range(0, len(items), size) ]

def draw_a_tree(center_x, horizon, trunk_width, branch_width, branch_count, height, color):
    draw_a_trunk(center_x, horizon, trunk_width, height, color)

    widths = sorted([ random.randint(branch_width // 2, int(branch_width)) for _ in range(0, branch_count) ], reverse=True)
    #heights = sorted([ random.randint(height * 0.25, height * 0.5) for _ in range(0, branch_count) ], reverse=True)
    #offsets = sorted([ random.randint(height * 0.5, height) for _ in range(0, branch_count) ])

    # TODO: random.triangle around these values?
    heights = split_distribute(range(height//4, height//3), branch_count)
    offsets = split_distribute(range(height//2, height), branch_count)

    for i in range(0, branch_count):
        draw_a_branch(center_x, horizon, widths[i], heights[i], offsets[i], color)

def draw_a_forest(tree_count, color, height_extents, aspect_ratio):
    for _ in range(0, tree_count):
        center_x = random.randint(0, image_size[0])
        horizon = image_size[1]
        height = random.randint(*height_extents)
        branch_width = height * aspect_ratio
        trunk_width = branch_width / 4

        branch_count = random.randint(2, 5)

        draw_a_tree(center_x, horizon, trunk_width, branch_width, branch_count, height, color)


def draw_some_birds(bird_count, color, x_extents, y_extents, width_extents, linewidth, aspect_ratio):

    for _ in range(0, bird_count):
        center_x = random.randint(*x_extents)
        baseline  = random.randint(*y_extents)
        width = random.randint(*width_extents)
        height = width * aspect_ratio

        draw.arc([(center_x-width, baseline), (center_x, baseline + height)], 270, 0, fill=color, width=linewidth)
        draw.arc([(center_x, baseline), (center_x + width, baseline + height)], 180, 270, fill=color, width=linewidth)

draw_a_sun((15, 20), (200, 300), sun_color)
draw_a_mountainrange((400, 700), (190, 400), image_size[1], level1_color, 128)
draw_a_mountainrange((400, 700), (140, 320), image_size[1], level2_color, 128)
draw_a_mountainrange((500, 800), (80, 230), image_size[1], level3_color, 128)
draw_a_forest(400, level4_color, (40, 170), 0.4)
draw_a_forest(1900, level5_color, (40, 100), 0.4)

draw_some_birds(3, bird_color, (200,400), (190, 220), (8, 28), 2, 2/3)
draw_some_birds(4, bird_color, (1400, 1700), (320, 390), (8, 16), 2, 2/3)

im.save('output.png')
