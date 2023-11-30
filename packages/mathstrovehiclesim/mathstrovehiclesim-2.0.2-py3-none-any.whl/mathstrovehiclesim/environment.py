import math
import random

import pygame

import mathstrovehiclesim.globals

from .utils import calculate_roadside_area_width, get_sidewalk_x_loc

# create horizontal veh_sim.globals.WHITE lines as well
# have a fixed veh_sim.globals.WIDTH road
# then add extra objects


class Env:
    def __init__(self, number_of_lanes, show_horizontal_line=False):
        # calculate and setup number of lanes, grass area veh_sim.globals.WIDTH, etc.
        self.number_of_lanes = number_of_lanes
        self.number_of_white_lines = self.number_of_lanes - 1
        self.roadside_area_widths = calculate_roadside_area_width(
            mathstrovehiclesim.globals.WIDTH
            - (
                mathstrovehiclesim.globals.ROAD_LANE_WIDTH * self.number_of_lanes
                + self.number_of_white_lines * mathstrovehiclesim.globals.WHITE_LANE_WIDTH
            ),
            mathstrovehiclesim.globals.GRASS_AREA_RATIO,
            mathstrovehiclesim.globals.SIDEWALK_AREA_RATIO,
        )
        self.show_horizontal_line = show_horizontal_line

        # calculate the start and end points of scene rectangles (sidewalk, road)
        self.sidewalk_border_left = self.roadside_area_widths.grass_area_width
        self.sidewalk_border_right = (
            mathstrovehiclesim.globals.WIDTH - self.roadside_area_widths.grass_area_width * 2
        )
        self.road_border_left = (
            self.roadside_area_widths.grass_area_width
            + self.roadside_area_widths.sidewalk_area_width
        )
        self.road_border_right = mathstrovehiclesim.globals.WIDTH - 2 * (
            self.roadside_area_widths.grass_area_width
            + self.roadside_area_widths.sidewalk_area_width
        )

        # calculate the positions of veh_sim.globals.WHITE lines
        self.distance_pointer_white_lines = 0
        if show_horizontal_line:
            self.horizontal_line_x_loc = (
                mathstrovehiclesim.globals.WIDTH
                - (
                    self.roadside_area_widths.grass_area_width
                    + self.roadside_area_widths.sidewalk_area_width
                )
                - mathstrovehiclesim.globals.HORIZONTAL_LANE_WIDTH
            )
            self.horizontal_line_y_loc = range(
                mathstrovehiclesim.globals.HORIZONTAL_LANE_START_Y,
                mathstrovehiclesim.globals.HEIGHT,
                mathstrovehiclesim.globals.HORIZONTAL_LANE_GAP + mathstrovehiclesim.globals.HORIZONTAL_LANE_HEIGHT,
            )
            if mathstrovehiclesim.globals.DEBUG:
                print(self.horizontal_line_y_loc)
        else:
            self.white_y_loc = range(
                -mathstrovehiclesim.globals.WHITE_LANE_HEIGHT,
                mathstrovehiclesim.globals.HEIGHT,
                math.floor(mathstrovehiclesim.globals.WHITE_LANE_HEIGHT + mathstrovehiclesim.globals.WHITE_LANE_GAP),
            )
            self.white_x_loc = range(
                math.floor(
                    self.roadside_area_widths.grass_area_width
                    + self.roadside_area_widths.sidewalk_area_width
                    + mathstrovehiclesim.globals.ROAD_LANE_WIDTH
                ),
                math.floor(
                    mathstrovehiclesim.globals.WIDTH
                    - (
                        self.roadside_area_widths.grass_area_width
                        + self.roadside_area_widths.sidewalk_area_width
                    )
                ),
                mathstrovehiclesim.globals.ROAD_LANE_WIDTH + mathstrovehiclesim.globals.WHITE_LANE_WIDTH,
            )

        # calculate the positions of trees
        self.distance_pointer_trees = 0
        self.trees_group = pygame.sprite.Group()
        for tree_idx in range(
            mathstrovehiclesim.globals.TREES_START_POINT,
            mathstrovehiclesim.globals.HEIGHT,
            math.floor(mathstrovehiclesim.globals.TREES_WIDTH + mathstrovehiclesim.globals.TREES_GAP),
        ):
            tree_right = Tree(
                mathstrovehiclesim.globals.TREES_IMAGES[random.randint(0, 3)],
                mathstrovehiclesim.globals.TREES_WIDTH,
                (self.roadside_area_widths.grass_area_width, tree_idx),
            )
            tree_left = Tree(
                mathstrovehiclesim.globals.TREES_IMAGES[random.randint(0, 3)],
                mathstrovehiclesim.globals.TREES_WIDTH,
                (mathstrovehiclesim.globals.WIDTH - self.roadside_area_widths.grass_area_width, tree_idx),
            )
            self.trees_group.add(tree_right)
            self.trees_group.add(tree_left)

        # calculate the positions of houses
        self.distance_pointer_houses = 0
        self.houses_group = pygame.sprite.Group()
        for house_idx in range(
            mathstrovehiclesim.globals.HOUSE_START_POINT,
            mathstrovehiclesim.globals.HEIGHT,
            math.floor(mathstrovehiclesim.globals.HOUSES_WIDTH + mathstrovehiclesim.globals.HOUSES_GAP),
        ):
            house_right = House(
                mathstrovehiclesim.globals.HOUSES_IMAGES[random.randint(0, 3)],
                mathstrovehiclesim.globals.HOUSES_WIDTH,
                (0, house_idx),
            )
            house_left = Tree(
                mathstrovehiclesim.globals.HOUSES_IMAGES[random.randint(0, 3)],
                mathstrovehiclesim.globals.HOUSES_WIDTH,
                (mathstrovehiclesim.globals.WIDTH, house_idx),
            )
            self.houses_group.add(house_right)
            self.houses_group.add(house_left)

        # calculate the positions of sidewalk objects
        self.distance_pointer_sidewalk = 0
        self.sidewalk_group = pygame.sprite.Group()
        for sidewalk_idx in range(
            mathstrovehiclesim.globals.SIDEWALK_OBJECTS_START_POINT,
            mathstrovehiclesim.globals.HEIGHT,
            math.floor(
                mathstrovehiclesim.globals.SIDEWALK_OBJECTS_WIDTH
                + random.randint(
                    mathstrovehiclesim.globals.SIDEWALK_OBJECTS_GAP_MIN, mathstrovehiclesim.globals.SIDEWALK_OBJECTS_GAP_MAX
                )
            ),
        ):
            right_idx = random.randint(0, 7)
            left_idx = random.randint(0, 7)

            # is the object in right lane or left lane of the sidewalk?
            right_pos = random.randint(0, 1)
            left_pos = random.randint(0, 1)

            swo_right = SidewalkObject(
                mathstrovehiclesim.globals.SIDEWALK_OBJECTS_IMAGES[right_idx],
                mathstrovehiclesim.globals.SIDEWALK_OBJECTS_WIDTH,
                0 if right_idx < 4 else 1,
                (
                    get_sidewalk_x_loc(
                        mathstrovehiclesim.globals.WIDTH,
                        self.roadside_area_widths.grass_area_width,
                        mathstrovehiclesim.globals.GRASS_AREA_RATIO,
                        mathstrovehiclesim.globals.SIDEWALK_AREA_RATIO,
                        right_pos,
                    ),
                    sidewalk_idx,
                ),
                sidewalk_loc=right_pos,
            )
            swo_left = SidewalkObject(
                mathstrovehiclesim.globals.SIDEWALK_OBJECTS_IMAGES[left_idx],
                mathstrovehiclesim.globals.SIDEWALK_OBJECTS_WIDTH,
                0 if right_idx < 4 else 1,
                (
                    get_sidewalk_x_loc(
                        mathstrovehiclesim.globals.WIDTH,
                        self.roadside_area_widths.grass_area_width,
                        mathstrovehiclesim.globals.GRASS_AREA_RATIO,
                        mathstrovehiclesim.globals.SIDEWALK_AREA_RATIO,
                        left_pos,
                        left_side=True,
                    ),
                    sidewalk_idx,
                ),
                sidewalk_loc=left_pos,
            )
            self.sidewalk_group.add(swo_right)
            self.sidewalk_group.add(swo_left)

    def get_horizontal_line_location(self):
        temp = []
        for y_loc in self.horizontal_line_y_loc:
            temp.append((self.horizontal_line_x_loc, y_loc))
        return temp

    def get_vertical_line_location(self):
        return list(self.white_x_loc)

    def get_sidwalk_road_borders(self):
        return [
            self.roadside_area_widths.grass_area_width
            + self.roadside_area_widths.sidewalk_area_width,
            mathstrovehiclesim.globals.WIDTH
            - (
                self.roadside_area_widths.grass_area_width
                + self.roadside_area_widths.sidewalk_area_width
            ),
        ]

    def update(self, speed):
        if mathstrovehiclesim.globals.DEBUG:
            print(f"speed inside env: {speed}")
        # update veh_sim.globals.WHITE lines
        if not self.show_horizontal_line:
            temp_y_list = []
            if self.distance_pointer_white_lines > (
                mathstrovehiclesim.globals.WHITE_LANE_GAP + mathstrovehiclesim.globals.WHITE_LANE_HEIGHT
            ):
                self.distance_pointer_white_lines = 0
                temp_y_list.append(-mathstrovehiclesim.globals.WHITE_LANE_HEIGHT)

            for y_loc in self.white_y_loc:
                temp = y_loc + speed
                if temp <= mathstrovehiclesim.globals.HEIGHT:
                    temp_y_list.append(temp)

            self.white_y_loc = temp_y_list
        else:
            speed = 0

        # update trees
        if self.distance_pointer_trees > (mathstrovehiclesim.globals.TREES_GAP + mathstrovehiclesim.globals.TREES_WIDTH):
            self.distance_pointer_trees = 0
            tree_right = Tree(
                mathstrovehiclesim.globals.TREES_IMAGES[random.randint(0, 3)],
                mathstrovehiclesim.globals.TREES_WIDTH,
                (self.roadside_area_widths.grass_area_width, mathstrovehiclesim.globals.TREES_START_POINT),
            )
            tree_left = Tree(
                mathstrovehiclesim.globals.TREES_IMAGES[random.randint(0, 3)],
                mathstrovehiclesim.globals.TREES_WIDTH,
                (
                    mathstrovehiclesim.globals.WIDTH - self.roadside_area_widths.grass_area_width,
                    mathstrovehiclesim.globals.TREES_START_POINT,
                ),
            )
            self.trees_group.add(tree_right)
            self.trees_group.add(tree_left)

        for tree in self.trees_group:
            tree.update(speed)

        # update houses
        if self.distance_pointer_houses > (mathstrovehiclesim.globals.HOUSES_WIDTH + mathstrovehiclesim.globals.HOUSES_GAP):
            self.distance_pointer_houses = 0
            house_right = House(
                mathstrovehiclesim.globals.HOUSES_IMAGES[random.randint(0, 3)],
                mathstrovehiclesim.globals.HOUSES_WIDTH,
                (0, mathstrovehiclesim.globals.HOUSE_START_POINT),
            )
            house_left = House(
                mathstrovehiclesim.globals.HOUSES_IMAGES[random.randint(0, 3)],
                mathstrovehiclesim.globals.HOUSES_WIDTH,
                (mathstrovehiclesim.globals.WIDTH, mathstrovehiclesim.globals.HOUSE_START_POINT),
            )
            self.houses_group.add(house_right)
            self.houses_group.add(house_left)

        for house in self.houses_group:
            house.update(speed)

        # update sidewalk objects
        if self.distance_pointer_sidewalk > (
            mathstrovehiclesim.globals.SIDEWALK_OBJECTS_WIDTH
            + random.randint(
                mathstrovehiclesim.globals.SIDEWALK_OBJECTS_GAP_MIN, mathstrovehiclesim.globals.SIDEWALK_OBJECTS_GAP_MAX
            )
        ):
            self.distance_pointer_sidewalk = 0
            right_idx = random.randint(0, 7)
            left_idx = random.randint(0, 7)

            # is the object in right lane or left lane of the sidewalk?
            right_pos = random.randint(0, 1)
            left_pos = random.randint(0, 1)

            swo_right = SidewalkObject(
                mathstrovehiclesim.globals.SIDEWALK_OBJECTS_IMAGES[right_idx],
                mathstrovehiclesim.globals.SIDEWALK_OBJECTS_WIDTH,
                0 if right_idx < 4 else 1,
                (
                    get_sidewalk_x_loc(
                        mathstrovehiclesim.globals.WIDTH,
                        self.roadside_area_widths.grass_area_width,
                        mathstrovehiclesim.globals.GRASS_AREA_RATIO,
                        mathstrovehiclesim.globals.SIDEWALK_AREA_RATIO,
                        right_pos,
                    ),
                    mathstrovehiclesim.globals.SIDEWALK_OBJECTS_START_POINT,
                ),
                sidewalk_loc=right_pos,
            )
            swo_left = SidewalkObject(
                mathstrovehiclesim.globals.SIDEWALK_OBJECTS_IMAGES[left_idx],
                mathstrovehiclesim.globals.SIDEWALK_OBJECTS_WIDTH,
                0 if right_idx < 4 else 1,
                (
                    get_sidewalk_x_loc(
                        mathstrovehiclesim.globals.WIDTH,
                        self.roadside_area_widths.grass_area_width,
                        mathstrovehiclesim.globals.GRASS_AREA_RATIO,
                        mathstrovehiclesim.globals.SIDEWALK_AREA_RATIO,
                        left_pos,
                        left_side=True,
                    ),
                    mathstrovehiclesim.globals.SIDEWALK_OBJECTS_START_POINT,
                ),
                sidewalk_loc=left_pos,
            )
            self.sidewalk_group.add(swo_right)
            self.sidewalk_group.add(swo_left)

        for swo in self.sidewalk_group:
            swo.update(speed)

        # update itr_number for each object group
        self.distance_pointer_white_lines += speed
        self.distance_pointer_trees += speed
        self.distance_pointer_houses += speed
        self.distance_pointer_sidewalk += speed

    def render(self, window, show_sidewalk_objects=True):
        # re-render the road, grass and sidewalk area
        pygame.draw.rect(
            window, mathstrovehiclesim.globals.GRASS_COLOR, (0, 0, mathstrovehiclesim.globals.WIDTH, mathstrovehiclesim.globals.HEIGHT)
        )
        pygame.draw.rect(
            window,
            mathstrovehiclesim.globals.SIDEWALK_COLOR,
            (self.sidewalk_border_left, 0, self.sidewalk_border_right, mathstrovehiclesim.globals.HEIGHT),
        )
        pygame.draw.rect(
            window,
            mathstrovehiclesim.globals.ASPHALT_COLOR,
            (self.road_border_left, 0, self.road_border_right, mathstrovehiclesim.globals.HEIGHT),
        )

        # draw veh_sim.globals.WHITE/veh_sim.globals.YELLOW lines
        if not self.show_horizontal_line:
            for x_loc in self.white_x_loc:
                for y_loc in self.white_y_loc:
                    if y_loc < mathstrovehiclesim.globals.HEIGHT:
                        pygame.draw.rect(
                            window,
                            mathstrovehiclesim.globals.WHITE,
                            (
                                x_loc,
                                y_loc,
                                mathstrovehiclesim.globals.WHITE_LANE_WIDTH,
                                mathstrovehiclesim.globals.WHITE_LANE_HEIGHT,
                            ),
                        )
        else:
            for y_loc in self.horizontal_line_y_loc:
                pygame.draw.rect(
                    window,
                    mathstrovehiclesim.globals.YELLOW,
                    (
                        self.horizontal_line_x_loc,
                        y_loc,
                        mathstrovehiclesim.globals.HORIZONTAL_LANE_WIDTH,
                        mathstrovehiclesim.globals.HORIZONTAL_LANE_HEIGHT,
                    ),
                )

        # draw sidewalk objects
        if show_sidewalk_objects:
            self.sidewalk_group.draw(window)

        # draw trees
        self.trees_group.draw(window)

        # draw houses
        self.houses_group.draw(window)

    def reset(self):
        self.distance_pointer_white_lines = 0


