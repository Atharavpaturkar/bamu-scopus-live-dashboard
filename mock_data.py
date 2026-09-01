import random
import os
import json
from datetime import datetime

# Real academic departments at Dr. Babasaheb Ambedkar Marathwada University (BAMU)
BAMU_DEPARTMENTS = [
    "Department of Chemistry",
    "Department of Physics",
    "Department of Computer Science & Information Technology",
    "Department of Biotechnology",
    "Department of Chemical Technology",
    "Department of Zoology",
    "Department of Botany",
    "Department of Environmental Science",
    "Department of Mathematics",
    "Department of Statistics",
    "Department of Pharmacy",
    "Department of Mechanical Engineering",
    "Department of Management Science",
    "Department of Commerce",
    "Department of English & Foreign Languages",
    "Department of History & Ancient Indian Culture"
]

# Prominent faculty and author names for BAMU research context
BAMU_FACULTY = [
    "Dr. K. M. Jadhav", "Dr. M. D. Shirsat", "Dr. K. V. Kale", "Dr. P. B. Joshi",
    "Dr. R. A. Mane", "Dr. B. R. Arbad", "Dr. C. H. Gill", "Dr. A. S. Dhabe",
    "Dr. S. B. Nimse", "Dr. R. R. Deshmukh", "Dr. M. S. Shingare", "Dr. S. S. Pekamwar",
    "Dr. S. N. Helambe", "Dr. V. A. Matsagar", "Dr. S. D. Naik", "Dr. A. G. Shankar",
    "Dr. P. V. Pawar", "Dr. S. A. Patil", "Dr. S. T. Gaikwad", "Dr. Y. B. Muley",
    "Dr. N. N. Karade", "Dr. B. N. Dole", "Dr. S. M. Sulakhe", "Dr. M. V. Kendre",
    "Dr. G. S. Chavan", "Dr. P. Dhole", "Dr. V. A. Mane", "Dr. R. P. Pawar"
]

CO_AUTHORS_POOL = [
    "J. A. Smith", "K. Takahashi", "M. Schmidt", "A. Al-Farsi", "L. Zhang",
    "R. Kumar", "S. Sharma", "P. Deshmukh", "V. Kulkarni", "A. Patil",
    "S. Gupta", "H. Park", "D. Miller", "E. Rossi", "C. Francois"
]

JOURNAL_POOL = {
    "Department of Chemistry": [
        ("Journal of Molecular Structure", "Q2", 4.2, 0.65),
        ("ACS Applied Materials & Interfaces", "Q1", 9.8, 1.85),
        ("Tetrahedron Letters", "Q2", 3.8, 0.58),
        ("Bioorganic & Medicinal Chemistry", "Q1", 5.2, 0.88),
        ("RSC Advances", "Q2", 4.0, 0.62),
        ("Journal of Pharmaceutical Innovation", "Q2", 3.5, 0.52),
        ("Polyhedron", "Q3", 2.8, 0.45)
    ],
    "Department of Physics": [
        ("Journal of Alloys and Compounds", "Q1", 6.2, 1.05),
        ("Applied Physics Letters", "Q1", 4.0, 0.98),
        ("Materials Today Communications", "Q2", 3.8, 0.60),
        ("Journal of Magnetism and Magnetic Materials", "Q2", 3.2, 0.55),
        ("Ceramics International", "Q1", 5.5, 0.92),
        ("Physica B: Condensed Matter", "Q3", 2.9, 0.48)
    ],
    "Department of Computer Science & Information Technology": [
        ("IEEE Transactions on Pattern Analysis and Machine Intelligence", "Q1", 23.6, 4.50),
        ("Pattern Recognition", "Q1", 8.0, 1.75),
        ("Expert Systems with Applications", "Q1", 8.5, 1.65),
        ("IEEE Access", "Q1", 3.9, 0.72),
        ("Smart Innovation Systems and Technologies", "Q3", 1.8, 0.32),
        ("Journal of King Saud University - Computer and Information Sciences", "Q1", 6.8, 1.20)
    ],
    "Department of Biotechnology": [
        ("International Journal of Biological Macromolecules", "Q1", 8.2, 1.45),
        ("Process Biochemistry", "Q2", 4.8, 0.82),
        ("Enzyme and Microbial Technology", "Q1", 4.5, 0.85),
        ("3 Biotech", "Q2", 2.8, 0.51),
        ("Applied Biochemistry and Biotechnology", "Q3", 3.1, 0.55)
    ],
    "Department of Chemical Technology": [
        ("Fuel", "Q1", 7.4, 1.40),
        ("Chemical Engineering Journal", "Q1", 13.3, 2.30),
        ("Industrial & Engineering Chemistry Research", "Q1", 4.2, 0.82),
        ("Desalination", "Q1", 9.9, 1.80),
        ("Journal of Cleaner Production", "Q1", 11.1, 1.95)
    ],
    "Department of Pharmacy": [
        ("European Journal of Medicinal Chemistry", "Q1", 6.7, 1.25),
        ("International Journal of Pharmaceutics", "Q1", 5.8, 1.10),
        ("Drug Delivery", "Q1", 6.9, 1.30),
        ("Journal of Drug Delivery Science and Technology", "Q2", 4.5, 0.75)
    ],
    "Department of Environmental Science": [
        ("Science of The Total Environment", "Q1", 9.8, 1.75),
        ("Environmental Pollution", "Q1", 8.9, 1.60),
        ("Environmental Monitoring and Assessment", "Q2", 3.3, 0.58),
        ("Chemosphere", "Q1", 8.8, 1.55)
    ]
}

