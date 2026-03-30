"""Experiment 8: Check whether a grammar is an operator grammar."""


def not_operator_grammar() -> None:
    print("Not operator grammar")


def is_nonterminal(ch: str) -> bool:
    return len(ch) == 1 and ch.isupper()


def main() -> None:
    n = int(input("Enter number of productions: "))
    productions = [input().strip() for _ in range(n)]

    has_operator = False
    for prod in productions:
        if "=" not in prod:
            not_operator_grammar()
            return

        _, rhs = prod.split("=", 1)
        if "$" in rhs or rhs == "":
            not_operator_grammar()
            return

        for i, ch in enumerate(rhs):
            if ch in "+-*/":
                has_operator = True

            if i + 1 < len(rhs) and is_nonterminal(ch) and is_nonterminal(rhs[i + 1]):
                not_operator_grammar()
                return

    if has_operator:
        print("Operator grammar")
    else:
        not_operator_grammar()


if __name__ == "__main__":
    main()
