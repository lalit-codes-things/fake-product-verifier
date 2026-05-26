Digital Supply Chain Ledger
Counterfeit medicines and fake luxury goods often enter supply chains because paper records or simple digital receipts can be easily forged.  
A trustworthy system must guarantee that once a movement is recorded, **nobody can alter it** without immediate detection.

How It Works
1. Every time a product moves (Factory → Distributor → Pharmacy), the script adds a **block** to a list (the ledger).
2. Each block contains:
   - The product ID
   - The from/to locations
   - A timestamp
   - The **cryptographic hash** (SHA‑256) of the previous block
   - Its own unique hash, computed from all its data **and** the previous hash
3. Because every block’s hash depends on the previous hash, the blocks form an unbreakable chain.
4. A verification function recomputes all hashes and checks the links. If a single character is changed in any past block, the verification instantly fails.
This is the exact same principle used in blockchain technology.

 Features
-  Immutable digital ledger using SHA‑256 hashing
-  Automatic block creation with timestamp
-  Demonstration of tampering – changes to a past block are caught immediately
- No external libraries required (Python standard library only)

  Technologies & Concepts Demonstrated

| Concept              | Implementation in the code |

| Data security         SHA‑256 hashing via `hashlib` |
| String manipulation  | Building hash inputs from block fields |
| Loops & conditionals | Chain verification loop and fraud detection |
| Lists & dictionaries | The ledger is a list of block dictionaries |
| Immutability         | Changing a past block breaks the hash chain |
| Real‑world problem   | Counterfeit detection in pharmaceutical supply chains |
