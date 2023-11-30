import json
import os

from easydict import EasyDict as edict

# read configuration file
dir = os.path.dirname(__file__)
cfg_file = os.path.join(dir,"simulation_cfg.json")
with open(cfg_file, "r") as f:
    sim_cfg = edict(json.load(f))

FPS = sim_cfg.screen.FPS


# define colors
ASPHALT_COLOR = (42, 41, 34)
SIDEWALK_COLOR = (183, 173, 63)
GRASS_COLOR = (0,154,23)
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255, 255, 0)
GREEN = (0,255,0)
BLUE = (0,0,255)
GRAY = (128, 128, 128)

# window sizes
# you can change the screen size here
WIDTH = 1100
TRAFFIC_SIGN_WIDTH = 400
HEIGHT = 600
FONT_SIZE = 32
PANEL_FONT_SIZE = 10
# PARALLEL_PARKING_STEPS = [63, 98, 190, 233, 255, 290, 385]#small
PARALLEL_PARKING_STEPS = [99, 134, 254, 289, 334, 369, 489]  # medium

# base size (don't change this size)
# base size => WIDTH: 1100, HEIGHT: 600
BASE_WIDTH = 1100
BASE_HEIGHT = 600

# road
WHITE_LANE_WIDTH = round(sim_cfg.road.whiteLaneWidth * WIDTH / BASE_WIDTH)
WHITE_LANE_HEIGHT = round(sim_cfg.road.whiteLaneHeight * HEIGHT / BASE_HEIGHT)
WHITE_LANE_GAP = round(sim_cfg.road.whiteLaneGap * HEIGHT / BASE_HEIGHT)
ROAD_LANE_WIDTH = round(sim_cfg.road.laneWidth * WIDTH / BASE_WIDTH)
HORIZONTAL_LANE_WIDTH = round(sim_cfg.road.horizontalLaneWidth * WIDTH / BASE_WIDTH)
HORIZONTAL_LANE_HEIGHT = round(sim_cfg.road.horizontalLaneThickness * HEIGHT / BASE_HEIGHT)
HORIZONTAL_LANE_GAP = round(sim_cfg.road.horizontalLaneGap * HEIGHT / BASE_HEIGHT)
HORIZONTAL_LANE_START_Y = round(sim_cfg.road.horizontalLaneStartY * HEIGHT / BASE_HEIGHT)
# LANE_BORDERS = [] I should use global variable for the lane borders in the Vehicle class later

# road sides
GRASS_AREA_RATIO = sim_cfg.road.GRASS_AREA_RATIO  # ratio of grass area WIDTH in the calculation
SIDEWALK_AREA_RATIO = sim_cfg.road.SIDEWALK_AREA_RATIO  # ratio of sidewalk area WIDTH in the calculation
# for example: grass_area_width = (window - n_lanes * lane_width)/(2 * (GRASS_AREA_RATIO + SIDEWALK_AREA_RATIO))

# trees
TREES_WIDTH = round(sim_cfg.env_objects.TREES_WIDTH * WIDTH / BASE_WIDTH)
TREES_GAP = round(sim_cfg.env_objects.TREES_GAP * HEIGHT / BASE_HEIGHT)
TREES_START_POINT = round(sim_cfg.env_objects.TREES_START_POINT * HEIGHT / BASE_HEIGHT)
TREES_IMAGES = [os.path.join(dir,sim_cfg.env_objects.images.tree_0),
                os.path.join(dir,sim_cfg.env_objects.images.tree_1),
                os.path.join(dir,sim_cfg.env_objects.images.tree_2),
                os.path.join(dir,sim_cfg.env_objects.images.tree_3)]
