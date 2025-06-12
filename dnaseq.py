def binaryToDNA(binary):
    # If we got an odd number, let's just add a 0 at the end to make it work
    if len(binary) % 2 != 0:
        binary += '0'
        print("Warning: Odd number of bits detected. Padding with '0' to ensure valid encoding.")
    
    DNA = ""
    # Walk through the binary string 2 bits at a time
    for i in range(0, len(binary), 2):
        temp = binary[i:i+2]  

        # This is our encoding scheme: 00->A, 01->T, 10->C, 11->G
        if temp == '00':
            DNA += 'A'
        elif temp == '01':  
            DNA += 'T'
        elif temp == '10':
            DNA += 'C'
        elif temp == '11':
            DNA += 'G'
    
    
    if 'AAAA' in DNA:
        print("Warning: Sequence contains AAAA, which might be unstable in practical applications.")
    
    print(DNA)
    return DNA  # Return the DNA string so other functions can use it

def DNADecoder(DNA):
    binaryString = ""
    # Go through each letter in the DNA sequence
    for i in range(len(DNA)):

        # This is our decoding scheme: A->00, T->01, C->10, G->11
        if DNA[i] == 'A':
            binaryString += '00'
        elif DNA[i] == 'T':
            binaryString += '01'
        elif DNA[i] == 'C':
            binaryString += '10'
        elif DNA[i] == 'G':
            binaryString += '11'
        else:
            print(f"Warning: Invalid nucleotide '{DNA[i]}' detected. Replacing with 'A' (00).")
            binaryString += '00'
    
    
    if len(DNA) % 4 != 0:
        print("Note: This sequence might have been padded during encoding.")
    
    return binaryString

def encodeBinary(msg):
    # First, make sure we actually have a valid binary string (just 0s and 1s)
    if not all(bit in '01' for bit in msg):
        print("Error: Input contains non-binary characters. Using only '0' and '1'.")

        msg = ''.join(bit for bit in msg if bit in '01')
    
    
    if not msg:
        print("Error: No valid binary digits found.")
        return
    
    
    binaryToDNA(msg)

def decodeBinary(DNA):
    
    binary = DNADecoder(DNA)
    print(binary)
    return binary

def encodeHex(msg):
    try:
        
        if msg.lower().startswith('0x'):
            msg = msg[2:]
        
        # Check if what we have left is actually valid hex
        int(msg, 16)
        toBin = bin(int(msg, 16))[2:].zfill(len(msg) * 4)
        return binaryToDNA(toBin)
    except ValueError:
        print("Error: Invalid hexadecimal input.")
        return None

def decodeHex(DNA):
    try:
        # First get the binary representation
        binary = DNADecoder(DNA)
        # Then convert that binary to a hex string
        hexValue = hex(int(binary, 2))
        print(hexValue)
        return hexValue
    except ValueError:
        print("Error: Could not convert to hexadecimal.")
        return None

def encodeChars(msg):
    # Can't encode an empty string!
    if not msg:
        print("Error: Empty input.")
        return
    
    try:
        # This is some fancy Python magic to convert text to binary:
        # 1. msg.encode() turns the string into bytes
        # 2. int.from_bytes(..., 'big') turns those bytes into one big number
        # 3. bin(...)[2:] converts that number to binary and removes the '0b' prefix
        # 4. zfill(...) adds leading zeros to ensure each character has exactly 8 bits
        binaryMsg = bin(int.from_bytes(msg.encode(), 'big'))[2:].zfill(len(msg) * 8)
        print(f"Binary representation: {binaryMsg}")
        return binaryToDNA(binaryMsg)
    except UnicodeEncodeError:
        # Some exotic characters might not encode well
        print("Error: Input contains characters that cannot be encoded.")
        return None

