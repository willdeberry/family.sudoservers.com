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
         "father": "Archibald DeBerry", "mother": "Mary Hazlett DeBerry", "order": 1, "married": "2 Mar 1882"},
        {"name": "Elizabeth Glover Maust", "order": 2},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 1},
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
})

ENTRIES.append({
    "code": "14",
    "name": "James B. Guthrie",
    "sex": "M",
    "born": "27 Dec 1826",
    "born_place": "Frostburg, MD",
    "died": "11 Oct 1888",
    "died_place": "Hazelton, WV",
    "spouses": [{
        "name": "Susannah B. Beeghly",
        "born": "1832",
        "died": "1900",
        "father": "Michael Beeghly",
        "mother": "Barbara Miller Beeghly",
    }],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 2},
})

ENTRIES.append({
    "code": "16",
    "name": "Elizabeth Guthrie",
    "sex": "F",
    "born": "26 Oct 1832",
    "died": "14 Mar 1912",
    "spouses": [{
        "name": "David Kalfus Harshbarger",
        "born": "27 Dec 1825",
        "died": "24 Sep 1909",
        "father": "Jacob Harshbarger",
        "mother": "Nancy Rankin Harshbarger",
        "buried": "Shady Grove Cemetery, WV",
    }],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 2},
})

ENTRIES.append({
    "code": "17",
    "name": "Susannah Guthrie",
    "sex": "F",
    "born": "26 Jun 1835",
    "born_alt": "20 Jun 1835",
    "died": "7 May 1880",
    "buried": "Shady Grove",
    "notes": "Susanna lived most of her life in Barbour County.",
    "spouses": [{
        "name": "Jacob B. Nicola",
        "born": "13 Oct 1832",
        "died": "23 May 1905",
        "father": "John Nicola",
        "mother": "Mary Boger Nicola",
        "married": "27 Apr 1856",
        "details": "German Baptist; mill wright, merchant and carpenter. Operated a Grist Mill at Orr, WV (between Cuzzart and Cranesville) when he died; buried near there in the Kelley Cemetery.",
    }],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 3},
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
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 8},
})

ENTRIES.append({
    "code": "19",
    "name": "Peter Guthrie",
    "sex": "M",
    "born": "13 Feb 1842",
    "died": "Aug 1916",
    "spouses": [{
        "name": "Catherine Nicola Wilson",
        "born": "30 Jan 1838",
        "died": "1907",
        "notes": "Her second marriage.",
    }],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 3},
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
})

ENTRIES.append({
    "code": "123",
    "name": "Lucy Ann DeBerry",
    "sex": "F",
    "born": "21 May 1853",
    "died": "29 Aug 1926",
    "spouses": [{"name": "John Henry Deal", "born": "19 Apr 1843", "died": "11 Apr 1911", "married": "1 Jan 1878"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 5},
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
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 5},
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
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 5},
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
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 5},
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
    "notes": "Son of Susannah Guthrie Nicola (#17). Married his cousin Lydia Alice Guthrie (#13E).",
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 8},
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
        "details": "Same as #743 in James's branch. This marriage is another John-line/James-line union.",
    }],
    "notes": "John-line man (via grandmother Elizabeth Guthrie #16) married James-line woman.",
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 7},
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
    "died": "27 Jan 1960",
    "buried": "Shady Grove Cemetery",
    "spouses": [{
        "name": "Stella Guthrie",
        "born": "8 May 1889",
        "died": "28 Jan 1960",
        "married": "16 May 1919",
        "details": "Same as #747 in James's branch.",
    }],
    "notes": "Son of Amos J. and Maggie Elizabeth (Harshbarger) Moyers. His mother "
             "Elizabeth Margaret Harshbarger (#162) is daughter of Elizabeth Guthrie "
             "(#16). So this marriage is a third John/James cross-link.",
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 18},
})

ENTRIES.append({
    "code": "162",
    "name": "Elizabeth (Maggie) Margaret Harshbarger",
    "sex": "F",
    "born": "13 May 1863",
    "died": "16 Mar 1928",
    "spouses": [{"name": "Amos J. Moyers", "born": "16 Jan 1836", "died": "21 Apr 1918", "married": "6 Nov 1886"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 7},
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
        "details": "Same as #715 in James's branch.",
    }],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 22},
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
    "code": "13F72",
    "name": "Mary Jean Guthrie",
    "sex": "F",
    "born": "29 Aug 1934",
    "spouses": [{
        "name": "Martin Luther Cupp",
        "born": "9 May 1918",
        "married": "9 May 1953",
        "details": "Same as #A456 in Alexander's branch.",
    }],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 9},
})

# Also add A45 (Alice Pearl Frankhouser) reference now that we're cross-referencing properly
# (already added above)

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
    "spouses": [{
        "name": "Jacob M. A. Thomas",
        "born": "16 Nov 1847",
        "died": "18 Jun 1934",
        "married": "1937",
        "details": "Son of Abraham and Nancy Meyers Thomas. Both buried at Shady Grove Cemetery.",
    }],
    "notes": "Raised Violet Seamon.",
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 2},
})