# houses
HOUSES_WIDTH = round(sim_cfg.env_objects.house_width * WIDTH / BASE_WIDTH)
HOUSES_GAP = round(sim_cfg.env_objects.house_gap * HEIGHT / BASE_HEIGHT)
HOUSE_START_POINT = round(sim_cfg.env_objects.HOUSE_START_POINT * HEIGHT / BASE_HEIGHT)
HOUSES_IMAGES = [os.path.join(dir,sim_cfg.env_objects.images.house_0),
                 os.path.join(dir,sim_cfg.env_objects.images.house_1),
                 os.path.join(dir,sim_cfg.env_objects.images.house_2),
                 os.path.join(dir,sim_cfg.env_objects.images.house_3)]


# sidewalk objects
SIDEWALK_OBJECTS_WIDTH = round(sim_cfg.env_objects.sidewalk_object_width * WIDTH / BASE_WIDTH)
SIDEWALK_OBJECTS_GAP_MIN = round(sim_cfg.env_objects.sidewalk_object_gap_min * HEIGHT / BASE_HEIGHT)
SIDEWALK_OBJECTS_GAP_MAX = round(sim_cfg.env_objects.sidewalk_object_gap_max * HEIGHT / BASE_HEIGHT)
SIDEWALK_OBJECTS_START_POINT = round(sim_cfg.env_objects.sidewalk_object_start_point * HEIGHT / BASE_HEIGHT)
SIDEWALK_OBJECTS_IMAGES = [os.path.join(dir,sim_cfg.env_objects.images.sidewalk_object_0),
                           os.path.join(dir,sim_cfg.env_objects.images.sidewalk_object_1),
                           os.path.join(dir,sim_cfg.env_objects.images.sidewalk_object_2),
                           os.path.join(dir,sim_cfg.env_objects.images.sidewalk_object_3),
                           os.path.join(dir,sim_cfg.env_objects.images.sidewalk_object_4),
                           os.path.join(dir,sim_cfg.env_objects.images.sidewalk_object_5),
                           os.path.join(dir,sim_cfg.env_objects.images.sidewalk_object_6),
                           os.path.join(dir,sim_cfg.env_objects.images.sidewalk_object_7)]
BIKE_SPEED = sim_cfg.env_objects.BIKE_SPEED
PEDESTRIAN_SPEED = sim_cfg.env_objects.PEDESTRIAN_SPEED

# stemhack
TRAFFIC_SIGN_BACKGROUND_COLOR = (224, 210, 148)
TRAFFIC_SIGN_RATIO = 0.1
MIN_BLANK_STEPS = sim_cfg.stemhack.blank_page_min_steps
MAX_BLANK_STEPS = sim_cfg.stemhack.blank_page_max_steps

STEMHACK_IMAGES_DIR = os.path.join(dir, sim_cfg.stemhack.images_directory)
STEMHACK_TS_DATA = sim_cfg.stemhack.sign_type_list
STEMHACK_IMAGES_NUMBER = sim_cfg.stemhack.number_of_images_per_sign
START_BUTTON_PATH = os.path.join(dir, "images/start_button.png")
LANDING_PAGE_BACKGROUND = os.path.join(dir, "images/stem_hack_background.jpg")
REPORT_BACKGROUND = os.path.join(dir, "images/final_report_small.png")
PANEL_BACKGROUND = os.path.join(dir, "images/panel_small.png")

# stemhack parameter panel
STEMHACK_PANEL_FONT_SIZE = 10
STEMHACK_PADDING = 5
STEMHACK_PARAMETER_PANEL_TEXT_HEIGHT = 20
STEMHACK_PARAMETER_PANEL_BLACK_RECT_WIDTH = 150
STEMHACK_PARAMETER_PANEL_YELLOW_RECT_WIDTH = STEMHACK_PARAMETER_PANEL_BLACK_RECT_WIDTH + 2 * STEMHACK_PADDING
STEMHACK_PARAMETER_PANEL_BLACK_RECT_START_y = 30
STEMHACK_PARAMETER_PANEL_YELLOW_RECT_START_y = 30 - STEMHACK_PADDING
STEMHACK_PARAMETER_PANEL_BLACK_RECT_HEIGHT = 15 * STEMHACK_PARAMETER_PANEL_TEXT_HEIGHT  # 15 is number of lines (len(data)) in the pannel
STEMHACK_PARAMETER_PANEL_YELLOW_RECT_HEIGHT = 15 * STEMHACK_PARAMETER_PANEL_TEXT_HEIGHT + 2 * STEMHACK_PADDING  # 15 is number of lines (len(data)) in the pannel

