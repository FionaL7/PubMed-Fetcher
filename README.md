# 🧪 PubMed Research Paper Fetcher

This Python program fetches research papers from PubMed based on a user-specified query. It filters the results to identify papers with at least one author affiliated with a pharmaceutical or biotech company and outputs the results as a CSV file.

## Features

 * Fetches papers using the PubMed API\n
 * Filters papers to identify non-academic authors affiliated with pharmaceutical/biotech companies\n
 * Outputs results to a CSV file\n
 * Command-line options for flexible usage (--debug, --file, --help)\n
 * Efficient and well-typed Python code with error handling\n

## Setup and Installation

### 1. Prerequisites

Ensure you have **Python 3.8+** installed.

### 2. Install Poetry

This project uses [Poetry](https://python-poetry.org/) for dependency management. Install it using:

```bash
pip install poetry
```

After installation, verify it works:

```bash
poetry --version
```

### 3. Clone Repository

git clone https://github.com/your-username/pubmed-fetcher.git
cd pubmed-fetcher

### 4. Install Dependencies

Run the following command inside the `pubmed-fetcher` directory:

```bash
poetry install
```

This will install all required dependencies.

---

## Usage

The program can be executed using the command:

```bash
poetry run get-papers-list --query "cancer therapy" --file results.csv
```

### Command Line Options

`--query` - The search query for PubMed (supports full PubMed query syntax).
`--file` - (Optional) The output CSV filename. If not provided, results are printed in the console.
`--debug` - (Optional) Enables debug mode to display additional logs.
`-h, --help` - Displays usage instructions.

Example:

```bash
poetry run get-papers-list --query "COVID-19 vaccine" --file papers.csv
```

## 📁 Output Format

The results are stored as a CSV file with the following columns:

| Column                         | Description                                                        |
| ------------------------------ | ------------------------------------------------------------------ |
| **PubmedID**                   | Unique identifier for the paper.                                   |
| **Title**                      | Title of the paper.                                                |
| **Publication Date**           | Date the paper was published.                                      |
| **Non-academic Author(s)**     | Names of authors affiliated with pharmaceutical/biotech companies. |
| **Company Affiliation(s)**     | Names of pharmaceutical/biotech companies.                         |
| **Corresponding Author Email** | Email address of the corresponding author.                         |

---
