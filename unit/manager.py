import time
from unit.unit import LETTERS

class UnitManager(object):
    def __init__(self, units):
        self.__units = units

    def move_to_letters(self, letters):
        if len(letters) > len(self.__units):
            print(f'[more letters then units]')
            return
        
        distances = {} 
        # max_distance = 0
        for unit_idx, letter in enumerate(letters):
            if letter.upper() not in LETTERS:
                print(f'[invalid letter]')
                return
            distances[unit_idx] = self.__units[unit_idx].get_distance_to_letter(letter)
        
        curr_distance = [0 for _ in self.__units]
        while True:
            units_moved = 0
            for unit_idx, unit in enumerate(self.__units):
                if curr_distance[unit_idx] >= distances[unit_idx]:
                    continue
                    
                movement = 11
                if curr_distance[unit_idx] + movement > distances[unit_idx]:
                    movement = distances[unit_idx] - curr_distance[unit_idx] 

                unit.move_motor(movement)
                curr_distance[unit_idx] += movement
                units_moved += 1
            
            if units_moved == 0:
                break
            
        # for unit_idx, distance in distances.items():
        #     self.__units[unit_idx].move_motor(distance)
    
    # TODO: Add interleave
    def reset_units(self):
        adj = [3, 9]
        for idx, unit in enumerate(self.__units):
            unit.reset(adj[idx])
            time.sleep_ms(100)