ENTRIES.append({
    "code": "132",
    "name": "John Guthrie",
    "sex": "M",
    "born": "28 Dec 1846",
    "died": "15 Jun 1917",
    "spouses": [{"name": "Emma Hollis Dotson", "born": "27 Jun 1840", "died": "16 May 1930"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 5},
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
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 5},
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
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 9},
})

ENTRIES.append({
    "code": "144",
    "name": "Barbara Ellen Guthrie",
    "sex": "F",
    "born": "17 Jul 1858",
    "died": "22 May 1921",
    "spouses": [{"name": "William Riley Thomas", "born": "19 Jul 1854", "died": "20 Jun 1921", "married": "4 Aug 1878"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 5},
})

ENTRIES.append({
    "code": "145",
    "name": "David G. Guthrie",
    "sex": "M",
    "born": "30 Aug 1860",
    "died": "26 Mar 1936",
    "spouses": [{"name": "Fidella M. Miller", "born": "Jul 1884", "died": "26 Apr 1925", "married": "26 Feb 1884"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 5},
})

ENTRIES.append({
    "code": "147",
    "name": "Albert M. Guthrie",
    "sex": "M",
    "born": "12 Jul 1864",
    "died": "8 Jan 1951",
    "spouses": [{"name": "Susan Caroline Miller", "born": "4 Dec 1856", "died": "21 Feb 1934", "married": "1886"}],
    "residences": ["Fairchance, PA"],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 6},
})

ENTRIES.append({
    "code": "148",
    "name": "Franklin C. Guthrie",
    "sex": "M",
    "born": "6 Jul 1868",
    "died": "28 Apr 1942",
    "spouses": [{"name": "Barbara Rosanna Miller", "born": "1868", "died": "30 Jul 1923", "married": "1889"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 6},
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
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 12},
})

ENTRIES.append({
    "code": "1132",
    "name": "Charles Allen Guthrie",
    "sex": "M",
    "born": "20 Feb 1873",
    "died": "1933",
    "spouses": [
        {"name": "Emma Spiker", "born": "22 Oct 1877", "died": "6 Aug 1905",
         "details": "Daughter of John P. and Katherine [Beeghley] Spiker.", "order": 1},
        {"name": "Florence (Flossie) Spoerlein", "born": "17 Aug 1887", "died": "30 Sep 1968",
         "buried": "Shady Grove Cemetery", "order": 2},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 12},
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
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 12},
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
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 12},
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
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 13},
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
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 8},
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
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 9},
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
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 9},
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

ENTRIES.append({
    "code": "1713",
    "name": "Oliver Clark Spiker",
    "sex": "M",
    "born": "15 Feb 1886",
    "died": "29 Sep 1974",
    "spouses": [{
        "name": "Laura Guthrie",
        "born": "19 Apr 1889",
        "died": "24 Oct 1944",
        "married": "14 Feb 1909",
        "details": "Same as #765 in James's branch — daughter of Harrison Guthrie #76.",
    }],
    "notes": "Another John/James cross-link: Oliver is son of Mary Elizabeth Nicola (#171, John line) "
             "and Jonas Spiker; he married Laura Guthrie (#765, James line). Both buried at Webbs Chapel Cemetery.",
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 21},
})


# === Generation 4 — children of 111 William Harrison Guthrie ===
ENTRIES.append({
    "code": "1111",
    "name": "Rhuey Pearl Guthrie",
    "sex": "F",
    "born": "22 Feb 1889",
    "died": "25 Sep 1977",
    "spouses": [
        {"name": "Albert Ross Frazee", "born": "6 Jul 1874", "died": "22 Jun 1938",
         "married": "26 May 1940", "order": 1},
        {"name": "Rev. Emra Fike", "born": "26 Sep 1872", "died": "20 Mar 1956", "order": 2},
        {"name": "Elmer Cline Shaffer", "born": "14 Sep 1885", "died": "7 Apr 1973", "order": 3},
    ],
    "buried": "Terra Alta, WV",
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 11},
})

ENTRIES.append({
    "code": "1112",
    "name": "Ada Ellen Guthrie",
    "sex": "F",
    "born": "17 Feb 1887",
    "died": "1 Jan 1976",
    "spouses": [
        {"name": "Harry C. Windell", "born": "28 Sep 1884", "died": "16 Sep 1942", "order": 1},
        {"name": "Charles E. Vought", "details": "Of Cransville.", "order": 2},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 11},
})

ENTRIES.append({
    "code": "1113",
    "name": "Chester Earl Guthrie",
    "sex": "M",
    "born": "11 Dec 1888",
    "died": "18 Aug 1967",
    "spouses": [{"name": "Martha Fike"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 11},
})

# === Archibald J. DeBerry's children (122x — completes 12 sub-tree) ===
ENTRIES.append({
    "code": "1222",
    "name": "Oliver Martin DeBerry",
    "sex": "M",
    "born": "28 Jun 1874",
    "died": "16 Nov 1947",
    "spouses": [{"name": "Anna Funk", "born": "11 Nov 1880", "died": "10 Jul 1953"}],
    "notes": "Had eleven children.",
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 13},
})

