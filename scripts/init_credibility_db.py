"""
Initialize credibility database with default trusted sources
"""

import csv
from pathlib import Path

# Default credibility database
SOURCES = [
    # Government sources - India
    ("pib.gov.in", "govt", 100),
    ("mohfw.gov.in", "govt", 100),
    ("eci.gov.in", "govt", 100),
    ("mygov.in", "govt", 95),
    ("india.gov.in", "govt", 95),
    
    # Health authorities
    ("who.int", "health_authority", 100),
    ("cdc.gov", "health_authority", 100),
    ("nih.gov", "health_authority", 100),
    
    # Fact-checking organizations
    ("afp.com", "factcheck", 95),
    ("factcheck.org", "factcheck", 95),
    ("snopes.com", "factcheck", 95),
    ("altnews.in", "factcheck", 95),
    ("boomlive.in", "factcheck", 95),
    ("thequint.com", "factcheck", 90),
    ("vishvasnews.com", "factcheck", 90),
    ("newschecker.in", "factcheck", 90),
    
    # Reputable news - International
    ("bbc.com", "news", 85),
    ("reuters.com", "news", 85),
    ("apnews.com", "news", 85),
    ("theguardian.com", "news", 85),
    ("npr.org", "news", 80),
    
    # Reputable news - India
    ("thehindu.com", "news", 85),
    ("indianexpress.com", "news", 85),
    ("hindustantimes.com", "news", 80),
    ("ndtv.com", "news", 80),
    ("timesofindia.com", "news", 80),
    ("livemint.com", "news", 75),
    ("scroll.in", "news", 75),
    ("thewire.in", "news", 75),
    ("news18.com", "news", 70),
    
    # Reference
    ("wikipedia.org", "reference", 70),
]

def create_credibility_db():
    """Create credibility CSV database"""
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    
    csv_path = data_dir / "credibility.csv"
    
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["domain", "type", "score"])
        writer.writerows(SOURCES)
    
    print(f"✅ Credibility database created with {len(SOURCES)} sources")
    print(f"   Location: {csv_path}")

if __name__ == "__main__":
    create_credibility_db()
