import argparse
import csv
import re
from typing import List, Dict, Any, Optional
from Bio import Entrez

Entrez.email = 'your-email@example.com'


EMAIL_PATTERN = r'[\w\.-]+@[\w\.-]+\.\w+'


def extract_email(text: str) -> Optional[str]:
    """
    Extract the first email from a given text using regex.
    """
    match = re.search(EMAIL_PATTERN, text)
    return match.group(0) if match else None


def fetch_papers(query: str) -> List[str]:
    """
    Fetch paper IDs from PubMed based on a search query.
    """
    handle = Entrez.esearch(db="pubmed", term=query, retmax=20)
    record = Entrez.read(handle)
    handle.close()

    return record.get('IdList', [])


def get_paper_details(paper_id: str) -> Optional[Dict[str, Any]]:
    """
    Get detailed paper information from PubMed.
    Filters out papers without at least one non-academic author.
    """
    handle = Entrez.efetch(db="pubmed", id=paper_id, retmode="xml")
    record = Entrez.read(handle)
    handle.close()

    if 'PubmedArticle' not in record:
        return None

    paper = record['PubmedArticle'][0]['MedlineCitation']
    article = paper['Article']
    authors = article.get('AuthorList', [])

    non_academic_authors = []
    company_affiliations = set()
    corresponding_email = None

    for author in authors:

        affiliation_info = author.get('AffiliationInfo', [])
        for aff in affiliation_info:
            affiliation = aff.get('Affiliation', '')

            if any(term in affiliation.lower() for term in ['pharma', 'biotech', 'company']):
                full_name = f"{author.get('ForeName', '')} {author.get('LastName', '')}".strip(
                )
                if full_name:
                    non_academic_authors.append(full_name)

                company_affiliations.add(affiliation)

                if not corresponding_email:
                    corresponding_email = extract_email(affiliation)

    if non_academic_authors:
        return {
            'PubmedID': paper_id,
            'Title': article.get('ArticleTitle', 'Unknown'),
            'Publication Date': paper.get('DateCompleted', {}).get('Year', 'Unknown'),
            'Non-academic Author(s)': ', '.join(non_academic_authors),
            'Company Affiliation(s)': ', '.join(company_affiliations),
            'Corresponding Author Email': corresponding_email or 'N/A'
        }

    return None


def save_to_csv(papers: List[Dict[str, Any]], filename: str) -> None:
    """
    Save the filtered papers to a CSV file.
    """
    if not papers:
        print("No papers to save.")
        return

    keys = papers[0].keys()
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=keys)
        writer.writeheader()
        writer.writerows(papers)

    print(f"Saved {len(papers)} papers to {filename}")


def fetch_and_save_papers(query: str, filename: Optional[str] = None, debug: bool = False) -> None:
    """
    Fetch papers based on the query, apply filtering, and save the results.
    """
    if debug:
        print(f"Searching PubMed for query: {query}")

    paper_ids = fetch_papers(query)

    if debug:
        print(f"Found {len(paper_ids)} papers")

    filtered_papers = []

    for paper_id in paper_ids:
        paper = get_paper_details(paper_id)
        if paper:
            filtered_papers.append(paper)

    if filename:
        save_to_csv(filtered_papers, filename)
    else:
        print(filtered_papers)


def main() -> None:
    """
    Main entry point for the CLI program.
    """

    parser = argparse.ArgumentParser(
        description="Fetch research papers from PubMed based on a query.")
    parser.add_argument('query', type=str, help="Search query for PubMed.")
    parser.add_argument('-f', '--file', type=str, help="Output file name.")
    parser.add_argument('-d', '--debug', action='store_true',
                        help="Enable debug mode.")

    args = parser.parse_args()

    fetch_and_save_papers(args.query, args.file, args.debug)


if __name__ == "__main__":
    main()
