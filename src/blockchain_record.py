import os
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv
from web3 import Web3


# --------------------------------------------------
# PROJECT PATHS
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent
INPUT_DIR = PROJECT_ROOT / "input"
OUTPUT_DIR = PROJECT_ROOT / "output"

IMAGE_PATH = INPUT_DIR / "test.jpeg"
EMBEDDING_PATH = OUTPUT_DIR / "face_1_embedding.npy"
SEARCH_RESULTS_PATH = OUTPUT_DIR / "reverse_search_results.json"

RECORD_PATH = OUTPUT_DIR / "verification_record.json"
BLOCKCHAIN_RESULT_PATH = OUTPUT_DIR / "blockchain_result.json"


# --------------------------------------------------
# ENVIRONMENT
# --------------------------------------------------

load_dotenv(PROJECT_ROOT / ".env")

RPC_URL = os.getenv("QUICKNODE_RPC_URL")
PRIVATE_KEY = os.getenv("SEPOLIA_PRIVATE_KEY")


# --------------------------------------------------
# HELPERS
# --------------------------------------------------

def sha256_file(path):
    sha256 = hashlib.sha256()

    with open(path, "rb") as file:
        for chunk in iter(lambda: file.read(8192), b""):
            sha256.update(chunk)

    return sha256.hexdigest()


# --------------------------------------------------
# CREATE VERIFICATION RECORD
# --------------------------------------------------

def create_verification_record():

    if not IMAGE_PATH.exists():
        print("ERROR: Input image not found.")
        return None

    if not EMBEDDING_PATH.exists():
        print("ERROR: Face embedding not found.")
        return None

    if not SEARCH_RESULTS_PATH.exists():
        print("ERROR: Reverse-search results not found.")
        return None

    image_hash = sha256_file(IMAGE_PATH)
    embedding_hash = sha256_file(EMBEDDING_PATH)

    with open(SEARCH_RESULTS_PATH, "r", encoding="utf-8") as file:
        results = json.load(file)

    exact_matches = results.get("exact_matches", [])
    visual_matches = results.get("visual_matches", [])

    matches = exact_matches if exact_matches else visual_matches

    if not matches:
        print("ERROR: No reverse-image-search matches found.")
        return None

    match = matches[0]

    record = {
        "pipeline": "Face ID + Blockchain Verification",
        "version": "1.0",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "image_sha256": image_hash,
        "embedding_sha256": embedding_hash,
        "match": {
            "title": match.get("title"),
            "source_url": match.get("link"),
        },
    }

    canonical_record = json.dumps(
        record,
        sort_keys=True,
        separators=(",", ":")
    )

    record_hash = hashlib.sha256(
        canonical_record.encode("utf-8")
    ).hexdigest()

    record["record_sha256"] = record_hash

    OUTPUT_DIR.mkdir(exist_ok=True)

    with open(RECORD_PATH, "w", encoding="utf-8") as file:
        json.dump(record, file, indent=2, ensure_ascii=False)

    print("Verification record created.")
    print(f"Record SHA-256: {record_hash}")

    return record


# --------------------------------------------------
# WRITE RECORD HASH TO SEPOLIA
# --------------------------------------------------

def write_to_blockchain(record):

    if not RPC_URL:
        print("ERROR: QUICKNODE_RPC_URL is missing from .env")
        return

    if not PRIVATE_KEY:
        print("ERROR: SEPOLIA_PRIVATE_KEY is missing from .env")
        print("Add your MetaMask private key locally to .env.")
        return

    print()
    print("Connecting to Ethereum Sepolia...")

    w3 = Web3(Web3.HTTPProvider(RPC_URL))

    if not w3.is_connected():
        print("ERROR: Could not connect to QuickNode.")
        return

    print("Connected: True")
    print(f"Chain ID: {w3.eth.chain_id}")

    if w3.eth.chain_id != 11155111:
        print("ERROR: This is not Ethereum Sepolia.")
        return

    account = w3.eth.account.from_key(PRIVATE_KEY)
    wallet_address = account.address

    balance = w3.eth.get_balance(wallet_address)
    balance_eth = w3.from_wei(balance, "ether")

    print(f"Wallet: {wallet_address}")
    print(f"SepoliaETH balance: {balance_eth}")

    if balance == 0:
        print()
        print("STOP: Wallet has 0 SepoliaETH.")
        print("Get test ETH first. No transaction was sent.")
        return

    record_hash = record["record_sha256"]

    # Only the verification hash is written on-chain.
    # The image, face embedding and personal data stay off-chain.
    data_text = f"TASK3:{record_hash}"
    data_hex = w3.to_hex(text=data_text)

    nonce = w3.eth.get_transaction_count(wallet_address)

    transaction = {
        "from": wallet_address,
        "to": wallet_address,
        "value": 0,
        "nonce": nonce,
        "chainId": 11155111,
        "data": data_hex,
    }

    # Let the network calculate the required gas.
    gas_estimate = w3.eth.estimate_gas(transaction)

    transaction["gas"] = gas_estimate
    transaction["gasPrice"] = w3.eth.gas_price

    print()
    print("Sending verification hash to Sepolia...")
    print(f"Gas estimate: {gas_estimate}")

    signed_transaction = w3.eth.account.sign_transaction(
        transaction,
        PRIVATE_KEY
    )

    tx_hash = w3.eth.send_raw_transaction(
        signed_transaction.raw_transaction
    )

    print(f"Transaction submitted: {tx_hash.hex()}")

    print("Waiting for confirmation...")

    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    print()
    print("BLOCKCHAIN SUCCESS!")
    print(f"Transaction hash: {tx_hash.hex()}")
    print(f"Block number: {receipt.blockNumber}")

    blockchain_result = {
        "network": "Ethereum Sepolia",
        "chain_id": 11155111,
        "wallet_address": wallet_address,
        "record_sha256": record_hash,
        "transaction_hash": tx_hash.hex(),
        "block_number": receipt.blockNumber,
        "etherscan_url": (
            f"https://sepolia.etherscan.io/tx/{tx_hash.hex()}"
        ),
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
    }

    with open(BLOCKCHAIN_RESULT_PATH, "w", encoding="utf-8") as file:
        json.dump(
            blockchain_result,
            file,
            indent=2
        )

    print(f"Saved: {BLOCKCHAIN_RESULT_PATH}")


# --------------------------------------------------
# MAIN
# --------------------------------------------------

def main():

    print("=" * 60)
    print("FACE ID + BLOCKCHAIN VERIFICATION")
    print("=" * 60)

    record = create_verification_record()

    if record is None:
        return

    write_to_blockchain(record)


if __name__ == "__main__":
    main()