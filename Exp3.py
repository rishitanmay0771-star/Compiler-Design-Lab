"""Experiment 3: Convert NFA to DFA using subset construction and test strings."""

from collections import deque


def bits_to_states(mask: int, st: int) -> str:
    if mask == 0:
        return "q0"
    items = [f"q{j}" for j in range(st) if mask & (1 << j)]
    return " ".join(items)


def main() -> None:
    print("Follow one-based indexing style from the original experiment.")
    st = int(input("Enter number of states: "))

    print(f"Give state numbers from 0 to {st - 1}")
    fin = int(input("Enter number of final states: "))
    finals = [int(input(f"Final state {i + 1}: ")) for i in range(fin)]

    rel = int(input("Enter number of transition rules in NFA: "))
    print('Define rule as: "initial_state input_symbol final_state"')

    dfa = [[[0 for _ in range(st)] for _ in range(2)] for _ in range(st)]
    for _ in range(rel):
        p, q, r = map(int, input().split())
        if q in (0, 1) and 0 <= p < st and 0 <= r < st:
            dfa[p][q][r] = 1

    initial = int(input("Enter initial state: "))
    initial_mask = 1 << initial

    go: dict[int, list[int]] = {}
    discovered: set[int] = set()
    queue: deque[int] = deque()

    for i in range(st):
        src = 1 << i
        go[src] = [0, 0]
        for sym in range(2):
            target = 0
            for k in range(st):
                if dfa[i][sym][k] == 1:
                    target |= 1 << k
            go[src][sym] = target

        discovered.add(src)
        if go[src][0] not in discovered:
            discovered.add(go[src][0])
            queue.append(go[src][0])
        if go[src][1] not in discovered:
            discovered.add(go[src][1])
            queue.append(go[src][1])

    while queue:
        curr = queue.popleft()
        if curr not in go:
            go[curr] = [0, 0]

        for sym in range(2):
            nxt = 0
            for k in range(st):
                if curr & (1 << k):
                    nxt |= go.get(1 << k, [0, 0])[sym]
            go[curr][sym] = nxt
            if nxt not in discovered:
                discovered.add(nxt)
                queue.append(nxt)

    print("\nThe distinct DFA states are:")
    print("STATE         0    1")
    for mask in sorted(discovered):
        if mask not in go:
            go[mask] = [0, 0]
        label = bits_to_states(mask, st)
        print(f"{label:<12} {go[mask][0]:<4} {go[mask][1]:<4}")

    for _ in range(3):
        s = input("\nEnter binary string: ").strip()
        curr = initial_mask
        print("Path:", end=" ")
        print(f"{curr}-", end="")

        valid = True
        for ch in s:
            if ch not in "01":
                valid = False
                break
            curr = go.get(curr, [0, 0])[int(ch)]
            print(f"{curr}-", end="")
        print()

        if not valid:
            print("Invalid input: only 0 and 1 are allowed")
            continue

        accepted = any(curr & (1 << f) for f in finals)
        print(f"Final state mask: {curr}")
        print("String Accepted" if accepted else "String Rejected")


if __name__ == "__main__":
    main()
