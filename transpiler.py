import sys
import os
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
    indent: int = 0
    indents: list[int] = [0]
    enterscope = False

    with (open(infilename) as infile,
          open(outfilename, "w") as outfile):
        for lineno, line in enumerate(infile, start=1):
            # We don't want blank lines to be detected as "\n"
            if line[-1] == "\n":
                line = line[:-1]

            realline = line.strip(" ")

            if realline == "": # blank line
                outfile.write("\n")
                continue

            indent = get_indent(line)

            if enterscope:
                indents.append(indent)
                enterscope = False
            elif indent != indents[-1]:
                if indent not in indents:
                    raise TranspilerError("Indentation error", lineno, realline)
                while indent != indents.pop():
                    pass
                indents.append(indent)
                if not (len(line) and line[indent] == "}"):
                    outfile.write(" " * indent + "}\n")

            if realline.startswith("goto "):
                raise TranspilerError("No gotos thanks", lineno, realline)

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

    print(f"Transpiling {infilename} to {outfilename} ...")

    tempfilename = ".krazyc-transpile." + outfilename # don't expose partially transpiled file

    try:
        transpile(infilename, tempfilename)
    except TranspilerError as e:
        print(e)
        os.remove(tempfilename)
    else:
        os.replace(tempfilename, outfilename)

if __name__ == "__main__":
    if len(sys.argv) not in (2, 3):
        print("Usage: python3 transpiler INFILE [OUTFILE]")
        exit(1)

    infilename = sys.argv[1]
    outfilename = None
    if len(sys.argv) == 3:
        outfilename = sys.argv[2]
    transpile_file(infilename, outfilename)
