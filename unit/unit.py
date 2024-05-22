LETTERS = [' ', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '$', '&', '#', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ':', '.', '-', '?', '!']
NUM_FLAPS = 45
LETTER_STEP = 11.3

class Unit(object):
    def __init__(self, motor, motor_id, sensor):
        self.__motor = motor
        self.__motor_id = motor_id
        self.__sensor = sensor
        self.__current_position = 0
        self.__d = {}
        self.__letter_dict()

    def move_to_letter(self, letter):
        if letter.upper() not in LETTERS:
            return 

        target_position = self.__d[letter.upper()]
        if target_position < self.__current_position:
            distance = (NUM_FLAPS - self.__current_position + target_position) * LETTER_STEP 
        else:
            distance = (target_position - self.__current_position) * LETTER_STEP 

        print(f'[letter={letter},distance={int(distance)},remainder={distance - int(distance)}]')
        self.__current_position = target_position
        self.__motor.move(distance)
    
    # FIXME: Remove this method, because it's only for initial tests
    def move_motor(self, distance):
        print(f'[moving motor={self.__motor_id} distance={distance}]')
        self.__motor.move(distance, delay=1)

    def get_distance_to_letter(self, letter):
        if letter.upper() not in LETTERS:
            return 

        target_position = self.__d[letter.upper()]
        if target_position < self.__current_position:
            distance = (NUM_FLAPS - self.__current_position + target_position) * LETTER_STEP 
        else:
            distance = (target_position - self.__current_position) * LETTER_STEP 

        print(f'[letter={letter},distance={int(distance)},remainder={distance - int(distance)}]')
        self.__current_position = target_position
        return distance

    def reset(self, adjustment):
        print(f'[roaming motor={self.__motor_id} to find magnet]')
        while True:
            value = self.__sensor.get_value()
            # print(f'[sensor={self.__motor_id} value={value}]')
            if value == 0:
                self.__motor.move_forward(delay=1)
            else:
                break

        print(f'[calibrating motor={self.__motor_id}]')
        while True:
            value = self.__sensor.get_value()
            # print(f'[sensor={self.__motor_id} value={value}]')
            if value == 1:
                self.__motor.move_forward(delay=1)
            else:
                self.__motor.move(adjustment)
                break

    def __letter_dict(self):
        for idx, letter in enumerate(LETTERS):
            self.__d[letter] = idx
