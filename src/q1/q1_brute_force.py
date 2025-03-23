from itertools import combinations
from collections import defaultdict

winners: defaultdict[int, list[tuple[list[int], list[int]]]] = defaultdict(list)
highest_score = 0

def main():
    global highest_score
    global winners

    die_faces = [i for i in range(1, 13)]

    test = [test for test in combinations(combinations(die_faces, 6), 2)]
    
    for die1, die2 in test:
        try:
            score = 0
            
            for roll1 in die1:
                if roll1 in die2:
                    raise StopIteration
                
                for roll2 in die2:
                    if roll2 in die1:
                        raise StopIteration
                    
                    if (roll1 + roll2) % 13 == 0:
                        score += 1
                        
            if score >= highest_score:
                # if len(winners[score]) < 20:
                winners[score].append((die1, die2))
                highest_score = score
        except StopIteration:
            pass
        
    best_score = max(winners.keys())
    best_rolls = winners[best_score]
                
    # for score, rolls in winners.items():
    for roll in best_rolls:
        print(f"{best_score} - {roll}")
        
    print(f"done. {sum(len(rolls) for rolls in winners.values())} total")
        

if __name__ == "__main__":
    main()
