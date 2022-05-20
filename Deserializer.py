
import struct
import array

# Luac File
LuaC_File_Name = "output.luac"

# Reading the bytecode
BytecodeFile = open(LuaC_File_Name, "rb") # Read as binary
bytecode = BytecodeFile.read()

"""
Important Notes:

1- This Deserializer is written for Lua 5.1.x (5.1.5 mainly but it works for other versions).
2- This is probably buggy, so please report any bugs you find.

"""


# ------ START OF ENUMS ------
OPCODE = {
    "Move":        0,
    "Loadk":       1,
    "LoadBool":    2,
    "LoadNil":     3,
    "GetUpval":    4,
    "GetGlobal":   5,
    "GetTable":    6,
    "SetGlobal":   7,
    "SetUpval":    8,
    "SetTable":    9,
    "NewTable":   10,
    "Self":       11,
    "Add":        12,
    "Sub":        13,
    "Mul":        14,
    "Div":        15,
    "Mod":        16,
    "Pow":        17,
    "Unm":        18,
    "Not":        19,
    "Len":        20,
    "Concat":     21,
    "Jmp":        22,
    "Eq":         23,
    "Lt":         24,
    "Le":         25,
    "Test":       26,
    "TestSet":    27,
    "Call":       28,
    "TailCall":   29,
    "Return":     30,
    "ForLoop":    31,
    "ForPrep":    32,
    "TForLoop":   33,
    "SetList":    34,
    "Close":      35,
    "Closure":    36,
    "Vararg":     37
}

OPNAME = [
    "Move",
    "Loadk",
    "LoadBool",
    "LoadNil",
    "GetUpval",
    "GetGlobal",
    "GetTable",
    "SetGlobal",
    "SetUpval",
    "SetTable",
    "NewTable",
    "Self",
    "Add",
    "Sub",
    "Mul",
    "Div",
    "Mod",
    "Pow",
    "Unm",
    "Not",
    "Len",
    "Concat",
    "Jmp",
    "Eq",
    "Lt",
    "Le",
    "Test",
    "TestSet",
    "Call",
    "TailCall",
    "Return",
    "ForLoop",
    "ForPrep",
    "TForLoop",
    "SetList",
    "Close",
    "Closure",
    "VarArg"
]

INSTRUCTIONTYPE = { #  I want to look cool B)
    "ABC": "ABC",
    "ABx": "ABx",
    "AsBx": "AsBx",
}

CONSTANTTYPE = { #  I want to look cool B)
    "Nil": "Nil",
    "Boolean": "Boolean",
    "Number": "Number",
    "String": "String",
}

INSTRUCTIONMAP = {
    OPCODE["Move"]:       INSTRUCTIONTYPE["ABC"],
    OPCODE["Loadk"]:      INSTRUCTIONTYPE["ABx"],
    OPCODE["LoadBool"]:   INSTRUCTIONTYPE["ABC"],
    OPCODE["LoadNil"]:    INSTRUCTIONTYPE["ABC"],
    OPCODE["GetUpval"]:   INSTRUCTIONTYPE["ABC"],
    OPCODE["GetGlobal"]:  INSTRUCTIONTYPE["ABx"],
    OPCODE["GetTable"]:   INSTRUCTIONTYPE["ABC"],
    OPCODE["SetGlobal"]:  INSTRUCTIONTYPE["ABx"],
    OPCODE["SetUpval"]:   INSTRUCTIONTYPE["ABC"],
    OPCODE["SetTable"]:   INSTRUCTIONTYPE["ABC"],
    OPCODE["NewTable"]:   INSTRUCTIONTYPE["ABC"],
    OPCODE["Self"]:       INSTRUCTIONTYPE["ABC"],
    OPCODE["Add"]:        INSTRUCTIONTYPE["ABC"],
    OPCODE["Sub"]:        INSTRUCTIONTYPE["ABC"],
    OPCODE["Mul"]:        INSTRUCTIONTYPE["ABC"],
    OPCODE["Div"]:        INSTRUCTIONTYPE["ABC"],
    OPCODE["Mod"]:        INSTRUCTIONTYPE["ABC"],
    OPCODE["Pow"]:        INSTRUCTIONTYPE["ABC"],
    OPCODE["Unm"]:        INSTRUCTIONTYPE["ABC"],
    OPCODE["Not"]:        INSTRUCTIONTYPE["ABC"],
    OPCODE["Len"]:        INSTRUCTIONTYPE["ABC"],
    OPCODE["Concat"]:     INSTRUCTIONTYPE["ABC"],
    OPCODE["Jmp"]:        INSTRUCTIONTYPE["AsBx"],
    OPCODE["Eq"]:         INSTRUCTIONTYPE["ABC"],
    OPCODE["Lt"]:         INSTRUCTIONTYPE["ABC"],
    OPCODE["Le"]:         INSTRUCTIONTYPE["ABC"],
    OPCODE["Test"]:       INSTRUCTIONTYPE["ABC"],
    OPCODE["TestSet"]:    INSTRUCTIONTYPE["ABC"],
    OPCODE["Call"]:       INSTRUCTIONTYPE["ABC"],
    OPCODE["TailCall"]:   INSTRUCTIONTYPE["ABC"],
    OPCODE["Return"]:     INSTRUCTIONTYPE["ABC"],
    OPCODE["ForLoop"]:    INSTRUCTIONTYPE["AsBx"],
    OPCODE["ForPrep"]:    INSTRUCTIONTYPE["AsBx"],
    OPCODE["TForLoop"]:   INSTRUCTIONTYPE["ABC"],
    OPCODE["SetList"]:    INSTRUCTIONTYPE["ABC"],
    OPCODE["Close"]:      INSTRUCTIONTYPE["ABC"],
    OPCODE["Closure"]:    INSTRUCTIONTYPE["ABx"],
    OPCODE["Vararg"]:     INSTRUCTIONTYPE["ABC"]
}
# ----------------- END OF ENUMS -----------------

