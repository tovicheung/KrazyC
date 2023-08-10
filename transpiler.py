import sys
from typing import Optional

print("KrazyC Transpiler")

class TranspilerError(Exception):
    def __init__(self, message, lineno, line):
        self.message = message
        self.lineno = lineno
        self.line = line

    def __str__(self):
        ret = "Transpiler Error:\n" + \
        f"    {self.message}\n" + \
        f"Line {self.lineno} | {self.line}\n"
        return ret

def get_indent(line: str) -> int:
    return len(line) - len(line.lstrip(" "))

def transpile(infilename: str, outfilename: str):
    print(f"Transpiling {infilename} to {outfilename} ...")

    indent: int = 0
    indents: list[int] = [0]
    enterscope = False

    with (open(infilename) as infile,
          open(outfilename, "w") as outfile):
        for lineno, line in enumerate(infile):
            # We don't want blank lines to be detected as "\n"
            if line[-1] == "\n":
                line = line[:-1]

            if line.strip(" ") == "": # blank line
                outfile.write("\n")
                continue

            indent = get_indent(line)

            if enterscope:
                indents.append(indent)
                enterscope = False
            elif indent != indents[-1]:
                if indent not in indents:
                    raise TranspilerError("Indentation error", lineno, line)
                while indent != indents.pop():
                    pass
                indents.append(indent)
                if not (len(line) and line[indent] == "}"):
                    outfile.write(" " * indent + "}\n")
                
            if len(line) and line[-1] == ":":
                line = line[:-1] + " {"
                enterscope = True
            elif len(line) and line[-1] == "{":
                enterscope = True

            outfile.write(line + "\n")

        for indent in reversed(indents[:-1]):
            outfile.write(" " * indent + "}\n")

def transpile_file(infilename: str, outfilename: Optional[str] = None):
    if outfilename is None:
        outfilename = "".join(infilename.split(".")[:-1]) + ".c"
    try:
        transpile(infilename, outfilename)
    except TranspilerError as e:
        print(e)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 transpiler [INFILE]")
        exit(1)

    infilename = sys.argv[1]
    transpile_file(infilename)
