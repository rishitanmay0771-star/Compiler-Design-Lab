"""Experiment 7: Shift-reduce parsing for grammar E->E+E | E*E | (E) | id."""


def reduce_stack(stack: list[str]) -> list[str]:
    actions = []
    changed = True
    while changed:
        changed = False
        joined = "".join(stack)

        idx = joined.find("id")
        if idx != -1:
            stack[idx : idx + 2] = ["E"]
            actions.append("REDUCE TO E")
            changed = True
            continue

        for pattern in ("E+E", "E*E", "(E)"):
            idx = joined.find(pattern)
            if idx != -1:
                stack[idx : idx + len(pattern)] = ["E"]
                actions.append("REDUCE TO E")
                changed = True
                break

    return actions


def tokenize(text: str) -> list[str]:
    tokens: list[str] = []
    i = 0
    while i < len(text):
        if text[i : i + 2] == "id":
            tokens.append("id")
            i += 2
        elif not text[i].isspace():
            tokens.append(text[i])
            i += 1
        else:
            i += 1
    return tokens


def main() -> None:
    print("GRAMMAR is E->E+E")
    print("          E->E*E")
    print("          E->(E)")
    print("          E->id")

    raw = input("Enter input string: ").strip()
    tokens = tokenize(raw)

    stack: list[str] = []
    remaining = tokens[:]

    print("stack\t\tinput\t\taction")
    for tok in tokens:
        stack.append(tok)
        remaining.pop(0)
        print(f"${''.join(stack)}\t\t{''.join(remaining)}$\t\tSHIFT->{tok}")

        reductions = reduce_stack(stack)
        for action in reductions:
            print(f"${''.join(stack)}\t\t{''.join(remaining)}$\t\t{action}")

    if stack == ["E"]:
        print("\nString accepted")
    else:
        print("\nString not accepted")


if __name__ == "__main__":
    main()