class Tree(pygame.sprite.Sprite):
    def __init__(self, p_image, WIDTH, p_bottom_pos=(0, 0)):
        pygame.sprite.Sprite.__init__(self)  # must do this
        self.image = pygame.transform.scale(
            pygame.image.load(p_image).convert_alpha(), (WIDTH, WIDTH)
        )
        self.rect = (
            self.image.get_rect()
        )  # rectangle that enclose the sprite..defines how wide and tall
        self.rect.centerx = p_bottom_pos[0]
        self.rect.bottom = p_bottom_pos[1]

    def update(self, p_spd):
        self.vy = p_spd
        self.rect.y += self.vy
        if self.rect.top >= mathstrovehiclesim.globals.HEIGHT:
            self.kill()


class House(pygame.sprite.Sprite):
    def __init__(self, p_image, WIDTH, p_bottom_pos=(0, 0)):
        pygame.sprite.Sprite.__init__(self)  # must do this
        self.image = pygame.transform.scale(
            pygame.image.load(p_image).convert_alpha(), (WIDTH, WIDTH)
        )
        self.rect = (
            self.image.get_rect()
        )  # rectangle that enclose the sprite..defines how wide and tall
        self.rect.centerx = p_bottom_pos[0]
        self.rect.bottom = p_bottom_pos[1]

    def update(self, p_spd):
        self.vy = p_spd
        self.rect.y += self.vy
        if self.rect.top >= mathstrovehiclesim.globals.HEIGHT:
            self.kill()