# CLASSES.PY START
class Instruction:
    Name   = None
    Type   = None
    Chunk  = None
    Opcode = None
    A      = None
    B      = None
    C      = None
    Line   = None
    Data   = None

    def __init__(self, C, Opc):
        self.Chunk  = C
        self.Opcode = Opc
        self.Name   = OPNAME[Opc];
        self.Type   = INSTRUCTIONMAP[Opc];

    def __getitem__(self, key):
        return getattr(self,key)

    def __setitem__(self, key, value):
        setattr(self,key,value)

class Constant:
    Data = None
    Type = None

    def __getitem__(self, key):
        return getattr(self,key)

    def __setitem__(self, key, value):
        setattr(self,key,value)

class Chunk:
    Name            = ""
    Line            = 0
    LastLine        = 0
    UpvalCount      = 0
    ParameterCount  = 0
    VarargCount     = 0
    StackSize       = 0

    Upvalues        = []
    Instructions    = []
    Constants       = []
    Prototypes      = []
    ConstantRef     = []


    def __init__(self, c):
        self.Name           = c["Name"]
        self.Line           = c["Line"]
        self.LastLine       = c["LastLine"]
        self.UpvalCount     = c["UpvalCount"]
        self.ParameterCount = c["ParameterCount"]
        self.VarargCount     = c["VarargCount"]
        self.StackSize      = c["StackSize"]

    def SetInstructionsLine(self, num, key):
        self.Instructions[num]["Line"] = key

    def __getitem__(self, key):
        return getattr(self,key)

    def __setitem__(self, key, value):
        setattr(self,key,value)

