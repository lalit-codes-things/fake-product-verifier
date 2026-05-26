import hashlib
import time
from datetime import datetime
def create_block(index, timestamp, product_id, from_loc, to_loc, previous_hash):
    data = f"{product_id} moved from {from_loc} to {to_loc}"
    block = {
        'index': index,
        'timestamp': timestamp,
        'product_id': product_id,
        'from': from_loc,
        'to': to_loc,
        'data': data,
        'previous_hash': previous_hash,
        'hash': ''  
    }
    block['hash'] = calculate_hash(block)
    return block
def calculate_hash(block):
    hash_string = (
        str(block['index']) +
        str(block['timestamp']) +
        block['product_id'] +
        block['from'] +
        block['to'] +
        block['previous_hash']
    )
    return hashlib.sha256(hash_string.encode()).hexdigest()
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
        previous_hash="0" * 64  
    )
def add_movement(chain, product_id, from_loc, to_loc):
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
def is_chain_valid(chain):
    """
    Loop through the chain and verify:
      1. The hash of each block matches a fresh calculation.
      2. The previous_hash field points to the previous block's actual hash.
    If any block fails, the chain has been tampered with.
    """
    for i in range(1, len(chain)):  
        current_block = chain[i]
        previous_block = chain[i-1]
        if current_block['hash'] != calculate_hash(current_block):
            print(f" Data tampered in block {i}: hash mismatch!")
            return False
        if current_block['previous_hash'] != previous_block['hash']:
            print(f" Chain broken at block {i}: previous_hash doesn't match!")
            return False
    print(" Blockchain integrity verified – no tampering detected.")
    return True
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
def main():
    print("INITIALISING SUPPLY CHAIN FOR PRODUCT 'MediCure-100'")
    print("----------------------------------------------------")
    blockchain = [create_genesis_block()]
    add_movement(blockchain, "MediCure-100", "Factory", "Distributor")
    time.sleep(0.1)
    add_movement(blockchain, "MediCure-100", "Distributor", "Pharmacy")
    print_chain(blockchain)
    print("\nRunning verification on the ORIGINAL chain...")
    is_chain_valid(blockchain)
    print("\n" + "=" * 70)
    print("ATTEMPTING TAMPERING: Changing the Distributor→Pharmacy block...")
    print("=" * 70)
    tampered_chain = [block.copy() for block in blockchain]
    tampered_chain[2]['to'] = "FAKE PHARMACY"
    print("Tampered block data now reads:")
    print(f"  {tampered_chain[2]['data']}")      
    tampered_chain[2]['data'] = f"MediCure-100 moved from Distributor to FAKE PHARMACY"
    print_chain(tampered_chain)
    print("\nVerifying the TAMPERED chain...")
    result = is_chain_valid(tampered_chain)
    if not result:
        print("\n  FRAUD DETECTED! The product's history has been altered.")
        print("This medicine could be counterfeit – do not distribute.")
    print("\n" + "=" * 70)
    print("Project complete. This demonstrates how hashing guarantees")
    print("data integrity in a supply chain – the foundation of")
    print("modern anti-counterfeiting systems.")
    print("=" * 70)


if __name__ == "__main__":
    main()
