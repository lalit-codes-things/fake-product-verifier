"""
Fake-Product Verifier – Digital Supply Chain Ledger
Author: [Your Name]
Date:   [Submission Date]

This script uses SHA‑256 hashing (from Python's hashlib library) to create a
tamper‑evident record of a product's journey:

    Factory  →  Distributor  →  Pharmacy

Every movement is recorded as a "block" that contains:
  - a transaction (from, to, timestamp)
  - the hash of the previous block
  - its own unique hash, computed from the block's data

If anyone modifies a past entry, all subsequent hashes become invalid and the
fraud is immediately detected. This is the same logic that makes modern
blockchain systems secure.
"""

import hashlib
import time
from datetime import datetime

# ----------------------------------------------------------------------
# 1. BLOCK STRUCTURE (using a dictionary)
# ----------------------------------------------------------------------
def create_block(index, timestamp, product_id, from_loc, to_loc, previous_hash):
    """
    Build a single block as a dictionary.
    The 'data' field is a concatenated string of the movement information.
    The 'hash' is computed by hashing index + timestamp + data + previous_hash.
    """
    data = f"{product_id} moved from {from_loc} to {to_loc}"
    block = {
        'index': index,
        'timestamp': timestamp,
        'product_id': product_id,
        'from': from_loc,
        'to': to_loc,
        'data': data,
        'previous_hash': previous_hash,
        'hash': ''   # will be set right after
    }
    # Hash the entire block (excluding the hash field itself)
    block['hash'] = calculate_hash(block)
    return block

def calculate_hash(block):
    """
    Create a SHA‑256 hash of the block's contents.
    The string we hash is: index + timestamp + product_id + from + to
                          + previous_hash
    """
    # Combine all the block fields that must stay unchanged
    hash_string = (
        str(block['index']) +
        str(block['timestamp']) +
        block['product_id'] +
        block['from'] +
        block['to'] +
        block['previous_hash']
    )
    # Return the hexadecimal digest
    return hashlib.sha256(hash_string.encode()).hexdigest()

# ----------------------------------------------------------------------
# 2. THE LEDGER (a list of blocks)
# ----------------------------------------------------------------------

def create_genesis_block():
    """
    The very first block has no predecessor.
    Its previous_hash is set to a string of zeros.
    """
    return create_block(
        index=0,
        timestamp=str(datetime.now()),
        product_id="Origin",
        from_loc="N/A",
        to_loc="Factory",
        previous_hash="0" * 64   # 64 zeros for SHA‑256
    )

def add_movement(chain, product_id, from_loc, to_loc):
    """
    Append a new block to the chain representing a movement.
    """
    previous_block = chain[-1]
    new_index = previous_block['index'] + 1
    timestamp = str(datetime.now())
    new_block = create_block(
        index=new_index,
        timestamp=timestamp,
        product_id=product_id,
        from_loc=from_loc,
        to_loc=to_loc,
        previous_hash=previous_block['hash']
    )
    chain.append(new_block)
    return new_block

# ----------------------------------------------------------------------
# 3. VERIFICATION – detects any tampering
# ----------------------------------------------------------------------
def is_chain_valid(chain):
    """
    Loop through the chain and verify:
      1. The hash of each block matches a fresh calculation.
      2. The previous_hash field points to the previous block's actual hash.
    If any block fails, the chain has been tampered with.
    """
    for i in range(1, len(chain)):   # start from block 1 (block 0 is genesis)
        current_block = chain[i]
        previous_block = chain[i-1]

        # Check 1: Recalculate the block's hash and compare with stored hash
        if current_block['hash'] != calculate_hash(current_block):
            print(f"❌ Data tampered in block {i}: hash mismatch!")
            return False

        # Check 2: Ensure the block points to the correct previous hash
        if current_block['previous_hash'] != previous_block['hash']:
            print(f"❌ Chain broken at block {i}: previous_hash doesn't match!")
            return False

    print("✅ Blockchain integrity verified – no tampering detected.")
    return True

# ----------------------------------------------------------------------
# 4. DISPLAY THE LEDGER
# ----------------------------------------------------------------------
def print_chain(chain):
    print("\n" + "=" * 70)
    print("DIGITAL SUPPLY CHAIN LEDGER")
    print("=" * 70)
    for block in chain:
        print(f"Block #{block['index']}  |  {block['timestamp']}")
        print(f"  Product  : {block['product_id']}")
        print(f"  Movement : {block['from']}  →  {block['to']}")
        print(f"  Prev Hash: {block['previous_hash'][:20]}...")
        print(f"  Own Hash : {block['hash'][:20]}...")
        print("-" * 70)

# ----------------------------------------------------------------------
# 5. MAIN DEMONSTRATION
# ----------------------------------------------------------------------
def main():
    print("INITIALISING SUPPLY CHAIN FOR PRODUCT 'MediCure-100'")
    print("----------------------------------------------------")

    # Create the chain and add the genesis block
    blockchain = [create_genesis_block()]

    # Simulate the journey
    add_movement(blockchain, "MediCure-100", "Factory", "Distributor")
    # Small pause to get different timestamps
    time.sleep(0.1)
    add_movement(blockchain, "MediCure-100", "Distributor", "Pharmacy")

    # Show the complete, valid chain
    print_chain(blockchain)
    print("\nRunning verification on the ORIGINAL chain...")
    is_chain_valid(blockchain)

    # ------------------------------------------------------------------
    # DEMONSTRATE TAMPERING DETECTION
    # ------------------------------------------------------------------
    print("\n" + "=" * 70)
    print("ATTEMPTING TAMPERING: Changing the Distributor→Pharmacy block...")
    print("=" * 70)

    # Make a copy of the chain to simulate a tampered version
    tampered_chain = [block.copy() for block in blockchain]
    # Change the "to" location of the last block (index 2)
    tampered_chain[2]['to'] = "FAKE PHARMACY"
    # The block's stored hash is now outdated, but we do NOT recalculate it.
    # A real attacker might try to recalculate, but they cannot change the
    # previous block's hash that is stored in the next block (there is none here,
    # but if there were, they'd need to change that too – the chain would break.)

    print("Tampered block data now reads:")
    print(f"  {tampered_chain[2]['data']}")   # data field is not automatically updated, but we modified 'to' directly
    # Actually we need to update the 'data' field to reflect the change, because
    # our calculate_hash uses the 'from' and 'to' fields, not 'data'. The 'data'
    # string is just for display. The hashing string uses 'from' and 'to', so
    # the hash will mismatch anyway. To make the tampering obvious in the
    # printed data, we could update the data field. Let's do that.
    tampered_chain[2]['data'] = f"MediCure-100 moved from Distributor to FAKE PHARMACY"

    # Show the tampered chain
    print_chain(tampered_chain)

    # Now try to verify the tampered chain
    print("\nVerifying the TAMPERED chain...")
    result = is_chain_valid(tampered_chain)

    if not result:
        print("\n⚠️  FRAUD DETECTED! The product's history has been altered.")
        print("This medicine could be counterfeit – do not distribute.")

    print("\n" + "=" * 70)
    print("Project complete. This demonstrates how hashing guarantees")
    print("data integrity in a supply chain – the foundation of")
    print("modern anti-counterfeiting systems.")
    print("=" * 70)


if __name__ == "__main__":
    main()