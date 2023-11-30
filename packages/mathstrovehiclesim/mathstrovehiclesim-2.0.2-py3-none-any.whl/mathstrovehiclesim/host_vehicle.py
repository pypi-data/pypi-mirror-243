from .vehicle import Vehicle


class HostVehicle(Vehicle):
    def __init__(self, p_image, lane_borders, lane=0, p_bottom_pos=(0,0), p_init_lat_spd=0, p_init_lng_spd=0, p_max_spd=30, p_cycle_limit=1000, is_motorcycle=False):
        if p_init_lng_spd < 0:
            raise ValueError("Initial speed should be positive number!")

        if type(p_init_lng_spd) is not int:
            raise TypeError("The initial speed should be an integer!")

        super().__init__(p_image, lane_borders, p_bottom_pos, p_init_lat_spd, p_init_lng_spd, p_max_spd, is_motorcycle)

        # set target speed
        self.set_speed(self.vy)

        # set target lane
        self.go_to_lane(lane)

        # simulation attributes
        self.status = 1  # (1; active, -1: terminate)
        self.cycle = 0
        self.cycle_limit = p_cycle_limit
        self.off_road_left = False
        self.off_road_right = False

    def update(self, action):
        if action == "speed_up":
            self.speed_up()
        elif action == "speed_down":
            self.speed_down()
        elif action == "shift_left":
            self.off_road_left = self.move_left()
            if self.off_road_left:
                print("ERROR: Car went off road from left side")
        elif action == "shift_right":
            self.off_road_right = self.move_right()
            if self.off_road_right:
                print("ERROR: Car went off road from right side")
        elif action == "stop":
            self.stop()
        elif action == "headlight_on":
            self.headlight_on()
        elif action == "headlight_off":
            self.headlight_off()
        elif action == "turn_right":
            self.turn_right()
        elif action == "turn_left":
            self.turn_left()
        elif action == "forward":
            self.forward()
        elif action == "reverse":
            self.reverse()
        elif action == "":
            pass
        else:
            print(f"WARNING: the given action ({action}) is not recognized!")
            pass

    # renders the host vehicle on the display

    def render(self, screen):
        screen.blit(self.image, self.get_rect_position())
