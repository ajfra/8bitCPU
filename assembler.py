"""
Authors: Milind Kathiari & AJ Francese
Date: 12/5/2023
Pledge: I pledge my honor that I have abided by the Stevens Honor System.

Description: Assembler for the Maffamatix Masheen CPU.
"""

import sys
import os

class Instruction():
    """
    Instruction class to standardize the instruction format. Attributes include:
    name: name of the instruction
    opcode: opcode of the instruction
    """
    def __init__(self, name, opcode):
        self.name = name
        self.opcode = opcode
        
    @staticmethod
    def getInstructionParams(line):
        """_summary_
        Takes a line of the input file and returns the instruction and parameters.

        Args:
            line (string): input string of one line from the input file

        Returns:
            tuple: tuple pair of instruction and list of parameters.
        """
        #sanitize input
        line = line.strip().lower()
        line.replace(" ", "")
        
        #grab first three letters as instruction
        instruc = line[:3]
        
        #grab parameters
        params = line[3:].split(",")
        
        #sanitize parameters
        for i in range(len(params)):
            params[i] = params[i].strip()
        
        return instruc, params

    @staticmethod
    def getRAMData(file):
        """_summary_

        Args:
            file (_type_): _description_
        """
        dataFound = False
        ram = "ram.o"
        for line in file:
            if dataFound:
                #write data to file
                with open(ram, "w") as f:
                    f.write("v3.0 hex words addressed") #header for ram image file
                    line = line.strip().split(" ")
                    for i in range(len(line)):
                        if i % 6 == 0: #new line every 6 bytes
                            f.write("\n") 
                            f.write(hex(i)[2:].zfill(2) + ": ") #address
                        f.write(hex(int(line[i]))[2:].zfill(2) + " ") #data
                    f.write("\n") #new line at end of file
                    return
            elif line.strip().lower() == "data":
                dataFound = True
                continue
    
    @staticmethod
    def getCode(file):
        """_summary_

        Args:
            file (_type_): _description_
        """
        codeFound = False
        lines = []
        for line in file:
            if codeFound:
                lines.append(Instruction.getInstructionParams(line))                   
            else:
                if line.strip().lower() == "code":
                    codeFound = True
                    continue        
        return lines

if __name__ == "__main__":
    
    #remove files if they exist 
    try:
        os.remove("code.o")
        os.remove("ram.o")
    except FileNotFoundError:
        pass    
    
    # Definition of our 4 instructions
    str = Instruction("str", "00")
    ldr = Instruction("ldr", "01")
    add = Instruction("add", "10")
    sub = Instruction("sub", "11")

    #dictionary of instruction objects
    instructions = {"str": str, "ldr": ldr, "add": add, "sub": sub}
    
    #standardized string instruction size for modular instruction size.
    isize = 3
    
    #read file
    file = sys.argv[1]
    f = open(file, "r")
    
    #get ram data
    Instruction.getRAMData(f)
    
    #get code
    lines = Instruction.getCode(f)
    
    machinecode = []
    for i in lines:
        if len(i[1]) == 2:
            register = i[1][0]
            addr = i[1][1]
            machinecode.append(hex(int(instructions[i[0]].opcode + bin(int(register[-1]))[2:].zfill(2) + bin(int(addr))[2:].zfill(4), 2))[2:].zfill(2))
        if len(i[1]) == 3:
            treg = i[1][0]
            reg1 = i[1][1]
            reg2 = i[1][2]
            machinecode.append(hex(int(instructions[i[0]].opcode + bin(int(treg[-1]))[2:].zfill(2) + bin(int(reg1[-1]))[2:].zfill(2) + bin(int(reg2[-1]))[2:].zfill(2), 2))[2:].zfill(2))
    
    objfile = "code.o"
    with open(objfile, "w") as f:
        f.write("v3.0 hex words addressed") #header for code file 
        for i in range(len(machinecode)):
            if i % 6 == 0:
                f.write("\n") 
                f.write(hex(i)[2:].zfill(2) + ": ") #address
            f.write(machinecode[i] + " ")
        f.write("\n")

