def binaryToDNA(binary):
    DNA = ""
    for i in range(0, len(binary), 2):
        temp = binary[i] + binary[i+1]
        if (temp == '00'):
            DNA += 'A'
        if (temp == '01'):
            DNA += 'T'
        if (temp == '10'):
            DNA += 'C'
        if (temp == '11'):
            DNA += 'G'
    print(DNA)

def DNADecoder(DNA):
    binaryString = ""
    for i in range(0, len(DNA)):
        if (DNA[i] == 'A'):
            binaryString += '00'
        elif (DNA[i] == 'T'):
            binaryString += '01'
        elif (DNA[i] == 'C'):
            binaryString += '10'
        elif (DNA[i] == 'G'):
            binaryString += '11'
    return binaryString

def encodeBinary(msg):
    toBin = bin(int(msg, 2))[2:].zfill(len(msg))
    binaryToDNA(toBin)

def decodeBinary(DNA):
    print(DNADecoder(DNA))

def encodeHex(msg):
    toBin = bin(int(msg, 16))[2:].zfill(len(msg) * 4)
    binaryToDNA(toBin)

def decodeHex(DNA):
    print(hex(int(DNADecoder(DNA), 2)))

def encodeChars(msg):
    binaryMsg = bin(int.from_bytes(msg.encode(), 'big'))[2:].zfill(len(msg) * 8)
    print(binaryMsg)
    binaryToDNA(binaryMsg)

def decodeChars(DNA):
    binaryString = DNADecoder(DNA)
    binToInt = int(binaryString, 2)
    print(binToInt.to_bytes((binToInt.bit_length() + 7) // 8, 'big').decode())

def init(endec):
    if (endec == "encoding"):
        seqtype = input("Are you encoding from binary, hex, or characters (standard English alphabet, numbers, and spaces)? ")
        msg = input("Enter your %s: " % (seqtype))
        if (seqtype == "binary"):
            encodeBinary(msg)
        elif (seqtype == "hex"):
            encodeHex(msg)
        elif (seqtype == "characters"):
            encodeChars(msg)
        else: 
            print("Invalid encoding type")
    elif (endec == "decoding"):
        seqtype = input("Are you decoding to binary, hex, characters (standard English alphabet, numbers, and spaces)? ")
        msg = input("Enter the DNA to decode: ")
        if (seqtype == "binary"):
            decodeBinary(msg)
        elif (seqtype == "hex"):
            decodeHex(msg)
        elif (seqtype == "characters"):
            decodeChars(msg)
        else: 
            print("Invalid decoding type")

init(input("Are you decoding a DNA sequence or encoding a DNA sequence? "))