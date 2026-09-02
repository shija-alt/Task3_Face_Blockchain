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
Task3_Face_Blockchain/
├── input/
│   └── test.jpeg
│
├── models/
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
└── README.md