import sys
from typing import Optional

print("KrazyC Transpiler")

def get_indent(line: str) -> int:
    return len(line) - len(line.lstrip(" "))

def transpile(infilename: str, outfilename: Optional[str] = None):
    if outfilename is None:
        outfilename = "".join(infilename.split(".")[:-1]) + ".c"
    print(f"Transpiling {infilename} to {outfilename} ...")

    indent: int = 0
    indents: list[int] = [0]
    enterscope = False

    with (open(infilename) as infile,
          open(outfilename, "w") as outfile):
        for line in infile:
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
                    raise SyntaxError(("Indentation error on:", line))
                while indent != indents.pop():
                    pass
                indents.append(indent)
                outfile.write(" " * indent + "}\n")
                
            if len(line) and line[-1] == ":":
                line = line[:-1] + " {"
                enterscope = True

            outfile.write(line + "\n")

        for indent in reversed(indents[:-1]):
            outfile.write(" " * indent + "}\n")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 transpiler [INFILE]")
        exit(1)

    infilename = sys.argv[1]
    transpile(infilename)
