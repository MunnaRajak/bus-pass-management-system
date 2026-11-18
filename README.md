# Bus Pass Management System

A simple command-line bus pass management application written in Python.

## Features

- Issue Monthly, Quarterly, and Yearly bus passes
- Apply a 25% discount for student passengers
- Automatically generate pass IDs starting at `BP101`
- Renew existing passes
- Search for a pass by ID
- View all issued passes
- Store pass records in `buspass.txt`

## Requirements

- Python 3

## Run the Project

```bash
python project2.py
```

On launch, the program displays a menu with five options:

1. Issue a new pass
2. Renew a pass
3. Search for a pass by ID
4. View all passes
5. Exit

## Pass Types

| Pass type | Validity | Base fee |
|---|---:|---:|
| Monthly | 30 days | Rs. 500 |
| Quarterly | 90 days | Rs. 1350 |
| Yearly | 365 days | Rs. 4800 |

Student passes receive a 25% discount on the base fee.

## Data Storage

Issued passes are saved automatically to `buspass.txt` in the project directory. Each record contains the pass ID, passenger name, route, pass type, fee, passenger category, and validity period.
