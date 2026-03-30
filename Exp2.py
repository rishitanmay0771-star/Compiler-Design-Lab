"""Experiment 2: Simulation of NFA from a simple regular expression."""


def init_table(size: int = 50) -> list[list[str]]:
    return [[" " for _ in range(size)] for _ in range(size)]


def main() -> None:
    print("\n\t\t\tSIMULATION OF NFA")
    print("\t\t\t*****************")
    regex = input("\nEnter a regular expression: ").strip()

    t = init_table()
    r = 0
    c = 0
    n = len(regex)

    for i in range(n):
        ch = regex[i]
        if ch == "|" and i > 0 and i + 1 < n:
            t[r][r + 1] = "E"
            t[r + 1][r + 2] = regex[i - 1]
            t[r + 2][r + 5] = "E"
            t[r][r + 3] = "E"
            t[r + 4][r + 5] = "E"
            t[r + 3][r + 4] = regex[i + 1]
            r += 5
        elif ch == "*" and i > 0:
            t[r - 1][r] = "E"
            t[r][r + 1] = "E"
            t[r][r + 3] = "E"
            t[r + 1][r + 2] = regex[i - 1]
            t[r + 2][r + 1] = "E"
            t[r + 2][r + 3] = "E"
            r += 3
        elif ch == "+" and i > 0:
            t[r][r + 1] = regex[i - 1]
            t[r + 1][r] = "E"
            r += 1
        else:
            if c == 0:
                if i + 1 < n and regex[i].isalpha() and regex[i + 1].isalpha():
                    t[r][r + 1] = regex[i]
                    t[r + 1][r + 2] = regex[i + 1]
                    r += 2
                    c = 1
                c = 1
            elif c == 1:
                if i + 1 < n and regex[i + 1].isalpha():
                    t[r][r + 1] = regex[i + 1]
                    r += 1
                    c = 2
            else:
                if i + 1 < n and regex[i + 1].isalpha():
                    t[r][r + 1] = regex[i + 1]
                    r += 1
                    c = 3

    print()
    for j in range(r + 1):
        print(f"  {j}", end="")
    print("\n" + "_" * 35)

    for i in range(r + 1):
        row = "".join(f"  {t[i][j]}" for j in range(r + 1))
        print(f"{row}  | {i}")

    print(f"\nStart state: 0\nFinal state: {r}")


if __name__ == "__main__":
    main()