class SidewalkObject(pygame.sprite.Sprite):
    def __init__(self, p_image, WIDTH, obj_type, p_bottom_pos=(0, 0), sidewalk_loc=0):
        pygame.sprite.Sprite.__init__(self)  # must do this
        self.image = pygame.image.load(p_image).convert_alpha()
        h_width, h_height = self.image.get_size()
        self.object_type = 0
        if obj_type == 0:  # pedestrian
            self.image = pygame.transform.scale(
                pygame.image.load(p_image).convert_alpha(),
                (WIDTH * 1.2, WIDTH * (h_height / h_width) * 1.3),
            )  # scale the image based on given veh_sim.globals.WIDTH
        else:  # bike
            self.object_type = 1
            self.image = pygame.transform.scale(
                pygame.image.load(p_image).convert_alpha(),
                (WIDTH, WIDTH * (h_height / h_width)),
            )  # scale the image based on given veh_sim.globals.WIDTH

        self.sidewalk_loc = 0
        if sidewalk_loc == 1:  # check that object is in which side of the sidewalk
            self.sidewalk_loc = 1
            self.image = pygame.transform.rotate(
                self.image, 180
            )  # because they should be in the opposite direction

        self.rect = (
            self.image.get_rect()
        )  # rectangle that enclose the sprite..defines how wide and tall
        self.rect.centerx = p_bottom_pos[0]
        self.rect.bottom = p_bottom_pos[1]

    def update(self, p_spd):
        ratio = 1
        if self.sidewalk_loc == 1:
            ratio = -1
        if self.object_type == 0:
            self.vy = p_spd + mathstrovehiclesim.globals.PEDESTRIAN_SPEED * ratio
        else:
            self.vy = p_spd + mathstrovehiclesim.globals.BIKE_SPEED * ratio
        self.rect.y += self.vy
        if self.rect.top >= mathstrovehiclesim.globals.HEIGHT:
            self.kill()
