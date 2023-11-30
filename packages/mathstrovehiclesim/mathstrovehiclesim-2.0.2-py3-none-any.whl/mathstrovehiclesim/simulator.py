import math
import random
import time

import cv2
import pygame

import mathstrovehiclesim.globals

from .environment import Env
from .host_vehicle import HostVehicle
from .traffic import SingleTargetAhead
from .traffic_router import TrafficRouter
from .utils import get_lane_borders

pygame.font.init()


class Simulator:
    def __init__(self, number_of_lanes, speed_limit, initial_speed=27, show_parameter_panel=True, show_odometer_panel=True, size="medium"):
        mathstrovehiclesim.globals.set_screen_size(size=size)
        self.screen = pygame.display.set_mode((mathstrovehiclesim.globals.WIDTH,mathstrovehiclesim.globals.HEIGHT))

        pygame.display.set_caption(mathstrovehiclesim.globals.CAPTION)

        self.num_lanes = number_of_lanes
        # create sprites
        self.env = Env(number_of_lanes, show_horizontal_line=False)
        self.road_borders = self.env.get_sidwalk_road_borders()
        self.lane_borders = get_lane_borders(self.road_borders[0], num_lane=self.num_lanes)
        self.show_parameter_panel = show_parameter_panel

        # ----------------------------------- SETUP TRAFFIC ---------------------------------
        # speed range of traffic objects
        low_speed = math.floor(0.7 * speed_limit)
        high_speed = math.floor(0.9 * speed_limit)

        # router class needs below parameters
        # gap_offset: offset for gap between two adjacent traffic objects (Y axis)
        # traffic_object_start_point: start point for adding new traffic objects (Y axis)
        # has_speed_change: should change the speed of traffic objects or not
        # speed_change_gap_low and speed_change_gap_high: range for spent time to change the speed of traffic objects
        self.traffic_router = TrafficRouter(self.lane_borders, self.road_borders, self.num_lanes,
                                            speed_range=[low_speed, high_speed], gap_offset=0,
                                            traffic_object_start_point=0, has_speed_change=True,
                                            new_traffic_object_probability=0.33)

        # -------------------------------- SETUP HOST VEHICLE ---------------------------------
        self.host_vehicle = HostVehicle(mathstrovehiclesim.globals.HOST_VEHICLE_IMAGES, self.lane_borders,
                                        p_bottom_pos=(0,mathstrovehiclesim.globals.HEIGHT),
                                        p_init_lng_spd=initial_speed, p_max_spd=speed_limit, is_motorcycle=False, lane=1)
        self.host_odometer_value = 0
        self.show_odometer_panel = show_parameter_panel
        # initialize scenario variables
        self.running = True
        self.perception = {}
        self.lanes_speed = [0] * self.num_lanes
        self.clock = pygame.time.Clock()
        self.quit_game = False
        self.failure_message = ""

    def step(self, action="", user_given_odometer_value=0):

        if self.running:

            # update host vehicle based on user input
            self.host_vehicle.update(action)

            # update the environment
            self.env.update(speed=self.host_vehicle.get_speed())

            # manage traffic objects (we should provide host vehicle lane in each step to manage the speed of that lane by specified step)
            targets, self.lanes_speed = self.traffic_router.update(host_speed=self.host_vehicle.get_speed())

            # get the self.perception from host vehicle
            self.perception = self.host_vehicle.sensing(targets)

            # update odometer value
            self.host_odometer_value += self.host_vehicle.get_speed()

            # check the possible collision
            self.running = self.perception.running

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.quit_game = True
                    self.perception.running = False
                    pygame.quit()
                    exit()

            self.render(user_given_odometer_value=user_given_odometer_value)
            return self.perception
        else:
            self.render(user_given_odometer_value=user_given_odometer_value)
            return {"running":False}

    def render(self, user_given_odometer_value=0):
        if not self.quit_game:
            if self.running:
                self.env.render(self.screen)

                # render the traffic objects
                self.traffic_router.render(self.screen)

                # render host vehicle
                self.host_vehicle.render(self.screen)

                if self.show_parameter_panel:

                    data = [
                        f"host_speed: {self.perception.host_speed}",
                        f"host_lane: {self.perception.host_lane}",
                        "",
                        f"forward dist: {self.perception.forward_target.dist}",
                        f"forward speed: {self.perception.forward_target.vy}",
                        "",
                        f"left_lane_available: {self.perception.left_lane_available}",
                        f"left dist: {self.perception.left_forward_target.dist}",
                        f"left speed: {self.perception.left_forward_target.vy}",
                        "",
                        f"right_lane_available: {self.perception.right_lane_available}",
                        f"right dist: {self.perception.right_forward_target.dist}",
                        f"right speed: {self.perception.right_forward_target.vy}",
                        "",
                        f"lanes speed: {self.lanes_speed}"
                    ]

                pygame.draw.rect(self.screen, mathstrovehiclesim.globals.YELLOW, pygame.Rect(mathstrovehiclesim.globals.PARAMETER_PANEL_YELLOW_RECT_START_X, mathstrovehiclesim.globals.PARAMETER_PANEL_YELLOW_RECT_START_y, mathstrovehiclesim.globals.PARAMETER_PANEL_YELLOW_RECT_WIDTH, mathstrovehiclesim.globals.PARAMETER_PANEL_YELLOW_RECT_HEIGHT))
                pygame.draw.rect(self.screen, mathstrovehiclesim.globals.BLACK, pygame.Rect(mathstrovehiclesim.globals.PARAMETER_PANEL_BLACK_RECT_START_X, mathstrovehiclesim.globals.PARAMETER_PANEL_BLACK_RECT_START_y, mathstrovehiclesim.globals.PARAMETER_PANEL_BLACK_RECT_WIDTH, mathstrovehiclesim.globals.PARAMETER_PANEL_BLACK_RECT_HEIGHT))
                for idx in range(len(data)):
                    font = pygame.font.Font('freesansbold.ttf', mathstrovehiclesim.globals.PANEL_FONT_SIZE)
                    text = font.render(data[idx], True, mathstrovehiclesim.globals.WHITE)
                    self.screen.blit(text, (mathstrovehiclesim.globals.PARAMETER_PANEL_TEXT_START_X, mathstrovehiclesim.globals.PARAMETER_PANEL_BLACK_RECT_START_y + mathstrovehiclesim.globals.PADDING + idx * mathstrovehiclesim.globals.PARAMETER_PANEL_TEXT_HEIGHT))

            if self.show_odometer_panel:
                pygame.draw.rect(self.screen, mathstrovehiclesim.globals.YELLOW, pygame.Rect(mathstrovehiclesim.globals.ODOMETER_PANEL_START_POINT, mathstrovehiclesim.globals.ODOMETER_PANEL_START_POINT, mathstrovehiclesim.globals.ODOMETER_PANEL_WIDTH + 2 * mathstrovehiclesim.globals.ODOMETER_PANEL_BORDER_WIDTH, mathstrovehiclesim.globals.ODOMETER_PANEL_HEIGHT + 2 * mathstrovehiclesim.globals.ODOMETER_PANEL_BORDER_WIDTH))
                pygame.draw.rect(self.screen, mathstrovehiclesim.globals.BLACK, pygame.Rect(mathstrovehiclesim.globals.ODOMETER_PANEL_START_POINT + mathstrovehiclesim.globals.ODOMETER_PANEL_BORDER_WIDTH, mathstrovehiclesim.globals.ODOMETER_PANEL_START_POINT + mathstrovehiclesim.globals.ODOMETER_PANEL_BORDER_WIDTH, mathstrovehiclesim.globals.ODOMETER_PANEL_WIDTH, mathstrovehiclesim.globals.ODOMETER_PANEL_HEIGHT))
                font = pygame.font.Font('freesansbold.ttf', mathstrovehiclesim.globals.PANEL_FONT_SIZE)
                text = font.render("ODOMETER PANEL", True, mathstrovehiclesim.globals.YELLOW)
                self.screen.blit(text, (mathstrovehiclesim.globals.ODOMETER_PANEL_START_POINT * 2, mathstrovehiclesim.globals.ODOMETER_PANEL_START_POINT * 2))
                font = pygame.font.Font('freesansbold.ttf', mathstrovehiclesim.globals.ODOMETER_FONT_SIZE)
                text = font.render(f"USER VALUE: {user_given_odometer_value:,}", True, mathstrovehiclesim.globals.WHITE)
                self.screen.blit(text, (mathstrovehiclesim.globals.ODOMETER_PANEL_START_POINT * 2, mathstrovehiclesim.globals.ODOMETER_PANEL_START_POINT * 2 + mathstrovehiclesim.globals.ODOMETER_PANEL_HEIGHT * 1 / 3))
                text = font.render(f"REAL VALUE: {self.host_odometer_value:,}", True, mathstrovehiclesim.globals.WHITE)
                self.screen.blit(text, (mathstrovehiclesim.globals.ODOMETER_PANEL_START_POINT * 2, mathstrovehiclesim.globals.ODOMETER_PANEL_START_POINT * 2 + mathstrovehiclesim.globals.ODOMETER_PANEL_HEIGHT * 2 / 3))

                pygame.display.flip()
            else:
                # draw/render
                self.env.render(self.screen)
                font = pygame.font.Font('freesansbold.ttf', mathstrovehiclesim.globals.FONT_SIZE)
                text = font.render('SIMULATION ENDED', True, mathstrovehiclesim.globals.GREEN, mathstrovehiclesim.globals.BLUE)
                text_rect = text.get_rect(center=(mathstrovehiclesim.globals.WIDTH / 2, mathstrovehiclesim.globals.HEIGHT / 2))
                self.screen.blit(text, text_rect)
                pygame.display.flip()

            pygame.display.update()
            self.clock.tick(mathstrovehiclesim.globals.FPS)


