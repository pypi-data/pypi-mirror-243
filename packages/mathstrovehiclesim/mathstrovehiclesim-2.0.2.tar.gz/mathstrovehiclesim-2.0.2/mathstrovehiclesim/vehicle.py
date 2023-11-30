import math

import pygame
from easydict import EasyDict as edict

import mathstrovehiclesim.globals

from .utils import get_lane, get_lane_coordinate, is_lane_available, is_on_screen


class Vehicle(pygame.sprite.Sprite):
    def __init__(self, p_image, lane_borders, p_bottom_pos=(0,0), p_init_lat_spd=0, p_init_lng_spd=0, p_max_spd=30, is_motorcycle=False, set_top=False):
        self.lane_borders = lane_borders
        # global target_vy
        # configure image for sprite
        pygame.sprite.Sprite. __init__(self)  # must do this
        self.image_path = p_image
        self.image = pygame.image.load(p_image).convert_alpha()
        h_width, h_height = self.image.get_size()

        # change the size of object to fit on the road lanes based on its type
        self.is_motorcycle = is_motorcycle
        if is_motorcycle:
            self.image = pygame.transform.scale(self.image, (mathstrovehiclesim.globals.ROAD_LANE_WIDTH * 0.3, mathstrovehiclesim.globals.ROAD_LANE_WIDTH * (h_height / h_width) * 0.3))  # scale the image based on given veh_sim.globals.WIDTH
        else:
            self.image = pygame.transform.scale(self.image, (mathstrovehiclesim.globals.ROAD_LANE_WIDTH * 0.6, mathstrovehiclesim.globals.ROAD_LANE_WIDTH * (h_height / h_width) * 0.6))  # scale the image based on given veh_sim.globals.WIDTH

        # save current rect position of the object
        self.rect = self.image.get_rect()  # rectangle that enclose the sprite..defines how wide and tall

        # initialize starting position
        self.rect.centerx = p_bottom_pos[0]
        self.rect.bottom = p_bottom_pos[1]
        if set_top:
            self.rect.top = p_bottom_pos[1]

        # initialize starting speed to zero
        self.vx = p_init_lat_spd
        self.vy = p_init_lng_spd
        self.max_vy = p_max_spd

        self.steering_wheel_angle = 0
        self.turning_speed = 50  # Increase this value to make the circular motion smoother
        self.turning_radius = 0
        self.initial_x = self.rect.centerx  # Store the initial position in case of straight movement
        self.initial_y = self.rect.centery
        self.angle_direction = 1
        self.angle = 0
        self.direction = 1
        self.initial_angle = 0
        self.initial_radius = 0

        self.rot_img = []
        self.min_angle = 1
        for i in range(360):
            # This rotation has to match the angle in radians later
            # So offet the angle (0 degrees = "north") by 90° to be angled 0-radians (so 0 rad is "east")
            rotated_image = pygame.transform.rotozoom(self.image, (i * self.min_angle), 1)
            self.rot_img.append(rotated_image)

    # --------------------------- GET INFO METHODS --------------------------

    def get_speed(self):
        return self.vy

    def get_rect_position(self):
        return self.rect

    def get_bottom_position(self):
        return self.rect.centerx, self.rect.bottom

    def get_lane(self):
        return get_lane(self.rect.centerx, self.lane_borders)

    def get_image_path(self):
        return self.image_path

    def get_size(self):
        return self.image.get_size()

    def get_steering_wheel_angle(self):
        return self.steering_wheel_angle

    # ---------------- SET/ACTION METHODS --------------------
    def set_speed(self, p_spd):
        self.vy = int(p_spd)

    def go_to_lane(self, p_lane_num):
        self.rect.centerx = get_lane_coordinate(p_lane_num, self.lane_borders)

    def speed_up(self, p_spd_inc=1):
        if self.vy < self.max_vy:
            self.vy += int(p_spd_inc)
            if self.vy > self.max_vy:
                self.vy = self.max_vy

    def speed_down(self, p_spd_inc=1):
        self.vy -= int(p_spd_inc)

    def stop(self):
        self.vy = 0

    def headlight_on(self):
        self.image = pygame.image.load(mathstrovehiclesim.globals.HOST_VEHICLE_IMAGE_HEADLIGHT_ON).convert_alpha()
        h_width, h_height = self.image.get_size()
        self.image = pygame.transform.scale(self.image, (mathstrovehiclesim.globals.ROAD_LANE_WIDTH * 0.6, mathstrovehiclesim.globals.ROAD_LANE_WIDTH * (h_height / h_width) * 0.6))  # scale the image based on given veh_sim.globals.WIDTH

    def headlight_off(self):
        self.image = pygame.image.load(mathstrovehiclesim.globals.HOST_VEHICLE_IMAGES).convert_alpha()
        h_width, h_height = self.image.get_size()
        self.image = pygame.transform.scale(self.image, (mathstrovehiclesim.globals.ROAD_LANE_WIDTH * 0.6, mathstrovehiclesim.globals.ROAD_LANE_WIDTH * (h_height / h_width) * 0.6))  # scale the image based on given veh_sim.globals.WIDTH

    def move_left(self):
        # returns False if the vehicle goes off the road
        off_road = False
        if self.is_left_lane_available():
            self.go_to_lane(self.get_lane() - 1)
        else:
            off_road = True
        return off_road

    def move_right(self):
        # returns False if the vehicle goes off the road
        off_road = False
        if self.is_right_lane_available():
            self.go_to_lane(self.get_lane() + 1)
        else:
            off_road = True
        return off_road

    # parallel parking methods

    def turn_right(self, degree_step=1):
        self.initial_angle = self.angle
        self.initial_radius = self.turning_radius
        self.steering_wheel_angle = max(self.steering_wheel_angle - degree_step, -mathstrovehiclesim.globals.MAX_STEERING_ANGLE)

    def turn_left(self, degree_step=1):
        self.initial_angle = self.angle
        self.initial_radius = self.turning_radius
        self.steering_wheel_angle = min(self.steering_wheel_angle + degree_step, +mathstrovehiclesim.globals.MAX_STEERING_ANGLE)

    def forward(self, speed=5):
        self.direction = 1

        if self.steering_wheel_angle == 0:
            # Update initial position when moving straight
            self.initial_x = self.rect.centerx
            self.initial_y = self.rect.centery

            # Move the car in a straight line without turning
            self.rect.centerx += self.direction * speed * math.sin(math.radians(self.angle))
            self.rect.centery -= self.direction * speed * math.cos(math.radians(self.angle))
        else:
            # Calculate turning radius based on steering angle and forward speed
            self.turning_radius = mathstrovehiclesim.globals.TURNING_RADIUS_MULTIPLIER / math.radians(self.steering_wheel_angle)

            # Update rotation angle
            rotation_angle = self.turning_speed / abs(self.turning_radius)
            if mathstrovehiclesim.globals.DEBUG:
                print(f"direct - initial angle: {math.degrees(self.initial_angle)} - angle: {math.degrees(self.angle)} - rotation angle: {rotation_angle} -  radius: {self.turning_radius} - steering: {self.steering_wheel_angle}")

            if self.initial_angle == 0:
                if self.steering_wheel_angle > 0:
                    self.angle -= rotation_angle
                    self.rect.centerx = self.initial_x + self.turning_radius * math.cos(math.radians(self.angle)) - self.turning_radius
                    self.rect.centery = self.initial_y + self.turning_radius * math.sin(math.radians(self.angle))
                else:
                    self.angle -= rotation_angle
                    self.rect.centerx = self.initial_x + self.turning_radius * math.cos(math.radians(self.angle)) - self.turning_radius
                    self.rect.centery = self.initial_y - self.turning_radius * math.sin(math.radians(self.angle))
            else:
                self.angle += rotation_angle
                self.rect.centerx = self.initial_x + self.turning_radius * math.cos(math.radians(self.angle))  # - self.turning_radius * math.cos(math.radians(self.initial_angle))
                self.rect.centery = self.initial_y + self.turning_radius * math.sin(math.radians(self.angle))  # - self.turning_radius * math.sin(math.radians(self.initial_angle))

    def reverse(self, speed=5):
        self.direction = -1
        if self.steering_wheel_angle == 0:
            # Update initial position when moving straight
            self.initial_x = self.rect.centerx
            self.initial_y = self.rect.centery

            # Move the car in a straight line without turning

            if self.angle != 0:
                self.rect.centerx += self.direction * speed * math.sin(math.radians(-self.angle))
                self.rect.centery -= self.direction * speed * math.cos(math.radians(-self.angle))
            else:
                self.rect.centerx += self.direction * speed * math.sin(math.radians(self.angle))
                self.rect.centery -= self.direction * speed * math.cos(math.radians(self.angle))

        else:
            # Calculate turning radius based on steering angle and forward speed
            self.turning_radius = mathstrovehiclesim.globals.TURNING_RADIUS_MULTIPLIER / math.radians(self.steering_wheel_angle)

            # Update rotation angle
            rotation_angle = self.turning_speed / abs(self.turning_radius)
            if mathstrovehiclesim.globals.DEBUG:
                print(f"reverse - angle: {math.degrees(self.angle)} - rotation angle: {rotation_angle} -  radius: {self.turning_radius} - steering: {self.steering_wheel_angle}")
            if self.initial_angle == 0:
                if self.steering_wheel_angle > 0:
                    self.angle += rotation_angle
                    self.rect.centerx = self.initial_x + self.turning_radius * math.cos(math.radians(self.angle)) - self.turning_radius + self.initial_radius
                    self.rect.centery = self.initial_y + self.turning_radius * math.sin(math.radians(self.angle))
                else:
                    self.angle += rotation_angle
                    self.rect.centerx = self.initial_x + self.turning_radius * math.cos(math.radians(self.angle)) - self.turning_radius + self.initial_radius
                    self.rect.centery = self.initial_y - self.turning_radius * math.sin(math.radians(self.angle))
            else:
                if self.steering_wheel_angle == 0:
                    self.angle += rotation_angle
                    self.rect.centerx = self.initial_x + self.turning_radius * math.cos(math.radians(self.angle)) - self.turning_radius + self.initial_radius
                    self.rect.centery = self.initial_y + self.turning_radius * math.sin(math.radians(self.angle))
                else:
                    self.angle -= rotation_angle
                    self.rect.centerx = self.initial_x + self.turning_radius * math.cos(math.radians(self.angle)) - self.turning_radius * math.cos(math.radians(self.initial_angle))
                    self.rect.centery = self.initial_y - self.turning_radius * math.sin(math.radians(self.angle)) + self.turning_radius * math.sin(math.radians(self.initial_angle))

    # renders the host vehicle on the display

    def parrallel_parking_render(self, screen):
        if self.initial_angle == 0:
            if self.direction == 1:
                if self.steering_wheel_angle > 0:
                    self.angle_direction = -1
                else:
                    self.angle_direction = 1
            else:
                if self.steering_wheel_angle > 0:
                    self.angle_direction = -1
                else:
                    self.angle_direction = 1

        rotated_car = pygame.transform.rotate(self.image, self.angle_direction * self.angle)

        car_rect = rotated_car.get_rect(center=(self.rect.centerx, self.rect.centery))
        screen.blit(rotated_car, car_rect.topleft)

    # ---------------------- SENSOR METHODS -----------------------

    def is_visible(self):
        return is_on_screen(self.rect.centerx, self.rect.top)

    def is_left_lane_available(self):
        return is_lane_available(self.rect.centerx, self.lane_borders, "left")

    def is_right_lane_available(self):
        return is_lane_available(self.rect.centerx, self.lane_borders, "right")

    def sensing(self, targets):
        inf = float('inf')
        perception = edict({
            "forward_target":{
                "vy": inf,
                "dist": inf
            },
            "left_forward_target":{
                "vy": inf,
                "dist": inf
            },
            "right_forward_target":{
                "vy": inf,
                "dist": inf
            },
            "collision": False,
            "running":True,
            "host_speed":self.get_speed(),
            "host_lane":self.get_lane(),
            "left_lane_available":self.is_left_lane_available(),
            "right_lane_available":self.is_right_lane_available()
        })

        for target in targets:
            # determine collision
            if self.rect.colliderect(target):
                perception["running"] = False
                perception.collision = True

            # foward perception
            if target.is_visible() and target.get_lane() == self.get_lane():
                # check if closest forward vehicle
                dist = self.rect.top - target.rect.bottom
                if dist < perception.forward_target.dist:
                    perception.forward_target.dist = dist
                    perception.forward_target.vy = target.vy

            # left perception
            if self.is_left_lane_available():
                if target.is_visible() and target.get_lane() == self.get_lane() - 1:
                    # check if closest left vehicle
                    dist = self.rect.top - target.rect.bottom
                    if dist < perception.left_forward_target.dist:
                        perception.left_forward_target.dist = dist
                        perception.left_forward_target.vy = target.vy

            # right perception
            if self.is_right_lane_available():
                if target.is_visible() and target.get_lane() == self.get_lane() + 1:
                    # check if closest right vehicle
                    dist = self.rect.top - target.rect.bottom
                    if dist < perception.right_forward_target.dist:
                        perception.right_forward_target.dist = dist
                        perception.right_forward_target.vy = target.vy

        return perception