def decodeChars(DNA):
    try:
        # First, get the binary string from DNA
        binaryString = DNADecoder(DNA)
        
        # Convert the binary string back to an integer
        binToInt = int(binaryString, 2)
        
        # Convert the integer back to bytes and then to a string
        # The (binToInt.bit_length() + 7) // 8 calculates how many bytes we need
        text = binToInt.to_bytes((binToInt.bit_length() + 7) // 8, 'big').decode()
        print(f"Decoded text: {text}")
        return text
    except (ValueError, OverflowError):
        # If our binary doesn't make sense as a number
        print("Error: Binary sequence cannot be converted to text.")
        return None
    except UnicodeDecodeError:
        # If our bytes don't make sense as text
        print("Error: Decoded bytes do not represent valid text.")
        return None

def analyze_dna_practicality(dna):
    """Let's check if this DNA sequence would work well in the real world."""
    issues = []
    
    # In real DNA, having too many of the same letter in a row can cause problems
    # DNA polymerase (the copying enzyme) can "slip" on repetitive sequences
    for nucleotide in 'ATCG':
        if nucleotide * 4 in dna:  # Four or more in a row
            issues.append(f"Contains {nucleotide * 4} which may cause replication issues")
    
    # The GC content (percentage of G's and C's) matters a lot for DNA stability
    # G-C pairs have 3 hydrogen bonds (stronger) while A-T pairs have only 2
    gc_count = dna.count('G') + dna.count('C')
    gc_percent = (gc_count / len(dna)) * 100 if dna else 0
    
    # Too few G's and C's? DNA might be too weak
    if gc_percent < 20:
        issues.append(f"Low GC content ({gc_percent:.1f}%) may reduce stability")
    # Too many G's and C's? DNA might be too hard to separate during replication
    elif gc_percent > 80:
        issues.append(f"High GC content ({gc_percent:.1f}%) may be difficult to replicate")
    
    # Palindromic sequences can be problematic because they can fold back on themselves
    # This creates "hairpins" that interfere with normal DNA processing
    # Let's look for 6-letter palindromes (common restriction enzyme sites)
    for i in range(len(dna) - 5):
        segment = dna[i:i+6]
        # DNA palindromes are special - they match when one strand is flipped AND complemented
        # A matches with T, and C matches with G when strands are antiparallel
        complement = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
        rev_comp = ''.join(complement.get(n, n) for n in reversed(segment))
        if segment == rev_comp:
            issues.append(f"Contains palindromic sequence {segment} which may form secondary structures")
            break
    
    return issues

def init():
    # Welcome screen
    print("DNA Encoder/Decoder Tool")
    print("========================")
    print("Convert between DNA and other formats!")
    
    # Main program loop
    while True:
        # Show main menu
        print("\nWhat would you like to do today?")
        print("1. Encode to DNA (turn regular data into DNA)")
        print("2. Decode from DNA (turn DNA back into regular data)")
        print("3. Analyze DNA sequence practicality (is this DNA sequence biologically realistic?)")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ")
        
        # ENCODING: Convert normal data to DNA
        if choice == '1':
            print("\nWhat kind of data are you starting with?")
            print("1. Binary (just 0s and 1s)")
            print("2. Hexadecimal (0-9 and A-F)")
            print("3. Text (normal letters, numbers, etc.)")
            
            encode_choice = input("\nEnter your choice (1-3): ")
            
            if encode_choice == '1':
                msg = input("Type your binary string (just 0s and 1s): ")
                encodeBinary(msg)
            elif encode_choice == '2':
                msg = input("Type your hexadecimal string (0-9, A-F): ")
                encodeHex(msg)
            elif encode_choice == '3':
                msg = input("Type your text message: ")
                encodeChars(msg)
            else:
                print("Hmm, that wasn't one of the options. Let's try again.")
        
        # DECODING: Convert DNA back to normal data
        elif choice == '2':
            print("\nWhat do you want to convert your DNA back into?")
            print("1. Binary (just 0s and 1s)")
            print("2. Hexadecimal (0-9 and A-F)")
            print("3. Text (normal letters, numbers, etc.)")
            
            decode_choice = input("\nEnter your choice (1-3): ")
            if decode_choice not in ['1', '2', '3']:
                print("Hmm, that wasn't one of the options. Let's try again.")
                continue

            dna = input("Type in your DNA sequence (just A, T, C, G letters): ").upper()
            
            # Make sure we got a valid DNA sequence
            if not all(n in 'ATCG' for n in dna):
                print("Warning: Your sequence has letters other than A, T, C, and G. This might not work well.")
            
            if decode_choice == '1':
                decodeBinary(dna)
            elif decode_choice == '2':
                decodeHex(dna)
            elif decode_choice == '3':
                decodeChars(dna)
        
        # ANALYZING: Check if DNA sequence would work in real life
        elif choice == '3':
            dna = input("Type in the DNA sequence you want to analyze: ").upper()
            issues = analyze_dna_practicality(dna)
            
            if issues:
                print("\nHeads up! Some potential issues with this DNA sequence:")
                for issue in issues:
                    print(f"- {issue}")
            else:
                print("\nGood news! This DNA sequence looks practical from a biological perspective.")
                
        # EXIT: End the program
        elif choice == '4':
            print("Thanks for using the DNA Encoder/Decoder Tool! Goodbye!")
            break
        
        else:
            print("Hmm, that wasn't one of the options. Let's try again.")

if __name__ == "__main__":
    init()