STEMHACK_PARAMETER_PANEL_LEFT_MARGIN = 50
STEMHACK_PARAMETER_PANEL_BLACK_RECT_START_X = WIDTH - STEMHACK_PARAMETER_PANEL_BLACK_RECT_WIDTH - STEMHACK_PARAMETER_PANEL_LEFT_MARGIN
STEMHACK_PARAMETER_PANEL_TEXT_START_X = WIDTH - STEMHACK_PARAMETER_PANEL_BLACK_RECT_WIDTH - STEMHACK_PARAMETER_PANEL_LEFT_MARGIN + STEMHACK_PADDING
STEMHACK_PARAMETER_PANEL_YELLOW_RECT_START_X = WIDTH - STEMHACK_PARAMETER_PANEL_BLACK_RECT_WIDTH - STEMHACK_PARAMETER_PANEL_LEFT_MARGIN - STEMHACK_PADDING


# ------ CONSTANT TEXT MESSAGES ------ #
CAPTION = sim_cfg.screen.CAPTION


# VEHICLES
VEHICLES = edict(sim_cfg.vehicle)
VEHICLE_IMAGES = [os.path.join(dir,sim_cfg.vehicle.images.car_0),
                  os.path.join(dir,sim_cfg.vehicle.images.car_1),
                  os.path.join(dir,sim_cfg.vehicle.images.car_2),
                  os.path.join(dir,sim_cfg.vehicle.images.car_3),
                  os.path.join(dir,sim_cfg.vehicle.images.motorcycle_0)]

# host vehicle
HOST_VEHICLE = edict(sim_cfg.HOST_VEHICLE)
HOST_VEHICLE_IMAGES = os.path.join(dir,sim_cfg.HOST_VEHICLE.image)
HOST_VEHICLE_IMAGE_HEADLIGHT_ON = os.path.join(dir,sim_cfg.HOST_VEHICLE.head_light_on_image)


# parameter panel
PADDING = 5

PARAMETER_PANEL_TEXT_HEIGHT = 20
PARAMETER_PANEL_BLACK_RECT_WIDTH = 150
PARAMETER_PANEL_YELLOW_RECT_WIDTH = PARAMETER_PANEL_BLACK_RECT_WIDTH + 2 * PADDING
PARAMETER_PANEL_BLACK_RECT_START_y = 30
PARAMETER_PANEL_YELLOW_RECT_START_y = 30 - PADDING
PARAMETER_PANEL_BLACK_RECT_HEIGHT = 15 * PARAMETER_PANEL_TEXT_HEIGHT  # 15 is number of lines (len(data)) in the pannel
PARAMETER_PANEL_YELLOW_RECT_HEIGHT = 15 * PARAMETER_PANEL_TEXT_HEIGHT + 2 * PADDING  # 15 is number of lines (len(data)) in the pannel

PARAMETER_PANEL_LEFT_MARGIN = 50
PARAMETER_PANEL_BLACK_RECT_START_X = WIDTH - PARAMETER_PANEL_BLACK_RECT_WIDTH - PARAMETER_PANEL_LEFT_MARGIN
PARAMETER_PANEL_TEXT_START_X = WIDTH - PARAMETER_PANEL_BLACK_RECT_WIDTH - PARAMETER_PANEL_LEFT_MARGIN + PADDING
PARAMETER_PANEL_YELLOW_RECT_START_X = WIDTH - PARAMETER_PANEL_BLACK_RECT_WIDTH - PARAMETER_PANEL_LEFT_MARGIN - PADDING


