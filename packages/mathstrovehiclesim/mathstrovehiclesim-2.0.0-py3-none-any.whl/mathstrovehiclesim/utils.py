from easydict import EasyDict as edict

import mathstrovehiclesim.globals


def calculate_roadside_area_width(remained_width, grass_area_ratio, sidewalk_area_ratio):
    grass_area_width = remained_width / (2 * (grass_area_ratio + sidewalk_area_ratio))
    sidewalk_area_width = grass_area_width * (sidewalk_area_ratio / grass_area_ratio)
    return edict({
        "grass_area_width": grass_area_width,
        "sidewalk_area_width": sidewalk_area_width
    })


def get_sidewalk_x_loc(screen_width, grass_area_width, grass_area_ratio, sidewalk_area_ratio, pos_mode, left_side=False):
    if left_side:
        return screen_width - grass_area_width * (grass_area_ratio + sidewalk_area_ratio * 0.75) + pos_mode * grass_area_width * (sidewalk_area_ratio * 0.5)
    else:
        return grass_area_width * (grass_area_ratio + sidewalk_area_ratio * 0.75) - pos_mode * grass_area_width * (sidewalk_area_ratio * 0.5)


def get_lane_borders(start_point, num_lane):
    return [(start_point + i * (mathstrovehiclesim.globals.ROAD_LANE_WIDTH + mathstrovehiclesim.globals.WHITE_LANE_WIDTH), start_point + (i + 1) * mathstrovehiclesim.globals.ROAD_LANE_WIDTH + i * mathstrovehiclesim.globals.WHITE_LANE_WIDTH) for i in range(0, num_lane)]


def get_lane(p_x_coord, lane_borders):
    result = -1
    lane_number = 0
    for lane in lane_borders:
        if lane[0] <= p_x_coord <= lane[1]:
            result = lane_number
            break

        lane_number += 1

    return result


def get_lane_coordinate(p_lane_num, lane_borders):
    result = -1
    if p_lane_num < len(lane_borders):
        temp = lane_borders[p_lane_num]
        result = (temp[0] + temp[1]) / 2

    return result


def is_lane_available(p_x_coord, lane_borders, side):
    if side == "left":
        return get_lane(p_x_coord, lane_borders) > 0
    elif side == "right":
        return get_lane(p_x_coord, lane_borders) < (len(lane_borders) - 1)


def is_on_screen(p_x_coord, p_y_coord):
    result = False
    if 0 <= p_x_coord <= mathstrovehiclesim.globals.WIDTH and 0 <= p_y_coord <= mathstrovehiclesim.globals.HEIGHT:
        result = True
    return result
