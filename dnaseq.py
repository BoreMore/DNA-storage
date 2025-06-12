def binaryToDNA(binary):
    binary_to_dna = {'00': 'A', '01': 'T', '10': 'C', '11': 'G'}

    if len(binary) % 2 != 0:
        binary += '0'
        print("Warning: Odd number of bits detected. Padding with '0' to ensure valid encoding.")

    DNA = ""
    for i in range(0, len(binary), 2):
        pair = binary[i:i+2]
        DNA += binary_to_dna.get(pair, 'A')  # Defaults to 'A' for unexpected bits

    if 'AAAA' in DNA:
        print("Warning: Sequence contains AAAA, which might be unstable in practical applications.")

    print(DNA)
    return DNA


def DNADecoder(DNA):
    dna_to_binary = {'A': '00', 'T': '01', 'C': '10', 'G': '11'}

    binaryString = ""
    for n in DNA:
        if n not in dna_to_binary:
            print(f"Warning: Invalid nucleotide '{n}' detected. Replacing with 'A' (00).")
        binaryString += dna_to_binary.get(n, '00')

    if len(DNA) % 4 != 0:
        print("Note: This sequence might have been padded during encoding.")

    return binaryString


def encodeBinary(msg):
    if not all(bit in '01' for bit in msg):
        print("Error: Input contains non-binary characters. Using only '0' and '1'.")
        msg = ''.join(bit for bit in msg if bit in '01')

    if not msg:
        print("Error: No valid binary digits found.")
        return

    return binaryToDNA(msg)


def decodeBinary(DNA):
    binary = DNADecoder(DNA)
    print(binary)
    return binary


def encodeHex(msg):
    try:
        if msg.lower().startswith('0x'):
            msg = msg[2:]
        int(msg, 16)  # validation
        toBin = bin(int(msg, 16))[2:].zfill(len(msg) * 4)
        return binaryToDNA(toBin)
    except ValueError:
        print("Error: Invalid hexadecimal input.")
        return None


def decodeHex(DNA):
    try:
        binary = DNADecoder(DNA)
        hexValue = hex(int(binary, 2))
        print(hexValue)
        return hexValue
    except ValueError:
        print("Error: Could not convert to hexadecimal.")
        return None


def encodeChars(msg):
    if not msg:
        print("Error: Empty input.")
        return

    try:
        binaryMsg = bin(int.from_bytes(msg.encode(), 'big'))[2:].zfill(len(msg) * 8)
        print(f"Binary representation: {binaryMsg}")
        return binaryToDNA(binaryMsg)
    except UnicodeEncodeError:
        print("Error: Input contains characters that cannot be encoded.")
        return None


def decodeChars(DNA):
    try:
        binaryString = DNADecoder(DNA)
        binToInt = int(binaryString, 2)
        text = binToInt.to_bytes((binToInt.bit_length() + 7) // 8, 'big').decode()
        print(f"Decoded text: {text}")
        return text
    except (ValueError, OverflowError):
        print("Error: Binary sequence cannot be converted to text.")
        return None
    except UnicodeDecodeError:
        print("Error: Decoded bytes do not represent valid text.")
        return None


def analyze_dna_practicality(dna):
    issues = []

    for nucleotide in 'ATCG':
        if nucleotide * 4 in dna:
            issues.append(f"Contains {nucleotide * 4} which may cause replication issues")

    gc_count = dna.count('G') + dna.count('C')
    gc_percent = (gc_count / len(dna)) * 100 if dna else 0

    if gc_percent < 20:
        issues.append(f"Low GC content ({gc_percent:.1f}%) may reduce stability")
    elif gc_percent > 80:
        issues.append(f"High GC content ({gc_percent:.1f}%) may be difficult to replicate")

    for i in range(len(dna) - 5):
        segment = dna[i:i+6]
        complement = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
        rev_comp = ''.join(complement.get(n, n) for n in reversed(segment))
        if segment == rev_comp:
            issues.append(f"Contains palindromic sequence {segment} which may form secondary structures")
            break

    return issues


def init():
    print("DNA Encoder/Decoder Tool")
    print("========================")
    print("Convert between DNA and other formats!")

    while True:
        print("\nWhat would you like to do today?")
        print("1. Encode to DNA (turn regular data into DNA)")
        print("2. Decode from DNA (turn DNA back into regular data)")
        print("3. Analyze DNA sequence practicality (is this DNA sequence biologically realistic?)")
        print("4. Exit")

        try:
            choice = input("\nEnter your choice (1-4): ")
        except (EOFError, KeyboardInterrupt):
            print("\nExiting...")
            break

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

            if not all(n in 'ATCG' for n in dna):
                print("Warning: Your sequence has letters other than A, T, C, and G. This might not work well.")

            if decode_choice == '1':
                decodeBinary(dna)
            elif decode_choice == '2':
                decodeHex(dna)
            elif decode_choice == '3':
                decodeChars(dna)

        elif choice == '3':
            dna = input("Type in the DNA sequence you want to analyze: ").upper()
            issues = analyze_dna_practicality(dna)

            if issues:
                print("\nHeads up! Some potential issues with this DNA sequence:")
                for issue in issues:
                    print(f"- {issue}")
            else:
                print("\nGood news! This DNA sequence looks practical from a biological perspective.")

        elif choice == '4':
            print("Thanks for using the DNA Encoder/Decoder Tool! Goodbye!")
            break
        else:
            print("Hmm, that wasn't one of the options. Let's try again.")


if __name__ == "__main__":
    init()
