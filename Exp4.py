"""Experiment 4: Left recursion elimination and recursive descent parsing demo."""


def eliminate_left_recursion(production: str) -> None:
    if "->" not in production:
        print("Invalid production format. Use A->Aalpha|beta")
        return

    lhs, rhs = production.split("->", 1)
    lhs = lhs.strip()
    alternatives = [x.strip() for x in rhs.split("|") if x.strip()]

    left = []
    non_left = []
    for alt in alternatives:
        if alt.startswith(lhs):
            left.append(alt[len(lhs) :])
        else:
            non_left.append(alt)

    if not left:
        print("The given grammar has no immediate left recursion.")
        return

    lhs_dash = f"{lhs}'"
    print("Productions after eliminating left recursion:")
    for beta in non_left:
        print(f"{lhs}->{beta}{lhs_dash}")
    for alpha in left:
        print(f"{lhs_dash}->{alpha}{lhs_dash}")
    print(f"{lhs_dash}->@")


class RecursiveDescentParser:
    """Grammar:
    E  -> T EP
    EP -> + T EP | @
    T  -> F TP
    TP -> * F TP | @
    F  -> (E) | ID
    """

    def __init__(self, text: str) -> None:
        self.text = text
        self.i = 0

    def current(self) -> str:
        if self.i < len(self.text):
            return self.text[self.i]
        return ""

    def consume_identifier(self) -> bool:
        if self.current().isalpha():
            while self.current().isalpha() or self.current().isdigit() or self.current() == "_":
                self.i += 1
            return True
        return False

    def E(self) -> bool:
        return self.T() and self.EP()

    def EP(self) -> bool:
        if self.current() == "+":
            self.i += 1
            return self.T() and self.EP()
        return True

    def T(self) -> bool:
        return self.F() and self.TP()

    def TP(self) -> bool:
        if self.current() == "*":
            self.i += 1
            return self.F() and self.TP()
        return True

    def F(self) -> bool:
        if self.current() == "(":
            self.i += 1
            ok = self.E() and self.current() == ")"
            if ok:
                self.i += 1
            return ok
        return self.consume_identifier()


def recursive_descent_demo() -> None:
    print("Recursive descent parsing for grammar:")
    print("E->TEP")
    print("EP->+TEP|@")
    print("T->FTP")
    print("TP->*FTP|@")
    print("F->(E)|ID")

    s = input("Enter the string to check (append $ at end): ").strip()
    if not s.endswith("$"):
        s += "$"

    parser = RecursiveDescentParser(s)
    accepted = parser.E() and parser.current() == "$"
    print("String is accepted" if accepted else "String is not accepted")


def main() -> None:
    print("1. Eliminate Immediate Left Recursion")
    print("2. Recursive Descent Parsing")
    choice = input("Enter choice (1/2): ").strip()

    if choice == "1":
        prod = input("Enter production (example A->Aa|b): ").strip()
        eliminate_left_recursion(prod)
    elif choice == "2":
        recursive_descent_demo()
    else:
        print("Invalid choice")


if __name__ == "__main__":
    main()