DEFAULT_JOURNALS = [
    ("Journal of Academic Research & Development", "Q3", 2.1, 0.38),
    ("International Journal of Advanced Science & Engineering", "Q2", 3.4, 0.52),
    ("Sadhana - Academy Proceedings in Engineering Sciences", "Q3", 1.9, 0.35),
    ("Journal of Scientific & Industrial Research", "Q3", 1.7, 0.30),
    ("Current Science", "Q2", 2.2, 0.42)
]

INTERNATIONAL_COUNTRIES = [
    "United States", "South Korea", "Germany", "Japan", "United Kingdom",
    "Saudi Arabia", "Malaysia", "Taiwan", "France", "Australia", "Canada"
]

INDUSTRY_ENTITIES = [
    "Wockhardt Ltd", "Lupin Pharmaceuticals", "Cipla Research Labs",
    "Reliance Industries Ltd", "Tata Chemicals R&D", "Bharat Biotech",
    "TCS Innovation Labs", "Thermax India Ltd"
]

TITLE_TEMPLATES = [
    "Synthesis, characterization, and evaluation of novel {substance} for {application}",
    "Development of {tech} based approach for enhanced {domain} performance",
    "In silico and experimental analysis of {substance} targeting {domain}",
    "Spatial and temporal analysis of {domain} in {region} using {tech}",
    "Investigation on structural and optical properties of {substance} thin films for {application}",
    "Machine learning driven classification of {domain} using {tech}",
    "Sustainable synthesis of green {substance} nanostructures and their {application} application",
    "Optimization of {tech} processes for scalable {domain} applications"
]

SUBSTANCES = [
    "Benzofuran-Triazole conjugates", "cobalt ferrite nanoparticles", "MOF-based photoelectrodes",
    "zinc oxide nanocomposites", "Ayurvedic plant extracts", "chitosan biopolymers",
    "perovskite quantum dots", "graphene oxide sheets", "heterocyclic chalcone derivatives"
]

APPLICATIONS = [
    "solar water splitting", "antitubercular evaluation", "EGFR inhibitor resistance",
    "heavy metal remediation", "hyperspectral data classification", "photocatalytic degradation",
    "energy storage supercapacitors", "antibacterial screening"
]

DOMAINS = [
    "air pollutant trends", "crop disease detection", "wastewater purification",
    "molecular docking and MD simulation", "renewable hydrogen generation", "dielectric response"
]

TECHS = [
    "Deep Convolutional Neural Networks", "Hybrid Computational Approach", "X-ray Diffraction & VSM",
    "Satellite Remote Sensing Data", "DFT calculations", "Response Surface Methodology"
]

REGIONS = [
    "Chhatrapati Sambhajinagar Region", "Marathwada Region, Maharashtra", "Godavari River Basin",
    "Decan Trap Volcanic Province"
]


