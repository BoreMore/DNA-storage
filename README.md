# DNA-storage
The intention with this project was to create an open source proof of concept that binary information can be stored as DNA sequences.

## How to Run
These instructions will allow you to run the program on your machine. 

### Requirements
* Requires Python 3.7

### Download
* Download dnaseq.py

### Usage
1. Run dnaseq.py
```
python dnaseq.py
```
2. Answer prompts in console
3. Encode/decode data

## Acknowledgements
This project was inspired by Dina Zielinski's Ted Talk: https://www.youtube.com/watch?v=wxStlzunxCw. 


## Changes (11-5-2025)
If odd number of bits are generated, the message gets lost in dna
so we have to make sure even number of bits are processed. To achieve that we add a 0 at the beginning

Also the previous code is impractical due to biological constraints. (It is illogical to encode data in a random DNA sting order).
If there

The new code solves both these problems. 