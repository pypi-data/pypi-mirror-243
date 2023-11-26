import random

import pygame

import mathstrovehiclesim.globals

from .traffic import SingleTargetAhead


class TrafficRouter:
    def __init__(self, lane_borders, road_borders, num_lanes, gap_offset=0, speed_range=[3, 8],
                 traffic_object_start_point=0, has_speed_change=True, speed_change_counter_range=[200, 700], new_traffic_object_probability=0.3):
        # initialize the router parameters
        self.lane_borders = lane_borders
        self.road_borders = road_borders
        self.num_lanes = num_lanes
        self.speed_range = speed_range
        self.gap_offset = gap_offset
        self.traffic_object_start_point = traffic_object_start_point
        self.has_speed_change = has_speed_change
        self.speed_change_counter_range = speed_change_counter_range
        # initialize distance for changing speed randomly
        self.speed_change_selected_counter = random.randint(self.speed_change_counter_range[0], self.speed_change_counter_range[1])
        # create random speed for each lane
        self.lanes_speed = [random.randint(self.speed_range[0], self.speed_range[1]) for i in range(0, self.num_lanes)]

        # setup traffic group
        self.targets = pygame.sprite.Group()
        self.distance_pointer_list = [0] * self.num_lanes
        self.gap_size_list = [0] * self.num_lanes
        self.new_traffic_object_probability = new_traffic_object_probability

    def generate_random_traffic_object(self, lane_number):
        # select an image randomly
        image_idx = random.randint(0,4)

        # check if selected image is motorcycle
        is_motorcycle = image_idx > 3

        # create new traffic object
        new_target = SingleTargetAhead(mathstrovehiclesim.globals.VEHICLE_IMAGES[image_idx], self.lane_borders,
                                       p_bottom_pos=(0,self.traffic_object_start_point),
                                       p_init_lng_spd=self.lanes_speed[lane_number], is_motorcycle=is_motorcycle, lane=lane_number)

        # get the veh_sim.globals.HEIGHT of the vehicle to find the gap_size for adding another traffic object
        new_target_width, new_target_height = new_target.get_size()
        self.gap_size_list[lane_number] = new_target_height + self.gap_offset + 10  # +10 to make sure there is at least a small gap between two consecutive objects
        self.targets.add(new_target)

    def change_lanes_speed(self, host_speed):
        # create new random speed array
        self.lanes_speed = [random.randint(self.speed_range[0], self.speed_range[1]) for i in range(0, self.num_lanes)]
        if mathstrovehiclesim.globals.DEBUG:
            print(f"new speed: {self.lanes_speed}")

        # change the speed of previous traffic objects and update them
        for target in self.targets:
            # get previous item information
            lane_idx = target.get_lane()
            target.set_speed(self.lanes_speed[lane_idx])
            target.update(host_speed)

    def update(self, host_speed):
        # for the distance pointer we should consider the fastest traffic object (as it would be in the screen for longer time)
        for i in range(0, self.num_lanes):
            self.distance_pointer_list[i] += host_speed - self.lanes_speed[i]

            # if the specified gap size is travelled, add new traffic object
            if self.distance_pointer_list[i] >= self.gap_size_list[i]:
                self.distance_pointer_list[i] = 0

                # add new traffic object with random probability
                temp_random = random.random()
                if temp_random < self.new_traffic_object_probability:
                    self.generate_random_traffic_object(i)

        # if the specified distance size is travelled, change lanes speed
        if self.speed_change_selected_counter <= 0 and self.has_speed_change:
            # select a random distance for next speed change period
            self.speed_change_selected_counter = random.randint(self.speed_change_counter_range[0], self.speed_change_counter_range[1])
            if mathstrovehiclesim.globals.DEBUG:
                print(f"new selected speed counter: {self.speed_change_selected_counter}")
            self.change_lanes_speed(host_speed)
        else:
            self.speed_change_selected_counter -= 1
            # update would occur inside change_lanes_speed whenever it is being called as it is more efficient
            for target in self.targets:
                target.update(host_speed)

        return self.targets, self.lanes_speed

    def render(self, screen):
        self.targets.draw(screen)