class Deserializer:
    def __init__(self, BTInput):
        self.input       = BTInput
        self.Index       = 4 # Skipping the header
        self.VMVersion   = None # Version of the VM i tested in Lua 5.1.5 0x51(81)
        self.BCFormat    = None # Bytecode format
        self.bigEndian   = None # Big endian or little endian
        self.IntSize     = None # Int size in bytes
        self.sizeT       = None # 
        self.InstrSize   = None # gets size of instructions
        self.LNumSize    = None # size of lua_Number
        self.FlagCount   = None # Number of flags

    def loadBlock(self, sz) -> bytearray: # stole the code
        if self.Index + sz > len(self.input):
            raise Exception("Malformed bytecode!")

        temp = bytearray(self.input[self.Index:self.Index+sz])
        self.Index = self.Index + sz
        #print("Temp: " + str(temp)) # DEBUG
        return temp

    def ReadByte(self) -> int:
        return self.loadBlock(1)[0]

    def ReadInt32(self, bigEndian = False) -> int:
        if (bigEndian):
            return int.from_bytes(self.loadBlock(4), byteorder='big', signed=False)
        else:
            return int.from_bytes(self.loadBlock(4), byteorder='little', signed=False)

    def GetSizeT(self) -> int:
        if (self.bigEndian):
            return int.from_bytes(self.loadBlock(self.sizeT), byteorder='big', signed=False)
        else:
            return int.from_bytes(self.loadBlock(self.sizeT), byteorder='little', signed=False)

    def ReadDouble(self) -> int:
        if self.bigEndian:
            return struct.unpack('>d', self.loadBlock(8))[0]
        else:
            return struct.unpack('<d', self.loadBlock(8))[0]

    def ReadString(self, size) -> str:
        if (size == None):
            size = self.GetSizeT()
            if (size == 0):
                return ""

        return "".join(chr(x) for x in self.loadBlock(size))
    
    def DecodeInstructions(self, c):
        li = []
        Sizecode = self.ReadInt32()
        
        for Idx in range(Sizecode):
            code = self.ReadInt32()
            Opco = (code & 0x3F)
            i = Instruction(c, Opco)

            i.__setitem__("Data", code)
            i.__setitem__("A", (code >> 6) & 0xFF)

            InstrType = i.Type
            #print("InstrType: ", InstrType)

            # Finding the instructions
            if InstrType == INSTRUCTIONTYPE["ABC"]:
                i.__setitem__("B", (code >> 6 + 8 + 9) & 0x1FF)
                i.__setitem__("C", (code >> 6 + 8) & 0x1FF)
            elif InstrType == INSTRUCTIONTYPE["ABx"]:
                i.__setitem__("B", (code >> 6 + 8) & 0x3FFFF)
            elif InstrType == INSTRUCTIONTYPE["AsBx"]:
                i.__setitem__("B", ((code >> 6 + 8) & 0x3FFFF) - 131071)
            li.append(i)
        return li

    def DecodeConstants(self):
        li = []
        Sizek = self.ReadInt32()

        for Idx in range(Sizek):
            Type = self.ReadByte()
            Cons = Constant()

            # Finding the constant Data and Type
            if Type == 0: # NIL
                Cons.__setitem__("Type", CONSTANTTYPE["Nil"])
                Cons.__setitem__("Data", None)
            elif Type == 1: # BOOLEAN
                Cons.__setitem__("Type", CONSTANTTYPE["Boolean"])
                Cons.__setitem__("Data", self.ReadByte() != 0)
            elif Type == 3: # NUMBER
                Cons.__setitem__("Type", CONSTANTTYPE["Number"])
                Cons.__setitem__("Data", self.ReadDouble())
            elif Type == 4: # STRING
                pppp = self.ReadString(None)
                Cons.__setitem__("Type", CONSTANTTYPE["String"])
                Cons.__setitem__("Data", pppp[:-1])
            li.append(Cons)
        return li
    
    def DecodePrototypes(self):
        li = []
        Sizep = self.ReadInt32()
        
        for Idx in range(Sizep):
            li.append(self.DecodeChunk())
        return li
    
    def DecodeChunk(self):
        #print("===== DecodeChunk =====")
        c = Chunk({
            "Name":            self.ReadString(None)[:-1], # might be a bug idk probably my skill issue
            "Line":            self.ReadInt32(),
            "LastLine":        self.ReadInt32(),
            "UpvalCount":    self.ReadByte(),
            "ParameterCount":  self.ReadByte(),
            "VarargCount":      self.ReadByte(),
            "StackSize":       self.ReadByte(),
        })
        
        c.__setitem__("Instructions", self.DecodeInstructions(c))
        c.__setitem__("Constants", self.DecodeConstants())
        c.__setitem__("Prototypes", self.DecodePrototypes())

        for Idx in range(len(c["Instructions"])): # Constant Refs. i think its not important so its not implemented
            pass 
        
        count = self.ReadInt32()
        for i in range(count): # Source line pos
            c.SetInstructionsLine(i, self.ReadInt32())
        

        count = self.ReadInt32()
        for i in range(count): # local list
            l1 = self.ReadString(None)
            l2 = self.ReadInt32()
            l3 = self.ReadInt32()

        count = self.ReadInt32()
        for i in range(count): # Upvalue
            Upvalue = self.ReadString(None)[:-1]
            c["Upvalues"].append(Upvalue)
            #print("Upvalues: ", c["Upvalues"]) # upvalues
        
        return c
    
    def RunDeserializer(self): # Main function

        self.VMVersion = self.ReadByte()
        self.BCFormat  = self.ReadByte()
        self.bigEndian = (self.ReadByte() == 0)
        self.IntSize   = self.ReadByte()
        self.sizeT     = self.ReadByte()
        #print("SizeT: ", self.sizeT)
        self.InstrSize = self.ReadByte() 
        self.LNumSize  = self.ReadByte()
        self.FlagCount = self.ReadByte()

        return self.DecodeChunk()


# Running the deserializer
LuaChunk = Deserializer(bytecode).RunDeserializer()

"""

Don't forget to DEBUG this file to read the LuaChunk data


"""


print("DONE")
