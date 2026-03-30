import random
import time

MIN_PER_RANK = 1
MAX_PER_RANK = 5
MIN_RANKS = 3
MAX_RANKS = 5
PERCENT = 30

def generate_dag():
    random.seed(time.time())
    
    nodes = 0
    ranks = random.randint(MIN_RANKS, MAX_RANKS)

    print("DIRECTED ACYCLIC GRAPH")

    for i in range(1, ranks):
        new_nodes = random.randint(MIN_PER_RANK, MAX_PER_RANK)

        for j in range(nodes):
            for k in range(new_nodes):
                if random.randint(0, 99) < PERCENT:
                    print(f"{j}->{k + nodes};")

        nodes += new_nodes

# Run
generate_dag()
