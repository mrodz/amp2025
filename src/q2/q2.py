from abc import ABC, abstractmethod
from collections import defaultdict
import math
import matplotlib.pyplot as plt
import random
from typing import Optional

class Strategy(ABC):
    @abstractmethod
    def get_tiles(self, index: int) -> list[int]:
        ...

    @abstractmethod
    def name(self) -> str:
        ...


SPY_CAN_MOVE_N_TILES = 1
MIN_K = 2 * SPY_CAN_MOVE_N_TILES + 1
"""
let Q_N = the set of possible spy positions after N days 
let x = the cardinality Q_{N+1} \ Q_{N}
K = x/2 + 1
"""
K = 10


class Bastion:
    spy_index: int
    
    def __init__(self, spy_slot: Optional[int] = None):
        if spy_slot is not None:
            self.spy_index = spy_slot
        else:
            self.spy_index = random.randint(1, 100)
            
    def __str__(self) -> str:
        return f"Spy is at {self.spy_index}"

    def __move(self, move_type: int):
        self.spy_index += move_type
        
        if self.spy_index > 100:
            self.spy_index = 1
        elif self.spy_index < 1:
            self.spy_index = 100
            
    def move(self, n: Optional[int] = None):
        if n is None:
            move_type = random.randint(-SPY_CAN_MOVE_N_TILES, SPY_CAN_MOVE_N_TILES)
        else:
            move_type = n
        self.__move(move_type)

    def eliminate(self, slots: Strategy, index: int) -> bool:
        return self.spy_index in slots.get_tiles(index)


class MinMaxStrategy(Strategy):
    def name(self) -> str:
        return "Min-Max"
    
    def get_tiles(self, index: int) -> list[int]:
        if K % 2 == 0:
            breadth = K // 2 - SPY_CAN_MOVE_N_TILES
            
            if breadth <= 0:
                raise ValueError(breadth)

            floor = list(range(1 + index * breadth, 6 + index * breadth))
            ceil = list(range(96 - index * breadth, 101 - index * breadth))
            return floor + ceil
        else:
            breadth_a = math.floor(K / 2) - SPY_CAN_MOVE_N_TILES
            breadth_b = math.ceil(K / 2) - SPY_CAN_MOVE_N_TILES
            
            if breadth_a < 0 or breadth_b < 0:
                raise ValueError(breadth_a, breadth_b)
            
            floor = list(range(1 + index * breadth_a, 6 + index * breadth_a))
            ceil = list(range(96 - index * breadth_b, 101 - index * breadth_b))
            return floor + ceil
    

class BreadthKMinusOneStrategy(Strategy):
    def name(self) -> str:
        return "Breadth K-1"
    
    def get_tiles(self, index: int) -> list[int]:
        start = ((1 + (index) * (K - 1) - 1) % 100) + 1
        end = ((start + K - 2) % 100) + 1

        if start <= end:
            return list(range(start, end + 1))
        else:
            return list(range(start, 101)) + list(range(1, end + 1))


FAIL_AFTER_N_DAYS = 10000
ITERATIONS_FOR_EACH_TEST = 1_000


def all_advance_edge_case(strategy: Strategy):
    days_taken = defaultdict(int)

    for i in range(1, 101):
        bastion = Bastion(i)
        
        for i in range(FAIL_AFTER_N_DAYS):
            bastion.move(SPY_CAN_MOVE_N_TILES)
            if bastion.eliminate(strategy, i):
                days_taken[i + 1] += 1
                break
        else:
            raise RuntimeWarning("The spy was not found")
        
    plt.scatter(days_taken.keys(), days_taken.values())

    plt.xlabel(f'Days to catch spy')
    plt.ylabel('Frequency')
    plt.title(f'Distribution of Bastion Pursuit Data with {strategy.name()} Strategy (K={K}, Spy Moves +{SPY_CAN_MOVE_N_TILES})')

    plt.show()


def test_breadthk1_chase_edge_case():
    strategy = BreadthKMinusOneStrategy()
    
    bastion = Bastion(4)
    
    for i in range(FAIL_AFTER_N_DAYS):
        bastion.move(1)
        
        print(f"day {i + 1}, {bastion}, {strategy.get_tiles(i)}")
        if bastion.eliminate(strategy, i):
            print(f"Finished on day {i + 1}")
            break
    else:
        raise RuntimeWarning("The spy was not found")    
    

def main():
    strategy = MinMaxStrategy()

    all_advance_edge_case(strategy)

    days_taken = []

    for i in range(1, 101):        
        for _ in range(ITERATIONS_FOR_EACH_TEST):
            bastion = Bastion(i)

            for i in range(FAIL_AFTER_N_DAYS):
                bastion.move()
                if bastion.eliminate(strategy, i):
                    days_taken.append(i + 1)
                    break
            else:
                raise RuntimeWarning("The spy was not found")

    _fig, ax = plt.subplots()

    ax.hist(days_taken, bins="auto")

    ax.set_xlabel(f'Days to catch spy')
    ax.set_ylabel('Frequency')
    ax.set_title(f'Distribution of Bastion Pursuit Data with {strategy.name()} Strategy (K={K}, Spy Moves Randomly ±{SPY_CAN_MOVE_N_TILES})')

    ax.set_yscale('log')

    plt.show()


if __name__ == "__main__":
    main()