def generate_mock_publications(count=2500, seed=42):
    """
    Generate realistic benchmark Scopus publications dataset for BAMU.
    Returns a list of dictionaries with all required document schema fields.
    """
    rng = random.Random(seed)
    publications = []
    
    start_year = 2012
    end_year = 2026

    for i in range(1, count + 1):
        dept = rng.choice(BAMU_DEPARTMENTS)
        
        # Select journal based on department or default
        dept_journals = JOURNAL_POOL.get(dept, DEFAULT_JOURNALS)
        journal_info = rng.choice(dept_journals)
        journal_name, quartile, base_citescore, base_sjr = journal_info
        
        # Year distribution skewed slightly towards recent years (2020-2026)
        year = rng.choices(
            population=list(range(start_year, end_year + 1)),
            weights=[3, 4, 5, 6, 7, 8, 10, 12, 14, 16, 18, 20, 22, 24, 25]
        )[0]

        # Citations model based on year age and journal quartile
        age = (2026 - year) + 1
        q_multiplier = {"Q1": 3.5, "Q2": 2.0, "Q3": 1.0, "Q4": 0.5}.get(quartile, 1.0)
        citations = int(max(0, rng.gammavariate(alpha=2.0, beta=4.0 * age * q_multiplier / 2.0)))

        # Authors & Collaborations
        primary_author = rng.choice(BAMU_FACULTY)
        num_coauthors = rng.randint(1, 4)
        coauthors = rng.sample(CO_AUTHORS_POOL, num_coauthors)
        authors = [primary_author] + coauthors
        
        is_international_collab = rng.random() < 0.28  # ~28% international collaboration
        is_industry_collab = rng.random() < 0.14       # ~14% industry collaboration

        countries = ["India"]
        if is_international_collab:
            intl_country = rng.choice(INTERNATIONAL_COUNTRIES)
            countries.append(intl_country)
            
        if is_industry_collab:
            ind_name = rng.choice(INDUSTRY_ENTITIES)
            authors.append(f"{ind_name} Research Team")

        # Title Generation
        title_tmpl = rng.choice(TITLE_TEMPLATES)
        title = title_tmpl.format(
            substance=rng.choice(SUBSTANCES),
            application=rng.choice(APPLICATIONS),
            domain=rng.choice(DOMAINS),
            tech=rng.choice(TECHS),
            region=rng.choice(REGIONS)
        )

        scopus_id = f"1050{rng.randint(10000000, 99999999)}"
        doi_suffix = f"10.1016/j.{dept.split()[-1].lower()}.{year}.{rng.randint(100000, 999999)}"

        pub = {
            "scopus_id": scopus_id,
            "title": title,
            "authors": authors,
            "primary_author": primary_author,
            "department": dept,
            "journal": journal_name,
            "year": year,
            "citations": citations,
            "citescore": round(max(0.5, rng.gauss(base_citescore, 0.5)), 2),
            "sjr": round(max(0.1, rng.gauss(base_sjr, 0.1)), 2),
            "quartile": quartile,
            "doi": doi_suffix,
            "is_international_collab": is_international_collab,
            "is_industry_collab": is_industry_collab,
            "countries": countries
        }
        publications.append(pub)

    # Sort descending by year, then by citations
    publications.sort(key=lambda x: (x['year'], x['citations']), reverse=True)
    return publications


def load_or_generate_mock_data(cache_path="data/bamu_scopus_mock.json", count=2500):
    """
    Loads mock benchmark dataset from disk cache or generates ~2500 publications.
    """
    if os.path.exists(cache_path):
        try:
            with open(cache_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, dict) and "publications" in data:
                    return data["publications"]
                elif isinstance(data, list):
                    return data
        except Exception as e:
            print(f"Warning reading mock cache: {e}")

    pubs = generate_mock_publications(count=count)
    
    # Save cache for fast reload
    os.makedirs(os.path.dirname(cache_path), exist_ok=True)
    try:
        payload = {
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "total_records": len(pubs),
                "source": "Mock Benchmark Data Generator"
            },
            "publications": pubs
        }
        with open(cache_path, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)
    except Exception as e:
        print(f"Warning saving mock cache: {e}")

    return pubs


if __name__ == "__main__":
    mock_pubs = generate_mock_publications(2500)
    print(f"Generated {len(mock_pubs)} mock publication records.")
    print("Sample publication:", json.dumps(mock_pubs[0], indent=2))
