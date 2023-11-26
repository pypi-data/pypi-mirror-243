import mathstrovehiclesim.globals

from .vehicle import Vehicle


class SingleTargetAhead(Vehicle):
    def __init__(self, p_image, lane_borders, lane=0, p_bottom_pos=(0,0), p_init_lat_spd=0, p_init_lng_spd=0, p_max_spd=30, p_cycle_limit=1000, is_motorcycle=False, set_top=False):
        super().__init__(p_image, lane_borders, p_bottom_pos, p_init_lat_spd, p_init_lng_spd, p_max_spd, is_motorcycle, set_top=set_top)

        # set target speed
        self.set_speed(self.vy)

        # set target lane
        self.go_to_lane(lane)

        # simulation attributes
        self.status = 1  # (1; active, -1: terminate)
        self.cycle = 0
        self.cycle_limit = p_cycle_limit

    def update(self, p_host_spd):
        if self.status == 1:
            # update longitudinal position based on relative speed
            self.rect.centery = self.rect.centery + (p_host_spd - self.vy)
            # check if deactivate vehicle
            if self.rect.top > mathstrovehiclesim.globals.HEIGHT or self.cycle > self.cycle_limit:
                self.status = -1

        if self.status == -1:
            self.terminate(p_host_spd)

    def terminate(self, p_host_spd):
        if self.rect.top > mathstrovehiclesim.globals.HEIGHT:
            self.kill()
        else:
            self.vy = int(p_host_spd * 2)
            self.rect.centery = self.rect.centery + (p_host_spd - self.vy)
            if self.rect.bottom < 0:
                if mathstrovehiclesim.globals.DEBUG:
                    print("kill")
                self.kill()


# I don't think that we need this class anymore
class MultipleTargetAhead:
    def __init__(self, p_images, lane_borders, number_of_vehicles=2, lane=0, p_bottom_pos=(0,0), p_init_lng_spd=0, p_max_spd=30, p_cycle_limit=1000, gap=mathstrovehiclesim.globals.ROAD_LANE_WIDTH * 0.4):
        self.p_images = p_images
        self.lane_borders = lane_borders
        self.vehicle_list = []

        start_point = p_bottom_pos[1]
        other_vehicle_height = 0
        for i in range(number_of_vehicles):
            temp = SingleTargetAhead(self.p_images[i], self.lane_borders,
                                     p_bottom_pos=(0,start_point + other_vehicle_height),
                                     p_init_lng_spd=0, is_motorcycle=False, p_max_spd=p_max_spd, p_cycle_limit=p_cycle_limit)
            temp.set_speed(p_init_lng_spd)
            temp.go_to_lane(lane)

            temp_width, temp_height = temp.get_size()
            other_vehicle_height += gap + temp_height

            self.vehicle_list.append(temp)
