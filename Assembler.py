import os
import sys


NEW_LINE_W = "\r"
ADD = "a"
WRITE = "w"
FIRST_VAR = 16
READ = "r"
CLOSE_LABEL = ")"
SUFFIX = ".asm"
NUM_OF_BITS = 15
NULL = "null"
A_FIRST_BIT = "0"
C_FIRST_BIT = "1"
JUMP = ";"
EQUALS = "="
OPEN_LABEL = "("
AMPERSAT = "@"
NEW_LINE = "\n"
HACK_ENDING = ".hack"
COMMENT = "//"
FILE_SEPARATOR = "/"

"""
Holds the binary representation of the destination
"""
DEST_DICT = {
    "null": "000",
    "M": "001",
    "D": "010",
    "MD": "011",
    "A": "100",
    "AM": "101",
    "AD": "110",
    "AMD": "111"
}"""
Holds the binary representation of the computation
"""
COMP_DICT = {
    "0": "110101010",
    "1": "110111111",
    "-1": "110111010",
    "D": "110001100",
    "A": "110110000",
    "!D": "110001101",
    "!A": "110110001",
    "-D": "110001111",
    "-A": "110110011",
    "D+1": "110011111",
    "1+D": "110011111",
    "A+1": "110110111",
    "1+A": "110110111",
    "D-1": "110001110",
    "A-1": "110110010",
    "D+A": "110000010",
    "A+D": "110000010",
    "D-A": "110010011",
    "A-D": "110000111",
    "D&A": "110000000",
    "A&D": "110000000",
    "D|A": "110010101",
    "A|D": "110010101",
    "M": "111110000",
    "!M": "111110001",
    "-M": "111110011",
    "M+1": "111110111",
    "1+M": "111110111",
    "M-1": "111110010",
    "D+M": "111000010",
    "M+D": "111000010",
    "D-M": "111010011",
    "M-D": "111000111",
    "D&M": "111000000",
    "M&D": "111000000",
    "D|M": "111010101",
    "M|D": "111010101",
    "D<<": "010110000",
    "A<<": "010100000",
    "M<<": "011100000",
    "D>>": "010010000",
    "A>>": "010000000",
    "M>>": "011000000"
}

"""
Holds the binary representation of the jump
"""
JUMP_DICT = {
    "null": "000",
    "JGT": "001",
    "JEQ": "010",
    "JGE": "011",
    "JLT": "100",
    "JNE": "101",
    "JLE": "110",
    "JMP": "111"
}

"""
Holds the pre-defined addresses
"""
PREDEF_DICT = {
    "R0": 0,
    "R1": 1,
    "R2": 2,
    "R3": 3,
    "R4": 4,
    "R5": 5,
    "R6": 6,
    "R7": 7,
    "R8": 8,
    "R9": 9,
    "R10": 10,
    "R11": 11,
    "R12": 12,
    "R13": 13,
    "R14": 14,
    "R15": 15,
    "SCREEN": 16384,
    "KBD": 24576,
    "SP": 0,
    "LCL": 1,
    "ARG": 2,
    "THIS": 3,
    "THAT": 4
}


def parser(filename):
    """
    Parses the file by sections - creates the table which holds the addresses, sends
    each instruction to the suitable function and sends the final output to the output file
    :param filename: the name of the file
    """
    f = open(filename, READ)
    lines = f.readlines()
    symbol_table = PREDEF_DICT
    label_parser(lines, symbol_table)
    variable_parser(lines, symbol_table)
    instruction_parser(filename, lines, symbol_table)
    f.close()


def instruction_parser(filename, lines, symbol_table):
    """
    Chooses the suitable instruction
    :param filename: the name of the file
    :param lines: the lines of the file
    :param symbol_table: the table that holds all the addresses of the symbols
    """
    line_num = 0
    for line in lines:
        line = comments_and_space_remover(line)
        if len(line) != 0 and line[0] != OPEN_LABEL:
            if line[0] != AMPERSAT:
                output_line = parse_c_instruction(line)
            else:
                output_line = parse_a_instruction(line, symbol_table)
            write_output_file(line_num, filename, output_line)
            line_num += 1


def variable_parser(lines, symbol_table):
    """
    Adds the variables to the symbol table
    :param lines: the lines of the file
    :param symbol_table: the table that holds all the addresses of the symbols
    """
    symbol_num = FIRST_VAR
    for line in lines:
        line = comments_and_space_remover(line)
        if (len(line) > 0) and (line[0] == AMPERSAT):
            symbol = line[1:]
            if (symbol not in symbol_table) and (not symbol.isdigit()):
                symbol_table[symbol] = symbol_num
                symbol_num += 1


def label_parser(lines, symbol_table):
    """
    Adds the labels and their addresses to the symbol table
    :param lines: the lines of the file
    :param symbol_table: the table that holds all the addresses of the symbols
    """
    line_num = 0
    for line in lines:
        line = comments_and_space_remover(line)
        if len(line) != 0:
            if line[0] == OPEN_LABEL:
                for j in range(len(line)):
                    if line[j] == CLOSE_LABEL:
                        symbol_table[line[1:j]] = line_num
            else:
                line_num += 1


def comments_and_space_remover(line):
    """
    Removes the spaces and the comments
    :param line: the line which may have spaces and comments
    """
    line, sep, leftover = line.partition(COMMENT)
    line, sep, leftover = line.partition(NEW_LINE)
    line, sep, leftover = line.partition(NEW_LINE_W)
    line = line.strip()
    return line


def parse_c_instruction(line):
    """
    Creates the binary representation of the C instruction
    :param line: the line which holds the C instruction
    """
    output_line = C_FIRST_BIT
    for i, letter in enumerate(line):
        if letter == EQUALS:
            is_parsed = False
            for j in range(len(line) - i):
                if line[j] == JUMP:
                    output_line += COMP_DICT[line[i + 1:j]]
                    output_line += DEST_DICT[line[0:i]]
                    jump_inst = line[j:]
                    output_line += JUMP_DICT[jump_inst]
                    is_parsed = True
                    break
            if not is_parsed:
                output_line += COMP_DICT[line[i + 1:]]
                output_line += DEST_DICT[line[0:i]]
                output_line += JUMP_DICT[NULL]
            break
        if letter == JUMP:
            output_line += COMP_DICT[line[:i]]
            output_line += DEST_DICT[NULL]
            jump_inst = line[i + 1:]
            output_line += JUMP_DICT[jump_inst]
    return output_line


def parse_a_instruction(line, symbol_table):
    """
    Creates the binary representation of the A instruction
    :param line: the line which holds the A instruction
    """
    output_line = A_FIRST_BIT
    var_name = line[1:]
    if var_name in symbol_table.keys():
        decimal_num = int(symbol_table[var_name])
    else:
        decimal_num = int(var_name)
    output_line += bin(decimal_num)[2:].zfill(NUM_OF_BITS)
    return output_line

def write_output_file(line_num, file_name, output_line):
    """
    Creates the output file and writes the given line to the output file
    :param file_name: the name of the file
    :param output_line: the line to write in the output file
    """
    if line_num == 0:
        output_file = open(file_name[:-4] + HACK_ENDING, WRITE)
    else:
        output_file = open(file_name[:-4] + HACK_ENDING, ADD)
    output_file.write(output_line)
    output_file.write(NEW_LINE)
    output_file.close()

def main():
    input = sys.argv[1]
    if os.path.isdir(input):
        for file_name in os.listdir(input):
            if file_name.endswith(SUFFIX):
                parser(input + FILE_SEPARATOR + file_name)
    else:
        parser(input)
if __name__ == '__main__':
    main()





