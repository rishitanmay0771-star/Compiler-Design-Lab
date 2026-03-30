"""Experiment 5: Compute FIRST and FOLLOW for a fixed grammar."""

from collections import defaultdict


PRODUCTIONS = {
    "E": ["TR"],
    "R": ["+TR", "#"],
    "T": ["FY"],
    "Y": ["*FY", "#"],
    "F": ["(E)", "i"],
}
START = "E"
EPS = "#"


def compute_first_sets() -> dict[str, set[str]]:
    first = defaultdict(set)

    changed = True
    while changed:
        changed = False
        for nt, rhs_list in PRODUCTIONS.items():
            before = len(first[nt])
            for rhs in rhs_list:
                if rhs == EPS:
                    first[nt].add(EPS)
                    continue

                nullable_prefix = True
                for sym in rhs:
                    if sym.isupper():
                        first[nt] |= (first[sym] - {EPS})
                        if EPS not in first[sym]:
                            nullable_prefix = False
                            break
                    else:
                        first[nt].add(sym)
                        nullable_prefix = False
                        break

                if nullable_prefix:
                    first[nt].add(EPS)

            if len(first[nt]) != before:
                changed = True

    return first


def first_of_string(s: str, first_sets: dict[str, set[str]]) -> set[str]:
    result: set[str] = set()
    if not s:
        result.add(EPS)
        return result

    nullable_prefix = True
    for sym in s:
        if sym.isupper():
            result |= (first_sets[sym] - {EPS})
            if EPS not in first_sets[sym]:
                nullable_prefix = False
                break
        else:
            result.add(sym)
            nullable_prefix = False
            break

    if nullable_prefix:
        result.add(EPS)
    return result


def compute_follow_sets(first_sets: dict[str, set[str]]) -> dict[str, set[str]]:
    follow = defaultdict(set)
    follow[START].add("$")

    changed = True
    while changed:
        changed = False
        for nt, rhs_list in PRODUCTIONS.items():
            for rhs in rhs_list:
                for i, sym in enumerate(rhs):
                    if not sym.isupper():
                        continue

                    suffix = rhs[i + 1 :]
                    suffix_first = first_of_string(suffix, first_sets)
                    before = len(follow[sym])
                    follow[sym] |= (suffix_first - {EPS})
                    if EPS in suffix_first or not suffix:
                        follow[sym] |= follow[nt]
                    if len(follow[sym]) != before:
                        changed = True

    return follow


def main() -> None:
    first_sets = compute_first_sets()
    follow_sets = compute_follow_sets(first_sets)

    order = ["E", "R", "T", "Y", "F"]
    for nt in order:
        vals = ", ".join(sorted(first_sets[nt]))
        print(f"First({nt}) = {{ {vals} }}")

    print("\n-----------------------------------------------\n")

    for nt in order:
        vals = ", ".join(sorted(follow_sets[nt]))
        print(f"Follow({nt}) = {{ {vals} }}")


if __name__ == "__main__":
    main()
