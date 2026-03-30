"""Experiment 1: Identify operators, keywords, and identifiers from a source file."""

from pathlib import Path


KEYWORDS = {
    "auto",
    "break",
    "case",
    "char",
    "const",
    "continue",
    "default",
    "do",
    "double",
    "else",
    "enum",
    "extern",
    "float",
    "for",
    "goto",
    "if",
    "int",
    "long",
    "register",
    "return",
    "short",
    "signed",
    "sizeof",
    "static",
    "struct",
    "switch",
    "typedef",
    "union",
    "unsigned",
    "void",
    "volatile",
    "while",
}

OPERATORS = set("+-*/%=")


def process_token(token: str) -> None:
    if not token:
        return
    if token in KEYWORDS:
        print(f"{token} is keyword")
    else:
        print(f"{token} is identifier")


def main() -> None:
    source = Path("program.txt")
    if not source.exists():
        print("program.txt not found in current directory.")
        return

    data = source.read_text(encoding="utf-8", errors="ignore")
    token = []

    for ch in data:
        if ch in OPERATORS:
            print(f"{ch} is operator")

        if ch.isalnum() or ch == "_":
            token.append(ch)
        else:
            process_token("".join(token))
            token.clear()

    process_token("".join(token))


if __name__ == "__main__":
    main()
