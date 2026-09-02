# Face ID + Blockchain Verification

## Overview

This project implements an end-to-end face verification pipeline that:

1. Detects a face from an input image.
2. Generates a face embedding.
3. Performs a genuine reverse-image search to find a matching social-media post.
4. Creates a verification record containing SHA-256 hashes.
5. Writes the verification record hash to the Ethereum Sepolia testnet.
6. Stores the blockchain transaction details for independent verification.

The project is designed as a local pipeline. No website or hosting is required.

---

## Pipeline

```text
Input Image
    |
    v
Face Detection
    |
    v
Face Embedding
    |
    v
Genuine Reverse Image Search
    |
    v
Matching Social Media Source
    |
    v
SHA-256 Verification Record
    |
    v
Ethereum Sepolia Blockchain
    |
    v
Blockchain Transaction Record
```

---

## Project Structure

```text
Task3_Face_Blockchain/

├── input/
│   └── test.jpeg
│
├── models/
│   ├── face_detection_yunet_2023mar.onnx
│   └── face_recognition_sface_2021dec.onnx
│
├── output/
│   ├── detected_faces.jpg
│   ├── face_1_embedding.npy
│   ├── reverse_search_results.json
│   ├── verification_record.json
│   └── blockchain_result.json
│
├── src/
│   ├── face_pipeline.py
│   ├── reverse_search.py
│   └── blockchain_record.py
│
├── .env
├── .gitignore
├── README.md
└── requirements.txt
```

---

## Technologies Used

- Python
- OpenCV
- NumPy
- SHA-256
- Reverse-image search
- Web3.py
- Ethereum Sepolia testnet
- QuickNode RPC
- GitHub

---

## Requirements

- Python 3.10 or newer
- OpenCV
- NumPy
- python-dotenv
- Web3.py
- QuickNode Ethereum Sepolia RPC endpoint
- Ethereum Sepolia wallet
- Sepolia test ETH

Install the Python dependencies using:

```bash
pip install -r requirements.txt
```

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/shija-alt/Task3_Face_Blockchain.git
cd Task3_Face_Blockchain
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

If PowerShell blocks the activation script, the project can still be run using the Python executable inside `.venv`.

### 4. Configure environment variables

Create a `.env` file in the project root:

```text
QUICKNODE_RPC_URL=your_quicknode_sepolia_rpc_url
SEPOLIA_PRIVATE_KEY=your_wallet_private_key
```

The private key must remain private and must never be committed to GitHub.

---

## Input

Place the input image in:

```text
input/test.jpeg
```

The face detection pipeline processes this image and generates the corresponding face embedding.

---

## Running the Pipeline

### Step 1 — Face Detection and Embedding

Run:

```bash
python src/face_pipeline.py
```

This produces the detected-face image and face embedding in the `output/` directory.

Expected outputs include:

```text
output/detected_faces.jpg
output/face_1_embedding.npy
```

### Step 2 — Reverse Image Search

Run:

```bash
python src/reverse_search.py
```

This performs the reverse-image-search step and saves the search results.

Output:

```text
output/reverse_search_results.json
```

The implementation uses the search result returned by the reverse-image-search process rather than hardcoding a social-media URL.

### Step 3 — Blockchain Verification

Run:

```bash
python src/blockchain_record.py
```

This:

1. Creates the verification record.
2. Calculates SHA-256 hashes.
3. Connects to Ethereum Sepolia through QuickNode.
4. Writes the verification record hash to the blockchain.
5. Waits for transaction confirmation.
6. Saves the transaction details.

Output:

```text
output/verification_record.json
output/blockchain_result.json
```

---

## Verification Record

The verification record contains information such as:

- Pipeline name
- Pipeline version
- UTC timestamp
- Input image SHA-256
- Face embedding SHA-256
- Matching source
- Verification record SHA-256

The SHA-256 hash provides a compact fingerprint of the verification record.

Only the verification hash is written to the blockchain.

The original image and face embedding remain off-chain.

---

## Blockchain Verification

The project uses the **Ethereum Sepolia testnet**.

Network:

```text
Ethereum Sepolia
```

Chain ID:

```text
11155111
```

The blockchain transaction details are saved in:

```text
output/blockchain_result.json
```

The file contains:

- Network
- Chain ID
- Wallet address
- Verification record hash
- Transaction hash
- Block number
- Etherscan transaction URL
- Timestamp

The transaction can be independently checked using the Sepolia Etherscan transaction URL stored in the JSON file.

### Example transaction

Transaction hash:

```text
8b5a2495947903b094598ec3cf919dd09a79a4fe5821b288e6f71e34f656289f
```

Block number:

```text
11621374
```

---

## Output Files

| File | Description |
|---|---|
| `detected_faces.jpg` | Image containing the detected face |
| `face_1_embedding.npy` | Generated numerical face embedding |
| `reverse_search_results.json` | Reverse-image-search results |
| `verification_record.json` | Verification record and SHA-256 hashes |
| `blockchain_result.json` | Blockchain transaction details |

---

## Security and Privacy

The project does not upload the original image or face embedding to the blockchain.

Instead, the verification record is hashed using SHA-256.

The blockchain stores only the verification hash through an Ethereum transaction.

The following sensitive files are excluded from GitHub using `.gitignore`:

```text
.env
input/*
output/*
```

The `.env` file contains credentials and must never be committed to the repository.

---

## Limitations

- Face recognition accuracy depends on the quality of the input image and the selected models.
- Reverse-image search depends on the external search service and the images indexed by that service.
- A matching social-media result may not always be available.
- Ethereum Sepolia is a testnet and is not intended for production-value transactions.
- Blockchain transactions are public, although the original image and embedding are kept off-chain.
- The pipeline requires valid RPC credentials.
- Reverse-image-search results can change as external websites and search indexes change.
- The system verifies the integrity of the stored record; it does not by itself prove the real-world identity of a person.

---

## Known Successful Blockchain Run

The pipeline was successfully executed on Ethereum Sepolia.

Example result:

```text
Network: Ethereum Sepolia
Chain ID: 11155111
Block: 11621374
Transaction:
8b5a2495947903b094598ec3cf919dd09a79a4fe5821b288e6f71e34f656289f
```

The complete transaction information is stored in:

```text
output/blockchain_result.json
```

---

## How to Verify the Result

1. Run the pipeline locally.
2. Open `output/verification_record.json`.
3. Note the `record_sha256` value.
4. Open `output/blockchain_result.json`.
5. Note the transaction hash.
6. Open the Sepolia Etherscan transaction page.
7. Verify that the transaction was confirmed on Ethereum Sepolia.
8. The transaction data contains the verification record hash.

This allows the verification record to be independently checked against the blockchain transaction.

---

## GitHub

Source code:

https://github.com/shija-alt/Task3_Face_Blockchain

The repository contains the source code, model files, dependency list, documentation, and `.gitignore` configuration required to reproduce the pipeline.

---

## License

This project was created as part of **Task #3 — Face ID + Blockchain Verification**.