ENTRIES.append({
    "code": "1224",
    "name": "Charles Allen DeBerry",
    "sex": "M",
    "born": "8 Jul 1878",
    "died": "7 Oct 1954",
    "spouses": [{
        "name": "Cora Margaret Lambert",
        "born": "6 Sep 1885",
        "died": "6 Oct 1961",
        "married": "12 Oct 1908",
        "details": "Daughter of John Allen and Emma Jane [Martin] Lambert. Both buried at Mt. Moriah Cemetery, Valley Point, WV.",
    }],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 13},
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
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 14},
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
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 14},
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
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 14},
})

# === Susannah Ella DeBerry's daughter ===
ENTRIES.append({
    "code": "124",
    "name": "Susanna Ella DeBerry",
    "sex": "F",
    "born": "27 Jul 1862",
    "died": "4 Jun 1896",
    "spouses": [{
        "name": "Wilbur Franklin Moyers",
        "born": "22 Aug 1864",
        "died": "1 Jun 1951",
        "details": "Son of Amos and Elizabeth [Herring] Moyers.",
    }],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 2},
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

# === Bruce Deal's children (1233x — gen 5 from John) ===
ENTRIES.append({
    "code": "12331",
    "name": "John Cornelius Deal",
    "sex": "M",
    "born": "10 Jul 1906",
    "died": "31 Oct 1958",
    "spouses": [{
        "name": "Laura Edith Stone",
        "born": "18 Feb 1907",
        "died": "1 Sep 1986",
        "married": "1 Nov 1930",
        "details": "Daughter of James William and Clara Bell [Smith] Stone.",
    }],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 50},
})

ENTRIES.append({
    "code": "12338",
    "name": "Ray Glenn Deal",
    "sex": "M",
    "born": "23 Jan 1922",
    "spouses": [{"name": "June Renee Kelly", "born": "26 Feb 1923", "married": "8 Aug 1946"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 50},
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
        "details": "Daughter of Oliver Martin (#1222) and Anna [Funk] DeBerry — same as #12241. "
                   "Cross-link Alexander↔John via Cupp-DeBerry marriage.",
    }],
    "buried": "Haywood, CA",
    "source": {"pdf": "Alexander_Guthrie - Five Generations.pdf", "page": 6},
})

ENTRIES.append({
    "code": "12241",
    "name": "Emma Elizabeth DeBerry",
    "sex": "F",
    "born": "8 May 1916",
    "spouses": [{
        "name": "Charles Henry Cupp",
        "born": "4 Jul 1904",
        "died": "9 May 1978",
        "married": "31 Mar 1934",
        "details": "Same as #A451 in Alexander's branch.",
    }],
    "notes": "Daughter of Oliver Martin DeBerry (#1222). Marriage connects John↔Alexander.",
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 13},
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


# === James Quinter Guthrie's children (13F7x — gen 4 of John line) ===
ENTRIES.append({
    "code": "13F71",
    "name": "Betty Guthrie",
    "sex": "F",
    "born": "8 Apr 1932",
    "spouses": [
        {"name": "Raymond Rishel", "born": "3 Mar 1931", "married": "Mar 1949",
         "details": "Son of Robert and Pearl [Thomas] Rishel.", "order": 1},
        {"name": "Harold S. (Pee Wee) Thomas", "born": "17 Jul 1920", "died": "28 Jun 1992",
         "married": "15 May 1954", "order": 2,
         "details": "Son of Harold Henry and Minnie Carol [Ryan] Thomas."},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 49},
})

ENTRIES.append({
    "code": "13F73",
    "name": "Walter Ray Guthrie",
    "sex": "M",
    "born": "26 Feb 1937",
    "died": "26 May 1990",
    "spouses": [{"name": "Shirley Jean Knabenshoe", "born": "27 Jan 1947"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 49},
})

ENTRIES.append({
    "code": "13F74",
    "name": "Alice Guthrie",
    "sex": "F",
    "born": "24 Oct 1939",
    "spouses": [{
        "name": "Franklin Richard Thomas",
        "born": "11 Mar 1933",
        "married": "1939",
        "details": "Son of J. Richard and Lula P. [Fike] Thomas — same as #14474 in John's branch.",
    }],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 49},
})

ENTRIES.append({
    "code": "13F75",
    "name": "Ethel Jane Guthrie",
    "sex": "F",
    "born": "24 Sep 1941",
    "died": "1 Aug 1975",
    "spouses": [{"name": "Troy Everey Rosier"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 49},
})

ENTRIES.append({
    "code": "13F76",
    "name": "Juanita Mae Guthrie",
    "sex": "F",
    "born": "16 May 1944",
    "spouses": [{"name": "Howard K. Pratt, Jr."}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 49},
})

ENTRIES.append({
    "code": "13F77",
    "name": "Judy Marie Guthrie",
    "sex": "F",
    "born": "15 Aug 1946",
    "spouses": [{"name": "Roger Lynn Hoffman", "born": "27 Jul 1942"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 49},
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