class TrafficSignInterpretionSimulator:
    def __init__(self, background_address=mathstrovehiclesim.globals.LANDING_PAGE_BACKGROUND, model=None, speed_limit=45, initial_speed=27, size="medium", development_mode=False):
        mathstrovehiclesim.globals.set_screen_size(size=size)
        self.screen = pygame.display.set_mode((mathstrovehiclesim.globals.WIDTH,mathstrovehiclesim.globals.HEIGHT))

        pygame.display.set_caption(mathstrovehiclesim.globals.CAPTION)
        self.num_lanes = 2
        # create sprites
        self.env = Env(self.num_lanes, show_horizontal_line=False)
        self.road_borders = self.env.get_sidwalk_road_borders()
        self.lane_borders = get_lane_borders(self.road_borders[0], num_lane=self.num_lanes)

        # -------------------------------- SETUP HOST VEHICLE ---------------------------------
        self.host_vehicle = HostVehicle(mathstrovehiclesim.globals.HOST_VEHICLE_IMAGES, self.lane_borders,
                                        p_bottom_pos=(0,mathstrovehiclesim.globals.HEIGHT),
                                        p_init_lng_spd=initial_speed, p_max_spd=speed_limit, is_motorcycle=False, lane=1)
        self.host_odometer_value = 0
        # initialize scenario variables
        self.running = True
        self.perception = {}
        self.lanes_speed = [0] * self.num_lanes
        self.clock = pygame.time.Clock()
        self.quit_game = False

        # traffic sign related parameters
        self.current_step = 0
        self.step_threshold = 20
        self.traffic_sign_data = mathstrovehiclesim.globals.STEMHACK_TS_DATA
        for k in self.traffic_sign_data.keys():
            self.traffic_sign_data[k].images = [f"{mathstrovehiclesim.globals.STEMHACK_IMAGES_DIR}{k}/{i}.jpg" for i in range(0, mathstrovehiclesim.globals.STEMHACK_IMAGES_NUMBER)]
            self.traffic_sign_data[k].correctly_classified = 0

        # check number of features in the model
        self.n_features = -1
        if model:
            self.n_features = len(model.feature_importances_)
        # select first sign to show
        temp_type_idx = random.randint(0, len(self.traffic_sign_data) - 1)
        selected_type = list(self.traffic_sign_data)[temp_type_idx]
        temp_image_idx = random.randint(0, len(self.traffic_sign_data[selected_type].images) - 1)
        selected_image = self.traffic_sign_data[selected_type].images[temp_image_idx]
        self.traffic_sign_data[selected_type].images.remove(selected_image)
        # print(selected_type)
        self.previous_type = selected_type  # to make sure we don't show same image consecutively
        self.previous_image = selected_image
        self.signs_finished = False
        self.number_of_show_signs = 0

        self.headlight_on = False
        self.show_blank = True
        self.development_mode = development_mode
        self.model_accuracy_score = 0
        self.number_of_correct_preditions = 0
        self.required_type = ""
        self.required_action = ""
        self.update_accuracy = False
        self.user_previous_action = ""
        self.control_code_score = 0
        self.frame_number = 0

        self.show_landing_page = True
        self.background_address = background_address

        self.sign_start_x = self.env.roadside_area_widths['grass_area_width']

        # self.font = pygame.font.Font(None, mathstrovehiclesim.globals.STEMHACK_PANEL_FONT_SIZE)
        self.panel_scale = mathstrovehiclesim.globals.WIDTH/1100
        self.font = pygame.font.SysFont("Courier New", int(12*self.panel_scale))

        # initialize panel background image
        panel_background = pygame.image.load(mathstrovehiclesim.globals.PANEL_BACKGROUND).convert_alpha()
        bkg_width, bkg_height = panel_background.get_size()
        self.panel_background = pygame.transform.scale(panel_background, (int(bkg_width*self.panel_scale), int(bkg_height*self.panel_scale)))

    def step(self, action="", user_type=''):

        # calculate accuracy score

        if self.update_accuracy:
            print(f"required type: {self.required_type} - given type: {user_type}")
            if self.required_type == user_type:
                self.number_of_correct_preditions += 1
                self.traffic_sign_data[self.required_type].correctly_classified += 1
            self.model_accuracy_score = (self.number_of_correct_preditions / self.number_of_show_signs) * 100
            self.update_accuracy = False

        # calculate control score
        host_speed = self.host_vehicle.get_speed()
        right_lane_available = self.host_vehicle.is_right_lane_available()
        left_lane_available = self.host_vehicle.is_left_lane_available()
        if user_type == "school-zone":
            if host_speed > 20:
                self.required_action = "speed_down"
            elif host_speed < 20:
                self.required_action = "speed_up"
            else:
                self.required_action = ""
        elif user_type == "keep-right":
            if right_lane_available and self.user_previous_action != "shift_right":
                self.required_action = "shift_right"
            else:
                self.required_action = ""
        elif user_type == "keep-left":
            if left_lane_available and self.user_previous_action != "shift_left":
                self.required_action = "shift_left"
            else:
                self.required_action = ""
        elif user_type == "stop":
            self.required_action = "stop"
        elif user_type == "speed-limit":
            if host_speed > 40:
                self.required_action = "speed_down"
            elif host_speed < 40:
                self.required_action = "speed_up"
            else:
                self.required_action = ""
        elif user_type == "headlights-on":
            self.required_action = "headlight_on"
        elif user_type == "headlights-off":
            self.required_action = "headlight_off"
        else:
            self.required_action = ""

        self.user_previous_action = action

        self.frame_number += 1
        if self.required_action == action:
            self.control_code_score += 1

        # print(f"required type: {self.required_type} - given type: {user_type} - required action: {self.required_action} - given action: {action} - number: {self.number_of_show_signs} - update acc: {self.update_accuracy}")

        # show landpage if necessary
        while self.show_landing_page:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.quit_game = True
                    self.perception.running = False
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    if (mathstrovehiclesim.globals.WIDTH // 2 - 100) <= mouse[0] <= ((mathstrovehiclesim.globals.WIDTH + mathstrovehiclesim.globals.TRAFFIC_SIGN_WIDTH) // 2 + 100) and (mathstrovehiclesim.globals.HEIGHT // 2 - 50) <= mouse[1] <= (mathstrovehiclesim.globals.HEIGHT // 2 + 50):
                        self.show_landing_page = False
            self.render(user_action="", user_type="")

        if self.running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.quit_game = True
                    self.perception.running = False
                    pygame.quit()
                    exit()

            self.host_vehicle.update(action)

            # update the environment
            self.env.update(speed=self.host_vehicle.get_speed())

            # get the self.perception from host vehicle
            self.perception = self.host_vehicle.sensing([])

            # update odometer value
            self.host_odometer_value += self.host_vehicle.get_speed()

            # check the possible collision
            self.running = self.perception.running and (not self.host_vehicle.off_road_left) and (not self.host_vehicle.off_road_right)
            self.perception.running = self.running

            self.render(action, user_type)

            if self.development_mode:
                return self.perception, self.required_type
            else:
                image = cv2.imread(self.previous_image)
                if self.show_blank:
                    image = None

                return self.perception, image
        else:
            return {"running":False}, ""

    def render(self, user_action, user_type):
        if self.show_landing_page:
            bg_image = pygame.image.load(self.background_address).convert_alpha()
            bg_image = pygame.transform.scale(bg_image, (mathstrovehiclesim.globals.WIDTH ,mathstrovehiclesim.globals.HEIGHT))
            bg_image_rect = bg_image.get_rect()
            # print(bg_image_rect)
            bg_image_rect.center = mathstrovehiclesim.globals.WIDTH // 2 , mathstrovehiclesim.globals.HEIGHT // 2
            self.screen.blit(bg_image, bg_image_rect)

            start_button = pygame.image.load(mathstrovehiclesim.globals.START_BUTTON_PATH).convert_alpha()
            # start_button = pygame.transform.scale(start_button, (mathstrovehiclesim.globals.WIDTH * 0.25,mathstrovehiclesim.globals.WIDTH * 0.25 * start_button.get_height() / start_button.get_width()))
            start_image_rect = start_button.get_rect()
            start_image_rect.center = mathstrovehiclesim.globals.WIDTH // 2 , mathstrovehiclesim.globals.HEIGHT // 2
            self.screen.blit(start_button, start_image_rect)

            pygame.display.flip()
        else:
            if self.running:
                self.env.render(self.screen)

                # render host vehicle
                self.host_vehicle.render(self.screen)

                # traffic sign
                if self.current_step == self.step_threshold:

                    if self.show_blank:
                        self.show_blank = False

                        # now show blank is off and we should select show time for previous sign
                        self.step_threshold = random.randint(
                            self.traffic_sign_data[self.previous_type].min_show_steps,
                            self.traffic_sign_data[self.previous_type].max_show_steps)
                        self.number_of_show_signs += 1
                        self.update_accuracy = True

                    else:
                        self.show_blank = True

                        selected_type = self.previous_type
                        while selected_type == self.previous_type:

                            if len(self.traffic_sign_data) == 1:
                                selected_type = list(self.traffic_sign_data)[0]
                                if len(self.traffic_sign_data[selected_type].images) == 0:
                                    self.signs_finished = True
                                    # print(self.traffic_sign_data)
                                    print(f"SIMULATION FINISHED")
                                else:
                                    temp_image_idx = random.randint(0, len(self.traffic_sign_data[selected_type].images) - 1)
                                    selected_image = self.traffic_sign_data[selected_type].images[temp_image_idx]
                                    # print(f"remove that image => new data:{self.traffic_sign_data}")
                                break
                            temp_type_idx = random.randint(0, len(self.traffic_sign_data) - 1)
                            selected_type = list(self.traffic_sign_data)[temp_type_idx]

                            # print(f"previous type: {self.previous_type} - selected type: {selected_type} - images len: {len(self.traffic_sign_data[selected_type].images)} - shown sign numbers: {self.number_of_show_signs}")
                            if len(self.traffic_sign_data[selected_type].images) == 0:
                                self.traffic_sign_data.pop(selected_type)
                                # print(f"pop that type => new data:{self.traffic_sign_data}")
                                selected_type = self.previous_type
                            else:
                                temp_image_idx = random.randint(0, len(self.traffic_sign_data[selected_type].images) - 1)
                                selected_image = self.traffic_sign_data[selected_type].images[temp_image_idx]
                                # print(f"remove that image => new data:{self.traffic_sign_data}")

                        if not self.signs_finished:
                            self.traffic_sign_data[selected_type].images.remove(selected_image)
                        if not self.signs_finished:
                            self.previous_type = selected_type
                            self.previous_image = selected_image

                            # we will show blank page next
                            self.step_threshold = random.randint(
                                mathstrovehiclesim.globals.MIN_BLANK_STEPS,
                                mathstrovehiclesim.globals.MIN_BLANK_STEPS)

                            if selected_type == "headlight_on":
                                self.headlight_on = True
                            elif selected_type == "headlight_off":
                                self.headlight_on = False

                    # print(f"threshold: {self.step_threshold}")
                    self.current_step = 0
                else:
                    self.current_step += 1
                    # print(f"step: {self.current_step}")

                if self.signs_finished:
                    while self.signs_finished:
                        # print(self.traffic_sign_data)
                        # print(f"number of signs: {self.number_of_show_signs}")
                        report_bg = pygame.image.load(mathstrovehiclesim.globals.REPORT_BACKGROUND).convert_alpha()
                        report_bg_rect = report_bg.get_rect()
                        report_bg_rect.center = (mathstrovehiclesim.globals.WIDTH // 2, mathstrovehiclesim.globals.HEIGHT // 2)

                        self.screen.blit(report_bg, (0, 0))

                        font = pygame.font.Font('freesansbold.ttf', 14)
                        text = font.render(f"ACCURACY SCORE: {self.model_accuracy_score:.2f}", True, mathstrovehiclesim.globals.BLACK)
                        self.screen.blit(text, (50, 50))
                        text = font.render(f"CONTROL CODE SCORE: {(self.control_code_score/self.frame_number)*100:.2f}", True, mathstrovehiclesim.globals.BLACK)
                        self.screen.blit(text, (50, 100))
                        text = font.render(f"NUMBER OF FEATURES: {self.n_features}", True, mathstrovehiclesim.globals.BLACK)
                        self.screen.blit(text, (50, 150))
                        pygame.display.update()

                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                self.running = False
                                self.quit_game = True
                                self.perception.running = False
                                pygame.quit()
                                exit()
                else:
                    if not self.show_blank:
                        selected_ts_image = pygame.image.load(self.previous_image).convert_alpha()

                        selected_ts_image = pygame.transform.scale(selected_ts_image, (mathstrovehiclesim.globals.WIDTH * mathstrovehiclesim.globals.TRAFFIC_SIGN_RATIO, mathstrovehiclesim.globals.WIDTH * mathstrovehiclesim.globals.TRAFFIC_SIGN_RATIO * selected_ts_image.get_height() / selected_ts_image.get_width()))
                        selected_ts_image_rect = selected_ts_image.get_rect()
                        selected_ts_image_rect.center = (mathstrovehiclesim.globals.WIDTH - self.sign_start_x + selected_ts_image.get_width() // 2) , mathstrovehiclesim.globals.HEIGHT - 25 - selected_ts_image.get_height() // 2

                        pygame.draw.rect(
                            self.screen, mathstrovehiclesim.globals.WHITE, (mathstrovehiclesim.globals.WIDTH - self.sign_start_x + selected_ts_image.get_width() // 2 - 5, mathstrovehiclesim.globals.HEIGHT - 30, 10,30)
                        )
                        self.screen.blit(selected_ts_image, selected_ts_image_rect)

                    # SPEED
                    speed_color = mathstrovehiclesim.globals.BLACK
                    if self.host_vehicle.get_speed() < 25:
                        speed_color = mathstrovehiclesim.globals.WHITE
                    elif self.host_vehicle.get_speed() < 30:
                        speed_color = mathstrovehiclesim.globals.GREEN
                    elif self.host_vehicle.get_speed() < 35:
                        speed_color = mathstrovehiclesim.globals.YELLOW
                    else:
                        speed_color = mathstrovehiclesim.globals.RED
                    font = pygame.font.Font('freesansbold.ttf', 30)
                    text = font.render(f"{self.host_vehicle.get_speed()}", True, speed_color)
                    self.screen.blit(text, (20, 20))

                    # pygame.draw.rect(self.screen, mathstrovehiclesim.globals.YELLOW, pygame.Rect(mathstrovehiclesim.globals.STEMHACK_PARAMETER_PANEL_YELLOW_RECT_START_X, mathstrovehiclesim.globals.STEMHACK_PARAMETER_PANEL_YELLOW_RECT_START_y, mathstrovehiclesim.globals.STEMHACK_PARAMETER_PANEL_YELLOW_RECT_WIDTH, mathstrovehiclesim.globals.STEMHACK_PARAMETER_PANEL_YELLOW_RECT_HEIGHT))
                    # pygame.draw.rect(self.screen, mathstrovehiclesim.globals.BLACK, pygame.Rect(mathstrovehiclesim.globals.STEMHACK_PARAMETER_PANEL_BLACK_RECT_START_X, mathstrovehiclesim.globals.STEMHACK_PARAMETER_PANEL_BLACK_RECT_START_y, mathstrovehiclesim.globals.STEMHACK_PARAMETER_PANEL_BLACK_RECT_WIDTH, mathstrovehiclesim.globals.STEMHACK_PARAMETER_PANEL_BLACK_RECT_HEIGHT))
                    
                    self.screen.blit(self.panel_background, (mathstrovehiclesim.globals.STEMHACK_PARAMETER_PANEL_YELLOW_RECT_START_X, mathstrovehiclesim.globals.STEMHACK_PARAMETER_PANEL_YELLOW_RECT_START_y))

                    # font = pygame.font.Font(None, mathstrovehiclesim.globals.STEMHACK_PANEL_FONT_SIZE)
                    text = self.font.render(f"MODEL SCORE: {self.model_accuracy_score:.2f}", True, mathstrovehiclesim.globals.BLACK)
                    self.screen.blit(text, (mathstrovehiclesim.globals.STEMHACK_PARAMETER_PANEL_TEXT_START_X, mathstrovehiclesim.globals.STEMHACK_PARAMETER_PANEL_BLACK_RECT_START_y + int(mathstrovehiclesim.globals.STEMHACK_PADDING*self.panel_scale) + 1 * mathstrovehiclesim.globals.STEMHACK_PARAMETER_PANEL_TEXT_HEIGHT))

                    text = self.font.render(f"CONTROL CODE SCORE: {(self.control_code_score/self.frame_number)*100:.2f}", True, mathstrovehiclesim.globals.BLACK)
                    self.screen.blit(text, (mathstrovehiclesim.globals.STEMHACK_PARAMETER_PANEL_TEXT_START_X, mathstrovehiclesim.globals.STEMHACK_PARAMETER_PANEL_BLACK_RECT_START_y + int(mathstrovehiclesim.globals.STEMHACK_PADDING*self.panel_scale) + 2 * mathstrovehiclesim.globals.STEMHACK_PARAMETER_PANEL_TEXT_HEIGHT))

                    text = self.font.render(f"PREDICTED TYPE: {user_type}", True, mathstrovehiclesim.globals.BLACK)
                    self.screen.blit(text, (mathstrovehiclesim.globals.STEMHACK_PARAMETER_PANEL_TEXT_START_X, mathstrovehiclesim.globals.STEMHACK_PARAMETER_PANEL_BLACK_RECT_START_y + int(mathstrovehiclesim.globals.STEMHACK_PADDING*self.panel_scale) + 3 * mathstrovehiclesim.globals.STEMHACK_PARAMETER_PANEL_TEXT_HEIGHT))

                    text = self.font.render(f"HOST SPEED: {self.host_vehicle.get_speed()}", True, mathstrovehiclesim.globals.BLACK)
                    self.screen.blit(text, (mathstrovehiclesim.globals.STEMHACK_PARAMETER_PANEL_TEXT_START_X, mathstrovehiclesim.globals.STEMHACK_PARAMETER_PANEL_BLACK_RECT_START_y + int(mathstrovehiclesim.globals.STEMHACK_PADDING*self.panel_scale) + 4 * mathstrovehiclesim.globals.STEMHACK_PARAMETER_PANEL_TEXT_HEIGHT))

                    # text = self.font.render(f"GIVEN ACTION: {user_action}", True, mathstrovehiclesim.globals.BLACK)
                    # self.screen.blit(text, (mathstrovehiclesim.globals.STEMHACK_PARAMETER_PANEL_TEXT_START_X, mathstrovehiclesim.globals.STEMHACK_PARAMETER_PANEL_BLACK_RECT_START_y + int(mathstrovehiclesim.globals.STEMHACK_PADDING*self.panel_scale) + 5 * mathstrovehiclesim.globals.STEMHACK_PARAMETER_PANEL_TEXT_HEIGHT))

                    pygame.display.flip()
                    if self.show_blank:
                        self.required_type = "blank"
                    else:
                        self.required_type = self.previous_type
            else:
                self.required_type = ""
                # draw/render
                self.env.render(self.screen)
                font = pygame.font.Font('freesansbold.ttf', mathstrovehiclesim.globals.FONT_SIZE)
                text = font.render('SIMULATION ENDED', True, mathstrovehiclesim.globals.GREEN, mathstrovehiclesim.globals.BLUE)
                text_rect = text.get_rect(center=(mathstrovehiclesim.globals.WIDTH / 2, mathstrovehiclesim.globals.HEIGHT / 2))
                self.screen.blit(text, text_rect)
                pygame.display.flip()

        pygame.display.update()
        self.clock.tick(mathstrovehiclesim.globals.FPS)


class MultiLaneHighwayAVSimulator:
    def __init__(self, speed_limit=30, initial_speed=27, show_parameter_panel=True, size="medium"):
        mathstrovehiclesim.globals.set_screen_size(size=size)
        self.screen = pygame.display.set_mode((mathstrovehiclesim.globals.WIDTH,mathstrovehiclesim.globals.HEIGHT))

        pygame.display.set_caption(mathstrovehiclesim.globals.CAPTION)
        self.num_lanes = 3
        # create sprites
        self.env = Env(self.num_lanes, show_horizontal_line=False)
        self.road_borders = self.env.get_sidwalk_road_borders()
        self.lane_borders = get_lane_borders(self.road_borders[0], num_lane=self.num_lanes)
        self.show_parameter_panel = show_parameter_panel

        # ----------------------------------- SETUP TRAFFIC ---------------------------------
        # speed range of traffic objects
        low_speed = math.floor(0.7 * speed_limit)
        high_speed = math.floor(0.9 * speed_limit)

        # router class needs below parameters
        # gap_offset: offset for gap between two adjacent traffic objects (Y axis)
        # traffic_object_start_point: start point for adding new traffic objects (Y axis)
        # has_speed_change: should change the speed of traffic objects or not
        # speed_change_gap_low and speed_change_gap_high: range for spent time to change the speed of traffic objects
        self.traffic_router = TrafficRouter(self.lane_borders, self.road_borders, self.num_lanes,
                                            speed_range=[low_speed, high_speed], gap_offset=0,
                                            traffic_object_start_point=0, has_speed_change=True,
                                            new_traffic_object_probability=0.33)

        # -------------------------------- SETUP HOST VEHICLE ---------------------------------
        self.host_vehicle = HostVehicle(mathstrovehiclesim.globals.HOST_VEHICLE_IMAGES, self.lane_borders,
                                        p_bottom_pos=(0,mathstrovehiclesim.globals.HEIGHT),
                                        p_init_lng_spd=initial_speed, p_max_spd=speed_limit, is_motorcycle=False, lane=1)
        self.host_odometer_value = 0
        self.show_odometer_panel = show_parameter_panel
        # initialize scenario variables
        self.running = True
        self.perception = {}
        self.lanes_speed = [0] * self.num_lanes
        self.clock = pygame.time.Clock()
        self.quit_game = False

    def step(self, action=""):
        if self.running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.quit_game = True
                    self.perception.running = False
                    pygame.quit()
                    exit()
            # update host vehicle based on user input
            self.host_vehicle.update(action)

            # update the environment
            self.env.update(speed=self.host_vehicle.get_speed())

            # manage traffic objects (we should provide host vehicle lane in each step to manage the speed of that lane by specified step)
            targets, self.lanes_speed = self.traffic_router.update(host_speed=self.host_vehicle.get_speed())

            # get the self.perception from host vehicle
            self.perception = self.host_vehicle.sensing(targets)

            # update odometer value
            self.host_odometer_value += self.host_vehicle.get_speed()

            # check the possible collision
            self.running = self.perception.running and (not self.host_vehicle.off_road_left) and (not self.host_vehicle.off_road_right)
            self.perception.running = self.running

            self.render()
            return self.perception
        else:
            return {"running":False}

    def render(self):
        if self.running:
            self.env.render(self.screen)

            # render the traffic objects
            self.traffic_router.render(self.screen)

            # render host vehicle
            self.host_vehicle.render(self.screen)

            if self.show_parameter_panel:

                data = [
                    f"host_speed: {self.perception.host_speed}",
                    f"host_lane: {self.perception.host_lane}",
                    "",
                    f"forward dist: {self.perception.forward_target.dist}",
                    f"forward speed: {self.perception.forward_target.vy}",
                    "",
                    f"left_lane_available: {self.perception.left_lane_available}",
                    f"left dist: {self.perception.left_forward_target.dist}",
                    f"left speed: {self.perception.left_forward_target.vy}",
                    "",
                    f"right_lane_available: {self.perception.right_lane_available}",
                    f"right dist: {self.perception.right_forward_target.dist}",
                    f"right speed: {self.perception.right_forward_target.vy}",
                    "",
                    f"lanes speed: {self.lanes_speed}"
                ]

                pygame.draw.rect(self.screen, mathstrovehiclesim.globals.YELLOW, pygame.Rect(mathstrovehiclesim.globals.PARAMETER_PANEL_YELLOW_RECT_START_X, mathstrovehiclesim.globals.PARAMETER_PANEL_YELLOW_RECT_START_y, mathstrovehiclesim.globals.PARAMETER_PANEL_YELLOW_RECT_WIDTH, mathstrovehiclesim.globals.PARAMETER_PANEL_YELLOW_RECT_HEIGHT))
                pygame.draw.rect(self.screen, mathstrovehiclesim.globals.BLACK, pygame.Rect(mathstrovehiclesim.globals.PARAMETER_PANEL_BLACK_RECT_START_X, mathstrovehiclesim.globals.PARAMETER_PANEL_BLACK_RECT_START_y, mathstrovehiclesim.globals.PARAMETER_PANEL_BLACK_RECT_WIDTH, mathstrovehiclesim.globals.PARAMETER_PANEL_BLACK_RECT_HEIGHT))
                for idx in range(len(data)):
                    font = pygame.font.Font('freesansbold.ttf', mathstrovehiclesim.globals.PANEL_FONT_SIZE)
                    text = font.render(data[idx], True, mathstrovehiclesim.globals.WHITE)
                    self.screen.blit(text, (mathstrovehiclesim.globals.PARAMETER_PANEL_TEXT_START_X, mathstrovehiclesim.globals.PARAMETER_PANEL_BLACK_RECT_START_y + mathstrovehiclesim.globals.PADDING + idx * mathstrovehiclesim.globals.PARAMETER_PANEL_TEXT_HEIGHT))

            pygame.display.flip()
        else:
            # draw/render
            self.env.render(self.screen)
            font = pygame.font.Font('freesansbold.ttf', mathstrovehiclesim.globals.FONT_SIZE)
            text = font.render('SIMULATION ENDED', True, mathstrovehiclesim.globals.GREEN, mathstrovehiclesim.globals.BLUE)
            text_rect = text.get_rect(center=(mathstrovehiclesim.globals.WIDTH / 2, mathstrovehiclesim.globals.HEIGHT / 2))
            self.screen.blit(text, text_rect)
            pygame.display.flip()

        pygame.display.update()
        self.clock.tick(mathstrovehiclesim.globals.FPS)


class OdometerCalculationSimulator:
    def __init__(self, size="medium", initial_speed=25, odometer_threshold=500, speed_range=[5, 10], varying_spd=False):
        if type(varying_spd) is not bool:
            raise TypeError("varying_spd should be a boolean!")
        self.varying_spd = varying_spd
        self.speed_range = speed_range
        mathstrovehiclesim.globals.set_screen_size(size=size)
        self.screen = pygame.display.set_mode((mathstrovehiclesim.globals.WIDTH,mathstrovehiclesim.globals.HEIGHT))

        pygame.display.set_caption(mathstrovehiclesim.globals.CAPTION)
        self.num_lanes = 1
        if odometer_threshold < 0:
            raise ValueError("The odometer threshold should be positive number!")

        if type(odometer_threshold) is not int:
            raise TypeError("Odometer threshold should be an integer!")
        self.odometer_threshold = odometer_threshold
        # create sprites
        self.env = Env(self.num_lanes, show_horizontal_line=False)

        self.road_borders = self.env.get_sidwalk_road_borders()
        self.lane_borders = get_lane_borders(self.road_borders[0], num_lane=self.num_lanes)

        # -------------------------------- SETUP HOST VEHICLE ---------------------------------
        self.host_vehicle = HostVehicle(mathstrovehiclesim.globals.HOST_VEHICLE_IMAGES, self.lane_borders,
                                        p_bottom_pos=(0,mathstrovehiclesim.globals.HEIGHT),
                                        p_init_lng_spd=initial_speed, is_motorcycle=False, lane=0)
        self.host_odometer_value = 0
        self.user_given_odometer_value = 0
        # initialize scenario variables
        self.running = True
        self.clock = pygame.time.Clock()
        self.quit_game = False

        self.time_step = 1
        self.message = ""

    def step(self, action="", user_given_odometer_value=0):

        if type(user_given_odometer_value) is not int:
            raise TypeError("user_given_odometer_value should be an integer!")

        self.user_given_odometer_value = user_given_odometer_value

        if self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.quit_game = True
                    pygame.quit()
                    exit()

            if (self.host_odometer_value - self.odometer_threshold) >= self.host_vehicle.get_speed():
                self.message = "FAIL: TRAVELLED PAST THE REQUIRED DISTANCE!"
            elif (self.host_odometer_value - self.odometer_threshold) < 0 and action == "stop":
                self.message = "FAIL: DID NOT TRAVEL THE REQUIRED DISTANCE!"
            elif action == "stop":
                self.message = "PASS: TRAVELLED THE CORRECT DISTANCE!"

            self.render()
            if self.varying_spd:
                new_speed = random.randint(self.speed_range[0], self.speed_range[1])
                self.host_vehicle.set_speed(new_speed)

            # update host vehicle based on user input
            if mathstrovehiclesim.globals.DEBUG:
                print(f"speed outside env: {self.host_vehicle.get_speed()}")
            self.host_vehicle.update("")

            # update the environment
            self.env.update(speed=self.host_vehicle.get_speed())

            # update odometer value
            self.host_odometer_value += self.host_vehicle.get_speed()

            return self.host_vehicle.get_speed(), self.time_step

        else:
            self.render()
            return {"running":False}

    def render(self):
        if not self.quit_game:
            if self.running:
                self.env.render(self.screen)

                # render host vehicle
                self.host_vehicle.render(self.screen)

            pygame.draw.rect(self.screen, mathstrovehiclesim.globals.YELLOW, pygame.Rect(mathstrovehiclesim.globals.ODOMETER_PANEL_START_POINT, mathstrovehiclesim.globals.ODOMETER_PANEL_START_POINT, mathstrovehiclesim.globals.ODOMETER_PANEL_WIDTH + 2 * mathstrovehiclesim.globals.ODOMETER_PANEL_BORDER_WIDTH, mathstrovehiclesim.globals.ODOMETER_PANEL_HEIGHT + 2 * mathstrovehiclesim.globals.ODOMETER_PANEL_BORDER_WIDTH))
            pygame.draw.rect(self.screen, mathstrovehiclesim.globals.BLACK, pygame.Rect(mathstrovehiclesim.globals.ODOMETER_PANEL_START_POINT + mathstrovehiclesim.globals.ODOMETER_PANEL_BORDER_WIDTH, mathstrovehiclesim.globals.ODOMETER_PANEL_START_POINT + mathstrovehiclesim.globals.ODOMETER_PANEL_BORDER_WIDTH, mathstrovehiclesim.globals.ODOMETER_PANEL_WIDTH, mathstrovehiclesim.globals.ODOMETER_PANEL_HEIGHT))
            font = pygame.font.Font('freesansbold.ttf', mathstrovehiclesim.globals.PANEL_FONT_SIZE)
            text = font.render("ODOMETER PANEL", True, mathstrovehiclesim.globals.YELLOW)
            self.screen.blit(text, (mathstrovehiclesim.globals.ODOMETER_PANEL_START_POINT * 2, mathstrovehiclesim.globals.ODOMETER_PANEL_START_POINT * 2))
            font = pygame.font.Font('freesansbold.ttf', mathstrovehiclesim.globals.ODOMETER_FONT_SIZE)
            color = mathstrovehiclesim.globals.RED
            if int(self.user_given_odometer_value) == int(self.host_odometer_value):
                color = mathstrovehiclesim.globals.GREEN

            text = font.render(f"USER VALUE: {self.user_given_odometer_value:,}", True, mathstrovehiclesim.globals.WHITE)
            self.screen.blit(text, (mathstrovehiclesim.globals.ODOMETER_PANEL_START_POINT * 2, mathstrovehiclesim.globals.ODOMETER_PANEL_START_POINT * 2 + mathstrovehiclesim.globals.ODOMETER_PANEL_HEIGHT * 1 / 4))
            delta = self.host_odometer_value - self.user_given_odometer_value
            text = font.render(f"ERROR: {delta:,}", True, color)
            self.screen.blit(text, (mathstrovehiclesim.globals.ODOMETER_PANEL_START_POINT * 2, mathstrovehiclesim.globals.ODOMETER_PANEL_START_POINT * 2 + mathstrovehiclesim.globals.ODOMETER_PANEL_HEIGHT * 2 / 4))
            text = font.render(f"SPEED: {self.host_vehicle.get_speed()}", True, mathstrovehiclesim.globals.WHITE)
            self.screen.blit(text, (mathstrovehiclesim.globals.ODOMETER_PANEL_START_POINT * 2, mathstrovehiclesim.globals.ODOMETER_PANEL_START_POINT * 2 + mathstrovehiclesim.globals.ODOMETER_PANEL_HEIGHT * 3 / 4))

            if self.message != "":
                font = pygame.font.Font('freesansbold.ttf', mathstrovehiclesim.globals.FONT_SIZE)
                if "PASS" in self.message:
                    text = font.render(self.message, True, mathstrovehiclesim.globals.GREEN, mathstrovehiclesim.globals.BLACK)
                else:
                    text = font.render(self.message, True, mathstrovehiclesim.globals.RED, mathstrovehiclesim.globals.BLACK)
                text_rect = text.get_rect(center=(mathstrovehiclesim.globals.WIDTH / 2, mathstrovehiclesim.globals.HEIGHT / 2))
                self.screen.blit(text, text_rect)

            pygame.display.flip()
        else:
            # draw/render
            self.env.render(self.screen)
            font = pygame.font.Font('freesansbold.ttf', mathstrovehiclesim.globals.FONT_SIZE)
            text = font.render('SIMULATION ENDED', True, mathstrovehiclesim.globals.GREEN, mathstrovehiclesim.globals.BLUE)
            text_rect = text.get_rect(center=(mathstrovehiclesim.globals.WIDTH / 2, mathstrovehiclesim.globals.HEIGHT / 2))
            self.screen.blit(text, text_rect)
            pygame.display.flip()

            pygame.display.update()
            self.clock.tick(mathstrovehiclesim.globals.FPS)


class ParallelParkingSimulator:
    def __init__(self, initial_speed=20, size="medium"):
        mathstrovehiclesim.globals.set_screen_size(size=size)
        self.screen = pygame.display.set_mode((mathstrovehiclesim.globals.WIDTH,mathstrovehiclesim.globals.HEIGHT))

        pygame.display.set_caption(mathstrovehiclesim.globals.CAPTION)
        self.num_lanes = 2
        # create sprites
        self.env = Env(self.num_lanes, show_horizontal_line=True)
        self.clock = pygame.time.Clock()

        self.check_position_list = []
        self.step_position_list = []
        self.step_image_list = []
        self.x_image = pygame.transform.scale(pygame.image.load(mathstrovehiclesim.globals.X_IMAGE).convert_alpha(), mathstrovehiclesim.globals.CHECK_SIZE)
        self.check_image = pygame.transform.scale(pygame.image.load(mathstrovehiclesim.globals.CHECK_IMAGE).convert_alpha(), mathstrovehiclesim.globals.CHECK_SIZE)
        for i in range(0, 7):
            self.step_image_list.append(pygame.transform.scale(pygame.image.load(mathstrovehiclesim.globals.STEPS_IMAGES[i]).convert_alpha(), mathstrovehiclesim.globals.STEP_SIZE))
            self.check_position_list.append(mathstrovehiclesim.globals.PARKING_PANEL_START_POINT * 2 + i * mathstrovehiclesim.globals.STEP_GAP)
            self.step_position_list.append(mathstrovehiclesim.globals.PARKING_PANEL_START_POINT * 2 + i * mathstrovehiclesim.globals.STEP_GAP)

        self.itr_step = 0
        self.required_action = "forward"
        self.failure_message = ""
        self.done_steps = [False, False, False, False, False, False, False]
        self.done_steps = [False, False, False, False, False, False, False]

        self.road_borders = self.env.get_sidwalk_road_borders()
        self.lane_borders = get_lane_borders(self.road_borders[0], num_lane=self.num_lanes)
        self.get_horizontal_line_location = self.env.get_horizontal_line_location()
        # add two veh_sim.globals.VEHICLES
        self.targets = pygame.sprite.Group()
        image_idx = random.randint(0,3)
        target_1 = SingleTargetAhead(mathstrovehiclesim.globals.VEHICLE_IMAGES[image_idx], self.lane_borders,
                                     p_bottom_pos=(0,self.get_horizontal_line_location[1][1] - 30),
                                     p_init_lng_spd=0, is_motorcycle=False, lane=1)
        image_idx = random.randint(0,3)
        target_2 = SingleTargetAhead(mathstrovehiclesim.globals.VEHICLE_IMAGES[image_idx], self.lane_borders,
                                     p_bottom_pos=(0,self.get_horizontal_line_location[2][1] + 30),
                                     p_init_lng_spd=0, is_motorcycle=False, lane=1, set_top=True)
        self.targets.add(target_1)
        self.targets.add(target_2)

        # -------------------------------- SETUP HOST VEHICLE ---------------------------------
        self.host_vehicle = HostVehicle(mathstrovehiclesim.globals.HOST_VEHICLE_IMAGES, self.lane_borders,
                                        p_bottom_pos=(0,mathstrovehiclesim.globals.HEIGHT),
                                        p_init_lng_spd=initial_speed, is_motorcycle=False, lane=0)

        # initialize scenario variables
        self.running = True
        self.clock = pygame.time.Clock()
        self.quit_game = False

    def step(self, action):
        if self.running and self.failure_message == "":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.quit_game = True
                    pygame.quit()
                    exit()

            if action != "stop":
                if action == self.required_action and self.failure_message == "":
                    # update host vehicle based on user input
                    self.host_vehicle.update(action)

                    # update the environment
                    self.env.update(speed=0)

                    if self.itr_step == mathstrovehiclesim.globals.PARALLEL_PARKING_STEPS[0]:
                        self.done_steps[0] = True
                        self.required_action = "turn_right"
                    elif self.itr_step == mathstrovehiclesim.globals.PARALLEL_PARKING_STEPS[1]:
                        self.done_steps[1] = True
                        self.required_action = "reverse"
                    elif self.itr_step == mathstrovehiclesim.globals.PARALLEL_PARKING_STEPS[2]:
                        self.done_steps[2] = True
                        self.required_action = "turn_left"
                    elif self.itr_step == mathstrovehiclesim.globals.PARALLEL_PARKING_STEPS[3]:
                        self.done_steps[3] = True
                        self.required_action = "reverse"
                    elif self.itr_step == mathstrovehiclesim.globals.PARALLEL_PARKING_STEPS[4]:
                        self.done_steps[4] = True
                        self.required_action = "turn_left"
                    elif self.itr_step == mathstrovehiclesim.globals.PARALLEL_PARKING_STEPS[5]:
                        self.done_steps[5] = True
                        self.required_action = "reverse"
                    elif self.itr_step == mathstrovehiclesim.globals.PARALLEL_PARKING_STEPS[6]:
                        self.done_steps[6] = True
                        self.required_action = "done"

                    self.itr_step += 1
                elif self.required_action != "done":
                    self.failure_message = f"You should use '{self.required_action}' action here"
                elif self.required_action == "done":
                    self.done_steps[6] = False
                    self.failure_message = "You should stop earlier"
            else:
                if self.required_action != "done":
                    self.failure_message = f"You should use '{self.required_action}' action here"

            if mathstrovehiclesim.globals.DEBUG:
                print(f"step: {self.itr_step} - action: {action} - next required_action: {self.required_action}")

            self.render()

        else:
            self.render()
            return {"running":False}

    def render(self):
        if not self.quit_game:
            if self.failure_message == "":
                self.env.render(self.screen, show_sidewalk_objects=False)

                self.targets.draw(self.screen)

                # render host vehicle
                self.host_vehicle.parrallel_parking_render(self.screen)

            else:
                self.env.render(self.screen)

                self.targets.draw(self.screen)

                # render host vehicle
                self.host_vehicle.parrallel_parking_render(self.screen)

                font = pygame.font.Font('freesansbold.ttf', mathstrovehiclesim.globals.FONT_SIZE)
                text = font.render(self.failure_message, True, mathstrovehiclesim.globals.GREEN, mathstrovehiclesim.globals.BLUE)
                text_rect = text.get_rect(center=(mathstrovehiclesim.globals.WIDTH / 2, mathstrovehiclesim.globals.HEIGHT / 2))
                self.screen.blit(text, text_rect)

            if self.required_action == "done" and self.itr_step == mathstrovehiclesim.globals.PARALLEL_PARKING_STEPS[6] + 1 and self.failure_message == "":
                font = pygame.font.Font('freesansbold.ttf', mathstrovehiclesim.globals.FONT_SIZE)
                text = font.render("WELL DONE!", True, mathstrovehiclesim.globals.GREEN, mathstrovehiclesim.globals.BLUE)
                text_rect = text.get_rect(center=(mathstrovehiclesim.globals.WIDTH / 2, mathstrovehiclesim.globals.HEIGHT / 2))
                self.screen.blit(text, text_rect)

        for i in range(0, 7):
            self.screen.blit(self.step_image_list[i], (mathstrovehiclesim.globals.PARKING_PANEL_START_POINT, self.step_position_list[i]))

        for i in range(7):
            if self.done_steps[i] == True:
                self.screen.blit(self.check_image, (mathstrovehiclesim.globals.STEP_SIZE[0] - mathstrovehiclesim.globals.CHECK_SIZE[0], self.check_position_list[i]))
            elif self.failure_message != "":
                self.screen.blit(self.x_image, (mathstrovehiclesim.globals.STEP_SIZE[0] - mathstrovehiclesim.globals.CHECK_SIZE[0], self.check_position_list[i]))
                break

        pygame.display.update()
        self.clock.tick(mathstrovehiclesim.globals.FPS)
