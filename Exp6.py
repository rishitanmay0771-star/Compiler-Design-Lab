"""Experiment 6: Build LL(1) parsing table and parse an input string."""

from collections import defaultdict

EPS = "#"


def parse_grammar(count: int) -> dict[str, list[str]]:
    grammar: dict[str, list[str]] = defaultdict(list)
    print(f"Enter {count} productions in form A=alpha")
    for _ in range(count):
        p = input().strip()
        if "=" not in p or len(p) < 3:
            continue
        lhs, rhs = p.split("=", 1)
        lhs = lhs.strip()
        rhs = rhs.strip()
        if lhs:
            grammar[lhs[0]].append(rhs)
    return grammar


def first_of_string(s: str, first_sets: dict[str, set[str]], non_terminals: set[str]) -> set[str]:
    result: set[str] = set()
    if not s:
        return {EPS}

    nullable_prefix = True
    for ch in s:
        if ch in non_terminals:
            result |= (first_sets[ch] - {EPS})
            if EPS not in first_sets[ch]:
                nullable_prefix = False
                break
        else:
            result.add(ch)
            nullable_prefix = False
            break

    if nullable_prefix:
        result.add(EPS)
    return result


def compute_first(grammar: dict[str, list[str]]) -> dict[str, set[str]]:
    non_terminals = set(grammar.keys())
    first = defaultdict(set)

    changed = True
    while changed:
        changed = False
        for lhs, rhs_list in grammar.items():
            before = len(first[lhs])
            for rhs in rhs_list:
                if rhs == EPS:
                    first[lhs].add(EPS)
                    continue
                rhs_first = first_of_string(rhs, first, non_terminals)
                first[lhs] |= rhs_first
            if len(first[lhs]) != before:
                changed = True

    return first


def compute_follow(grammar: dict[str, list[str]], first: dict[str, set[str]], start: str) -> dict[str, set[str]]:
    non_terminals = set(grammar.keys())
    follow = defaultdict(set)
    follow[start].add("$")

    changed = True
    while changed:
        changed = False
        for lhs, rhs_list in grammar.items():
            for rhs in rhs_list:
                for i, ch in enumerate(rhs):
                    if ch not in non_terminals:
                        continue
                    suffix = rhs[i + 1 :]
                    sf = first_of_string(suffix, first, non_terminals)
                    before = len(follow[ch])
                    follow[ch] |= (sf - {EPS})
                    if EPS in sf or not suffix:
                        follow[ch] |= follow[lhs]
                    if len(follow[ch]) != before:
                        changed = True

    return follow


def terminals_of(grammar: dict[str, list[str]]) -> list[str]:
    nts = set(grammar.keys())
    terms: list[str] = []
    for rhs_list in grammar.values():
        for rhs in rhs_list:
            for ch in rhs:
                if ch not in nts and ch != EPS and ch not in terms:
                    terms.append(ch)
    if "$" not in terms:
        terms.append("$")
    return terms


def build_table(
    grammar: dict[str, list[str]],
    first: dict[str, set[str]],
    follow: dict[str, set[str]],
) -> dict[str, dict[str, str]]:
    nts = set(grammar.keys())
    table: dict[str, dict[str, str]] = {nt: {} for nt in grammar}

    for lhs, rhs_list in grammar.items():
        for rhs in rhs_list:
            rhs_first = first_of_string(rhs, first, nts)
            for t in (rhs_first - {EPS}):
                table[lhs][t] = f"{lhs}={rhs}"
            if EPS in rhs_first:
                for t in follow[lhs]:
                    table[lhs][t] = f"{lhs}={EPS}"

    return table


def print_sets(name: str, sets: dict[str, set[str]], order: list[str]) -> None:
    for nt in order:
        vals = ", ".join(sorted(sets[nt]))
        print(f"{name}({nt}) = {{ {vals} }}")


def print_table(table: dict[str, dict[str, str]], nts: list[str], terms: list[str]) -> None:
    print("\nLL(1) Parsing Table")
    header = "NT\\T".ljust(8) + "".join(t.ljust(12) for t in terms)
    print(header)
    print("-" * len(header))

    for nt in nts:
        row = nt.ljust(8)
        for t in terms:
            row += table.get(nt, {}).get(t, "").ljust(12)
        print(row)


def parse_input(
    table: dict[str, dict[str, str]],
    start: str,
    terms: list[str],
) -> None:
    s = input("\nPlease enter the input string (end with $): ").strip()
    if not s.endswith("$"):
        s += "$"

    stack = ["$", start]
    i = 0

    print("\nStack\t\tInput\t\tAction")
    while stack:
        top = stack[-1]
        cur = s[i] if i < len(s) else ""
        stack_view = "".join(stack)
        input_view = s[i:]

        if top == cur == "$":
            print(f"{stack_view}\t\t{input_view}\t\tAccept")
            print("String accepted by LL(1) parser")
            return

        if top not in table:
            if top == cur:
                stack.pop()
                i += 1
                print(f"{stack_view}\t\t{input_view}\t\tMatch {cur}")
            else:
                print(f"{stack_view}\t\t{input_view}\t\tError")
                print("String rejected by LL(1) parser")
                return
        else:
            prod = table.get(top, {}).get(cur)
            if not prod:
                print(f"{stack_view}\t\t{input_view}\t\tError")
                print("String rejected by LL(1) parser")
                return

            stack.pop()
            rhs = prod.split("=", 1)[1]
            if rhs != EPS:
                for ch in reversed(rhs):
                    stack.append(ch)
            print(f"{stack_view}\t\t{input_view}\t\t{prod}")


def main() -> None:
    count = int(input("How many productions? : "))
    grammar = parse_grammar(count)
    if not grammar:
        print("No valid productions were provided.")
        return

    nts = list(grammar.keys())
    start = nts[0]
    first = compute_first(grammar)
    follow = compute_follow(grammar, first, start)
    terms = terminals_of(grammar)
    table = build_table(grammar, first, follow)

    print()
    print_sets("First", first, nts)
    print("\n-----------------------------------------------\n")
    print_sets("Follow", follow, nts)
    print_table(table, nts, terms)
    parse_input(table, start, terms)


if __name__ == "__main__":
    main()
