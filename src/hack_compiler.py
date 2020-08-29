"""
------------------------------------------------------------------------------
    @file       hack_compiler.py
    @author     Milos Milicevic (milosh.mkv@gmail.com)
    @brief      Tool bar.
    @version    0.1
    @date       2020-08-29
    @copyright 	Copyright (c) 2020
    
    Distributed under the MIT software license, see the accompanying
    file COPYING or http://www.opensource.org/licenses/mit-license.php.
------------------------------------------------------------------------------
"""
import re
import sys

class InternalException(Exception):
    pass

class InvalidSyntaxException(Exception):
    pass

class HackAssemblyCompiler(object):

    def __init__(self, hack_assembly_file, out_file):

        self.__hack_assembly_file      = hack_assembly_file
        self.__hack_assembly_out_file  = out_file

        self.rewind()

    def rewind(self):
        self.SYMBOLS = { "R0": 0, "R1": 1, "R2" :  2, "R3" :  3, "R4" :  4, "R5" :  5, "R6" : 6,  "R7" :  7, 
                         "R8": 8, "R9": 9, "R10": 10, "R11": 11, "R12": 12, "R13": 13, "R14": 14, "R15": 15, 
                         "SCREEN": 16384, "KBD": 24576, "SP": 0, "LCL": 1, "ARG": 2, "THIS": 3, "THAT": 4  }

        self.NEXT_SYMBOL_VALUE = 16

        self.DESTINATIONS = { "NULL": "000", "M" : "001", "D" : "010", "MD" : "011", 
                              "A"   : "100", "AM": "101", "AD": "110", "AMD": "111" }

        self.JUMPS = { "NULL": "000", "JGT": "001", "JEQ": "010", "JGE": "011", "JLT": "100", 
                       "JNE" : "101", "JLE": "110", "JMP": "111" }

        self.COMPARISONS = { "0"  : "0101010", "1"  : "0111111", "-1" : "0111010", "D"  : "0001100",
                             "A"  : "0110000", "!D" : "0001101", "!A" : "0110001", "-D" : "0001111",
                             "-A" : "0110011", "D+1": "0011111", "A+1": "0110111", "D-1": "0001110",
                             "A-1": "0110010", "D+A": "0000010", "D-A": "0010011", "A-D": "0000111",
                             "D&A": "0000000", "D|A": "0010101", "M"  : "1110000", "!M" : "1110001",
                             "-M" : "1110011", "M+1": "1110111", "M-1": "1110010", "D+M": "1000010",
                             "D-M": "1010011", "M-D": "1000111", "D&M": "1000000", "D|M": "1010101",
                             "M+D": "1000010" }

        self.__hack_assembly_file_content           = []
        self.__hack_assembly_compiled_code          = []
        self.__hack_assembly_program_counter_buffer = {}
        self.__hack_assembly_program_counter        = 0
        self.__hack_assembly_current_line           = 1
        self.__load_hack_assembly_file_content()

    def add_new_symbol(self, symbol_name, value=None):

        if symbol_name in self.SYMBOLS.keys():
            return

        if value:
            self.SYMBOLS[symbol_name] = value
        else:
            self.SYMBOLS[symbol_name] = self.NEXT_SYMBOL_VALUE
            self.NEXT_SYMBOL_VALUE += 1

    def get_symbol_value(self, symbol_name):

        try:
            return self.SYMBOLS[symbol_name]
        except Exception as e:
            raise V3_Internal_Exception("Cannot locate symbol: {0}".format(e))
            # print("Cannot find symbol [{0}] in symbols!".format(e))

    def __load_hack_assembly_file_content(self):

        try:
            with open(self.__hack_assembly_file, "r") as hack_assembly_file:
                self.__hack_assembly_file_content = hack_assembly_file.read().split("\n")
        except Exception as exception:
            raise Exception(exception)

    def compile(self):
        self.__process_labels()
        self.__process_code()
        self.__write_to_file_output()

    def __write_to_file_output(self):
        with open(self.__hack_assembly_out_file, "w") as file:
            for l in self.__hack_assembly_compiled_code:
                file.write(l+"\n")

    def __process_code(self):

        for full_line in self.__hack_assembly_file_content:

            line = full_line.replace(" ", "").split("//")[0]
            # Check if it is comment or white space or label
            if not line or re.match(r"(\([a-zA-Z.:$_]+\)$|\([a-zA-Z.:$_][a-zA-Z0-9.:$_]+\)$)", line):
                # print(full_line + "\t Line: ", self.__hack_assembly_current_line)
                pass
            # Check if it is A instruction
            elif re.match(r"(@[a-zA-Z.:$_]+$|@[a-zA-Z.:$_][a-zA-Z0-9.:$_]+$|@[0-9]+$)", line):

                symbol_name = line[1:]

                if symbol_name.isdigit():
                    number = int(symbol_name)
                else:
                    self.add_new_symbol(symbol_name)
                    number = self.get_symbol_value(symbol_name)

                try:
                    binary_value = "0" + self.get_15_bit_binary_value_for_number(number)
                except Exception as e:
                    raise V3_Invalid_Syntax_Exception("{0}:{1}".format(self.__hack_assembly_current_line, str(e)))
                self.__hack_assembly_compiled_code.append(binary_value)
                # print(line +"\t Line: ", self.__hack_assembly_current_line, "\t" + binary_value)

            # Here should go C instructions
            else:

                destination = None; comparison = None; jump = None

                if re.match(r".+=.+;.+", line):

                    destination_end = re.search("=", line).start()
                    destination = line[:destination_end]

                    comparison_end  = re.search(";", line).start()
                    comparison  = line[destination_end + 1 : comparison_end]

                    jump = line[comparison_end + 1 : ]

                elif re.match(r".+=.+", line):

                    destination_end = re.search("=", line).start()
                    destination = line[:destination_end]

                    comparison  = line[destination_end + 1 : ]

                elif re.match(r".+;.+", line):

                    comparison_end  = re.search(";", line).start()
                    comparison  = line[ : comparison_end]

                    jump = line[comparison_end + 1 : ]

                else:
                    raise V3_Invalid_Syntax_Exception("{0}:{1}".format(self.__hack_assembly_current_line, line))

                try:
                    destination_binary = self.DESTINATIONS[destination] if destination is not None else self.DESTINATIONS["NULL"]
                    comparison_binary = self.COMPARISONS[comparison] if comparison is not None else self.COMPARISONS["NULL"]
                    jump_binary = self.JUMPS[jump] if jump is not None else self.JUMPS["NULL"]
                except:
                    raise V3_Invalid_Syntax_Exception("{0}:{1}".format(self.__hack_assembly_current_line, line))

                binary_value = "111" + comparison_binary + destination_binary + jump_binary
                self.__hack_assembly_compiled_code.append(binary_value)

            self.__hack_assembly_current_line += 1


    def get_15_bit_binary_value_for_number(self, number):

        number = "{0:b}".format(number)

        if len(number) > 15:
            raise Exception("You can only use 15bit numbers!")

        while len(number) < 15:
            number = "0" + number

        return number

    def __process_labels(self):        

        for line in self.__hack_assembly_file_content:

            line = line.replace(" ", "")

            if re.match(r"\/\/.+$", line) or not line:
                self.__hack_assembly_current_line += 1
                continue

            if re.match(r"(\([a-zA-Z.:$_]+\)$|\([a-zA-Z.:$_][a-zA-Z0-9.:$_]+\)$)", line):
                self.add_new_symbol(line[1:-1], self.__hack_assembly_program_counter)
                self.__hack_assembly_current_line += 1
                continue

            self.__hack_assembly_program_counter_buffer[self.__hack_assembly_program_counter] = self.__hack_assembly_current_line
            self.__hack_assembly_program_counter += 1
            self.__hack_assembly_current_line += 1

        # Reset program counter
        self.__hack_assembly_program_counter = 0
        self.__hack_assembly_current_line    = 1

    @property
    def binary_data(self):
        return self.__hack_assembly_compiled_code
    
    @property
    def program_counter_and_lines(self):
        return self.__hack_assembly_program_counter_buffer