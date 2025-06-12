def binaryToDNA(binary):
    binary_to_dna = {'00': 'A', '01': 'T', '10': 'C', '11': 'G'}

    if len(binary) % 2 != 0:
        binary += '0'
        print("Notice: Input contained an odd number of bits. Padding with '0' for proper encoding.")

    DNA = ""
    for i in range(0, len(binary), 2):
        pair = binary[i:i+2]
        DNA += binary_to_dna.get(pair, 'A')

    if 'AAAA' in DNA:
        print("Caution: The DNA sequence includes 'AAAA', which may present instability in biological contexts.")

    print(f"Encoded DNA sequence: {DNA}")
    return DNA


def DNADecoder(DNA):
    dna_to_binary = {'A': '00', 'T': '01', 'C': '10', 'G': '11'}

    binaryString = ""
    for n in DNA:
        if n not in dna_to_binary:
            print(f"Warning: Invalid nucleotide '{n}' found. Substituting with 'A' (00).")
        binaryString += dna_to_binary.get(n, '00')

    if len(DNA) % 4 != 0:
        print("Notice: DNA sequence length suggests possible padding during encoding.")

    return binaryString


def encodeBinary(msg):
    if not all(bit in '01' for bit in msg):
        print("Error: Input includes non-binary characters. Filtering to retain only '0' and '1'.")
        msg = ''.join(bit for bit in msg if bit in '01')

    if not msg:
        print("Error: No valid binary digits provided.")
        return

    return binaryToDNA(msg)


def decodeBinary(DNA):
    binary = DNADecoder(DNA)
    print(f"Decoded binary string: {binary}")
    return binary


def encodeHex(msg):
    try:
        if msg.lower().startswith('0x'):
            msg = msg[2:]
        int(msg, 16)
        toBin = bin(int(msg, 16))[2:].zfill(len(msg) * 4)
        return binaryToDNA(toBin)
    except ValueError:
        print("Error: Provided string is not valid hexadecimal.")
        return None


def decodeHex(DNA):
    try:
        binary = DNADecoder(DNA)
        hexValue = hex(int(binary, 2))
        print(f"Decoded hexadecimal value: {hexValue}")
        return hexValue
    except ValueError:
        print("Error: Conversion to hexadecimal failed.")
        return None


def encodeChars(msg):
    if not msg:
        print("Error: No input text provided.")
        return

    try:
        binaryMsg = bin(int.from_bytes(msg.encode(), 'big'))[2:].zfill(len(msg) * 8)
        print(f"Binary representation of text: {binaryMsg}")
        return binaryToDNA(binaryMsg)
    except UnicodeEncodeError:
        print("Error: Text contains unsupported characters for encoding.")
        return None


def decodeChars(DNA):
    try:
        binaryString = DNADecoder(DNA)
        binToInt = int(binaryString, 2)
        text = binToInt.to_bytes((binToInt.bit_length() + 7) // 8, 'big').decode()
        print(f"Decoded text: {text}")
        return text
    except (ValueError, OverflowError):
        print("Error: Binary data is not interpretable as text.")
        return None
    except UnicodeDecodeError:
        print("Error: Decoded binary does not represent valid UTF-8 text.")
        return None


def analyze_dna_practicality(dna):
    issues = []

    for nucleotide in 'ATCG':
        if nucleotide * 4 in dna:
            issues.append(f"Contains repetitive sequence '{nucleotide * 4}' which can affect replication stability.")

    gc_count = dna.count('G') + dna.count('C')
    gc_percent = (gc_count / len(dna)) * 100 if dna else 0

    if gc_percent < 20:
        issues.append(f"Low GC content ({gc_percent:.1f}%) may compromise DNA stability.")
    elif gc_percent > 80:
        issues.append(f"High GC content ({gc_percent:.1f}%) may hinder replication efficiency.")

    for i in range(len(dna) - 5):
        segment = dna[i:i+6]
        complement = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
        rev_comp = ''.join(complement.get(n, n) for n in reversed(segment))
        if segment == rev_comp:
            issues.append(f"Detected palindromic sequence '{segment}' which could lead to secondary structure formation.")
            break

    return issues


def init():
    print("DNA Encoder/Decoder Tool")
    print("========================")
    print("Perform conversions between DNA and various data formats.")

    while True:
        print("\nPlease select an option:")
        print("1. Encode to DNA")
        print("2. Decode from DNA")
        print("3. Analyze DNA sequence practicality")
        print("4. Exit")

        try:
            choice = input("\nEnter your choice (1-4): ")
        except (EOFError, KeyboardInterrupt):
            print("\nSession terminated. Exiting...")
            break

        if choice == '1':
            print("\nSelect the type of data to encode:")
            print("1. Binary")
            print("2. Hexadecimal")
            print("3. Text")

            encode_choice = input("\nEnter your choice (1-3): ")

            if encode_choice == '1':
                msg = input("Enter binary string: ")
                encodeBinary(msg)
            elif encode_choice == '2':
                msg = input("Enter hexadecimal string: ")
                encodeHex(msg)
            elif encode_choice == '3':
                msg = input("Enter text to encode: ")
                encodeChars(msg)
            else:
                print("Invalid option selected. Please try again.")

        elif choice == '2':
            print("\nSelect the target format for decoding:")
            print("1. Binary")
            print("2. Hexadecimal")
            print("3. Text")

            decode_choice = input("\nEnter your choice (1-3): ")
            if decode_choice not in ['1', '2', '3']:
                print("Invalid option selected. Please try again.")
                continue

            dna = input("Enter DNA sequence (A, T, C, G only): ").upper()

            if not all(n in 'ATCG' for n in dna):
                print("Warning: Input includes non-standard DNA characters.")

            if decode_choice == '1':
                decodeBinary(dna)
            elif decode_choice == '2':
                decodeHex(dna)
            elif decode_choice == '3':
                decodeChars(dna)

        elif choice == '3':
            dna = input("Enter DNA sequence to analyze: ").upper()
            issues = analyze_dna_practicality(dna)

            if issues:
                print("\nPotential concerns identified in the DNA sequence:")
                for issue in issues:
                    print(f"- {issue}")
            else:
                print("\nThe DNA sequence appears to be biologically viable.")

        elif choice == '4':
            print("Thank you for using the DNA Encoder/Decoder Tool. Goodbye!")
            break
        else:
            print("Invalid selection. Please choose an option from 1 to 4.")


if __name__ == "__main__":
    init()
