"""
Raw genealogical entries transcribed from the source PDFs in
~/Documents/Family Tree/.

Format:
    code            Lineage code from the source PDFs (e.g. "1", "13B", "172A").
                    Each digit/letter is one generation. Single character = founder
                    generation. Two = founder's child. Etc.
                    "0" is the placeholder for the unnamed common patriarch.
    name            Full name as displayed in source.
    sex             "M" or "F" (optional; can usually be inferred from spouse role
                    but we record where known).
    born            Birth date string from the source.
    born_alt        Alternative birth date when source gives one in parens.
    born_place      Place of birth.
    died            Death date.
    died_place      Place of death.
    buried          Burial location.
    spouses         List of marriage dicts: {name, born, died, father, mother,
                    married, married_place, order, buried, details, notes}
    notes           Free-text biographical info.
    residences      Places of residence.
    occupation      Known occupation.
    flags           {diedInInfancy, adopted, stepChild, fosterChild}
    children        List of {code, name, born, died, flags} — used to create stub
                    Person records for kids who don't have their own full entry yet.
    source          {pdf, page}

SEE_REFS marks two codes that refer to the same person. The build script merges
them, preserving both codes in lineageCodes.

To add a new person: append a dict to ENTRIES. Re-run parser/build.py.
"""

SOURCE_FILES = [
    "John_Guthrie - Eight Generations.pdf",
    "William_Guthrie - One Generation.pdf",
    "Stephen_Guthrie - One Generation.pdf",
    "Rachel_Guthrie - One Generation.pdf",
    "James_Guthrie - Seven Generations.pdf",
    "Absalom_Guthrie - One Generation.pdf",
    "Alexander_Guthrie - Five Generations.pdf",
]

FOUNDER_NOTE = (
    "All seven documented PDFs are children of an unnamed common Guthrie patriarch. "
    "Their lineage codes are 1 (John), 2 (William), 5 (Stephen), 6 (Rachel), "
    "7 (James), 8 (Absalom), A (Alexander). Codes 3, 4, 9 are unaccounted for "
    "and may represent siblings whose lines were never documented. The unnamed "
    "patriarch is recorded here as code '0' so all branches connect to a single root."
)

# Same-person-multiple-codes table. Each entry merges into one Person record.
SEE_REFS = [
    # Ray Guthrie appears under James's branch (74A, as son of Jeremiah) and
    # under John's branch (172A, via mother Nancy Ann Nicola). Same person.
    {"codes": ["74A", "172A"], "reason": "Father Jeremiah=74 in James line; mother Nancy Ann Nicola=172 in John line"},
    # Ward Barnes Guthrie: father Samuel Floyd Guthrie (1133, John line);
    # mother Rosa Mae Barnes (715, James line)
    {"codes": ["11331", "7151"], "reason": "Mother is 715 in James line; father is 1133 in John line"},
    # Stella Guthrie's children appear in both James (747x) and John (1622x) branches
    # via her marriage to Charles C. Moyers
    {"codes": ["7471", "16221"], "reason": "Stella Guthrie 747 (James) m. Charles Moyers 1622 (John)"},
    {"codes": ["7472", "16222"], "reason": "Same"},
    {"codes": ["7473", "16223"], "reason": "Same"},
    {"codes": ["7474", "16224"], "reason": "Same"},
    # Lydia Alice Guthrie (13E, John line) m. Christian Nicola (174, John line) —
    # both are John's descendants; their children appear under both codes
    {"codes": ["13E1", "1741"], "reason": "Lydia 13E m. her cousin Christian Nicola 174"},
    {"codes": ["13E2", "1742"], "reason": "Same"},
    {"codes": ["13E3", "1743"], "reason": "Same"},
    {"codes": ["13E4", "1744"], "reason": "Same"},
    {"codes": ["13E5", "1745"], "reason": "Same"},
    {"codes": ["13E6", "1746"], "reason": "Same"},
    {"codes": ["13E7", "1747"], "reason": "Same"},
    {"codes": ["13E8", "1748"], "reason": "Same"},
    {"codes": ["13E9", "1749"], "reason": "Same"},
]

# ---------------------------------------------------------------------------
# ENTRIES
# ---------------------------------------------------------------------------
ENTRIES = []

# === Founder placeholder ===
ENTRIES.append({
    "code": "0",
    "name": "Unknown Guthrie Patriarch",
    "notes": "Inferred common ancestor of the seven documented sibling branches. "
             "Not directly attested in any of the source PDFs but logically required: "
             "John (b. 1792), William (b. 1794), Stephen (b. 1801), Rachel (b. 1804), "
             "James (b. 1806), Absalom (b. 1810), and Alexander (b. 1815) share "
             "the Guthrie surname, overlap geographically (WV/PA), and the PDFs' "
             "shared numbering scheme treats them as siblings. Gaps at codes 3, 4, "
             "and 9 suggest additional undocumented siblings.",
    "children": [
        {"code": "1", "name": "John Guthrie", "born": "31 Aug 1792"},
        {"code": "2", "name": "William Guthrie", "born": "10 Sep 1794"},
        {"code": "5", "name": "Stephen Guthrie", "born": "26 Mar 1801"},
        {"code": "6", "name": "Rachel Guthrie", "born": "16 Apr 1804"},
        {"code": "7", "name": "James Guthrie", "born": "7 Sep 1806"},
        {"code": "8", "name": "Absalom Guthrie", "born": "20 Feb 1810"},
        {"code": "A", "name": "Alexander B. Guthrie", "born": "30 Apr 1815"},
    ],
})

# === 1. JOHN GUTHRIE ===
ENTRIES.append({
    "code": "1",
    "name": "John Guthrie",
    "sex": "M",
    "born": "31 Aug 1792",
    "born_alt": "21 Sep 1792",
    "died": "10 Dec 1870",
    "buried": "Shady Grove Cemetery",
    "occupation": "Farmer",
    "residences": ["Hazelton, WV (2½ miles east of Brandonville, Grant district)"],
    "notes": "John was a German Baptist farmer and lived 2½ miles east of "
             "Brandonville, WV on part of the farm that was sold to him by his "
             "father near the Guthrie school, Grant district. All nine of his "
             "children were born at Hazelton, WV.",
    "spouses": [{
        "name": "Elizabeth Boger",
        "born": "31 May 1799",
        "died": "15 Feb 1875",
        "father": "John Boger",
        "mother": "Veronica (Fanny) Cober Boger",
        "buried": "Shady Grove Cemetery",
    }],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 1},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "11", "name": "William Guthrie", "born": "1 Apr 1819"},
        {"code": "12", "name": "Nancy Guthrie", "born": "26 Apr 1821", "born_alt": "25 Apr 1821"},
        {"code": "13", "name": "Christian Guthrie", "born": "29 Apr 1824"},
        {"code": "14", "name": "James B. Guthrie", "born": "27 Dec 1826"},
        {"code": "15", "name": "Sarah Guthrie", "born": "22 Oct 1829", "died": "Dec 1833", "flags": {"diedInInfancy": True}},
        {"code": "16", "name": "Elizabeth Guthrie", "born": "26 Oct 1832"},
        {"code": "17", "name": "Susannah Guthrie", "born": "26 May 1835", "born_alt": "20 May 1835"},
        {"code": "18", "name": "John Guthrie", "born": "19 Mar 1839", "died": "1841", "flags": {"diedInInfancy": True}},
        {"code": "19", "name": "Peter Guthrie", "born": "13 Feb 1842", "born_alt": "18 Feb 1842"},
    ],
})

# === 1's children (full entries) ===
ENTRIES.append({
    "code": "11",
    "name": "William Guthrie",
    "sex": "M",
    "born": "1 Apr 1819",
    "died": "19 Feb 1909",
    "notes": "All four first-marriage children were born near Hazelton, WV.",
    "spouses": [
        {"name": "Marih DeBerry", "born": "11 Nov 1823", "died": "17 Apr 1884",
         "father": "Archibald DeBerry", "mother": "Mary Hazlett DeBerry", "order": 1},
        {"name": "Elizabeth Glover Maust", "order": 2},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 1},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "111", "name": "William H. Guthrie", "born": "7 Apr 1841"},
        {"code": "112", "name": "Samuel Guthrie", "born": "21 Jun 1844"},
        {"code": "113", "name": "Joseph Guthrie", "born": "1 Jun 1846"},
        {"code": "114", "name": "Mary Jane Guthrie", "born": "about 1855"},
    ],
})

ENTRIES.append({
    "code": "12",
    "name": "Nancy Guthrie",
    "sex": "F",
    "born": "26 Apr 1821",
    "born_alt": "25 Apr 1821",
    "died": "21 Sep 1891",
    "spouses": [{
        "name": "Martin DeBerry",
        "born": "23 May 1822",
        "died": "27 Apr 1902",
        "father": "Archibald DeBerry",
        "mother": "Mary Hazlett DeBerry",
        "buried": "Shady Grove Cemetery",
    }],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 1},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "121", "name": "Mary E. DeBerry", "born": "about 1846"},
        {"code": "122", "name": "Archibald J. DeBerry", "born": "4 Aug 1850"},
        {"code": "123", "name": "Lucy Ann DeBerry", "born": "21 May 1853"},
        {"code": "124", "name": "Susanna Ella DeBerry", "born": "27 Jul 1862"},
    ],
})

ENTRIES.append({
    "code": "13",
    "name": "Christian Guthrie",
    "sex": "M",
    "born": "29 Apr 1824",
    "died": "18 May 1899",
    "died_alt": "8 May 1899",
    "buried": "Rodeheaver Cemetery near Mt. Dale, WV",
    "occupation": "Farmer",
    "residences": ["Locust Grove, WV"],
    "spouses": [{
        "name": "Almyra Smith",
        "born": "about 1825",
        "father": "Aaron Smith",
        "mother": "Permelia Roberts Smith",
    }],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 2},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "131", "name": "Sopheonia Guthrie", "born": "8 Nov 1845"},
        {"code": "132", "name": "John Guthrie", "born": "28 Dec 1846"},
        {"code": "133", "name": "Sivilla Guthrie", "born": "11 Sep 1848"},
        {"code": "134", "name": "Permilia Guthrie", "born": "28 Feb 1850"},
        {"code": "135", "name": "Elizabeth Ann Guthrie", "born": "28 Feb 1850"},
        {"code": "136", "name": "Jemima Guthrie", "born": "1 Jan 1852"},
        {"code": "137", "name": "Lucinda Guthrie", "born": "16 Apr 1853"},
        {"code": "138", "name": "Florence E. Guthrie", "born": "28 Aug 1854"},
        {"code": "139", "name": "Matilda C. Guthrie", "born": "30 Sep 1856"},
        {"code": "13A", "name": "Mary Alverna Guthrie", "born": "20 Sep 1858", "died": "16 Jun 1937"},
        {"code": "13B", "name": "Isabelle Guthrie", "born": "25 Aug 1860"},
        {"code": "13C", "name": "Arley Smith Guthrie", "born": "14 Mar 1862"},
        {"code": "13D", "name": "Susan Emma Guthrie", "born": "3 May 1864"},
        {"code": "13E", "name": "Lydia Alice Guthrie", "born": "5 May 1866"},
        {"code": "13F", "name": "Walter Christian Guthrie", "born": "10 Jan 1868"},
    ],
})

ENTRIES.append({
    "code": "14",
    "name": "James B. Guthrie",
    "sex": "M",
    "born": "27 Dec 1826",
    "died": "11 Oct 1888",
    "spouses": [{
        "name": "Susannah B. Beeghly",
        "born": "1832",
        "born_place": "Frostburg, MD",
        "died": "1900",
        "died_place": "Hazelton, WV",
        "father": "Michael Beeghly",
        "mother": "Barbara Miller Beeghly",
    }],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 2},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "141", "name": "Elizabeth Guthrie", "born": "4 Jul 1850"},
        {"code": "142", "name": "John Mike Guthrie", "born": "11 Sep 1854"},
        {"code": "143", "name": "Catherine Guthrie", "born": "1856"},
        {"code": "144", "name": "Barbara Ellen Guthrie", "born": "17 Jul 1858"},
        {"code": "145", "name": "David G. Guthrie", "born": "30 Aug 1860"},
        {"code": "146", "name": "Nancy Guthrie", "born": "12 Apr 1863", "died": "1 Jun 1926"},
        {"code": "147", "name": "Albert M. Guthrie", "born": "12 Jul 1864"},
        {"code": "148", "name": "Franklin C. Guthrie", "born": "6 Jul 1868"},
        {"code": "149", "name": "Levi Guthrie", "born": "1871", "died": "10 Jan 1872", "flags": {"diedInInfancy": True}},
        {"code": "14A", "name": "Lucian Guthrie", "born": "about 1872"},
        {"code": "14B", "name": "Mary Guthrie", "born": "about 1874"},
        {"code": "14C", "name": "Jane Guthrie"},
    ],
})

ENTRIES.append({
    "code": "16",
    "name": "Elizabeth Guthrie",
    "sex": "F",
    "born": "26 Oct 1832",
    "died": "14 Mar 1912",
    "buried": "Shady Grove Cemetery, WV",
    "spouses": [{
        "name": "David Kalfus Harshbarger",
        "born": "27 Dec 1825",
        "died": "24 Sep 1909",
        "father": "Jacob Harshbarger",
        "mother": "Nancy Rankin Harshbarger",
        "buried": "Shady Grove Cemetery, WV",
    }],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 2},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "161", "name": "Amanda Jane Harshbarger", "born": "9 Jun 1860"},
        {"code": "162", "name": "Elizabeth M. Harshbarger", "born": "13 May 1863"},
        {"code": "163", "name": "Virginia Alice Harshbarger", "born": "6 Nov 1865"},
        {"code": "164", "name": "Charles A. Harshbarger", "born": "9 Jan 1868"},
        {"code": "165", "name": "David Jacob Harshbarger", "born": "5 Jun 1870"},
        {"code": "166", "name": "Joseph Henry Harshbarger", "born": "3 Mar 1874"},
    ],
})

ENTRIES.append({
    "code": "17",
    "name": "Susannah Guthrie",
    "sex": "F",
    "born": "26 Jun 1835",
    "born_alt": "20 Jun 1835",
    "died": "7 May 1880",
    "buried": "Shady Grove",
    "notes": "Susanna lived most of her life in Barbour County. After her death, "
             "Jacob B. Nicola married Mary Ann (Mollie) Sisler Hayes on 30 Apr 1882. "
             "Mary was born 6 Jan 1844, died 1 Oct 1917, dau of Jacob Henry and Margaret "
             "Teets Sisler, buried at Bluemont Cemetery, Grafton, WV. Their children "
             "(Susannah's stepchildren) were Jacob George Stanley Nicola (b. 6 Apr 1883, "
             "d. 29 Jul 1950), Asa Franklin Nicola (b. 14 Jan 1885, d. 18 Oct 1957), and "
             "Harrison Walter (Harry) Nicola (b. 13 Mar 1887, d. 16 Mar 1973).",
    "spouses": [{
        "name": "Jacob B. Nicola",
        "born": "13 Oct 1832",
        "died": "23 May 1905",
        "father": "John Nicola",
        "mother": "Mary [Boger] Nicola",
        "married": "27 Apr 1856",
        "details": "German Baptist; mill wright, merchant and carpenter. Operated a Grist Mill at Orr, WV (between Cuzzart and Cranesville) when he died; buried near there in the Kelley Cemetery.",
    }],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 3},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "171", "name": "Mary Elizabeth Nicola", "born": "19 Apr 1857"},
        {"code": "172", "name": "Nancy Ann Nicola", "born": "12 Apr 1859"},
        {"code": "173", "name": "John Nicola", "born": "11 Jun 1861"},
        {"code": "174", "name": "Christian Nicola", "born": "21 Dec 1863"},
        {"code": "175", "name": "James W. Nicola", "born": "24 Nov 1865"},
        {"code": "176", "name": "Peter Martin Nicola", "born": "29 Jan 1868"},
        {"code": "177", "name": "Barbara Ellen Nicola", "born": "6 Aug 1870"},
        {"code": "178", "name": "Lovina C. Nicola", "born": "6 Aug 1870"},
        {"code": "179", "name": "Emma C. Nicola", "born": "28 Mar 1875"},
    ],
})

ENTRIES.append({
    "code": "172",
    "name": "Nancy Ann Nicola",
    "sex": "F",
    "born": "12 Apr 1859",
    "died": "1 Jun 1926",
    "spouses": [{
        "name": "Jeremiah Guthrie",
        "born": "10 Sep 1852",
        "died": "25 Apr 1918",
        "married": "7 Apr 1878",
        "details": "Same as #74 in James's branch. This marriage connects John's and James's lines.",
    }],
    "notes": "Daughter of Susannah Guthrie (#17) and Jacob B. Nicola. Her marriage to "
             "Jeremiah Guthrie (#74) connects John's branch to James's branch. Their "
             "children carry double codes: e.g., Ray Guthrie is both 74A and 172A.",
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 11},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1721", "name": "James Guthrie", "born": "2 Feb 1879"},
        {"code": "1722", "name": "Susanna Guthrie", "born": "14 Feb 1880", "died": "14 Sep 1961"},
        {"code": "1723", "name": "Hattie Guthrie", "born": "20 Dec 1881"},
        {"code": "1724", "name": "Norton Guthrie", "born": "13 Apr 1884", "died": "28 Feb 1966"},
        {"code": "1725", "name": "Infant Daughter", "born": "29 Jan 1886", "died": "29 Jan 1886", "flags": {"diedInInfancy": True}},
        {"code": "1726", "name": "Loyd (Lloyd) Guthrie", "born": "2 Apr 1887"},
        {"code": "1727", "name": "Stella Guthrie", "born": "8 May 1889"},
        {"code": "1728", "name": "Troy Guthrie", "born": "24 Feb 1891"},
        {"code": "1729", "name": "Dellie Guthrie", "born": "17 Sep 1893", "died": "22 Jan 1895", "flags": {"diedInInfancy": True}},
        {"code": "172A", "name": "Ray Guthrie", "born": "17 Dec 1895", "died": "16 Jan 1976"},
        {"code": "172B", "name": "Dessie Guthrie", "born": "6 Apr 1899"},
        {"code": "172C", "name": "Infant Son", "born": "1 Jun 1902", "died": "1 Jun 1902", "flags": {"diedInInfancy": True}},
    ],
})

ENTRIES.append({
    "code": "19",
    "name": "Peter Guthrie",
    "sex": "M",
    "born": "13 Feb 1842",
    "born_alt": "18 Feb 1842",
    "died": "Aug 1916",
    "spouses": [{
        "name": "Catherine Nicola Wilson",
        "born": "30 Jan 1838",
        "died": "1907",
        "notes": "Her second marriage.",
    }],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 3},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "191", "name": "Susie Elizabeth Guthrie", "born": "1867"},
        {"code": "192", "name": "John Guthrie", "born": "4 Feb 1869", "died": "in infancy", "flags": {"diedInInfancy": True}},
        {"code": "193", "name": "Henry M. Guthrie", "born": "6 Jul 1870"},
        {"code": "194", "name": "Rev. Wilbert Guthrie", "born": "1875", "died": "1934"},
        {"code": "195", "name": "Charles H. Guthrie", "born": "4 Oct 1876"},
        {"code": "196", "name": "Ida Guthrie", "born": "1880", "born_alt": "1882"},
    ],
})

# === 2. WILLIAM GUTHRIE ===
ENTRIES.append({
    "code": "2",
    "name": "William Guthrie",
    "sex": "M",
    "born": "10 Sep 1794",
    "died": "12 Jul 1873",
    "buried": "Shady Grove Cemetery",
    "spouses": [{
        "name": "Rebecca Jefferys",
        "born": "9 Mar 1801",
        "died": "15 Apr 1869",
        "father": "Benjamin Jefferys",
        "mother": "Elizabeth Smith Jefferys",
        "buried": "Shady Grove Cemetery",
    }],
    "source": {"pdf": "William_Guthrie - One Generation.pdf", "page": 1},
    "children": [
        {"code": "21", "name": "Ruth G. Guthrie", "born": "22 May 1838"},
        {"code": "22", "name": "Eleanor Jane Guthrie", "born": "28 Aug 1840"},
        {"code": "23", "name": "Elnor Guthrie", "born": "1841", "died": "1927"},
        {"code": "24", "name": "Eugenus Guthrie", "born": "16 Mar 1844", "died": "24 Feb 1857"},
    ],
})

ENTRIES.append({
    "code": "21",
    "name": "Ruth G. Guthrie",
    "sex": "F",
    "born": "22 May 1838",
    "died": "6 Dec 1933",
    "buried": "Shady Grove Cemetery",
    "spouses": [{
        "name": "Jonas Frankhouser",
        "born": "20 Sep 1833",
        "died": "3 Feb 1920",
        "father": "Daniel Frankhouser",
        "mother": "Elizabeth Moyers Frankhouser",
        "buried": "Shady Grove Cemetery",
    }],
    "source": {"pdf": "William_Guthrie - One Generation.pdf", "page": 1},
})

ENTRIES.append({
    "code": "22",
    "name": "Eleanor Jane Guthrie",
    "sex": "F",
    "born": "28 Aug 1840",
    "died": "26 Nov 1913",
    "died_alt": "1912",
    "spouses": [{
        "name": "Abner Gaines Harshbarger",
        "born": "1836",
        "died": "1919",
        "father": "Jacob Harshbarger",
        "mother": "Nancy Rankin Harshbarger",
        "married": "27 Oct 1859",
    }],
    "source": {"pdf": "William_Guthrie - One Generation.pdf", "page": 1},
})

# === 5. STEPHEN GUTHRIE ===
ENTRIES.append({
    "code": "5",
    "name": "Stephen Guthrie",
    "sex": "M",
    "born": "26 Mar 1801",
    "died": "28 Nov 1888",
    "buried": "Old Brick Church Cemetery",
    "spouses": [
        {"name": "Fanny Hazlet", "order": 1},
        {"name": "Barbara Dennis", "born": "25 May 1800", "died": "22 Apr 1873", "order": 2},
    ],
    "source": {"pdf": "Stephen_Guthrie - One Generation.pdf", "page": 1},
    "children": [
        # First marriage
        {"code": "51", "name": "Harrison Guthrie"},
        {"code": "52", "name": "Elizabeth Guthrie"},
        # Second marriage
        {"code": "53", "name": "Stephen Guthrie", "born": "7 Apr 1827"},
        {"code": "54", "name": "Catherine Guthrie", "born": "about 1833"},
        {"code": "55", "name": "Mary Guthrie", "born": "about 1835"},
        {"code": "56", "name": "Amy Guthrie", "born": "20 Dec 1840", "died": "1899"},
        {"code": "57", "name": "Bell Guthrie", "born": "1843"},
        {"code": "58", "name": "Israel Guthrie", "born": "1847"},
        {"code": "59", "name": "Absalom Guthrie", "died": "about 1899"},
        {"code": "5A", "name": "Florence Guthrie", "born": "1854", "died": "1887"},
    ],
})

ENTRIES.append({
    "code": "51",
    "name": "Harrison Guthrie",
    "sex": "M",
    "occupation": "Physician in Minnesota",
    "source": {"pdf": "Stephen_Guthrie - One Generation.pdf", "page": 1},
    "children": [
        {"code": "511", "name": "Arthur Guthrie", "occupation": "Major General in the Army"},
    ],
})

ENTRIES.append({
    "code": "53",
    "name": "Stephen Guthrie",
    "sex": "M",
    "born": "7 Apr 1827",
    "born_alt": "17 Apr 1827",
    "died": "31 Mar 1895",
    "spouses": [{
        "name": "Elizabeth Brookmire",
        "born": "1835",
        "died": "1931",
    }],
    "source": {"pdf": "Stephen_Guthrie - One Generation.pdf", "page": 1},
})

ENTRIES.append({
    "code": "56",
    "name": "Amy Guthrie",
    "sex": "F",
    "born": "20 Dec 1840",
    "died": "7 Mar 1917",
    "spouses": [{
        "name": "Daniel Frankhouser",
        "born": "15 Oct 1843",
        "died": "31 Mar 1929",
    }],
    "source": {"pdf": "Stephen_Guthrie - One Generation.pdf", "page": 1},
})

ENTRIES.append({
    "code": "59",
    "name": "Absalom Guthrie",
    "sex": "M",
    "died": "1899",
    "spouses": [{
        "name": "Demaris Denham",
        "died": "11 Sep 1916",
    }],
    "residences": ["Kansas"],
    "source": {"pdf": "Stephen_Guthrie - One Generation.pdf", "page": 1},
})

# === 6. RACHEL GUTHRIE ===
ENTRIES.append({
    "code": "6",
    "name": "Rachel Guthrie",
    "sex": "F",
    "born": "16 Apr 1804",
    "died": "28 Sep 1874",
    "buried": "Shady Grove Cemetery",
    "spouses": [{
        "name": "James G. Crawford",
        "born": "25 Jun 1815",
        "died": "22 Feb 1902",
        "father": "James Crawford",
        "mother": "Maragret Hamilton (Gillis) Crawford",
        "married": "1827",
        "buried": "Shady Grove Cemetery",
    }],
    "source": {"pdf": "Rachel_Guthrie - One Generation.pdf", "page": 1},
    "children": [
        {"code": "61", "name": "Absalom G. Crawford", "born": "27 Jul 1842", "died": "19 Jan 1848", "flags": {"diedInInfancy": True}},
        {"code": "62", "name": "Isabel Crawford"},
        {"code": "63", "name": "Rachel Jane Crawford", "born": "1847"},
        {"code": "64", "name": "Virginia Crawford"},
        {"code": "65", "name": "Mary Ann Crawford"},
    ],
})

ENTRIES.append({
    "code": "62",
    "name": "Isabel Crawford",
    "sex": "F",
    "spouses": [{"name": "Hamilton Gillis"}],
    "source": {"pdf": "Rachel_Guthrie - One Generation.pdf", "page": 1},
})

ENTRIES.append({
    "code": "63",
    "name": "Rachel Jane Crawford",
    "sex": "F",
    "born": "1847",
    "died": "28 Nov 1919",
    "spouses": [{
        "name": "William F. Thomas",
        "born": "16 Apr 1853",
        "died": "19 Feb 1930",
    }],
    "source": {"pdf": "Rachel_Guthrie - One Generation.pdf", "page": 1},
})

# === 7. JAMES GUTHRIE ===
ENTRIES.append({
    "code": "7",
    "name": "James Guthrie",
    "sex": "M",
    "born": "7 Sep 1806",
    "died": "29 Mar 1879",
    "buried": "Shady Grove",
    "spouses": [{
        "name": "Barbara Boger",
        "born": "13 Aug 1820",
        "died": "2 May 1888",
        "father": "John Boger",
        "mother": "Barbara Breneison Boger",
        "married": "28 Jul 1844",
        "buried": "Shady Grove",
    }],
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 1},
    "children": [
        {"code": "71", "name": "Alcinda J. Guthrie", "born": "8 Sep 1845"},
        {"code": "72", "name": "Sarah Ann Guthrie", "born": "21 Feb 1847"},
        {"code": "73", "name": "Ephraim Guthrie", "born": "14 Jun 1850", "died": "20 Oct 1854", "flags": {"diedInInfancy": True}},
        {"code": "74", "name": "Jeremiah Guthrie", "born": "10 Sep 1852"},
        {"code": "75", "name": "Mary Guthrie", "born": "15 Oct 1854", "died": "23 Dec 1872"},
        {"code": "76", "name": "Harrison Guthrie", "born": "22 Apr 1858"},
        {"code": "77", "name": "Lucretia Guthrie", "born": "28 Apr 1860", "died": "28 Apr 1877"},
    ],
})

ENTRIES.append({
    "code": "71",
    "name": "Alcinda J. Guthrie",
    "sex": "F",
    "born": "8 Sep 1845",
    "died": "18 Sep 1923",
    "spouses": [{
        "name": "Fleming C. Barnes",
        "born": "9 Mar 1839",
        "died": "4 Feb 1927",
        "married": "20 Apr 1862",
    }],
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 1},
})

ENTRIES.append({
    "code": "74",
    "name": "Jeremiah Guthrie",
    "sex": "M",
    "born": "10 Sep 1852",
    "died": "25 Apr 1918",
    "spouses": [{
        "name": "Nancy Ann Nicola",
        "born": "12 Apr 1859",
        "died": "1 Jun 1926",
        "married": "7 Apr 1878",
        "notes": "Same person as #172 in John's branch — daughter of Susannah Guthrie Nicola.",
    }],
    "notes": "His marriage to Nancy Ann Nicola is the most significant Guthrie/Guthrie "
             "cross-branch union: James-line man marries John-line woman. Their children "
             "therefore carry two valid lineage codes (e.g., Ray Guthrie = 74A = 172A).",
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 1},
})

ENTRIES.append({
    "code": "76",
    "name": "Harrison Guthrie",
    "sex": "M",
    "born": "22 Apr 1858",
    "died": "5 Apr 1937",
    "spouses": [{
        "name": "Lydia Faucet",
        "born": "18 May 1858",
        "died": "5 Nov 1938",
        "married": "13 Apr 1882",
    }],
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 2},
})

# Ray Guthrie (the canonical cross-reference example)
ENTRIES.append({
    "code": "74A",
    "name": "Ray Guthrie",
    "sex": "M",
    "born": "17 Dec 1895",
    "died": "16 Jan 1976",
    "spouses": [{
        "name": "Rhuie Lena Frankhouser",
        "born": "3 Oct 1891",
        "died": "22 Apr 1944",
        "married": "18 Mar 1922",
        "details": "Same person as #A46 in Alexander's branch (daughter of Lucian Frankhouser).",
    }],
    "notes": "Carries two lineage codes: 74A (via father Jeremiah, James's branch) "
             "and 172A (via mother Nancy Ann Nicola, John's branch). Married into "
             "Alexander's branch via Rhuie Lena Frankhouser — connecting three of "
             "the seven sibling lines through one couple.",
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 1},
})

# Stella Guthrie - another cross-branch case (her kids are double-coded)
ENTRIES.append({
    "code": "747",
    "name": "Stella Guthrie",
    "sex": "F",
    "born": "8 May 1889",
    "died": "28 Jan 1960",
    "spouses": [{
        "name": "Charles C. Moyers",
        "born": "23 Sep 1889",
        "died": "27 Jan 1960",
        "married": "16 May 1919",
        "buried": "Shady Grove Cemetery",
        "details": "Same as #1622 in John's branch — son of Amos J. and Maggie Elizabeth (Harshbarger) Moyers, "
                   "grandson of Elizabeth Guthrie (#16). Her children therefore carry double codes (7471=16221, etc).",
    }],
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 1},
})

# === 8. ABSALOM GUTHRIE ===
ENTRIES.append({
    "code": "8",
    "name": "Absalom Guthrie",
    "sex": "M",
    "born": "20 Feb 1810",
    "died": "9 Feb 1869",
    "spouses": [{
        "name": "Sarah Armstrong",
        "born": "15 Nov 1817",
        "died": "31 Dec 1901",
        "married": "6 May 1839",
    }],
    "source": {"pdf": "Absalom_Guthrie - One Generation.pdf", "page": 1},
    "children": [
        {"code": "81", "name": "Isaac Armstrong Guthrie", "born": "8 Feb 1838"},
        {"code": "82", "name": "Mary Frances Guthrie", "born": "6 Feb 1840"},
        {"code": "83", "name": "Rachel Ann Guthrie", "born": "11 Feb 1843", "died": "27 Nov 1912"},
        {"code": "84", "name": "James Marshall Guthrie", "born": "20 May 1845"},
        {"code": "85", "name": "A son", "born": "15 Sep 1847", "died": "in infancy", "flags": {"diedInInfancy": True}},
        {"code": "86", "name": "Isabella Guthrie", "born": "10 May 1849", "died": "1852", "flags": {"diedInInfancy": True}},
        {"code": "87", "name": "John Forman Guthrie", "born": "2 Nov 1851"},
        {"code": "88", "name": "Martha Bell Guthrie", "born": "15 Feb 1854"},
        {"code": "89", "name": "Virginia Alice Guthrie", "born": "6 Apr 1856"},
        {"code": "8A", "name": "Sarah Louise Guthrie", "born": "23 Jan 1859"},
        {"code": "8B", "name": "William Nolan Guthrie", "born": "27 Dec 1861"},
    ],
})

ENTRIES.append({
    "code": "81",
    "name": "Isaac Armstrong Guthrie",
    "sex": "M",
    "born": "8 Feb 1838",
    "died": "29 Jul 1903",
    "spouses": [{
        "name": "Mary Jane Fickell",
        "born": "23 Dec 1842",
        "died": "10 Jul 1905",
        "married": "7 Sep 1865",
    }],
    "source": {"pdf": "Absalom_Guthrie - One Generation.pdf", "page": 1},
})

ENTRIES.append({
    "code": "82",
    "name": "Mary Frances Guthrie",
    "sex": "F",
    "born": "6 Feb 1840",
    "died": "10 Nov 1907",
    "residences": ["Hocking County, Ohio (moved 1863)"],
    "spouses": [{
        "name": "Joseph Harned",
        "born": "26 Jul 1836",
        "died": "29 Mar 1890",
        "married": "26 Nov 1858",
    }],
    "source": {"pdf": "Absalom_Guthrie - One Generation.pdf", "page": 1},
})

ENTRIES.append({
    "code": "87",
    "name": "John Forman Guthrie",
    "sex": "M",
    "born": "2 Nov 1851",
    "died": "14 Apr 1929",
    "spouses": [{
        "name": "Hannah Grimes",
        "born": "6 Jan 1859",
        "married": "27 Dec 1881",
    }],
    "source": {"pdf": "Absalom_Guthrie - One Generation.pdf", "page": 1},
})

ENTRIES.append({
    "code": "88",
    "name": "Martha Bell Guthrie",
    "sex": "F",
    "born": "15 Feb 1854",
    "died": "5 May 1930",
    "spouses": [{
        "name": "Benjamin O'Neil",
        "born": "28 Nov 1852",
        "died": "23 Oct 1909",
        "married": "29 Nov 1874",
        "details": "Hocking County, Ohio.",
    }],
    "source": {"pdf": "Absalom_Guthrie - One Generation.pdf", "page": 2},
})

ENTRIES.append({
    "code": "8B",
    "name": "William Nolan Guthrie",
    "sex": "M",
    "born": "27 Dec 1861",
    "died": "30 Nov 1918",
    "spouses": [{
        "name": "Jennie Aiken",
        "married": "10 Apr 1895",
        "details": "Of Pittsburgh, PA.",
    }],
    "source": {"pdf": "Absalom_Guthrie - One Generation.pdf", "page": 2},
})

# === A. ALEXANDER B. GUTHRIE ===
ENTRIES.append({
    "code": "A",
    "name": "Alexander B. Guthrie",
    "sex": "M",
    "born": "30 Apr 1815",
    "died": "2 Jun 1877",
    "buried": "Shady Grove Cemetery",
    "spouses": [
        {"name": "Mary Jeffers", "born": "11 Jul 1819", "died": "26 May 1848", "order": 1},
        {"name": "Anna Smith", "born": "30 Apr 1818", "died": "12 Jun 1897", "order": 2},
    ],
    "source": {"pdf": "Alexander_Guthrie - Five Generations.pdf", "page": 1},
    "children": [
        # First marriage
        {"code": "A1", "name": "Abner F. Guthrie", "born": "5 Feb 1840", "died": "15 May 1875"},
        {"code": "A2", "name": "Preston T. Guthrie", "born": "4 Jul 1842"},
        {"code": "A3", "name": "Persis Ann Guthrie", "born": "4 May 1844"},
        {"code": "A4", "name": "Louise Alida (Lide) Guthrie", "born": "3 Mar 1846"},
        {"code": "A5", "name": "Mary Caroline Guthrie", "born": "10 May 1847"},
        {"code": "A6", "name": "Edgar W. Guthrie"},
        # Second marriage
        {"code": "A7", "name": "Melissa J. Guthrie", "born": "26 Oct 1848"},
        {"code": "A8", "name": "Allen C. Guthrie", "born": "22 Nov 1849", "died": "1936"},
        {"code": "A9", "name": "Clarissa A. Guthrie", "born": "Dec 1851", "died": "1935"},
        {"code": "AA", "name": "Leander Kidwell Guthrie", "born": "25 Feb 1856", "died": "20 Oct 1914"},
        {"code": "AB", "name": "Demeris E. Guthrie", "born": "22 Feb 1859"},
    ],
})

ENTRIES.append({
    "code": "A2",
    "name": "Preston T. Guthrie",
    "sex": "M",
    "born": "4 Jul 1842",
    "died": "27 Dec 1895",
    "spouses": [{
        "name": "Martha Meyers",
        "born": "18 Jan 1848",
        "died": "29 Jun 1936",
        "married": "7 Mar 1867",
    }],
    "source": {"pdf": "Alexander_Guthrie - Five Generations.pdf", "page": 1},
})

ENTRIES.append({
    "code": "A3",
    "name": "Persis Ann Guthrie",
    "sex": "F",
    "born": "4 May 1844",
    "died": "12 Jul 1918",
    "spouses": [{
        "name": "Samuel F. Romesburg",
        "born": "6 Aug 1840",
        "died": "8 May 1922",
        "married": "17 Jun 1866",
    }],
    "source": {"pdf": "Alexander_Guthrie - Five Generations.pdf", "page": 1},
})

ENTRIES.append({
    "code": "A4",
    "name": "Louise Alida (Lide) Guthrie",
    "sex": "F",
    "born": "3 Mar 1846",
    "died": "18 Mar 1924",
    "spouses": [{
        "name": "Henry Frankhouser",
        "born": "2 Feb 1839",
        "died": "14 Feb 1914",
        "married": "12 Apr 1866",
    }],
    "source": {"pdf": "Alexander_Guthrie - Five Generations.pdf", "page": 1},
})

ENTRIES.append({
    "code": "A5",
    "name": "Mary Caroline Guthrie",
    "sex": "F",
    "born": "10 May 1847",
    "died": "21 May 1915",
    "spouses": [{"name": "Nicolas Bolyard"}],
    "source": {"pdf": "Alexander_Guthrie - Five Generations.pdf", "page": 2},
})

ENTRIES.append({
    "code": "A45",
    "name": "Alice Pearl Frankhouser",
    "sex": "F",
    "born": "9 Jun 1880",
    "died": "3 Jan 1969",
    "spouses": [{
        "name": "Melvin (Mel) Ray Cupp",
        "born": "18 May 1879",
        "died": "12 May 1935",
        "married": "25 May 1904",
    }],
    "notes": "Mother of Mary Cupp Summers (who married Glenn Webster Barnes #7144 in James's line).",
    "source": {"pdf": "Alexander_Guthrie - Five Generations.pdf", "page": 4},
})

# === Deeper John branch — generation 3 ===
ENTRIES.append({
    "code": "111",
    "name": "William Harrison Guthrie",
    "sex": "M",
    "born": "7 Apr 1841",
    "died": "29 Sep 1943",
    "spouses": [{"name": "Matilda May Strawser", "died": "1 Jan 1938", "married": "2 Mar 1882"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 4},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1111", "name": "Rhuey Pearl Guthrie", "born": "22 Feb 1885"},
        {"code": "1112", "name": "Ada Ellen Guthrie", "born": "17 Feb 1887"},
        {"code": "1113", "name": "Chester Earl Guthrie", "born": "11 Dec 1888"},
        {"code": "1114", "name": "Cora May Guthrie", "born": "13 Oct 1895"},
        {"code": "1115", "name": "Martha Guthrie"},
    ],
})

ENTRIES.append({
    "code": "113",
    "name": "Joseph Guthrie",
    "sex": "M",
    "born": "1 Jun 1846",
    "died": "12 Nov 1912",
    "occupation": "Pastor of the Brethren Church; blacksmith and farmer",
    "notes": "Elected to the ministry in 1880. Lived east of Hazelton on a farm and "
             "moved to Hazelton when he retired. Died at Hazelton.",
    "spouses": [{"name": "Hannah Ellen Kelly", "born": "17 Mar 1850", "died": "26 Oct 1947", "married": "1870"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 4},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1131", "name": "Martha Ellen Guthrie", "born": "22 Jul 1871"},
        {"code": "1132", "name": "Charles Allen Guthrie", "born": "20 Feb 1873"},
        {"code": "1133", "name": "Samuel Floyd Guthrie", "born": "7 Sep 1878"},
        {"code": "1134", "name": "Mary Etta Guthrie", "born": "16 Jul 1882"},
        {"code": "1135", "name": "Sarah Jane Guthrie", "born": "1 Jun 1885"},
        {"code": "1136", "name": "Frank Guthrie", "born": "1 Jun 1885"},
    ],
})

ENTRIES.append({
    "code": "122",
    "name": "Archibald J. DeBerry",
    "sex": "M",
    "born": "4 Aug 1850",
    "died": "10 Jun 1895",
    "spouses": [
        {"name": "Rebecca Graham", "born": "23 May 1851", "died": "15 Jun 1892", "married": "12 Oct 1871", "order": 1},
        {"name": "Sarah M. Plum", "married": "15 Jun 1894", "order": 2},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 4},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1221", "name": "James R. DeBerry", "born": "22 Nov 1872", "died": "13 Dec 1896"},
        {"code": "1222", "name": "Oliver Martin DeBerry", "born": "28 Jun 1874"},
        {"code": "1223", "name": "Nancy Arletta DeBerry", "born": "7 May 1876"},
        {"code": "1224", "name": "Charles Allen DeBerry", "born": "8 Jul 1878"},
        {"code": "1225", "name": "John C. DeBerry", "born": "29 Oct 1880", "died": "11 Dec 1897"},
        {"code": "1226", "name": "Henry R. DeBerry", "born": "5 Dec 1882"},
        {"code": "1227", "name": "Stanford Earl DeBerry", "born": "11 Dec 1884"},
        {"code": "1228", "name": "Edna (Eline) Ethel DeBerry", "born": "2 Feb 1885", "born_alt": "2 Feb 1886", "died": "24 Jul 1899"},
        {"code": "1229", "name": "William Vance DeBerry", "born": "24 Nov 1888"},
        {"code": "122A", "name": "Ola Otis DeBerry", "born": "11 May 1891"},
        {"code": "122B", "name": "Jasper Nelson DeBerry", "born": "17 Nov 1894"},
    ],
})

ENTRIES.append({
    "code": "123",
    "name": "Lucy Ann DeBerry",
    "sex": "F",
    "born": "21 May 1853",
    "died": "29 Aug 1926",
    "spouses": [{"name": "John Henry Deal", "born": "19 Apr 1843", "died": "11 Apr 1911", "married": "1 Jan 1878"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 5},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1231", "name": "Charles Deal", "born": "1878"},
        {"code": "1232", "name": "Grace Deal"},
        {"code": "1233", "name": "Bruce Deal", "born": "24 May 1881"},
        {"code": "1234", "name": "Daisy Deal", "born": "26 Jan 1883"},
        {"code": "1235", "name": "Julia Deal", "born": "23 Dec 1884"},
        {"code": "1236", "name": "Ella Delmerrl Deal", "born": "13 Jan 1887"},
        {"code": "1237", "name": "Ina Deal", "born": "26 Jan 1889"},
        {"code": "1238", "name": "Rhoda Deal", "born": "2 May 1892"},
        {"code": "1239", "name": "Rena Deal", "born": "3 Aug 1896", "died": "11 Jul 1965"},
        {"code": "123A", "name": "Jackson Deal", "born": "21 Feb 1899", "died": "16 Oct 1923"},
    ],
})

ENTRIES.append({
    "code": "13B",
    "name": "Isabelle Guthrie",
    "sex": "F",
    "born": "25 Aug 1860",
    "died": "Apr 1916",
    "spouses": [
        {"name": "George James Skiles", "order": 1},
        {"name": "John Haddix", "order": 2},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 6},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "13B1", "name": "William Skiles", "died": "as a child", "flags": {"diedInInfancy": True}},
        {"code": "13B2", "name": "Lily May Skiles", "born": "19 Aug 1883"},
        {"code": "13B3", "name": "Mary Elizabeth Skiles", "born": "23 Aug 1886", "died": "1958"},
        {"code": "13B4", "name": "Pearl Tracy Skiles", "born": "1888", "died": "1906", "died_alt": "1911"},
        {"code": "13B5", "name": "James Fieldon Skiles", "born": "1890"},
        {"code": "13B6", "name": "Rosa Ola Skiles", "born": "20 Aug 1892"},
        {"code": "13B7", "name": "Frederick Haddix", "born": "1896", "born_place": "Barbour County", "died": "1976"},
        {"code": "13B8", "name": "Florence Haddix"},
        {"code": "13B9", "name": "Claud Haddix", "died": "about 1924"},
        {"code": "13BA", "name": "Denzid Haddix", "born": "1903", "died": "1909", "flags": {"diedInInfancy": True}},
    ],
})

ENTRIES.append({
    "code": "13E",
    "name": "Lydia Alice Guthrie",
    "sex": "F",
    "born": "5 May 1866",
    "died": "1 May 1948",
    "spouses": [{
        "name": "Christian Nicola",
        "born": "21 Dec 1863",
        "died": "8 Mar 1932",
        "married": "2 Dec 1884",
        "details": "Same as #174 in John's branch (her cousin — son of Susannah Guthrie Nicola).",
    }],
    "notes": "Married her first cousin Christian Nicola. Their children appear under both 13E* (via her) and 174* (via him).",
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 7},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "13E1", "name": "Troy A. Nicola", "born": "11 Jun 1886"},
        {"code": "13E2", "name": "Estella L. Nicola", "born": "11 Oct 1887"},
        {"code": "13E3", "name": "Fredrick Nicola", "born": "1891"},
        {"code": "13E4", "name": "Clarence Herbert Nicola", "born": "28 Mar 1894"},
        {"code": "13E5", "name": "Homer Andrew Nicola", "born": "16 Oct 1896"},
        {"code": "13E6", "name": "Ruby May Nicola", "born": "5 Apr 1901"},
        {"code": "13E7", "name": "Luara B. Nicola", "born": "1904"},
        {"code": "13E8", "name": "Dorsey E. Nicola"},
        {"code": "13E9", "name": "Ola Ruth Nicola", "born": "1908"},
        {"code": "13EA", "name": "Infant", "died": "in infancy", "flags": {"diedInInfancy": True}},
        {"code": "13EB", "name": "Infant", "died": "in infancy", "flags": {"diedInInfancy": True}},
    ],
})

ENTRIES.append({
    "code": "13F",
    "name": "Walter Christian Guthrie",
    "sex": "M",
    "born": "10 Jan 1868",
    "died": "22 Oct 1923",
    "spouses": [
        {"name": "Malinda Jane Rodeheaver", "died": "1900", "order": 1},
        {"name": "Elizabeth Thomas", "died": "30 May 1901", "order": 2},
        {"name": "Cora Catherine Knox", "born": "18 Feb 1883", "died": "25 Apr 1960", "order": 3},
    ],
    "notes": "PDF lists children 13F1-13F6 under \"Second Marriage\" (1886-1899) and "
             "13F7-13FG under \"Third Marriage\" (1902+). The dates for Malinda's "
             "death (1900) and Elizabeth's death (30 May 1901) sit awkwardly with "
             "the children's birth years; likely one of those death dates is an OCR "
             "or transcription error in the source PDF.",
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 7},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        # Second marriage (per PDF)
        {"code": "13F1", "name": "Lloyd Milton Guthrie", "born": "24 Jul 1886"},
        {"code": "13F2", "name": "Della Mae Guthrie", "born": "1891", "died": "1891", "flags": {"diedInInfancy": True}},
        {"code": "13F3", "name": "Infant Daughter", "born": "10 Dec 1894", "died": "1894", "flags": {"diedInInfancy": True}},
        {"code": "13F4", "name": "Troy McCledlon Guthrie", "born": "11 Jan 1895", "died": "31 Jul 1919"},
        {"code": "13F5", "name": "Matila (Mammie) Mae Guthrie", "born": "9 Dec 1897"},
        {"code": "13F6", "name": "Henry Rudolph (Dolph) Guthrie", "born": "31 Dec 1899", "died": "6 Aug 1918"},
        # Third marriage (per PDF)
        {"code": "13F7", "name": "James Quinter Guthrie", "born": "31 Dec 1902"},
        {"code": "13F8", "name": "George Robert Guthrie", "born": "12 Feb 1903"},
        {"code": "13F9", "name": "Martha Guthrie", "born": "18 Mar 1906"},
        {"code": "13FA", "name": "Mary Elizabeth Guthrie", "born": "18 Mar 1907"},
        {"code": "13FB", "name": "Dessie Myrtle Guthrie", "born": "1 Jul 1909"},
        {"code": "13FC", "name": "Susan (Susie) Murhl Guthrie", "born": "26 May 1911"},
        {"code": "13FD", "name": "John Ray Guthrie", "born": "1 Oct 1914"},
        {"code": "13FE", "name": "Nellie Virginia Guthrie", "born": "20 Mar 1917"},
        {"code": "13FF", "name": "Alice Frances Guthrie", "born": "6 Jun 1919"},
        {"code": "13FG", "name": "Harley Theodore Guthrie", "born": "28 Mar 1922", "died": "31 Oct 1925", "flags": {"diedInInfancy": True}},
    ],
})

ENTRIES.append({
    "code": "174",
    "name": "Christian Nicola",
    "sex": "M",
    "born": "21 Dec 1863",
    "died": "8 Mar 1932",
    "spouses": [{
        "name": "Lydia Alice Guthrie",
        "born": "5 May 1866",
        "died": "1 May 1948",
        "married": "2 Dec 1884",
        "details": "Same as #13E in John's branch (his cousin).",
    }],
    "notes": "Son of Susannah Guthrie Nicola (#17). Married his cousin Lydia Alice Guthrie (#13E). "
             "Children are shared with 13E and appear under both 13Ex (via her) and 174x (via him); "
             "see SEE_REFS.",
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 7},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": "Detailed entry is documented under 13E on page 7; this is the cross-branch placeholder."},
})

ENTRIES.append({
    "code": "166",
    "name": "Joseph Henry Harshbarger",
    "sex": "M",
    "born": "3 Mar 1874",
    "died": "15 Jan 1938",
    "spouses": [{
        "name": "Hattie Guthrie",
        "born": "20 Dec 1881",
        "died": "7 Jan 1925",
        "married": "28 Apr 1902",
        "details": "Same as #743 in James's branch. Also referenced as 1723 (see). This marriage is another John-line/James-line union.",
    }],
    "notes": "John-line man (via grandmother Elizabeth Guthrie #16) married James-line woman.",
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 10},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1661", "name": "Homer Loid Harshbarger", "born": "27 Sep 1902", "died": "6 Apr 1927"},
        {"code": "1662", "name": "Emma Harshbarger", "born": "30 Jan 1906"},
        {"code": "1663", "name": "Jeremiah Joseph Harshbarger", "born": "6 Jul 1911"},
        {"code": "1664", "name": "David Harshbarger", "born": "9 Dec 1913"},
    ],
})

ENTRIES.append({
    "code": "743",
    "name": "Hattie Guthrie",
    "sex": "F",
    "born": "20 Dec 1881",
    "died": "7 Jan 1925",
    "spouses": [{
        "name": "Joseph Henry Harshbarger",
        "born": "3 Mar 1874",
        "died": "15 Jan 1938",
        "married": "28 Apr 1902",
        "details": "Same as #166 in John's branch.",
    }],
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 3},
})

ENTRIES.append({
    "code": "1622",
    "name": "Charles C. Moyers",
    "sex": "M",
    "born": "23 Sep 1889",
    "died": "26 May 1956",
    "buried": "Shady Grove Cemetery, WV",
    "spouses": [{
        "name": "Stella Guthrie",
        "born": "8 May 1889",
        "died": "27 Jan 1960",
        "married": "16 May 1920",
        "details": "Same as #747 in James's branch.",
    }],
    "notes": "Son of Amos J. and Maggie Elizabeth (Harshbarger) Moyers. His mother "
             "Elizabeth Margaret Harshbarger (#162) is daughter of Elizabeth Guthrie "
             "(#16). So this marriage is a third John/James cross-link. Older entry "
             "had died: 27 Jan 1960 (his death) and Stella died: 28 Jan 1960 — PDF p 30 "
             "shows Charles d. 26 May 1956 and Stella d. 27 Jan 1960; marriage was 16 May 1920.",
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 30},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "16221", "name": "Beatrice Mae Moyers", "born": "7 Sep 1921"},
        {"code": "16222", "name": "Alma Maxine Moyers", "born": "20 Oct 1925"},
        {"code": "16223", "name": "Pauline Grace Moyers", "born": "15 Feb 1927"},
        {"code": "16224", "name": "Charles Ray Moyers", "born": "28 Jul 1931"},
    ],
})

ENTRIES.append({
    "code": "162",
    "name": "Elizabeth (Maggie) Margaret Harshbarger",
    "sex": "F",
    "born": "13 May 1863",
    "died": "16 Mar 1928",
    "spouses": [{"name": "Amos J. Moyers", "born": "16 Jan 1836", "died": "21 Apr 1918", "married": "6 Nov 1886"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 10},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1621", "name": "Walter Amos Moyers", "born": "27 Aug 1887"},
        {"code": "1622", "name": "Charles C. Moyers", "born": "23 Sep 1889"},
        {"code": "1623", "name": "Harold D. Moyers", "born": "24 Apr 1891"},
        {"code": "1624", "name": "Rosella May Moyers", "born": "3 May 1899"},
        {"code": "1625", "name": "Bertha O. Moyers"},
        {"code": "1626", "name": "Bessie L. Moyers", "born": "1 Apr 1893", "died": "27 Jan 1933"},
    ],
})

# === Deeper James branch ===
ENTRIES.append({
    "code": "72",
    "name": "Sarah Ann Guthrie",
    "sex": "F",
    "born": "21 Feb 1847",
    "died": "30 Jan 1880",
    "spouses": [{"name": "Jacob Peter Barnes", "born": "21 Jun 1842", "died": "12 Jan 1938", "married": "27 Aug 1868"}],
    "notes": "After Sarah's death, Jacob Peter Barnes married Amanda Jane Harshbarger (#161). See entry 161.",
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 1},
})

ENTRIES.append({
    "code": "161",
    "name": "Amanda Jane Harshbarger",
    "sex": "F",
    "born": "9 Jun 1860",
    "died": "25 Sep 1933",
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1611", "name": "Vida Barnes", "born": "27 Mar 1881"},
        {"code": "1612", "name": "Nannie Barnes", "born": "15 Dec 1882"},
        {"code": "1613", "name": "Walter Scott Barnes", "born": "4 Jun 1886", "died": "1 Dec 1957"},
        {"code": "1614", "name": "Russell Emerson Barnes", "born": "15 Mar 1891", "died": "3 Jan 1925"},
        {"code": "1615", "name": "Leslie Virgil Barnes", "born": "3 Mar 1893", "died": "Dec 1959"},
    ],
    "spouses": [{
        "name": "Jacob Peter Barnes",
        "born": "21 Jun 1842",
        "died": "12 Jan 1938",
        "married": "17 Jun 1880",
        "details": "Second marriage for Jacob; his first wife was Sarah Ann Guthrie (#72).",
    }],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 6},
})

ENTRIES.append({
    "code": "715",
    "name": "Rosa Mae Barnes",
    "sex": "F",
    "born": "2 Sep 1877",
    "died": "3 Oct 1956",
    "spouses": [{
        "name": "Samuel Floyd Guthrie",
        "born": "7 Sep 1878",
        "died": "13 Sep 1939",
        "married": "17 May 1906",
        "details": "Same as #1133 in John's branch — son of Joseph Guthrie (#113).",
    }],
    "notes": "Mother Alcinda J. Guthrie (#71, James's branch), father Fleming C. Barnes. "
             "Her marriage to Samuel Floyd Guthrie is yet another John/James cross-union.",
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 2},
})

ENTRIES.append({
    "code": "1133",
    "name": "Samuel Floyd Guthrie",
    "sex": "M",
    "born": "7 Sep 1878",
    "died": "13 Sep 1939",
    "spouses": [{
        "name": "Rosa Mae Barnes",
        "born": "2 Sep 1877",
        "died": "3 Oct 1956",
        "married": "17 May 1906",
        "details": "Same as #715 in James's branch — daughter of Fleming C. and Alcinda J. [Guthrie] Barnes.",
    }],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 14},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "11331", "name": "Ward Barnes Guthrie", "born": "29 Jul 1916"},
    ],
})

# Ward Barnes Guthrie - their son, double-coded
ENTRIES.append({
    "code": "11331",
    "name": "Ward Barnes Guthrie",
    "sex": "M",
    "born": "29 Jul 1916",
    "died": "11 Jul 1982",
    "died_place": "AZ",
    "buried": "Shady Grove Cemetery",
    "spouses": [
        {"name": "Laura Cole Barnes", "born": "16 Dec 1918", "died": "15 Nov 1977",
         "married": "29 Jun 1939", "order": 1,
         "details": "Same as #7234 — also a James-line descendant. Ward married within his own extended family."},
        {"name": "Erma Acuna", "married": "16 Mar 1978", "order": 2},
    ],
    "notes": "Carries codes 11331 (via Samuel Floyd Guthrie, John line) and 7151 (via Rosa Mae Barnes, James line). "
             "Married Laura Cole Barnes, herself a James-line descendant.",
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 26},
})

# === Deeper Alexander branch ===
ENTRIES.append({
    "code": "A1",
    "name": "Abner F. Guthrie",
    "sex": "M",
    "born": "5 Feb 1840",
    "born_alt": "12 Apr 1840",
    "died": "15 May 1875",
    "died_alt": "Apr 1875",
    "source": {"pdf": "Alexander_Guthrie - Five Generations.pdf", "page": 1},
})

ENTRIES.append({
    "code": "AB",
    "name": "Demeris E. Guthrie",
    "sex": "F",
    "born": "22 Feb 1859",
    "died": "27 Feb 1919",
    "spouses": [{
        "name": "Benjamin F. Faulkner",
        "born": "25 Aug 1860",
        "died": "4 Nov 1917",
        "married": "2 Apr 1892",
    }],
    "source": {"pdf": "Alexander_Guthrie - Five Generations.pdf", "page": 2},
})

ENTRIES.append({
    "code": "A41",
    "name": "Lucian Emmer Frankhouser",
    "sex": "M",
    "born": "24 Mar 1866",
    "died": "17 Dec 1934",
    "spouses": [{"name": "Laura M. Deal", "born": "7 Nov 1869", "died": "11 Sep 1957", "married": "14 Feb 1895"}],
    "source": {"pdf": "Alexander_Guthrie - Five Generations.pdf", "page": 3},
})

ENTRIES.append({
    "code": "A456",
    "name": "Martin Luther Cupp",
    "sex": "M",
    "born": "9 May 1918",
    "spouses": [{
        "name": "Mary Jean Guthrie",
        "born": "29 Aug 1934",
        "married": "9 May 1953",
        "details": "Same as #13F72 in John's branch (daughter of James Quinter Guthrie #13F7).",
    }],
    "notes": "Marriage connects Alexander's branch (via Alice Pearl Frankhouser #A45) "
             "to John's branch (via Mary Jean Guthrie #13F72).",
    "source": {"pdf": "Alexander_Guthrie - Five Generations.pdf", "page": 7},
})

ENTRIES.append({
    "code": "A46",
    "name": "Rhuie Lena Frankhouser",
    "sex": "F",
    "born": "3 Oct 1891",
    "died": "22 Apr 1944",
    "spouses": [{
        "name": "Ray Guthrie",
        "born": "17 Dec 1895",
        "died": "16 Jan 1976",
        "married": "18 Mar 1922",
        "details": "Same person as 74A in James's branch / 172A in John's branch.",
    }],
    "notes": "Her marriage to Ray Guthrie links Alexander's branch with both James's and John's branches.",
    "source": {"pdf": "Alexander_Guthrie - Five Generations.pdf", "page": 1},
})

# === Children of Lydia/Christian (13E*/174* — activates that SEE_REF cluster) ===
ENTRIES.append({
    "code": "13E1",
    "name": "Troy A. Nicola",
    "sex": "M",
    "born": "11 Jun 1886",
    "died": "10 Jul 1952",
    "spouses": [
        {"name": "Bertha Montgomery", "order": 1},
        {"name": "Elsie Lambert", "born": "1905", "died": "1956", "order": 2},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 22},
})

ENTRIES.append({
    "code": "13E2",
    "name": "Estella L. Nicola",
    "sex": "F",
    "born": "10 Oct 1887",
    "born_alt": "11 Oct 1887",
    "died": "20 Oct 1911",
    "spouses": [{"name": "George Moore", "born": "22 Jun 1884", "died": "1940", "married": "12 Nov 1904"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 22},
})

ENTRIES.append({
    "code": "13E4",
    "name": "Clarence Herbert Nicola",
    "sex": "M",
    "born": "28 Mar 1894",
    "died": "1971",
    "spouses": [{"name": "Lillian S. Ridenour", "born": "23 Oct 1902", "died": "1965", "married": "1920"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 23},
})

ENTRIES.append({
    "code": "13E5",
    "name": "Homer Andrew Nicola",
    "sex": "M",
    "born": "16 Oct 1896",
    "spouses": [{"name": "Dove Poling", "born": "22 Jun 1898", "married": "24 Jun 1921"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 23},
})

# === Children of Stella/Charles (7471-7474 = 16221-16224 — activates that cluster) ===
ENTRIES.append({
    "code": "7471",
    "name": "Beatrice Mae Moyers",
    "sex": "F",
    "born": "7 Sep 1921",
    "spouses": [{"name": "Lloyd Baysinger", "born": "3 Oct 1909", "married": "11 Feb 1950"}],
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 9},
})

ENTRIES.append({
    "code": "7472",
    "name": "Alma Maxine Moyers",
    "sex": "F",
    "born": "20 Oct 1925",
    "spouses": [{"name": "Urban Lavern Long", "born": "13 Sep 1929", "married": "20 Jun 1951"}],
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 9},
})

ENTRIES.append({
    "code": "7473",
    "name": "Pauline Grace Moyers",
    "sex": "F",
    "born": "15 Feb 1927",
    "died": "23 Jun 1981",
    "spouses": [{"name": "Paul Carlus Sines", "married": "Sep 1953", "details": "Son of Alvin and Anna [Guthrie] Sines."}],
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 9},
})

ENTRIES.append({
    "code": "7474",
    "name": "Charles Ray Moyers",
    "sex": "M",
    "born": "28 Jul 1931",
    "spouses": [{"name": "Dorothy (Dottie) N. Shoemaker", "born": "22 Dec 1934", "married": "12 Apr 1953"}],
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 9},
})

# === More John gen 2/3 depth ===
ENTRIES.append({
    "code": "13A",
    "name": "Mary Alverna Guthrie",
    "sex": "F",
    "born": "20 Sep 1858",
    "died": "16 Jun 1937",
    "buried": "Shady Grove Cemetery",
    "spouses": [{
        "name": "Jacob M. A. Thomas",
        "born": "16 Nov 1847",
        "died": "18 Jun 1934",
        "father": "Abraham Thomas",
        "mother": "Nancy Meyers Thomas",
        "buried": "Shady Grove Cemetery",
    }],
    "notes": "Raised Violet Seamon.",
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 2},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
})

ENTRIES.append({
    "code": "132",
    "name": "John Guthrie",
    "sex": "M",
    "born": "28 Dec 1846",
    "died": "15 Jun 1917",
    "spouses": [{"name": "Emma Hollis Dotson", "born": "27 Jun 1840", "died": "16 May 1930"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 5},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1321", "name": "Herbert Holland Guthrie", "born": "20 Feb 1870"},
        {"code": "1322", "name": "Charles Dotson Guthrie", "born": "2 Mar 1872"},
        {"code": "1323", "name": "Homer Rudolph Guthrie", "born": "8 Oct 1874", "died": "14 Dec 1962"},
        {"code": "1324", "name": "V.O. Della Guthrie", "born": "17 Sep 1876"},
        {"code": "1325", "name": "Maude May Guthrie", "born": "23 Dec 1879"},
        {"code": "1326", "name": "Rena Clyde Guthrie", "born": "10 Oct 1884"},
    ],
})

# === John gen 3 — new from pages 4-5 vision pass (2026-06-07) ===
ENTRIES.append({
    "code": "112",
    "name": "Samuel Guthrie",
    "sex": "M",
    "born": "21 Jun 1844",
    "died": "22 Mar 1902",
    "spouses": [{"name": "Mary C. Miller", "born": "8 Mar 1848"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 4},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1121", "name": "George Walter Guthrie", "born": "12 May 1870"},
        {"code": "1122", "name": "Laura A. Guthrie", "born": "Mar 1875"},
        {"code": "1123", "name": "Nancy Ellen Guthrie", "born": "8 Aug 1877"},
        {"code": "1124", "name": "Effie F. Guthrie", "born": "24 Dec 1884"},
    ],
})

ENTRIES.append({
    "code": "114",
    "name": "Mary Jane Guthrie",
    "sex": "F",
    "born": "about 1855",
    "spouses": [{"name": "Elisha A. Hartman", "married": "2 Jun 1871"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 4},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1141", "name": "Walter Reed Hartman", "born": "26 Jul 1872"},
        {"code": "1142", "name": "Minnie M. Hartman", "born": "9 Jul 1879", "died": "12 Jan 1960"},
    ],
})

ENTRIES.append({
    "code": "124",
    "name": "Susanna Ella DeBerry",
    "sex": "F",
    "born": "27 Jul 1862",
    "died": "4 Jul 1896",
    "spouses": [{
        "name": "Wilbur Franklin Moyers",
        "born": "22 Aug 1864",
        "died": "1 Jun 1951",
        "father": "Amos Moyers",
        "mother": "Elizabeth [Herring] Moyers",
    }],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 5},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1241", "name": "Virgie May Moyers", "born": "8 Nov 1895"},
    ],
})

ENTRIES.append({
    "code": "133",
    "name": "Sivilla Guthrie",
    "sex": "F",
    "born": "11 Sep 1848",
    "spouses": [{"name": "Levi L. Strawser", "born": "about 1850", "married": "4 Jun 1871"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 5},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1331", "name": "Frank Strawser"},
        {"code": "1332", "name": "Lewis Strawser"},
        {"code": "1333", "name": "Rebecca Strawser"},
        {"code": "1334", "name": "Rena Strawser"},
    ],
})

ENTRIES.append({
    "code": "135",
    "name": "Elizabeth Ann Guthrie",
    "sex": "F",
    "born": "28 Feb 1850",
    "died": "3 Oct 1940",
    "spouses": [{"name": "Richard Lewis", "born": "1851", "died": "1932", "married": "30 Oct 1871"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 5},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1351", "name": "Charles Howard Lewis", "born": "1873", "died": "25 Feb 1953"},
        {"code": "1352", "name": "Melvin Lewis"},
        {"code": "1353", "name": "Walter Cristy Lewis", "born": "14 Jun 1880", "died": "1967"},
        {"code": "1354", "name": "Clyde D. Lewis", "born": "14 Jun 1890"},
    ],
})

ENTRIES.append({
    "code": "136",
    "name": "Jemima Guthrie",
    "sex": "F",
    "born": "1 Jan 1852",
    "died": "12 Jun 1942",
    "spouses": [{"name": "Ezra Turney", "born": "12 Aug 1838", "died": "19 Dec 1923", "married": "1871"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 5},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1361", "name": "Stephen Turney", "born": "19 Dec 1872", "died": "11 Apr 1881"},
        {"code": "1362", "name": "Florence Iey Turney", "born": "10 May 1874", "died": "20 Jul 1953"},
        {"code": "1363", "name": "Henry R. Turney", "born": "12 May 1875", "died": "12 Oct 1953"},
        {"code": "1364", "name": "Christian Turney", "born": "23 Jul 1877", "died": "12 Mar 1878", "flags": {"diedInInfancy": True}},
        {"code": "1365", "name": "Maud Turney"},
        {"code": "1366", "name": "Pearl A. Turney", "born": "10 Mar 1884"},
        {"code": "1367", "name": "Clarence I. Turney", "born": "21 Apr 1885", "died": "1885", "flags": {"diedInInfancy": True}},
        {"code": "1368", "name": "George Turney", "born": "24 Jan 1888", "died": "28 Dec 1910"},
    ],
})

# === John gen 3/4 — terminal entries with marriage info, page 1-5 vision pass ===
ENTRIES.append({
    "code": "131",
    "name": "Sopheonia Guthrie",
    "sex": "F",
    "born": "8 Nov 1845",
    "spouses": [{"name": "Charles Murphy", "married": "29 Mar 1874"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 2},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
})

ENTRIES.append({
    "code": "134",
    "name": "Permilia Guthrie",
    "sex": "F",
    "born": "28 Feb 1850",
    "residences": ["Terra Alta"],
    "spouses": [
        {"name": "John Henline", "order": 1},
        {"name": "J. Allen Bucklew", "born": "16 Jan 1843", "married": "Aug 1909", "order": 2},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 2},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
})

ENTRIES.append({
    "code": "137",
    "name": "Lucinda Guthrie",
    "sex": "F",
    "born": "16 Apr 1853",
    "spouses": [{"name": "Howard Welsh"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 2},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
})

ENTRIES.append({
    "code": "139",
    "name": "Matilda C. Guthrie",
    "sex": "F",
    "born": "30 Sep 1856",
    "spouses": [{"name": "James Meyers"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 2},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
})

ENTRIES.append({
    "code": "1115",
    "name": "Martha Guthrie",
    "sex": "F",
    "spouses": [
        {"name": "Walter Wendell", "order": 1},
        {"name": "Robert McCorick", "order": 2},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 4},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
})

ENTRIES.append({
    "code": "193",
    "name": "Henry M. Guthrie",
    "sex": "M",
    "born": "6 Jul 1870",
    "spouses": [{"name": "Malada McGee"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 3},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
})

ENTRIES.append({
    "code": "194",
    "name": "Rev. Wilbert Guthrie",
    "sex": "M",
    "born": "1875",
    "died": "1934",
    "spouses": [{"name": "Ninda Myers"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 3},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
})

ENTRIES.append({
    "code": "1239",
    "name": "Rena Deal",
    "sex": "F",
    "born": "3 Aug 1896",
    "died": "11 Jul 1965",
    "spouses": [
        {"name": "Ted Groves", "order": 1},
        {"name": "Clark Riggs", "born": "1881", "died": "1936", "order": 2},
        {"name": "Charles Gainer", "order": 3},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 5},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
})

ENTRIES.append({
    "code": "1323",
    "name": "Homer Rudolph Guthrie",
    "sex": "M",
    "born": "8 Oct 1874",
    "died": "14 Dec 1962",
    "spouses": [{
        "name": "Esther Reckart",
        "born": "22 Sep 1885",
        "died": "6 Mar 1963",
        "notes": "PDF appears to show '22 Sep 1985' but that's an OCR/print artifact — context (predeceasing husband by 9 months in 1963) requires 1885.",
    }],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 5},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
})

ENTRIES.append({
    "code": "1362",
    "name": "Florence Iey Turney",
    "sex": "F",
    "born": "10 May 1874",
    "died": "20 Jul 1953",
    "spouses": [{"name": "Frank Frazee"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 5},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
})

# === John gen 3 parents — pages 6-10 (2026-06-07 vision pass) ===
ENTRIES.append({
    "code": "138",
    "name": "Florence E. Guthrie",
    "sex": "F",
    "born": "28 Aug 1854",
    "died": "15 Apr 1887",
    "spouses": [{"name": "Harrison Teets", "born": "19 Mar 1848", "died": "12 Apr 1928", "married": "3 Dec 1870"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 6},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1381", "name": "John Teets", "died": "at age 37"},
        {"code": "1382", "name": "Albert E. Teets", "born": "24 Jan 1875"},
        {"code": "1383", "name": "Effie M. Teets", "born": "1876", "died": "1958"},
        {"code": "1384", "name": "William Mack Teets", "born": "9 Apr 1879"},
        {"code": "1385", "name": "Minnie Teets"},
        {"code": "1386", "name": "Blanch Bertha Teets", "born": "3 Aug 1885"},
        {"code": "1387", "name": "Lizzie Teets"},
    ],
})

ENTRIES.append({
    "code": "13C",
    "name": "Arley Smith Guthrie",
    "sex": "M",
    "born": "14 Mar 1862",
    "died": "13 Feb 1946",
    "spouses": [
        {"name": "Anna Miller", "died": "24 Dec 1944", "order": 1},
        {"name": "Mary Emma Shartzer", "born": "7 Dec 1880", "died": "24 Dec 1943", "order": 2},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 6},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        # First marriage
        {"code": "13C1", "name": "Earl Guthrie"},
        {"code": "13C2", "name": "Worley Guthrie", "died": "6 May 1949"},
        {"code": "13C3", "name": "Alvin Guthrie"},
        {"code": "13C4", "name": "Alice (Allie) S. Guthrie"},
        {"code": "13C5", "name": "Rena K. Guthrie", "born": "26 Mar 1898"},
        {"code": "13C6", "name": "Elma Guthrie"},
        # Second marriage
        {"code": "13C7", "name": "Russell Guthrie"},
        {"code": "13C8", "name": "Ernest Guthrie"},
        {"code": "13C9", "name": "Arlie Guthrie, Jr.", "born": "5 May 1908"},
        {"code": "13CA", "name": "Edna Guthrie"},
        {"code": "13CB", "name": "Woodrow Wilson Guthrie"},
        {"code": "13CC", "name": "Chester E. Guthrie", "born": "25 Dec 1916", "died": "24 Mar 1962"},
    ],
})

ENTRIES.append({
    "code": "13D",
    "name": "Susan Emma Guthrie",
    "sex": "F",
    "born": "3 May 1864",
    "died": "3 Feb 1923",
    "spouses": [{"name": "David Myers"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 6},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "13D1", "name": "Daniel Myers"},
        {"code": "13D2", "name": "Myrtle Myers"},
        {"code": "13D3", "name": "Roy Myers"},
    ],
})

ENTRIES.append({
    "code": "141",
    "name": "Elizabeth Guthrie",
    "sex": "F",
    "born": "4 Jul 1850",
    "died": "20 May 1908",
    "spouses": [{"name": "James Uphold", "born": "21 May 1845", "died": "13 Sep 1897"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 7},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1411", "name": "James L Uphold, Jr.", "born": "21 Nov 1872", "died": "10 Jun 1914"},
        {"code": "1412", "name": "John Jacob Uphold", "born": "23 Mar 1877"},
        {"code": "1413", "name": "Mary A. Uphold", "born": "15 Jul 1881"},
        {"code": "1414", "name": "Flemming Clyde Uphold", "born": "3 May 1883", "died": "Jan 1945"},
        {"code": "1415", "name": "Charles Ray Uphold", "born": "19 Nov 1885"},
        {"code": "1416", "name": "David Franklin Uphold", "born": "8 Oct 1887"},
        {"code": "1417", "name": "William H. Uphold", "born": "21 May 1890", "died": "21 Nov 1890", "flags": {"diedInInfancy": True}},
        {"code": "1418", "name": "Ella May Uphold", "born": "2 Jul 1892"},
        {"code": "1419", "name": "Laura Bell Uphold"},
        {"code": "141A", "name": "Basil M. Uphold"},
    ],
})

ENTRIES.append({
    "code": "143",
    "name": "Catherine Guthrie",
    "sex": "F",
    "born": "1856",
    "died": "1918",
    "spouses": [
        {"name": "Noah Ross", "born": "7 Nov 1856", "died": "25 Dec 1881", "married": "10 Aug 1879", "order": 1},
        {"name": "Joseph Sliger", "born": "20 Oct 1843", "died": "8 Aug 1935", "order": 2},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 8},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        # First marriage
        {"code": "1431", "name": "Infant", "flags": {"diedInInfancy": True}},
        # Second marriage
        {"code": "1432", "name": "Margaret (Maggie) Sliger", "born": "1883"},
        {"code": "1433", "name": "Sarah Ellen Sliger", "born": "14 Sep 1885"},
        {"code": "1434", "name": "Mollie Sliger", "born": "14 Nov 1888"},
        {"code": "1435", "name": "Emma Pearl Sliger", "born": "15 Aug 1895"},
        {"code": "1436", "name": "Anna Sliger"},
        {"code": "1437", "name": "Bruce Sliger", "died": "1946"},
        {"code": "1438", "name": "Herman Joseph Sliger", "born": "2 Jul 1900"},
    ],
})

ENTRIES.append({
    "code": "146",
    "name": "Nancy Guthrie",
    "sex": "F",
    "born": "12 Apr 1863",
    "died": "1 Jun 1926",
    "spouses": [{"name": "Frank Miller", "born": "20 Mar 1861", "died": "20 Aug 1927"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 9},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1461", "name": "Sarah (Sadie) Catherine Miller", "born": "22 Nov 1883"},
        {"code": "1462", "name": "David C. Miller", "born": "4 Sep 1885"},
        {"code": "1463", "name": "Rosa Mary Miller", "born": "8 May 1887", "died": "6 Sep 1907"},
        {"code": "1464", "name": "Jammy Russie Miller", "born": "20 Jun 1891", "died": "15 Jan 1892", "flags": {"diedInInfancy": True}},
        {"code": "1465", "name": "Rosia Miller", "died": "1928"},
        {"code": "1466", "name": "Howard Miller", "died": "1934"},
        {"code": "1467", "name": "Pearl D. Miller", "born": "22 Mar 1921"},
    ],
})

ENTRIES.append({
    "code": "14A",
    "name": "Lucian Guthrie",
    "sex": "M",
    "born": "about 1872",
    "spouses": [{"name": "Ella Daniel"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 9},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "14A1", "name": "William Guthrie"},
    ],
})

ENTRIES.append({
    "code": "14B",
    "name": "Mary Guthrie",
    "sex": "F",
    "born": "about 1874",
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 9},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "14B1", "name": "Norman Guthrie", "born": "8 Mar 1897"},
    ],
})

ENTRIES.append({
    "code": "163",
    "name": "Virginia Alice (Jennie) Harshbarger",
    "sex": "F",
    "born": "6 Nov 1865",
    "died": "26 Dec 1946",
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 10},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1631", "name": "Jessie Ellen Harshbarger", "born": "20 Feb 1890"},
    ],
})

ENTRIES.append({
    "code": "164",
    "name": "Charles Anderson Harshbarger",
    "sex": "M",
    "born": "9 Jan 1868",
    "died": "5 Mar 1956",
    "spouses": [{
        "name": "Minnie May Thomas",
        "born": "11 Aug 1886",
        "died": "24 Nov 1965",
        "married": "19 Apr 1903",
        "details": "Same as #1443 — daughter of his cousin Barbara Ellen Guthrie (#144). First-cousin-once-removed marriage.",
    }],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 10},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1641", "name": "William Ralph Harshbarger", "born": "3 Feb 1904"},
        {"code": "1642", "name": "Walter David Harshbarger", "born": "16 Oct 1906"},
        {"code": "1643", "name": "Albert Richard Harshbarger", "born": "14 Dec 1908"},
        {"code": "1644", "name": "Harrison Theodore Harshbarger", "born": "4 Apr 1911"},
        {"code": "1645", "name": "Elizabeth Ellen Harshbarger", "born": "7 Apr 1913"},
        {"code": "1646", "name": "May Thomas Harshbarger", "born": "3 Apr 1916", "died": "13 Apr 1916", "flags": {"diedInInfancy": True}},
        {"code": "1647", "name": "Charles Reuben Harshbarger", "born": "16 Nov 1917"},
        {"code": "1648", "name": "Pearl Catherine Harshbarger", "born": "2 Jul 1919"},
        {"code": "1649", "name": "Violet May Harshbarger", "born": "9 Jun 1921"},
        {"code": "164A", "name": "Myrtle Grace Harshbarger", "born": "22 Feb 1923"},
        {"code": "164B", "name": "Daisy Bell Harshbarger", "born": "11 Feb 1925"},
        {"code": "164C", "name": "Goldie Irene Harshbarger", "born": "13 May 1927"},
    ],
})

ENTRIES.append({
    "code": "165",
    "name": "David Jacob Harshbarger",
    "sex": "M",
    "born": "5 Jun 1870",
    "died": "2 Feb 1945",
    "spouses": [{"name": "Francis May Sliger", "married": "1892"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 10},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1651", "name": "Gilbert Harshbarger", "born": "10 Oct 1893"},
        {"code": "1652", "name": "Blanche Harshbarger"},
    ],
})

ENTRIES.append({
    "code": "171",
    "name": "Mary Elizabeth Nicola",
    "sex": "F",
    "born": "19 Apr 1857",
    "died": "10 Dec 1932",
    "spouses": [{"name": "Jonas Spiker", "born": "15 Jun 1845", "died": "9 May 1931", "married": "8 Apr 1875"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 10},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1711", "name": "Jacob George Spiker", "born": "5 Oct 1877"},
        {"code": "1712", "name": "John Henry Spiker", "born": "5 Apr 1881"},
        {"code": "1713", "name": "Oliver Clark Spiker", "born": "15 Feb 1886"},
    ],
})

ENTRIES.append({
    "code": "142",
    "name": "John Mike Guthrie",
    "sex": "M",
    "born": "11 Sep 1854",
    "died": "30 Jul 1932",
    "spouses": [
        {"name": "Susan Elizabeth Guthrie", "born": "1867", "died": "15 Apr 1886",
         "married": "25 Aug 1881", "order": 1,
         "details": "Same as #191 — daughter of his uncle Peter Guthrie (#19). First-cousin marriage."},
        {"name": "Jane Harden", "born": "15 Jan 1865", "married": "1886", "order": 2},
        {"name": "Emma Matheny", "born": "6 May 1867", "died": "16 May 1930", "order": 3},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 8},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        # First marriage
        {"code": "1421", "name": "Truman Guthrie", "born": "1 Apr 1884", "died": "26 Sep 1885", "flags": {"diedInInfancy": True}},
        {"code": "1422", "name": "Son", "born": "15 Apr 1886", "died": "15 Apr 1886", "flags": {"diedInInfancy": True}},
        # Second marriage
        {"code": "1423", "name": "Mary Guthrie", "born": "27 Aug 1886", "died": "12 Aug 1887", "flags": {"diedInInfancy": True}},
        {"code": "1424", "name": "a daughter", "born": "14 Apr 1887", "flags": {"diedInInfancy": True}},
        {"code": "1425", "name": "George Franklin Guthrie", "born": "5 Mar 1890"},
        {"code": "1426", "name": "Sarah Guthrie"},
        # Third marriage
        {"code": "1427", "name": "Orva Guthrie", "born": "18 Jan 1892"},
        {"code": "1428", "name": "Anna Gay Guthrie", "born": "23 Jan 1895"},
        {"code": "1429", "name": "Earl Guthrie", "born": "23 Apr 1896"},
    ],
})

ENTRIES.append({
    "code": "191",
    "name": "Susie Elizabeth Guthrie",
    "sex": "F",
    "born": "1867",
    "died": "15 Apr 1886",
    "spouses": [{
        "name": "John Mike Guthrie",
        "born": "11 Sep 1854",
        "died": "30 Jul 1932",
        "married": "25 Aug 1881",
        "details": "Same as #142 in John's branch — her first cousin. Susie died young.",
    }],
    "notes": "Daughter of Peter Guthrie (#19). Married her first cousin John Mike Guthrie (#142).",
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 8},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": "Detailed entry is documented under 142 on page 8; this is the cross-reference."},
})

ENTRIES.append({
    "code": "144",
    "name": "Barbara Ellen Guthrie",
    "sex": "F",
    "born": "17 Jul 1858",
    "died": "22 May 1921",
    "spouses": [{"name": "William Riley Thomas", "born": "19 Jul 1854", "died": "20 Jun 1921", "married": "4 Aug 1878"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 8},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1441", "name": "Lillie Bell Thomas", "born": "4 Jun 1879"},
        {"code": "1442", "name": "Susannah A. Thomas", "born": "31 Jan 1881"},
        {"code": "1443", "name": "Minnie May Thomas", "born": "11 Aug 1886"},
        {"code": "1444", "name": "Wilbert Thomas", "born": "14 Mar 1889", "died": "30 Sep 1905", "died_alt": "30 Oct 1905"},
        {"code": "1445", "name": "Laura Catherine Thomas", "born": "28 Jan 1891"},
        {"code": "1446", "name": "John Marshall Thomas", "born": "1 Feb 1893"},
        {"code": "1447", "name": "James Richard Thomas", "born": "11 Mar 1896"},
        {"code": "1448", "name": "Daisy Pearl Thomas", "born": "7 Sep 1897"},
        {"code": "1449", "name": "Charles Chester Thomas", "born": "22 Aug 1900", "died": "1 Jan 1963"},
        {"code": "144A", "name": "Alberta Thomas", "died": "in infancy", "flags": {"diedInInfancy": True}},
    ],
})

ENTRIES.append({
    "code": "145",
    "name": "David G. Guthrie",
    "sex": "M",
    "born": "30 Aug 1860",
    "died": "26 Mar 1936",
    "spouses": [{"name": "Fidella M. Miller", "born": "Jul 1884", "died": "26 Apr 1925", "married": "26 Feb 1884"}],
    "notes": "PDF lists Fidella's birth as Jul 1884 but the marriage as 26 Feb 1884; one of these is probably a typo (likely her birth is earlier, perhaps 1864 or similar).",
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 8},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1451", "name": "Irvin A. Guthrie", "born": "4 Nov 1884"},
        {"code": "1452", "name": "Violet M. Guthrie", "born": "1886"},
        {"code": "1453", "name": "Lillian A. Guthrie"},
        {"code": "1454", "name": "Nola E. Guthrie", "born": "28 Mar 1891"},
        {"code": "1455", "name": "Daisy E. Guthrie", "born": "4 Mar 1893"},
        {"code": "1456", "name": "George Cecil Guthrie", "born": "1893", "died": "18 Jul 1982"},
        {"code": "1457", "name": "Groover Guthrie", "born": "1893", "died": "8 Nov 1946"},
        {"code": "1458", "name": "David Paul Guthrie", "born": "4 Apr 1900"},
        {"code": "1459", "name": "Elfleda A. Guthrie", "born": "13 Feb 1903"},
    ],
})

ENTRIES.append({
    "code": "147",
    "name": "Albert M. Guthrie",
    "sex": "M",
    "born": "12 Jul 1864",
    "died": "8 Jan 1951",
    "spouses": [{"name": "Susan Caroline Miller", "born": "4 Dec 1856", "died": "21 Feb 1934", "married": "1886", "notes": "PDF shows '1886 or 1887' for marriage year."}],
    "residences": ["Fairchance, PA"],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 9},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1471", "name": "Ada Ora Guthrie", "born": "10 Apr 1886"},
        {"code": "1472", "name": "Hosea H. Guthrie", "born": "16 Mar 1888"},
        {"code": "1473", "name": "Sarah Vivian Guthrie", "born": "10 Feb 1890"},
        {"code": "1474", "name": "Effie Guthrie", "born": "7 Sep 1892", "died": "1895", "flags": {"diedInInfancy": True}},
        {"code": "1475", "name": "Carrie E. Guthrie", "born": "12 Sep 1895"},
        {"code": "1476", "name": "Herbert J. Guthrie", "born": "22 Aug 1898"},
    ],
})

ENTRIES.append({
    "code": "148",
    "name": "Franklin C. Guthrie",
    "sex": "M",
    "born": "6 Jul 1868",
    "died": "28 Apr 1942",
    "spouses": [{"name": "Barbara Rosanna Miller", "born": "1868", "died": "30 Jul 1923", "married": "1889"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 9},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": "PDF shows 'd. 28 Apr 28 1942' — the duplicated '28' is a typesetting artifact."},
    "children": [
        {"code": "1481", "name": "Mary Mae Guthrie", "born": "8 Sep 1891"},
        {"code": "1482", "name": "Russell R. Guthrie", "born": "23 Jun 1895"},
        {"code": "1483", "name": "Arthur H. Guthrie", "born": "15 Apr 1896", "died": "26 Feb 1923"},
        {"code": "1484", "name": "Walter Guthrie", "born": "1898"},
        {"code": "1485", "name": "Bessie E. Guthrie", "born": "Jul 1899"},
        {"code": "1486", "name": "Emma V. Guthrie", "born": "1903"},
        {"code": "1487", "name": "James E. Guthrie", "born": "1904"},
        {"code": "1488", "name": "Sarah E. Guthrie", "born": "14 Nov 1906"},
        {"code": "1489", "name": "Helen J. Guthrie", "born": "28 Oct 1908"},
        {"code": "148A", "name": "Charles H. Guthrie", "born": "1 May 1919"},
        {"code": "148B", "name": "Amy B. Guthrie", "died": "in infancy", "flags": {"diedInInfancy": True}},
        {"code": "148C", "name": "Alice Guthrie", "died": "in infancy", "flags": {"diedInInfancy": True}},
        {"code": "148D", "name": "William Guthrie", "died": "in infancy", "flags": {"diedInInfancy": True}},
    ],
})

# === More Stephen branch depth ===
ENTRIES.append({
    "code": "532",
    "name": "Samuel Spenser Guthrie",
    "sex": "M",
    "born": "1858",
    "died": "1927",
    "spouses": [{"name": "Julia D. Deahl", "born": "1860", "died": "1928", "married": "10 Apr 1884"}],
    "source": {"pdf": "Stephen_Guthrie - One Generation.pdf", "page": 2},
})

ENTRIES.append({
    "code": "536",
    "name": "Zana Estella Guthrie",
    "sex": "F",
    "born": "25 Nov 1875",
    "died": "3 Nov 1941",
    "spouses": [
        {"name": "William H. G. Strawser", "born": "1859", "married": "22 Mar 1903", "order": 1},
        {"name": "Joshua Grant Bishop", "died": "1951", "married": "16 Feb 1892", "order": 2},
    ],
    "source": {"pdf": "Stephen_Guthrie - One Generation.pdf", "page": 2},
})

# === Alexander A3 (Persis Ann)'s children — Romesburg line ===
ENTRIES.append({
    "code": "A32",
    "name": "Alexander G. Romesburg",
    "sex": "M",
    "born": "13 Aug 1868",
    "died": "22 May 1965",
    "spouses": [{"name": "Anna Blanche Raymond", "born": "1875", "died": "11 Feb 1966"}],
    "source": {"pdf": "Alexander_Guthrie - Five Generations.pdf", "page": 3},
})

ENTRIES.append({
    "code": "A35",
    "name": "S. Walter Romesburg",
    "sex": "M",
    "born": "7 Jan 1870",
    "died": "1954",
    "spouses": [{"name": "Della M. Ridenour", "born": "3 Sep 1876", "died": "22 Aug 1940"}],
    "source": {"pdf": "Alexander_Guthrie - Five Generations.pdf", "page": 3},
})

ENTRIES.append({
    "code": "A3B",
    "name": "William Franklin Romesburg",
    "sex": "M",
    "born": "19 Nov 1871",
    "died": "7 Dec 1948",
    "spouses": [{"name": "Sarah Catherine Hileman", "born": "16 Feb 1886"}],
    "source": {"pdf": "Alexander_Guthrie - Five Generations.pdf", "page": 3},
})

# === Children of John Forman Guthrie (87, Absalom line) ===
ENTRIES.append({
    "code": "873",
    "name": "Harry Grimes Guthrie",
    "sex": "M",
    "born": "8 Sep 1886",
    "spouses": [{"name": "Ester McLaughlin", "married": "18 Oct 1922"}],
    "residences": ["2583 Glen Echo Drive, Columbus, OH"],
    "source": {"pdf": "Absalom_Guthrie - One Generation.pdf", "page": 3},
})

ENTRIES.append({
    "code": "874",
    "name": "Bruce Forman Guthrie",
    "sex": "M",
    "born": "23 Sep 1890",
    "spouses": [{"name": "Elizabeth Shaws", "born": "3 Nov 1894", "married": "15 Jun 1918"}],
    "residences": ["321 Dryden Rd., Ithaca, NY"],
    "source": {"pdf": "Absalom_Guthrie - One Generation.pdf", "page": 3},
})

# === A few more James gen 3 to show depth ===
ENTRIES.append({
    "code": "713",
    "name": "James (Bub) M. Barnes",
    "sex": "M",
    "born": "9 Feb 1869",
    "died": "21 Oct 1965",
    "spouses": [{"name": "Cora Idessa Ditmore", "born": "11 Aug 1875", "died": "10 Jan 1956", "married": "20 Jan 1904"}],
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 2},
})

ENTRIES.append({
    "code": "714",
    "name": "Harrison Franklin Barnes",
    "sex": "M",
    "born": "17 Dec 1871",
    "died": "14 Jan 1946",
    "spouses": [{"name": "Virginia Jennie Moyers", "born": "8 Feb 1871", "died": "8 Feb 1953", "married": "17 Jun 1900"}],
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 2},
})

ENTRIES.append({
    "code": "763",
    "name": "Effie Guthrie",
    "sex": "F",
    "born": "25 Feb 1886",
    "died": "5 Jun 1968",
    "spouses": [{
        "name": "Harrison Rosco (Ock) Frankhouser",
        "born": "21 Jan 1883",
        "died": "2 Feb 1966",
        "married": "7 Apr 1909",
        "details": "Son of John and Amanda [Cupp] Frankhouser.",
    }],
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 4},
})


# === Joseph Guthrie's children (113x — fills out 113→1133 line and siblings) ===
ENTRIES.append({
    "code": "1131",
    "name": "Martha Ellen Guthrie",
    "sex": "F",
    "born": "22 Jul 1871",
    "died": "21 Aug 1931",
    "spouses": [{
        "name": "Rev. George W. VanSickle",
        "born": "24 Oct 1869",
        "died": "28 Apr 1942",
        "married": "7 Apr 1892",
        "details": "Son of Zachariah and Mary [Burgess] VanSickle.",
    }],
    "buried": "Shady Grove Cemetery, WV",
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 14},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "11311", "name": "Cora Ellen VanSickle", "born": "5 Aug 1893", "died": "6 Feb 1896", "flags": {"diedInInfancy": True}},
        {"code": "11312", "name": "Walter E. VanSickle", "born": "24 Jun 1895"},
        {"code": "11313", "name": "Rosa Virginia VanSickle", "born": "9 Nov 1897"},
        {"code": "11314", "name": "Asa R. VanSickle", "born": "6 Jan 1900", "died": "19 Dec 1905", "flags": {"diedInInfancy": True}},
        {"code": "11315", "name": "Quinter VanSickle", "born": "14 Aug 1902"},
        {"code": "11316", "name": "Ruby VanSickle", "born": "14 Feb 1912"},
    ],
})

ENTRIES.append({
    "code": "1132",
    "name": "Charles Allen Guthrie",
    "sex": "M",
    "born": "20 Feb 1873",
    "died": "1933",
    "spouses": [
        {"name": "Emma Spiker", "born": "22 Oct 1877", "died": "6 Aug 1905",
         "details": "Daughter of John P. and Katherine [Beeghley] Spiker. Buried at Accident, MD.", "order": 1},
        {"name": "Florence (Flossie) Spoerlein", "born": "17 Aug 1887", "died": "30 Sep 1968",
         "buried": "Shady Grove Cemetery", "order": 2},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 14},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        # First marriage
        {"code": "11321", "name": "Harry Milton Guthrie", "born": "16 Mar 1899"},
        {"code": "11322", "name": "Grace Catherine Guthrie", "born": "14 May 1903"},
        {"code": "11323", "name": "Eula Guthrie", "born": "23 May"},
        {"code": "11324", "name": "Wayne Guthrie", "born": "5 Jan"},
    ],
})

ENTRIES.append({
    "code": "1134",
    "name": "Mary Etta Guthrie",
    "sex": "F",
    "born": "16 Jul 1882",
    "died": "25 Nov 1977",
    "spouses": [{
        "name": "Arthur Oren VanSickle",
        "born": "30 Aug 1881",
        "died": "22 Apr 1956",
        "details": "Son of Elias and Emma [Robinson] VanSickle. Both buried at Shady Grove Cemetery, WV.",
    }],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 14},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "11341", "name": "Winnifred Ruth VanSickle", "born": "6 Jul 1896", "died": "Apr 1978"},
        {"code": "11342", "name": "Evelyn VanSickle"},
        {"code": "11343", "name": "David Guthrie VanSickle", "born": "16 Dec 1911"},
    ],
})

ENTRIES.append({
    "code": "1135",
    "name": "Sarah Jane Guthrie",
    "sex": "F",
    "born": "1 Jun 1885",
    "died": "15 Dec 1966",
    "spouses": [{"name": "David Warren VanSickle", "born": "7 Nov 1883", "died": "7 Aug 1939"}],
    "buried": "Shady Grove Cemetery, WV",
    "residences": ["Hazelton, WV"],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 14},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "11351", "name": "Marian Spencer VanSickle", "born": "8 Jul 1931"},
    ],
})

ENTRIES.append({
    "code": "1136",
    "name": "Frank Guthrie",
    "sex": "M",
    "born": "1 Jun 1885",
    "died": "27 Mar 1962",
    "spouses": [{
        "name": "Millie C. Knox",
        "born": "15 Apr 1887",
        "died": "1 Mar 1983",
        "married": "30 Dec 1908",
        "details": "Daughter of Joshua and Martha [Casseday] Knox. Married in Uniontown, PA.",
    }],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 15},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "11361", "name": "Helen Lucilla Guthrie", "born": "5 Aug 1909"},
        {"code": "11362", "name": "Beatrice Mae Guthrie", "born": "5 Oct 1911"},
    ],
})

# === Pages 11-15 vision pass (2026-06-07): Nicola siblings + start of gen 4 ===
ENTRIES.append({
    "code": "173",
    "name": "John Nicola",
    "sex": "M",
    "born": "11 Jun 1861",
    "died": "1 Jan 1937",
    "spouses": [{"name": "Clara Elizabeth Teets", "born": "24 Dec 1861", "died": "9 Jul 1938"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 11},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1731", "name": "Jacob George Nicola", "born": "2 Apr 1881"},
        {"code": "1732", "name": "Jeremiah Judson Nicola", "born": "11 Feb 1888"},
        {"code": "1733", "name": "Carrie May Nicola", "born": "5 Mar 1892"},
    ],
})

ENTRIES.append({
    "code": "175",
    "name": "James William Nicola",
    "sex": "M",
    "born": "24 Nov 1865",
    "died": "26 Mar 1952",
    "spouses": [{"name": "Martha Mitchell", "born": "15 Mar 1866", "died": "23 Nov 1918", "married": "4 Mar 1889"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 11},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1751", "name": "Goldie Nicola", "born": "3 Feb 1890"},
        {"code": "1752", "name": "Blanche Nicola", "born": "6 Jan 1892", "died": "18 Jul 1972"},
    ],
})

ENTRIES.append({
    "code": "176",
    "name": "Peter Martin Nicola",
    "sex": "M",
    "born": "29 Jan 1868",
    "died": "27 Dec 1955",
    "spouses": [{"name": "Helen Virginia Wilson", "born": "27 Oct 1873", "died": "15 May 1936", "married": "4 Aug 1895"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 11},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1761", "name": "Annie E. Nicola", "born": "1896", "died": "1896", "flags": {"diedInInfancy": True}},
        {"code": "1762", "name": "Edna Anna Nicola", "born": "21 Mar 1897", "died": "1973"},
    ],
})

ENTRIES.append({
    "code": "177",
    "name": "Barbara (Ella) Ellen Nicola",
    "sex": "F",
    "born": "6 Aug 1870",
    "died": "6 Aug 1957",
    "spouses": [{"name": "James Zella Frey", "born": "23 Aug 1859", "died": "10 Mar 1946", "married": "3 Jan 1889"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 12},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1771", "name": "Clyde E. Frey", "born": "27 Apr 1890", "died": "5 Sep 1914"},
        {"code": "1772", "name": "Floyd Thamer Frey", "born": "17 Feb 1892"},
        {"code": "1773", "name": "Hugh M. Frey", "born": "9 Jan 1894"},
        {"code": "1774", "name": "Charles H. Frey", "born": "18 Aug 1897", "died": "10 Jan 1946"},
        {"code": "1775", "name": "Earl Frey", "born": "27 Aug 1900"},
        {"code": "1776", "name": "William Darrel Frey", "born": "13 Jul 1903"},
        {"code": "1777", "name": "James Doyle Frey", "born": "4 May 1912"},
    ],
})

ENTRIES.append({
    "code": "178",
    "name": "Lovina Catherine Nicola",
    "sex": "F",
    "born": "6 Aug 1870",
    "died": "24 May 1957",
    "spouses": [{"name": "Samuel B. Ball", "born": "6 Aug 1869", "died": "1944", "married": "12 Jul 1890"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 12},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1781", "name": "Clarence Everett Ball", "born": "6 Jul 1891"},
        {"code": "1782", "name": "Stanley R. Ball", "born": "13 Aug 1893"},
        {"code": "1783", "name": "Herman E. Ball", "born": "29 Dec 1895"},
    ],
})

ENTRIES.append({
    "code": "179",
    "name": "Emma C. Nicola",
    "sex": "F",
    "born": "28 Mar 1875",
    "died": "19 Sep 1913",
    "spouses": [{"name": "John Carol", "born": "24 May 1851", "died": "31 Jan 1934", "married": "3 Mar 1899"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 12},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1791", "name": "Edith Grace Carol", "born": "4 Feb 1901"},
        {"code": "1792", "name": "Lawrence Carol", "born": "26 Dec 1903"},
    ],
})

ENTRIES.append({
    "code": "196",
    "name": "Ida M. Guthrie",
    "sex": "F",
    "born": "1880",
    "born_alt": "1882",
    "died": "1941",
    "spouses": [
        {"name": "Victor Berry", "order": 1},
        {"name": "Dewey (David) Berry", "order": 2},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 12},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1961", "name": "Denely Berry"},
    ],
})

# === Page 13: William Harrison Guthrie's children full entries ===
ENTRIES.append({
    "code": "1111",
    "name": "Rhuey Pearl Guthrie",
    "sex": "F",
    "born": "22 Feb 1889",
    "died": "25 Sep 1977",
    "buried": "Terra Alta, WV",
    "notes": "Rhuey and Albert (first husband) are buried in Terra Alta, WV.",
    "spouses": [
        {"name": "Albert Ross Frazee", "born": "6 Jul 1874", "died": "22 Jun 1938", "order": 1},
        {"name": "Rev. Emra Fike", "born": "26 Sep 1872", "died": "20 Mar 1956", "married": "26 May 1940", "order": 2},
        {"name": "Elmer Cline Shaffer", "born": "14 Sep 1885", "died": "7 Apr 1973", "order": 3},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 13},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "11111", "name": "Earl Glenn Frazee", "born": "12 Sep 1913", "died": "6 Jan 1960"},
        {"code": "11112", "name": "Edna Mae Frazee", "born": "6 Sep 1921"},
    ],
})

ENTRIES.append({
    "code": "1112",
    "name": "Ada Ellen Guthrie",
    "sex": "F",
    "born": "17 Feb 1887",
    "died": "16 Jan 1976",
    "spouses": [
        {"name": "Harry C. Windell", "born": "28 Sep 1884", "died": "16 Sep 1942", "order": 1},
        {"name": "Charles E. Vought", "details": "of Cransville", "order": 2},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 13},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        # First marriage
        {"code": "11121", "name": "William Carl Windell", "born": "24 Nov 1911"},
        {"code": "11122", "name": "Glenn F. Windell"},
        {"code": "11123", "name": "Paul C. Windell"},
        {"code": "11124", "name": "Beatrice Windell"},
        {"code": "11125", "name": "Bivilene Windell"},
        {"code": "11126", "name": "Faye C. Windell"},
        {"code": "11127", "name": "Eleanor Windell"},
    ],
})

ENTRIES.append({
    "code": "1113",
    "name": "Chester Earl Guthrie",
    "sex": "M",
    "born": "11 Dec 1888",
    "died": "18 Aug 1967",
    "spouses": [{"name": "Martha Fike"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 13},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "11131", "name": "Madeline Guthrie"},
        {"code": "11132", "name": "Wilda Guthrie"},
        {"code": "11133", "name": "Lorraine Guthrie"},
        {"code": "11134", "name": "Robert M. Guthrie"},
        {"code": "11135", "name": "Richard D. Guthrie"},
    ],
})

ENTRIES.append({
    "code": "1114",
    "name": "Cora Mae Guthrie",
    "sex": "F",
    "born": "13 Oct 1895",
    "died": "1 Apr 1971",
    "buried": "Terra Alta",
    "spouses": [{"name": "Leroy Bestwick"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 13},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "11141", "name": "Eleanor Bestwick"},
        {"code": "11142", "name": "Charles Bestwick"},
    ],
})

# === Page 13: Samuel Guthrie's children ===
ENTRIES.append({
    "code": "1121",
    "name": "George Walter Guthrie",
    "sex": "M",
    "born": "12 May 1870",
    "died": "before 1967",
    "spouses": [
        {"name": "Malissa Whitehair", "born": "15 Apr 1872", "died": "9 Jul 1920", "married": "22 May 1890", "order": 1},
        {"name": "Mrs. Effie Livengood Feathers", "born": "1 Jun 1879", "died": "16 Mar 1968", "married": "15 Apr 1925",
         "father": "David S. Livengood", "mother": "Virginia [Crane] Livengood", "order": 2},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 13},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "11211", "name": "Tressie Guthrie", "born": "26 Nov 1870"},
        {"code": "11212", "name": "Russell E. Guthrie", "born": "11 Jul 1898"},
    ],
})

ENTRIES.append({
    "code": "1122",
    "name": "Laura A. Guthrie",
    "sex": "F",
    "born": "Mar 1875",
    "spouses": [{"name": "Lee Roy Trembly", "born": "26 Jun 1870", "died": "20 Apr 1937",
                 "father": "John W. Trembly", "mother": "Lydia A. [Feathers] Trembly"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 13},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "11221", "name": "Bessie Gertude Trembly", "born": "21 Jun 1893"},
        {"code": "11222", "name": "Lena Ellen Trembly", "born": "29 Apr 1896"},
        {"code": "11223", "name": "Earl C. Trembly", "born": "4 Nov 1903", "died": "28 Apr 1924"},
        {"code": "11224", "name": "Regina C. Trembly", "born": "10 Feb 1914"},
    ],
})

ENTRIES.append({
    "code": "1123",
    "name": "Nancy Ellen Guthrie",
    "sex": "F",
    "born": "8 Aug 1877",
    "died": "14 Mar 1967",
    "buried": "Sugar Grove Cemetery, Piqua, OH",
    "spouses": [{"name": "John Burns", "born": "1841", "died": "3 Feb 1932", "buried": "Sugar Grove Cemetery, Piqua, OH"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 14},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "11231", "name": "Joseph Burns", "died": "19 Jan 1967"},
        {"code": "11232", "name": "Samuel Herbert Burns"},
        {"code": "11233", "name": "Robert Burns"},
        {"code": "11234", "name": "Allen Burns"},
        {"code": "11235", "name": "Mary Burns"},
        {"code": "11236", "name": "Edith Burns"},
    ],
})

ENTRIES.append({
    "code": "1124",
    "name": "Effie F. Guthrie",
    "sex": "F",
    "born": "24 Dec 1884",
    "died": "before Mar 1967",
    "spouses": [{"name": "Ira Cupp"}],
    "notes": "PDF shows 'd. before Mar 1867' but 1867 must be a typo for 1967 since she was born 1884.",
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 14},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "11241", "name": "Erma Cupp"},
        {"code": "11242", "name": "Vivian Cupp"},
        {"code": "11243", "name": "Nellie Cupp", "born": "23 Apr 1903"},
    ],
})

# === Page 15: Mary Jane's son (Walter Reed Hartman) ===
ENTRIES.append({
    "code": "1141",
    "name": "Walter Reed Hartman",
    "sex": "M",
    "born": "26 Jul 1872",
    "died": "31 Oct 1960",
    "notes": "PDF heading shows 'HARTMAM' — typesetting artifact for Hartman.",
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 15},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "11411", "name": "Wilford Hartman"},
        {"code": "11412", "name": "Carlton Hartman"},
        {"code": "11413", "name": "Cora Hartman"},
    ],
})

# === Page 15: Archibald J. DeBerry's children ===
ENTRIES.append({
    "code": "1222",
    "name": "Oliver Martin DeBerry",
    "sex": "M",
    "born": "28 Jun 1874",
    "died": "16 Nov 1947",
    "spouses": [{"name": "Anna Funk", "born": "11 Nov 1880", "died": "10 Jul 1953"}],
    "notes": "PDF says only 'Had eleven children' — children not individually listed on this page.",
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 15},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
})

ENTRIES.append({
    "code": "1223",
    "name": "Nancy Arletta DeBerry",
    "sex": "F",
    "born": "7 May 1876",
    "died": "Dec 1939",
    "spouses": [{"name": "Edward Brown"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 15},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "12231", "name": "May Brown"},
    ],
})

ENTRIES.append({
    "code": "1224",
    "name": "Charles Allen DeBerry",
    "sex": "M",
    "born": "8 Jul 1878",
    "died": "7 Oct 1954",
    "buried": "Mt. Moriah Cemetery, Valley Point, WV",
    "spouses": [{
        "name": "Cora Margaret Lambert",
        "born": "6 Sep 1885",
        "died": "6 Oct 1961",
        "married": "12 Oct 1908",
        "father": "John Allen Lambert",
        "mother": "Emma Jane [Martin] Lambert",
        "buried": "Mt. Moriah Cemetery, Valley Point, WV",
    }],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 15},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "12241", "name": "Hazel Belle DeBerry", "born": "18 May 1909"},
        {"code": "12242", "name": "Lucy Elizabeth DeBerry", "born": "3 Sep 1910"},
        {"code": "12243", "name": "William Henry DeBerry", "born": "16 Jan 1912"},
        {"code": "12244", "name": "Junior Clark DeBerry", "born": "24 Sep 1913"},
        {"code": "12245", "name": "Jessie Harold DeBerry", "born": "20 Nov 1915", "died": "22 Nov 1915", "flags": {"diedInInfancy": True}},
        {"code": "12246", "name": "Herbert Lee DeBerry", "born": "8 Oct 1916", "died": "8 Oct 1916", "flags": {"diedInInfancy": True}},
        {"code": "12247", "name": "James Oliver DeBerry", "born": "24 Aug 1917"},
        {"code": "12248", "name": "Mary Alice DeBerry", "born": "25 Nov 1919"},
        {"code": "12249", "name": "Arletta Lucille DeBerry", "born": "11 Aug 1922"},
        {"code": "1224A", "name": "Albert Ray DeBerry", "born": "8 Oct 1924", "died": "20 Nov 1968"},
        {"code": "1224B", "name": "Flory Murle Lambert", "born": "1 Jul 1903", "died": "8 Feb 1968", "flags": {"stepChild": True}},
    ],
})

ENTRIES.append({
    "code": "1226",
    "name": "Henry R. DeBerry",
    "sex": "M",
    "born": "5 Dec 1882",
    "died": "1952",
    "spouses": [{"name": "Emma"}],
    "notes": "PDF says only 'Had three children' — children not individually listed.",
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 15},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
})

ENTRIES.append({
    "code": "1227",
    "name": "Stanford Earl DeBerry",
    "sex": "M",
    "born": "11 Dec 1887",
    "died": "15 Apr 1973",
    "spouses": [
        {"name": "Louise Boyd Gabler", "born": "8 Aug 1889", "died": "25 Nov 1970", "order": 1},
        {"name": "Cristine Sheffield", "order": 2},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 15},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "12271", "name": "DeBerry child"},
    ],
})

ENTRIES.append({
    "code": "1229",
    "name": "William Vance DeBerry",
    "sex": "M",
    "born": "24 Nov 1888",
    "died": "20 Dec 1966",
    "spouses": [{"name": "Maude E. Frazee"}],
    "notes": "PDF says only 'Had four children' — children not individually listed.",
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 15},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
})

ENTRIES.append({
    "code": "1231",
    "name": "Charles Deal",
    "sex": "M",
    "born": "18 Oct 1878",
    "died": "1935",
    "spouses": [{
        "name": "Anna Thomas",
        "born": "1881",
        "died": "1945",
        "father": "Moses Thomas",
        "mother": "Diana [Silbaugh] Thomas",
        "details": "Of Smithfield, PA.",
    }],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 15},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "12311", "name": "Laura Susan Deal", "born": "28 Nov 1903"},
        {"code": "12312", "name": "Elmer Deal"},
    ],
})

# === Ward Barnes Guthrie's children (11331's kids) ===
ENTRIES.append({
    "code": "113311",
    "name": "Suzanne Kay Guthrie",
    "sex": "F",
    "born": "2 Dec 1942",
    "spouses": [{"name": "Glenn Duane Evenstad", "born": "25 May 1935", "married": "27 Dec 1967",
                 "details": "Son of Ole M. Evenstad."}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 80},
})

ENTRIES.append({
    "code": "113312",
    "name": "Samuel Fleming Guthrie",
    "sex": "M",
    "born": "14 Feb 1945",
    "spouses": [{"name": "Bonnie Jane Duncan", "born": "6 Apr 1947", "married": "7 Apr 1968"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 80},
})

ENTRIES.append({
    "code": "113313",
    "name": "Ward David Guthrie",
    "sex": "M",
    "born": "17 Mar 1946",
    "spouses": [{"name": "Carol Ann Shaw", "born": "30 Dec 1952", "married": "21 Jan 1978"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 80},
})

ENTRIES.append({
    "code": "113314",
    "name": "Stephen Byron Guthrie",
    "sex": "M",
    "born": "25 Mar 1960",
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 80},
})

# === More Lydia/Christian Nicola kids (completes the 13E*/174* SEE_REF cluster) ===
ENTRIES.append({
    "code": "13E3",
    "name": "Fredrick R. Nicola",
    "sex": "M",
    "born": "1891",
    "died": "24 Nov 1970",
    "spouses": [
        {"name": "Edna ---", "married": "1914", "order": 1},
        {"name": "Ethel ---", "born": "1903", "order": 2},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 23},
})

ENTRIES.append({
    "code": "13E7",
    "name": "Laura Bell Nicola",
    "sex": "F",
    "born": "1904",
    "spouses": [{"name": "James Rockwell", "married": "1918"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 23},
})

# === Walter Christian Guthrie's kids (13F* — the patriarch's last child's line) ===
ENTRIES.append({
    "code": "13F1",
    "name": "Lloyd Milton Guthrie",
    "sex": "M",
    "born": "24 Jul 1886",
    "died": "1 Mar 1975",
    "spouses": [{
        "name": "Pearl Savage",
        "born": "1899",
        "died": "1965",
        "details": "Daughter of Samuel and Sarah [Uphold] Savage. Both buried at Blooming Grove Cemetery.",
    }],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 20},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "13F11", "name": "Samuel Playford Guthrie"},
        {"code": "13F12", "name": "Junior Walter Guthrie", "born": "16 Jun 1922", "died": "26 Jan 1994"},
        {"code": "13F13", "name": "George D. Guthrie", "born": "1925"},
        {"code": "13F14", "name": "William Guthrie"},
        {"code": "13F15", "name": "Clarence Robert Guthrie"},
        {"code": "13F16", "name": "Mabel Guthrie"},
        {"code": "13F17", "name": "Pauline Guthrie"},
        {"code": "13F18", "name": "Sarah R. Guthrie", "born": "11 Jul 1925", "died": "11 Jul 1925", "flags": {"diedInInfancy": True}},
        {"code": "13F19", "name": "Daisy M. Guthrie", "born": "11 Jul 1925"},
    ],
})

ENTRIES.append({
    "code": "13F5",
    "name": "Matila (Mamie) Mae Guthrie",
    "sex": "F",
    "born": "9 Dec 1897",
    "spouses": [{
        "name": "Samuel Walter Ditmore",
        "born": "1895",
        "died": "14 Jul 1962",
        "married": "18 Oct 1915",
        "details": "Son of John and Melanda [Teets] Ditmore. Married at Kingwood, WV.",
    }],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 21},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "13F51", "name": "Freda Beatrice Ditmore", "born": "30 Dec 1916"},
        {"code": "13F52", "name": "Ethel Marie Ditmore", "born": "8 Jul 1919"},
        {"code": "13F53", "name": "Nellie Pauline Ditmore", "born": "1 Apr 1921", "died": "1 Jun 1939"},
        {"code": "13F54", "name": "Calvin Ray Ditmore", "born": "8 Mar 1924"},
        {"code": "13F55", "name": "Thelma May Ditmore", "born": "8 Aug 1925"},
        {"code": "13F56", "name": "Samuel Walter Ditmore, Jr.", "born": "21 Nov 1927"},
        {"code": "13F57", "name": "Beulah Dreme Ditmore", "born": "14 Dec 1929"},
        {"code": "13F58", "name": "Thomas Dale Ditmore", "born": "27 Aug 1934"},
        {"code": "13F59", "name": "Ronald Lee Ditmore", "born": "15 Nov 1936"},
        {"code": "13F5A", "name": "James Franklin Ditmore", "born": "2 Jun 1942"},
    ],
})

ENTRIES.append({
    "code": "13F7",
    "name": "James Quinter Guthrie",
    "sex": "M",
    "born": "31 Dec 1902",
    "died": "22 Jul 1980",
    "notes": "Died when lightning struck his house.",
    "spouses": [{
        "name": "Anna Florida (Braham) Reckart",
        "born": "2 Jan 1907",
        "died": "28 Mar 1983",
        "details": "Daughter of William Herbert and Margaret [Dunbar] Reckart.",
    }],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 21},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "13F71", "name": "Betty Guthrie", "born": "8 Apr 1932"},
        {"code": "13F72", "name": "Mary Jean Guthrie", "born": "29 Aug 1934"},
        {"code": "13F73", "name": "Walter Ray Guthrie", "born": "26 Feb 1937"},
        {"code": "13F74", "name": "Alice Virginia Guthrie", "born": "24 Oct 1939"},
        {"code": "13F75", "name": "Ethel Jane Guthrie", "born": "24 Sep 1941"},
        {"code": "13F76", "name": "Juanita Mae Guthrie", "born": "16 May 1944"},
        {"code": "13F77", "name": "Judy Marie Guthrie", "born": "15 Aug 1946"},
        {"code": "13F78", "name": "Albert Lee Guthrie", "born": "10 Apr 1950", "died": "8 Jul 1950", "flags": {"diedInInfancy": True}},
    ],
})

# === More Alexander branch (gen 4 — A22 line) ===
ENTRIES.append({
    "code": "A22",
    "name": "Marshal Abner Guthrie",
    "sex": "M",
    "born": "12 Jun 1871",
    "died": "25 Mar 1956",
    "spouses": [{"name": "Cora Cuppett", "born": "27 Aug 1875", "died": "29 Jan 1956", "married": "17 Mar 1898"}],
    "source": {"pdf": "Alexander_Guthrie - Five Generations.pdf", "page": 2},
})

ENTRIES.append({
    "code": "A21",
    "name": "Isabelle Rachel Guthrie",
    "sex": "F",
    "born": "16 Apr 1869",
    "died": "24 Jul 1940",
    "spouses": [{"name": "Truman Elsworth Frazee", "born": "1868", "died": "9 May 1942", "married": "19 Dec 1895"}],
    "source": {"pdf": "Alexander_Guthrie - Five Generations.pdf", "page": 2},
})

ENTRIES.append({
    "code": "A24",
    "name": "Elizabeth (Lizzie) Alice Guthrie",
    "sex": "F",
    "born": "11 Jan 1877",
    "died": "27 Jun 1943",
    "spouses": [{"name": "Chancy L. Miller", "married": "1906"}],
    "source": {"pdf": "Alexander_Guthrie - Five Generations.pdf", "page": 2},
})

ENTRIES.append({
    "code": "A211",
    "name": "Asa Ralph Frazee",
    "sex": "M",
    "born": "17 Dec 1896",
    "spouses": [{
        "name": "Grace Catherine Guthrie",
        "born": "14 May 1903",
        "married": "12 Sep 1925",
        "details": "Same as #11322 — daughter of Charles Allen Guthrie (#1132), John's branch. "
                   "Another cross-branch marriage.",
    }],
    "source": {"pdf": "Alexander_Guthrie - Five Generations.pdf", "page": 4},
})

ENTRIES.append({
    "code": "11322",
    "name": "Grace Catherine Guthrie",
    "sex": "F",
    "born": "14 May 1903",
    "spouses": [{
        "name": "Asa Ralph Frazee",
        "born": "17 Dec 1896",
        "married": "12 Sep 1925",
        "details": "Same as #A211 in Alexander's branch. Son of Truman E. and Isabelle R. [Guthrie] Frazee.",
    }],
    "notes": "Daughter of Charles Allen Guthrie (#1132). Her marriage links John's branch to Alexander's via the Frazee line.",
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 80},
})

# === Stephen branch — Amy Guthrie's son line (565) ===
ENTRIES.append({
    "code": "565",
    "name": "Kenneth Bruce Frankhouser",
    "sex": "M",
    "born": "5 Dec 1868",
    "died": "12 Oct 1941",
    "spouses": [{"name": "Sarah E. Felton", "born": "28 Mar 1865", "died": "1 Sep 1928"}],
    "source": {"pdf": "Stephen_Guthrie - One Generation.pdf", "page": 2},
})

ENTRIES.append({
    "code": "5325",
    "name": "Roy Leslie Guthrie",
    "sex": "M",
    "born": "18 Feb 1894",
    "died": "1969",
    "spouses": [{"name": "Elizabeth V. Ramsey", "born": "1895", "died": "1976"}],
    "source": {"pdf": "Stephen_Guthrie - One Generation.pdf", "page": 4},
})

# === James gen 4-5 chains ===
ENTRIES.append({
    "code": "741",
    "name": "James Guthrie",
    "sex": "M",
    "born": "2 Feb 1879",
    "died": "29 Apr 1965",
    "spouses": [{"name": "Caroline (Carrie) B. Maust", "born": "21 Jun 1889", "died": "9 May 1965", "married": "6 Mar 1908"}],
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 21},
})

ENTRIES.append({
    "code": "748",
    "name": "Troy Guthrie",
    "sex": "M",
    "born": "24 Feb 1891",
    "died": "3 Dec 1966",
    "spouses": [{"name": "Eula Esta Fike", "born": "21 May 1901", "died": "21 May 1921",
                 "details": "Daughter of Charles and Elizabeth [Cupp] Fike."}],
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 21},
})

ENTRIES.append({
    "code": "765",
    "name": "Laura Guthrie",
    "sex": "F",
    "born": "19 Apr 1889",
    "spouses": [{"name": "Oliver Clark Spiker"}],
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 4},
})

# === Lucy Ann DeBerry's children (123x) ===
ENTRIES.append({
    "code": "1233",
    "name": "Bruce Deal",
    "sex": "M",
    "born": "24 May 1881",
    "died": "25 Jul 1951",
    "born_place": "Cherry Grove",
    "spouses": [{
        "name": "Pearl Disa Rodeheaver",
        "born": "30 May 1887",
        "died": "2 Nov 1983",
        "married": "1905",
        "details": "Daughter of Cornelius and Isminnie [Sisler] Rodeheaver.",
    }],
    "buried": "Shady Grove Cemetery, WV",
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 16},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "12331", "name": "John Cornelius Deal", "born": "10 Jul 1906"},
        {"code": "12332", "name": "Edna Faye Deal", "born": "19 Dec 1907"},
        {"code": "12333", "name": "Carl Claude Deal", "born": "5 May 1910"},
        {"code": "12334", "name": "Hazel Lucy Deal", "born": "4 Nov 1912"},
        {"code": "12335", "name": "Ralph Paul Deal", "born": "3 Oct 1914"},
        {"code": "12336", "name": "Clarence Hermon Deal", "born": "29 Aug 1916", "died": "12 Dec 1916", "flags": {"diedInInfancy": True}},
        {"code": "12337", "name": "Mary Mae Deal", "born": "30 Sep 1918", "died": "13 Feb 1919", "flags": {"diedInInfancy": True}},
        {"code": "12338", "name": "Ray Glenn Deal", "born": "23 Jan 1922"},
    ],
})

ENTRIES.append({
    "code": "1235",
    "name": "Julia Deal",
    "sex": "F",
    "born": "23 Dec 1884",
    "died": "9 Jan 1961",
    "spouses": [
        {"name": "Clark (Clyde) Martin DeBerry", "born": "19 Feb 1878", "died": "3 Nov 1922",
         "married": "1907", "order": 1,
         "details": "Son of James and Louise [Fredlock] DeBerry."},
        {"name": "Andrew Elias Feather", "born": "12 Dec 1865", "died": "4 Apr 1958",
         "married": "13 Nov 1926", "order": 2,
         "details": "Son of Isaac B. and Elizabeth [Reckart] Feather."},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 16},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        # First marriage
        {"code": "12351", "name": "Dempsey Ernest DeBerry", "born": "25 Sep 1904"},
        {"code": "12352", "name": "Gilbert Preston DeBerry", "born": "13 Jun 1907"},
        {"code": "12353", "name": "Mabel Ellen DeBerry", "born": "5 Jan 1915", "died": "5 Jan 1915", "flags": {"diedInInfancy": True}},
    ],
})

ENTRIES.append({
    "code": "1236",
    "name": "Ella Delmerrl Deal",
    "sex": "F",
    "born": "13 Jan 1887",
    "died": "18 Jun 1948",
    "spouses": [{
        "name": "Winfield Scott Feather",
        "born": "9 Dec 1880",
        "died": "20 Aug 1951",
        "details": "Son of Jacob E. and Mariah Ann [Welch] Feather.",
    }],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 16},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "12361", "name": "Nellie Pauline Feather", "born": "22 Sep 1907"},
        {"code": "12362", "name": "Lena Alfreda Feather", "born": "12 Feb 1909", "died": "27 Apr 1909", "flags": {"diedInInfancy": True}},
        {"code": "12363", "name": "Virgie Loda Feather", "born": "25 Oct 1910"},
        {"code": "12364", "name": "Rosalie Francine Feather", "born": "23 Mar 1916"},
        {"code": "12365", "name": "Wilmeth Scott Feather", "born": "24 Jun 1919"},
        {"code": "12366", "name": "Fred Lynn Feather", "born": "23 Mar 1923"},
    ],
})

# === Mary Frances Guthrie (82, Absalom)'s children — Harned line ===
ENTRIES.append({
    "code": "823",
    "name": "Walter Harned",
    "sex": "M",
    "born": "13 Jul 1862",
    "died": "31 Dec 1930",
    "spouses": [{
        "name": "Mrs. H. J. Woodward, nee Hulda Tomelson",
        "born": "29 Nov 1855",
        "married": "26 Jul 1884",
    }],
    "source": {"pdf": "Absalom_Guthrie - One Generation.pdf", "page": 1},
})

ENTRIES.append({
    "code": "825",
    "name": "Jennie Harned",
    "sex": "F",
    "born": "6 Jun 1873",
    "spouses": [{"name": "Edward Alexander", "born": "12 Mar 1872", "married": "10 May 1896"}],
    "residences": ["Epping, ND"],
    "source": {"pdf": "Absalom_Guthrie - One Generation.pdf", "page": 2},
})

# === James Marshall Guthrie (84, Absalom)'s children ===
ENTRIES.append({
    "code": "84",
    "name": "James Marshall Guthrie",
    "sex": "M",
    "born": "20 May 1845",
    "died": "7 Jan 1917",
    "spouses": [{"name": "Elizabeth Jane Linton", "born": "26 Jan 1856", "married": "2 Nov 1875"}],
    "source": {"pdf": "Absalom_Guthrie - One Generation.pdf", "page": 1},
})

ENTRIES.append({
    "code": "843",
    "name": "John Clyde Guthrie",
    "sex": "M",
    "born": "11 Jun 1881",
    "spouses": [{"name": "Gertrude Simpson", "born": "31 Mar 1881", "married": "9 Jan 1913"}],
    "residences": ["Logan, OH"],
    "source": {"pdf": "Absalom_Guthrie - One Generation.pdf", "page": 3},
})

ENTRIES.append({
    "code": "845",
    "name": "Mellie Irene Guthrie",
    "sex": "F",
    "born": "14 Aug 1888",
    "spouses": [{"name": "Ernest Brown", "born": "28 May 1884", "married": "13 Oct 1906"}],
    "residences": ["155 Overwood Road, Akron, OH"],
    "source": {"pdf": "Absalom_Guthrie - One Generation.pdf", "page": 3},
})

# === Alexander gen 4 — A22's kids ===
ENTRIES.append({
    "code": "A221",
    "name": "Martha Guthrie",
    "sex": "F",
    "born": "22 May 1899",
    "spouses": [{"name": "Theodore B. Alexander", "married": "6 Jul 1922"}],
    "source": {"pdf": "Alexander_Guthrie - Five Generations.pdf", "page": 4},
})

ENTRIES.append({
    "code": "A222",
    "name": "Grace Drusilla Guthrie",
    "sex": "F",
    "born": "3 Mar 1902",
    "died": "1988",
    "spouses": [{"name": "John Franks", "married": "19 Jan 1949"}],
    "source": {"pdf": "Alexander_Guthrie - Five Generations.pdf", "page": 4},
})

ENTRIES.append({
    "code": "A225",
    "name": "Paul Johnson Guthrie",
    "sex": "M",
    "born": "1 Nov 1910",
    "died": "5 May 1977",
    "spouses": [{"name": "Mildred Catherine Sturm", "died": "1989", "married": "23 Aug 1934"}],
    "source": {"pdf": "Alexander_Guthrie - Five Generations.pdf", "page": 4},
})

# === Alexander A4 line (Louise Alida's grandkids/great-grandkids) ===
ENTRIES.append({
    "code": "A411",
    "name": "Ivan Deal Frankhouser",
    "sex": "M",
    "born": "13 Dec 1896",
    "died": "19 Dec 1953",
    "spouses": [{"name": "Madelon Junk", "born": "12 Oct 1902"}],
    "source": {"pdf": "Alexander_Guthrie - Five Generations.pdf", "page": 6},
})

ENTRIES.append({
    "code": "A412",
    "name": "Ralph W. Frankhouser",
    "sex": "M",
    "born": "22 Feb 1898",
    "died": "6 Nov 1981",
    "spouses": [{"name": "Georgia Lynn", "born": "1895"}],
    "source": {"pdf": "Alexander_Guthrie - Five Generations.pdf", "page": 6},
})

ENTRIES.append({
    "code": "A451",
    "name": "Charles Henry Cupp",
    "sex": "M",
    "born": "4 Jul 1904",
    "died": "9 May 1978",
    "spouses": [{
        "name": "Emma Elizabeth DeBerry",
        "born": "8 May 1916",
        "married": "31 Mar 1934",
        "details": "Per Alexander PDF: daughter of Oliver Martin DeBerry and Anna [Funk] DeBerry. "
                   "Earlier dataset claimed this is #12241 but the John PDF clearly shows 12241 = "
                   "Hazel Belle DeBerry (m. McNear). The Cupp-DeBerry cross-link is real but the "
                   "exact John-side code needs reverification against the Alexander PDF.",
    }],
    "buried": "Haywood, CA",
    "source": {"pdf": "Alexander_Guthrie - Five Generations.pdf", "page": 6},
})

ENTRIES.append({
    "code": "12241",
    "name": "Hazel Belle DeBerry",
    "sex": "F",
    "born": "18 May 1909",
    "died": "31 Jan 1983",
    "spouses": [{
        "name": "Marshall Grey McNear",
        "born": "18 Nov 1906",
        "married": "12 Apr 1926",
        "father": "Albert Claude McNear",
        "mother": "Matilda C. [Summers] McNear",
    }],
    "notes": "Daughter of Charles Allen DeBerry (#1224), NOT Oliver Martin (#1222). "
             "An older entry here mislabeled her as 'Emma Elizabeth DeBerry' married "
             "to Charles Henry Cupp (#A451); that mapping was wrong — corrected on "
             "2026-06-07 from PDF page 40. The A451 Cupp cross-marriage, if real, "
             "belongs to a different DeBerry code (possibly Edna Ethel #1228 or similar).",
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 40},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "122411", "name": "Glennis Hugh McNear", "born": "5 Jan 1928"},
        {"code": "122412", "name": "Betty Mary Elizabeth McNear", "born": "24 Mar 1931"},
        {"code": "122413", "name": "Melvin Grey McNear", "born": "2 May 1933"},
        {"code": "122414", "name": "Shirley Ann McNear", "born": "19 Jun 1936"},
        {"code": "122415", "name": "Judy Lee McNear", "born": "15 Dec 1943"},
        {"code": "122416", "name": "Harold Ray McNear", "born": "21 Jun 1946"},
    ],
})

# === James gen 4 — Alcinda's grandkids (71's grandkids via 715 and via 711) ===
ENTRIES.append({
    "code": "711",
    "name": "Lovina Catherine Barnes",
    "sex": "F",
    "born": "23 Mar 1863",
    "died": "12 May 1923",
    "spouses": [
        {"name": "Noah Thomas", "born": "13 Sep 1864", "died": "29 Apr 1956", "married": "3 May 1885",
         "details": "Daughter Ethel born 1886; died 1886.", "order": 1},
    ],
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 1},
})

ENTRIES.append({
    "code": "712",
    "name": "Barbara Ellen Barnes",
    "sex": "F",
    "born": "16 Jul 1866",
    "died": "25 Apr 1895",
    "spouses": [
        {"name": "Ira Thomas", "born": "24 Aug 1867", "died": "18 Mar 1958", "married": "19 Jan 1893",
         "details": "Son Ray Ernest born 19 Jan 1895; died 22 Jun 1895."},
    ],
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 1},
})


# === Stephen branch — more depth (53x sub-line) ===
ENTRIES.append({
    "code": "531",
    "name": "Mary Alice Guthrie",
    "sex": "F",
    "born": "about 1855",
    "source": {"pdf": "Stephen_Guthrie - One Generation.pdf", "page": 2},
})

ENTRIES.append({
    "code": "535",
    "name": "Caroline Bell Guthrie",
    "sex": "F",
    "born": "1871",
    "died": "1943",
    "spouses": [{"name": "John Maust"}],
    "source": {"pdf": "Stephen_Guthrie - One Generation.pdf", "page": 2},
})

ENTRIES.append({
    "code": "5322",
    "name": "Mary Alice Guthrie",
    "sex": "F",
    "born": "6 Nov 1887",
    "died": "Mar 1952",
    "spouses": [{"name": "Chester Victor Cupp", "born": "1878", "died": "1955",
                 "married": "1908"}],
    "source": {"pdf": "Stephen_Guthrie - One Generation.pdf", "page": 3},
})

ENTRIES.append({
    "code": "594",
    "name": "Stephen Dudley Guthrie",
    "sex": "M",
    "spouses": [{"name": "Lillie May Whithorn", "born": "1873", "married": "1893"}],
    "source": {"pdf": "Stephen_Guthrie - One Generation.pdf", "page": 3},
})

ENTRIES.append({
    "code": "597",
    "name": "Alva Arthur Guthrie",
    "sex": "M",
    "spouses": [{"name": "Eleen Geary"}],
    "source": {"pdf": "Stephen_Guthrie - One Generation.pdf", "page": 3},
})

# === Generation 5/6 examples — Linda Joyce Lightner / etc. ===
ENTRIES.append({
    "code": "17282",
    "name": "Thelma Pearl Guthrie",
    "sex": "F",
    "born": "5 Feb 1930",
    "spouses": [
        {"name": "Junior Lewis Lightner", "born": "27 Feb 1927", "order": 1},
        {"name": "Marion W. Penland", "born": "27 Mar 1920", "married": "30 Aug 1975", "order": 2},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 36},
})

ENTRIES.append({
    "code": "172821",
    "name": "Linda Joyce Lightner",
    "sex": "F",
    "born": "9 May 1947",
    "spouses": [
        {"name": "James W. Pickett", "details": "Son of Lewis Pickett of Morgantown.", "order": 1},
        {"name": "Robert James", "married": "16 Sep 1985", "order": 2},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 41},
})

# === Alexander branch — A45 sub-line (Cupp family) ===
ENTRIES.append({
    "code": "A452",
    "name": "Ivan Daniel Cupp",
    "sex": "M",
    "born": "7 Jan 1906",
    "died": "29 Jul 1995",
    "spouses": [
        {"name": "Helen Tabon", "order": 1},
        {"name": "Annariah Blake", "born": "2 Aug 1906", "died": "19 Jan 1990", "order": 2},
    ],
    "source": {"pdf": "Alexander_Guthrie - Five Generations.pdf", "page": 4},
})

ENTRIES.append({
    "code": "A454",
    "name": "Mary Virginia Cupp",
    "sex": "F",
    "born": "1 Oct 1912",
    "spouses": [
        {"name": "Clyde (Jim) Summers", "born": "19 May 1893", "died": "8 Nov 1960",
         "married": "26 Nov 1943", "order": 1},
        {"name": "Glenn Webster Barnes", "born": "24 Dec 1906", "died": "4 Mar 1983",
         "married": "5 Feb 1970", "order": 2,
         "details": "Same as #7144 in James's branch. Cross-link Alexander↔James."},
    ],
    "source": {"pdf": "Alexander_Guthrie - Five Generations.pdf", "page": 4},
})

ENTRIES.append({
    "code": "7144",
    "name": "Glenn Webster Barnes",
    "sex": "M",
    "born": "24 Dec 1906",
    "died": "4 Mar 1983",
    "spouses": [
        {"name": "Helen Younkin", "born": "27 Feb 1907", "died": "6 Feb 1969",
         "married": "18 Jun 1930", "order": 1},
        {"name": "Mary Cupp Summers", "born": "1 Oct 1912", "married": "5 Feb 1970",
         "order": 2,
         "details": "Same as #A454 in Alexander's branch. Daughter of Melvin R. and Alice Pearl [Frankhouser] Cupp."},
    ],
    "notes": "His second marriage links James↔Alexander.",
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 2},
})


# === Pages 16-20 vision pass (2026-06-07): gen 4 detail ===
ENTRIES.append({
    "code": "1232",
    "name": "Grace Deal",
    "sex": "F",
    "spouses": [{"name": "Martin Hoffman"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 16},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "12321", "name": "Ross Hoffman"},
        {"code": "12322", "name": "Henrietta Hoffman"},
        {"code": "12323", "name": "Lucy Hoffman"},
    ],
})

ENTRIES.append({
    "code": "1234",
    "name": "Daisy Deal",
    "sex": "F",
    "born": "26 Jan 1883",
    "died": "13 Jul 1936",
    "spouses": [{
        "name": "John Charles Trembly",
        "born": "5 Sep 1882",
        "died": "16 Aug 1981",
        "married": "26 Jan 1907",
        "father": "Joseph Harrison Trembly",
        "mother": "Sarah Catherine [Whetsell] Trembly",
    }],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 16},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "12341", "name": "Gertrude Trembly", "born": "12 Feb 1908"},
        {"code": "12342", "name": "Lillian Beatrice Trembly", "born": "29 Mar 1912"},
        {"code": "12343", "name": "Lucille Trembly", "born": "3 Feb 1916", "died": "22 Apr 1992"},
    ],
})

ENTRIES.append({
    "code": "1237",
    "name": "Ina Deal",
    "sex": "F",
    "born": "26 Jan 1889",
    "died": "11 Jul 1944",
    "spouses": [{
        "name": "John Foman Miller",
        "born": "20 Jun 1883",
        "died": "17 Nov 1981",
        "father": "Solomon S. Miller",
        "mother": "Hester [Forman] Miller",
    }],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 16},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "12371", "name": "Kermit Walton Miller", "born": "23 Aug 1911"},
        {"code": "12372", "name": "Ruby Fern Miller", "born": "5 Jul 1913"},
        {"code": "12373", "name": "Emerson Scott Miller", "born": "11 Jun 1918"},
    ],
})

ENTRIES.append({
    "code": "1238",
    "name": "Rhoda Deal",
    "sex": "F",
    "born": "2 May 1892",
    "died": "3 Aug 1964",
    "spouses": [{
        "name": "Charles Lloyd Liston",
        "born": "5 Mar 1894",
        "died": "2 Sep 1977",
        "father": "Frank Liston",
        "mother": "Ida [Smith] Liston",
    }],
    "notes": "PDF source shows 'Ronda' but spelling is Rhoda elsewhere.",
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 17},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "12381", "name": "Evelyn Fern Liston", "born": "6 Sep 1918"},
        {"code": "12382", "name": "Ralph Waldo Liston", "born": "6 Dec 1920"},
        {"code": "12383", "name": "Charles J. Liston", "born": "3 Jun 1935", "died": "2 Jan 1962"},
        {"code": "12384", "name": "Mrs. Willard Teets", "flags": {"stepChild": True}},
    ],
})

ENTRIES.append({
    "code": "1241",
    "name": "Virgie May Moyers",
    "sex": "F",
    "born": "8 Nov 1895",
    "died": "27 Apr 1974",
    "buried": "Shady Grove Cemetery, WV",
    "spouses": [{
        "name": "Chester Messenger",
        "born": "17 Aug 1892",
        "died": "1 Feb 1980",
        "married": "27 Jun 1915",
        "father": "George Wesley Messenger",
        "mother": "Johanna Belle [Garner] Messenger",
        "buried": "Shady Grove Cemetery, WV",
    }],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 17},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "12411", "name": "Elmer Woodrow Messenger", "born": "8 Mar 1916", "died": "1955"},
        {"code": "12412", "name": "Blaine Messenger"},
        {"code": "12413", "name": "Claude Messenger"},
    ],
})

ENTRIES.append({
    "code": "1321",
    "name": "Herbert Holland Guthrie",
    "sex": "M",
    "born": "20 Feb 1870",
    "born_alt": "10 Nov 1869",
    "buried": "Parnell Cemetery",
    "notes": "PDF: 'd. between 04 Dec 1945 and 25 Mar 1946; found near Lake Lynn PA'. County record gives birth as 10 Nov 1869.",
    "spouses": [
        {"name": "Edith Sisler", "married": "1903", "order": 1},
        {"name": "Sadie Ellen Reckart", "born": "2 Aug 1901", "died": "21 Nov 1976", "father": "Clair Reckart", "order": 2},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 17},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        # First marriage
        {"code": "13211", "name": "Rena Guthrie"},
        # Second marriage
        {"code": "13212", "name": "Elwood Herbert Guthrie", "born": "8 Sep 1916"},
        {"code": "13213", "name": "Charles Ellis Guthrie", "born": "28 Feb 19"},
        {"code": "13214", "name": "Stanley Vernon Guthrie", "born": "11 Sep 1920"},
        {"code": "13215", "name": "Rose Guthrie", "born": "18 Jun 1927"},
        {"code": "13216", "name": "Ralph Harold Guthrie", "born": "4 Jan 1933"},
        {"code": "13217", "name": "Virginia Ruth Guthrie", "born": "6 Oct 1939"},
        {"code": "13218", "name": "Connie Ellen Guthrie"},
    ],
})

ENTRIES.append({
    "code": "1322",
    "name": "Charles Dotson Guthrie",
    "sex": "M",
    "born": "2 Mar 1872",
    "died": "8 Dec 1959",
    "buried": "Parnell Cemetery",
    "spouses": [{
        "name": "Mary Elizabeth Reckart",
        "born": "28 Aug 1879",
        "died": "11 Jan 1961",
        "father": "John Adam Reckart",
        "mother": "Amanda DeBerry Reckart",
        "buried": "Parnell Cemetery",
    }],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 17},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "13221", "name": "Ada C. Guthrie", "born": "25 Dec 1895", "died": "10 Oct 1898", "flags": {"diedInInfancy": True}},
        {"code": "13222", "name": "Donna Mae Guthrie", "born": "6 Aug 1897"},
        {"code": "13223", "name": "Charles Ray Guthrie", "born": "16 Feb 1902"},
        {"code": "13224", "name": "Edna Pauline Guthrie", "born": "30 Jun 1914"},
    ],
})

ENTRIES.append({
    "code": "1324",
    "name": "V. O. Della Guthrie",
    "sex": "F",
    "born": "17 Sep 1876",
    "spouses": [{
        "name": "Jay Smith Trembly",
        "born": "30 Jul 1871",
        "married": "9 Mar 1891",
        "father": "George Hartman Trembly",
        "mother": "Eva Charity [Smith] Trembly",
    }],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 17},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "13241", "name": "Nora May Trembly", "born": "18 May 1892"},
        {"code": "13242", "name": "Flora May Trembly", "born": "14 Feb 1894"},
        {"code": "13243", "name": "Nellie Clove Trembly", "born": "14 Feb 1895"},
        {"code": "13244", "name": "Chester Paul Trembly", "born": "13 Jun 1900", "died": "7 Jan 1976"},
        {"code": "13245", "name": "Martin Trembly", "born": "23 Feb 1902"},
        {"code": "13246", "name": "Maude Trembly", "born": "23 Feb 1903"},
    ],
})

ENTRIES.append({
    "code": "1325",
    "name": "Maude May Guthrie",
    "sex": "F",
    "born": "23 Dec 1879",
    "died": "15 Nov 1967",
    "buried": "Sisler Cemetery",
    "spouses": [{
        "name": "Jacob Grant Wilhelm",
        "born": "2 Jan 1870",
        "died": "22 Dec 1942",
        "married": "18 Apr 1897",
        "father": "John Wilhelm",
        "buried": "Sisler Cemetery",
        "details": "Farmer who lived near the Mt Dale church.",
    }],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 17},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "13251", "name": "Ethel Marie Wilhelm", "born": "25 Aug 1907", "died": "1 Mar 1970"},
    ],
})

ENTRIES.append({
    "code": "1326",
    "name": "Rena Clyde Guthrie",
    "sex": "F",
    "born": "10 Oct 1884",
    "died": "28 Jun 1978",
    "buried": "Parnell Cemetery",
    "spouses": [{
        "name": "Robert (Bob) E. Lawson",
        "born": "14 Feb 1882",
        "died": "1 Jan 1970",
        "married": "1 Jan 1903",
        "father": "William Lawson",
        "mother": "Emma [Jones] Lawson",
        "buried": "Parnell Cemetery",
        "details": "Lived near the Mt Dale Church.",
    }],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 18},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "13261", "name": "Chester Dotson Lawson", "born": "29 Sep 1903"},
        {"code": "13262", "name": "Ralph H. Lawson", "born": "23 Jan 1906"},
        {"code": "13263", "name": "Emma Evelyn Lawson", "born": "13 Dec 1907"},
        {"code": "13264", "name": "Everett Paul Larson", "born": "17 Jul 1911"},
        {"code": "13265", "name": "Russell Ray Lawson", "born": "23 Mar 1914"},
        {"code": "13266", "name": "Robert G. Lawson", "born": "13 Mar 1916", "died": "1969"},
        {"code": "13267", "name": "Clarence S. Lawson", "born": "22 Mar 1920"},
        {"code": "13268", "name": "Sheldon Lawson", "born": "30 Jun 1922", "died": "1969"},
    ],
})

ENTRIES.append({
    "code": "1354",
    "name": "Clyde D. Lewis",
    "sex": "M",
    "born": "14 Jun 1890",
    "died": "17 Oct 1970",
    "buried": "Shady Grove Cemetery, WV",
    "spouses": [{
        "name": "Mary Jane Savage",
        "born": "10 Sep 1889",
        "died": "23 Mar 1977",
        "married": "26 Sep 1914",
        "father": "Preston Savage",
        "mother": "Cindy [Fear] Savage",
        "buried": "Shady Grove Cemetery, WV",
    }],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 18},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "13541", "name": "Osa Freda Lewis", "born": "19 Nov 1915"},
        {"code": "13542", "name": "Herbert Ray Lewis", "born": "16 Apr 1917"},
    ],
})

ENTRIES.append({
    "code": "1365",
    "name": "Maud Turney",
    "sex": "F",
    "spouses": [{
        "name": "Marshall Walter Hauger",
        "father": "William Joseph Hauger",
        "mother": "Terace L. [Welch] Hauger",
        "details": "Lived on the farm at Lenox now owned Ralph Livengood. PDF: 'Hauger [Haugher]'.",
    }],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 18},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "13651", "name": "Dessie Alice Hauger", "born": "5 May 1898"},
        {"code": "13652", "name": "Dora Hauger"},
        {"code": "13653", "name": "Edna Hauger"},
        {"code": "13654", "name": "Cora Hauger", "born": "3 Nov 1899"},
        {"code": "13655", "name": "Daughter", "died": "1923", "flags": {"diedInInfancy": True}},
        {"code": "13656", "name": "Pauline Hauger"},
        {"code": "13657", "name": "Lois Hauger"},
        {"code": "13658", "name": "Lulu Hauger"},
        {"code": "13659", "name": "Herbert Hauger"},
        {"code": "1365A", "name": "Grace Hauger"},
    ],
})

ENTRIES.append({
    "code": "1366",
    "name": "Pearl A. Turney",
    "sex": "F",
    "born": "10 Mar 1884",
    "died": "27 Sep 1959",
    "buried": "Shady Grove Cemetery, WV",
    "spouses": [
        {"name": "Joseph Ficky", "died": "1908", "married": "1906", "order": 1},
        {"name": "Daniel DeBerry", "born": "28 Aug 1860", "died": "8 May 1945", "married": "1909", "order": 2},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 18},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        # First marriage
        {"code": "13661", "name": "Ethel Ficky"},
        # Second marriage
        {"code": "13662", "name": "Dorthy Rolls DeBerry"},
    ],
})

ENTRIES.append({
    "code": "1381",
    "name": "John Teets",
    "sex": "M",
    "died": "at age 37",
    "spouses": [{"name": "Lillie B. Friend"}],
    "occupation": "Engineer",
    "notes": "Died in his sleep of a heart attack at Rowlesburg.",
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 18},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "13811", "name": "John L. Teets"},
        {"code": "13812", "name": "Fred Teets"},
        {"code": "13813", "name": "Claude Teets"},
    ],
})

ENTRIES.append({
    "code": "1382",
    "name": "Albert E. Teets",
    "sex": "M",
    "born": "24 Jan 1875",
    "died": "25 Apr 1959",
    "buried": "Parnell Cemetery",
    "spouses": [{
        "name": "Mary Virginia (Mollie) Rodeheaver",
        "born": "26 Sep 1876",
        "died": "12 Aug 1946",
        "father": "Rufus Rodeheaver",
        "mother": "Sabra Jane [Feather] Rodeheaver",
        "buried": "Parnell Cemetery",
    }],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 19},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "13821", "name": "Edith M. Teets", "born": "19 Jan 1898"},
        {"code": "13822", "name": "Charles R. Teets", "born": "1899", "died": "1916"},
        {"code": "13823", "name": "Cora Teets", "born": "1902"},
        {"code": "13824", "name": "Harvey Teets", "born": "Aug 1904", "died": "27 Jan 1975"},
        {"code": "13825", "name": "Marie Teets", "born": "11 Apr 1911", "died": "12 Jan 1978"},
        {"code": "13826", "name": "Rosalee Teets", "born": "Sep 1917"},
        {"code": "13827", "name": "Rollin Adair Teets", "born": "26 Mar 1919"},
    ],
})

ENTRIES.append({
    "code": "1383",
    "name": "Effie M. Teets",
    "sex": "F",
    "born": "1876",
    "died": "1958",
    "buried": "Blooming Rose Cemetery",
    "spouses": [{"name": "John Uphold", "born": "1871", "died": "1951", "buried": "Blooming Rose Cemetery"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 19},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "13831", "name": "Elizah Alen Uphold", "born": "1 May 1897", "died": "7 May 1958"},
        {"code": "13832", "name": "Adam E. Uphold", "died": "31 May 1980"},
        {"code": "13833", "name": "Gertrude Uphold"},
        {"code": "13834", "name": "Jene Uphold"},
        {"code": "13835", "name": "Delia Uphold"},
        {"code": "13836", "name": "Sam Uphold"},
        {"code": "13837", "name": "Orval Uphold"},
        {"code": "13838", "name": "Theodore Uphold"},
    ],
})

ENTRIES.append({
    "code": "1384",
    "name": "William Mack Teets",
    "sex": "M",
    "born": "9 Apr 1879",
    "died": "25 Feb 1959",
    "buried": "Sisler Cemetery near Mt. Dale, WV",
    "spouses": [{
        "name": "Ada Elizabeth Casteel",
        "born": "16 Oct 1883",
        "died": "3 Jun 1938",
        "married": "19 Jun 1903",
        "father": "Thomas Casteel",
        "mother": "Susan Casteel",
        "buried": "Sisler Cemetery near Mt. Dale, WV",
    }],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 19},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "13841", "name": "Theadore Teets"},
        {"code": "13842", "name": "Arthur Paul Teet", "born": "7 Dec 1920"},
        {"code": "13843", "name": "Maude Teets"},
        {"code": "13844", "name": "Florence F. (Flora) Teets", "born": "31 Dec 1909"},
        {"code": "13845", "name": "Esta Teets"},
    ],
})

ENTRIES.append({
    "code": "1385",
    "name": "Minnie Teets",
    "sex": "F",
    "spouses": [{"name": "Shroyer"}],
    "notes": "PDF says only 'Had four children' — children not individually listed.",
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 19},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
})

ENTRIES.append({
    "code": "1386",
    "name": "Blanch Bertha Teets",
    "sex": "F",
    "born": "3 Aug 1885",
    "died": "1 Dec 1966",
    "buried": "Blooming Rose Cemetery",
    "spouses": [{
        "name": "Peter Lucian Uphold",
        "born": "1 Apr 1878",
        "died": "18 May 1945",
        "married": "16 Jul 1899",
        "father": "Frank Uphold",
        "mother": "Mollie Uphold",
        "buried": "Blooming Rose Cemetery",
    }],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 19},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "13861", "name": "Robert Uphold"},
        {"code": "13862", "name": "Cora Uphold", "born": "1 Jan 1904"},
        {"code": "13863", "name": "Bessie Uphold"},
        {"code": "13864", "name": "Edna Uphold", "born": "1906"},
        {"code": "13865", "name": "Grace Uphold"},
        {"code": "13866", "name": "Icie Myrtle Uphold"},
        {"code": "13867", "name": "Russel Uphold"},
        {"code": "13868", "name": "Troy Uphold"},
        {"code": "13869", "name": "Gladys Uphold"},
        {"code": "1386A", "name": "Infant", "buried": "Keeler Glade Cemetery", "flags": {"diedInInfancy": True}},
        {"code": "1386B", "name": "Infant", "buried": "Keeler Glade Cemetery", "flags": {"diedInInfancy": True}},
        {"code": "1386C", "name": "Infant", "buried": "Keeler Glade Cemetery", "flags": {"diedInInfancy": True}},
    ],
})

ENTRIES.append({
    "code": "13B2",
    "name": "Lily May Sikes",
    "sex": "F",
    "born": "19 Aug 1883",
    "died": "Jan 1970",
    "spouses": [
        {"name": "Edward Lee Murphy", "died": "28 Jan 1970", "order": 1},
        {"name": "Ralph Bee", "born": "7 Jun 1886", "died": "4 Jan 1968", "married": "1911", "order": 2},
    ],
    "notes": "PDF heading shows 'SIKES' but children take both 'Sikes' and 'Bee' / 'Murphy' surnames per marriage. Family name appears to be Skiles.",
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 20},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        # First marriage
        {"code": "13B21", "name": "Lola Violet Murphy", "born": "21 Feb 1905"},
        {"code": "13B22", "name": "Marie Edna Sikes", "born": "23 Mar 1907"},
        # Second marriage
        {"code": "13B23", "name": "Hazel Pearl Bee", "born": "12 Sep 1912"},
        {"code": "13B24", "name": "Verna Jane Bee", "born": "9 Aug 1915", "died": "1952"},
        {"code": "13B25", "name": "Ester Mae Bee", "born": "24 Jul 1917"},
        {"code": "13B26", "name": "Mary Catherine Bee", "born": "9 Jun 1922"},
        {"code": "13B27", "name": "Charles Paul Bee", "born": "4 Mar 1930"},
    ],
})

ENTRIES.append({
    "code": "13C2",
    "name": "Worley Guthrie",
    "sex": "M",
    "died": "6 May 1949",
    "spouses": [{"name": "Leona Markley", "order": 2, "details": "His 2nd marriage. Lived at the Pa line."}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 20},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "13C21", "name": "William R. Guthrie", "born": "25 May 1939"},
    ],
})

ENTRIES.append({
    "code": "13C3",
    "name": "Alvin Guthrie",
    "sex": "M",
    "died": "30 Apr 1940",
    "spouses": [{"name": "Wilma Thomas"}],
    "notes": "PDF says only 'Had four children'.",
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 20},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
})

ENTRIES.append({
    "code": "13C5",
    "name": "Rena K. Guthrie",
    "sex": "F",
    "born": "26 Mar 1898",
    "died": "7 Apr 1972",
    "spouses": [{"name": "Benjamin Frank Smith", "born": "1885", "died": "4 Nov 1960"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 20},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "13C51", "name": "Ray Smith", "born": "10 Jun 1918"},
        {"code": "13C52", "name": "Ocelea Elizabeth Smith", "born": "1 May 1926", "died": "4 May 1926", "flags": {"diedInInfancy": True}},
        {"code": "13C53", "name": "Janice Smith", "born": "30 Jul 1939"},
    ],
})

ENTRIES.append({
    "code": "13C9",
    "name": "Arlie Guthrie, Jr.",
    "sex": "M",
    "born": "5 May 1908",
    "died": "2 Dec 1965",
    "buried": "Thomas Cemetery, Markleysburg, PA",
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 20},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "13C91", "name": "Emma Jean Guthrie"},
        {"code": "13C92", "name": "J. R. Guthrie", "died": "13 Jan 1993"},
        {"code": "13C93", "name": "Harvey (Harry) Guthrie"},
    ],
})

ENTRIES.append({
    "code": "13D2",
    "name": "Myrtle Myers",
    "sex": "F",
    "spouses": [{"name": "Leech", "notes": "PDF gives only surname."}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 20},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "13D21", "name": "Victor Leech"},
    ],
})


# === Pages 21-25 vision pass (2026-06-07): 13F gen 4 + 14x gen 4 + 14xx gen 5 ===
ENTRIES.append({
    "code": "13F8",
    "name": "George Robert Guthrie",
    "sex": "M",
    "born": "12 Feb 1903",
    "died": "7 Aug 1963",
    "spouses": [{"name": "Faye Darlene Purtee", "born": "12 Mar 1926", "married": "7 Jul 1943"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 21},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "13F81", "name": "Macie Mae Guthrie", "born": "28 Aug 1944"},
        {"code": "13F82", "name": "Ezra Grant Guthrie", "born": "19 Dec 1945"},
        {"code": "13F83", "name": "Helen Marie Guthrie", "born": "6 Oct 1947"},
        {"code": "13F84", "name": "Walter Herbert Guthrie", "born": "8 Mar 1950"},
        {"code": "13F85", "name": "Catherine Ruth Guthrie", "born": "30 Jul 1951"},
        {"code": "13F86", "name": "Samuel Franklin Guthrie", "born": "21 Aug 1953"},
        {"code": "13F87", "name": "Dorothy Elaine Guthrie", "born": "16 Apr 1956"},
        {"code": "13F88", "name": "George Daniel Guthrie", "born": "24 Mar 1958"},
        {"code": "13F89", "name": "Cora Rose Guthrie", "born": "7 May 1960"},
        {"code": "13F8A", "name": "Mary Maude Guthrie", "born": "21 Feb 1962"},
        {"code": "13F8B", "name": "Glenn Wesley Guthrie", "born": "21 Feb 1962", "died": "21 Feb 1962", "flags": {"diedInInfancy": True}},
    ],
})

ENTRIES.append({
    "code": "13FA",
    "name": "Mary Elizabeth Guthrie",
    "sex": "F",
    "born": "18 Mar 1907",
    "died": "18 Jul 1978",
    "spouses": [{"name": "Paul Conaway", "father": "Obe Conaway"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 21},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "13FA1", "name": "Ralph Conaway"},
        {"code": "13FA2", "name": "Freda Conaway"},
        {"code": "13FA3", "name": "Lula Conaway"},
    ],
})

ENTRIES.append({
    "code": "13FB",
    "name": "Dessie Myrtle Guthrie",
    "sex": "F",
    "born": "1 Jul 1909",
    "died": "7 Jul 1987",
    "spouses": [{
        "name": "Aubrey Fred Dennis",
        "born": "2 Jan 1913",
        "died": "26 Oct 1964",
        "father": "Jessie Dennis",
        "mother": "Roxy [Thomas] Dennis",
        "buried": "Shade Grove Cemetery, WV",
    }],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 21},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "13FB1", "name": "Barbara Dennis", "flags": {"adopted": True}},
    ],
})

ENTRIES.append({
    "code": "13FC",
    "name": "Susan (Susie) Murhl Guthrie",
    "sex": "F",
    "born": "26 May 1911",
    "died": "20 Mar 1972",
    "spouses": [{"name": "Lloyd Tom Loudermilk", "born": "30 May 1906", "died": "10 Jun 1977"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 22},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "13FC1", "name": "William (Billy) Casteel", "details": "son of Dale Casteel"},
    ],
})

ENTRIES.append({
    "code": "13FD",
    "name": "John Ray Guthrie",
    "sex": "M",
    "born": "1 Oct 1914",
    "died": "11 Mar 1987",
    "spouses": [
        {"name": "Edna Ellen (Sisler) Casteel", "born": "23 Aug 1914", "died": "21 Feb 1948",
         "father": "Walter Sisler", "mother": "Clara [Reckart] Sisler", "order": 1,
         "details": "Widow of Orval (Jerry) Casteel. Edna had 10 children to die at birth; the last child lived and Edna died."},
        {"name": "Nellie (Sisler) Casteel", "father": "Martin Sisler", "order": 2,
         "details": "Widow of George Casteel."},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 22},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        # First marriage
        {"code": "13FD1", "name": "Daughter", "details": "raised by John's sister Frances Frazee"},
        # Second marriage
        {"code": "13FD2", "name": "Shirley Guthrie"},
        {"code": "13FD3", "name": "Janey I. Guthrie", "born": "14 Sep 1952", "died": "19 Apr 1953", "flags": {"diedInInfancy": True}, "buried": "Parnell cemetery"},
        {"code": "13FD4", "name": "Donald (Buddy) Guthrie", "born": "about 1953"},
        {"code": "13FD5", "name": "Lucy Guthrie"},
        {"code": "13FD6", "name": "Billy Wade Guthrie", "born": "11 Oct 1957", "died": "21 Dec 1977"},
    ],
})

ENTRIES.append({
    "code": "13FE",
    "name": "Nellie Virginia Guthrie",
    "sex": "F",
    "born": "20 Mar 1917",
    "died": "19 Dec 1992",
    "spouses": [{
        "name": "Earl Richard Noss Sr.",
        "born": "25 Apr 1901",
        "died": "1 Dec 1973",
        "father": "Charles Noss",
        "mother": "Wilhelmina [Wahl] Noss",
        "details": "Earl was a farmer and a sawyer; they lived near Shady Grove Cemetery, WV.",
    }],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 22},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "13FE1", "name": "Earl Richard Noss Jr.", "born": "16 Oct 1933"},
        {"code": "13FE2", "name": "Noami Virginia Noss", "born": "19 Sep 1935"},
        {"code": "13FE3", "name": "John Frederick Noss", "born": "20 Apr 1939"},
        {"code": "13FE4", "name": "Wayne E. Noss"},
        {"code": "13FE5", "name": "James T. Noss", "born": "29 Jun 1945", "died": "3 Jul 1966"},
        {"code": "13FE6", "name": "Shirley Noss"},
        {"code": "13FE7", "name": "Robert E. Noss"},
    ],
})

ENTRIES.append({
    "code": "1412",
    "name": "John Jacob Uphold",
    "sex": "M",
    "born": "23 Mar 1877",
    "died": "9 Jun 1953",
    "spouses": [{
        "name": "Minnie S. Burd",
        "born": "24 May 1893",
        "died": "9 Nov 1947",
        "father": "W. Frank Burd",
        "mother": "Virginia B. Burd",
        "buried": "Mt. Grove Cemetery",
    }],
    "buried": "Mt. Grove Cemetery",
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 22},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "14121", "name": "Franklin Uphold", "born": "11 Dec 1911"},
        {"code": "14122", "name": "Mary Virginia Uphold", "born": "30 Jul 1914", "died": "18 Oct 1914", "flags": {"diedInInfancy": True}},
        {"code": "14123", "name": "Charles M. Uphold", "born": "1925", "died": "8 Jul 1946"},
        {"code": "14124", "name": "William Uphold", "died": "1948"},
    ],
})

ENTRIES.append({
    "code": "1415",
    "name": "Charles Ray Uphold",
    "sex": "M",
    "born": "19 Nov 1885",
    "died": "2 Jun 1968",
    "buried": "Lafayette Memorial Park, Brier Hill, PA",
    "spouses": [{
        "name": "Nellie Faye Ryan",
        "born": "12 Feb 1887",
        "died": "4 Feb 1974",
        "married": "25 Mar 1908",
        "father": "Thomas Ryan",
        "mother": "Adelia [King] Ryan",
        "buried": "Lafayette Memorial Park, Brier Hill, PA",
    }],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 22},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "14151", "name": "Beryl Uphold", "born": "15 Nov 1908"},
        {"code": "14152", "name": "Helen Clarice Uphold", "born": "24 May 1910"},
        {"code": "14153", "name": "Donald Dale Uphold", "born": "27 Jul 1913"},
        {"code": "14154", "name": "Dorothy E. Uphold", "born": "7 Oct 1915"},
        {"code": "14155", "name": "Charles Ray Uphold", "born": "3 Jul 1923"},
    ],
})

ENTRIES.append({
    "code": "1416",
    "name": "David Franklin Uphold",
    "sex": "M",
    "born": "8 Oct 1887",
    "died": "7 Sep 1964",
    "spouses": [{"name": "Edna Smith"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 22},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "14161", "name": "Agnes Winnofred Uphold", "born": "17 Feb 1917"},
    ],
})

ENTRIES.append({
    "code": "1418",
    "name": "Ella May Uphold",
    "sex": "F",
    "born": "2 Jul 1892",
    "died": "8 May 1966",
    "spouses": [{"name": "Chancy Turner", "born": "8 Jul 1980"}],
    "notes": "PDF shows Chancy Turner born '8 Jul 1980' which is impossible — likely an OCR or typesetting error for an earlier year.",
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 23},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "14181", "name": "Elizabeth Matilda Turner", "born": "19 Aug 1912"},
        {"code": "14182", "name": "Wendell Floyd Turner", "born": "18 Oct 1918"},
        {"code": "14183", "name": "Sarapto Marie Turner", "born": "8 Apr 1919"},
        {"code": "14184", "name": "Daisy Winona Turner", "born": "30 Nov 1922"},
        {"code": "14185", "name": "Earl Donald Turner", "born": "4 May 1927"},
        {"code": "14186", "name": "Kenneth George Turner", "born": "30 Jul 1929"},
    ],
})

ENTRIES.append({
    "code": "141A",
    "name": "Basel M. Uphold",
    "sex": "M",
    "spouses": [{"name": "Annie Bracky"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 23},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "141A1", "name": "John Uphold"},
        {"code": "141A2", "name": "Charley Uphold"},
        {"code": "141A3", "name": "Basel Uphold, Jr."},
        {"code": "141A4", "name": "Walter Uphold"},
    ],
})

ENTRIES.append({
    "code": "1425",
    "name": "George Franklin Guthrie",
    "sex": "M",
    "born": "5 Mar 1890",
    "died": "30 Sep 1971",
    "buried": "Shady Grove Cemetery, WV",
    "spouses": [{
        "name": "Lulu Myrrah Thomas",
        "born": "21 Jan 1891",
        "died": "8 Nov 1971",
        "married": "1910",
        "father": "Daniel Thomas",
        "mother": "Anna [Baugh] Thomas",
        "buried": "Shady Grove Cemetery, WV",
    }],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 23},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "14251", "name": "Charles B. Guthrie", "born": "10 Nov 1910", "died": "3 Dec 1910", "flags": {"diedInInfancy": True}},
        {"code": "14252", "name": "Edna Grace Guthrie", "born": "23 Apr 1912"},
        {"code": "14253", "name": "John Edward Guthrie", "born": "2 Jan 1914", "died": "5 Aug 1957"},
        {"code": "14254", "name": "Scott Franklin Guthrie", "born": "7 Mar 1917", "died": "11 Feb 1948"},
        {"code": "14255", "name": "Blaine Austin Guthrie", "born": "24 Dec 1927", "died": "9 Nov 1942"},
        {"code": "14256", "name": "Nellie Mae Guthrie", "born": "8 Jan 1935", "died": "8 Jan 1935", "flags": {"diedInInfancy": True}},
    ],
})

ENTRIES.append({
    "code": "1427",
    "name": "Orva Guthrie",
    "sex": "M",
    "born": "18 Jan 1892",
    "died": "13 Oct 1976",
    "spouses": [{
        "name": "Hazel Dorothy Ringer",
        "born": "18 Jul 1897",
        "died": "1971",
        "father": "James A. Ringer",
        "mother": "Martha [Glove] Ringer",
        "buried": "Miller Cemetery at Terra Alta, WV",
    }],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 23},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "14271", "name": "Edna Mae Guthrie"},
        {"code": "14272", "name": "Emma Ruth Guthrie"},
        {"code": "14273", "name": "Mary Eleanor Guthrie"},
        {"code": "14274", "name": "Goldie Marie Guthrie"},
        {"code": "14275", "name": "Ralph Guthrie", "residences": ["Florida"]},
        {"code": "14276", "name": "Asa B. Guthrie", "residences": ["Barton, MD"]},
    ],
})

ENTRIES.append({
    "code": "1428",
    "name": "Anna Gay Guthrie",
    "sex": "F",
    "born": "23 Jan 1895",
    "died": "5 Dec 1944",
    "buried": "Shady Grove Cemetery, WV",
    "spouses": [{
        "name": "James Alvin Sines",
        "born": "16 Jun 1891",
        "died": "17 May 1964",
        "married": "Oct 1919",
        "father": "Lige Sines",
        "buried": "Shady Grove Cemetery, WV",
    }],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 23},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "14281", "name": "James Franklin Sines", "born": "18 Oct 1921"},
        {"code": "14282", "name": "Paul Carlus Sines", "born": "7 Dec 1923"},
        {"code": "14283", "name": "Mary Elizabeth Sines", "born": "23 Jan 1926", "died": "18 Oct 1975"},
        {"code": "14284", "name": "Robert Jackson Sines", "born": "1 Jun 1928"},
        {"code": "14285", "name": "Martha Sines", "born": "Mar 1930", "died": "15 Aug 1930", "flags": {"diedInInfancy": True}},
        {"code": "14286", "name": "Ethel Mae Sines", "born": "8 Sep 1931"},
        {"code": "14287", "name": "Willard Elijah Sines", "born": "22 Feb 1934"},
        {"code": "14288", "name": "Ralph Edward Sines", "born": "7 Feb 1936"},
    ],
})

ENTRIES.append({
    "code": "1429",
    "name": "Earl Guthrie",
    "sex": "M",
    "born": "23 Apr 1896",
    "died": "1971",
    "residences": ["Elliotsville Road"],
    "spouses": [{
        "name": "Myrtle Mae Rosenberger",
        "born": "1898",
        "died": "11 Nov 1976",
        "father": "Philp Rosenberger",
        "mother": "Sophronia Rosenberger",
    }],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 24},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "14291", "name": "Martha Guthrie", "born": "8 Sep 1914", "notes": "daughter of Myrtle"},
        {"code": "14292", "name": "Clyde Guthrie", "born": "4 Jun 1916"},
        {"code": "14293", "name": "Dorothy Guthrie", "born": "4 Jul 1918"},
        {"code": "14294", "name": "Fred Guthrie", "born": "28 Oct 1920"},
        {"code": "14295", "name": "Jessie Guthrie", "born": "20 Aug 1922"},
        {"code": "14296", "name": "Mabel Guthrie", "born": "1 Apr 1924"},
        {"code": "14297", "name": "Betty Guthrie", "born": "19 Feb 1927"},
        {"code": "14298", "name": "Earl Guthrie, Jr.", "born": "28 Mar 1928"},
        {"code": "14299", "name": "Lucy Guthrie", "born": "26 Jul 1931"},
        {"code": "1429A", "name": "Glen Guthrie", "born": "27 Mar 1933"},
        {"code": "1429B", "name": "Jack Guthrie", "born": "2 Feb 1936"},
        {"code": "1429C", "name": "Donna Jean Guthrie", "born": "18 Apr 1939"},
    ],
})

ENTRIES.append({
    "code": "1432",
    "name": "Margaret (Maggie) Sliger",
    "sex": "F",
    "born": "7 Aug 1883",
    "died": "24 Jul 1961",
    "spouses": [{"name": "Lewis Espon Myers"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 24},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "14321", "name": "Vernie Myers"},
        {"code": "14322", "name": "Hazel Myers"},
        {"code": "14323", "name": "Edna Myers"},
        {"code": "14324", "name": "Pearl Myers"},
        {"code": "14325", "name": "Effie Myers"},
        {"code": "14326", "name": "Jessie Myers"},
        {"code": "14327", "name": "Mildred Myers"},
        {"code": "14328", "name": "Gilbert Myers"},
        {"code": "14329", "name": "Donald Myers", "born": "31 Aug 1919"},
    ],
})

ENTRIES.append({
    "code": "1433",
    "name": "Sarah Ellen Sliger",
    "sex": "F",
    "born": "14 Sep 1885",
    "died": "7 May 1976",
    "spouses": [{"name": "Jacob Darnell"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 24},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "14331", "name": "Samuel Darnell"},
        {"code": "14332", "name": "Earl Darnell"},
        {"code": "14333", "name": "Albert Darnell"},
        {"code": "14334", "name": "Adam Darnell"},
        {"code": "14335", "name": "Elmer Darnell"},
        {"code": "14336", "name": "Pearl Darnell"},
        {"code": "14337", "name": "Dorothy Darnell"},
        {"code": "14338", "name": "Mae Darnell"},
        {"code": "14339", "name": "Mary Darnell"},
        {"code": "1433A", "name": "Sarah Darnell"},
        {"code": "1433B", "name": "Roberta Darnell"},
    ],
})

ENTRIES.append({
    "code": "1434",
    "name": "Mollie Sliger",
    "sex": "F",
    "born": "14 Nov 1888",
    "died": "18 May 1966",
    "spouses": [{"name": "Elmer Cuppett"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 24},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "14341", "name": "Bertha Elizabeth Cuppett"},
        {"code": "14342", "name": "Nellie Cuppett", "born": "6 Jul 1920"},
        {"code": "14343", "name": "Mamie Cuppett"},
        {"code": "14344", "name": "Harry Cuppett"},
    ],
})

ENTRIES.append({
    "code": "1435",
    "name": "Emma Pearl Sliger",
    "sex": "F",
    "born": "15 Aug 1895",
    "died": "17 Jun 1918",
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 24},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "14351", "name": "Joseph R. Sliger", "born": "7 Jun 1916"},
    ],
})

ENTRIES.append({
    "code": "1437",
    "name": "Bruce Sliger",
    "sex": "M",
    "died": "1946",
    "spouses": [{"name": "Olla Bell Goodwin", "born": "1 Sep 1907", "died": "25 Oct 1975"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 25},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "14371", "name": "Emma Sliger"},
        {"code": "14372", "name": "Jane Sliger"},
        {"code": "14373", "name": "Anna Bell Sliger"},
    ],
})

ENTRIES.append({
    "code": "1438",
    "name": "Herman Joseph Sliger",
    "sex": "M",
    "born": "2 Jul 1900",
    "died": "2 Apr 1977",
    "spouses": [{"name": "Myrtle E. Curvie", "married": "23 Oct 1922"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 25},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "14381", "name": "William Herman Sliger", "born": "1 Jun 1923", "died": "15 Jul 1992"},
    ],
})

ENTRIES.append({
    "code": "1441",
    "name": "Lillie Bell Thomas",
    "sex": "F",
    "born": "4 Jun 1879",
    "died": "11 Jul 1955",
    "buried": "Centenery Cemetery",
    "spouses": [{
        "name": "William Homer Sisler",
        "born": "1882",
        "died": "Mar 1925",
        "married": "20 Sep 1903",
        "father": "Jacob H. Sisler",
        "mother": "Mary Elizabeth [Wright] Sisler",
        "buried": "Centenery Cemetery",
        "details": "Married at Hazelton, WV by Joseph Guthrie.",
    }],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 25},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "14411", "name": "Charles Orval Sisler", "born": "20 Jul 1904"},
        {"code": "14412", "name": "Troy Wilbert Sisler", "born": "20 Nov 1905"},
        {"code": "14413", "name": "Carlus Eugene Sisler", "born": "3 Apr 1907"},
        {"code": "14414", "name": "Mary Ellen Sisler", "born": "27 Jan 1909"},
        {"code": "14415", "name": "Paul Edgar Sisler", "born": "28 Feb 1911"},
        {"code": "14416", "name": "George Ray Sisler", "born": "18 May 1916"},
    ],
})

ENTRIES.append({
    "code": "1442",
    "name": "Susannah A. Thomas",
    "sex": "F",
    "born": "31 Jan 1881",
    "died": "23 Aug 1929",
    "spouses": [{
        "name": "Jacob George Nicola",
        "born": "2 Apr 1881",
        "died": "3 Mar 1964",
        "married": "21 May 1903",
        "father": "John Nicola",
        "mother": "Clara [Teets] Nicola",
        "details": "Son of #173 John Nicola and Clara Teets.",
    }],
    "notes": "Yet another John-line endogamous marriage: she's grand-daughter of Christian (#13) via 144 Barbara Ellen; he's grandson of Susannah (#17) via 173 John Nicola.",
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 25},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "14421", "name": "Infant son", "born": "22 Aug 1909", "died": "22 Aug 1909", "flags": {"diedInInfancy": True}},
        {"code": "14422", "name": "Chester Martin Nicola", "born": "7 Oct 1914"},
    ],
})

ENTRIES.append({
    "code": "1443",
    "name": "Minnie May Thomas",
    "sex": "F",
    "born": "11 Aug 1886",
    "died": "24 Nov 1965",
    "buried": "Shady Grove",
    "spouses": [{
        "name": "Charles Anderson Harshbarger",
        "born": "9 Jan 1868",
        "died": "5 Mar 1956",
        "married": "19 Apr 1903",
        "father": "David K. Harshbarger",
        "mother": "Elizabeth [Guthrie] Harshbarger",
        "details": "Same as #164 — her first-cousin-once-removed (his mother is her grandmother's sister). See 164's entry for the children, who are recorded under both 1443x and 164x codes.",
    }],
    "notes": "PDF cross-references all her children to 164's children (1641-164C). Children appear under both lineage codes — see SEE_REFS.",
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 25},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
})

ENTRIES.append({
    "code": "1445",
    "name": "Laura Catherine Thomas",
    "sex": "F",
    "born": "28 Jan 1891",
    "died": "3 Jun 1961",
    "buried": "Shady Grove Cemetery, WV",
    "spouses": [{
        "name": "Lloyd Ray Friend",
        "born": "23 Jun 1890",
        "died": "18 Oct 1974",
        "father": "William H. Friend",
        "mother": "Eliza [Umbel] Friend",
        "buried": "Shady Grove Cemetery, WV",
    }],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 25},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "14451", "name": "Ethel H. Friend", "born": "7 Jun 1913"},
        {"code": "14452", "name": "Ivan Samuel Friend", "born": "7 Mar 1915"},
        {"code": "14453", "name": "Pearl Lovine Friend", "born": "29 Nov 1916"},
        {"code": "14454", "name": "Helen Dorothy Friend", "born": "12 Apr 1918"},
        {"code": "14455", "name": "Avis Mae Friend", "born": "28 Jun 1920"},
        {"code": "14456", "name": "Charles Orval Friend", "born": "3 Apr 1923", "died": "11 Aug 1985"},
        {"code": "14457", "name": "Virgil William Friend", "born": "17 Mar 1926", "died": "9 May 1994"},
        {"code": "14458", "name": "Sylvia Marie Friend", "born": "23 Jul 1930", "died": "17 Jun 1935", "flags": {"diedInInfancy": True}},
    ],
})


# === Pages 26-30 vision pass (2026-06-07): gen 5 detail ===
ENTRIES.append({
    "code": "1446",
    "name": "John Marshall Thomas",
    "sex": "M",
    "born": "1 Feb 1893",
    "died": "10 Sep 1964",
    "buried": "Shady Grove Cemetery, WV",
    "spouses": [{"name": "Margaret Lucille Griffith", "born": "1904", "died": "21 Apr 1948", "buried": "Shady Grove Cemetery, WV"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 26},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "14461", "name": "Arnold E. (Jack) Thomas"},
        {"code": "14462", "name": "Clifford E. (Buck) Thomas"},
        {"code": "14463", "name": "Janet Louise Thomas", "born": "19 Apr 1925"},
    ],
})

ENTRIES.append({
    "code": "1447",
    "name": "James Richard Thomas",
    "sex": "M",
    "born": "11 Mar 1896",
    "died": "30 Sep 1968",
    "buried": "Shady Grove Cemetery, WV",
    "spouses": [{
        "name": "Lula Pearl Fike",
        "born": "9 Nov 1903",
        "died": "16 Jul 1988",
        "father": "Gertrude Fike",
        "details": "Step-daughter of John Spiker.",
        "buried": "Shady Grove Cemetery, WV",
    }],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 26},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "14471", "name": "Infant son", "born": "11 Feb 1922", "died": "11 Feb 1922", "flags": {"diedInInfancy": True}},
        {"code": "14472", "name": "Jessie Mae Thomas", "born": "25 May 1923", "died": "30 Sep 1931", "buried": "Shady Grove Cemetery, WV"},
        {"code": "14473", "name": "James Robert Thomas", "born": "2 Mar 1930", "died": "22 Jun 1933", "buried": "Shady Grove Cemetery, WV"},
        {"code": "14474", "name": "Franklin Richard Thomas", "born": "11 Mar 1933"},
        {"code": "14475", "name": "David Ervin Thomas", "born": "6 Apr 1939"},
        {"code": "14476", "name": "Clarence Dewight Thomas", "born": "29 Oct 1942"},
    ],
})

ENTRIES.append({
    "code": "1448",
    "name": "Daisy Pearl Thomas",
    "sex": "F",
    "born": "7 Sep 1897",
    "died": "22 Jul 1967",
    "buried": "Maplewood Cemetery, Kingwood, WV",
    "spouses": [{
        "name": "Ray O. Strawser",
        "born": "5 Aug 1895",
        "died": "16 Apr 1977",
        "married": "27 Aug 1916",
        "father": "Elmer Strawser",
        "mother": "Sarah [Livengood] Strawser",
        "buried": "Maplewood Cemetery, Kingwood, WV",
        "details": "Married by Calvin Wolfe.",
    }],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 26},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "14481", "name": "Donna Mae Strawser", "born": "18 Jun 1917"},
        {"code": "14482", "name": "Paul Woodrow Strawser", "born": "23 Apr 1920"},
        {"code": "14483", "name": "Charles Ford Strawser", "born": "6 Jun 1923"},
        {"code": "14484", "name": "Lucilla V. Strawser", "born": "16 Nov 1926"},
        {"code": "14485", "name": "Cecil Ray Strawser", "born": "11 Aug 1935"},
    ],
})

ENTRIES.append({
    "code": "1451",
    "name": "Irvin A. Guthrie",
    "sex": "M",
    "born": "4 Nov 1884",
    "died": "4 Jun 1951",
    "spouses": [{"name": "Daisy M. Grim", "born": "12 May 1884", "married": "3 May 1902"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 26},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "14511", "name": "Helen L. Guthrie", "born": "4 Nov 1903"},
        {"code": "14512", "name": "Charles D. H. Guthrie", "born": "18 Dec 1905"},
    ],
})

ENTRIES.append({
    "code": "1452",
    "name": "Violet M. Guthrie",
    "sex": "F",
    "born": "1886",
    "died": "Mar 1953",
    "spouses": [{"name": "Howard Grim", "married": "1906"}],
    "notes": "PDF says only 'Had four Children'.",
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 26},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
})

ENTRIES.append({
    "code": "1454",
    "name": "Nola E. Guthrie",
    "sex": "F",
    "born": "28 Mar 1891",
    "died": "1950",
    "spouses": [{"name": "John P. Blosser, Sr.", "born": "7 Jul 1886", "died": "1952", "married": "21 Dec 1910"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 26},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "14541", "name": "John P. Blosser", "born": "8 Apr 1912"},
        {"code": "14542", "name": "Rosala V. Blosser"},
        {"code": "14543", "name": "Dorothy M. Blosser", "born": "20 Apr 1919"},
        {"code": "14544", "name": "David G. Blosser", "born": "24 Sep 1922"},
    ],
})

ENTRIES.append({
    "code": "1455",
    "name": "Daisy E. Guthrie",
    "sex": "F",
    "born": "4 Mar 1893",
    "spouses": [{"name": "James R. Baily", "born": "6 Jan 1892", "died": "28 Jul 1955", "married": "26 Oct 1911"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 26},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "14551", "name": "Leonard G. Baily", "born": "15 Dec 1914"},
        {"code": "14552", "name": "James Baily", "born": "12 Dec 1917"},
        {"code": "14553", "name": "Warren H. Baily", "born": "15 Jun 1921"},
        {"code": "14554", "name": "Betty J. Baily", "born": "28 Feb 1927"},
        {"code": "14555", "name": "Donald Baily", "born": "24 Apr 1931"},
        {"code": "14556", "name": "Robert D. Baily", "born": "28 Jun 1934"},
    ],
})

ENTRIES.append({
    "code": "1458",
    "name": "David Paul Guthrie",
    "sex": "M",
    "born": "4 Apr 1900",
    "died": "1963",
    "spouses": [
        {"name": "Stella Wilson", "born": "1900", "died": "1925", "married": "1918", "order": 1},
        {"name": "Nellie Weese", "married": "18 Feb 1929", "order": 2},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 27},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        # First marriage
        {"code": "14581", "name": "W. P. Guthrie", "born": "23 Jul 1922"},
        {"code": "14582", "name": "Vernice Elaine Guthrie", "born": "13 Nov 1923"},
        {"code": "14583", "name": "Rita Guthrie", "born": "4 Mar 1926"},
        {"code": "14584", "name": "Wallace J. Hinkle", "flags": {"adopted": True}},
    ],
})

ENTRIES.append({
    "code": "1459",
    "name": "Efleda A. Guthrie",
    "sex": "F",
    "born": "13 Feb 1903",
    "spouses": [{"name": "Charles Cole", "born": "14 Jun 1899", "married": "25 Feb 1926"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 27},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "14591", "name": "Charles Cole, Jr."},
        {"code": "14592", "name": "Sarah Jeremiah Cole"},
        {"code": "14593", "name": "Robert Cole"},
        {"code": "14594", "name": "Betty Sue Cole"},
        {"code": "14595", "name": "Ronald Cole"},
    ],
})

ENTRIES.append({
    "code": "1461",
    "name": "Sarah (Sadie) Catherine Miller",
    "sex": "F",
    "born": "22 Nov 1883",
    "died": "4 Apr 1958",
    "spouses": [
        {"name": "Earsmes Dodid (Dadid)", "born": "15 Apr 1875", "died": "13 Mar 1908", "married": "20 Oct 1904", "order": 1},
        {"name": "Alexander Miller", "born": "20 Nov 1867", "died": "25 Jan 1935", "married": "9 Aug 1914", "order": 2},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 27},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        # First marriage
        {"code": "14611", "name": "Irene Dodid", "born": "15 Apr 1905", "died": "19 Jul 1909", "flags": {"diedInInfancy": True}},
        {"code": "14612", "name": "Herbert Dodid", "born": "22 Mar 1907", "died": "19 Jul 1907", "flags": {"diedInInfancy": True}},
        {"code": "14613", "name": "George E. Dodid", "born": "27 Mar 1909"},
        # Second marriage
        {"code": "14614", "name": "Birges (Birdie) Agnes Miller", "born": "9 Jul 1915"},
        {"code": "14615", "name": "Violet Miller"},
        {"code": "14616", "name": "Person Miller"},
        {"code": "14617", "name": "Mable Miller", "born": "29 Jul 1917"},
    ],
})

ENTRIES.append({
    "code": "1462",
    "name": "David C. Miller",
    "sex": "M",
    "born": "4 Sep 1885",
    "died": "11 Feb 1957",
    "spouses": [{"name": "Mary Spellman", "born": "1883", "married": "1914"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 27},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "14621", "name": "James Miller", "born": "1917", "died": "1918", "flags": {"diedInInfancy": True}},
    ],
})

ENTRIES.append({
    "code": "1467",
    "name": "Pearl D. Miller",
    "sex": "F",
    "born": "22 Mar 1921",
    "spouses": [{"name": "Claude Jordon", "born": "1920", "married": "1938"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 27},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "14671", "name": "Betty Lou Jordon", "born": "11 Oct 1939"},
        {"code": "14672", "name": "Floyd Jordon", "born": "12 Oct 1942"},
    ],
})

ENTRIES.append({
    "code": "1471",
    "name": "Ada Ora Guthrie",
    "sex": "F",
    "born": "10 Apr 1886",
    "died": "1962",
    "spouses": [{"name": "Wallace Valentine Kahl", "born": "30 Apr 1871", "died": "15 Sep 1940", "married": "1905"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 27},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "14711", "name": "Emma C. Kahl", "born": "1906"},
        {"code": "14712", "name": "Opal I. Kahl", "born": "1908"},
        {"code": "14713", "name": "Russel R. Kahl", "born": "1910"},
        {"code": "14714", "name": "Ralph Kahl", "born": "19 Apr 1913"},
        {"code": "14715", "name": "Edna M. Kahl", "born": "1915"},
        {"code": "14716", "name": "Floyd R. Kahl", "born": "1917"},
        {"code": "14717", "name": "Eleanor E. Kahl", "born": "2 Apr 1920"},
        {"code": "14718", "name": "Edward Harold Kahl", "born": "16 Dec 1922"},
        {"code": "14719", "name": "Everett Kahl", "flags": {"stepChild": True}},
    ],
})

ENTRIES.append({
    "code": "1472",
    "name": "Hosea H. Guthrie",
    "sex": "M",
    "born": "16 Mar 1888",
    "died": "24 Mar 1919",
    "spouses": [{"name": "Addie Baily"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 28},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "14721", "name": "Gertrude Guthrie"},
        {"code": "14722", "name": "Ruth Guthrie"},
        {"code": "14723", "name": "Leona Guthrie"},
        {"code": "14724", "name": "Mildred Guthrie"},
    ],
})

ENTRIES.append({
    "code": "1473",
    "name": "Sarah Vivian Guthrie",
    "sex": "F",
    "born": "10 Feb 1890",
    "died": "1968",
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 28},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "14731", "name": "Everett Samuel Miller", "born": "21 Dec 1901"},
    ],
})

ENTRIES.append({
    "code": "1475",
    "name": "Carrie E. Guthrie",
    "sex": "F",
    "born": "12 Sep 1895",
    "died": "2 Dec 1959",
    "spouses": [{
        "name": "Edward Appleby",
        "born": "1889",
        "died": "1970",
        "married": "13 Feb 1910",
        "father": "John Appleby",
        "mother": "Renna [Benson] Appleby",
    }],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 28},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "14751", "name": "Thomas Edward Appleby", "born": "27 Sep 1911"},
        {"code": "14752", "name": "Margaret Irene Susan Appleby", "born": "29 Sep 1914"},
        {"code": "14753", "name": "Ida Mae Appleby", "born": "16 Oct 1926"},
    ],
})

ENTRIES.append({
    "code": "1476",
    "name": "Herbert J. Guthrie",
    "sex": "M",
    "born": "22 Aug 1898",
    "died": "27 Oct 1976",
    "spouses": [{"name": "Bessie Marie Wolfe", "born": "13 Jul 1903", "died": "13 Aug 1980", "married": "1 Apr 1920"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 28},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "14761", "name": "Thelma Edith Guthrie", "born": "19 Jan 1921"},
        {"code": "14762", "name": "Helen O. Guthrie", "born": "30 Nov 1924"},
        {"code": "14763", "name": "Magaret Irene Guthrie", "born": "24 Oct 1931"},
    ],
})

ENTRIES.append({
    "code": "1481",
    "name": "Mary Mae Guthrie",
    "sex": "F",
    "born": "8 Sep 1891",
    "died": "1954",
    "spouses": [{"name": "Chester H. McKenzie", "born": "12 Jan 1887", "died": "1954", "married": "9 Apr 1909"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 28},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "14811", "name": "Myrtle P. McKenzie", "born": "13 Jan 1920"},
        {"code": "14812", "name": "Violet R. McKenzie", "born": "19 Aug 1921"},
        {"code": "14813", "name": "Bessie Ellen McKenzie", "born": "28 Oct 1923"},
        {"code": "14814", "name": "Lillie M. McKenzie", "born": "8 Feb 1925"},
        {"code": "14815", "name": "Alice B. McKenzie", "born": "23 Jul 1926"},
        {"code": "14816", "name": "Chester F. McKenzie", "born": "15 Jan 1928"},
        {"code": "14817", "name": "Garnet Grace McKenzie", "born": "21 Aug 1929"},
        {"code": "14818", "name": "James R. McKenzie", "born": "8 Jun 1931", "died": "1 Oct 1931", "flags": {"diedInInfancy": True}},
        {"code": "14819", "name": "Martha Jane McKenzie", "born": "29 Jul 1933", "died": "5 Dec 1933", "flags": {"diedInInfancy": True}},
    ],
})

ENTRIES.append({
    "code": "1482",
    "name": "Russell R. Guthrie",
    "sex": "M",
    "born": "23 Jun 1895",
    "died": "28 Feb 1971",
    "spouses": [{"name": "Angeline Brandage", "died": "1900", "married": "13 Nov 1916"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 28},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "14821", "name": "Barbara Guthrie", "born": "11 Dec 1917"},
        {"code": "14822", "name": "Charles H. Guthrie"},
        {"code": "14823", "name": "Virginia Guthrie", "born": "17 Nov 1922"},
        {"code": "14824", "name": "Samuel F. Guthrie"},
    ],
})

ENTRIES.append({
    "code": "1484",
    "name": "Walter Guthrie",
    "sex": "M",
    "born": "1898",
    "died": "8 Mar 1960",
    "residences": ["Texas"],
    "spouses": [
        {"name": "Ethel or Edith Powell", "born": "1900", "died": "1919", "married": "1917", "order": 1},
        {"name": "Icy Snyder", "married": "1922", "order": 2},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 28},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        # First marriage
        {"code": "14841", "name": "Harman Guthrie", "born": "1918"},
        # Second marriage
        {"code": "14842", "name": "Arrena Guthrie"},
        {"code": "14843", "name": "Pauline Guthrie"},
        {"code": "14844", "name": "A. J. Guthrie"},
    ],
})

ENTRIES.append({
    "code": "1485",
    "name": "Bessie E. Guthrie",
    "sex": "F",
    "born": "15 Jul 1899",
    "died": "30 May 1949",
    "spouses": [{"name": "Rev. Oliver E. Hart", "born": "19 Jul 1895", "married": "3 Jun 1932", "details": "or 1942 — PDF ambiguous; lived at Fairchance, PA on the home place of Frank Guthrie."}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 29},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "14851", "name": "Delbert Guthrie", "born": "8 Jun 1928", "flags": {"adopted": True}, "notes": "nephew — son of Helen J. (#1489); see 14891"},
        {"code": "14852", "name": "Irene McKenzie", "flags": {"adopted": True}, "notes": "niece"},
    ],
})

ENTRIES.append({
    "code": "1486",
    "name": "Emma V. Guthrie",
    "sex": "F",
    "born": "1903",
    "spouses": [
        {"name": "James Kendall", "married": "1922", "order": 1},
        {"name": "Andrew Baker", "married": "1930", "order": 2},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 29},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        # First marriage
        {"code": "14861", "name": "Irene Kendall", "born": "25 Jan 1924"},
        {"code": "14862", "name": "Infant", "flags": {"diedInInfancy": True}},
        {"code": "14863", "name": "Infant", "flags": {"diedInInfancy": True}},
        # Second marriage
        {"code": "14864", "name": "Irma M. Baker", "born": "13 Jan 1930"},
        {"code": "14865", "name": "Thomas A. Baker", "born": "19 Jul 1932"},
        {"code": "14866", "name": "Donald Franklin Baker", "born": "9 Oct 1935"},
    ],
})

ENTRIES.append({
    "code": "1487",
    "name": "James E. Guthrie",
    "sex": "M",
    "born": "1904",
    "died": "1963",
    "spouses": [{"name": "Ida Mae Tates", "born": "1906", "married": "6 Apr 1924"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 29},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "14871", "name": "Elsie Elizabeth Guthrie", "born": "17 Jul 1926"},
        {"code": "14872", "name": "Perry Franklin Guthrie", "born": "28 Nov 1928"},
        {"code": "14873", "name": "Herbert Lester Guthrie", "born": "5 Jul 1933"},
        {"code": "14874", "name": "Ray Marshall Guthrie", "born": "21 Apr 1936"},
        {"code": "14875", "name": "Shirley Ann Guthrie", "born": "1 Feb 1943"},
        {"code": "14876", "name": "James E. Guthrie, Jr.", "born": "24 Apr 1945"},
    ],
})

ENTRIES.append({
    "code": "1488",
    "name": "Sarah E. Guthrie",
    "sex": "F",
    "born": "14 Nov 1906",
    "spouses": [{"name": "Peter Ray Brandgard", "born": "2 Feb 1903", "married": "12 Feb 1923"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 29},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "14881", "name": "Edward F. Brandgard", "born": "25 Dec 1923"},
        {"code": "14882", "name": "Evelene J. Brandgard", "born": "19 Jul 1927"},
        {"code": "14883", "name": "Marie Brandgard", "born": "29 Jan 1930", "died": "18 Feb 1930", "flags": {"diedInInfancy": True}},
        {"code": "14884", "name": "Pearl L. Brandgard", "born": "5 May 1934"},
        {"code": "14885", "name": "Peter Ray Brandgard, Jr.", "born": "5 Jan 1936"},
        {"code": "14886", "name": "Ralph S. Brandgard", "born": "16 Jun 1938"},
        {"code": "14887", "name": "Walter Joseph Brandgard", "born": "5 Nov 1939", "died": "19 Dec 1951"},
        {"code": "14888", "name": "Laura Bell Brandgard", "born": "16 Mar 1940", "died": "3 Aug 1940", "flags": {"diedInInfancy": True}},
        {"code": "14889", "name": "John R. Brandgard", "born": "18 Oct 1942"},
        {"code": "1488A", "name": "Clarence R. Brandgard", "born": "7 Nov 1944"},
    ],
})

ENTRIES.append({
    "code": "1489",
    "name": "Helen J. Guthrie",
    "sex": "F",
    "born": "28 Oct 1908",
    "spouses": [{"name": "Perry S. Tate", "born": "31 Aug 1908", "married": "24 Dec 1929"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 29},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "14891", "name": "Delbert Guthrie", "born": "8 Jun 1928", "notes": "Raised by Rev. Oliver R. and Bessie Hart his aunt (see 14851)"},
        {"code": "14892", "name": "Ester Leona Tate", "born": "8 May 1933"},
        {"code": "14893", "name": "Paul Kenneth Tate", "born": "14 Dec 1935"},
        {"code": "14894", "name": "Elenor Delores Tate", "born": "7 Nov 1939"},
        {"code": "14895", "name": "Elsie Loretta Tate", "born": "25 Jun 1941"},
        {"code": "14896", "name": "Nancy Arlene Tate", "born": "30 May 1945"},
    ],
})

ENTRIES.append({
    "code": "1611",
    "name": "Vida Barnes",
    "sex": "F",
    "born": "27 Mar 1881",
    "died": "26 Nov 1939",
    "spouses": [{"name": "David Earl Cuppett", "born": "13 Feb 1878", "died": "13 May 1959", "married": "26 Dec 1905", "occupation": "Attorney"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 29},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "16111", "name": "Reardon Stewart Colton Cuppett", "born": "29 Jan 1908"},
        {"code": "16112", "name": "David Earl Cuppett, Jr.", "born": "27 Feb 1913"},
        {"code": "16113", "name": "Mary Elizabeth Cuppett", "born": "19 Jun 1921"},
    ],
})

ENTRIES.append({
    "code": "1612",
    "name": "Nannie Barnes",
    "sex": "F",
    "born": "15 Dec 1882",
    "died": "20 Sep 1965",
    "spouses": [{"name": "Charles E. Burner", "born": "21 Sep 1882", "died": "2 May 1940", "married": "16 Nov 1907", "buried": "Shady Grove Cemetery, WV"}],
    "buried": "Shady Grove Cemetery, WV",
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 30},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "16121", "name": "Grant Irwin Burner", "born": "13 Aug 1908"},
    ],
})

ENTRIES.append({
    "code": "1621",
    "name": "Walter Amos Moyers",
    "sex": "M",
    "born": "27 Aug 1887",
    "died": "10 Mar 1968",
    "spouses": [{"name": "Mary G. VanSickle"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 30},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "16211", "name": "Rasely B. Moyers", "born": "5 Apr 1914"},
        {"code": "16212", "name": "Thomas Ugene Moyers", "born": "16 Jan 1918"},
        {"code": "16213", "name": "Walter Moyers, Jr."},
    ],
})

ENTRIES.append({
    "code": "1623",
    "name": "Harold D. Moyers",
    "sex": "M",
    "born": "24 Apr 1891",
    "died": "11 Jul 1971",
    "spouses": [{
        "name": "Grace Edith Rodeheaver",
        "born": "2 Aug 1895",
        "died": "30 Oct 1978",
        "married": "25 Sep 1912",
        "father": "Benton Rodeheaver",
        "mother": "Ida [Beeghly] Rodeheaver",
    }],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 30},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "16231", "name": "Helen Margaret Moyers", "born": "3 May 1913"},
        {"code": "16232", "name": "Juanita Ida Moyers", "born": "25 Nov 1917"},
        {"code": "16233", "name": "Irene Fay Moyers", "born": "17 Nov 1921"},
        {"code": "16234", "name": "Myron Harold Moyers", "born": "9 Oct 1924"},
        {"code": "16235", "name": "Hubert Benton Moyers", "born": "5 Feb 1929"},
        {"code": "16236", "name": "Katherline Grace Moyers", "born": "21 Jan 1931", "died": "21 Jan 1931", "flags": {"diedInInfancy": True}},
        {"code": "16237", "name": "Dwight Lorain Moyers", "born": "4 Oct 1932"},
    ],
})

ENTRIES.append({
    "code": "1624",
    "name": "Rosella May Moyers",
    "sex": "F",
    "born": "30 May 1899",
    "died": "5 Sep 1935",
    "spouses": [{"name": "Leman Wentworth Wright", "born": "13 Apr 1898", "died": "7 Jan 1966", "married": "1918"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 30},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "16241", "name": "Vernon Ray Wright", "born": "15 Sep 1920"},
        {"code": "16242", "name": "Norval G. Wright", "born": "1924", "died": "7 Jan 1944", "died_place": "Italy during WW II"},
        {"code": "16243", "name": "Gladys Marie Wright", "born": "28 Aug 1927"},
        {"code": "16244", "name": "Vivian Wright"},
        {"code": "16245", "name": "Naomi Irene Wright", "born": "22 Aug 1935", "died": "23 Aug 1935", "flags": {"diedInInfancy": True}, "buried": "Shady Grove Cemetery, WV"},
    ],
})

ENTRIES.append({
    "code": "1631",
    "name": "Jessie Ellen Harshbarger",
    "sex": "F",
    "born": "20 Feb 1890",
    "died": "31 Jan 1971",
    "buried": "Shady Grove Cemetery, WV",
    "spouses": [{
        "name": "Jeremiah Judson Nicola",
        "born": "11 Feb 1888",
        "died": "29 Sep 1972",
        "married": "23 Feb 1907",
        "father": "John Nicola",
        "mother": "Clara E. [Teets] Nicola",
        "details": "Same as #1732 — son of John Nicola (#173). Another John/John cross-marriage.",
        "buried": "Shady Grove Cemetery, WV",
    }],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 30},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "16311", "name": "Rosa Ethel Nicola", "born": "27 Sep 1907"},
        {"code": "16312", "name": "Earl Jackson Nicola", "born": "26 Sep 1909"},
        {"code": "16313", "name": "Ray Judson Nicola", "born": "4 Apr 1912", "died": "4 Sep 1935"},
        {"code": "16314", "name": "Pauline Lavena Nicola", "born": "1 Apr 1914"},
        {"code": "16315", "name": "Marie Pearl Nicola", "born": "9 Apr 1919"},
        {"code": "16316", "name": "Margaret Ellen Nicola", "born": "1 Jun 1923"},
        {"code": "16317", "name": "Thelma Virginia Nicola", "born": "24 Oct 1925"},
        {"code": "16318", "name": "Judson (Nick) Junior Nicola", "born": "27 Feb 1930"},
    ],
})

ENTRIES.append({
    "code": "1641",
    "name": "William Ralph Harshbarger",
    "sex": "M",
    "born": "3 Feb 1904",
    "died": "16 Oct 1988",
    "buried": "Shady Grove",
    "spouses": [{
        "name": "Edna Mae Spiker",
        "born": "27 Aug 1911",
        "died": "29 Nov 1987",
        "married": "8 Sep 1928",
        "married_place": "Hazelton, WV",
        "father": "Oliver Clark Spiker",
        "mother": "Laura [Guthrie] Spiker",
        "details": "Same as #17132 — daughter of Oliver Clark Spiker (#1713).",
        "buried": "Shady Grove",
    }],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 30},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "16411", "name": "Beulah Mae Harshbarger", "born": "7 Apr 1929"},
    ],
})


# === Pages 31-35 vision pass (2026-06-07): 164x continued + 17xx Spiker/Nicola/Frey ===
ENTRIES.append({
    "code": "1642",
    "name": "Walter David Harshbarger",
    "sex": "M",
    "born": "16 Oct 1906",
    "died": "25 May 1968",
    "buried": "Shady Grove Cemetery, WV",
    "spouses": [{"name": "Edna Pearl Seese", "born": "28 Feb 1907", "died": "1 Feb 1979", "married": "7 Oct 1933",
                 "father": "William Brice Seese", "mother": "Maggie [Methemy] Seese",
                 "buried": "Shady Grove Cemetery, WV"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 31},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "16421", "name": "Anna Marie Harshbarger", "born": "5 Jun 1935"},
        {"code": "16422", "name": "Mary Ellen Harshbarger", "born": "6 Feb 1937"},
        {"code": "16423", "name": "Shirley Mae Harshbarger", "born": "26 Oct 1942"},
    ],
})

ENTRIES.append({
    "code": "1643",
    "name": "Albert Richard Harshbarger",
    "sex": "M",
    "born": "14 Dec 1908",
    "died": "6 Nov 1973",
    "spouses": [{"name": "Alma Morrison", "born": "21 Jun 1922", "died": "11 Jun 1997", "married": "18 Sep 1943",
                 "father": "Lewis W. Morrison", "mother": "Victoria [Burgess] Morrison"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 31},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "16431", "name": "Sylvia Ionea Harshbarger", "born": "8 Nov 1946"},
        {"code": "16432", "name": "Lillie Sue Harshbarger", "born": "7 Jul 1954"},
    ],
})

ENTRIES.append({
    "code": "1644",
    "name": "Harrison Theodore Harshbarger",
    "sex": "M",
    "born": "4 Apr 1911",
    "died": "4 Jun 1986",
    "spouses": [
        {"name": "Wilma [Philipps] Niner", "married": "24 Oct 1943", "order": 1},
        {"name": "Mildred (Judy) Arlene Scell", "born": "8 Feb 1940", "married": "6 Oct 1962",
         "father": "James Harold Scell", "mother": "Emma Marion [Eisentrout] Scell", "order": 2},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 31},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "16441", "name": "Harrison (Teddy) Theodore Harshbarger", "born": "15 May 1963"},
        {"code": "16442", "name": "James Allen Harshbarger", "born": "6 Dec 1965"},
    ],
})

ENTRIES.append({
    "code": "1645",
    "name": "Elizabeth Ellen Harshbarger",
    "sex": "F",
    "born": "7 Apr 1913",
    "died": "17 Jul 1957",
    "spouses": [{"name": "Francis Fresh", "born": "13 Jul 1910", "died": "1 Jul 1987", "married": "6 Feb 1937",
                 "father": "David Grant Fresh", "mother": "Rebecca Lucinda [Bittinger] Fresh"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 31},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "16451", "name": "Rosetta Grace Fresh", "born": "5 Sep 1937"},
        {"code": "16452", "name": "Alvin Francis Fresh", "born": "21 May 1939"},
        {"code": "16453", "name": "Doris Jean Fresh", "born": "4 Nov 1943"},
        {"code": "16454", "name": "Infant Daughter", "born": "4 Nov 1943", "died": "4 Nov 1943", "flags": {"diedInInfancy": True}},
        {"code": "16455", "name": "Infant Daughter", "born": "4 Nov 1943", "died": "5 Nov 1943", "flags": {"diedInInfancy": True}},
        {"code": "16456", "name": "Betty Mae Fresh", "born": "10 Mar 1955"},
    ],
})

ENTRIES.append({
    "code": "1647",
    "name": "Charles Reuben Harshbarger",
    "sex": "M",
    "born": "16 Nov 1917",
    "spouses": [{"name": "Helen Mae Thomas", "born": "10 Sep 1920", "married": "25 Dec 1940",
                 "father": "Frank Thomas", "mother": "Maggie [Huff] Thomas"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 31},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "16471", "name": "Barbara Jean Harshbarger", "born": "27 Mar 1936", "notes": "Reuben adopted Helen's daughter."},
    ],
})

ENTRIES.append({
    "code": "1648",
    "name": "Pearl Catherine Harshbarger",
    "sex": "F",
    "born": "2 Jul 1919",
    "died": "7 Mar 1984",
    "spouses": [{"name": "Ross Carlton Miller", "born": "4 Sep 1908", "died": "29 May 1990", "married": "9 May 1942"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 31},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "16481", "name": "Infant son", "born": "12 Aug 1943", "died": "12 Aug 1943", "flags": {"diedInInfancy": True}},
        {"code": "16482", "name": "Ross Carlton Miller", "born": "14 Apr 1946"},
        {"code": "16483", "name": "Norma Jean Miller", "born": "6 Sep 1947"},
    ],
})

ENTRIES.append({
    "code": "164A",
    "name": "Myrtle Grace Harshbarger",
    "sex": "F",
    "born": "22 Feb 1923",
    "died": "2 Sep 1964",
    "spouses": [{"name": "Verl Wilton Smith", "born": "23 Dec 1922", "married": "22 Feb 1943",
                 "buried": "Fairview Cemetery, Pisgah, WV"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 31},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "164A1", "name": "Verl Junior Smith", "born": "6 Jun 1943"},
        {"code": "164A2", "name": "Ronald Kenneth Smith", "born": "28 Feb 1947"},
        {"code": "164A3", "name": "Linda Grace Smith", "born": "3 Jan 1949"},
    ],
})

ENTRIES.append({
    "code": "164B",
    "name": "Daisy Bell Harshbarger",
    "sex": "F",
    "born": "11 Feb 1925",
    "spouses": [
        {"name": "James W. Ressler", "born": "1914", "died": "25 Nov 1981", "married": "Jun 1946", "order": 1},
        {"name": "John George Jacob Rude", "born": "30 Aug 1922", "died": "23 Jun 1971", "married": "5 Apr 1957", "order": 2},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 31},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "164B1", "name": "Charles Marion Ressler", "born": "11 Jun 1947"},
    ],
})

ENTRIES.append({
    "code": "164C",
    "name": "Goldie Irene Harshbarger",
    "sex": "F",
    "born": "13 May 1927",
    "spouses": [{"name": "Dayton Lee Sager", "born": "3 Nov 1921", "died": "10 Aug 1980", "married": "29 Mar 1947"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 32},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "164C1", "name": "Kenneth Lee Sager", "born": "19 Jan 1948"},
        {"code": "164C2", "name": "Richard Ervin Sager", "born": "7 Nov 1949"},
        {"code": "164C3", "name": "Dolores Irene Sager", "born": "21 May 1955"},
    ],
})

ENTRIES.append({
    "code": "1662",
    "name": "Emma Harshbarger",
    "sex": "F",
    "born": "30 Jan 1906",
    "spouses": [{"name": "Playford Clyde Hileman", "born": "4 Jul 1901", "died": "2 Feb 1982", "married": "2 Jul 1923",
                 "buried": "Oaklawn Cemetery, Uniontown, PA"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 32},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "16621", "name": "Charles Ray Hileman", "born": "18 Feb 1925"},
        {"code": "16622", "name": "Playford Gail Hileman", "born": "7 Jan 1929"},
    ],
})

ENTRIES.append({
    "code": "1663",
    "name": "Jeremiah Joseph Harshbarger",
    "sex": "M",
    "born": "6 Jul 1911",
    "spouses": [{"name": "Mildred Maud Spiker", "born": "13 Mar 1916", "died": "6 Jun 1983", "married": "6 Jan 1934",
                 "details": "Same as #17133 — daughter of Oliver Clark Spiker (#1713)."}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 32},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "16631", "name": "Mary Louise Harshbarger", "born": "4 Jul 1935"},
        {"code": "16632", "name": "Vernice Ann Harshbarger", "born": "20 Mar 1954", "died": "22 Mar 1954", "flags": {"diedInInfancy": True}, "buried": "Shady Grove Cemetery, WV"},
    ],
})

ENTRIES.append({
    "code": "1664",
    "name": "David Harshbarger",
    "sex": "M",
    "born": "9 Dec 1913",
    "died": "24 Aug 1987",
    "spouses": [{"name": "Dorothy Lou Hileman", "born": "30 Aug 1920", "married": "20 Jul 1946"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 32},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "16641", "name": "Marvin Lee Hileman", "born": "20 Sep 1942"},
    ],
})

ENTRIES.append({
    "code": "1711",
    "name": "Jacob George Spiker",
    "sex": "M",
    "born": "5 Oct 1877",
    "died": "30 May 1944",
    "spouses": [{"name": "Mary Mae Faulkner", "born": "27 Dec 1878", "died": "14 May 1961", "married": "8 Nov 1903",
                 "buried": "Webbs Chapel Cemetery"}],
    "buried": "Webbs Chapel Cemetery",
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 32},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "17111", "name": "Clarence Webster Spiker", "born": "9 Jun 1906", "died": "2 Jul 1932"},
        {"code": "17112", "name": "Ivon Theadore Spiker", "born": "12 Dec 1910"},
        {"code": "17113", "name": "Rosa Silvia Spiker", "born": "24 May 1917"},
    ],
})

ENTRIES.append({
    "code": "1712",
    "name": "John Henry Spiker",
    "sex": "M",
    "born": "5 Apr 1881",
    "died": "6 Oct 1938",
    "occupation": "Farmer and timber cutter",
    "buried": "Webbs Chapel Cemetery",
    "spouses": [
        {"name": "Laura Fike", "born": "7 Oct 1888", "died": "1 Nov 1911", "married": "14 Feb 1906", "order": 1},
        {"name": "Gertrude Mae Fike", "born": "8 Sep 1887", "died": "11 Sep 1976", "married": "8 Sep 1912", "order": 2},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 32},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "17121", "name": "Floyd Sanford Spiker", "born": "8 Oct 1907", "died": "6 Jun 1944", "died_place": "France"},
        {"code": "17122", "name": "Grace Evelyn Spiker", "born": "5 Sep 1910"},
        {"code": "17123", "name": "Blanche Goldie Spiker", "born": "24 Dec 1913"},
        {"code": "17124", "name": "Dora Spiker", "born": "14 Oct 1919"},
    ],
})

ENTRIES.append({
    "code": "1713",
    "name": "Oliver Clark Spiker",
    "sex": "M",
    "born": "15 Feb 1886",
    "died": "29 Sep 1974",
    "buried": "Webbs Chapel Cemetery",
    "spouses": [{
        "name": "Laura Guthrie",
        "born": "19 Apr 1889",
        "died": "24 Oct 1944",
        "married": "14 Feb 1909",
        "details": "Same as #765 in James's branch.",
    }],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 33},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "17131", "name": "Ralph Ersel Spiker", "born": "17 Jan 1910", "died": "18 Dec 1912", "flags": {"diedInInfancy": True}},
        {"code": "17132", "name": "Edna Mae Spiker", "born": "27 Aug 1911"},
        {"code": "17133", "name": "Mildred Maud Spiker", "born": "13 Mar 1916"},
        {"code": "17134", "name": "Shirel Victoria Spiker", "born": "6 Jul 1918"},
        {"code": "17135", "name": "Thelma Olieta Spiker", "born": "2 Dec 1921"},
        {"code": "17136", "name": "Ruth Virginia Spiker", "born": "23 Apr 1923"},
    ],
})

ENTRIES.append({
    "code": "1721",
    "name": "James Guthrie",
    "sex": "M",
    "born": "2 Feb 1879",
    "died": "29 Apr 1965",
    "spouses": [{"name": "Caroline (Carrie) B. Maust", "born": "21 Jun 1889", "died": "9 May 1965", "married": "6 Mar 1908"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 33},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "17211", "name": "Glenn Guthrie", "born": "4 Sep 1909"},
        {"code": "17212", "name": "Ruth Guthrie", "born": "3 May 1912"},
        {"code": "17213", "name": "Ethel Guthrie", "born": "18 Jan 1914"},
        {"code": "17214", "name": "Dora Guthrie", "born": "24 Apr 1916"},
        {"code": "17215", "name": "Ada Bell Guthrie", "born": "27 Sep 1921"},
    ],
})

ENTRIES.append({
    "code": "1723",
    "name": "Hattie Guthrie",
    "sex": "F",
    "born": "20 Dec 1881",
    "died": "7 Jan 1925",
    "spouses": [{
        "name": "Joseph Henry Harshbarger",
        "born": "3 Mar 1874",
        "died": "15 Jan 1938",
        "married": "28 Apr 1902",
        "details": "Same as #166. Hattie also has code #743 in James's branch.",
    }],
    "notes": "Triple-coded: 1723, 743 (James), husband is 166 (John).",
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 33},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "17231", "name": "Homer Loid Harshbarger", "born": "27 Sep 1902", "died": "6 Apr 1927"},
        {"code": "17232", "name": "Emma Harshbarger", "born": "30 Jan 1906"},
        {"code": "17233", "name": "Jeremiah Joseph Harshbarger", "born": "6 Jul 1911"},
        {"code": "17234", "name": "David Harshbarger", "born": "9 Dec 1913"},
    ],
})

ENTRIES.append({
    "code": "1726",
    "name": "Loyd (Lloyd) Guthrie",
    "sex": "M",
    "born": "2 Apr 1887",
    "died": "21 Oct 1979",
    "spouses": [{"name": "Minnie Catherine Thomas", "born": "24 Dec 1902", "died": "3 Feb 1986", "married": "9 Jul 1921"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 33},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "17261", "name": "Clarence Edward Guthrie", "born": "8 Jan 1925"},
        {"code": "17262", "name": "Ruth Dennis", "born": "17 Nov 1926"},
    ],
})

ENTRIES.append({
    "code": "1727",
    "name": "Stella Guthrie",
    "sex": "F",
    "born": "8 May 1889",
    "died": "27 Jan 1960",
    "buried": "Shady Grove Cemetery, WV",
    "spouses": [{
        "name": "Charles C. Moyers",
        "born": "23 Sep 1889",
        "died": "26 May 1956",
        "married": "16 May 1919",
        "details": "Same as #1622. Triple-cross-marriage: Stella has codes 747 (James), 1727 (here), wife of 1622.",
    }],
    "notes": "Children 17271-17274 are the same as 16221-16224 (under Charles's mother's side).",
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 33},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": "Children are SEE_REF to 16221-16224."},
})

ENTRIES.append({
    "code": "1728",
    "name": "Troy Guthrie",
    "sex": "M",
    "born": "24 Feb 1891",
    "died": "3 Dec 1966",
    "spouses": [{"name": "Eula Esta Fike", "born": "21 May 1901", "married": "21 May 1921"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 33},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "17281", "name": "Robert Eugene Guthrie", "born": "6 Feb 1929", "died": "7 Feb 1929", "flags": {"diedInInfancy": True}},
        {"code": "17282", "name": "Thelma Pearl Guthrie", "born": "5 Feb 1930"},
        {"code": "17283", "name": "Alice Mae Guthrie", "born": "6 Oct 1932"},
        {"code": "17284", "name": "Dwight J. Guthrie", "born": "6 May 1934"},
    ],
})

ENTRIES.append({
    "code": "172B",
    "name": "Dessie Guthrie",
    "sex": "F",
    "born": "6 Apr 1899",
    "died": "26 Nov 1986",
    "spouses": [{"name": "Claud Bartholomew", "born": "14 May 1890", "died": "3 Apr 1968", "married": "18 Mar 1922"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 34},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "172B1", "name": "Donald Bartholomew", "born": "4 Feb 1923", "died": "9 Feb 1923", "flags": {"diedInInfancy": True}},
        {"code": "172B2", "name": "Agnes Rosalie Bartholomew", "born": "15 Mar 1924"},
        {"code": "172B3", "name": "Evelyn Irene Bartholomew", "born": "24 Sep 1926"},
        {"code": "172B4", "name": "Paul Eugene Bartholomew", "born": "18 May 1928"},
        {"code": "172B5", "name": "Dorothy May Bartholomew", "born": "31 May 1930"},
        {"code": "172B6", "name": "Mable Viola Bartholomew", "born": "27 Dec 1933"},
        {"code": "172B7", "name": "David Matthew Bartholomew", "born": "12 Jan 1940"},
    ],
})

ENTRIES.append({
    "code": "1731",
    "name": "Jacob George Nicola",
    "sex": "M",
    "born": "2 Apr 1881",
    "died": "3 Mar 1964",
    "spouses": [
        {"name": "Susannah Thomas", "born": "31 Jan 1881", "died": "23 Aug 1929", "married": "21 May 1903",
         "details": "Same as #1442 — daughter of Barbara Ellen Guthrie #144.", "order": 1},
        {"name": "Martha (Matt) Bishoff Ringer", "born": "14 Sep 1866", "died": "29 Dec 1944", "married": "6 May 1932",
         "details": "Widow of Noah Ringer.", "order": 2},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 34},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "17311", "name": "Infant son", "born": "22 Aug 1909", "died": "22 Aug 1909", "flags": {"diedInInfancy": True}},
        {"code": "17312", "name": "Chester Martin Nicola", "born": "7 Oct 1914"},
    ],
})

ENTRIES.append({
    "code": "1732",
    "name": "Jeremiah Judson Nicola",
    "sex": "M",
    "born": "11 Feb 1888",
    "died": "29 Sep 1972",
    "spouses": [{
        "name": "Jessie Ellen Harshbarger",
        "born": "20 Feb 1890",
        "died": "31 Jan 1971",
        "married": "23 Feb 1907",
        "details": "Same as #1631 — daughter of Virginia Alice Jennie Harshbarger #163.",
    }],
    "notes": "Children share codes with 1631x (mother's side).",
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 34},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": "Children cross-coded as 1631x."},
})

ENTRIES.append({
    "code": "1733",
    "name": "Carrie May Nicola",
    "sex": "F",
    "born": "5 Mar 1892",
    "died": "10 Oct 1972",
    "spouses": [{"name": "Orval C. Friend", "born": "13 Mar 1888", "died": "18 Apr 1982", "married": "10 Jun 1909",
                 "buried": "Shady Grove"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 34},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "17331", "name": "Harry C. Friend", "born": "23 May 1910", "died": "27 May 1910", "flags": {"diedInInfancy": True}},
        {"code": "17332", "name": "Goldie Marie Friend", "born": "24 Oct 1911"},
        {"code": "17333", "name": "Gilbert Arnold Friend", "born": "1 Aug 1914", "died": "28 Feb 1951"},
        {"code": "17334", "name": "Frank William Friend"},
        {"code": "17335", "name": "Edna Friend", "born": "2 May 1919"},
        {"code": "17336", "name": "Junior Clinton Friend", "born": "24 May 1928"},
        {"code": "17337", "name": "Thelma Grace Friend", "born": "13 Mar 1930"},
    ],
})

ENTRIES.append({
    "code": "1741",
    "name": "Troy A. Nicola",
    "sex": "M",
    "born": "11 Jun 1886",
    "died": "10 Jul 1952",
    "spouses": [
        {"name": "Bertha Montgomery", "married": "1905", "order": 1},
        {"name": "Elsie Lambert", "born": "1902", "died": "1956", "order": 2},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 34},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "17411", "name": "Mildred Nicola"},
        {"code": "17412", "name": "Helen Nicola"},
    ],
})

ENTRIES.append({
    "code": "1742",
    "name": "Estella L. Nicola",
    "sex": "F",
    "born": "11 Oct 1887",
    "born_alt": "10 Oct 1887",
    "died": "20 Oct 1911",
    "spouses": [{"name": "George Moore", "born": "22 Jun 1884", "died": "1940", "married": "12 Nov 1904"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 34},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "17421", "name": "Hazel Moore", "born": "4 Nov 1908"},
    ],
})

ENTRIES.append({
    "code": "1743",
    "name": "Fredrick R. Nicola",
    "sex": "M",
    "born": "1891",
    "died": "24 Nov 1970",
    "spouses": [
        {"name": "Edna", "married": "1914", "order": 1},
        {"name": "Ethel", "born": "1903", "order": 2},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 34},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "17431", "name": "Paul Nicola"},
    ],
})

ENTRIES.append({
    "code": "1744",
    "name": "Clarence Herbert Nicola",
    "sex": "M",
    "born": "28 Mar 1894",
    "died": "1971",
    "spouses": [{"name": "Lillian S. Ridenour", "born": "23 Oct 1902", "died": "1965", "married": "1920"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 35},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "17441", "name": "Clarence Herbert Nicola Jr.", "born": "20 Nov 1920"},
    ],
})

ENTRIES.append({
    "code": "1745",
    "name": "Homer Andrew Nicola",
    "sex": "M",
    "born": "16 Oct 1896",
    "spouses": [{"name": "Dove Poling", "born": "22 Jun 1898", "married": "24 Jun 1921"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 35},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "17451", "name": "Ruth Bertha Nicola", "born": "31 Aug 1923"},
        {"code": "17452", "name": "Hilda Colleen Nicola", "born": "6 Oct 1925"},
        {"code": "17453", "name": "Howard Andrew Nicola", "born": "12 May 1928"},
        {"code": "17454", "name": "Joan Nicola", "born": "23 Oct 1930"},
        {"code": "17455", "name": "Bernald Nale Nicola", "born": "30 Jul 1937"},
        {"code": "17456", "name": "Dorsey Eugene Nicola", "born": "5 Apr 1940"},
    ],
})

ENTRIES.append({
    "code": "1747",
    "name": "Laura Bell Nicola",
    "sex": "F",
    "born": "1904",
    "spouses": [{"name": "James Rockwell", "married": "1918"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 35},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "17471", "name": "Son"},
        {"code": "17472", "name": "Son"},
    ],
})

ENTRIES.append({
    "code": "1751",
    "name": "Goldie Nicola",
    "sex": "F",
    "born": "3 Feb 1890",
    "died": "22 Jul 1934",
    "spouses": [{"name": "Howard Phillips"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 35},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "17511", "name": "Martha Phillips", "born": "24 Jan 1918"},
    ],
})

ENTRIES.append({
    "code": "1762",
    "name": "Edna Anna Nicola",
    "sex": "F",
    "born": "21 Mar 1897",
    "died": "2 Dec 1973",
    "spouses": [{"name": "Albert Terry (Bert) Miller", "born": "5 Aug 1881", "born_place": "Utah", "married": "8 Jun 1918"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 35},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "17621", "name": "Robert Martin Miller", "born": "8 Aug 1920"},
        {"code": "17622", "name": "Wilson Nicola Miller", "born": "3 Apr 1925"},
        {"code": "17623", "name": "Helen Virginia Miller", "born": "11 Dec 1926"},
    ],
})

ENTRIES.append({
    "code": "1772",
    "name": "Floyd Thamer Frey",
    "sex": "M",
    "born": "17 Feb 1892",
    "died": "1965",
    "spouses": [
        {"name": "Hazel Elizabeth Marshall", "born": "21 Jun 1896", "died": "7 Mar 1936", "married": "1914", "order": 1},
        {"name": "Mildred M. Semmelman", "married": "25 Mar 1938", "order": 2},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 36},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "17721", "name": "Floyd Thamer Frey, Jr.", "born": "7 Aug 1916"},
        {"code": "17722", "name": "Ella Christine Frey", "born": "25 Dec 1917"},
        {"code": "17723", "name": "Robert Lewis Frey", "born": "19 May 1919"},
        {"code": "17724", "name": "Edythe Lucille Frey"},
        {"code": "17725", "name": "Ralph Marshall Frey"},
        {"code": "17726", "name": "James William Frey", "born": "4 Aug 1923", "died": "19 Jan 1939"},
        {"code": "17727", "name": "Lelia Margaret Frey", "born": "6 Sep 1925"},
        {"code": "17728", "name": "George Calvin Frey", "born": "1 Mar 1927"},
        {"code": "17729", "name": "Charles Leon Frey", "born": "17 Aug 1929"},
        {"code": "1772A", "name": "Daniel Harold Frey", "born": "17 Jun 1931"},
        {"code": "1772B", "name": "Joanne Frey", "died": "in infancy", "flags": {"diedInInfancy": True}},
        {"code": "1772C", "name": "John Thomas Frey"},
        {"code": "1772D", "name": "Darl Eugene Frey"},
        {"code": "1772E", "name": "Donald Semmelman", "flags": {"stepChild": True}},
        {"code": "1772F", "name": "Lewis Semmelman", "flags": {"stepChild": True}},
    ],
})


# === Pages 36-40 vision pass (2026-06-07): end of gen 4 + start of gen 5 detail ===
ENTRIES.append({
    "code": "1773",
    "name": "Hugh M. Frey",
    "sex": "M",
    "born": "9 Jan 1894",
    "died": "2 Mar 1951",
    "spouses": [{"name": "Myrtle Shaffer", "born": "26 May 1900"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 36},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "17731", "name": "Harold Frey", "born": "12 Dec 1920"},
        {"code": "17732", "name": "Evelyn Frey", "born": "23 Jan 1923"},
        {"code": "17733", "name": "Ellen Frey", "born": "6 May 1927"},
    ],
})

ENTRIES.append({
    "code": "1774",
    "name": "Charles Hobert Frey",
    "sex": "M",
    "born": "18 Aug 1897",
    "died": "10 Jan 1946",
    "spouses": [
        {"name": "Nima Blake", "born": "31 Dec 1900", "order": 1},
        {"name": "Ethel Heckle", "order": 2},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 36},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "17741", "name": "Ruth Frey", "born": "14 Sep 1921"},
        {"code": "17742", "name": "Infant son", "flags": {"diedInInfancy": True}},
    ],
})

ENTRIES.append({
    "code": "1775",
    "name": "Earl Frey",
    "sex": "M",
    "born": "27 Aug 1900",
    "spouses": [{"name": "Addie Dove Shaffer", "born": "25 Dec 1905", "died": "Nov 1989"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 36},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "17751", "name": "William A. Frey", "born": "15 Apr 1922"},
        {"code": "17752", "name": "Geraldine Frey", "born": "9 Apr 1925"},
        {"code": "17753", "name": "Don Robert Frey", "born": "28 Apr 1927"},
        {"code": "17754", "name": "Hilda L. Frey", "born": "1 Aug 1934"},
    ],
})

ENTRIES.append({
    "code": "1776",
    "name": "William Darrel Frey",
    "sex": "M",
    "born": "13 Jul 1903",
    "died": "15 Mar 1992",
    "spouses": [
        {"name": "Trella Wolfe", "born": "19 Apr 1903", "died": "Mar 1975", "married": "11 Jul 1921", "order": 1},
        {"name": "Alice Ruth Austin", "married": "Jun 1977", "order": 2},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 36},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "17761", "name": "Dorothy V. Frey", "born": "28 Jun 1926"},
        {"code": "17762", "name": "William D. Frey", "born": "30 May 1934"},
    ],
})

ENTRIES.append({
    "code": "1777",
    "name": "James Doyle Frey",
    "sex": "M",
    "born": "4 May 1912",
    "spouses": [{"name": "Phylis", "born": "16 Apr 1912"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 36},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "17771", "name": "Jean Frey", "born": "9 Nov 1933"},
    ],
})

ENTRIES.append({
    "code": "1781",
    "name": "Clarence Everett Ball",
    "sex": "M",
    "born": "6 Jul 1891",
    "died": "18 Aug 1960",
    "spouses": [
        {"name": "Katie Griffith", "married": "Jan 1919", "order": 1, "details": "Lived in Grafton, WV"},
        {"name": "Icy Wilson", "order": 2},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 36},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "17811", "name": "Vincent Lee Ball", "born": "10 Feb 1922"},
        {"code": "17812", "name": "Ada Catherine Ball", "born": "12 Jan 1923"},
        {"code": "17813", "name": "Anna Bell Ball", "born": "4 Sep 1925"},
    ],
})

ENTRIES.append({
    "code": "1782",
    "name": "Stanley R. Ball",
    "sex": "M",
    "born": "13 Aug 1893",
    "died": "1 Nov 1917",
    "spouses": [{"name": "Bessie McDaniels", "born": "1897", "died": "15 May 1921", "married": "Mar 1916"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 36},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "17821", "name": "Raymond Murl Ball", "born": "23 Aug 1916"},
        {"code": "17822", "name": "Evelyn Ball", "born": "29 Dec 1917"},
    ],
})

ENTRIES.append({
    "code": "1783",
    "name": "Herman E. Ball",
    "sex": "M",
    "born": "29 Dec 1895",
    "died": "29 Jul 1957",
    "spouses": [{"name": "Lillie C. Moats", "born": "15 Dec 1890", "married": "15 May 1921"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 36},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "17831", "name": "Paul Morris Ball", "born": "5 May 1922"},
        {"code": "17832", "name": "Charles William Ball", "born": "21 Aug 1923"},
        {"code": "17833", "name": "Russell Edgar Ball", "born": "3 Dec 1924", "died_alt": "1926"},
        {"code": "17834", "name": "Leo Dennis Ball"},
    ],
})

ENTRIES.append({
    "code": "1791",
    "name": "Edith Grace Carol",
    "sex": "F",
    "born": "4 Feb 1901",
    "died": "27 Jun 1963",
    "spouses": [{"name": "Clarence N. Gelhausen", "born": "21 Mar 1892", "married": "31 Dec 1924"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 36},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "17911", "name": "Harold D. Gelhausen", "born": "13 Sep 1934"},
        {"code": "17912", "name": "Georgie Lee Gelhausen", "born": "2 Aug 1936"},
        {"code": "17913", "name": "Freddie Gelhausen"},
        {"code": "17914", "name": "Sonny Gelhausen"},
    ],
})

# === Gen 5 detail (page 38-40) ===
ENTRIES.append({
    "code": "11112",
    "name": "Edna Mae Frazee",
    "sex": "F",
    "born": "6 Sep 1921",
    "spouses": [{"name": "Charles E. Frantz", "born": "18 Jul 1917", "married": "20 May 1937",
                 "father": "Elizah F. Frantz", "mother": "Martha (Mollie) [Hoff] Frantz"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 38},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "111121", "name": "James Albert Frantz", "born": "24 Jan 1941"},
        {"code": "111122", "name": "Elina Edna Frantz", "born": "5 Feb 1947"},
        {"code": "111123", "name": "Charles Elmer Frantz", "born": "14 Oct 1951"},
    ],
})

ENTRIES.append({
    "code": "11121",
    "name": "William Carl Windell",
    "sex": "M",
    "born": "24 Nov 1911",
    "died": "9 Sep 1978",
    "buried": "Terra Alta Cemetery, WV",
    "spouses": [{"name": "Osa Freda Lewis", "father": "Clyde Lewis", "details": "Same as #13541 — daughter of Clyde D. Lewis."}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 38},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "111211", "name": "Joseph Harry Windell"},
        {"code": "111212", "name": "Jean Windell"},
        {"code": "111213", "name": "Charlotte Windell"},
        {"code": "111214", "name": "Bonnie Windell"},
    ],
})

ENTRIES.append({
    "code": "11211",
    "name": "Tressie Guthrie",
    "sex": "F",
    "born": "26 Nov 1870",
    "spouses": [{"name": "Notley Frankhouser"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 38},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "112111", "name": "Elizabeth J. Frankhouser"},
        {"code": "112112", "name": "Lucile Jane Frankhouser"},
    ],
})

ENTRIES.append({
    "code": "11222",
    "name": "Lena Ellen Trembly",
    "sex": "F",
    "born": "29 Apr 1896",
    "died": "30 Jun 1976",
    "spouses": [{"name": "Charles A. or B. Smith", "born": "18 Aug 1890", "died": "9 Apr 1972",
                 "father": "Jacob A. Smith", "mother": "Alice [Birch] Smith"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 38},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "112221", "name": "Richard A. Smith"},
        {"code": "112222", "name": "Betty Smith"},
        {"code": "112223", "name": "Patricia Ann Smith"},
    ],
})

ENTRIES.append({
    "code": "11243",
    "name": "Nellie Cupp",
    "sex": "F",
    "born": "23 Apr 1903",
    "died": "5 Mar 1976",
    "spouses": [{"name": "Bruce E. Dodge", "died": "16 Aug 1975",
                 "father": "Josha Dodge", "mother": "Berlinda [Teets] Dodge"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 38},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "112431", "name": "Donald Dodge"},
        {"code": "112432", "name": "Ronald Dodge"},
        {"code": "112433", "name": "Marion Dodge"},
        {"code": "112434", "name": "Dale Dodge"},
        {"code": "112435", "name": "Michael Dodge"},
    ],
})

ENTRIES.append({
    "code": "11312",
    "name": "Walter E. VanSickle",
    "sex": "M",
    "born": "24 Jun 1895",
    "died": "22 Jan 1979",
    "spouses": [{
        "name": "Grace Hewitt",
        "born": "20 Sep 1897",
        "married": "26 Apr 1922",
        "father": "Marcellus W. Hewitt",
        "mother": "Malinda E. Hewitt",
        "details": "Grace was a school teacher.",
    }],
    "occupation": "School teacher and postmaster at Hazelton, WV; ordained minister",
    "notes": "Elected to the ministry 6 Apr 1918 and to the Eldership in 1945 for the Church of the Brethren. They reared three children, their father was a brother to Grace.",
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 38},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "113121", "name": "Orley D. VanSickle", "born": "8 Mar 1930", "died": "8 Mar 1930", "flags": {"diedInInfancy": True}},
        {"code": "113122", "name": "Ersel R. Hewitt", "born": "6 Feb 1925", "died": "6 Oct 1982", "flags": {"adopted": True}},
        {"code": "113123", "name": "Jessie Hewitt", "flags": {"adopted": True}},
        {"code": "113124", "name": "Elsie Hewitt", "born": "15 Jul 1928", "flags": {"adopted": True}},
    ],
})

ENTRIES.append({
    "code": "11313",
    "name": "Rosa Virginia VanSickle",
    "sex": "F",
    "born": "9 Nov 1897",
    "died": "23 Jul 1967",
    "spouses": [{"name": "Everett Reckart", "father": "Worley Reckart", "mother": "Lula [Rodeheaver] Reckart"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 38},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "113131", "name": "Inez M. Burd", "born": "3 Sep 1928", "died": "11 Nov 1928", "flags": {"diedInInfancy": True}},
    ],
})

ENTRIES.append({
    "code": "11315",
    "name": "Quinter VanSickle",
    "sex": "M",
    "born": "14 Aug 1902",
    "died": "26 Apr 1931",
    "spouses": [{"name": "Mary Welch"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 39},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "113151", "name": "Lois Winnifred VanSickle"},
    ],
})

ENTRIES.append({
    "code": "11323",
    "name": "Eula Guthrie",
    "sex": "F",
    "born": "23 May",
    "spouses": [{"name": "Fyock"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 39},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "113231", "name": "Fyock child"},
    ],
})

ENTRIES.append({
    "code": "11343",
    "name": "David Guthrie VanSickle",
    "sex": "M",
    "born": "16 Dec 1911",
    "died": "18 Feb 1965",
    "buried": "Lancaster Rural Cemetery, Lancaster, NY",
    "spouses": [{"name": "Lucy Gore"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 39},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "113431", "name": "Rebecca VanSickle"},
        {"code": "113432", "name": "David VanSickle, Jr."},
        {"code": "113433", "name": "John R. VanSickle"},
    ],
})

ENTRIES.append({
    "code": "11351",
    "name": "Marian Spencer VanSickle",
    "sex": "F",
    "born": "8 Jul 1931",
    "spouses": [{"name": "Wallace Benton Nieman", "born": "30 Nov 1925", "married": "2 Jul 1947",
                 "father": "Alvy Wilson Nieman", "mother": "Mable Irene [Forman] Nieman"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 39},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "113511", "name": "Richard Warren Nieman", "born": "13 Feb 1948"},
        {"code": "113512", "name": "Deborah Jo Nieman", "born": "19 May 1950"},
    ],
})

ENTRIES.append({
    "code": "11361",
    "name": "Helen Lucilla Guthrie",
    "sex": "F",
    "born": "5 Aug 1909",
    "spouses": [{"name": "Melvin Slaubaugh", "born": "4 Jun 1903", "married": "17 May 1933",
                 "father": "John J. Slaubaugh", "mother": "Ora May [Fike] Slaubaugh"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 39},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "113611", "name": "Dale M. Slaubaugh", "born": "13 Sep 1935"},
        {"code": "113612", "name": "Terry Guthrie Slaubaugh", "born": "8 May 1938"},
    ],
})

ENTRIES.append({
    "code": "11362",
    "name": "Beatrice Mae Guthrie",
    "sex": "F",
    "born": "5 Oct 1911",
    "spouses": [{"name": "Revie Slaubaugh", "married": "1933",
                 "father": "John J. Slaubaugh", "mother": "Ora May [Fike] Slaubaugh"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 39},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "113621", "name": "Jean Slaubaugh"},
        {"code": "113622", "name": "Donald Ray Slaubaugh", "born": "3 Jan 1939"},
        {"code": "113623", "name": "Ruth Ann Slaubaugh"},
    ],
})

# === Gen 5 DeBerry detail (12241 handled above as bug fix) ===
ENTRIES.append({
    "code": "12242",
    "name": "Lucy Elizabeth DeBerry",
    "sex": "F",
    "born": "3 Sep 1910",
    "died": "26 Jun 1981",
    "spouses": [{"name": "James Edward Gerken", "born": "19 Feb 1900", "died": "17 Jun 1966", "married": "27 Apr 1943",
                 "father": "John Gerken", "mother": "Ida [Seargeant] Gerken"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 40},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "122421", "name": "Hugh Charles Gerken", "flags": {"stepChild": True}},
    ],
})

ENTRIES.append({
    "code": "12243",
    "name": "William Henry (Ted) DeBerry",
    "sex": "M",
    "born": "16 Jan 1912",
    "died": "14 Aug 1993",
    "spouses": [{"name": "Shirel Victoria Spiker", "born": "6 Jul 1918", "married": "16 Jan 1937",
                 "father": "Oliver Clark Spiker", "mother": "Laura [Guthrie] Spiker",
                 "details": "Same as #17134 — daughter of Oliver Clark Spiker (#1713)."}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 40},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "122431", "name": "Kermit Nelson DeBerry", "born": "6 Dec 1937"},
        {"code": "122432", "name": "Lois Nita DeBerry", "born": "4 Apr 1944"},
    ],
})

ENTRIES.append({
    "code": "12244",
    "name": "Junior Clark DeBerry",
    "sex": "M",
    "born": "24 Sep 1913",
    "died": "7 Sep 1989",
    "spouses": [
        {"name": "Virginia Alice Methemy", "born": "18 Aug 1917", "died": "19 Aug 1986",
         "father": "Oakey Methemy", "mother": "Ethel Mae [Smith] Methemy", "order": 1},
        {"name": "Mary Aldens Sisler DeWitt", "born": "24 Feb 1934", "father": "Harvey Sisler", "order": 2},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 40},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        # First marriage
        {"code": "122441", "name": "Thomas Eugene DeBerry", "born": "9 Nov 1935"},
        {"code": "122442", "name": "James Franklin DeBerry", "born": "11 Jan 1937"},
        {"code": "122443", "name": "Robert Dale DeBerry", "born": "4 Jul 1938"},
        {"code": "122444", "name": "Ethel Mae DeBerry", "born": "5 Jun 1940"},
        {"code": "122445", "name": "Patty Ann DeBerry", "born": "12 Sep 1941"},
        {"code": "122446", "name": "David Carl DeBerry", "born": "19 Oct 1944"},
        {"code": "122447", "name": "Terry Lee DeBerry", "born": "11 Apr 1948"},
        # Second marriage
        {"code": "122448", "name": "Ronald Junior DeBerry", "born": "6 Jul 1954"},
        {"code": "122449", "name": "Sandra Dianne DeBerry", "born": "12 Oct 1955"},
        {"code": "12244A", "name": "Michael Dean DeBerry", "born": "3 Nov 1956"},
        # Stepchildren
        {"code": "12244B", "name": "David Eugene DeWitt", "born": "3 Feb 1950", "flags": {"stepChild": True}},
        {"code": "12244C", "name": "Carolyn Sue DeWitt", "born": "15 Mar 1951", "flags": {"stepChild": True}},
    ],
})

ENTRIES.append({
    "code": "12247",
    "name": "James Oliver DeBerry",
    "sex": "M",
    "born": "24 Aug 1917",
    "spouses": [{"name": "Rosa Silvia Spiker", "born": "24 May 1917", "died": "23 Jul 1985", "married": "8 Oct 1938",
                 "father": "Jacob G. Spiker", "mother": "Mary M. [Faulkner] Spiker",
                 "details": "Same as #17113 — daughter of Jacob George Spiker (#1711)."}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 40},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "122471", "name": "Delbert Dwain DeBerry", "born": "14 Aug 1939"},
        {"code": "122472", "name": "Margaret Mae DeBerry", "born": "25 Oct 1940"},
        {"code": "122473", "name": "Marvin Glenn DeBerry", "born": "8 May 1942"},
        {"code": "122474", "name": "Judy Ann DeBerry", "born": "23 Aug 1943"},
        {"code": "122475", "name": "Gerald (Jerry) Wade DeBerry", "born": "29 Jul 1949"},
    ],
})

ENTRIES.append({
    "code": "12248",
    "name": "Mary Alice DeBerry",
    "sex": "F",
    "born": "25 Nov 1919",
    "spouses": [{"name": "Ebert Gilbert Hornick", "born": "24 Sep 1915", "died": "21 Jan 1982", "married": "15 Mar 1941",
                 "father": "Jessie Clay Hornick", "mother": "Willow Pearl Hornick"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 40},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "122481", "name": "Everett Dwight Wolfe", "born": "15 May 1936", "died": "9 Dec 1936", "flags": {"diedInInfancy": True}, "buried": "Mt. Moriah Cemetery, Valley Point, WV"},
        {"code": "122482", "name": "Jessie Allen Hornick", "born": "14 Apr 1943"},
    ],
})


# === Pages 41-45 vision pass (2026-06-07): gen 5 DeBerry + Deal + Feather + 132x ===
ENTRIES.append({
    "code": "12249",
    "name": "Arletta Lucille DeBerry",
    "sex": "F",
    "born": "11 Aug 1922",
    "spouses": [{"name": "Fernando (Fred)(Fritz) Bernabei", "born": "18 Feb 1913", "died": "26 Dec 1973", "married": "25 Aug 1949"}],
    "notes": "Adopted 30 Nov 1949 the children of Fritz and first wife Angelina Russo.",
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 41},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "122491", "name": "Lenna Italia Mary Bernabei", "born": "28 Jul 1941", "flags": {"adopted": True}},
        {"code": "122492", "name": "Janice Margaret Mae Bernabei", "born": "13 Jul 1943", "flags": {"adopted": True}},
        {"code": "122493", "name": "Arthur Umberto Charles Bernabei", "born": "31 Oct 1944", "flags": {"adopted": True}},
        {"code": "122494", "name": "Lorraine Jestina Arletta Bernabei", "born": "3 Jan 1946", "flags": {"adopted": True}},
    ],
})

ENTRIES.append({
    "code": "1224A",
    "name": "Albert Ray DeBerry",
    "sex": "M",
    "born": "8 Oct 1924",
    "died": "20 Nov 1968",
    "spouses": [{"name": "Lexie Jeanelle Cole", "born": "24 Feb 1927", "married": "1 Jun 1946"}],
    "notes": "Killed in the Farmington #9 Mine explosion 20 Nov 1968. His body was removed 12 Jan 1971.",
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 41},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1224A1", "name": "Roger DeVaughn DeBerry", "born": "13 Apr 1947"},
    ],
})

ENTRIES.append({
    "code": "12311",
    "name": "Laura Susan Deal",
    "sex": "F",
    "born": "28 Nov 1903",
    "died": "6 Apr 1956",
    "spouses": [{"name": "Joseph William Kelly", "born": "10 Sep 1896", "died": "13 Dec 1965", "married": "31 Jul 1931"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 41},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "123111", "name": "Jo Annabel Kelly", "born": "8 Jan 1930"},
    ],
})

ENTRIES.append({
    "code": "12312",
    "name": "Elmer Deal",
    "sex": "M",
    "spouses": [{"name": "Bertha Irene Buron"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 41},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "123121", "name": "Jacklyn Deal"},
        {"code": "123122", "name": "Judy Deal"},
    ],
})

ENTRIES.append({
    "code": "12322",
    "name": "Henrietta Hoffman",
    "sex": "F",
    "spouses": [{"name": "Lester Keefover"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 41},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "123221", "name": "Cecil Keefover"},
    ],
})

ENTRIES.append({
    "code": "12331",
    "name": "John Cornelius Deal",
    "sex": "M",
    "born": "10 Jul 1906",
    "died": "31 Oct 1958",
    "spouses": [{"name": "Laura Edith Stone", "born": "18 Feb 1907", "died": "1 Sep 1986", "married": "1 Nov 1930"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 41},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "123311", "name": "William Guy Deal", "born": "26 Nov 1931"},
        {"code": "123312", "name": "Bruce Earl Deal", "born": "22 Oct 1936"},
        {"code": "123313", "name": "Glenn Paul Deal", "born": "3 Aug 1941"},
        {"code": "123314", "name": "Dale Allen Deal", "born": "5 May 1943"},
        {"code": "123315", "name": "Everett Clyde Deal", "born": "28 Jun 1946"},
    ],
})

ENTRIES.append({
    "code": "12332",
    "name": "Edna Faye Deal",
    "sex": "F",
    "born": "19 Dec 1907",
    "died": "12 Jan 1955",
    "buried": "Shady Grove Cemetery, WV",
    "spouses": [{"name": "William Cyrus Shaffer", "born": "20 Mar 1906", "died": "28 Aug 1983", "married": "25 Nov 1925",
                 "buried": "Shady Grove Cemetery, WV"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 41},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "123321", "name": "Dorothy Irene Shaffer", "born": "21 Feb 1926"},
        {"code": "123322", "name": "Betty Jane Shaffer", "born": "16 Feb 1928"},
        {"code": "123323", "name": "Grace Pearl Shaffer", "born": "19 Oct 1930"},
        {"code": "123324", "name": "Mary Lou Shaffer", "born": "5 Nov 1933"},
        {"code": "123325", "name": "Chester Junior Shaffer", "born": "11 Mar 1935"},
        {"code": "123326", "name": "William Jackson Shaffer", "born": "22 Nov 1937"},
        {"code": "123327", "name": "Glenn Dale Shaffer", "born": "3 Feb 1943", "died": "3 Feb 1943", "flags": {"diedInInfancy": True}},
        {"code": "123328", "name": "Sharlett Shaffer", "born": "24 May 1944", "died": "3 Jun 1944", "flags": {"diedInInfancy": True}},
        {"code": "123329", "name": "Joyce Elaine Shaffer", "born": "14 Sep 1946"},
    ],
})

ENTRIES.append({
    "code": "12333",
    "name": "Carl Claude Deal",
    "sex": "M",
    "born": "5 May 1910",
    "died": "3 Oct 1981",
    "spouses": [{"name": "Alva Mildred Awman", "born": "2 Jul 1916", "married": "25 Sep 1937"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 41},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "123331", "name": "Charles Bruce Deal", "born": "1 Feb 1938", "died": "25 Jan 1956"},
    ],
})

ENTRIES.append({
    "code": "12334",
    "name": "Hazel Lucy Deal",
    "sex": "F",
    "born": "4 Nov 1912",
    "died": "21 Apr 1984",
    "spouses": [{"name": "Lester Chester Livengood", "born": "10 Aug 1906", "died": "18 Jul 1972"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 42},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "123341", "name": "Wilma Jean Livengood", "born": "1 Mar 1932"},
        {"code": "123342", "name": "Lester Ray Livengood", "born": "14 Jun 1935"},
        {"code": "123343", "name": "Dorothy Marie Livengood", "born": "15 May 1937"},
        {"code": "123344", "name": "Robert Glenn Livengood", "born": "15 Feb 1939"},
    ],
})

ENTRIES.append({
    "code": "12335",
    "name": "Ralph Paul Deal",
    "sex": "M",
    "born": "3 Oct 1914",
    "born_place": "Hazelton",
    "died": "20 Mar 1994",
    "spouses": [{"name": "Dorothy Lucille Seese", "born": "25 Feb 1917", "married": "Mar 1937"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 42},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "123351", "name": "Russell Ray Deal", "born": "18 Dec 1937"},
        {"code": "123352", "name": "Junior Glen Deal", "born": "6 Jun 1945"},
    ],
})

ENTRIES.append({
    "code": "12338",
    "name": "Ray Glenn Deal",
    "sex": "M",
    "born": "23 Jan 1922",
    "spouses": [{"name": "June Renee Kelly", "born": "26 Feb 1923", "married": "8 Aug 1946"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 42},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "123381", "name": "Paul Franklin Deal", "born": "30 May 1947"},
        {"code": "123382", "name": "Larry Guy Deal", "born": "17 Jun 1949"},
        {"code": "123383", "name": "Donald Perry Deal", "born": "5 Mar 1952"},
        {"code": "123384", "name": "Kay Marlene Deal", "born": "6 Dec 1958"},
        {"code": "123385", "name": "Mark Cecil Deal", "born": "8 Jun 1962"},
    ],
})

ENTRIES.append({
    "code": "12341",
    "name": "Gertrude Trembly",
    "sex": "F",
    "born": "12 Feb 1908",
    "died": "21 Aug 1987",
    "spouses": [
        {"name": "George E. Grogg", "married": "25 Oct 1927", "order": 1},
        {"name": "Alfred R. Sten", "married": "25 Jan 1946", "order": 2},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 42},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "123411", "name": "Carolyn", "flags": {"stepChild": True}},
    ],
})

ENTRIES.append({
    "code": "12342",
    "name": "Lillian Beatrice Tremble",
    "sex": "F",
    "born": "29 Mar 1912",
    "spouses": [{"name": "Leo Kotchek", "born": "9 May 1918", "married": "23 Jun 1946"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 42},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "123421", "name": "Cynthia Louise Kotchek", "born": "25 Aug 1947"},
        {"code": "123422", "name": "Patricia Lee Kotchek", "born": "9 Jun 1949"},
    ],
})

ENTRIES.append({
    "code": "12351",
    "name": "Dempsey Ernest DeBerry",
    "sex": "M",
    "born": "25 Sep 1904",
    "died": "20 Nov 1962",
    "spouses": [{"name": "Vadna Merle Sisler", "born": "5 Jun 1912", "died": "2 Oct 1984"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 42},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "123511", "name": "Lillian Ruth DeBerry", "born": "11 Jan 1936"},
        {"code": "123512", "name": "Janet Sue DeBerry"},
        {"code": "123513", "name": "Nancy Kay DeBerry"},
        {"code": "123514", "name": "Jack Dempsey DeBerry", "born": "4 Dec 1942"},
        {"code": "123515", "name": "Don Everett DeBerry", "born": "11 May 1946"},
        {"code": "123516", "name": "Karen Diane DeBerry"},
        {"code": "123517", "name": "Duane Chester DeBerry"},
        {"code": "123518", "name": "Rita Bevelyn DeBerry"},
    ],
})

ENTRIES.append({
    "code": "12352",
    "name": "Gilbert Preseon DeBerry",
    "sex": "M",
    "born": "13 Jun 1907",
    "died": "18 Aug 1968",
    "spouses": [{"name": "Violetta Loraw", "born": "8 Jun 1910", "married": "17 Oct 1931"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 42},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "123521", "name": "Ronald Prentice DeBerry", "born": "29 Sep 1932"},
    ],
})

ENTRIES.append({
    "code": "12361",
    "name": "Nellie Pauline Feather",
    "sex": "F",
    "born": "22 Sep 1907",
    "born_place": "Albright, WV",
    "spouses": [{"name": "Loren Dwight Wiles", "born": "10 Dec 1902", "born_place": "Aurora, WV", "married": "25 Jun 1927",
                 "married_place": "Borghman, WV"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 42},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "123611", "name": "Loren Dwight Wiles, Jr.", "born": "1 Jul 1928"},
        {"code": "123612", "name": "Elizabeth Rosalie Wiles", "born": "6 Jun 1933"},
        {"code": "123613", "name": "Harold Gene Wiles", "born": "17 Jan 1943", "born_place": "Albright, WV"},
    ],
})

ENTRIES.append({
    "code": "12363",
    "name": "Virgie Leda Feather",
    "sex": "F",
    "born": "25 Oct 1910",
    "born_place": "Albright, WV",
    "spouses": [{"name": "Loyal Dick Shirley", "born": "9 Mar 1909", "married": "25 Oct 1930", "married_place": "Oakland, MD"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 43},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "123631", "name": "Patricia Ann Shirley", "born": "22 Nov 1936"},
        {"code": "123632", "name": "Elizabeth Sue Shirley", "born": "14 Dec 1941"},
    ],
})

ENTRIES.append({
    "code": "12364",
    "name": "Rosalie Francine Feather",
    "sex": "F",
    "born": "23 Mar 1916",
    "born_place": "Albright, WV",
    "spouses": [{"name": "Samuel Edward Henry", "born": "5 Jan 1911", "married": "31 Dec 1938", "married_place": "Kingwood, WV"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 43},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "123641", "name": "William Edward Henry", "born": "19 Jul 1942"},
        {"code": "123642", "name": "Sharon Kay Henry", "born": "13 Dec 1946"},
    ],
})

ENTRIES.append({
    "code": "12365",
    "name": "Wilmeth Scott Feather",
    "sex": "M",
    "born": "24 Jun 1919",
    "born_place": "Albright, WV",
    "spouses": [{"name": "Maxine Alice Elliott", "born": "27 Apr 1922", "married": "11 Aug 1945", "married_place": "Hutton, MD"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 43},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "123651", "name": "Robert Lynn Feather", "born": "17 Dec 1945"},
        {"code": "123652", "name": "Mary Ann Feather", "born": "30 May 1947"},
        {"code": "123653", "name": "Ella Lee Feather", "born": "7 Sep 1949"},
        {"code": "123654", "name": "Linda Joy Feather", "born": "27 May 1951"},
    ],
})

ENTRIES.append({
    "code": "12366",
    "name": "Fred Lynn Feather",
    "sex": "M",
    "born": "23 Mar 1923",
    "born_place": "Albright, WV",
    "spouses": [{"name": "Mary Rebecca Keener", "born": "22 Oct 1922", "born_place": "Fairmont, WV"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 43},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "123661", "name": "Kathy Lynn Feather", "born": "6 Nov 1958"},
        {"code": "123662", "name": "Mark Lee Feather", "born": "5 Oct 1962"},
    ],
})

ENTRIES.append({
    "code": "12371",
    "name": "Kermit Walton Miller",
    "sex": "M",
    "born": "23 Aug 1911",
    "spouses": [{"name": "Lora Burhl Harned", "born": "30 Jul 1913", "married": "13 May 1939"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 43},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "123711", "name": "Jon Max Miller", "born": "16 Oct 1939"},
        {"code": "123712", "name": "Marvin Kay Miller", "born": "29 Apr 1945"},
        {"code": "123713", "name": "Marion Fay Miller", "born": "29 Apr 1945"},
    ],
})

ENTRIES.append({
    "code": "12372",
    "name": "Ruby Fern Miller",
    "sex": "F",
    "born": "5 Jul 1913",
    "spouses": [{"name": "James A. Romano", "born": "2 Jan 1914", "married": "16 Oct 1940"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 43},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "123721", "name": "Mary Romano"},
    ],
})

ENTRIES.append({
    "code": "12373",
    "name": "Emerson Scott Miller",
    "sex": "M",
    "born": "11 Jun 1918",
    "spouses": [{"name": "Louise Shaw", "born": "2 Nov 1921", "married": "22 Nov 1945"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 43},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "123731", "name": "Mary Elizabeth Miller"},
        {"code": "123732", "name": "Martha Sue Miller"},
    ],
})

ENTRIES.append({
    "code": "12381",
    "name": "Evelyn Fern Liston",
    "sex": "F",
    "born": "6 Sep 1918",
    "died": "29 Sep 1954",
    "spouses": [{"name": "Charles R. Addis", "born": "1903", "died": "1984"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 43},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "123811", "name": "Walter F. Addis", "born": "1936", "died": "1937", "flags": {"diedInInfancy": True}},
    ],
})

ENTRIES.append({
    "code": "12382",
    "name": "Ralph Waldo Liston",
    "sex": "M",
    "born": "6 Dec 1920",
    "spouses": [{"name": "Bessie Marie Nedrow", "born": "22 Dec 1919"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 43},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "123821", "name": "Judith Ann Liston"},
    ],
})

ENTRIES.append({
    "code": "12412",
    "name": "Blaine Messinger",
    "sex": "M",
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 44},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "124121", "name": "Donna Lee Messinger"},
    ],
})

ENTRIES.append({
    "code": "13212",
    "name": "Elwood Herbert Guthrie",
    "sex": "M",
    "born": "8 Sep 1916",
    "died": "25 Aug 1983",
    "spouses": [
        {"name": "Macie Mae Frazee", "died": "8 Dec 1982", "order": 1},
        {"name": "Florence Fike", "order": 2},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 44},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "132121", "name": "Mary Ann Guthrie", "born": "1937"},
        {"code": "132122", "name": "Judith Eileen (Judy) Guthrie", "born": "19 Dec 1954"},
    ],
})

ENTRIES.append({
    "code": "13213",
    "name": "Charles Ellis Guthrie",
    "sex": "M",
    "spouses": [{"name": "Delphine Fearer"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 44},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "132131", "name": "Kenneth Guthrie"},
        {"code": "132132", "name": "James Guthrie"},
        {"code": "132133", "name": "Frances Guthrie"},
        {"code": "132134", "name": "Ralph V. Guthrie", "born": "1960", "died": "14 Jul 1979"},
        {"code": "132135", "name": "Ernest Guthrie"},
    ],
})

ENTRIES.append({
    "code": "13214",
    "name": "Stanley Vernon Guthrie",
    "sex": "M",
    "born": "11 Sep 1920",
    "died": "29 May 1978",
    "buried": "Thomas Cemetery, Rt. 40, Markleysburg, PA",
    "spouses": [{"name": "Ruth I. Conaway"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 44},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "132141", "name": "Candice Rae Guthrie"},
    ],
})

ENTRIES.append({
    "code": "13215",
    "name": "Rose Guthrie",
    "sex": "F",
    "born": "18 Jun 1927",
    "died": "3 Feb 1996",
    "spouses": [{"name": "Raymond Myers", "died": "11 Apr 1984"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 44},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "132151", "name": "Ruth Myers"},
        {"code": "132152", "name": "Sandy Myers"},
        {"code": "132153", "name": "Raymond Myers"},
        {"code": "132154", "name": "Vickey Myers"},
        {"code": "132155", "name": "Ronald M. Myers", "born": "23 Dec 1953", "died": "16 Jun 1954", "flags": {"diedInInfancy": True}},
        {"code": "132156", "name": "Kieth Myers", "born": "1953"},
        {"code": "132157", "name": "Marlene Margaret Myers"},
        {"code": "132158", "name": "Shelly Myers"},
        {"code": "132159", "name": "Erick Myers"},
    ],
})

ENTRIES.append({
    "code": "13216",
    "name": "Ralph Harold Guthrie",
    "sex": "M",
    "born": "4 Jan 1933",
    "died": "27 Jul 1982",
    "buried": "Parnell Cemetery",
    "notes": "PDF says only 'Had Two Children'.",
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 44},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
})

ENTRIES.append({
    "code": "13217",
    "name": "Virginia Ruth Guthrie",
    "sex": "F",
    "born": "6 Oct 1939",
    "died": "27 Sep 1987",
    "spouses": [{"name": "Russell Ray Deal", "born": "18 Dec 1937", "details": "Same as #123351 — son of Ralph Paul Deal #12335."}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 44},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "132171", "name": "Debra Joyce Deal", "born": "27 Feb 1959"},
        {"code": "132172", "name": "Pamela Deal"},
        {"code": "132173", "name": "Randy Deal", "born": "7 Feb 1962"},
        {"code": "132174", "name": "Michael (Mike) Ray Deal", "born": "25 May 1963"},
    ],
})

ENTRIES.append({
    "code": "13218",
    "name": "Connie Ellen Guthrie",
    "sex": "F",
    "born": "1 Oct 1944",
    "spouses": [{"name": "Gary Ray Smith", "married": "12 Oct 1962", "details": "Same as #13C512 — son of Rena K. Guthrie (#13C5)."}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 44},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "132181", "name": "Gary Michael Smith"},
        {"code": "132182", "name": "Tamara Lynn Smith", "born": "24 Dec 1966"},
        {"code": "132183", "name": "Kimberly Ellen Smith", "born": "1 Nov 1969", "died": "2 Nov 1969", "flags": {"diedInInfancy": True}},
    ],
})

ENTRIES.append({
    "code": "13222",
    "name": "Donna Mae Guthrie",
    "sex": "F",
    "born": "6 Aug 1897",
    "died": "11 Mar 1995",
    "spouses": [{"name": "Greeley Emerson Strawser", "born": "24 Jun 1897", "died": "29 Oct 1963", "married": "20 Aug 1920"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 45},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "132221", "name": "Geraldine Rita Strawser", "born": "29 May 1927"},
    ],
})

ENTRIES.append({
    "code": "13223",
    "name": "Clarence Ray Guthrie",
    "sex": "M",
    "born": "16 Feb 1902",
    "died": "29 Jul 1971",
    "buried": "Centenary Cemetery",
    "spouses": [{"name": "Mary Mae Livengood", "born": "26 Mar 1906", "died": "7 May 1989", "buried": "Centenary Cemetery"}],
    "notes": "PDF header is 'CLARENCE RAY GUTHRIE' but appears as Charles Ray elsewhere; using PDF header.",
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 45},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "132231", "name": "Hagan L. Guthrie", "born": "27 Mar 1930"},
        {"code": "132232", "name": "Marlin Guthrie", "born": "20 Feb 1932"},
        {"code": "132233", "name": "Audrey Jean Guthrie", "born": "20 Dec 1937"},
        {"code": "132234", "name": "Wendell Ray Guthrie", "born": "21 Sep 1940"},
    ],
})

ENTRIES.append({
    "code": "13224",
    "name": "Edna Pauline Guthrie",
    "sex": "F",
    "born": "30 Jun 1914",
    "died": "14 Jan 1997",
    "spouses": [{"name": "John I. VanSickle", "born": "15 Aug 1912", "died": "4 Oct 1979"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 45},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "132241", "name": "Myron L. VanSickle", "born": "10 Jun 1941"},
        {"code": "132242", "name": "Mark J. VanSickle", "born": "29 Aug 1951"},
    ],
})

ENTRIES.append({
    "code": "13241",
    "name": "Nora May Trembly",
    "sex": "F",
    "born": "18 May 1892",
    "spouses": [{"name": "Clyde Epley", "married": "12 Oct 1912"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 45},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "132411", "name": "Clyde Epley, Jr."},
    ],
})

ENTRIES.append({
    "code": "13243",
    "name": "Nellie Clove Trembly",
    "sex": "F",
    "born": "14 Feb 1895",
    "spouses": [{"name": "Harold Wendell", "married": "16 Oct 1916"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 45},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "132431", "name": "Josephine Eleanor Wendell", "born": "8 Sep 1917"},
        {"code": "132432", "name": "Betty Wendell"},
    ],
})

ENTRIES.append({
    "code": "13261",
    "name": "Chester Dotson Lawson",
    "sex": "M",
    "born": "29 Sep 1903",
    "died": "27 Aug 1992",
    "spouses": [{"name": "Faye Evelyn Rodeheaver", "born": "9 Nov 1908", "married": "30 Jul 1927"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 45},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "132611", "name": "Donley Blaine Lawson", "born": "18 Mar 1928"},
        {"code": "132612", "name": "Gayle Owens Lawson", "born": "9 Oct 1930"},
        {"code": "132613", "name": "Wahneta Jean Lawson", "born": "11 Jun 1935"},
        {"code": "132614", "name": "Chester Kent Lawson", "born": "20 Nov 1949"},
    ],
})

ENTRIES.append({
    "code": "13262",
    "name": "Ralph H. Lawson",
    "sex": "M",
    "born": "26 Jan 1906",
    "spouses": [{"name": "Lillian Ryland", "died": "22 Jun 1996"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 45},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "132621", "name": "Iris Lawson", "flags": {"diedInInfancy": True}},
        {"code": "132622", "name": "Caroline Lawson", "born": "18 Nov 1941"},
        {"code": "132623", "name": "Greg Lawson", "born": "8 Aug 1944"},
        {"code": "132624", "name": "David Lawson", "born": "20 Nov 1947"},
    ],
})

ENTRIES.append({
    "code": "13263",
    "name": "Emma Evelyn Lawson",
    "sex": "F",
    "born": "13 Dec 1907",
    "spouses": [{"name": "John Howard Kelly", "born": "7 Nov 1909", "died": "26 Oct 1974"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 45},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "132631", "name": "Phyllis Joann Kelly", "born": "28 Nov 1950"},
    ],
})

ENTRIES.append({
    "code": "13264",
    "name": "Everett Paul Lawson",
    "sex": "M",
    "born": "17 Jul 1911",
    "spouses": [{"name": "Vivian Rosalie Reckart", "born": "15 May 1913"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 45},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "132641", "name": "Thomas Robert (Bobby) Lawson"},
        {"code": "132642", "name": "Jackson Paul Lawson", "born": "29 Oct 1934"},
    ],
})


# === Pages 46-50 vision pass (2026-06-07): gen 5/6 ===
ENTRIES.append({
    "code": "13265",
    "name": "Russell Ray Lawson",
    "sex": "M",
    "born": "23 Mar 1914",
    "died": "24 Feb 1975",
    "spouses": [{"name": "Freda M. Sisler", "died": "10 Apr 1979"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 46},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "132651", "name": "Marlon Lawson"},
        {"code": "132652", "name": "Garry E. Lawson"},
        {"code": "132653", "name": "Larry D. Lawson"},
    ],
})

ENTRIES.append({
    "code": "13267",
    "name": "Clarence S. Lawson",
    "sex": "M",
    "born": "22 Mar 1920",
    "spouses": [{"name": "Faye Teets"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 46},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "132671", "name": "Eva Kay Lawson", "born": "1 Oct 1947"},
        {"code": "132672", "name": "Janet Lawson"},
    ],
})

ENTRIES.append({
    "code": "13541",
    "name": "Osa Freda Lewis",
    "sex": "F",
    "born": "19 Nov 1915",
    "died": "23 Apr 1981",
    "spouses": [{"name": "William C. Windell", "born": "24 Nov 1911", "died": "9 Sep 1978", "details": "Same as #11121."}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 46},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
})

ENTRIES.append({
    "code": "13651",
    "name": "Dessie Alice Hauger",
    "sex": "F",
    "born": "5 May 1898",
    "died": "3 Mar 1983",
    "spouses": [{"name": "Frank McKinley Shafer", "born": "13 Jul 1897", "died": "27 Apr 1951", "married": "25 Nov 1916"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 46},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "136511", "name": "Alva Lester Shafer", "born": "26 Dec 1917"},
        {"code": "136512", "name": "Glenna Adra Shafer", "born": "24 Feb 1919"},
        {"code": "136513", "name": "Thelma Maxine Shafer", "born": "18 Dec 1920"},
        {"code": "136514", "name": "Herbert David Shafer", "born": "24 Feb 1922"},
        {"code": "136515", "name": "Fredy Junior Shafer", "born": "13 Mar 1924"},
        {"code": "136516", "name": "Paul Eugene Shafer", "born": "26 Feb 1926"},
        {"code": "136517", "name": "Ada Mae Shafer", "born": "18 Apr 1929"},
        {"code": "136518", "name": "Walter Franklin Shafer", "born": "27 Mar 1931"},
        {"code": "136519", "name": "Lou Anna Shafer", "born": "19 Oct 1932"},
        {"code": "13651A", "name": "Olaf Hugh (Buddy) Shafer", "born": "22 May 1934"},
        {"code": "13651B", "name": "Martha Elizabeth Shafer", "born": "7 Sep 1936"},
        {"code": "13651C", "name": "Russell Lee Shafer", "born": "7 Sep 1939"},
    ],
})

ENTRIES.append({
    "code": "13654",
    "name": "Cora Hauger",
    "sex": "F",
    "born": "3 Nov 1899",
    "died": "25 Jun 1978",
    "spouses": [{"name": "Oakey Reckart", "born": "15 Jan 1894", "died": "22 Apr 1978"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 46},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "136541", "name": "Darwin Reckart"},
        {"code": "136542", "name": "Delbert Reckart"},
        {"code": "136543", "name": "Dailey Reckart"},
        {"code": "136544", "name": "Donald Reckart"},
        {"code": "136545", "name": "Herbert Reckart"},
        {"code": "136546", "name": "Harland Reckart"},
        {"code": "136547", "name": "Floyd Reckart"},
        {"code": "136548", "name": "Wayne Reckart"},
        {"code": "136549", "name": "Playford Reckart"},
    ],
})

ENTRIES.append({
    "code": "13661",
    "name": "Ethel Ficky",
    "sex": "F",
    "spouses": [{"name": "Professor Ward", "died": "1955"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 46},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "136611", "name": "Daughter"},
    ],
})

ENTRIES.append({
    "code": "13821",
    "name": "Edith M. Teets",
    "sex": "F",
    "born": "19 Jan 1898",
    "died": "9 Jan 1992",
    "spouses": [{"name": "Paul R. Wilburn"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 47},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "138211", "name": "Wayne Wilburn", "born": "2 Feb 1917"},
        {"code": "138212", "name": "Eleanor Virginia Wilburn"},
    ],
})

ENTRIES.append({
    "code": "13823",
    "name": "Cora Teets",
    "sex": "F",
    "born": "1902",
    "died": "1957",
    "spouses": [{"name": "Russell Bucklew"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 47},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "138231", "name": "Maxine Bucklew"},
        {"code": "138232", "name": "Ruby Bucklew"},
        {"code": "138233", "name": "Eugene Bucklew"},
        {"code": "138234", "name": "Child"},
        {"code": "138235", "name": "Edna Bucklew"},
    ],
})

ENTRIES.append({
    "code": "13826",
    "name": "Rosalee Teets",
    "sex": "F",
    "born": "Sep 1917",
    "died": "1967",
    "spouses": [{"name": "Charles Cole", "born": "1907"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 47},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "138261", "name": "Junior Cole"},
        {"code": "138262", "name": "Mary Jean Cole"},
        {"code": "138263", "name": "Shirley Cole"},
        {"code": "138264", "name": "Patty Cole"},
    ],
})

ENTRIES.append({
    "code": "13827",
    "name": "Rollin Adair Teets",
    "sex": "M",
    "born": "26 Mar 1919",
    "died": "7 Jan 1981",
    "spouses": [
        {"name": "Eleanor Hinbaugh", "order": 1},
        {"name": "Dorothy Jane Smith", "born": "1 Jan 1927", "married": "24 Apr 1945", "order": 2},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 47},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "138271", "name": "Virginia Ellen Teets", "born": "23 Jan 1940", "died": "26 Jan 1940", "flags": {"diedInInfancy": True}},
        {"code": "138272", "name": "Stanley Teets", "born": "29 Aug 1943", "died": "27 Mar 1944", "flags": {"diedInInfancy": True}},
        {"code": "138273", "name": "Johnny Teets", "born": "Sep 1944"},
        {"code": "138274", "name": "Clarence Cecil Teets", "born": "24 Oct 1947"},
        {"code": "138275", "name": "Rollin Eugene Teets", "born": "16 Jan 1951"},
        {"code": "138276", "name": "Allen Ray Teets", "born": "7 Feb 1960"},
    ],
})

ENTRIES.append({
    "code": "13842",
    "name": "Arthur Paul Teets",
    "sex": "M",
    "born": "7 Dec 1920",
    "died": "21 Jun 1966",
    "buried": "Sugar Valley Cemetery",
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 47},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "138421", "name": "Michael Teets"},
        {"code": "138422", "name": "Ray Teets"},
        {"code": "138423", "name": "Timothy Teets"},
        {"code": "138424", "name": "Linda Teets"},
        {"code": "138425", "name": "Janice Teets"},
        {"code": "138426", "name": "Ada Teets"},
    ],
})

ENTRIES.append({
    "code": "13844",
    "name": "Florence F. (Flora) Teets",
    "sex": "F",
    "born": "31 Dec 1909",
    "died": "31 Mar 1981",
    "spouses": [{"name": "Artie F. Johnson", "born": "1905"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 47},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "138441", "name": "Howard (Buss) Johnson"},
        {"code": "138442", "name": "Everett (Chum) Johnson"},
        {"code": "138443", "name": "Don Johnson"},
        {"code": "138444", "name": "Burley Johnson"},
        {"code": "138445", "name": "Shirley Johnson"},
    ],
})

ENTRIES.append({
    "code": "13862",
    "name": "Cora Uphold",
    "sex": "F",
    "born": "1 Jan 1904",
    "died": "18 Sep 1978",
    "spouses": [{"name": "Troy B. DeWitt", "died": "1976"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 48},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "138621", "name": "Donald DeWitt"},
        {"code": "138622", "name": "Otis DeWitt"},
        {"code": "138623", "name": "Marie DeWitt"},
        {"code": "138624", "name": "Dolly DeWitt"},
        {"code": "138625", "name": "Betty DeWitt"},
        {"code": "138626", "name": "Norma DeWitt"},
    ],
})

ENTRIES.append({
    "code": "13863",
    "name": "Bessie Uphold",
    "sex": "F",
    "spouses": [{"name": "Arthur Casteel"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 48},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "138631", "name": "Fred Uphold"},
        {"code": "138632", "name": "Bud Casteel"},
        {"code": "138633", "name": "Chum Casteel"},
        {"code": "138634", "name": "Junior Casteel"},
        {"code": "138635", "name": "Ger Casteel"},
    ],
})

ENTRIES.append({
    "code": "13864",
    "name": "Edna Uphold",
    "sex": "F",
    "born": "1906",
    "spouses": [{"name": "Dewey Rodeheaver", "born": "11 Dec 1889", "died": "18 Aug 1972", "married": "28 Feb 1923"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 48},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "138641", "name": "Vernon Rodeheaver"},
        {"code": "138642", "name": "Mildred Rodeheaver"},
    ],
})

ENTRIES.append({
    "code": "13865",
    "name": "Grace Uphold",
    "sex": "F",
    "spouses": [
        {"name": "Chancy Rodeheaver", "order": 1},
        {"name": "Allen Wilson", "order": 2},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 48},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "138651", "name": "Ruth Rodeheaver"},
        {"code": "138652", "name": "Ramon Richard Rodeheaver"},
        {"code": "138653", "name": "Willie Wilson"},
        {"code": "138654", "name": "Joe Wilson"},
    ],
})

ENTRIES.append({
    "code": "13866",
    "name": "Icie Myrtle Uphold",
    "sex": "F",
    "spouses": [
        {"name": "Jack Thomas", "order": 1},
        {"name": "Glenn Humberson", "order": 2},
        {"name": "Junior Gibson", "died": "1976", "order": 3},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 48},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "138661", "name": "Helen Thomas"},
        {"code": "138662", "name": "Lucilla Thomas"},
        {"code": "138663", "name": "Paul Thomas"},
    ],
})

ENTRIES.append({
    "code": "13B21",
    "name": "Lola Violet Murphy",
    "sex": "F",
    "born": "21 Feb 1905",
    "died": "11 May 1979",
    "spouses": [{"name": "Joseph Seamon", "born": "19 May 1891", "died": "Jan 1979", "married": "25 Jul 1921"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 48},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "13B211", "name": "Freda Agnes Seamon", "born": "10 Apr 1923"},
        {"code": "13B212", "name": "Charles Joseph Seamon", "born": "18 Mar 1925"},
        {"code": "13B213", "name": "Mildred Elizabeth Seamon", "born": "11 Feb 1929"},
        {"code": "13B214", "name": "Oliver George Seamon", "born": "15 Dec 1930"},
        {"code": "13B215", "name": "Carl Steven Seamon", "born": "4 Mar 1933"},
        {"code": "13B216", "name": "Edward Michael Seamon", "born": "13 Jul 1938", "died": "1958"},
        {"code": "13B217", "name": "Larry Donald Seamon", "born": "31 Jul 1945"},
    ],
})

ENTRIES.append({
    "code": "13C51",
    "name": "Ray Smith",
    "sex": "M",
    "born": "10 Jun 1918",
    "spouses": [{"name": "Ellen Sisler", "born": "31 May 1920"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 48},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "13C511", "name": "Darwin Wayne Smith", "born": "17 May 1943"},
        {"code": "13C512", "name": "Gary Ray Smith", "born": "12 Jan 1945"},
        {"code": "13C513", "name": "James Ward Smith", "born": "14 Mar 1949"},
        {"code": "13C514", "name": "Stanley Aldren Smith", "born": "3 Nov 1955"},
        {"code": "13C515", "name": "Connie Smith", "born": "10 Feb 1959"},
    ],
})

ENTRIES.append({
    "code": "13C53",
    "name": "Janice Smith",
    "sex": "F",
    "born": "30 Jul 1939",
    "died": "21 May 1975",
    "spouses": [{"name": "Dean Bishoff"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 49},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "13C531", "name": "Bradley Bishoff"},
        {"code": "13C532", "name": "Katherine Bishoff"},
    ],
})

ENTRIES.append({
    "code": "13F12",
    "name": "Junior Walter Guthrie",
    "sex": "M",
    "born": "16 Jun 1922",
    "died": "26 Jan 1994",
    "spouses": [{"name": "Gladys Marie Durst"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 49},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "13F121", "name": "Ray Guthrie"},
        {"code": "13F122", "name": "Linda Guthrie"},
        {"code": "13F123", "name": "Marine Guthrie", "flags": {"stepChild": True}},
        {"code": "13F124", "name": "Marvin Durst", "flags": {"stepChild": True}},
    ],
})

ENTRIES.append({
    "code": "13F71",
    "name": "Betty Guthrie",
    "sex": "F",
    "born": "8 Apr 1932",
    "spouses": [
        {"name": "Raymond Rishel", "born": "3 Mar 1931", "married": "Mar 1949", "order": 1},
        {"name": "Harold S. (Pee Wee) Thomas", "born": "17 Jul 1920", "died": "28 Jun 1992", "married": "15 May 1954", "order": 2},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 49},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "13F711", "name": "Linda Ray Rishel", "born": "11 Mar 1950"},
        {"code": "13F712", "name": "Ward Ray Thomas", "born": "2 Sep 1954"},
        {"code": "13F713", "name": "Crystal Lou Thomas", "born": "8 Dec 1961"},
        {"code": "13F714", "name": "Tammy Thomas", "born": "28 Mar 1963"},
        {"code": "13F715", "name": "Henry Thomas", "born": "20 Mar 1969"},
    ],
})

ENTRIES.append({
    "code": "13F72",
    "name": "Mary Jean Guthrie",
    "sex": "F",
    "born": "29 Aug 1934",
    "spouses": [{"name": "Martin Luther Cupp", "born": "9 May 1918", "married": "9 May 1953", "details": "Same as #A456."}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 49},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "13F721", "name": "Martin Edward Cupp", "born": "30 Dec 1953"},
        {"code": "13F722", "name": "Roger Lee Cupp", "born": "13 Mar 1955"},
        {"code": "13F723", "name": "James Melvin Cupp", "born": "13 Oct 1957"},
        {"code": "13F724", "name": "Marvin Dale Cupp", "born": "18 Dec 1959"},
        {"code": "13F725", "name": "Charles Wesley Cupp", "born": "13 Jul 1961"},
        {"code": "13F726", "name": "Richard Glenn Cupp", "born": "17 Sep 1963"},
        {"code": "13F727", "name": "Sharon Louise Cupp", "born": "12 Dec 1965"},
    ],
})

ENTRIES.append({
    "code": "13F73",
    "name": "Walter Ray Guthrie",
    "sex": "M",
    "born": "26 Feb 1937",
    "died": "26 May 1990",
    "spouses": [{"name": "Shirley Jean Knabenshoe", "born": "27 Jan 1947"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 49},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "13F731", "name": "Mary Jane Guthrie", "born": "19 Jun 1966"},
        {"code": "13F732", "name": "Walter Ray Guthrie, Jr.", "born": "13 Jun 1968"},
    ],
})

ENTRIES.append({
    "code": "13F74",
    "name": "Alice Guthrie",
    "sex": "F",
    "born": "24 Oct 1939",
    "spouses": [{"name": "Franklin Richard Thomas", "born": "11 Mar 1933", "details": "Same as #14474."}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 49},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "13F741", "name": "Anna Pearl Thomas", "born": "5 May 1958"},
        {"code": "13F742", "name": "James Franklin Thomas", "born": "21 Jun 1960"},
        {"code": "13F743", "name": "Howard Dale Thomas", "born": "2 Jul 1966"},
    ],
})

ENTRIES.append({
    "code": "13F75",
    "name": "Ethel Jane Guthrie",
    "sex": "F",
    "born": "24 Sep 1941",
    "died": "1 Aug 1975",
    "spouses": [{"name": "Troy Everey Rosier"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 50},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "13F751", "name": "Patricia Ann Rosier", "born": "16 Apr 1959"},
        {"code": "13F752", "name": "Peggy Sue Rosier", "born": "2 Feb 1962"},
    ],
})

ENTRIES.append({
    "code": "13F76",
    "name": "Juanita Mae Guthrie",
    "sex": "F",
    "born": "16 May 1944",
    "spouses": [{"name": "Howard K. Pratt, Jr."}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 50},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "13F761", "name": "Lee Burdette Pratt", "born": "20 Jun 1962"},
    ],
})

ENTRIES.append({
    "code": "13F77",
    "name": "Judy Marie Guthrie",
    "sex": "F",
    "born": "15 Aug 1946",
    "spouses": [{"name": "Roger Lynn Hoffman", "born": "27 Jul 1942"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 50},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "13F771", "name": "Judith Ann Hoffman", "born": "9 Jan 1964"},
        {"code": "13F772", "name": "Roger Lynn Hoffman II", "born": "28 May 1967"},
        {"code": "13F773", "name": "Rebecca Jean Hoffman", "born": "20 Oct 1973"},
    ],
})

ENTRIES.append({
    "code": "13F81",
    "name": "Macie May Guthrie",
    "sex": "F",
    "born": "28 Aug 1944",
    "spouses": [{"name": "Fred Lawless"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 50},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "13F811", "name": "Fred Lawless", "born": "20 Dec 1964"},
        {"code": "13F812", "name": "Vince Lawless", "born": "10 Mar 1966"},
        {"code": "13F813", "name": "Kathy Michelle Lawless", "born": "13 Aug 1967", "died": "31 Aug 1967", "flags": {"diedInInfancy": True}},
    ],
})

ENTRIES.append({
    "code": "13F82",
    "name": "Ezra Grant Guthrie",
    "sex": "M",
    "born": "19 Dec 1945",
    "spouses": [
        {"name": "Carol Heady", "order": 1},
        {"name": "Mary Breland", "order": 2},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 50},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "13F821", "name": "Michael Guthrie"},
        {"code": "13F822", "name": "Andrew Guthrie"},
        {"code": "13F823", "name": "Lesley Ann Guthrie", "born": "1 Apr 1974"},
        {"code": "13F824", "name": "Ezra Grant Guthrie, Jr.", "born": "7 Aug 1975", "died": "3 Nov 1975", "flags": {"diedInInfancy": True}},
        {"code": "13F825", "name": "Janice Lynn Guthrie", "born": "30 Jan 1977"},
        {"code": "13F826", "name": "Elizabeth Ann Guthrie", "born": "11 Sep 1982"},
    ],
})

ENTRIES.append({
    "code": "13F83",
    "name": "Helen Marie Guthrie",
    "sex": "F",
    "born": "6 Oct 1947",
    "spouses": [{"name": "Robert Sparenberg"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 50},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "13F831", "name": "Mary Sparenberg"},
        {"code": "13F832", "name": "Joseph Sparenberg"},
        {"code": "13F833", "name": "Faye Sparenberg"},
        {"code": "13F834", "name": "Rita Sparenberg"},
        {"code": "13F835", "name": "George Sparenberg"},
    ],
})

ENTRIES.append({
    "code": "13F84",
    "name": "Walter Herbert Guthrie",
    "sex": "M",
    "born": "8 Mar 1950",
    "spouses": [{"name": "Bluietta Cornellue"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 50},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "13F841", "name": "Walter John Guthrie", "born": "Sep 1988"},
    ],
})

ENTRIES.append({
    "code": "13F85",
    "name": "Catherine Guthrie",
    "sex": "F",
    "born": "30 Jul 1951",
    "spouses": [{"name": "Robert Taylor"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 50},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "13F851", "name": "Darlene Taylor"},
    ],
})

ENTRIES.append({
    "code": "13F87",
    "name": "Dorothy Elaine Guthrie",
    "sex": "F",
    "born": "16 Apr 1956",
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 50},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "13F871", "name": "Melissa"},
        {"code": "13F872", "name": "Germainne"},
    ],
})

ENTRIES.append({
    "code": "13F89",
    "name": "Cora Rose Guthrie",
    "sex": "F",
    "born": "7 May 1960",
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 50},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "13F891", "name": "Robert Lee Ault", "born": "23 Aug 1976"},
        {"code": "13F892", "name": "Walter Harry Henning", "born": "12 May 1982"},
    ],
})


# === Pages 51-55 vision pass (2026-06-07): gen 6 13F + 14x gen 5 ===
ENTRIES.append({
    "code": "13F8A",
    "name": "Mary Maude Guthrie",
    "sex": "F",
    "born": "21 Feb 1962",
    "spouses": [{"name": "Fred Poling"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 51},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "13F8A1", "name": "Anna Marie Poling", "born": "12 Nov 1980"},
        {"code": "13F8A2", "name": "Jason Allen Poling", "born": "23 Mar 1982"},
        {"code": "13F8A3", "name": "Toyna Renue Poling", "born": "9 Feb 1984"},
    ],
})

ENTRIES.append({
    "code": "13FB1",
    "name": "Barbara Dennis",
    "sex": "F",
    "flags": {"adopted": True},
    "spouses": [{"name": "Ronald Rosenberger"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 51},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "13FB11", "name": "Sandy Rosenberger"},
        {"code": "13FB12", "name": "Jennie Rosenberger"},
    ],
})

ENTRIES.append({
    "code": "13FD2",
    "name": "Shirley Guthrie",
    "sex": "F",
    "spouses": [{"name": "Marvin Silbaugh"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 51},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "13FD21", "name": "Tammy Silbaugh", "born": "9 Sep 1961"},
    ],
})

ENTRIES.append({
    "code": "13FE1",
    "name": "Earl Richard Noss, Jr.",
    "sex": "M",
    "born": "16 Oct 1933",
    "spouses": [{"name": "Jeanetta Ann Ringer", "born": "13 May 1937", "married": "25 May 1957"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 51},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "13FE11", "name": "Kenneth Richard Noss", "born": "14 Jan 1959"},
        {"code": "13FE12", "name": "David Alan Noss", "born": "5 Sep 1962"},
        {"code": "13FE13", "name": "Joy Ann Noss", "born": "16 Sep 1963"},
    ],
})

ENTRIES.append({
    "code": "13FE2",
    "name": "Noami Virginia Noss",
    "sex": "F",
    "born": "19 Sep 1935",
    "spouses": [{"name": "Lloyd Dwight Ringer", "born": "9 Jul 1934", "married": "10 Oct 1953"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 51},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "13FE21", "name": "Carolyn Sue Ringer", "born": "14 Feb 1954"},
        {"code": "13FE22", "name": "Linda Diana Ringer", "born": "5 Feb 1957"},
        {"code": "13FE23", "name": "Sandra Kay Ringer", "born": "19 Mar 1965", "died": "17 Nov 1968", "flags": {"diedInInfancy": True}},
    ],
})

ENTRIES.append({
    "code": "13FE3",
    "name": "John Frederick Noss",
    "sex": "M",
    "born": "20 Apr 1939",
    "spouses": [{"name": "Kay Marie Clark", "born": "30 Mar 1945"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 51},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "13FE31", "name": "Stephen Kent Noss", "born": "13 Aug 1970"},
        {"code": "13FE32", "name": "Aaron Neal Noss", "born": "26 Feb 1974"},
    ],
})

ENTRIES.append({
    "code": "13FE4",
    "name": "Wayne E. Noss",
    "sex": "M",
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 51},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "13FE41", "name": "Daughter", "born": "23 Jul 1963"},
    ],
})

ENTRIES.append({
    "code": "13FE6",
    "name": "Shirley Noss",
    "sex": "F",
    "spouses": [{"name": "Harry Wayne Evans"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 51},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "13FE61", "name": "Harry Wayne (Chipper) Evans"},
        {"code": "13FE62", "name": "Debbie Evans"},
        {"code": "13FE63", "name": "Randy Evans"},
    ],
})

ENTRIES.append({
    "code": "14151",
    "name": "Beryl Uphold",
    "sex": "F",
    "born": "15 Nov 1908",
    "spouses": [{"name": "Clyde L. Anderson", "born": "20 Feb 1911", "died": "6 Apr 1973", "married": "6 Oct 1934"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 51},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "141511", "name": "Janet P. Anderson", "born": "4 May 1935"},
        {"code": "141512", "name": "Thomas J. Anderson", "born": "25 Apr 1936"},
        {"code": "141513", "name": "Clyde Lloyd Anderson", "born": "11 Aug 1937"},
        {"code": "141514", "name": "Charles Robert Anderson", "born": "8 Jan 1939"},
    ],
})

ENTRIES.append({
    "code": "14152",
    "name": "Helen Clarice Uphold",
    "sex": "F",
    "born": "24 May 1910",
    "spouses": [{"name": "Leo Frye Caldwell", "born": "3 Apr 1911", "married": "28 Jun 1937"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 52},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "141521", "name": "Deborah Lee Caldwell", "born": "24 Dec 1947"},
    ],
})

ENTRIES.append({
    "code": "14153",
    "name": "Donald Dale Uphold",
    "sex": "M",
    "born": "27 Jul 1913",
    "died": "15 Feb 1954",
    "spouses": [{"name": "Donetta P. Drennon", "born": "16 Aug 1911", "died": "21 Jul 1960"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 52},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "141531", "name": "Ronald D. Uphold", "born": "22 Sep 1938"},
        {"code": "141532", "name": "Donetta Faye Uphold", "born": "16 Dec 1943"},
    ],
})

ENTRIES.append({
    "code": "14154",
    "name": "Dorothy E. Uphold",
    "sex": "F",
    "born": "7 Oct 1915",
    "spouses": [{"name": "Robert E. Jones", "born": "16 Jul 1911", "died": "10 Sep 1957", "married": "12 Jun 1938"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 52},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "141541", "name": "Robert E. Jones, Jr.", "born": "4 Apr 1940"},
        {"code": "141542", "name": "Cholly Rae Jones", "born": "18 Feb 1946"},
    ],
})

ENTRIES.append({
    "code": "14155",
    "name": "Charles Ray Uphold",
    "sex": "M",
    "born": "3 Jul 1923",
    "spouses": [{"name": "Myrtle John", "born": "21 May 1924", "married": "18 Jan 1947"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 52},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "141551", "name": "Connie Rae Uphold", "born": "26 Jun 1951"},
        {"code": "141552", "name": "Bonnie Lynn Uphold", "born": "20 Feb 1957"},
    ],
})

ENTRIES.append({
    "code": "14161",
    "name": "Agnes Winnofred Uphold",
    "sex": "F",
    "born": "17 Feb 1917",
    "died": "8 May 1988",
    "spouses": [{"name": "Manuel Bankhead", "born": "20 Dec 1917", "died": "21 Oct 1971", "married": "3 Dec 1939"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 52},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "141611", "name": "Marvin Ray Bankhead", "born": "8 Jul 1940"},
        {"code": "141612", "name": "Lawson Lee Bankhead", "born": "16 Jul 1941"},
        {"code": "141613", "name": "Shirley Leona Bankhead", "born": "19 Oct 1942"},
        {"code": "141614", "name": "Geraldine Patrica Bankhead", "born": "9 May 1944"},
        {"code": "141615", "name": "Galend Manuel Bankhead", "born": "21 Sep 1948"},
        {"code": "141616", "name": "Melvin Jerold Bankhead", "born": "10 Apr 1950"},
        {"code": "141617", "name": "Stanley Ray Bankhead", "born": "3 Jan 1952"},
        {"code": "141618", "name": "David Blaine Bankhead", "born": "18 Mar 1953"},
        {"code": "141619", "name": "Edna Diane Bankhead", "born": "19 Sep 1955"},
        {"code": "14161A", "name": "Ruby Elain Bankhead", "born": "16 Oct 1956", "died": "16 Oct 1956", "flags": {"diedInInfancy": True}},
        {"code": "14161B", "name": "David Anthony Bankhead", "born": "23 Feb 1959", "died": "23 Feb 1959", "flags": {"diedInInfancy": True}},
    ],
})

ENTRIES.append({
    "code": "14181",
    "name": "Elizabeth Matilda Turner",
    "sex": "F",
    "born": "19 Aug 1912",
    "spouses": [{"name": "Theodore Moats"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 52},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "141811", "name": "Velma Elaine Moats", "born": "8 Jun 1929"},
        {"code": "141812", "name": "Daisy Geraldene Moats", "born": "3 Sep 1934"},
        {"code": "141813", "name": "Shirley Mae Moats", "born": "3 Jul 1936"},
        {"code": "141814", "name": "William Harold Moats", "born": "8 Oct 1939"},
        {"code": "141815", "name": "Dortha Marlene Moats", "born": "18 Nov 1941"},
        {"code": "141816", "name": "Beverly Charlene Moats", "born": "12 Sep"},
    ],
})

ENTRIES.append({
    "code": "14183",
    "name": "Sarapto Mari Turner",
    "sex": "F",
    "born": "8 Apr 1919",
    "spouses": [{"name": "William Hileman"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 53},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "141831", "name": "Vernon William Hileman", "born": "21 Feb 1938"},
        {"code": "141832", "name": "Wendell Philip Hileman", "born": "18 Oct 1945"},
        {"code": "141833", "name": "Carolyn June Hileman", "born": "11 Jun 1947"},
        {"code": "141834", "name": "Linda Lou Hileman", "born": "7 Mar 1954"},
    ],
})

ENTRIES.append({
    "code": "14186",
    "name": "Kenneth George Turner",
    "sex": "M",
    "born": "30 Jul 1929",
    "spouses": [{"name": "Ruby Hartman"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 53},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "141861", "name": "Kenneth Mitchell Turner", "born": "1 Apr 1949"},
    ],
})

ENTRIES.append({
    "code": "14252",
    "name": "Edna Grace Guthrie",
    "sex": "F",
    "born": "23 Apr 1912",
    "spouses": [{"name": "Earl Jackson Nicola", "born": "26 Sep 1909", "married": "8 Feb 1930", "details": "Same as #16312."}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 53},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "142521", "name": "Mary Maxine Nicola", "born": "3 Aug 1930", "died": "2 Mar 1931", "flags": {"diedInInfancy": True}},
        {"code": "142522", "name": "Martha Marie Nicola", "born": "3 Aug 1930", "died": "3 Aug 1930", "flags": {"diedInInfancy": True}},
        {"code": "142523", "name": "Robert Eugene Nicola", "born": "26 Mar 1934"},
        {"code": "142524", "name": "Dorothy Jean Nicola", "born": "6 Oct 1937"},
    ],
})

ENTRIES.append({
    "code": "14281",
    "name": "James Franklin Sines",
    "sex": "M",
    "born": "18 Oct 1921",
    "spouses": [
        {"name": "Dorothy Leasure", "married": "15 Feb 1941", "order": 1},
        {"name": "Kathrine McGarildy", "order": 2},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 53},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "142811", "name": "James Franklin Sines, Jr."},
        {"code": "142812", "name": "Barbara Sines"},
        {"code": "142813", "name": "John Sines"},
        {"code": "142814", "name": "Delbert Sines"},
        {"code": "142815", "name": "Donald Sines"},
        {"code": "142816", "name": "Carol Sue Sines"},
        {"code": "142817", "name": "Linda Sines"},
        {"code": "142818", "name": "Pat Sines"},
    ],
})

ENTRIES.append({
    "code": "14282",
    "name": "Paul Sines",
    "sex": "M",
    "born": "7 Dec 1923",
    "spouses": [{"name": "Pauline Grace Moyers", "born": "15 Feb 1927", "died": "23 Jun 1981", "married": "20 Sep 1953", "details": "Same as #17273."}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 53},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "142821", "name": "Catherine Louise Sines", "born": "28 Feb 1954"},
        {"code": "142822", "name": "Wendy Gay Sines", "born": "13 Feb 1963"},
    ],
})

ENTRIES.append({
    "code": "14284",
    "name": "Robert Jackson Sines",
    "sex": "M",
    "born": "1 Jun 1928",
    "died": "22 Feb 1989",
    "spouses": [{"name": "Dutch Janet Smidley"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 53},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "142841", "name": "Sandy Sines"},
        {"code": "142842", "name": "Mary Ann Sines"},
        {"code": "142843", "name": "Robert Sines"},
        {"code": "142844", "name": "James Sines"},
    ],
})

ENTRIES.append({
    "code": "14286",
    "name": "Ethel Mae Sines",
    "sex": "F",
    "born": "8 Sep 1931",
    "spouses": [
        {"name": "Harold Rosenberger", "married": "16 Oct 1948", "order": 1},
        {"name": "Calvin C. McDonald", "married": "28 Jun 1980", "order": 2},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 53},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "142861", "name": "Harold Glen (Hump) Rosenberger", "born": "6 May 1950"},
        {"code": "142862", "name": "Melvin Lee Rosenberger", "born": "27 Jul 1952"},
    ],
})

ENTRIES.append({
    "code": "14287",
    "name": "Willard Elijah Sines",
    "sex": "M",
    "born": "22 Feb 1934",
    "spouses": [{"name": "Ilene"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 53},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "142871", "name": "Eugene Sines"},
        {"code": "142872", "name": "Died at birth", "flags": {"diedInInfancy": True}},
        {"code": "142873", "name": "Kevin Sines"},
    ],
})

ENTRIES.append({
    "code": "14288",
    "name": "Ralph Edward Sines",
    "sex": "M",
    "born": "7 Feb 1936",
    "spouses": [{"name": "Evelyn Thomas", "born": "27 Sep 1943"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 54},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "142881", "name": "Lisa Sines", "born": "1 Dec 1963"},
        {"code": "142882", "name": "Tomothy Ray Sines", "born": "12 May 1965", "died": "1 Nov 1987"},
        {"code": "142883", "name": "Jeannette Sines", "born": "25 Jan 1968"},
        {"code": "142884", "name": "Tiffany Sines", "born": "5 Jun 1975"},
    ],
})

ENTRIES.append({
    "code": "14292",
    "name": "Clyde Guthrie",
    "sex": "M",
    "born": "4 Jun 1916",
    "died": "2 Jan 1956",
    "spouses": [{"name": "Lynch"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 54},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "142921", "name": "James Guthrie"},
        {"code": "142922", "name": "Clyde Guthrie, Jr.", "born": "Sep 1941", "died": "17 Dec 1941", "flags": {"diedInInfancy": True}},
    ],
})

ENTRIES.append({
    "code": "14293",
    "name": "Dorothy Guthrie",
    "sex": "F",
    "born": "4 Jul 1918",
    "spouses": [{"name": "Savage"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 54},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "142931", "name": "Robert Savage", "born": "16 Jul 1936"},
    ],
})

ENTRIES.append({
    "code": "14294",
    "name": "Fred Guthrie",
    "sex": "M",
    "born": "28 Oct 1920",
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 54},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "142941", "name": "Mary Guthrie", "born": "21 Oct 1941"},
        {"code": "142942", "name": "Paul Guthrie", "born": "10 Feb 1943"},
        {"code": "142943", "name": "Bill Guthrie", "born": "1 May 1946"},
        {"code": "142944", "name": "Jean Guthrie", "born": "6 Sep 1947"},
        {"code": "142945", "name": "Joan Guthrie", "born": "11 Aug 1949"},
        {"code": "142946", "name": "Harry Guthrie", "born": "18 Mar 1951"},
        {"code": "142947", "name": "Larry Guthrie", "born": "18 Mar 1951"},
        {"code": "142948", "name": "Robert Guthrie", "born": "16 Apr 1952"},
    ],
})

ENTRIES.append({
    "code": "14298",
    "name": "Earl Guthrie, Jr.",
    "sex": "M",
    "born": "28 Mar 1928",
    "spouses": [{"name": "Lois", "born": "21 Jul 1933"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 54},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "142981", "name": "Earl Guthrie, III", "born": "22 Mar 1952"},
        {"code": "142982", "name": "Carl Guthrie", "born": "6 Apr 1953"},
        {"code": "142983", "name": "Sharon Guthrie", "born": "12 Jun 1955"},
        {"code": "142984", "name": "Gerald Guthrie", "born": "21 Feb 1959"},
        {"code": "142985", "name": "Roger Guthrie", "born": "3 Dec 1962"},
    ],
})

ENTRIES.append({
    "code": "14299",
    "name": "Lucy Guthrie",
    "sex": "F",
    "born": "26 Jul 1931",
    "spouses": [{"name": "Harold S. Eutsey"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 54},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "142991", "name": "Deborah Mae Eutsey", "born": "12 Nov 1952"},
        {"code": "142992", "name": "Shirley Ann Eutsey", "born": "5 Dec 1954"},
        {"code": "142993", "name": "Dale Eugene Eutsey", "born": "26 Aug 1957"},
    ],
})

ENTRIES.append({
    "code": "1429C",
    "name": "Donna Jean Guthrie",
    "sex": "F",
    "born": "18 Apr 1939",
    "spouses": [{"name": "Hartman"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 54},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1429C1", "name": "Paul Franklin Hartman", "born": "26 Oct 1958"},
        {"code": "1429C2", "name": "Phyliss Jean Hartman", "born": "31 May 1963"},
    ],
})

ENTRIES.append({
    "code": "14329",
    "name": "Donald Myers",
    "sex": "M",
    "born": "31 Aug 1913",
    "died": "18 Jan 1981",
    "spouses": [{"name": "Geraldine Johnston", "born": "24 Sep 1924"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 54},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "143291", "name": "Donald Myers", "born": "7 May 1947"},
        {"code": "143292", "name": "Larry Myers", "born": "4 Feb 1951"},
        {"code": "143293", "name": "Linda Myers", "born": "4 Jun 1955"},
    ],
})

ENTRIES.append({
    "code": "14341",
    "name": "Bertha Elizabeth Cuppett",
    "sex": "F",
    "spouses": [{"name": "Earl Grayson Collins"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 55},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "143411", "name": "Mary Collins"},
        {"code": "143412", "name": "Raymond Collins"},
        {"code": "143413", "name": "Carl Collins"},
        {"code": "143414", "name": "William (Billy) Lee Collins"},
    ],
})

ENTRIES.append({
    "code": "14342",
    "name": "Nellie Cuppett",
    "sex": "F",
    "born": "6 Jul 1920",
    "died": "9 Dec 1973",
    "spouses": [{"name": "Chester Martin Nicola", "born": "7 Oct 1914", "died": "11 Feb 1963", "married": "12 Oct 1941", "details": "Same as #14422."}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 55},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "143421", "name": "Glenn D. Cuppett"},
        {"code": "143422", "name": "Paul J. Nicola"},
        {"code": "143423", "name": "Elizabeth Mae Nicola", "born": "5 Jul 1942", "died": "25 Sep 1942", "flags": {"diedInInfancy": True}},
        {"code": "143424", "name": "Carl R. Nicola", "born": "9 Sep 1946"},
        {"code": "143425", "name": "Robert Martin Nicola", "born": "26 Sep 1951"},
        {"code": "143426", "name": "Betty K. Nicola", "born": "13 Sep 1953"},
        {"code": "143427", "name": "Jacob George Nicola, Jr.", "born": "27 May 1960"},
        {"code": "143428", "name": "Infant", "flags": {"diedInInfancy": True}},
        {"code": "143429", "name": "Infant", "flags": {"diedInInfancy": True}},
        {"code": "14342A", "name": "Charles E. Nicola"},
        {"code": "14342B", "name": "Charlotte K. Nicola"},
    ],
})

ENTRIES.append({
    "code": "14343",
    "name": "Mamie Cuppett",
    "sex": "F",
    "spouses": [{"name": "Frank Winfield Collins"}],
    "notes": "PDF says only 'Had two Sons'.",
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 55},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
})

ENTRIES.append({
    "code": "14351",
    "name": "Joseph R. Sliger",
    "sex": "M",
    "born": "7 Jun 1916",
    "spouses": [{"name": "Eveline Giltner", "born": "26 Mar 1916", "married": "26 Mar 1937"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 55},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "143511", "name": "Ester G. Sliger", "born": "6 Jul 1938"},
        {"code": "143512", "name": "Richard F. Sliger", "born": "23 Sep 1939"},
        {"code": "143513", "name": "Rofelma L. Sliger", "born": "12 Jan 1941"},
        {"code": "143514", "name": "Frank A. Sliger", "born": "4 Sep 1942"},
    ],
})

ENTRIES.append({
    "code": "14411",
    "name": "Charles Orval Sisler",
    "sex": "M",
    "born": "20 Jul 1904",
    "died": "May 1961",
    "spouses": [{"name": "Azile Authur"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 55},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "144111", "name": "Betty Sisler"},
        {"code": "144112", "name": "Lois Jean Sisler"},
        {"code": "144113", "name": "Dale Arthur Sisler", "born": "1929"},
        {"code": "144114", "name": "William Sisler"},
    ],
})

ENTRIES.append({
    "code": "14412",
    "name": "Troy Wilbert Sisler",
    "sex": "M",
    "born": "20 Nov 1905",
    "died": "23 Nov 1965",
    "spouses": [{"name": "Lydia Pearl Hileman"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 55},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "144121", "name": "Dwight Marcus Sisler", "born": "May 1935"},
        {"code": "144122", "name": "Robert Clayton Sisler", "born": "1937"},
        {"code": "144123", "name": "Virginia Faye Sisler", "born": "1944"},
    ],
})

ENTRIES.append({
    "code": "14413",
    "name": "Carlos Eugene Sisler",
    "sex": "M",
    "born": "3 Apr 1907",
    "died": "13 May 1972",
    "spouses": [{"name": "Anna Jane Shaffer", "married": "24 Jun 1931"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 55},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "144131", "name": "Donald Ray Sisler", "born": "1932"},
        {"code": "144132", "name": "Dorthy Jean Sisler", "born": "Jul 1935"},
        {"code": "144133", "name": "Delbert Jack Sisler", "born": "1939"},
        {"code": "144134", "name": "Delores Ann Sisler", "born": "1947"},
    ],
})

ENTRIES.append({
    "code": "14414",
    "name": "Mary Ellen Sisler",
    "sex": "F",
    "born": "27 Jan 1909",
    "spouses": [{"name": "Paul Vamber Frezee", "born": "26 Jun 1910", "died": "Nov 1965"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 55},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "144141", "name": "Audrey Frazee", "born": "20 Jan 1932"},
    ],
})


# === Pages 56-60 vision pass (2026-06-07): Sisler/Friend/Thomas/Strawser/Blosser/Kahl ===
ENTRIES.append({
    "code": "14415",
    "name": "Paul Edgar Sisler",
    "sex": "M",
    "born": "28 Feb 1911",
    "died": "8 Sep 1987",
    "spouses": [{"name": "Lydia Jane Schnopp", "born": "26 Jan 1912", "died": "8 Aug 1996", "married": "8 May 1932"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 56},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "144151", "name": "Benjamin Paul Sisler", "born": "19 Apr 1933"},
        {"code": "144152", "name": "William Floyd Sisler", "born": "Jan 1937"},
        {"code": "144153", "name": "Mary Ellen Sisler", "born": "22 Oct 1940"},
        {"code": "144154", "name": "Jane Elaine Sisler", "born": "23 Jan 1944"},
        {"code": "144155", "name": "Wilma Marie Sisler", "born": "17 Feb 1946"},
        {"code": "144156", "name": "Shirley Ann Sisler", "born": "6 Jan 1949"},
    ],
})

ENTRIES.append({
    "code": "14416",
    "name": "George Ray Sisler",
    "sex": "M",
    "born": "18 May 1916",
    "died": "3 Sep 1966",
    "spouses": [{"name": "Edith Darby"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 56},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "144161", "name": "Norma Jean Sisler", "born": "12 Apr 1939"},
        {"code": "144162", "name": "John Lee Sisler"},
        {"code": "144163", "name": "Nancy Sisler"},
        {"code": "144164", "name": "George Ray Sisler, Jr."},
    ],
})

ENTRIES.append({
    "code": "14422",
    "name": "Chester Martin Nicola",
    "sex": "M",
    "born": "7 Oct 1914",
    "died": "9 Dec 1973",
    "buried": "Webbs Chapel Cemetery",
    "spouses": [{"name": "Nellie Cuppett", "born": "6 Jul 1920", "died": "11 Feb 1963", "married": "12 Oct 1941", "details": "Same as #14342."}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 56},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": "Children duplicate 14342x."},
})

ENTRIES.append({
    "code": "14452",
    "name": "Ivan Samuel Friend",
    "sex": "M",
    "born": "7 Mar 1915",
    "died": "21 Oct 1972",
    "spouses": [{"name": "Alma Ault"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 57},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "144521", "name": "Janet Friend"},
    ],
})

ENTRIES.append({
    "code": "14453",
    "name": "Pearl Lovine Friend",
    "sex": "F",
    "born": "29 Nov 1916",
    "died": "11 Sep 1978",
    "spouses": [{"name": "Ivon Theodore Spiker", "born": "12 Dec 1910", "died": "17 Apr 1978", "married": "14 Sep 1935", "details": "Same as #17112."}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 57},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "144531", "name": "Stanley Ray Spiker", "born": "2 Jun 1936"},
        {"code": "144532", "name": "Glenna Catherine Spiker", "born": "20 Sep 1941"},
        {"code": "144533", "name": "Ruby Lovine Spiker", "born": "21 Dec 1945"},
    ],
})

ENTRIES.append({
    "code": "14454",
    "name": "Helen Dorothy Friend",
    "sex": "F",
    "born": "12 Apr 1918",
    "spouses": [{"name": "Virgil P. Groves"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 57},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "144541", "name": "Donald Groves"},
        {"code": "144542", "name": "Charlotte Groves"},
        {"code": "144543", "name": "Larry Groves"},
    ],
})

ENTRIES.append({
    "code": "14455",
    "name": "Avis Mae Friend",
    "sex": "F",
    "born": "28 Jun 1920",
    "spouses": [{"name": "Willard Evans", "born": "7 Sep 1920", "died": "17 May 1997", "married": "21 Sep 1941"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 58},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "144551", "name": "Roy Evans"},
    ],
})

ENTRIES.append({
    "code": "14461",
    "name": "Arnold E. (Jack) Thomas",
    "sex": "M",
    "spouses": [{"name": "Cleo Rebekah (Becky) Stover", "born": "10 Jan 1925", "died": "20 Aug 1996", "married": "1944"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 58},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "144611", "name": "John Thomas"},
        {"code": "144612", "name": "Tom Thomas"},
        {"code": "144613", "name": "Jerry Thomas"},
        {"code": "144614", "name": "Jackie Thomas"},
        {"code": "144615", "name": "Kathy Thomas"},
        {"code": "144616", "name": "Fanny Thomas"},
        {"code": "144617", "name": "Patti Thomas"},
    ],
})

ENTRIES.append({
    "code": "14463",
    "name": "Janet Louise Thomas",
    "sex": "F",
    "born": "19 Apr 1925",
    "spouses": [{"name": "Elmer Dorris Strawser", "born": "25 Feb 1919", "married": "13 Dec 1949"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 58},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "144631", "name": "Terry Max Strawser", "born": "14 Jul 1943"},
        {"code": "144632", "name": "Linda Kay Strawser", "born": "13 Feb 1951"},
        {"code": "144633", "name": "Thomas Michael Strawser", "born": "7 Dec 1953"},
    ],
})

ENTRIES.append({
    "code": "14474",
    "name": "Franklin Richard Thomas",
    "sex": "M",
    "born": "11 Mar 1933",
    "spouses": [{"name": "Alice Guthrie", "born": "24 Oct 1939", "details": "Same as #13F74."}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 58},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": "Children cross-coded 13F741-3."},
})

ENTRIES.append({
    "code": "14475",
    "name": "David Ervin Thomas",
    "sex": "M",
    "born": "6 Apr 1939",
    "spouses": [{"name": "Ester Casteel"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 58},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "144751", "name": "Jane Elizabeth Thomas", "born": "6 May 1963"},
        {"code": "144752", "name": "Tina Barbarella Thomas", "born": "11 Jul 1970"},
    ],
})

ENTRIES.append({
    "code": "14476",
    "name": "Clarence Dewight Thomas",
    "sex": "M",
    "born": "29 Oct 1942",
    "spouses": [{"name": "Elizabeth Marie Early", "born": "18 Aug 1943", "married": "17 Mar 1962"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 58},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "144761", "name": "Kenneth Dewight Thomas", "born": "20 Oct 1962"},
        {"code": "144762", "name": "Jeffrey Dale Thomas", "born": "22 Aug 1963"},
        {"code": "144763", "name": "Michelle Dawn Thomas", "born": "11 Dec 1968"},
        {"code": "144764", "name": "Christine Marie Thomas", "born": "2 Feb 1971"},
        {"code": "144765", "name": "Rebecca Joanne Thomas", "born": "6 Dec 1972"},
        {"code": "144766", "name": "Jamie Scott Thomas", "born": "23 Sep 1975"},
        {"code": "144767", "name": "Matthew John Thomas", "born": "10 Aug 1977"},
    ],
})

ENTRIES.append({
    "code": "14481",
    "name": "Donna Mae Strawser",
    "sex": "F",
    "born": "18 Jun 1917",
    "died": "10 Jun 1973",
    "spouses": [{"name": "Benjamin Richard Reckart", "born": "12 Dec 1913"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 59},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "144811", "name": "Rev. Donald H. Reckart"},
        {"code": "144812", "name": "Kenneth W. Reckart"},
        {"code": "144813", "name": "Rev. Charles L. Reckart"},
        {"code": "144814", "name": "Rev. Gary P. Reckart"},
        {"code": "144815", "name": "Rev. Ray E. Reckart"},
        {"code": "144816", "name": "Regina Reckart"},
        {"code": "144817", "name": "Charlotte D. Reckart"},
        {"code": "144818", "name": "Doris A. Reckart"},
    ],
})

ENTRIES.append({
    "code": "14482",
    "name": "Paul Woodrow Strawser",
    "sex": "M",
    "born": "23 Apr 1920",
    "spouses": [{"name": "Lona Mildred (Pudd) Friend", "married": "3 Jul 1946"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 59},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "144821", "name": "Bonnie Kay Strawser"},
        {"code": "144822", "name": "Judy Rae Strawser"},
        {"code": "144823", "name": "Gary Strawser", "born": "1 Jul 1948"},
        {"code": "144824", "name": "Joy Ann Strawser"},
    ],
})

ENTRIES.append({
    "code": "14485",
    "name": "Cecil Ray Strawser",
    "sex": "M",
    "born": "11 Aug 1935",
    "spouses": [{"name": "Justine Fay Echart", "married": "1959"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 59},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "144851", "name": "Melanie Strawser", "born": "3 Feb 1961"},
    ],
})

ENTRIES.append({
    "code": "14511",
    "name": "Helen L. Guthrie",
    "sex": "F",
    "born": "4 Nov 1903",
    "spouses": [{"name": "Oscar J. Harvey", "born": "28 Feb 1903", "married": "7 Apr 1928"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 59},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "145111", "name": "Malon A. Harvey", "born": "3 May 1929"},
        {"code": "145112", "name": "Myron A. Harvey", "born": "13 Mar 1934"},
        {"code": "145113", "name": "Sheila D. Harvey", "born": "6 Oct 1943"},
    ],
})

ENTRIES.append({
    "code": "14541",
    "name": "John P. Blosser",
    "sex": "M",
    "born": "8 Apr 1912",
    "spouses": [{"name": "Rosalee V. Dissinger", "born": "10 Oct 1914", "married": "9 Jun 1934"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 59},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "145411", "name": "Carol Lee Blosser", "born": "11 Oct 1934"},
        {"code": "145412", "name": "John W. Blosser", "born": "1 Dec 1935"},
    ],
})

ENTRIES.append({
    "code": "14543",
    "name": "Dorothy M. Blosser",
    "sex": "F",
    "born": "20 Apr 1919",
    "spouses": [{"name": "Howard A. McDaniel", "born": "9 Mar 1916", "married": "25 Apr 1940"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 59},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "145431", "name": "Beverly Lee McDaniel", "born": "11 Jan 1942"},
    ],
})

ENTRIES.append({
    "code": "14544",
    "name": "David G. Blosser",
    "sex": "M",
    "born": "24 Sep 1922",
    "spouses": [{"name": "Dorothy M. Woods", "born": "24 Dec 1922", "married": "22 Mar 1941"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 59},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "145441", "name": "Judith Darlene Blosser", "born": "16 Jul 1943"},
    ],
})

ENTRIES.append({
    "code": "14581",
    "name": "W. P. Guthrie",
    "sex": "M",
    "born": "23 Jul 1922",
    "spouses": [{"name": "Edna Roselda", "born": "Jun 1921", "married": "Jun 1939"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 59},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "145811", "name": "Jeremiah W. Guthrie", "born": "8 Jan 1942"},
        {"code": "145812", "name": "Infant", "born": "8 Oct 1943", "died": "1943", "flags": {"diedInInfancy": True}},
        {"code": "145813", "name": "Jean Marie Guthrie", "born": "4 May 1945"},
    ],
})

ENTRIES.append({
    "code": "14613",
    "name": "George E. Dodid",
    "sex": "M",
    "born": "27 Mar 1909",
    "spouses": [{"name": "Helen Pastara", "born": "1920", "married": "Sep 1944"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 59},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "146131", "name": "Eric Dodid", "born": "Aug 1945"},
    ],
})

ENTRIES.append({
    "code": "14614",
    "name": "Birges (Birdie) Agnes Miller",
    "sex": "F",
    "born": "9 Jul 1915",
    "spouses": [{"name": "James Kerso", "born": "1918", "married": "Nov 1944"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 60},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "146141", "name": "Charles A. Wolf"},
        {"code": "146142", "name": "Infant Son"},
    ],
})

ENTRIES.append({
    "code": "14714",
    "name": "Ralph Kahl",
    "sex": "M",
    "born": "19 Apr 1913",
    "died": "19 Jan 1978",
    "spouses": [{"name": "Mabel E. Campbell"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 60},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "147141", "name": "Marcella Kahl"},
        {"code": "147142", "name": "Dixie Lee Kahl"},
    ],
})

ENTRIES.append({
    "code": "14717",
    "name": "Eleanor E. Kahl",
    "sex": "F",
    "born": "2 Apr 1920",
    "died": "18 Oct 1987",
    "spouses": [{"name": "William Amos Deal"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 60},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "147171", "name": "Judy Deal"},
        {"code": "147172", "name": "Roger A. Deal"},
    ],
})

ENTRIES.append({
    "code": "14718",
    "name": "Edward Harold Kahl",
    "sex": "M",
    "born": "16 Dec 1922",
    "spouses": [{"name": "Mary Ellen Forman", "born": "18 Aug 1923", "married": "22 Nov 1940"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 60},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "147181", "name": "Donna Louise Kahl", "born": "18 Jun 1942"},
        {"code": "147182", "name": "Edward Wallace Kahl", "born": "29 Dec 1943", "died": "26 Jan 1944", "flags": {"diedInInfancy": True}},
        {"code": "147183", "name": "Shirley Jean Kahl", "born": "20 Jul 1945"},
        {"code": "147184", "name": "Roy Douglas Kahl", "born": "8 Sep 1949"},
    ],
})

ENTRIES.append({
    "code": "14719",
    "name": "Everett Kahl",
    "sex": "M",
    "flags": {"stepChild": True},
    "spouses": [{"name": "Grace Sumey"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 60},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "147191", "name": "Walter Kahl"},
        {"code": "147192", "name": "Eric Kahl"},
        {"code": "147193", "name": "David Kahl"},
        {"code": "147194", "name": "Everett Wade Kahl", "born": "4 Dec 1953", "died": "1 Nov 1972"},
        {"code": "147195", "name": "Linda Kahl"},
        {"code": "147196", "name": "Wanda Kahl"},
        {"code": "147197", "name": "Mary Kahl"},
        {"code": "147198", "name": "Ella Kahl"},
    ],
})

ENTRIES.append({
    "code": "14731",
    "name": "Everett Samuel Miller",
    "sex": "M",
    "born": "21 Dec 1901",
    "spouses": [{"name": "Irene Postal", "born": "7 Jun 1910", "married": "Dec 1933"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 60},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "147311", "name": "Albert Miller", "born": "10 Mar 1934", "died": "1934", "flags": {"diedInInfancy": True}},
        {"code": "147312", "name": "Russell E. Miller", "born": "28 Feb 1935"},
        {"code": "147313", "name": "Deloris Jane Miller", "born": "11 Apr 1936"},
        {"code": "147314", "name": "William Howard Miller", "born": "16 Apr 1938"},
        {"code": "147315", "name": "Helen Jean Miller", "born": "12 Jun 1939", "died": "12 Jun 1939", "flags": {"diedInInfancy": True}},
        {"code": "147316", "name": "Douglas Paul Miller", "born": "2 Feb 1942"},
        {"code": "147317", "name": "Caroline Miller", "born": "18 Oct 1943", "died": "18 Oct 1943", "flags": {"diedInInfancy": True}},
    ],
})


# === Drafts extracted from rachel.txt by draft_from_ocr.py ===
ENTRIES.append({
    'code': '632',
    'name': 'Mary (Maggic) Thomas',
    "source": {
        'pdf': 'Rachel_Guthrie - One Generation .pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'died': '1948',
    "spouses": [
        {
            'name': 'Estelle Scese',
        },
    ],
})


# === Drafts extracted from william.txt by draft_from_ocr.py ===
ENTRIES.append({
    'code': '212',
    'name': 'Wilbur Finley Frankhouser',
    "source": {
        'pdf': 'William_Guthrie - One Generation.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '12 Sep 1870',
    'died': '25 Feb 1963',
    "spouses": [
        {
            'name': 'T. W',
        },
    ],
})

ENTRIES.append({
    'code': '2121',
    'name': 'Ometa Bianch Frankhouser',
    "source": {
        'pdf': 'William_Guthrie - One Generation.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
})

ENTRIES.append({
    'code': '2124',
    'name': 'Iva Frankhouser',
    "source": {
        'pdf': 'William_Guthrie - One Generation.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '26 Jan 1887',
    "spouses": [
        {
            'name': 'James R',
            'married': '26 Jan 1887',
        },
    ],
})

ENTRIES.append({
    'code': '214',
    'name': 'Effie Jane Frankhouser',
    "source": {
        'pdf': 'William_Guthrie - One Generation.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
})

ENTRIES.append({
    'code': '215',
    'name': 'Walter Frankhouser',
    "source": {
        'pdf': 'William_Guthrie - One Generation.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '19 Jan 1880',
    'died': '26 Nov 1913',
})

ENTRIES.append({
    'code': '222',
    'name': 'William Asbury Harshbarger',
    "source": {
        'pdf': 'William_Guthrie - One Generation.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '16 Aug 1866',
    'died': '17 Jul 1942',
    "spouses": [
        {
            'name': 'Wilma Perry Ralph Platt Harshbar',
            'married': '24 Jul 1903',
        },
    ],
})

ENTRIES.append({
    'code': '22211',
    'name': 'Eugene Lee Harshbarger',
    "source": {
        'pdf': 'William_Guthrie - One Generation.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
})

ENTRIES.append({
    'code': '22212',
    'name': 'Carolyn Harshbarger',
    "source": {
        'pdf': 'William_Guthrie - One Generation.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    "spouses": [
        {
            'name': 'A Bc',
        },
    ],
})

ENTRIES.append({
    'code': '2222',
    'name': 'Frank Victor Harshbarger',
    "source": {
        'pdf': 'William_Guthrie - One Generation.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '23 Oct 1893',
    'died': '11 Jan 1985',
    "spouses": [
        {
            'name': 'Wilma Perry',
            'married': '12 Jan 1896',
        },
    ],
})

ENTRIES.append({
    'code': '22221',
    'name': 'Frank Victor Harshbarger',
    "source": {
        'pdf': 'William_Guthrie - One Generation.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '07 Jun 1933',
})

ENTRIES.append({
    'code': '222211',
    'name': 'Sharon Mane Harshbarger',
    "source": {
        'pdf': 'William_Guthrie - One Generation.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '09 Sep 1958',
})

ENTRIES.append({
    'code': '222213',
    'name': 'Mary',
    "source": {
        'pdf': 'William_Guthrie - One Generation.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '02 Jun 1978',
    "spouses": [
        {
            'name': 'Edward Moomau',
            'married': 'Mav 1988',
        },
    ],
})

ENTRIES.append({
    'code': '2222134',
    'name': 'Derick Peters',
    "source": {
        'pdf': 'William_Guthrie - One Generation.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '23 Aug 1989',
})

ENTRIES.append({
    'code': '222215',
    'name': 'Raymond Stephan H',
    "source": {
        'pdf': 'William_Guthrie - One Generation.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '18 Jul 1966',
})

ENTRIES.append({
    'code': '222216',
    'name': 'Diane Harshbareer',
    "source": {
        'pdf': 'William_Guthrie - One Generation.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '16 Oct 1967',
})

ENTRIES.append({
    'code': '22222',
    'name': 'Marjorie Harshbarger',
    "source": {
        'pdf': 'William_Guthrie - One Generation.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '13 Feb 1930',
    'died': '13 may 1984',
    "spouses": [
        {
            'name': 'Joseph Lats',
            'married': '14 Jan 1930',
        },
    ],
})

ENTRIES.append({
    'code': '2262',
    'name': 'Mary Louise',
    "source": {
        'pdf': 'William_Guthrie - One Generation.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '17 Apr 1913',
    "spouses": [
        {
            'name': 'Paul Brower',
        },
    ],
})

ENTRIES.append({
    'code': '2263',
    'name': 'Wil Leelia Harshbarger',
    "source": {
        'pdf': 'William_Guthrie - One Generation.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '24 Jun 1915',
    "spouses": [
        {
            'name': 'Dennis Dunn',
        },
    ],
})


# === Drafts extracted from absalom.txt by draft_from_ocr.py ===
ENTRIES.append({
    'code': '8254',
    'name': 'Ruth Alice Alexander',
    "source": {
        'pdf': 'Absalom_Guthrie - One Generation .pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '03 Dec 1904',
})

ENTRIES.append({
    'code': '8261',
    'name': 'Harry Hardesty',
    "source": {
        'pdf': 'Absalom_Guthrie - One Generation .pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
})

ENTRIES.append({
    'code': '8271',
    'name': 'Dale Hardesty',
    "source": {
        'pdf': 'Absalom_Guthrie - One Generation .pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': 'about 1900',
})

ENTRIES.append({
    'code': '8741',
    'name': 'Elizabeth Ann Guthrie',
    "source": {
        'pdf': 'Absalom_Guthrie - One Generation .pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
})

ENTRIES.append({
    'code': '876',
    'name': 'Park Edward Guthrie',
    "source": {
        'pdf': 'Absalom_Guthrie - One Generation .pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '07 Jan 1930',
})

ENTRIES.append({
    'code': '882',
    'name': "Gracie O'Neil",
    "source": {
        'pdf': 'Absalom_Guthrie - One Generation .pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '06 Apr 1884',
    'died': '23 Oct 1900',
    "spouses": [
        {
            'name': 'Hammond Hardesty - Lived in Pauldine',
            'married': 'Sep 1898',
        },
    ],
})


# === Drafts extracted from stephen.txt by draft_from_ocr.py ===
ENTRIES.append({
    'code': '53253',
    'name': 'Leslie Hadden Guthrie',
    "source": {
        'pdf': 'Stephen_Guthrie - One Generation .pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '24 Oct 1920',
})

ENTRIES.append({
    'code': '5326',
    'name': 'Russel Guthrie',
    "source": {
        'pdf': 'Stephen_Guthrie - One Generation .pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '1898',
    'died': '06 Sep 1963',
    "spouses": [
        {
            'name': 'Edna Sullwan CHILDREN',
        },
    ],
})

ENTRIES.append({
    'code': '532A',
    'name': 'Lee Guthr',
    "source": {
        'pdf': 'Stephen_Guthrie - One Generation .pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '09 Jan 1904',
    'died': '15 Mar 1980',
    "spouses": [
        {
            'name': 'Clara IE',
            'married': '09 Jan 1904',
        },
    ],
})

ENTRIES.append({
    'code': '53611',
    'name': 'Virginia Maxine Bishop',
    "source": {
        'pdf': 'Stephen_Guthrie - One Generation .pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '17 Nov 1931',
})

ENTRIES.append({
    'code': '53612',
    'name': 'Marvin Paul Bishop',
    "source": {
        'pdf': 'Stephen_Guthrie - One Generation .pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '02 May 1937',
})

ENTRIES.append({
    'code': '5362',
    'name': 'Frewilliam Debishop',
    "source": {
        'pdf': 'Stephen_Guthrie - One Generation .pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '21 Jun 1913',
    'died': '21 Apr 1929',
    "spouses": [
        {
            'name': 'Vern Burl Gibson',
            'married': '21 Jun 1913',
        },
    ],
})

ENTRIES.append({
    'code': '53622',
    'name': 'Everett Clayton Bishop',
    "source": {
        'pdf': 'Stephen_Guthrie - One Generation .pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '23 Aug 1930',
})

ENTRIES.append({
    'code': '53623',
    'name': 'Lula Berlene Bishop',
    "source": {
        'pdf': 'Stephen_Guthrie - One Generation .pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '01 Mar 1933',
})

ENTRIES.append({
    'code': '53624',
    'name': 'Violet Rosalee Bishop',
    "source": {
        'pdf': 'Stephen_Guthrie - One Generation .pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '15 Jul 1935',
})

ENTRIES.append({
    'code': '536241',
    'name': 'Randal Alan Rhodes',
    "source": {
        'pdf': 'Stephen_Guthrie - One Generation .pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '11 Feb 1957',
})

ENTRIES.append({
    'code': '536242',
    'name': 'Robm Lynn Rhodes',
    "source": {
        'pdf': 'Stephen_Guthrie - One Generation .pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '23 Oct 1961',
    "spouses": [
        {
            'name': 'Lels Elaine Thom',
            'married': 'Dec 1938',
        },
    ],
})

ENTRIES.append({
    'code': '536262',
    'name': 'Stephanie Lee Bishop',
    "source": {
        'pdf': 'Stephen_Guthrie - One Generation .pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '06 Nov 1967',
})

ENTRIES.append({
    'code': '56522',
    'name': 'Sarah Frances Frankhouser',
    "source": {
        'pdf': 'Stephen_Guthrie - One Generation .pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '19 Jan 1945',
    "spouses": [
        {
            'name': 'John Mitchell Humberson son of John W',
            'married': '20 Oct 1977',
        },
    ],
})

ENTRIES.append({
    'code': '591',
    'name': 'Belle Guth',
    "source": {
        'pdf': 'Stephen_Guthrie - One Generation .pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    "spouses": [
        {
            'name': 'Alva RIE Russell',
        },
    ],
})


# === Drafts extracted from alexander.txt by draft_from_ocr.py ===
ENTRIES.append({
    'code': 'A21121',
    'name': 'Kathy Maric Frazee',
    "source": {
        'pdf': 'Alexander_Guthrie - Five Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '01 Jun 1956',
})

ENTRIES.append({
    'code': 'A21122',
    'name': 'Brenda Kay Frazee',
    "source": {
        'pdf': 'Alexander_Guthrie - Five Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '24 Aug 1959',
    "spouses": [
        {
            'name': 'Fred Allen Baislew',
            'married': '07 Sep 1952',
        },
    ],
})

ENTRIES.append({
    'code': 'A211221',
    'name': 'Jamue Lynn Balsley',
    "source": {
        'pdf': 'Alexander_Guthrie - Five Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '15 Jun 1985',
})

ENTRIES.append({
    'code': 'A211222',
    'name': 'Brad Allen Balsiev',
    "source": {
        'pdf': 'Alexander_Guthrie - Five Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '26 May 1988',
})

ENTRIES.append({
    'code': 'A21131',
    'name': 'Kamberiy Frazec',
    "source": {
        'pdf': 'Alexander_Guthrie - Five Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '13 Jul 1960',
})

ENTRIES.append({
    'code': 'A2121',
    'name': 'Norma Ruth Frazee',
    "source": {
        'pdf': 'Alexander_Guthrie - Five Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '30 Aug 1938',
    'died': '20 Feb 1989',
})

ENTRIES.append({
    'code': 'A21211',
    'name': 'Barbara Ann Frazee',
    "source": {
        'pdf': 'Alexander_Guthrie - Five Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '09 Sep 1957',
    'died': '01 Jun 1996',
})

ENTRIES.append({
    'code': 'A212111',
    'name': 'Harlan Benjamin Strawser',
    "source": {
        'pdf': 'Alexander_Guthrie - Five Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '15 Feb 1978',
    'died': '09 May 1982',
})

ENTRIES.append({
    'code': 'A21212',
    'name': 'Gail Darlene Frazec',
    "source": {
        'pdf': 'Alexander_Guthrie - Five Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '30 Oct 1958',
})

ENTRIES.append({
    'code': 'A212121',
    'name': 'Serena Celeste Show',
    "source": {
        'pdf': 'Alexander_Guthrie - Five Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '12 Jun 1987',
})

ENTRIES.append({
    'code': 'A212142',
    'name': 'Tras James Rounds',
    "source": {
        'pdf': 'Alexander_Guthrie - Five Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '1989',
})

ENTRIES.append({
    'code': 'A21221',
    'name': 'James Walter Eisentrout',
    "source": {
        'pdf': 'Alexander_Guthrie - Five Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '08 Jan 1960',
})

ENTRIES.append({
    'code': 'A212211',
    'name': 'Patrick Tyler Eisent',
    "source": {
        'pdf': 'Alexander_Guthrie - Five Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
})

ENTRIES.append({
    'code': 'A212212',
    'name': 'Kelli Renee Eisentrou',
    "source": {
        'pdf': 'Alexander_Guthrie - Five Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
})

ENTRIES.append({
    'code': 'A212213',
    'name': 'Reb Leigh Eisentrout',
    "source": {
        'pdf': 'Alexander_Guthrie - Five Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '28 Dec 1989',
})

ENTRIES.append({
    'code': 'A21222',
    'name': 'Donna Sue Ensentrout',
    "source": {
        'pdf': 'Alexander_Guthrie - Five Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
})

ENTRIES.append({
    'code': 'A213',
    'name': 'Frank Clark Frazee',
    "source": {
        'pdf': 'Alexander_Guthrie - Five Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '04 Aug 1902',
    'died': '29 Jan 1956',
    "spouses": [
        {
            'name': 'Anna Blanche Ravmond',
            'married': '11 Feb 1966',
        },
    ],
})

ENTRIES.append({
    'code': 'A2131',
    'name': 'Mary Louise Frazee',
    "source": {
        'pdf': 'Alexander_Guthrie - Five Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '27 Apr 1941',
    'died': '07 Jan 1966',
})

ENTRIES.append({
    'code': 'A21311',
    'name': 'Robert Carroll Hager Ill',
    "source": {
        'pdf': 'Alexander_Guthrie - Five Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '24 Sep 1960',
})

ENTRIES.append({
    'code': 'A21312',
    'name': 'Jonathan Allen Hager',
    "source": {
        'pdf': 'Alexander_Guthrie - Five Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '21 Jun 1964',
})

ENTRIES.append({
    'code': 'A2141',
    'name': 'Darwin Roy Shaffer',
    "source": {
        'pdf': 'Alexander_Guthrie - Five Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '08 Aug 1944',
})

ENTRIES.append({
    'code': 'A2211',
    'name': 'Martha Louise Alexander',
    "source": {
        'pdf': 'Alexander_Guthrie - Five Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '15 Jul 1924',
})

ENTRIES.append({
    'code': 'A227',
    'name': 'Sarah Ellen Guthrie',
    "source": {
        'pdf': 'Alexander_Guthrie - Five Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '14 Jun 1916',
    'died': '23 Sep 1968',
})

ENTRIES.append({
    'code': 'A242',
    'name': 'Martha Leona Miller',
    "source": {
        'pdf': 'Alexander_Guthrie - Five Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '29 Sep 1913',
})

ENTRIES.append({
    'code': 'A2422',
    'name': 'Alice Elizabeth Hinebaugh',
    "source": {
        'pdf': 'Alexander_Guthrie - Five Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '14 Sep 1944',
})

ENTRIES.append({
    'code': 'A353',
    'name': 'Mary Blanche Romesburg',
    "source": {
        'pdf': 'Alexander_Guthrie - Five Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '29 Feb 1904',
})

ENTRIES.append({
    'code': 'A354',
    'name': 'Millie A',
    "source": {
        'pdf': 'Alexander_Guthrie - Five Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '19 Feb 1906',
})

ENTRIES.append({
    'code': 'A355',
    'name': 'Lucy May Romesburg',
    "source": {
        'pdf': 'Alexander_Guthrie - Five Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '13 Apr 1945',
})

ENTRIES.append({
    'code': 'A356',
    'name': 'Myrtle P',
    "source": {
        'pdf': 'Alexander_Guthrie - Five Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '08 Apr 1912',
})

ENTRIES.append({
    'code': 'A357',
    'name': 'Sameul M',
    "source": {
        'pdf': 'Alexander_Guthrie - Five Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '22 May 1917',
})

ENTRIES.append({
    'code': 'A3571',
    'name': 'Louis Martin Romesburg',
    "source": {
        'pdf': 'Alexander_Guthrie - Five Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '1941',
    'died': '19 Dec 1953',
    "spouses": [
        {
            'name': 'Madelon Junk',
            'married': '24 Dec 1944',
        },
    ],
})

ENTRIES.append({
    'code': 'A3B5',
    'name': 'Donald Edward',
    "source": {
        'pdf': 'Alexander_Guthrie - Five Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
})

ENTRIES.append({
    'code': 'A3B6',
    'name': 'Dorothy Jean Rom',
    "source": {
        'pdf': 'Alexander_Guthrie - Five Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '07 Nov 1869',
    'died': '17 Dec 1934',
    "spouses": [
        {
            'name': 'Helen Tabon',
            'married': '02 Aug 1906',
        },
    ],
})

ENTRIES.append({
    'code': 'A41131',
    'name': 'Mark Chnstian Endsley',
    "source": {
        'pdf': 'Alexander_Guthrie - Five Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '10 Oct 1959',
    "spouses": [
        {
            'name': 'Dorothy Eicher',
            'married': '04 Aug 1921',
        },
    ],
})

ENTRIES.append({
    'code': 'A4122',
    'name': 'Jack L',
    "source": {
        'pdf': 'Alexander_Guthrie - Five Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '16 Jan 1900',
    'died': '1970',
    "spouses": [
        {
            'name': 'Cecelia Bonchosky',
        },
    ],
})

ENTRIES.append({
    'code': 'A4131',
    'name': 'Geraldine Lorraine Frankhob',
    "source": {
        'pdf': 'Alexander_Guthrie - Five Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '27 Jun 1938',
})

ENTRIES.append({
    'code': 'A4134',
    'name': 'Francis G',
    "source": {
        'pdf': 'Alexander_Guthrie - Five Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '22 Sep 1939',
    'died': '09 May 1978',
})

ENTRIES.append({
    'code': 'A415',
    'name': 'GUY FRANKb',
    "source": {
        'pdf': 'Alexander_Guthrie - Five Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '12 Nov 1913',
})

ENTRIES.append({
    'code': 'A41524',
    'name': 'Tami Linn Frankhouser',
    "source": {
        'pdf': 'Alexander_Guthrie - Five Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '17 Aug 1962',
})

ENTRIES.append({
    'code': 'A41525',
    'name': 'Thomas Todd Frankhouser',
    "source": {
        'pdf': 'Alexander_Guthrie - Five Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '02 Sep 1964',
    "spouses": [
        {
            'name': 'Dorothy Markutsa',
        },
    ],
})

ENTRIES.append({
    'code': 'A41531',
    'name': 'Eric Joseph Frankhouser - adopted',
    "source": {
        'pdf': 'Alexander_Guthrie - Five Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '10 Nov 1971',
})

ENTRIES.append({
    'code': 'A41532',
    'name': 'Jennifer Lynette Frankhouser - adopted',
    "source": {
        'pdf': 'Alexander_Guthrie - Five Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '28 Oct 1974',
    "spouses": [
        {
            'name': 'Sarah Thomas',
            'married': 'Apr 1961',
        },
    ],
})

ENTRIES.append({
    'code': 'A435',
    'name': 'Ro Eugene Be Cupp',
    "source": {
        'pdf': 'Alexander_Guthrie - Five Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '03 Apr 1923',
})

ENTRIES.append({
    'code': 'A435121',
    'name': 'Ejicen Patricia Underwo',
    "source": {
        'pdf': 'Alexander_Guthrie - Five Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
})

ENTRIES.append({
    'code': 'A436',
    'name': 'Martin Luther Cupp',
    "source": {
        'pdf': 'Alexander_Guthrie - Five Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '09 May 1918',
})

ENTRIES.append({
    'code': 'A44911',
    'name': 'Ryan David Smith',
    "source": {
        'pdf': 'Alexander_Guthrie - Five Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '27 Apr 1984',
})

ENTRIES.append({
    'code': 'A44912',
    'name': 'Eric Paul Smith',
    "source": {
        'pdf': 'Alexander_Guthrie - Five Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '27 Apr 1984',
    "spouses": [
        {
            'name': 'David Edward Brvte CHILDREN',
        },
    ],
})

ENTRIES.append({
    'code': 'A45122',
    'name': 'Lioyd Charlies Linderwood',
    "source": {
        'pdf': 'Alexander_Guthrie - Five Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '20 May 1963',
})

ENTRIES.append({
    'code': 'A4514',
    'name': 'Patty Jo Cupp',
    "source": {
        'pdf': 'Alexander_Guthrie - Five Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '30 May 1941',
})

ENTRIES.append({
    'code': 'A45141',
    'name': 'Sharon Kay Smith',
    "source": {
        'pdf': 'Alexander_Guthrie - Five Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '23 Jul 1963',
})

ENTRIES.append({
    'code': 'A45142',
    'name': 'Otto Sauers',
    "source": {
        'pdf': 'Alexander_Guthrie - Five Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '07 Dec 1967',
})

ENTRIES.append({
    'code': 'A45153',
    'name': 'Charles Phillip Anderson',
    "source": {
        'pdf': 'Alexander_Guthrie - Five Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '04 Sep 1964',
})

ENTRIES.append({
    'code': 'A45154',
    'name': 'Tammy Daveb',
    "source": {
        'pdf': 'Alexander_Guthrie - Five Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '21 May 1969',
})

ENTRIES.append({
    'code': 'A45156',
    'name': 'Keith Daven',
    "source": {
        'pdf': 'Alexander_Guthrie - Five Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '26 Oct 1943',
})

ENTRIES.append({
    'code': 'A453',
    'name': 'Infant Son',
    "source": {
        'pdf': 'Alexander_Guthrie - Five Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '01 Oct 1912',
    'died': '08 Nov 1960',
})

ENTRIES.append({
    'code': 'A45511',
    'name': 'Shelley Cupp',
    "source": {
        'pdf': 'Alexander_Guthrie - Five Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '11 Jul 1965',
    'died': '25 Jul 1965',
})

ENTRIES.append({
    'code': 'A45512',
    'name': 'Shawn Cupp',
    "source": {
        'pdf': 'Alexander_Guthrie - Five Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
})

ENTRIES.append({
    'code': 'A45513',
    'name': 'Ronald Scott Cupp',
    "source": {
        'pdf': 'Alexander_Guthrie - Five Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
})

ENTRIES.append({
    'code': 'A45514',
    'name': 'Michsel Eugene Cupp',
    "source": {
        'pdf': 'Alexander_Guthrie - Five Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '03 Apr 1975',
})

ENTRIES.append({
    'code': 'A45621',
    'name': 'Enmca Mane Myers',
    "source": {
        'pdf': 'Alexander_Guthrie - Five Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '29 Jun 1971',
})

ENTRIES.append({
    'code': 'A45622',
    'name': 'Meghan Cortney Cupp',
    "source": {
        'pdf': 'Alexander_Guthrie - Five Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '26 Jun 1978',
})

ENTRIES.append({
    'code': 'A4565',
    'name': 'Charles Wesley Cupp',
    "source": {
        'pdf': 'Alexander_Guthrie - Five Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
})

ENTRIES.append({
    'code': 'A45652',
    'name': 'Tracy Varndell',
    "source": {
        'pdf': 'Alexander_Guthrie - Five Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
})

ENTRIES.append({
    'code': 'A45671',
    'name': 'Jenn Dawn ifer Cupp',
    "source": {
        'pdf': 'Alexander_Guthrie - Five Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '08 Mar 1979',
})

ENTRIES.append({
    'code': 'A45672',
    'name': 'Tiffany Jo Reckart',
    "source": {
        'pdf': 'Alexander_Guthrie - Five Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '11 May 1983',
})

ENTRIES.append({
    'code': 'A457',
    'name': 'Ray Darwin Cupp',
    "source": {
        'pdf': 'Alexander_Guthrie - Five Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '07 Apr 1921',
    'died': '1974',
    "spouses": [
        {
            'name': 'Clyde Coates',
        },
    ],
})

ENTRIES.append({
    'code': 'A4591',
    'name': 'Sher Kay Rie King',
    "source": {
        'pdf': 'Alexander_Guthrie - Five Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '06 Jun 1950',
})

ENTRIES.append({
    'code': 'AB2',
    'name': 'Ruby Pearl Guthrie',
    "source": {
        'pdf': 'Alexander_Guthrie - Five Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '18 Jan 1893',
    'died': '18 Oct 1979',
    "spouses": [
        {
            'name': 'Edwin Ross Evans',
            'married': '14 Jul 1879',
        },
    ],
})

ENTRIES.append({
    'code': 'AB21',
    'name': 'Vesty D',
    "source": {
        'pdf': 'Alexander_Guthrie - Five Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
})

ENTRIES.append({
    'code': 'AB22',
    'name': 'MaEvans',
    "source": {
        'pdf': 'Alexander_Guthrie - Five Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    "spouses": [
        {
            'name': 'Clyde een Caates',
        },
    ],
})

ENTRIES.append({
    'code': 'AB23',
    'name': 'Wanda M',
    "source": {
        'pdf': 'Alexander_Guthrie - Five Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '03 Apr 1922',
    'died': '11 Aug 1985',
    "spouses": [
        {
            'name': 'Charies Friend',
            'married': '03 Apr 1922',
        },
    ],
})

ENTRIES.append({
    'code': 'AB24',
    'name': 'Stanicy Regis Evans',
    "source": {
        'pdf': 'Alexander_Guthrie - Five Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '17 Dec 1896',
    'died': '19 Oct 1988',
})

ENTRIES.append({
    'code': 'AB241',
    'name': 'Darlene Fike Evans',
    "source": {
        'pdf': 'Alexander_Guthrie - Five Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '02 May 1955',
    'died': '09 Aug 1974',
    "spouses": [
        {
            'name': 'Virginia Umbel',
        },
    ],
})

ENTRIES.append({
    'code': 'AB2411',
    'name': 'Brian Eugene Bryte',
    "source": {
        'pdf': 'Alexander_Guthrie - Five Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '09 Sep 1973',
})

ENTRIES.append({
    'code': 'AB244',
    'name': 'We Jo Evans',
    "source": {
        'pdf': 'Alexander_Guthrie - Five Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '1952',
})


# === Drafts extracted from james.txt by draft_from_ocr.py ===
ENTRIES.append({
    'code': '7131111',
    'name': 'Erin Jennifer Blankenship',
    "source": {
        'pdf': 'James_Guthrie - Seven Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '07 Dec 1975',
    'died': '14 Apr 1977',
})

ENTRIES.append({
    'code': '71331',
    'name': 'James Freeland Cale',
    "source": {
        'pdf': 'James_Guthrie - Seven Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '15 Apr 1945',
    'died': '02 Jun 1986',
    "spouses": [
        {
            'name': 'Charics (Bud) Dailev of Alum Bank',
        },
    ],
})

ENTRIES.append({
    'code': '7145',
    'name': 'Ina Winifred Barnes',
    "source": {
        'pdf': 'James_Guthrie - Seven Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '13 Jan 1908',
    'died': '20 Aug 1984',
})

ENTRIES.append({
    'code': '71454',
    'name': 'Alda Mae Wolfe',
    "source": {
        'pdf': 'James_Guthrie - Seven Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '02 May 1935',
})

ENTRIES.append({
    'code': '71455',
    'name': 'Dwain Edwin Wolfe',
    "source": {
        'pdf': 'James_Guthrie - Seven Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '24 Aug 1936',
    'died': '09 Sep 1979',
    "spouses": [
        {
            'name': 'Ins May Wayne CHILDREN',
        },
    ],
})

ENTRIES.append({
    'code': '7146',
    'name': 'Fleming Clark Barnes',
    "source": {
        'pdf': 'James_Guthrie - Seven Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '29 Aug 1913',
})

ENTRIES.append({
    'code': '71511',
    'name': 'Suzanne Kay Guthrie',
    "source": {
        'pdf': 'James_Guthrie - Seven Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '02 Dec 1942',
    'died': '23 May 1963',
})

ENTRIES.append({
    'code': '717',
    'name': 'Pear Grace Barnes Lie',
    "source": {
        'pdf': 'James_Guthrie - Seven Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '24 Apr 1886',
    'died': '17 May 1925',
    "spouses": [
        {
            'name': 'Kathleen Nordeck',
            'married': '25 Mar 1914',
        },
    ],
})

ENTRIES.append({
    'code': '717631',
    'name': 'Emily Scott Fike',
    "source": {
        'pdf': 'James_Guthrie - Seven Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '11 Mar 1983',
})

ENTRIES.append({
    'code': '722',
    'name': 'Virginia Barbara',
    "source": {
        'pdf': 'James_Guthrie - Seven Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '10 Dec 1864',
    'died': '19 Jul 1972',
})

ENTRIES.append({
    'code': '722122',
    'name': 'Chandler Campbell Thornton',
    "source": {
        'pdf': 'James_Guthrie - Seven Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '02 May 1975',
})

ENTRIES.append({
    'code': '7231',
    'name': 'Howard Emerson Barnes',
    "source": {
        'pdf': 'James_Guthrie - Seven Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '02 Apr 1913',
})

ENTRIES.append({
    'code': '723111',
    'name': 'Sharon Leigh Shelton',
    "source": {
        'pdf': 'James_Guthrie - Seven Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
})

ENTRIES.append({
    'code': '723112',
    'name': 'Joseph Vanderbilt Shelton',
    "source": {
        'pdf': 'James_Guthrie - Seven Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '10 Mar 1964',
})

ENTRIES.append({
    'code': '7232',
    'name': 'Genevieve Lillian Bames',
    "source": {
        'pdf': 'James_Guthrie - Seven Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '22 Sep 1914',
    'died': '15 Jun 1932',
})

ENTRIES.append({
    'code': '7233',
    'name': 'James Quinter Barnes',
    "source": {
        'pdf': 'James_Guthrie - Seven Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '22 May 1919',
    'died': '03 Jul 1969',
})

ENTRIES.append({
    'code': '72331',
    'name': 'Jack Lloyd Bames',
    "source": {
        'pdf': 'James_Guthrie - Seven Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '23 Feb 1953',
})

ENTRIES.append({
    'code': '7234',
    'name': 'Lau Cole Barnes',
    "source": {
        'pdf': 'James_Guthrie - Seven Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '16 Dec 1918',
    'died': '15 Nov 1977',
    "spouses": [
        {
            'name': 'Ailene Barger Thompson',
            'married': '13 Sep 1903',
        },
    ],
})

ENTRIES.append({
    'code': '725',
    'name': 'John Jacob Barnes',
    "source": {
        'pdf': 'James_Guthrie - Seven Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '22 Oct 1877',
    'died': '30 Sep 1963',
})

ENTRIES.append({
    'code': '72511',
    'name': 'Eli Carolyn zab Bames',
    "source": {
        'pdf': 'James_Guthrie - Seven Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '10 Jun 1941',
    'died': '29 Oct 1996',
})

ENTRIES.append({
    'code': '7252',
    'name': 'Edith Barnes',
    "source": {
        'pdf': 'James_Guthrie - Seven Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '10 Aug 1902',
})

ENTRIES.append({
    'code': '72521',
    'name': 'Wilkiam Edgar Slavins',
    "source": {
        'pdf': 'James_Guthrie - Seven Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '06 Aug 1927',
})

ENTRIES.append({
    'code': '72522',
    'name': 'Frances Ann Siavins',
    "source": {
        'pdf': 'James_Guthrie - Seven Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '23 Oct 1933',
})

ENTRIES.append({
    'code': '725222',
    'name': 'Thomsne Conley (Adena) Welch',
    "source": {
        'pdf': 'James_Guthrie - Seven Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '15 Feb 1960',
})

ENTRIES.append({
    'code': '73332',
    'name': 'James Ronald Barnes',
    "source": {
        'pdf': 'James_Guthrie - Seven Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '25 Aug 1955',
})

ENTRIES.append({
    'code': '73333',
    'name': 'Nancy Carolyn Barnes',
    "source": {
        'pdf': 'James_Guthrie - Seven Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '25 Apr 1957',
})

ENTRIES.append({
    'code': '741121',
    'name': 'Dule Eugene Guthrie',
    "source": {
        'pdf': 'James_Guthrie - Seven Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '11 Nov 1963',
})

ENTRIES.append({
    'code': '74114',
    'name': 'Betty Ruth Guthrie',
    "source": {
        'pdf': 'James_Guthrie - Seven Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '22 Jun 1943',
})

ENTRIES.append({
    'code': '7411513',
    'name': 'Cristen Richeli Blosser',
    "source": {
        'pdf': 'James_Guthrie - Seven Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '10 Jul 1984',
    'died': '29 Apr 1974',
})

ENTRIES.append({
    'code': '74116',
    'name': 'Delbert Glenn Guthrie',
    "source": {
        'pdf': 'James_Guthrie - Seven Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '01 Sep 1938',
})

ENTRIES.append({
    'code': '74118',
    'name': 'Thelma Jean Guthrie',
    "source": {
        'pdf': 'James_Guthrie - Seven Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '14 Nov 1973',
})

ENTRIES.append({
    'code': '741182',
    'name': 'Gary DeWayne Russell',
    "source": {
        'pdf': 'James_Guthrie - Seven Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '28 Oct 1961',
})

ENTRIES.append({
    'code': '74119',
    'name': 'Harvey Paul Guthrie',
    "source": {
        'pdf': 'James_Guthrie - Seven Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '14 Nov 1941',
})

ENTRIES.append({
    'code': '741194',
    'name': 'Harvey Paul Guthrie',
    "source": {
        'pdf': 'James_Guthrie - Seven Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '14 Jan 1984',
})

ENTRIES.append({
    'code': '7411B',
    'name': 'Carl Lee Guthrie',
    "source": {
        'pdf': 'James_Guthrie - Seven Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '27 Feb 1945',
})

ENTRIES.append({
    'code': '7411B1',
    'name': 'Carl Joseph Guthrie',
    "source": {
        'pdf': 'James_Guthrie - Seven Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '31 Jan 1968',
})

ENTRIES.append({
    'code': '7411D',
    'name': 'Helen Ann Guthrie',
    "source": {
        'pdf': 'James_Guthrie - Seven Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '23 Oct 1949',
})

ENTRIES.append({
    'code': '7411D1',
    'name': 'Susan Michella Fike',
    "source": {
        'pdf': 'James_Guthrie - Seven Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '25 Jun 1977',
})

ENTRIES.append({
    'code': '7411D2',
    'name': 'Beth Ann Fike',
    "source": {
        'pdf': 'James_Guthrie - Seven Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '03 Jan 1980',
})

ENTRIES.append({
    'code': '74121',
    'name': 'James W',
    "source": {
        'pdf': 'James_Guthrie - Seven Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '06 Aug 1930',
})

ENTRIES.append({
    'code': '741211',
    'name': 'An Ann Seese',
    "source": {
        'pdf': 'James_Guthrie - Seven Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '23 Nov 1953',
    'died': '07 Jan 1955',
})

ENTRIES.append({
    'code': '74122',
    'name': 'The Mac lma Scese',
    "source": {
        'pdf': 'James_Guthrie - Seven Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '01 Dec 1932',
})

ENTRIES.append({
    'code': '74123',
    'name': 'ThRay oras Seese',
    "source": {
        'pdf': 'James_Guthrie - Seven Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '19 Jun 1934',
})

ENTRIES.append({
    'code': '74126',
    'name': 'Mark Leeseese',
    "source": {
        'pdf': 'James_Guthrie - Seven Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '14 Jun 1976',
})

ENTRIES.append({
    'code': '74132',
    'name': 'Donald Ray Ritchey',
    "source": {
        'pdf': 'James_Guthrie - Seven Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '03 Oct 1935',
})

ENTRIES.append({
    'code': '741322',
    'name': 'Rodney Wayne Ritchey',
    "source": {
        'pdf': 'James_Guthrie - Seven Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '27 Dec 1959',
})

ENTRIES.append({
    'code': '74133',
    'name': 'Jane Louise Ritchey',
    "source": {
        'pdf': 'James_Guthrie - Seven Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '01 Jul 1959',
})

ENTRIES.append({
    'code': '741332',
    'name': 'William (Bobby) Dean Moore',
    "source": {
        'pdf': 'James_Guthrie - Seven Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '16 Sep 1939',
})

ENTRIES.append({
    'code': '74136',
    'name': 'Kenneth Dale Ritchey',
    "source": {
        'pdf': 'James_Guthrie - Seven Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '25 Nov 1944',
})

ENTRIES.append({
    'code': '741362',
    'name': 'Adam Shane Ritchey',
    "source": {
        'pdf': 'James_Guthrie - Seven Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '07 Aug 1972',
})

ENTRIES.append({
    'code': '74138',
    'name': 'Delm Georgeor Ritchey',
    "source": {
        'pdf': 'James_Guthrie - Seven Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '17 Nov 1942',
})

ENTRIES.append({
    'code': '7414',
    'name': 'Dora Guthrie',
    "source": {
        'pdf': 'James_Guthrie - Seven Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '24 Apr 1916',
})

ENTRIES.append({
    'code': '74142',
    'name': 'Ruth rene McNair',
    "source": {
        'pdf': 'James_Guthrie - Seven Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
})

ENTRIES.append({
    'code': '74144',
    'name': 'Dortha Jean McNair',
    "source": {
        'pdf': 'James_Guthrie - Seven Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
})

ENTRIES.append({
    'code': '741456',
    'name': 'Fred Allen Ulderich',
    "source": {
        'pdf': 'James_Guthrie - Seven Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '05 Feb 1983',
})

ENTRIES.append({
    'code': '7415',
    'name': 'Ada Bell Guthrie',
    "source": {
        'pdf': 'James_Guthrie - Seven Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '27 Sep 1921',
})

ENTRIES.append({
    'code': '74151',
    'name': 'Shirley Jane Boyd',
    "source": {
        'pdf': 'James_Guthrie - Seven Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '04 Dec 1937',
})

ENTRIES.append({
    'code': '7432',
    'name': 'Emma Harshbarger',
    "source": {
        'pdf': 'James_Guthrie - Seven Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '30 Jan 1906',
})

ENTRIES.append({
    'code': '74321',
    'name': 'Charles Ray Hileman',
    "source": {
        'pdf': 'James_Guthrie - Seven Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '18 Feb 1925',
})

ENTRIES.append({
    'code': '743212',
    'name': 'Cynthia Lee Hileman',
    "source": {
        'pdf': 'James_Guthrie - Seven Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '20 Apr 1951',
})

ENTRIES.append({
    'code': '743215',
    'name': 'Melissa Ann Hileman',
    "source": {
        'pdf': 'James_Guthrie - Seven Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '05 Nov 1961',
})

ENTRIES.append({
    'code': '74322',
    'name': 'Playford Gail Hileman',
    "source": {
        'pdf': 'James_Guthrie - Seven Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '07 Jan 1929',
})

ENTRIES.append({
    'code': '743221',
    'name': 'Tarm Lynn Hileman',
    "source": {
        'pdf': 'James_Guthrie - Seven Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '28 Jan 1960',
})

ENTRIES.append({
    'code': '7432221',
    'name': 'Garrett Steven Reed',
    "source": {
        'pdf': 'James_Guthrie - Seven Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '23 Mar 1977',
})

ENTRIES.append({
    'code': '7433',
    'name': 'Jeremiah Joseph Harshbarger',
    "source": {
        'pdf': 'James_Guthrie - Seven Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '04 Jul 1935',
})

ENTRIES.append({
    'code': '7436',
    'name': 'Mabel Viola Bartholomew',
    "source": {
        'pdf': 'James_Guthrie - Seven Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '27 Dec 1933',
})

ENTRIES.append({
    'code': '7445',
    'name': 'P(Polly) au Ann lin McNair',
    "source": {
        'pdf': 'James_Guthrie - Seven Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
})

ENTRIES.append({
    'code': '7461',
    'name': 'Clarence Edward Guthrie',
    "source": {
        'pdf': 'James_Guthrie - Seven Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '03 Nov 1956',
})

ENTRIES.append({
    'code': '74612',
    'name': 'Clair Edward Guthrie',
    "source": {
        'pdf': 'James_Guthrie - Seven Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '22 Sep 1961',
})

ENTRIES.append({
    'code': '746121',
    'name': 'Clair (CJ) Edward Guthrie',
    "source": {
        'pdf': 'James_Guthrie - Seven Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '19 Jul 1996',
})

ENTRIES.append({
    'code': '747111',
    'name': 'Elizabeth Ann Baysinger',
    "source": {
        'pdf': 'James_Guthrie - Seven Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '09 Jul 1976',
})

ENTRIES.append({
    'code': '74712',
    'name': 'Rebecca Jane Baysinger',
    "source": {
        'pdf': 'James_Guthrie - Seven Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '15 Sep 1964',
})

ENTRIES.append({
    'code': '74721',
    'name': 'Dovle Wavne Long',
    "source": {
        'pdf': 'James_Guthrie - Seven Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '03 Aug 1952',
})

ENTRIES.append({
    'code': '74722',
    'name': 'Nola Wade Long',
    "source": {
        'pdf': 'James_Guthrie - Seven Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
})

ENTRIES.append({
    'code': '74742',
    'name': 'Charles Howard Movers',
    "source": {
        'pdf': 'James_Guthrie - Seven Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '29 Jul 1957',
})

ENTRIES.append({
    'code': '74743',
    'name': 'William Ray Movers',
    "source": {
        'pdf': 'James_Guthrie - Seven Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '19 Dec 1961',
})

ENTRIES.append({
    'code': '7482',
    'name': 'The Pearl Lma Guthrie',
    "source": {
        'pdf': 'James_Guthrie - Seven Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '5 Feb 1930',
})

ENTRIES.append({
    'code': '7483',
    'name': 'Al Mae Ic Guthrie',
    "source": {
        'pdf': 'James_Guthrie - Seven Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '06 Oct 1932',
})

ENTRIES.append({
    'code': '748432',
    'name': 'Rebckah Jov Guthne',
    "source": {
        'pdf': 'James_Guthrie - Seven Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
})

ENTRIES.append({
    'code': '74844',
    'name': 'Darryl Lee Guthrie',
    "source": {
        'pdf': 'James_Guthrie - Seven Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '03 Jun 1987',
})

ENTRIES.append({
    'code': '748522',
    'name': 'Kristie Micolle Habenicht',
    "source": {
        'pdf': 'James_Guthrie - Seven Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '26 Sep 1987',
})

ENTRIES.append({
    'code': '74873',
    'name': 'Deborah Annette Bartholomew',
    "source": {
        'pdf': 'James_Guthrie - Seven Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '28 Nov 1990',
})

ENTRIES.append({
    'code': '74B3',
    'name': 'Evelvn lrene Bartholomew',
    "source": {
        'pdf': 'James_Guthrie - Seven Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '24 Sep 1926',
})

ENTRIES.append({
    'code': '74B32',
    'name': 'Joy Trene Miller',
    "source": {
        'pdf': 'James_Guthrie - Seven Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '18 Apr 1952',
})

ENTRIES.append({
    'code': '74B4',
    'name': 'Paul Eugene Bartholomew',
    "source": {
        'pdf': 'James_Guthrie - Seven Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '18 May 1928',
})

ENTRIES.append({
    'code': '74B422',
    'name': 'Adam Paul Lindquist',
    "source": {
        'pdf': 'James_Guthrie - Seven Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '24 Jul 1981',
})

ENTRIES.append({
    'code': '74B5',
    'name': 'Doro May Bartholomew',
    "source": {
        'pdf': 'James_Guthrie - Seven Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '31 May 1930',
})

ENTRIES.append({
    'code': '74B51',
    'name': 'Valerie Kay Habenicht',
    "source": {
        'pdf': 'James_Guthrie - Seven Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '14 Feb 1978',
})

ENTRIES.append({
    'code': '74B61',
    'name': 'Douglas Robert Hale',
    "source": {
        'pdf': 'James_Guthrie - Seven Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '24 Oct 1952',
})

ENTRIES.append({
    'code': '74B74',
    'name': 'Dwane Ira Bartholomew',
    "source": {
        'pdf': 'James_Guthrie - Seven Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '18 Apr 1968',
})

ENTRIES.append({
    'code': '7652',
    'name': 'Edn Mac Spiker',
    "source": {
        'pdf': 'James_Guthrie - Seven Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '13 Mar 1916',
})

ENTRIES.append({
    'code': '76521121',
    'name': 'Ash Renne Narivanchik',
    "source": {
        'pdf': 'James_Guthrie - Seven Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '24 Feb 1993',
})

ENTRIES.append({
    'code': '7652113',
    'name': 'William (Billy) Ralph Narivanchik',
    "source": {
        'pdf': 'James_Guthrie - Seven Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '30 Jul 1979',
})

ENTRIES.append({
    'code': '765212',
    'name': 'Paul Joseph Narivanchik',
    "source": {
        'pdf': 'James_Guthrie - Seven Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '14 Sep 1954',
})

ENTRIES.append({
    'code': '7653',
    'name': 'Mild Maud Re Spike D R',
    "source": {
        'pdf': 'James_Guthrie - Seven Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '20 Mar 1954',
})

ENTRIES.append({
    'code': '7654',
    'name': 'Shirel Victoria Spiker',
    "source": {
        'pdf': 'James_Guthrie - Seven Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
})

ENTRIES.append({
    'code': '76541',
    'name': 'Kermit Nelson DeBerry',
    "source": {
        'pdf': 'James_Guthrie - Seven Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '06 Dec 1937',
})

ENTRIES.append({
    'code': '765421',
    'name': 'Sherry Lynne Shea',
    "source": {
        'pdf': 'James_Guthrie - Seven Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '27 Jan 1963',
})

ENTRIES.append({
    'code': '7654221',
    'name': 'Kmsti Mane Shea',
    "source": {
        'pdf': 'James_Guthrie - Seven Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '03 Apr 1995',
})

ENTRIES.append({
    'code': '7655',
    'name': 'Thelma Olieta Spiker',
    "source": {
        'pdf': 'James_Guthrie - Seven Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '02 Dec 1921',
})

ENTRIES.append({
    'code': '76551',
    'name': 'Glad Kay Duncan',
    "source": {
        'pdf': 'James_Guthrie - Seven Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '07 Sep 1946',
})

ENTRIES.append({
    'code': '768422',
    'name': 'Kenneth Scot Shea',
    "source": {
        'pdf': 'James_Guthrie - Seven Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '05 Apr 1969',
})


# === Drafts extracted from john.txt by draft_from_ocr.py ===
ENTRIES.append({
    'code': '1132221',
    'name': 'Kathy Marie Frazee',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '20 Feb 1956',
    "spouses": [
        {
            'name': 'Fred Allen Baisley',
            'married': '07 Sep 1932',
        },
    ],
})

ENTRIES.append({
    'code': '11322221',
    'name': 'Jamie Lynn Balsiey',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
})

ENTRIES.append({
    'code': '11322222',
    'name': 'Brad Allan Balsicy',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '26 May 1988',
})

ENTRIES.append({
    'code': '1132232',
    'name': 'Alan Fraze',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '01 Jun 1973',
    'died': '26 Apr 1989',
    "spouses": [
        {
            'name': 'Charles G',
            'married': '20 Nov 1976',
        },
    ],
})

ENTRIES.append({
    'code': '12241112',
    'name': 'Ton Lea Livengood',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
})

ENTRIES.append({
    'code': '12241113',
    'name': 'Roger Lee (RJ) Livengood',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '11 Jun 1987',
})

ENTRIES.append({
    'code': '12241121',
    'name': 'Eliza Ellen beth MeNear',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '10 May 1971',
    'died': '31 Jul 1977',
})

ENTRIES.append({
    'code': '12241231',
    'name': 'Rebeoca Jean Selby',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '25 Jun 1974',
})

ENTRIES.append({
    'code': '12241251',
    'name': 'Dusty Durr',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '23 Apr 1981',
})

ENTRIES.append({
    'code': '1224143',
    'name': 'Stella Dartene Hoover',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '14 Aug 1958',
})

ENTRIES.append({
    'code': '12241431',
    'name': 'David S',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '11 Feb 1978',
})

ENTRIES.append({
    'code': '12241432',
    'name': 'Sessica Shaffer',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '11 Oct 1980',
    'died': '30 Aug 1990',
})

ENTRIES.append({
    'code': '12241442',
    'name': 'Tara Jean Braham',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '07 Jun 1961',
})

ENTRIES.append({
    'code': '1224147',
    'name': 'Lissa Lynn Hoover',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
})

ENTRIES.append({
    'code': '1224148',
    'name': 'David Allen Hoover',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '07 Mar 1972',
})

ENTRIES.append({
    'code': '12243121',
    'name': 'Willi Daleam DeBerry',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '27 Jan 1963',
})

ENTRIES.append({
    'code': '12243211',
    'name': 'Kayla Mane Kanosky',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '18 May 1988',
})

ENTRIES.append({
    'code': '1224331',
    'name': 'Michacl Nelson DeBerry',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '25 Mar 1961',
    'died': '01 Apr 1990',
})

ENTRIES.append({
    'code': '1224421',
    'name': 'Douglas Mark DeBerry',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '05 Sep 1959',
})

ENTRIES.append({
    'code': '1224431',
    'name': 'Robin Lynn DeBerry',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '14 Feb 1958',
})

ENTRIES.append({
    'code': '1224432',
    'name': 'Juhe Lee DeBerry',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '01 May 1960',
})

ENTRIES.append({
    'code': '12244321',
    'name': 'Brandie Christionna DeBerry',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '02 Aug 1980',
})

ENTRIES.append({
    'code': '12244322',
    'name': 'Chase Douglas DeBerry',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '30 Dec 1983',
})

ENTRIES.append({
    'code': '12244411',
    'name': 'Robert Eugene Goff',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '12 Nov 1974',
    "spouses": [
        {
            'name': 'Emest Lee Sargent',
        },
    ],
})

ENTRIES.append({
    'code': '1224442',
    'name': 'Wikma Lee Thomas',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '26 Oct 1957',
})

ENTRIES.append({
    'code': '1224444',
    'name': 'James Oliver Thomas',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '11 Apr 1961',
})

ENTRIES.append({
    'code': '1224445',
    'name': 'Christo Allen Thomas',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '22 Jul 1962',
})

ENTRIES.append({
    'code': '1224446',
    'name': 'Christina Alvena Thomas',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '22 Jul 1962',
})

ENTRIES.append({
    'code': '1224447',
    'name': 'Brvson Lynn Thomas',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '16 Sep 1964',
    "spouses": [
        {
            'name': 'James Metz',
            'married': '21 Feb 1942',
        },
    ],
})

ENTRIES.append({
    'code': '1224454',
    'name': 'Brian Timothy Jones',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '26 Dec 1969',
})

ENTRIES.append({
    'code': '1224471',
    'name': 'Ryan Lee DeBerry',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '12 May 1970',
})

ENTRIES.append({
    'code': '1224A11',
    'name': 'Timothy Roger DeBerry',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '07 Mar 1969',
})

ENTRIES.append({
    'code': '1231112',
    'name': 'Joseph Eugene Feency',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '12 Sep 1952',
})

ENTRIES.append({
    'code': '1231116',
    'name': 'Jennife Suc Feeney',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
})

ENTRIES.append({
    'code': '12332111',
    'name': 'RoLec nal Collins',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '09 Aug 1959',
})

ENTRIES.append({
    'code': '1233212',
    'name': 'William Lee Fike',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
})

ENTRIES.append({
    'code': '12332121',
    'name': 'Shervi Ann Fike',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '23 Nov 1969',
})

ENTRIES.append({
    'code': '12332124',
    'name': 'William Lee Fike',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
})

ENTRIES.append({
    'code': '12332125',
    'name': 'Scott Nich Fike',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    "spouses": [
        {
            'name': 'Randy B',
        },
    ],
})

ENTRIES.append({
    'code': '12332131',
    'name': 'Te Lynn rr Fike',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '16 Dec. 1965',
})

ENTRIES.append({
    'code': '12332132',
    'name': 'Co Suelit Thomas',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '10 Apr 1972',
})

ENTRIES.append({
    'code': '12332133',
    'name': 'Brvan Sharpe Thomas',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '21 Mar 1976',
})

ENTRIES.append({
    'code': '1233214',
    'name': 'Janet Sue Fike',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '28 Dec 1948',
})

ENTRIES.append({
    'code': '12332141',
    'name': 'Jerry Allen Valen Jr',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
})

ENTRIES.append({
    'code': '12332142',
    'name': 'Sharlene Sue Valentine',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
})

ENTRIES.append({
    'code': '12332143',
    'name': 'Gerald Allen Valentine',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    "spouses": [
        {
            'name': 'LoMille ra r',
        },
    ],
})

ENTRIES.append({
    'code': '1233217',
    'name': 'Jame Dale Fike',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
})

ENTRIES.append({
    'code': '12332171',
    'name': 'JamesDale Fike',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '10 Jun 1975',
})

ENTRIES.append({
    'code': '1233231',
    'name': 'Danicl J',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
})

ENTRIES.append({
    'code': '1233233',
    'name': 'Steven Lee Lewis',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
})

ENTRIES.append({
    'code': '1233234',
    'name': 'Disne Lynn Lew',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
})

ENTRIES.append({
    'code': '1233235',
    'name': 'Mack Arthur Lewis',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '07 Sep 1958',
})

ENTRIES.append({
    'code': '1233236',
    'name': 'Paul Kevin Lewis',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '07 Apr 1961',
    'died': '08 Oct 1977',
})

ENTRIES.append({
    'code': '1233242',
    'name': 'Edith Willis',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '31 Aug 1953',
})

ENTRIES.append({
    'code': '12332421',
    'name': 'Sus Kay san Pickerill',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '10 Apr 1976',
})

ENTRIES.append({
    'code': '12332422',
    'name': 'Nathan Lynn Pickerill',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '16 Dec 1977',
})

ENTRIES.append({
    'code': '12332423',
    'name': 'Emily Fay Pickerill',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
})

ENTRIES.append({
    'code': '12332424',
    'name': 'Sam Jacob Pickerill ua',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '05 Jul 1984',
})

ENTRIES.append({
    'code': '12332425',
    'name': 'Jesse William Pick',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '05 Jul 1955',
})

ENTRIES.append({
    'code': '12332431',
    'name': 'Jason Michael Willis',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '11 Jul 1977',
})

ENTRIES.append({
    'code': '1233252',
    'name': 'Deborah Kay Shaffer',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '04 Dec 1956',
    'died': '18 Apr 1988',
})

ENTRIES.append({
    'code': '12332521',
    'name': 'Jennifer Rence Shaffer',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '26 Apr 1986',
})

ENTRIES.append({
    'code': '12332611',
    'name': 'Kurtis Jackson Shaffer',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '13 Aug 1980',
})

ENTRIES.append({
    'code': '12332612',
    'name': 'Lori Beth Shaffer',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '21 Jan 1961',
})

ENTRIES.append({
    'code': '1233262',
    'name': 'Roger Lee Shaffer',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
})

ENTRIES.append({
    'code': '12332621',
    'name': 'Carla Marie Shaffer',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '16 Nov 1980',
    'died': '20 Jan 1996',
    "spouses": [
        {
            'name': 'Tammy Reckart',
            'married': '18 Jul 1965',
        },
    ],
})

ENTRIES.append({
    'code': '1233263',
    'name': 'Harold Stephen Shaffer',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '30 Jan 1964',
})

ENTRIES.append({
    'code': '1233511',
    'name': 'Debra Deal',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
})

ENTRIES.append({
    'code': '1233512',
    'name': 'Pamela Deal',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
})

ENTRIES.append({
    'code': '1236123',
    'name': 'Joe Beth Fnend',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '28 Feb 1960',
    "spouses": [
        {
            'name': 'Robert Morgan Kmeht CHILDREN',
            'married': 'Feb 1958',
        },
    ],
})

ENTRIES.append({
    'code': '1237132',
    'name': 'Lesa Jean Feather',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '19 Jul 1972',
    "spouses": [
        {
            'name': 'Kenneth Frazoc',
        },
    ],
})

ENTRIES.append({
    'code': '1321211',
    'name': 'Kenneth Frazec',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '1958',
})

ENTRIES.append({
    'code': '13212111',
    'name': 'Bridge Mare Frazee',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '1960',
})

ENTRIES.append({
    'code': '1321212',
    'name': 'Eddic Frazee',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '1960',
})

ENTRIES.append({
    'code': '13212121',
    'name': 'Carne Yvonne Fravec',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': 'Mar 1980',
})

ENTRIES.append({
    'code': '1321822',
    'name': 'Raellen Wittman',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': 'Nov 1995',
    "spouses": [
        {
            'name': 'Rudolph Havnila',
            'married': 'Jan 1927',
        },
    ],
})

ENTRIES.append({
    'code': '13223421',
    'name': 'Seth Andrew Guthrie',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
})

ENTRIES.append({
    'code': '13223422',
    'name': 'Jenna Mariah Guthric',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '23 Oct 1989',
})

ENTRIES.append({
    'code': '13261111',
    'name': 'Matthew Frank Kochtan',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '28 Dec 1973',
    "spouses": [
        {
            'name': 'Peggy Whitaker',
            'married': '10 Dec 1949',
        },
    ],
})

ENTRIES.append({
    'code': '13261121',
    'name': 'Amy Heather Lawson',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
})

ENTRIES.append({
    'code': '13261122',
    'name': 'Sarah Elizabeth Lawson',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '16 Jun 1986',
    "spouses": [
        {
            'name': 'Maun Hardy',
            'married': '09 Jan 1947',
        },
    ],
})

ENTRIES.append({
    'code': '1326114',
    'name': 'Nina Lawson',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '28 Jan 1953',
    'died': '20 Jul 1994',
    "spouses": [
        {
            'name': 'Mervin Wade Frnend',
            'married': '21 Mar 1931',
        },
    ],
})

ENTRIES.append({
    'code': '13261211',
    'name': 'Seth Augustus Lawson',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '27 Dec 1982',
})

ENTRIES.append({
    'code': '1326142',
    'name': 'Tonya Marie Lawson',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '04 Oct 1975',
    "spouses": [
        {
            'name': 'Todd Bednarz CHILDREN',
            'married': '12 Nov 1995',
        },
    ],
})

ENTRIES.append({
    'code': '1326241',
    'name': 'Alice Kay Lawson',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': 'About 1975',
    "spouses": [
        {
            'name': 'Annabelle Sypolt',
        },
    ],
})

ENTRIES.append({
    'code': '1326411',
    'name': 'Michact Lyn Lawson',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '25 Oct 1954',
})

ENTRIES.append({
    'code': '1326413',
    'name': 'Marlin Robert Lawson',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '25 Oct 1954',
})

ENTRIES.append({
    'code': '13264131',
    'name': 'Amic Beth Lawson',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '21 Jan 1978',
})

ENTRIES.append({
    'code': '13264132',
    'name': 'Nicho Paul Lawson',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '14 Jul 1982',
})

ENTRIES.append({
    'code': '1345113',
    'name': 'James Harold Shafer',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '09 Mar 1946',
})

ENTRIES.append({
    'code': '135412',
    'name': 'Jean Windell',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '05 May 1898',
    'died': '03 Mar 1983',
})

ENTRIES.append({
    'code': '13631231',
    'name': 'James Edward McCany',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '01 Dec 1977',
})

ENTRIES.append({
    'code': '13631321',
    'name': 'Dawn Machelle Shafer',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '26 Nov 1972',
})

ENTRIES.append({
    'code': '1363162',
    'name': 'George McKinley Shafer',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '23 Jul 1954',
})

ENTRIES.append({
    'code': '1363178',
    'name': 'Cheryl Leigh Kumpel',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '10 Jan 1968',
})

ENTRIES.append({
    'code': '13634',
    'name': 'Cora Hauger',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '15 Jan 1294',
    'died': '22 Apr 1978',
    "spouses": [
        {
            'name': 'Oukev Reckart',
            'married': '15 Jan 1294',
        },
    ],
})

ENTRIES.append({
    'code': '13635156',
    'name': 'Amelia Jane Shafer',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '18 Mar 1961',
})

ENTRIES.append({
    'code': '1365112',
    'name': 'Janct Louise Shafer',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '12 Jun 1943',
})

ENTRIES.append({
    'code': '13651131',
    'name': 'Janene Lynn Shafer',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '31 May 1975',
})

ENTRIES.append({
    'code': '1365114',
    'name': 'Infant',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '20 Jan 1948',
    'died': '30 Jan 1947',
})

ENTRIES.append({
    'code': '1365116',
    'name': 'Margaret Janc Shafer',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '05 Jan 1949',
})

ENTRIES.append({
    'code': '13651162',
    'name': 'Jamic Bolvard',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
})

ENTRIES.append({
    'code': '1365117',
    'name': 'Mary Alice Shafer',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '01 Jun 1953',
    'died': '13 Mar 1981',
})

ENTRIES.append({
    'code': '13651171',
    'name': 'Joseph Arthur Lewis',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '14 Dec 1969',
})

ENTRIES.append({
    'code': '13651172',
    'name': 'Christina Mane Shafer',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '02 Oct 1975',
})

ENTRIES.append({
    'code': '13651174',
    'name': 'Lester Grant Shafer',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
})

ENTRIES.append({
    'code': '1365118',
    'name': 'Mary Alice Shafer',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '08 Oct 1933',
})

ENTRIES.append({
    'code': '1365119',
    'name': 'Lind June Shafer',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '24 Jun 1952',
})

ENTRIES.append({
    'code': '13651211',
    'name': 'Mic Ray Collins',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '21 Jun 1949',
})

ENTRIES.append({
    'code': '13651221',
    'name': 'Ene Lec Fnend',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '10 Aug 1967',
})

ENTRIES.append({
    'code': '1365123',
    'name': 'CHARLES RICHARD McCARTY',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '08 Jun 1952',
})

ENTRIES.append({
    'code': '13651232',
    'name': 'Am Leannber McCarty',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '10 Jun 1982',
})

ENTRIES.append({
    'code': '1365124',
    'name': 'DA WARD VI McCARTY D',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '20 Sep 1958',
    'died': '03 Sep 1985',
    "spouses": [
        {
            'name': 'Yvette Rexroad',
            'married': 'Jul 1984',
        },
    ],
})

ENTRIES.append({
    'code': '13651313',
    'name': 'Shirley Burgess',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '03 Jun 1965',
    "spouses": [
        {
            'name': 'Timothy Miller',
            'married': '08 Jul 1994',
        },
    ],
})

ENTRIES.append({
    'code': '1365132',
    'name': 'Mary Ann Sisler',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '02 Sep 1943',
    'died': '03 Jul 1990',
})

ENTRIES.append({
    'code': '1365133',
    'name': 'Hub Martin Sisler',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '07 Mar 1958',
})

ENTRIES.append({
    'code': '13651331',
    'name': 'Thelma Lou Sisler',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '02 Dec 1980',
})

ENTRIES.append({
    'code': '1365141',
    'name': 'Vivion Leah Shafer',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '02 Nov 1946',
    'died': '13 Apr 1996',
})

ENTRIES.append({
    'code': '13651412',
    'name': 'Patricia Daricen Rvan',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '17 Feb 1970',
})

ENTRIES.append({
    'code': '1365143',
    'name': 'Donald Franklin Shafer',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '11 Jan 1961',
})

ENTRIES.append({
    'code': '13651431',
    'name': 'Sarah Elizabeth Reese',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '01 Jun 1973',
    'died': '05 Apr 1975',
})

ENTRIES.append({
    'code': '1365152',
    'name': 'Anthony Thomas Shafer',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '10 Mar 1952',
    'died': '20 May 1957',
})

ENTRIES.append({
    'code': '13651531',
    'name': 'Matthew Wayne Gibson',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '18 Sep 1974',
})

ENTRIES.append({
    'code': '13651562',
    'name': 'Stephanie Jean Olde',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '04 Jun 1949',
})

ENTRIES.append({
    'code': '1365157',
    'name': 'Predy Junior Shafer',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'died': '02 Feb 1959',
})

ENTRIES.append({
    'code': '13651741',
    'name': 'Michelle Lynn Krimpel',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '17 Jun 1970',
})

ENTRIES.append({
    'code': '1365175',
    'name': 'Lathan Carr Krimpel',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '09 Aug 1956',
})

ENTRIES.append({
    'code': '13651751',
    'name': 'Bryan Keith Krimpel',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
})

ENTRIES.append({
    'code': '13651752',
    'name': 'Bradley Michael Krimpel',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
})

ENTRIES.append({
    'code': '1365176',
    'name': 'Joseph J',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'died': '28 May 1957',
})

ENTRIES.append({
    'code': '1365177',
    'name': 'Alice Mae Krimpel',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '18 Sep 1956',
    "spouses": [
        {
            'name': 'Candy Reckner CHILDEN',
        },
    ],
})

ENTRIES.append({
    'code': '13651811',
    'name': 'Antho Allen Castecl',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '21 Oct 1948',
    'died': '22 Jul 1972',
})

ENTRIES.append({
    'code': '1365191',
    'name': 'Rov Lee Sister',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
})

ENTRIES.append({
    'code': '1365192',
    'name': 'Rich David Sisler',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '17 Oct 1949',
})

ENTRIES.append({
    'code': '13651921',
    'name': 'David Roy Sisler',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '26 Oct 1972',
})

ENTRIES.append({
    'code': '13651922',
    'name': 'Dan Ray Sissler',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '25 Sep 1973',
})

ENTRIES.append({
    'code': '1365193',
    'name': 'Adra Ann Sisler',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '10 Mar 1953',
    'died': '9 Jul 1945',
})

ENTRIES.append({
    'code': '1365194',
    'name': 'Linda Lou Sisler',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '13 Apr 1952',
})

ENTRIES.append({
    'code': '13651962',
    'name': 'Douglas Eugene Sisler',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '17 May 1978',
})

ENTRIES.append({
    'code': '13651A2',
    'name': 'Olaf Dwayne Shafer',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '19 Sep 1957',
})

ENTRIES.append({
    'code': '13651A31',
    'name': 'Donald Franklin Shafer',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '27 Feb 1959',
})

ENTRIES.append({
    'code': '13651C1',
    'name': 'Monika Crystal Shafer',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '12 Mar 1960',
})

ENTRIES.append({
    'code': '13651C2',
    'name': 'Anita Maric Shafer',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '05 Feb 1961',
    'died': '03 Dec 1979',
    "spouses": [
        {
            'name': 'Arlene Mock CHILDREN',
            'married': '04 Dec 1955',
        },
    ],
})

ENTRIES.append({
    'code': '13651C21',
    'name': 'Tami Marie Treas',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '04 Apr 1982',
})

ENTRIES.append({
    'code': '1368156',
    'name': 'Am Jane Eli Shafer',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
})

ENTRIES.append({
    'code': '1382122',
    'name': 'Robert Scott Seamon',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '25 Apr 1955',
    'died': '16 Apr 1967',
})

ENTRIES.append({
    'code': '13821541',
    'name': 'Shame Scamon',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '20 Jul 1994',
})

ENTRIES.append({
    'code': '1384451',
    'name': 'Melisha Philips',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '10 Dec 1971',
})

ENTRIES.append({
    'code': '1384452',
    'name': 'Machella Philips',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': 'Jul 1968',
    'died': 'Jun 1976',
    "spouses": [
        {
            'name': 'Ward Sisler',
        },
    ],
})

ENTRIES.append({
    'code': '13B2112',
    'name': 'Wilham Ronald Sines',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '26 Jul 1946',
})

ENTRIES.append({
    'code': '13B2114',
    'name': 'Thomas Eugene Sines',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    "spouses": [
        {
            'name': 'Donna Knapp',
        },
    ],
})

ENTRIES.append({
    'code': '13B2115',
    'name': 'Cathyv Ann Sines',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
})

ENTRIES.append({
    'code': '13B2133',
    'name': 'Melva Susan Abbey',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '26 Dec 1953',
    "spouses": [
        {
            'name': 'Paul Benna',
        },
    ],
})

ENTRIES.append({
    'code': '13B21332',
    'name': 'Cora Robin Ervin',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '08 May 1976',
})

ENTRIES.append({
    'code': '13B2154',
    'name': 'Eric Donald Scamon',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '10 Jul 1970',
})

ENTRIES.append({
    'code': '13C5122',
    'name': 'Tamara Lynn Smith',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '24 dec 1966',
    'died': '02 Nov 1969',
    "spouses": [
        {
            'name': 'Kay Hevner',
            'married': '16 Jan 1977',
        },
    ],
})

ENTRIES.append({
    'code': '13F32',
    'name': 'Ezra Grant Guthrieb',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
})

ENTRIES.append({
    'code': '13F7272',
    'name': 'Tiffany Jo Rockart',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '11 May 1983',
})

ENTRIES.append({
    'code': '13F7411',
    'name': 'Angela Virginia Spreng',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '22 Jun 1978',
})

ENTRIES.append({
    'code': '13F7412',
    'name': 'Melissa Spreng',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '05 Mar 1983',
    'died': '01 Sep 1964',
})

ENTRIES.append({
    'code': '1415413',
    'name': 'Robert E',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '05 Feb 1980',
    'died': '11 Jul 1990',
    "spouses": [
        {
            'name': 'Ricky Marchi',
            'married': '10 Jun 1978',
        },
    ],
})

ENTRIES.append({
    'code': '1425231',
    'name': 'Ar Louise vet Nicola',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '16 Sep 1953',
})

ENTRIES.append({
    'code': '1425232',
    'name': 'Cather Ann Nicola',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '29 Aug 1962',
})

ENTRIES.append({
    'code': '1425233',
    'name': 'Barba Grace Nicola',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '13 Oct 1956',
})

ENTRIES.append({
    'code': '1425234',
    'name': 'Robert Eugene Nicola',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '29 Aug 1962',
})

ENTRIES.append({
    'code': '14252411',
    'name': 'Samantha Hope Whipkey',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
})

ENTRIES.append({
    'code': '1425242',
    'name': 'Tamra Lynn Whipkev',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '28 Feb 1954',
    "spouses": [
        {
            'name': 'Shadv Grove Church to Oakey Stanley',
            'married': '24 Jul 1986',
        },
    ],
})

ENTRIES.append({
    'code': '14252421',
    'name': 'Travis Cody Gatian',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '19 Oct 1985',
})

ENTRIES.append({
    'code': '1432931',
    'name': 'Dwam Scese',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '21 Aug 1980',
    "spouses": [
        {
            'name': 'Betty',
            'married': '19 Oct 1950',
        },
    ],
})

ENTRIES.append({
    'code': '144135',
    'name': 'Wilm Maric Sisler',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '17 Feb 1946',
})

ENTRIES.append({
    'code': '1441511',
    'name': 'Anita Louise Sister',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '15 Oct 1965',
    "spouses": [
        {
            'name': 'Betty -',
            'married': '19 Oct 1950',
        },
    ],
})

ENTRIES.append({
    'code': '144224',
    'name': 'Carl R',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
})

ENTRIES.append({
    'code': '144227',
    'name': 'Jacob George Nicola',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '27 May 1960',
})

ENTRIES.append({
    'code': '14431',
    'name': 'Wilham Ralph Harshbar',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '16 Oct 1906',
})

ENTRIES.append({
    'code': '14431111',
    'name': 'Sabrina Louise Narivanchik',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '06 Sep 1971',
})

ENTRIES.append({
    'code': '14431113',
    'name': 'Witham (Billy) Ralph Narivanb',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '14 Sep 1954',
})

ENTRIES.append({
    'code': '1443112',
    'name': 'Paul Joseph Narivanchik',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '02 Jan 1957',
})

ENTRIES.append({
    'code': '14431121',
    'name': 'Kara Elizabeth',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '02 Jul 1962',
})

ENTRIES.append({
    'code': '14431122',
    'name': 'Alic Maric Sonntag',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '04 Aug 1970',
})

ENTRIES.append({
    'code': '14431131',
    'name': 'Robert Joseph Yingling Ill',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '28 May 1976',
})

ENTRIES.append({
    'code': '144321',
    'name': 'Anna Marie Harshbarger',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '05 Jun 1935',
})

ENTRIES.append({
    'code': '144322',
    'name': 'Mary Ellen Harshbarger',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '06 Feb 1937',
})

ENTRIES.append({
    'code': '144323',
    'name': 'Shirley Mac Harsh',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
})

ENTRIES.append({
    'code': '144332',
    'name': 'Glenna Catherine Spiker',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '20 Sep 1941',
    'died': '20 May 1997',
    "spouses": [
        {
            'name': 'Jean Howdershett Charlotte Groves Larry Groves il P',
            'married': '28 Jun 1920',
        },
    ],
})

ENTRIES.append({
    'code': '144341',
    'name': 'Harson (Teddy) Theodore Harshbarge r',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '07 Apr 1913',
})

ENTRIES.append({
    'code': '1443413',
    'name': 'Cry Dawn Sta Groves',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '20 Feb 1967',
})

ENTRIES.append({
    'code': '144343',
    'name': 'Linda Grace Smith',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '03 Jan 1949',
})

ENTRIES.append({
    'code': '144352',
    'name': 'Aivin Francis Fresh',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '21 May 1939',
})

ENTRIES.append({
    'code': '144353',
    'name': 'Dons Jean Fresh',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '04 Nov 1943',
})

ENTRIES.append({
    'code': '144354',
    'name': 'Infant Daughter',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '04 Nov 1943',
    'died': '05 Nov 1943',
})

ENTRIES.append({
    'code': '144356',
    'name': 'Betty Mae Fresh',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '16 Nov 1917',
})

ENTRIES.append({
    'code': '14436',
    'name': 'May Thomas Harshbarger',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '03 Apr 1916',
    'died': '13 Apr 1916',
})

ENTRIES.append({
    'code': '144371',
    'name': 'Barbara Jean Harshbarecr',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '27 Mar 1936',
})

ENTRIES.append({
    'code': '14438',
    'name': 'Pearl Catherine Harshbarger',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '02 Jul 1919',
})

ENTRIES.append({
    'code': '144381',
    'name': 'Infant son',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '14 Apr 1946',
    'died': '12 Aug 1943',
})

ENTRIES.append({
    'code': '144382',
    'name': 'Ross Carlton Miller',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '14 Apr 1946',
})

ENTRIES.append({
    'code': '144383',
    'name': 'Nor Jeanma Miller',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '22 Feb 1923',
})

ENTRIES.append({
    'code': '1443A',
    'name': 'Myrtic Grace Harshbar',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
})

ENTRIES.append({
    'code': '1443A1',
    'name': 'Veri Junior Smith',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '06 Jun 1943',
})

ENTRIES.append({
    'code': '1443A2',
    'name': 'Ronald Kenneth Smith',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '28 Feb 1947',
})

ENTRIES.append({
    'code': '1443B',
    'name': 'Daisy Bell Harshbarger',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '11 Feb 1925',
})

ENTRIES.append({
    'code': '1443C11',
    'name': 'Jennifer Lynn Sager',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '14 Oct 1980',
})

ENTRIES.append({
    'code': '1443C2',
    'name': 'RicErvin har Sager',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '07 Nov 1949',
    'died': '21 Oct 1972',
    "spouses": [
        {
            'name': 'McCartw FRIEND',
            'married': '11 Sep 1978',
        },
    ],
})

ENTRIES.append({
    'code': '1443C21',
    'name': 'Richard Alicn Sager',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '01 Jan 1977',
    'died': '01 Apr 1995',
})

ENTRIES.append({
    'code': '14453111',
    'name': 'Nicholas Ray',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '09 Aug 1980',
})

ENTRIES.append({
    'code': '14453112',
    'name': 'Jennifer Alynn Spiker',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '08 Jul 1983',
})

ENTRIES.append({
    'code': '1445312',
    'name': 'Ra Dale ndy Spiker',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '25 Jul 1968',
    "spouses": [
        {
            'name': 'Patricia (Patty) Smith',
        },
    ],
})

ENTRIES.append({
    'code': '14453121',
    'name': 'Ryan Dale Spiker',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '23 Feb 1990',
})

ENTRIES.append({
    'code': '14454111',
    'name': 'Sheresha Mane Groves',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
})

ENTRIES.append({
    'code': '14454131',
    'name': 'Joshua Charles Monroe',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '25 Sep 1992',
})

ENTRIES.append({
    'code': '14454132',
    'name': 'Seth Allan Monro',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '17 Oct 1957',
})

ENTRIES.append({
    'code': '144741',
    'name': 'An Pearl Thomas',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '05 May 1958',
})

ENTRIES.append({
    'code': '1447421',
    'name': 'Hillary Thomas',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '30 Apr 1994',
})

ENTRIES.append({
    'code': '1447611',
    'name': 'Steven Paul Thomas',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '25 Mar 1980',
})

ENTRIES.append({
    'code': '1471831',
    'name': 'Eric Benton Braums',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '21 Jun 1937',
})

ENTRIES.append({
    'code': '14751111',
    'name': 'Timothy Grayson Wotning',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '02 Feb 1977',
})

ENTRIES.append({
    'code': '1475112',
    'name': 'Kathy Mane Appleby',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '02 Jul 1959',
})

ENTRIES.append({
    'code': '14751121',
    'name': 'Ashicy Mane Spindler',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '23 Sep 1984',
})

ENTRIES.append({
    'code': '14751122',
    'name': 'Nicole Elizabeth Spindler',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '31 Jul 1994',
})

ENTRIES.append({
    'code': '1475113',
    'name': 'Scott Harold App',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '14 Dec 1962',
})

ENTRIES.append({
    'code': '147512',
    'name': 'Richard Harland Appleby',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '21 May 1936',
})

ENTRIES.append({
    'code': '1475122',
    'name': 'Terri Lynn Appleby',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '02 Jun 1960',
})

ENTRIES.append({
    'code': '14751221',
    'name': 'Amy Jo Bloom',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
})

ENTRIES.append({
    'code': '14751222',
    'name': 'Chad Allen Bloom',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
})

ENTRIES.append({
    'code': '147513',
    'name': 'Sandra Fave Appleby',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '24 Sep 1937',
})

ENTRIES.append({
    'code': '1475131',
    'name': 'Linda Carol Wolfe',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '23 Jun 1957',
    'died': '04 Jun 1990',
    "spouses": [
        {
            'name': 'Howard Lewis',
        },
    ],
})

ENTRIES.append({
    'code': '14751314',
    'name': 'Brian Keith Cuppett',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '11 Mar 1976',
})

ENTRIES.append({
    'code': '1475132',
    'name': 'Shelda Lee Wolfe',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '26 May 1961',
})

ENTRIES.append({
    'code': '14751321',
    'name': 'Hol Ann Wotring',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '02 jan 1980',
})

ENTRIES.append({
    'code': '14751322',
    'name': 'Meg Lee Wotring',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '16 Jun 1983',
})

ENTRIES.append({
    'code': '1475133',
    'name': 'She Lynn Wolfe',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '13 Feb 1960',
    "spouses": [
        {
            'name': 'Kellie Frie daw of Larry nd',
        },
    ],
})

ENTRIES.append({
    'code': '1475134',
    'name': 'Charles Rov Wolfe',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '27 Apr 1970',
})

ENTRIES.append({
    'code': '14751341',
    'name': 'Wyatt Christop Wolfe',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '24 Apr 1960',
    "spouses": [
        {
            'name': 'Henry Theod (Ted) Inman',
            'married': '12 Sep 1964',
        },
    ],
})

ENTRIES.append({
    'code': '147514',
    'name': 'Nancy Lee Appleby',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '01 Oct 1938',
})

ENTRIES.append({
    'code': '1475142',
    'name': 'Deborah Ann Gregory',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '24 Apr 1960',
})

ENTRIES.append({
    'code': '1475143',
    'name': 'Barbar Ann a Gregory',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '08 Sep 1965',
})

ENTRIES.append({
    'code': '147515',
    'name': 'Carol Ann Appleby',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '28 Jun 1944',
    'died': '14 Apr 1963',
    "spouses": [
        {
            'name': 'Omer R Cummingham',
            'married': '04 Jun 1935',
        },
    ],
})

ENTRIES.append({
    'code': '1475151',
    'name': 'Stove Miller',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '21 Feb 1966',
    'died': '04 Jun 1972',
})

ENTRIES.append({
    'code': '147611',
    'name': 'Betty Jean Buchb',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
})

ENTRIES.append({
    'code': '147621',
    'name': 'Larry Brady',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '22 Sep 1946',
    'died': '27 Nov 1951',
})

ENTRIES.append({
    'code': '147631',
    'name': 'Harold Ray Dice',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '16 Sep 1949',
})

ENTRIES.append({
    'code': '147632',
    'name': 'Rebecca Anna Dice',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '28 Aug 1954',
    'died': 'Sep 1959',
})

ENTRIES.append({
    'code': '148113',
    'name': 'Brenda G',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '22 Nov 1945',
})

ENTRIES.append({
    'code': '148114',
    'name': 'Jerry L',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '27 Aug 1947',
})

ENTRIES.append({
    'code': '148121',
    'name': 'Mary Ann Bowden',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '22 Aug 1939',
})

ENTRIES.append({
    'code': '148131',
    'name': 'Nancy Diane Bartha',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '02 Aug 1942',
})

ENTRIES.append({
    'code': '148212',
    'name': 'Phillis Rae Guthnie',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '08 Jun 1952',
    "spouses": [
        {
            'name': 'Charlies RIE',
            'married': '25 Jan 1924',
        },
    ],
})

ENTRIES.append({
    'code': '148611',
    'name': 'Virginia Ann Harbarger',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '05 Dec 1947',
})

ENTRIES.append({
    'code': '148811',
    'name': 'Peter E',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
})

ENTRIES.append({
    'code': '148812',
    'name': 'James Ray Brandgard',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '27 Jun 1955',
    'died': '16 May 1960',
})

ENTRIES.append({
    'code': '1611111',
    'name': 'Mark Stephen Fanto',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '24 Mar 1958',
    "spouses": [
        {
            'name': 'Jeff John French',
            'married': '12 Sep 1964',
        },
    ],
})

ENTRIES.append({
    'code': '1611221',
    'name': 'David Earl Cuppe IV',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '17 Oct 1970',
})

ENTRIES.append({
    'code': '161132',
    'name': 'Bar Gene ba Bickel',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '01 Dec 1947',
})

ENTRIES.append({
    'code': '161133',
    'name': 'Cynthia Jane Bickel',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '30 Mar 1916',
    'died': '15 May 1985',
})

ENTRIES.append({
    'code': '1611332',
    'name': 'Melissa Lynn Shannon',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '31 May 1960',
})

ENTRIES.append({
    'code': '162212',
    'name': 'Reb Jane Bavs ecinge ca r',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '15 Sep 1964',
    'died': '23 Jun 1981',
})

ENTRIES.append({
    'code': '162221',
    'name': 'Dovie Wavne Long',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '03 Aug 1952',
})

ENTRIES.append({
    'code': '162222',
    'name': 'Nolan Wade Long',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '04 Dec 1953',
})

ENTRIES.append({
    'code': '1622221',
    'name': 'Jordan Tobias long',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '15 Jul 1983',
})

ENTRIES.append({
    'code': '162223',
    'name': 'Carma Long',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
})

ENTRIES.append({
    'code': '162231',
    'name': 'Catherine Louise Sines',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '28 Feb 1954',
})

ENTRIES.append({
    'code': '162232',
    'name': 'Wendy Gay Sines',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '13 Feb 1963',
})

ENTRIES.append({
    'code': '162241',
    'name': 'Diana Suc Moyers',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '05 Jul 1954',
    'died': '16 Apr 1970',
    "spouses": [
        {
            'name': 'James lotte Walls',
            'married': '25 Nov 1917',
        },
    ],
})

ENTRIES.append({
    'code': '1622411',
    'name': 'Daniel Arron Hewitt',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '24 Jul 1977',
    "spouses": [
        {
            'name': 'Nanev L Valisko',
            'married': '12 Feb 1936',
        },
    ],
})

ENTRIES.append({
    'code': '1623111',
    'name': 'Mark Spear',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
})

ENTRIES.append({
    'code': '1623112',
    'name': 'Sean Spear',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '09 Jan 1969',
    "spouses": [
        {
            'name': 'James Walls',
        },
    ],
})

ENTRIES.append({
    'code': '162321',
    'name': 'Judith Anna McMillen',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '28 Dec 1946',
})

ENTRIES.append({
    'code': '162322',
    'name': 'Joyce Ella McMillen',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '22 Apr 1951',
    'died': '21 Mar 1992',
})

ENTRIES.append({
    'code': '162352',
    'name': 'Perry Hubert Movers',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '29 Mar 1959',
})

ENTRIES.append({
    'code': '162353',
    'name': 'Clarence Wade Movers',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '03 Dec 1961',
    'died': '25 Oct 1989',
})

ENTRIES.append({
    'code': '162371',
    'name': 'Kim Laram Movers',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '17 Mar 1951',
    'died': '09 Jan 1960',
})

ENTRIES.append({
    'code': '1623721',
    'name': 'Scott Movers',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '1975',
    "spouses": [
        {
            'name': 'Pamels Youst CHILDREN',
            'married': 'Aug 1985',
        },
    ],
})

ENTRIES.append({
    'code': '162412',
    'name': 'Paulette Mane Wright',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '23 Mar 1957',
})

ENTRIES.append({
    'code': '163111',
    'name': 'John Robert Tagger',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '25 Mar 1926',
})

ENTRIES.append({
    'code': '163112',
    'name': 'Clara Rosalie Tagga',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '26 Sep 1909',
})

ENTRIES.append({
    'code': '1631121',
    'name': 'Robert Kyle Weaver',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '20 Aug 1951',
})

ENTRIES.append({
    'code': '1631122',
    'name': 'Thomas William Weaver',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '06 Dec 1954',
})

ENTRIES.append({
    'code': '16311221',
    'name': 'Justi Fellix Weaver',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
})

ENTRIES.append({
    'code': '16311222',
    'name': 'Jesse Charles Weaver',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
})

ENTRIES.append({
    'code': '163121',
    'name': 'Mary Maxine Nicola',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '03 Aug 1930',
    'died': '02 Mar 1931',
})

ENTRIES.append({
    'code': '163123',
    'name': 'Robert Eugene Nicola',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '26 Mar 1934',
    'died': '30 Jan 1980',
})

ENTRIES.append({
    'code': '1631231',
    'name': 'Arveta Louise Nicola',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '16 Sep 1953',
    'died': '21 Feb 1988',
    "spouses": [
        {
            'name': 'Llovd (Red) Jackson Hall',
            'married': 'Sep 1923',
        },
    ],
})

ENTRIES.append({
    'code': '16312311',
    'name': 'Amy Noel Hammons',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '23 Dec 1974',
})

ENTRIES.append({
    'code': '16312312',
    'name': 'Jillian Jean Hammons',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '07 Aug 1975',
})

ENTRIES.append({
    'code': '16312341',
    'name': 'Robert Theodore (Teddy) Nicola',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '20 Oct 1981',
})

ENTRIES.append({
    'code': '1631242',
    'name': 'Tamra Lynn Whipkey',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '09 Jan 1968',
})

ENTRIES.append({
    'code': '16312421',
    'name': 'Travis Cody Gatian',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '19 Oct 1985',
})

ENTRIES.append({
    'code': '16314211',
    'name': 'Christine Lloyd Parnell',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '03 Mar 1970',
    "spouses": [
        {
            'name': 'Shady Grove Church to Yvonne Larosa Morcland',
            'married': '12 Nov 1961',
        },
    ],
})

ENTRIES.append({
    'code': '16314231',
    'name': 'Dean Alan Moye',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
})

ENTRIES.append({
    'code': '16314232',
    'name': 'Jeremy Colt Moyers',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '23 Sep 1982',
})

ENTRIES.append({
    'code': '1631424',
    'name': 'Darie Louise Movers',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '24 Feb 1959',
})

ENTRIES.append({
    'code': '163143',
    'name': 'Robert M Collin',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'died': '1940',
})

ENTRIES.append({
    'code': '163144',
    'name': 'Larry Robert Collins',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '03 Feb 1932',
    'died': '06 Jul 1989',
})

ENTRIES.append({
    'code': '16315211',
    'name': 'Jarrett John Walters',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '28 Oct 1990',
})

ENTRIES.append({
    'code': '163161',
    'name': 'Stanley Ray Moody',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '09 Jun 1940',
})

ENTRIES.append({
    'code': '1631612',
    'name': 'Debra Lynn Moody',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '27 Oct 1964',
})

ENTRIES.append({
    'code': '163171',
    'name': 'Betty Carol Cramer',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '31 Dec 1946',
    'died': '26 Dec 1993',
})

ENTRIES.append({
    'code': '163182',
    'name': 'Jarme Judson Nicola',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '26 Jun 1954',
})

ENTRIES.append({
    'code': '163183',
    'name': 'Kumberiy Rae Nicola',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '20 Sep 1964',
})

ENTRIES.append({
    'code': '164111',
    'name': 'Theodore Ralph Narivanchik',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '07 Sep 1949',
})

ENTRIES.append({
    'code': '16411111',
    'name': 'Casey Cayenne Martin',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '16 Feb 1993',
})

ENTRIES.append({
    'code': '16411121',
    'name': 'Ashicy Renee Narivanb',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
})

ENTRIES.append({
    'code': '164112',
    'name': 'Paul Joseph Narvanchik',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '14 Sep 1954',
    'died': '02 Apr 1988',
    "spouses": [
        {
            'name': 'Paul Fike',
            'married': '26 Apr 1968',
        },
    ],
})

ENTRIES.append({
    'code': '1641131',
    'name': 'Robert Joseph Yingling Ill',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '28 May 1976',
})

ENTRIES.append({
    'code': '1641132',
    'name': 'Kimberlic Mae Edwards',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '13 Feb 1979',
    "spouses": [
        {
            'name': 'Larry Lee CHILDREN',
        },
    ],
})

ENTRIES.append({
    'code': '1642311',
    'name': 'Joel Joseph Peterman',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '17 Apr 1989',
})

ENTRIES.append({
    'code': '164311',
    'name': 'Lida Rose Harsh',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
})

ENTRIES.append({
    'code': '164411',
    'name': 'Joshua James Harshbareer',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '28 Mar 1994',
})

ENTRIES.append({
    'code': '164412',
    'name': 'Tavior Nicole Harshbarger',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '05 Sep 1937',
})

ENTRIES.append({
    'code': '164511',
    'name': 'Carol Lynn Craig',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '17 Jul 1966',
    'died': '26 Dec 1993',
})

ENTRIES.append({
    'code': '164561',
    'name': 'Jennifer Lynn Sager',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '14 Oct 1980',
})

ENTRIES.append({
    'code': '1648352',
    'name': 'Christina Marie Stevanus',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '18 Aug 1969',
})

ENTRIES.append({
    'code': '164C22',
    'name': 'Melonie Ann Sager',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '30 Jan 1982',
})

ENTRIES.append({
    'code': '164C31',
    'name': 'Robert Lee Watson',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '06 Oct 1977',
})

ENTRIES.append({
    'code': '166213',
    'name': 'Ch Ray Hileman arle ILs',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '14 Feb 1954',
})

ENTRIES.append({
    'code': '166214',
    'name': 'Susan Marte Hileman',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '13 Dec 1958',
})

ENTRIES.append({
    'code': '1662142',
    'name': 'Matthew Edward Nichols',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '05 Nov 1961',
    "spouses": [
        {
            'name': 'James Smallwood',
        },
    ],
})

ENTRIES.append({
    'code': '16621511',
    'name': 'Eric Todd Bittinger',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '13 Jul 1994',
})

ENTRIES.append({
    'code': '1662153',
    'name': 'Shannon Lee Smal',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '28 Jan 1960',
})

ENTRIES.append({
    'code': '166221',
    'name': 'Tami Lynn Hilem',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '03 Apr 1963',
    'died': '26 Aug 1958',
})

ENTRIES.append({
    'code': '1662211',
    'name': 'Mirelle Tiffany Messner',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '22 May 1982',
})

ENTRIES.append({
    'code': '166312',
    'name': 'Patrici Ann a Summers',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '13 Apr 1957',
})

ENTRIES.append({
    'code': '17112111',
    'name': 'Nich Rayolas Spiker',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '09 Aug 1980',
})

ENTRIES.append({
    'code': '17112112',
    'name': 'Jenn Alynn ifer Spiker',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '08 Jul 1983',
})

ENTRIES.append({
    'code': '171122',
    'name': 'Gienna Cathenne Spiker',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
})

ENTRIES.append({
    'code': '1711221',
    'name': 'Teresa Lynn Carpenter',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '09 Nov 1967',
    'died': '25 Jun 1997',
})

ENTRIES.append({
    'code': '171123',
    'name': 'Ruby Lovine Spiker',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '21 Dec 1945',
    'died': '23 Jul 1985',
})

ENTRIES.append({
    'code': '171133',
    'name': 'Marvin Glenn DeBerry',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '08 May 1942',
})

ENTRIES.append({
    'code': '171134',
    'name': 'Judy Ann DeBerry',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '23 Aug 1943',
    'died': '28 Sep 1992',
})

ENTRIES.append({
    'code': '171231',
    'name': 'Charolette Kay Castel',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '01 Sep 1945',
    'died': '29 Nov 1987',
})

ENTRIES.append({
    'code': '1713211',
    'name': 'Th Ralph eod Narivanc ore hik',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '07 Sep 1949',
})

ENTRIES.append({
    'code': '1713212',
    'name': 'Paul Joseph Narivanchik',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '17 Sep 1954',
    'died': '26 Aug 1958',
})

ENTRIES.append({
    'code': '17132131',
    'name': 'Robert Joseph Yingling',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
})

ENTRIES.append({
    'code': '17132132',
    'name': 'Kaimb Mac Edwards',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '13 Feb 1979',
})

ENTRIES.append({
    'code': '1713312',
    'name': 'Pa Ann tnc Summers ia',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '13 Apr 1957',
})

ENTRIES.append({
    'code': '171341',
    'name': 'Kermut Neison DeBerry',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '06 Dec 1937',
})

ENTRIES.append({
    'code': '1713412',
    'name': 'William (Teddy) Dale DeBerry',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '06 Apr 1963',
    'died': '01 Apr 1990',
})

ENTRIES.append({
    'code': '17134121',
    'name': 'Willi Daleam DeBerry',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '14 Sep 1986',
})

ENTRIES.append({
    'code': '171342',
    'name': 'Lots Nita DeBerry',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '04 Apr 1944',
    "spouses": [
        {
            'name': 'Baltim MD to ore',
            'married': '22 May 1913',
        },
    ],
})

ENTRIES.append({
    'code': '1713421',
    'name': 'Sherry Lynne Shea',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '27 Jan 1963',
})

ENTRIES.append({
    'code': '17134211',
    'name': 'Kayla Maric Kanosky',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
})

ENTRIES.append({
    'code': '1713422',
    'name': 'Kenneth Scott Shea',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '05 Apr 1969',
})

ENTRIES.append({
    'code': '17134221',
    'name': 'Knsti Mane Shea',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '03 Apr 1995',
})

ENTRIES.append({
    'code': '17135111',
    'name': 'Timothy James Mosher',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '22 Aug 1991',
})

ENTRIES.append({
    'code': '172111',
    'name': 'Ge Caroline nev Guthrie',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
})

ENTRIES.append({
    'code': '1721112',
    'name': 'Betty Jo Swau',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '07 Apr 1945',
})

ENTRIES.append({
    'code': '17211131',
    'name': 'Todd Willkam Garlitz',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '30 Dec 1978',
})

ENTRIES.append({
    'code': '17211133',
    'name': 'Jack Warmck',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '07 May 1991',
    "spouses": [
        {
            'name': 'Jewell Kave Adkins',
        },
    ],
})

ENTRIES.append({
    'code': '172112',
    'name': 'James Franklin Guthrie',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
})

ENTRIES.append({
    'code': '1721121',
    'name': 'Dale Eugene Guthrie',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
})

ENTRIES.append({
    'code': '17211211',
    'name': 'Dale Eugene Guthnie',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '13 Jun 1987',
})

ENTRIES.append({
    'code': '1721122',
    'name': 'Ch Annerv Guthric',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '18 May 1939',
})

ENTRIES.append({
    'code': '17211221',
    'name': 'Jessica Ann Emmart',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '13 Mar 1983',
    "spouses": [
        {
            'name': 'Larry Blosser',
        },
    ],
})

ENTRIES.append({
    'code': '172113',
    'name': 'Jere Jacob mia Guthric',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'died': '11 Sep 1934',
})

ENTRIES.append({
    'code': '172114',
    'name': 'Ro Dale ber Guthrie',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '13 Jun 1936',
})

ENTRIES.append({
    'code': '172115',
    'name': 'Viola Mane Guthne',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '10 Jul 1937',
})

ENTRIES.append({
    'code': '17211511',
    'name': 'Hea Lynn Galloway',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '25 Sep 1974',
})

ENTRIES.append({
    'code': '17211513',
    'name': 'Kristen Richelle Blosser',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '10 Jul 1984',
})

ENTRIES.append({
    'code': '17211514',
    'name': 'Matth Ray Blosser',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
})

ENTRIES.append({
    'code': '1721152',
    'name': 'Donna June Hixon',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '06 Nov 1956',
    'died': '20 Jan 1957',
})

ENTRIES.append({
    'code': '1721156',
    'name': 'Jef Lynn Fr Hixon',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
})

ENTRIES.append({
    'code': '172116',
    'name': 'De Gienn lber Guthrie',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '01 Sep 1938',
    "spouses": [
        {
            'name': 'Debbie Rhodes Jean Gu',
            'married': '14 Nov 1941',
        },
    ],
})

ENTRIES.append({
    'code': '1721162',
    'name': 'Tima Marie Guthrie',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '05 Dec 1968',
})

ENTRIES.append({
    'code': '172118',
    'name': 'Carl Lee Guthrie',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '27 Feb 1945',
    'died': '1987',
})

ENTRIES.append({
    'code': '1721182',
    'name': 'Gary DeWayne Russell',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '28 Oct 1961',
})

ENTRIES.append({
    'code': '172119',
    'name': 'Harvey Paul Guthrie',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '21 May 1966',
})

ENTRIES.append({
    'code': '1721196',
    'name': 'Rebecea Mane Guthric',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '25 Jan 1985',
})

ENTRIES.append({
    'code': '17212111',
    'name': 'Chad Ene Clark',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '18 Mar 1987',
})

ENTRIES.append({
    'code': '1721212',
    'name': 'KLuke ev Seese',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '02 Apr 1929',
})

ENTRIES.append({
    'code': '172122',
    'name': 'Thelma Mae Scesc',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
})

ENTRIES.append({
    'code': '1721221',
    'name': 'Cindv Diane Wolfe',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '27 Sep 1956',
    'died': '07 Jan 1955',
})

ENTRIES.append({
    'code': '17212212',
    'name': 'Mich Curtis Wilson',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '29 Nov 1975',
})

ENTRIES.append({
    'code': '1721224',
    'name': 'Damel Thurman Wolfe',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '08 Jan 1965',
    'died': '15 Oct 1994',
})

ENTRIES.append({
    'code': '17212241',
    'name': 'Rebecca Maric Wolfe',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'died': '29 Apr 1974',
})

ENTRIES.append({
    'code': '172123',
    'name': 'Th Ray omSeese',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '23 Nov 1943',
})

ENTRIES.append({
    'code': '1721232',
    'name': 'Jeffrey Howard Seese',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '14 Sep 1969',
    'died': '15 Oct 1994',
})

ENTRIES.append({
    'code': '172124',
    'name': 'Dale Franklin Seese',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '28 May 1949',
    "spouses": [
        {
            'name': 'Sheila Jean Pretzel',
        },
    ],
})

ENTRIES.append({
    'code': '172125',
    'name': 'David Henry',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '03 Sep 1950',
    'died': '07 May 1982',
})

ENTRIES.append({
    'code': '1721251',
    'name': 'Dav Shawn Seese',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '1999',
})

ENTRIES.append({
    'code': '1721262',
    'name': 'Joseph Bryson Scese',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '04 Aug 1977',
})

ENTRIES.append({
    'code': '1721311',
    'name': 'Faye Diana Rucinski',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '29 Apr 1960',
    'died': '24 Oct 1995',
})

ENTRIES.append({
    'code': '17213221',
    'name': 'Joseph Alan Ritchey',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
})

ENTRIES.append({
    'code': '17213222',
    'name': 'Jul Mae Ritchey',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '28 Mar 1965',
})

ENTRIES.append({
    'code': '172134',
    'name': 'Susie Alberta Ritchey',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '16 Sep 1939',
})

ENTRIES.append({
    'code': '172135',
    'name': 'Delmore George Ritchey',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '17 Nov 1942',
})

ENTRIES.append({
    'code': '1721351',
    'name': 'Sherri Lee Ritchey',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '28 Mar 1965',
})

ENTRIES.append({
    'code': '17213511',
    'name': 'Tari Jones',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '18 May 1994',
})

ENTRIES.append({
    'code': '17213512',
    'name': 'Bandi Jones',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '24 Sep 1995',
    "spouses": [
        {
            'name': 'Melody Warrington CHILDREN',
        },
    ],
})

ENTRIES.append({
    'code': '1721361',
    'name': 'Mic Dale hael Ritchey',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '16 Sep 1968',
})

ENTRIES.append({
    'code': '17213611',
    'name': 'Soot Ritchev',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
})

ENTRIES.append({
    'code': '17213612',
    'name': 'Taylor Ritchey',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '09 Jan 1947',
})

ENTRIES.append({
    'code': '1721362',
    'name': 'Adam Shane Ritchey',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '07 Aug 1972',
})

ENTRIES.append({
    'code': '1721363',
    'name': 'Eric Mathew Ritchey',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '27 May 1977',
})

ENTRIES.append({
    'code': '1721371',
    'name': 'David Christopher Ritchey',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '12 Mar 1982',
})

ENTRIES.append({
    'code': '1721372',
    'name': 'Daniel Patrick Ritchey',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '04 Sep 1984',
    'died': '30 Oct 1988',
    "spouses": [
        {
            'name': 'RovButlerm',
            'married': '14 Jul 1990',
        },
    ],
})

ENTRIES.append({
    'code': '172142',
    'name': 'Ruth Irene McNair',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '29 Feb 1944',
})

ENTRIES.append({
    'code': '172143',
    'name': 'Donald Rav McNair',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '05 Feb 1947',
})

ENTRIES.append({
    'code': '172144',
    'name': 'Dortha Jean McNair',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '26 May 1948',
})

ENTRIES.append({
    'code': '1721452',
    'name': 'Karen Lynn Butler',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
})

ENTRIES.append({
    'code': '1721454',
    'name': 'Donald James',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '19 Mar 1978',
})

ENTRIES.append({
    'code': '172151',
    'name': 'Shirlev Jane Bovd',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '04 Dec 1937',
})

ENTRIES.append({
    'code': '172152',
    'name': 'Betty Maxine Boyd',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '20 Dec 1939',
})

ENTRIES.append({
    'code': '172153',
    'name': 'Nelds Mac Bovd',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '25 Mar 1945',
    'died': '02 Feb 1982',
})

ENTRIES.append({
    'code': '1723211',
    'name': 'Ch Rea arle Hileman',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
})

ENTRIES.append({
    'code': '17232111',
    'name': 'Jeffrey Allen Bunda',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '08 Dec 1980',
})

ENTRIES.append({
    'code': '1723212',
    'name': 'Cynthia Lee Hileman',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '20 Apr 1951',
})

ENTRIES.append({
    'code': '1723213',
    'name': 'Charles Ray Hileman',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '14 Feb 1954',
})

ENTRIES.append({
    'code': '17232131',
    'name': 'Laura Nicole Hileman',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '02 Dec 1975',
})

ENTRIES.append({
    'code': '17232141',
    'name': 'Heat Marieher Cindric',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '12 Jun 1980',
})

ENTRIES.append({
    'code': '17232142',
    'name': 'Matthew Edward Nichols',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '12 Nov 1977',
})

ENTRIES.append({
    'code': '17232152',
    'name': 'Amos Lewis',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '05 Oct 1979',
})

ENTRIES.append({
    'code': '172322',
    'name': 'Plavford Gail Hileman',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '07 Jan 1929',
})

ENTRIES.append({
    'code': '1723221',
    'name': 'Tami Lynn Hileman',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '28 Jan 1960',
})

ENTRIES.append({
    'code': '1723222',
    'name': 'Te Lee Hileman',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '03 Apr 1963',
})

ENTRIES.append({
    'code': '17232221',
    'name': 'Garrett Steven Reed',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '02 Aug 1993',
})

ENTRIES.append({
    'code': '17233121',
    'name': 'Chad David Summers',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '23 Mar 1977',
})

ENTRIES.append({
    'code': '172612',
    'name': 'Clair Edward Guthrie',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
})

ENTRIES.append({
    'code': '17271',
    'name': 'Beatrice Mae Moyers',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '07 Sep 1921',
})

ENTRIES.append({
    'code': '172711',
    'name': 'Lawrence Keith Baysinger',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '2 Aug 1954',
})

ENTRIES.append({
    'code': '1727111',
    'name': 'Elizabeth Ann Basinger',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '09 Jul 1976',
})

ENTRIES.append({
    'code': '172712',
    'name': 'Rebecca Jane Baysinger',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '15 Sep 1964',
})

ENTRIES.append({
    'code': '17272',
    'name': 'Alma Maxine Moyers',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '20 Oct 1925',
})

ENTRIES.append({
    'code': '172721',
    'name': 'Dovie Wavne Long',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '03 Aug 1952',
})

ENTRIES.append({
    'code': '172722',
    'name': 'Nolan Wade Long',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
})

ENTRIES.append({
    'code': '172723',
    'name': 'Carma Long',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '09 Mar 1961',
})

ENTRIES.append({
    'code': '17273',
    'name': 'Pauline Grace Moyers',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '25 Feb 1927',
})

ENTRIES.append({
    'code': '172731',
    'name': 'Cathennme Louse Sines',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '28 Feb 1954',
})

ENTRIES.append({
    'code': '17274',
    'name': 'Ch Ray arics Moyers',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
})

ENTRIES.append({
    'code': '1727411',
    'name': 'Daniel Aaron Hewitt',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '24 Jul 1977',
})

ENTRIES.append({
    'code': '172742',
    'name': 'Charies Howard Moyers',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '29 Jul 1957',
})

ENTRIES.append({
    'code': '1727421',
    'name': 'Charles (CJ) Howard Movers',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '12 Oct 1982',
})

ENTRIES.append({
    'code': '172743',
    'name': 'Wilham Ray Movers',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '19 Dec. 1961',
})

ENTRIES.append({
    'code': '1728211',
    'name': 'Lincoln Lewis Pickett',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '07 Apr 1968',
    'died': '31 May 1987',
    "spouses": [
        {
            'name': 'Shervi Knotts CHILDREN',
        },
    ],
})

ENTRIES.append({
    'code': '172831',
    'name': 'Gwen Redeen Sheppard',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '06 Jan 1968',
})

ENTRIES.append({
    'code': '1728411',
    'name': 'Grant Andrew Uber',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': 'Feb 1992',
})

ENTRIES.append({
    'code': '172842',
    'name': 'Dwight David Guthrie',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '27 Sep 1954',
})

ENTRIES.append({
    'code': '1728421',
    'name': 'Christie Brooke Guthrie',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
})

ENTRIES.append({
    'code': '1728422',
    'name': 'David Justin Guthne',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '09 Sep 1986',
    "spouses": [
        {
            'name': 'Walter CHILDREN',
        },
    ],
})

ENTRIES.append({
    'code': '1728521',
    'name': 'Lauren Flynn Habenicht',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
})

ENTRIES.append({
    'code': '1728522',
    'name': 'Knstse Micolle Habenicht',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '26 Sep 1987',
})

ENTRIES.append({
    'code': '172862',
    'name': 'Cind Lou Hale',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
})

ENTRIES.append({
    'code': '1728721',
    'name': 'Summer Michelle Bart holo',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
})

ENTRIES.append({
    'code': '172874',
    'name': 'Dw Irs Bartholomew ane',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '18 Apr 1968',
    'died': '11 Feb 1963',
})

ENTRIES.append({
    'code': '172B211',
    'name': 'Jeanette Lee Gaines',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '09 Mar 1972',
})

ENTRIES.append({
    'code': '172B212',
    'name': 'Jeffrey Thomas Gaines',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '17 Dec 1974',
})

ENTRIES.append({
    'code': '172B22',
    'name': 'Susan Adele Lavens',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '08 Mar 1953',
})

ENTRIES.append({
    'code': '172B32',
    'name': 'Joy lrene Miller',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '18 Apr 1952',
})

ENTRIES.append({
    'code': '172B422',
    'name': 'Adam Paul Lindqu',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
})

ENTRIES.append({
    'code': '172B43',
    'name': 'Timothy Eugene Bartholomew',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '06 Jun 1957',
})

ENTRIES.append({
    'code': '172B61',
    'name': 'Douglas Robert Hale',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '24 Oct 1952',
})

ENTRIES.append({
    'code': '172B611',
    'name': 'Raynee Sue Hale',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '17 Apr 1978',
})

ENTRIES.append({
    'code': '172B612',
    'name': 'Benjamen Robert Hale',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
})

ENTRIES.append({
    'code': '172B621',
    'name': 'Jeffrey Daniel Kicin',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '16 May 1983',
})

ENTRIES.append({
    'code': '172B622',
    'name': 'William Peter Kicin',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '05 Jul 1985',
})

ENTRIES.append({
    'code': '172B63',
    'name': 'Tina Dianne Hale',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '3 Jan 1971',
})

ENTRIES.append({
    'code': '172B71',
    'name': 'Dale Arion Barthol',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '24 Mar 1963',
})

ENTRIES.append({
    'code': '172B722',
    'name': 'Tabitha Michelle Bartholomew',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '09 Dec 1987',
})

ENTRIES.append({
    'code': '172B73',
    'name': 'De Annetic bor Bartholome ah w',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '11 Jan 1967',
})

ENTRIES.append({
    'code': '172B731',
    'name': 'Thomas David Jones',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '28 Nov 1990',
})

ENTRIES.append({
    'code': '173124',
    'name': 'Carl R',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '09 Sep 1946',
})

ENTRIES.append({
    'code': '173127',
    'name': 'Ja George co Nicola',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '27 May 1960',
})

ENTRIES.append({
    'code': '17312B',
    'name': 'Charlotte K',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '26 Sep 1909',
})

ENTRIES.append({
    'code': '17322',
    'name': 'Earl Jackson Nicola',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '26 Sep 1909',
})

ENTRIES.append({
    'code': '173221',
    'name': 'Mary Maxine Nicols',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '3 Aug 1930',
    'died': '02 Mar 1931',
})

ENTRIES.append({
    'code': '173222',
    'name': 'Martha Mane Nicola',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'died': '03 Aug 1930',
})

ENTRIES.append({
    'code': '17322311',
    'name': 'Amy Noel Hammons',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
})

ENTRIES.append({
    'code': '17322312',
    'name': 'Jillian Jean Hammons',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '12 Oct 1978',
})

ENTRIES.append({
    'code': '1732232',
    'name': 'Cather Ann Nicola',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '10 Dec 1934',
})

ENTRIES.append({
    'code': '1732233',
    'name': 'Ba Grace rba Nicola',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '13 Oct 1956',
})

ENTRIES.append({
    'code': '17322331',
    'name': 'Amanda Suc Baver',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '29 Aug 1962',
})

ENTRIES.append({
    'code': '17322341',
    'name': 'Robert Theodore (Teddy) Nicola',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '20 Oct 1981',
})

ENTRIES.append({
    'code': '17322342',
    'name': 'Jonathan David Nicola',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '15 Mar 1988',
})

ENTRIES.append({
    'code': '173224',
    'name': 'Dorothy Jean Nicola',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '06 Oct 1937',
    'died': '30 Jan 1980',
})

ENTRIES.append({
    'code': '1732241',
    'name': 'Daniel (DANNY) George Whipkey',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '09 Jan 1968',
})

ENTRIES.append({
    'code': '1732242',
    'name': 'Tamra Lynn Whipkev',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '09 Jan 1968',
})

ENTRIES.append({
    'code': '17324',
    'name': 'Pau Lavenaline Nicola',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '01 Apr 1914',
})

ENTRIES.append({
    'code': '173242',
    'name': 'Loretta Mae Glover',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '25 Jul 1933',
    'died': '1940',
})

ENTRIES.append({
    'code': '1732421',
    'name': 'Rachard Blaine Movers',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '24 Aug 1951',
})

ENTRIES.append({
    'code': '17324211',
    'name': 'Christine Lloyd Pamell',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '03 Mar 1970',
})

ENTRIES.append({
    'code': '17324212',
    'name': 'Richard Blaine Movers',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '01 Apr 1978',
})

ENTRIES.append({
    'code': '1732422',
    'name': 'Randv Wavne Movers',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
})

ENTRIES.append({
    'code': '17324221',
    'name': 'Aaron Troy Movers',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '23 Jul 1977',
})

ENTRIES.append({
    'code': '1732423',
    'name': 'Keith Alan Movers',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '29 Jul 1954',
})

ENTRIES.append({
    'code': '17324231',
    'name': 'Dean Alan Movers',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '25 Sep 1980',
})

ENTRIES.append({
    'code': '17324232',
    'name': 'Jeremy Colt Movers',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '23 Sep 1982',
})

ENTRIES.append({
    'code': '173244',
    'name': 'Larry Collins',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '03 Feb 1952',
})

ENTRIES.append({
    'code': '17325',
    'name': 'Marie Pearl Nicola',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '09 Apr 1919',
    'died': '18 Nov 1994',
})

ENTRIES.append({
    'code': '173251',
    'name': 'Harold E',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '30 Oct 1937',
    'died': '22 Dec 1937',
})

ENTRIES.append({
    'code': '173252',
    'name': 'Shirley Jean Greathouse',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '17 May 1939',
})

ENTRIES.append({
    'code': '17326',
    'name': 'Margaret Elion Nicola',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '01 Jun 1923',
})

ENTRIES.append({
    'code': '173261',
    'name': 'Stanlev Rav Moody',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '09 Jun 1940',
})

ENTRIES.append({
    'code': '17328',
    'name': 'JUDSON (Nick) JUNIOR NICOLA',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '27 Feb 1930',
})

ENTRIES.append({
    'code': '173282',
    'name': 'Jamic Judson Nicola',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '26 Jun 1954',
    'died': '04 Oct 1935',
    "spouses": [
        {
            'name': 'Rufus Ray Rodheaver',
            'married': '15 Apr 1905',
        },
    ],
})

ENTRIES.append({
    'code': '173321',
    'name': 'Willa Amoild Shaffer',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '05 Apr 1929',
})

ENTRIES.append({
    'code': '17332111',
    'name': 'Travis Benjamin Shaffer',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '16 Apr 1983',
})

ENTRIES.append({
    'code': '173322',
    'name': 'Ma Virginia rga Shaffer',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '23 Apr 1934',
    'died': '28 Feb 1951',
})

ENTRIES.append({
    'code': '17332211',
    'name': 'Maria Early',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '23 Jan 1981',
})

ENTRIES.append({
    'code': '17332221',
    'name': 'Paula Diane Rosenberger',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '05 Sep 1974',
})

ENTRIES.append({
    'code': '17332311',
    'name': 'Gregory Shaffer',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '07 jun 1981',
})

ENTRIES.append({
    'code': '17332321',
    'name': 'Dawn Shaffer',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '10 May 1977',
})

ENTRIES.append({
    'code': '17332324',
    'name': 'Robert Shaffer',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '11 Dec 1985',
})

ENTRIES.append({
    'code': '17332331',
    'name': 'Crystal Shaffer',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '14 Apr 1982',
    "spouses": [
        {
            'name': 'Thomas Roseson of nberg Melvin and Barbara er',
            'married': '10 Sep 1944',
        },
    ],
})

ENTRIES.append({
    'code': '173341',
    'name': 'Ruth Friend',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': 'Apr 1947',
})

ENTRIES.append({
    'code': '173361',
    'name': 'Robert Clinton Friend',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '27 Aug 1949',
})

ENTRIES.append({
    'code': '1733611',
    'name': 'Robert Clinton Delmar Friend',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '17 Feb 1977',
    "spouses": [
        {
            'name': 'Linda Hinebaugh',
        },
    ],
})

ENTRIES.append({
    'code': '174211',
    'name': 'Ravmond Dure Freeman',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '02 Dec 1925',
})

ENTRIES.append({
    'code': '174212',
    'name': 'Paul Edward Freeman',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '20 Aug 1927',
})

ENTRIES.append({
    'code': '174213',
    'name': 'Herb Lee Freeman',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '14 Feb 1929',
})

ENTRIES.append({
    'code': '174214',
    'name': 'Janita Bell Freeman',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '22 Jun 1941',
    'died': '27 Jun 1941',
})

ENTRIES.append({
    'code': '174216',
    'name': 'Betty Louise Freeman',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '09 Oct. 1933',
})

ENTRIES.append({
    'code': '174217',
    'name': 'Calleen May ee se',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
})

ENTRIES.append({
    'code': '174218',
    'name': 'George Jonathan Freeman',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
})

ENTRIES.append({
    'code': '174219',
    'name': 'Tomy Ray Freeman',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
})

ENTRIES.append({
    'code': '17421B',
    'name': 'Anna Lee Freeman',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '04 Jun 1942',
    'died': '07 Jun 1942',
})

ENTRIES.append({
    'code': '17421C',
    'name': 'Kenneth Darl Freeman',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '30 Aug 1943',
    'died': '30 May 1945',
})

ENTRIES.append({
    'code': '17421D',
    'name': 'Richard Nathan Freeman',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '10 May 1945',
    "spouses": [
        {
            'name': 'Burchell (Burk) Pritchard',
            'married': '07 Mar 1915',
        },
    ],
})

ENTRIES.append({
    'code': '174583',
    'name': 'Howard Andrew Nicola',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '23 Oct 1930',
})

ENTRIES.append({
    'code': '175111',
    'name': 'Shurley Ann Pritc',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '20 Feb 1969',
    'died': '17 Mar 1964',
    "spouses": [
        {
            'name': 'Theo Fisher Pa Ann tric Miller ia',
            'married': '20 Feb 1969',
        },
    ],
})

ENTRIES.append({
    'code': '177283',
    'name': 'Marsha Frey',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '17 Aug 1929',
})

ENTRIES.append({
    'code': '177833',
    'name': 'Lary Deana Baby',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '1956',
})

ENTRIES.append({
    'code': '178211',
    'name': 'Beatrice Lee Ball',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '18 May 1940',
})

ENTRIES.append({
    'code': '178212',
    'name': 'Raymond Muri Baill',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '29 Jan 1946',
})

ENTRIES.append({
    'code': '178312',
    'name': 'Joseph Ball',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '31 Aug 1949',
})

ENTRIES.append({
    'code': '178331',
    'name': 'Shirlean Ann Bail',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '25 Dec 1945',
    'died': '24 Apr 1975',
    "spouses": [
        {
            'name': 'Garw B',
            'married': '14 Oct 1951',
        },
    ],
})

ENTRIES.append({
    'code': '198',
    'name': 'Ito Cynthy Krager',
    "source": {
        'pdf': 'John_Guthrie - Eight Generations.pdf',
        'page': 1,
    },
    "verification": {
        'status': 'draft',
        'source': 'ocr',
        'lastChecked': None,
        'notes': 'Extracted via regex from ocrmypdf output. Dates/names may have OCR errors — verify against source PDF before trusting.',
    },
    'born': '27 Feb 1956',
})