# PARALLEL PARKING
MAX_STEERING_ANGLE = 45


# ODOMETER parameters
ODOMETER_PANEL_BORDER_WIDTH = 5
ODOMETER_PANEL_START_POINT = 10
ODOMETER_PANEL_WIDTH = 200
ODOMETER_PANEL_HEIGHT = 75
ODOMETER_FONT_SIZE = 15

STEPS_IMAGES = []
for img in sim_cfg.parallel_parking.step_images:
    STEPS_IMAGES.append(os.path.join(dir,img))
CHECK_IMAGE = os.path.join(dir,sim_cfg.parallel_parking.check_image)
X_IMAGE = os.path.join(dir,sim_cfg.parallel_parking.x_image)


MAX_STEERING_ANGLE = 35
TURNING_RADIUS_MULTIPLIER = 100

PARKING_PANEL_START_POINT = 10
STEP_SIZE = (200, 50)
CHECK_SIZE = (40, 40)
STEP_GAP = 60


DEBUG = False


def set_screen_size(size="medium"):
    global HEIGHT, WIDTH
    global WHITE_LANE_WIDTH, WHITE_LANE_HEIGHT, WHITE_LANE_GAP, ROAD_LANE_WIDTH, HORIZONTAL_LANE_WIDTH
    global HORIZONTAL_LANE_HEIGHT, HORIZONTAL_LANE_GAP, HORIZONTAL_LANE_START_Y, TREES_WIDTH, TREES_GAP
    global REES_START_POINT, TREES_START_POINT, HOUSES_WIDTH, HOUSES_GAP, HOUSE_START_POINT, SIDEWALK_OBJECTS_WIDTH
    global SIDEWALK_OBJECTS_GAP_MIN, SIDEWALK_OBJECTS_GAP_MAX, SIDEWALK_OBJECTS_START_POINT, PARALLEL_PARKING_STEPS
    global TURNING_RADIUS_MULTIPLIER, STEP_SIZE, CHECK_SIZE, STEP_GAP, FONT_SIZE
    global PARAMETER_PANEL_BLACK_RECT_START_X, PARAMETER_PANEL_TEXT_START_X, PARAMETER_PANEL_YELLOW_RECT_START_X
    global PARAMETER_PANEL_YELLOW_RECT_WIDTH, PARAMETER_PANEL_LEFT_MARGIN, PARAMETER_PANEL_BLACK_RECT_START_y, PARAMETER_PANEL_YELLOW_RECT_START_y
    global PARAMETER_PANEL_BLACK_RECT_WIDTH, PANEL_FONT_SIZE, PARAMETER_PANEL_TEXT_HEIGHT, PARAMETER_PANEL_BLACK_RECT_HEIGHT
    global PARAMETER_PANEL_YELLOW_RECT_HEIGHT, ODOMETER_FONT_SIZE, ODOMETER_PANEL_WIDTH, ODOMETER_PANEL_START_POINT

    global STEMHACK_PADDING, STEMHACK_PARAMETER_PANEL_BLACK_RECT_START_X, STEMHACK_PARAMETER_PANEL_TEXT_START_X, STEMHACK_PARAMETER_PANEL_YELLOW_RECT_START_X
    global STEMHACK_PANEL_FONT_SIZE, STEMHACK_PARAMETER_PANEL_YELLOW_RECT_WIDTH, STEMHACK_PARAMETER_PANEL_LEFT_MARGIN, STEMHACK_PARAMETER_PANEL_BLACK_RECT_START_y, STEMHACK_PARAMETER_PANEL_YELLOW_RECT_START_y
    global STEMHACK_PARAMETER_PANEL_BLACK_RECT_WIDTH, STEMHACK_PANEL_FONT_SIZE, STEMHACK_PARAMETER_PANEL_TEXT_HEIGHT, STEMHACK_PARAMETER_PANEL_BLACK_RECT_HEIGHT
    global STEMHACK_PARAMETER_PANEL_YELLOW_RECT_HEIGHT, STEMHACK_ODOMETER_FONT_SIZE, STEMHACK_ODOMETER_PANEL_WIDTH, STEMHACK_ODOMETER_PANEL_START_POINT
    if size == "small":
        PARALLEL_PARKING_STEPS = [50, 85, 140, 175, 200, 235, 290]  # small
        WIDTH = 550
        HEIGHT = 300
        STEP_SIZE = (100, 30)
        CHECK_SIZE = (25, 25)
        STEP_GAP = 30
        FONT_SIZE = 24
        PANEL_FONT_SIZE = 8

        PARAMETER_PANEL_BLACK_RECT_WIDTH = 100
        PARAMETER_PANEL_LEFT_MARGIN = 10
        PARAMETER_PANEL_YELLOW_RECT_WIDTH = PARAMETER_PANEL_BLACK_RECT_WIDTH + 2 * PADDING
        PARAMETER_PANEL_TEXT_HEIGHT = 13
        PARAMETER_PANEL_BLACK_RECT_START_y = 5
        PARAMETER_PANEL_YELLOW_RECT_START_y = PARAMETER_PANEL_BLACK_RECT_START_y - PADDING
        PARAMETER_PANEL_BLACK_RECT_HEIGHT = 15 * PARAMETER_PANEL_TEXT_HEIGHT  # 15 is number of lines (len(data)) in the pannel
        PARAMETER_PANEL_YELLOW_RECT_HEIGHT = 15 * PARAMETER_PANEL_TEXT_HEIGHT + 2 * PADDING  # 15 is number of lines (len(data)) in the pannel
        ODOMETER_FONT_SIZE = 8
        ODOMETER_PANEL_WIDTH = 90
        ODOMETER_PANEL_START_POINT = 5

        # stemhack parameter panel
        STEMHACK_PANEL_FONT_SIZE = 8
        STEMHACK_PADDING = 2
        STEMHACK_PARAMETER_PANEL_TEXT_HEIGHT = 20
        STEMHACK_PARAMETER_PANEL_BLACK_RECT_WIDTH = 160
        STEMHACK_PARAMETER_PANEL_YELLOW_RECT_WIDTH = STEMHACK_PARAMETER_PANEL_BLACK_RECT_WIDTH + 2 * STEMHACK_PADDING
        STEMHACK_PARAMETER_PANEL_BLACK_RECT_START_y = 5
        STEMHACK_PARAMETER_PANEL_YELLOW_RECT_START_y = STEMHACK_PARAMETER_PANEL_BLACK_RECT_START_y - STEMHACK_PADDING
        STEMHACK_PARAMETER_PANEL_BLACK_RECT_HEIGHT = 7 * STEMHACK_PARAMETER_PANEL_TEXT_HEIGHT  # 15 is number of lines (len(data)) in the pannel
        STEMHACK_PARAMETER_PANEL_YELLOW_RECT_HEIGHT = 7 * STEMHACK_PARAMETER_PANEL_TEXT_HEIGHT + 2 * STEMHACK_PADDING  # 15 is number of lines (len(data)) in the pannel

        STEMHACK_PARAMETER_PANEL_LEFT_MARGIN = 5
        STEMHACK_PARAMETER_PANEL_BLACK_RECT_START_X = WIDTH - STEMHACK_PARAMETER_PANEL_BLACK_RECT_WIDTH - STEMHACK_PARAMETER_PANEL_LEFT_MARGIN
        STEMHACK_PARAMETER_PANEL_TEXT_START_X = WIDTH - STEMHACK_PARAMETER_PANEL_BLACK_RECT_WIDTH - STEMHACK_PARAMETER_PANEL_LEFT_MARGIN + STEMHACK_PADDING * 2
        STEMHACK_PARAMETER_PANEL_YELLOW_RECT_START_X = WIDTH - STEMHACK_PARAMETER_PANEL_BLACK_RECT_WIDTH - STEMHACK_PARAMETER_PANEL_LEFT_MARGIN - STEMHACK_PADDING

    elif size == "medium":
        PARALLEL_PARKING_STEPS = [99, 134, 254, 289, 334, 369, 489]  # medium
        WIDTH = 1100
        HEIGHT = 600
        FONT_SIZE = 32
        # stemhack parameter panel
        STEMHACK_PANEL_FONT_SIZE = 20
        STEMHACK_PADDING = 5
        STEMHACK_PARAMETER_PANEL_LEFT_MARGIN = 20
        STEMHACK_PARAMETER_PANEL_TEXT_HEIGHT = 25
        STEMHACK_PARAMETER_PANEL_BLACK_RECT_WIDTH = 250
        STEMHACK_PARAMETER_PANEL_YELLOW_RECT_WIDTH = STEMHACK_PARAMETER_PANEL_BLACK_RECT_WIDTH + 2 * STEMHACK_PADDING
        STEMHACK_PARAMETER_PANEL_BLACK_RECT_START_y = 20
        STEMHACK_PARAMETER_PANEL_YELLOW_RECT_START_y = STEMHACK_PARAMETER_PANEL_BLACK_RECT_START_y - STEMHACK_PADDING
        STEMHACK_PARAMETER_PANEL_BLACK_RECT_HEIGHT = 7 * STEMHACK_PARAMETER_PANEL_TEXT_HEIGHT  # 15 is number of lines (len(data)) in the pannel
        STEMHACK_PARAMETER_PANEL_YELLOW_RECT_HEIGHT = 7 * STEMHACK_PARAMETER_PANEL_TEXT_HEIGHT + 2 * STEMHACK_PADDING  # 15 is number of lines (len(data)) in the pannel

    elif size == "large":
        FONT_SIZE = 36
        PARALLEL_PARKING_STEPS = [160, 195, 340, 375, 485, 520, 665]  # large
        WIDTH = 1650
        HEIGHT = 900
        STEP_SIZE = (250, 75)
        CHECK_SIZE = (60, 60)
        STEP_GAP = 75

        # stemhack parameter panel
        STEMHACK_PANEL_FONT_SIZE = 14
        STEMHACK_PADDING = 5
        STEMHACK_PARAMETER_PANEL_LEFT_MARGIN = 20
        STEMHACK_PARAMETER_PANEL_TEXT_HEIGHT = 30
        STEMHACK_PARAMETER_PANEL_BLACK_RECT_WIDTH = 300
        STEMHACK_PARAMETER_PANEL_YELLOW_RECT_WIDTH = STEMHACK_PARAMETER_PANEL_BLACK_RECT_WIDTH + 2 * STEMHACK_PADDING
        STEMHACK_PARAMETER_PANEL_BLACK_RECT_START_y = 20
        STEMHACK_PARAMETER_PANEL_YELLOW_RECT_START_y = STEMHACK_PARAMETER_PANEL_BLACK_RECT_START_y - STEMHACK_PADDING
        STEMHACK_PARAMETER_PANEL_BLACK_RECT_HEIGHT = 7 * STEMHACK_PARAMETER_PANEL_TEXT_HEIGHT  # 15 is number of lines (len(data)) in the pannel
        STEMHACK_PARAMETER_PANEL_YELLOW_RECT_HEIGHT = 7 * STEMHACK_PARAMETER_PANEL_TEXT_HEIGHT + 2 * STEMHACK_PADDING  # 15 is number of lines (len(data)) in the pannel

    PARAMETER_PANEL_BLACK_RECT_START_X = WIDTH - PARAMETER_PANEL_BLACK_RECT_WIDTH - PARAMETER_PANEL_LEFT_MARGIN
    PARAMETER_PANEL_TEXT_START_X = WIDTH - PARAMETER_PANEL_BLACK_RECT_WIDTH - PARAMETER_PANEL_LEFT_MARGIN + PADDING
    PARAMETER_PANEL_YELLOW_RECT_START_X = WIDTH - PARAMETER_PANEL_BLACK_RECT_WIDTH - PARAMETER_PANEL_LEFT_MARGIN - PADDING

    STEMHACK_PARAMETER_PANEL_BLACK_RECT_START_X = WIDTH - STEMHACK_PARAMETER_PANEL_BLACK_RECT_WIDTH - STEMHACK_PARAMETER_PANEL_LEFT_MARGIN
    STEMHACK_PARAMETER_PANEL_TEXT_START_X = WIDTH - STEMHACK_PARAMETER_PANEL_BLACK_RECT_WIDTH - STEMHACK_PARAMETER_PANEL_LEFT_MARGIN + STEMHACK_PADDING * 2
    STEMHACK_PARAMETER_PANEL_YELLOW_RECT_START_X = WIDTH - STEMHACK_PARAMETER_PANEL_BLACK_RECT_WIDTH - STEMHACK_PARAMETER_PANEL_LEFT_MARGIN - STEMHACK_PADDING

    WHITE_LANE_WIDTH = round(sim_cfg.road.whiteLaneWidth * WIDTH / BASE_WIDTH)
    WHITE_LANE_HEIGHT = round(sim_cfg.road.whiteLaneHeight * HEIGHT / BASE_HEIGHT)
    WHITE_LANE_GAP = round(sim_cfg.road.whiteLaneGap * HEIGHT / BASE_HEIGHT)
    ROAD_LANE_WIDTH = round(sim_cfg.road.laneWidth * WIDTH / BASE_WIDTH)
    HORIZONTAL_LANE_WIDTH = round(sim_cfg.road.horizontalLaneWidth * WIDTH / BASE_WIDTH)
    HORIZONTAL_LANE_HEIGHT = round(sim_cfg.road.horizontalLaneThickness * HEIGHT / BASE_HEIGHT)
    HORIZONTAL_LANE_GAP = round(sim_cfg.road.horizontalLaneGap * HEIGHT / BASE_HEIGHT)
    HORIZONTAL_LANE_START_Y = round(sim_cfg.road.horizontalLaneStartY * HEIGHT / BASE_HEIGHT)
    TREES_WIDTH = round(sim_cfg.env_objects.TREES_WIDTH * WIDTH / BASE_WIDTH)
    TREES_GAP = round(sim_cfg.env_objects.TREES_GAP * HEIGHT / BASE_HEIGHT)
    TREES_START_POINT = round(sim_cfg.env_objects.TREES_START_POINT * HEIGHT / BASE_HEIGHT)
    HOUSES_WIDTH = round(sim_cfg.env_objects.house_width * WIDTH / BASE_WIDTH)
    HOUSES_GAP = round(sim_cfg.env_objects.house_gap * HEIGHT / BASE_HEIGHT)
    HOUSE_START_POINT = round(sim_cfg.env_objects.HOUSE_START_POINT * HEIGHT / BASE_HEIGHT)
    SIDEWALK_OBJECTS_WIDTH = round(sim_cfg.env_objects.sidewalk_object_width * WIDTH / BASE_WIDTH)
    SIDEWALK_OBJECTS_GAP_MIN = round(sim_cfg.env_objects.sidewalk_object_gap_min * HEIGHT / BASE_HEIGHT)
    SIDEWALK_OBJECTS_GAP_MAX = round(sim_cfg.env_objects.sidewalk_object_gap_max * HEIGHT / BASE_HEIGHT)
    SIDEWALK_OBJECTS_START_POINT = round(sim_cfg.env_objects.sidewalk_object_start_point * HEIGHT / BASE_HEIGHT)
    TURNING_RADIUS_MULTIPLIER = round(100 * HEIGHT / BASE_HEIGHT)
