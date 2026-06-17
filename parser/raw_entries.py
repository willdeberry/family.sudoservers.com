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
    "All seven documented PDFs share an unnamed common Guthrie patriarch — "
    "logically required by the overlapping geography and the shared lineage-code "
    "numbering, but never directly attested in any source. The seven sibling "
    "branches are 1 (John), 2 (William), 5 (Stephen), 6 (Rachel), 7 (James), "
    "8 (Absalom), A (Alexander). Codes 3, 4, 9 are unaccounted for and may "
    "represent siblings whose lines were never documented. The patriarch was "
    "previously recorded under code '0' as a synthesized root; that placeholder "
    "was removed at the submitter's request, and each sibling now roots its own "
    "subtree."
)

# Same-person-multiple-codes table. Each entry merges into one Person record.
SEE_REFS = [
    # Ray Guthrie appears under James's branch (74A, as son of Jeremiah) and
    # under John's branch (172A, via mother Nancy Ann Nicola). Same person.
    {"codes": ["74A", "172A"], "reason": "Father Jeremiah=74 in James line; mother Nancy Ann Nicola=172 in John line"},
    # Ward Barnes Guthrie: father Samuel Floyd Guthrie (1133, John line);
    # mother Rosa Mae Barnes (715, James line)
    {"codes": ["11331", "7151"], "reason": "Mother is 715 in James line; father is 1133 in John line"},
    # James Guthrie (son of Jeremiah=74 and Nancy Nicola=172) coded both 741 and 1721
    {"codes": ["741", "1721"], "reason": "James Guthrie b. 2 Feb 1879 — Jeremiah & Nancy's son; James/John cross-coding"},
    # Troy Guthrie (also Jeremiah & Nancy's son) coded 748 and 1728
    {"codes": ["748", "1728"], "reason": "Troy Guthrie b. 24 Feb 1891 — Jeremiah & Nancy's son; James/John cross-coding"},
    # Theodore Ralph Narivanchik coded both 164111 and 1443111
    {"codes": ["164111", "1443111"], "reason": "Theodore Ralph Narivanchik — cross-coded parent"},

    # Stella Guthrie herself: same person under James 747 and John 1727
    # (daughter of Jeremiah Guthrie = 74 and Nancy Ann Nicola = 172).
    # Her children also appear under THREE codes because their parents are
    # cross-coded too. Without this merge, Beatrice/Alma/Pauline/Charles end
    # up with the two duplicate Stella records as separate parents (3 total).
    {"codes": ["747", "1727"], "reason": "Stella Guthrie — daughter of Jeremiah (74) and Nancy Nicola (172, James/John cross)"},
    # Stella's children appear in James (747x), John (1622x via Charles), and
    # John (1727x via Stella as Susannah's granddaughter).
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

    # Auto-merged OCR-draft / verified pairs (2026-06-08). Each pair is the
    # same person under multiple lineage codes — either a real cross-marriage
    # (e.g. James/John crosses) or an OCR code-recognition error in the source.
    {"codes": ["1363162", "1365162"], "reason": "George McKinley Shafer b. 23 Jul 1954 — OCR code variant"},
    {"codes": ["13635156", "1365156"], "reason": "Amelia Jane Shafer b. 18 Mar 1961 — OCR code variant"},
    {"codes": ["144332", "144532"], "reason": "Glenna Catherine Spiker b. 20 Sep 1941 — OCR code variant"},
    {"codes": ["144382", "16482"], "reason": "Ross Carlton Miller b. 14 Apr 1946 — cross-coded"},
    {"codes": ["1443A2", "164A2"], "reason": "Ronald Kenneth Smith b. 28 Feb 1947 — cross-coded"},
    {"codes": ["1443B", "164B"], "reason": "Daisy Bell Harshbarger b. 11 Feb 1925 — cross-coded"},
    {"codes": ["162231", "142821"], "reason": "Catherine Louise Sines b. 28 Feb 1954 — Sines cross-marriage"},
    {"codes": ["163123", "142523"], "reason": "Robert Eugene Nicola b. 26 Mar 1934 — Nicola cross-marriage"},
    {"codes": ["1631231", "1425231"], "reason": "Arveta Louise Nicola b. 16 Sep 1953 — Nicola cross-marriage"},
    {"codes": ["1648352", "164832"], "reason": "Christina Marie Stevanus b. 18 Aug 1969 — OCR code variant"},
    {"codes": ["171123", "144533"], "reason": "Ruby Lovine Spiker b. 21 Dec 1945 — Spiker cross-marriage"},
    {"codes": ["171134", "122474"], "reason": "Judy Ann DeBerry b. 23 Aug 1943 — DeBerry cross-marriage"},
    {"codes": ["1713421", "1224321"], "reason": "Sherry Lynne Shea b. 27 Jan 1963 — Shea cross-marriage"},
    {"codes": ["1723212", "166212"], "reason": "Cynthia Lee Hileman b. 20 Apr 1951 — Hileman cross-marriage"},
    {"codes": ["1723221", "166221"], "reason": "Tami Lynn Hileman b. 28 Jan 1960 — Hileman cross-marriage"},
    {"codes": ["17272", "7472"], "reason": "Alma Maxine Moyers b. 20 Oct 1925 — Stella Guthrie's daughter (James/John cross)"},
    {"codes": ["173242", "163142"], "reason": "Loretta Mae Glover b. 25 Jul 1933 — cross-coded"},
    {"codes": ["173252", "163152"], "reason": "Shirley Jean Greathouse b. 17 May 1939 — cross-coded"},
    {"codes": ["17328", "16318"], "reason": "Judson Junior Nicola b. 27 Feb 1930 — Nicola cross-marriage"},
    {"codes": ["73332", "72332"], "reason": "James Ronald Barnes b. 25 Aug 1955 — OCR code variant"},
    {"codes": ["73333", "72333"], "reason": "Nancy Carolyn Barnes b. 25 Apr 1957 — OCR code variant"},
    {"codes": ["74114", "17211A"], "reason": "Betty Ruth Guthrie b. 22 Jun 1943 — James/John cross via Jeremiah-Nancy Nicola"},
    {"codes": ["741182", "1721182"], "reason": "Gary DeWayne Russell b. 28 Oct 1961 — James/John cross"},
    {"codes": ["74119", "172119"], "reason": "Harvey Paul Guthrie b. 14 Nov 1941 — James/John cross"},
    {"codes": ["7411B", "17211B"], "reason": "Carl Lee Guthrie b. 27 Feb 1945 — James/John cross"},
    {"codes": ["7411D", "17211D"], "reason": "Helen Ann Guthrie b. 23 Oct 1949 — James/John cross"},
    {"codes": ["741322", "1721322"], "reason": "Rodney Wayne Ritchey b. 27 Dec 1959 — James/John cross"},
    {"codes": ["74136", "172136"], "reason": "Kenneth Dale Ritchey b. 25 Nov 1944 — James/John cross"},
    {"codes": ["7414", "17214"], "reason": "Dora Guthrie b. 24 Apr 1916 — James/John cross"},
    {"codes": ["7432", "1662"], "reason": "Emma Harshbarger b. 30 Jan 1906 — James/John cross"},
    {"codes": ["74321", "16621"], "reason": "Charles Ray Hileman b. 18 Feb 1925 — James/John cross"},
    {"codes": ["743212", "166212"], "reason": "Cynthia Lee Hileman b. 20 Apr 1951 — James/John cross (third code)"},
    # NOTE: removed the prior "7436 = 172B6" SEE_REF. The OCR-extracted code
    # "7436" was actually a mangled read of "74B6" (B vs 3), so it should have
    # been 74B6 = 172B6 with parent 74B (Dessie). The earlier merge gave Mabel
    # both 743 (Hattie, wrong) and 172B (Dessie, correct) as parents.
    {"codes": ["74612", "172612"], "reason": "Clair Edward Guthrie b. 22 Sep 1961 — James/John cross"},
    {"codes": ["74B4", "172B4"], "reason": "Paul Eugene Bartholomew b. 18 May 1928 — James/John cross via Dessie"},
    {"codes": ["74B61", "172B61"], "reason": "Douglas Robert Hale b. 24 Oct 1952 — James/John cross"},
    {"codes": ["74B74", "172B74"], "reason": "Dwane Ira Bartholomew b. 18 Apr 1968 — James/John cross"},
    {"codes": ["765212", "1443112"], "reason": "Paul Joseph Narivanchik b. 14 Sep 1954 — Narivanchik cross-coding"},
    {"codes": ["765421", "1224321"], "reason": "Sherry Lynne Shea b. 27 Jan 1963 — Shea cross (third code)"},
    {"codes": ["A21122", "1132222"], "reason": "Brenda Kay Frazee b. 24 Aug 1959 — Alexander/John cross"},

    # Second pass — same person, OCR date-format variant (e.g. "05 Jun" vs "5 Jun")
    {"codes": ["1345113", "1365113"], "reason": "James Harold Shafer b. 9 Mar 1946 — OCR code variant"},
    {"codes": ["13C5122", "132182"], "reason": "Tamara Lynn Smith b. 24 Dec 1966 — cross-coded"},
    {"codes": ["14431111", "1641111"], "reason": "Sabrina Louise Narivanchik b. 6 Sep 1971 — Narivanchik cross"},
    {"codes": ["144321", "16421"], "reason": "Anna Marie Harshbarger b. 5 Jun 1935 — cross-coded"},
    {"codes": ["144322", "16422"], "reason": "Mary Ellen Harshbarger b. 6 Feb 1937 — cross-coded"},
    {"codes": ["144343", "164A3"], "reason": "Linda Grace Smith b. 3 Jan 1949 — cross-coded"},
    {"codes": ["14438", "1648"], "reason": "Pearl Catherine Harshbarger b. 2 Jul 1919 — cross-coded"},
    {"codes": ["1631242", "1425242"], "reason": "Tamra Lynn Whipkey b. 9 Jan 1968 — Nicola cross"},
    {"codes": ["171133", "122473"], "reason": "Marvin Glenn DeBerry b. 8 May 1942 — DeBerry cross"},
    {"codes": ["1713422", "1224322"], "reason": "Kenneth Scott Shea b. 5 Apr 1969 — Shea cross"},
    {"codes": ["17271", "7471"], "reason": "Beatrice Mae Moyers b. 7 Sep 1921 — Stella Guthrie's daughter"},
    {"codes": ["172711", "162211"], "reason": "Lawrence Keith Baysinger b. 28 Aug 1954 — cross-coded (draft has OCR date '2 Aug')"},
    {"codes": ["17273", "7473"], "reason": "Pauline Grace Moyers b. 15 Feb 1927 — Stella's daughter (draft has OCR date '25 Feb')"},
    {"codes": ["173224", "142524"], "reason": "Dorothy Jean Nicola b. 6 Oct 1937 — Nicola cross"},
    {"codes": ["17325", "16315"], "reason": "Marie Pearl Nicola b. 9 Apr 1919 — Nicola cross"},
    {"codes": ["74116", "172116"], "reason": "Delbert Glenn Guthrie b. 1 Sep 1938 — James/John cross"},
    {"codes": ["74132", "172132"], "reason": "Donald Ray Ritchey b. 3 Oct 1935 — James/John cross"},
    {"codes": ["74151", "172151"], "reason": "Shirley Jane Boyd b. 4 Dec 1937 — James/John cross"},
    {"codes": ["743215", "166215"], "reason": "Melissa Ann Hileman b. 5 Nov 1961 — James/John cross"},
    {"codes": ["74322", "16622"], "reason": "Playford Gail Hileman b. 7 Jan 1929 — James/John cross"},
    {"codes": ["76541", "122431"], "reason": "Kermit Nelson DeBerry b. 6 Dec 1937 — James/John cross"},
    {"codes": ["7655", "17135"], "reason": "Thelma Olieta Spiker b. 2 Dec 1921 — James/John cross"},
    {"codes": ["A436", "A456"], "reason": "Martin Luther Cupp b. 9 May 1918 — OCR code variant"},

    # Third pass — OCR-mangled name matches confirmed by exact birth date
    # NOTE: removed prior "144135 = 144155" SEE_REF. The OCR draft "144135"
    # was a mangled read of "144155" (Wilma, Paul's daughter); the earlier
    # merge spuriously gave her Carlos (14413) as a second parent.
    {"codes": ["144227", "143427"], "reason": "Jacob George Nicola Jr. — cross-coded"},
    {"codes": ["144371", "16471"], "reason": "Barbara Jean Harshbarger — cross-coded"},
    {"codes": ["171341", "122431"], "reason": "Kermit Nelson DeBerry — cross-coded (third code)"},
    {"codes": ["1723213", "166213"], "reason": "Charles Ray Hileman II — cross-coded"},
    {"codes": ["172731", "142821"], "reason": "Catherine Louise Sines — cross-coded (third code)"},
    {"codes": ["172742", "162242"], "reason": "Charles Howard Moyers — cross-coded"},
    {"codes": ["173124", "143424"], "reason": "Carl R. Nicola — cross-coded"},
    {"codes": ["1732242", "1425242"], "reason": "Tamra Lynn Whipkey — cross-coded (third code)"},
    {"codes": ["17324", "16314"], "reason": "Pauline Lavena Nicola — Nicola cross"},
    {"codes": ["1732423", "1631423"], "reason": "Keith Alan Moyers — cross-coded"},
    {"codes": ["17326", "16316"], "reason": "Margaret Ellen Nicola — Nicola cross"},
    {"codes": ["173261", "163161"], "reason": "Stanley Ray Moody — cross-coded"},
    {"codes": ["173282", "163182"], "reason": "Jamie Judson Nicola — Nicola cross"},
    {"codes": ["71511", "113311"], "reason": "Suzanna Kay Guthrie — cross-coded"},
    {"codes": ["74121", "172121"], "reason": "James W. Seese — James/John cross"},
    {"codes": ["74138", "172135"], "reason": "Delmore George Ritchey — cross-coded"},
    {"codes": ["7415", "17215"], "reason": "Ada Belle Guthrie — James/John cross"},
    {"codes": ["74742", "162242"], "reason": "Charles Howard Moyers — Stella Guthrie's grandson (third code)"},
    {"codes": ["74743", "162243"], "reason": "William Ray Moyers — cross-coded"},
    {"codes": ["74B3", "172B3"], "reason": "Evelyn Irene Bartholomew — Dessie cross"},
    {"codes": ["74B5", "172B5"], "reason": "Dorothy May Bartholomew — Dessie cross"},
    {"codes": ["76551", "171351"], "reason": "Gladys Kay Duncan — cross-coded"},
    {"codes": ["768422", "1224322"], "reason": "Kenneth Scott Shea — cross-coded (third code)"},
    {"codes": ["A21121", "1132221"], "reason": "Kathy Marie Frazee — Alexander/John cross"},
    # NOTE: removed prior "A4134 = A4154" SEE_REF. OCR misread one as the
    # other but they have different parents (A413 Edna vs A415 Guy); the merge
    # gave Francis two unrelated parents.
    {"codes": ["173244", "163144"], "reason": "Larry Robert Collins — cross-coded"},
    {"codes": ["74B32", "172B32"], "reason": "Joy Irene Miller — cross-coded"},

    # Fourth pass — OCR-mangled names verified by exact date + character overlap
    {"codes": ["1224331", "1224311"], "reason": "Michael Nelson DeBerry — OCR code variant"},
    {"codes": ["12332111", "1434121"], "reason": "Ronald Lee Collins — cross-coded (Jenkins marriage)"},
    {"codes": ["1443413", "1445413"], "reason": "Crystal Dawn Groves — OCR code variant"},
    {"codes": ["144352", "16452"], "reason": "Alvin Francis Fresh — cross-coded"},
    {"codes": ["1443A1", "164A1"], "reason": "Verl Junior Smith — cross-coded"},
    {"codes": ["1443C2", "164C2"], "reason": "Richard Ervin Sager — cross-coded"},
    {"codes": ["144741", "13F741"], "reason": "Anna Pearl Thomas — cross-coded"},
    {"codes": ["1713211", "1443111"], "reason": "Theodore Ralph Narivanchik — cross-coded (third code)"},
    {"codes": ["171342", "122432"], "reason": "Lois Nita DeBerry — cross-coded"},
    {"codes": ["172322", "16622"], "reason": "Playford Gail Hileman — cross-coded (third code)"},
    {"codes": ["1723222", "166222"], "reason": "Terah Lee Hileman — cross-coded"},
    {"codes": ["172721", "162221"], "reason": "Doyle Wayne Long — cross-coded"},
    {"codes": ["172874", "172B74"], "reason": "Dwane Ira Bartholomew — OCR code variant"},
    {"codes": ["173127", "143427"], "reason": "Jacob George Nicola Jr. — cross-coded (third code)"},
    {"codes": ["1732233", "1425233"], "reason": "Barbara Grace Nicola — cross-coded"},
    {"codes": ["1732421", "1631421"], "reason": "Richard Blaine Moyers — cross-coded"},
    {"codes": ["741121", "1721121"], "reason": "Dale Eugene Guthrie — James/John cross"},
    {"codes": ["743221", "166221"], "reason": "Tami Lynn Hileman — cross-coded (third code)"},
    {"codes": ["74721", "162221"], "reason": "Doyle Wayne Long — cross-coded (third code)"},
    {"codes": ["7482", "17282"], "reason": "Thelma Pearl Guthrie — James/John cross"},
    {"codes": ["7483", "17283"], "reason": "Alice Mae Guthrie — James/John cross"},

    # Fifth pass — no-date drafts matched by unambiguous normalized name
    {"codes": ["1233512", "132172"], "reason": "Pamela Deal — cross-marriage"},
    {"codes": ["172722", "162222"], "reason": "Nolan Wade Long — Stella Guthrie's grandson"},
    {"codes": ["74144", "172144"], "reason": "Dortha Jean McNair — James/John cross"},
    {"codes": ["A4565", "13F725"], "reason": "Charles Wesley Cupp — Alexander/John cross"},

    # Sixth pass — date-exact cross-code matches (wrong-person matches manually filtered out)
    {"codes": ["13631231", "13651231"], "reason": "James Edward McCarty — OCR code variant"},
    {"codes": ["13631321", "13651521"], "reason": "Dawn Machelle Shafer — OCR code variant"},
    {"codes": ["1363178", "1365178"], "reason": "Cheryl Leigh Krimpel — OCR code variant"},
    {"codes": ["13821541", "13B21541"], "reason": "Shame Seamon — OCR code variant"},
    {"codes": ["144353", "16453"], "reason": "Doris Jean Fresh — cross-coded"},
    {"codes": ["144354", "16454"], "reason": "Infant Daughter Fresh — cross-coded"},
    {"codes": ["14436", "1646"], "reason": "May Thomas Harshbarger — cross-coded"},
    {"codes": ["1443C11", "164561"], "reason": "Jennifer Lynn Sager — cross-coded"},
    {"codes": ["1443C21", "164C21"], "reason": "Richard Allen Sager — cross-coded"},
    {"codes": ["14751314", "14751311"], "reason": "Brian Keith Cuppett — OCR code variant"},
    {"codes": ["162232", "142822"], "reason": "Wendy Gay Sines — Sines cross"},
    {"codes": ["163121", "142521"], "reason": "Mary Maxine Nicola — Nicola cross"},
    {"codes": ["16312311", "14252311"], "reason": "Amy Noel Hammons — Nicola cross"},
    {"codes": ["16312341", "14252341"], "reason": "Robert Theodore (Teddy) Nicola — Nicola cross"},
    {"codes": ["16312421", "14252421"], "reason": "Travis Cody Gatian — Nicola cross"},
    {"codes": ["17112111", "14453111"], "reason": "Nicholas Ray Spiker — Spiker cross"},
    {"codes": ["17112112", "14453112"], "reason": "Jennifer Alynn Spiker — Spiker cross"},
    {"codes": ["1711221", "1445321"], "reason": "Teresa Lynn Carpenter — cross-coded"},
    {"codes": ["17132132", "1641132"], "reason": "Kimberlie Mae Edwards — Narivanchik cross"},
    {"codes": ["17134221", "12243221"], "reason": "Kristin Marie Shea — DeBerry cross"},
    {"codes": ["17232111", "1662111"], "reason": "Jeffrey Allen Bunda — Hileman cross"},
    {"codes": ["17232131", "1662131"], "reason": "Laura Nicole Hileman — Hileman cross"},
    {"codes": ["17232141", "1662141"], "reason": "Heather Marie Cindric — Hileman cross"},
    {"codes": ["17232152", "1662152"], "reason": "Amos Lewis — Hileman cross"},
    {"codes": ["17232221", "1662221"], "reason": "Garrett Steven Reed — Hileman cross"},
    {"codes": ["17233121", "1663121"], "reason": "Chad David Summers — cross-coded"},
    {"codes": ["1727111", "1622112"], "reason": "Elizabeth Ann Baysinger — Moyers cross"},
    {"codes": ["1727411", "1622411"], "reason": "Daniel Arron Hewitt — Moyers cross"},
    {"codes": ["1727421", "1622421"], "reason": "Charles Junior (CJ) Moyers — Moyers cross"},
    {"codes": ["1728522", "172B522"], "reason": "Kristie Micolle Habenicht — OCR code variant"},
    {"codes": ["17322", "16312"], "reason": "Earl Jackson Nicola — Nicola cross"},
    {"codes": ["173221", "142521"], "reason": "Mary Maxine Nicola — Nicola cross (third code)"},
    {"codes": ["17322312", "14252312"], "reason": "Jillian Jean Hammons — Nicola cross"},
    {"codes": ["17322341", "14252341"], "reason": "Robert Theodore Nicola — Nicola cross (third code)"},
    {"codes": ["17322342", "14252342"], "reason": "Jonathan David Nicola — Nicola cross"},
    {"codes": ["17324211", "16314211"], "reason": "Christine Lloyd Parnell — Moyers cross"},
    {"codes": ["17324212", "16314212"], "reason": "Richard Blaine Moyers, Jr. — Moyers cross"},
    {"codes": ["17324221", "1728312"], "reason": "Aaron Troy Moyers — cross-coded"},
    {"codes": ["17324231", "16314231"], "reason": "Dean Alan Moyers — Moyers cross"},
    {"codes": ["17324232", "16314232"], "reason": "Jeremy Colt Moyers — Moyers cross"},
    {"codes": ["173251", "163151"], "reason": "Harold E. Greathouse — cross-coded"},
    {"codes": ["7411513", "17211513"], "reason": "Kristen Richelle Blosser — James/John cross"},
    {"codes": ["7411B1", "17211B1"], "reason": "Carl Joseph Guthrie — James/John cross"},
    {"codes": ["7411D1", "17211D1"], "reason": "Susan Michella Fike — James/John cross"},
    {"codes": ["741362", "1721362"], "reason": "Adam Shane Ritchey — James/John cross"},
    {"codes": ["741456", "1721456"], "reason": "Fred Allen Ulderich — James/John cross"},
    {"codes": ["746121", "1726121"], "reason": "Clair (CJ) Edward Guthrie, Jr. — James/John cross"},
    {"codes": ["747111", "1622112"], "reason": "Elizabeth Ann Baysinger — Moyers cross (third code)"},
    {"codes": ["748522", "172B522"], "reason": "Kristie Micolle Habenicht — James/John cross"},
    {"codes": ["74B422", "172B422"], "reason": "Adam Paul Lindquist — James/John cross"},
    {"codes": ["76521121", "16411121"], "reason": "Ashley Renee Narivanchik — Narivanchik cross"},
    {"codes": ["7652113", "1641113"], "reason": "William (Billy) Ralph Narivanchik — Narivanchik cross"},
    {"codes": ["7654221", "12243221"], "reason": "Kristin Marie Shea — Shea cross (third code)"},
    {"codes": ["A211221", "11322221"], "reason": "Jamie Lynn Balsley — Alexander/John cross"},
    {"codes": ["A211222", "11322222"], "reason": "Brad Allan Balsley — Alexander/John cross"},
    {"codes": ["A21131", "1132231"], "reason": "Kimberly Frazee — Alexander/John cross"},
    {"codes": ["A45621", "1321571"], "reason": "Erica Marie Myers — Alexander/John cross"},
    {"codes": ["A45622", "1321572"], "reason": "Meghan Cortney Cupp — Alexander/John cross"},
    {"codes": ["A45671", "13F7271"], "reason": "Jennifer Dawn Cupp — Alexander/John cross"},
    {"codes": ["A45672", "13F7272"], "reason": "Tiffany Jo Reckart — Alexander/John cross"},

    # === Final pass: 38 duplicate clusters found by name+birth-date matching ===

    # DeBerry / Shea cross-marriage (Kermit Nelson DeBerry 122431 = 171341)
    {"codes": ["1224311", "1713411"], "reason": "Michael Nelson DeBerry — DeBerry/Shea cross"},
    {"codes": ["1224312", "1713412"], "reason": "William (Teddy) Dale DeBerry — DeBerry/Shea cross"},
    {"codes": ["12243111", "17134111"], "reason": "Jennifer Leanne DeBerry — DeBerry/Shea cross"},
    {"codes": ["12243112", "17134112"], "reason": "Melissa Sue DeBerry — DeBerry/Shea cross"},
    {"codes": ["12243121", "17134121"], "reason": "William Dale DeBerry Jr. — DeBerry/Shea cross"},

    # Narivanchik cross-coding (Theodore/Paul/Linda Narivanchik = 164111-113 / 1443111-113)
    {"codes": ["164112", "1443112"], "reason": "Paul Joseph Narivanchik — Narivanchik cross"},
    {"codes": ["164113", "1443113"], "reason": "Linda Mae Narivanchik — Narivanchik cross"},
    {"codes": ["1641112", "14431112"], "reason": "Theodore Ralph Narivanchik Jr. — Narivanchik cross"},
    {"codes": ["1641113", "14431113"], "reason": "William Ralph Narivanchik — Narivanchik cross"},
    {"codes": ["1641121", "14431121"], "reason": "Kara Elizabeth Sonntag — Narivanchik cross"},
    {"codes": ["1641122", "14431122"], "reason": "Alicia Marie Sonntag — Narivanchik cross"},
    {"codes": ["1641123", "14431123"], "reason": "Adam Edward Sonntag — Narivanchik cross"},
    {"codes": ["1641131", "14431131"], "reason": "Robert Joseph Yingling III — Narivanchik cross"},
    {"codes": ["1641132", "14431132"], "reason": "Kimberlie Mae Edwards — Narivanchik cross"},

    # Jeremiah Guthrie's line — gen 4 children of 74=172 (James/John cross)
    {"codes": ["743", "1723"], "reason": "Hattie Guthrie — Jeremiah's daughter; James/John cross"},

    # Hattie's daughter Emma Harshbarger appears under three codes
    {"codes": ["1662", "17232"], "reason": "Emma Harshbarger — Hattie's daughter; James/John cross"},
    {"codes": ["1661", "17231"], "reason": "Homer Loid Harshbarger — same family"},
    {"codes": ["1663", "17233"], "reason": "Jeremiah Joseph Harshbarger — same"},
    {"codes": ["1664", "17234"], "reason": "David Harshbarger — same"},

    # Spiker cross-coding (children of Laura Guthrie 17xx and via the cross-marriage)
    {"codes": ["7651", "17131"], "reason": "Ralph Ersel Spiker — James/John cross"},
    {"codes": ["7656", "17136"], "reason": "Ruth Virginia Spiker — James/John cross"},

    # Ward Barnes Guthrie's children: 113311-113314 = 72341-72344 via Ward+Laura marriage
    {"codes": ["113312", "72342"], "reason": "Samuel Fleming Guthrie — Ward+Laura's child"},
    {"codes": ["113313", "72343"], "reason": "Ward David Guthrie — same"},
    {"codes": ["113314", "72344"], "reason": "Stephen Byron Guthrie — same"},

    # Cupp/Frankhouser cross-marriage: 13F72 (Mary Jean Guthrie) m. A456 (Martin Luther Cupp)
    {"codes": ["13F721", "A4561"], "reason": "Martin Edward Cupp — Cupp/Guthrie cross"},
    {"codes": ["13F722", "A4562"], "reason": "Roger Lee Cupp — same"},
    {"codes": ["13F723", "A4563"], "reason": "James Melvin Cupp — same"},
    {"codes": ["13F724", "A4564"], "reason": "Marvin Dale Cupp — same"},
    {"codes": ["13F726", "A4566"], "reason": "Richard Glenn Cupp — same"},
    {"codes": ["13F727", "A4567"], "reason": "Sharon Louise Cupp — same"},

    # Nicola cross-marriage: 1442 (Chester Martin Nicola family) intersects 1731
    {"codes": ["14422", "17312"], "reason": "Chester Martin Nicola — Nicola cross"},
    {"codes": ["14421", "17311"], "reason": "Infant Son (b. 22 Aug 1909) — same"},

    # Lawson/Collins cross (Sheldon Lawson's daughter Tammie m. Collins)
    {"codes": ["1434122", "12332112"], "reason": "Tammie Sue Collins — Collins cross"},

    # Other surviving duplicates from name+date match:
    {"codes": ["166312", "1713312"], "reason": "Patricia Ann Summers — cross-coded"},
    {"codes": ["16454", "16455"], "reason": "Infant Daughter Fresh — OCR code variant"},
    # NOTE: 14851 and 14891 both named "Delbert Guthrie" born 8 Jun 1928 but
    # have different parents (Bessie 1485 vs Helen 1489) — likely two
    # different cousins with the same name and birth date, not duplicates.
    # Removed the SEE_REF that was treating them as one person.
    {"codes": ["74C", "172C"], "reason": "Infant son (Jeremiah's, b. 1 Jun 1902) — James/John cross"},
    {"codes": ["1663121", "17133121"], "reason": "Chad David Summers — Harshbarger/Spiker cross"},
]

# ---------------------------------------------------------------------------
# Lineage-parent opt-out
# ---------------------------------------------------------------------------
# Codes whose lineage-derived parent should be suppressed. parent_code() in
# build.py would normally link these to a higher-level code in the same
# sibling system, but listing one here makes that person a tree root.
# Used to break a person off from the synthesized Patriarch (code "0") at
# the submitter's request.
NO_LINEAGE_PARENT: set[str] = set()
# Codes listed here are treated as tree roots even when parent_code() would
# otherwise link them to a higher-level code in the same sibling system.
# We don't currently need any — code "0" (the synthesized patriarch) has
# been removed from the dataset (issue #12), so the heuristic naturally
# stops at single-character codes since parent_code("1") = "0" but no
# entry with code "0" exists. Kept here as the documented opt-out hook
# in case a future submitter wants another branch detached.

# ---------------------------------------------------------------------------
# ENTRIES
# ---------------------------------------------------------------------------
# Note: the seven sibling branches (codes 1, 2, 5, 6, 7, 8, A) used to all
# point at a synthesized "Unknown Guthrie Patriarch" at code "0". That
# placeholder was removed at the submitter's request (issue #12); each
# sibling now roots its own subtree. See FOUNDER_NOTE for context.
ENTRIES = []

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
        {"code": "15", "name": "Sarah Guthrie", "born": "22 Oct 1829", "died": "Dec 1833", "flags": {"diedInInfancy": True}, "verified_terminal": True},
        {"code": "16", "name": "Elizabeth Guthrie", "born": "26 Oct 1832"},
        {"code": "17", "name": "Susannah Guthrie", "born": "26 May 1835", "born_alt": "20 May 1835"},
        {"code": "18", "name": "John Guthrie", "born": "19 Mar 1839", "died": "1841", "flags": {"diedInInfancy": True}, "verified_terminal": True},
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
        {"code": "121", "name": "Mary E. DeBerry", "born": "about 1846", "verified_terminal": True},
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
        {"code": "149", "name": "Levi Guthrie", "born": "1871", "died": "10 Jan 1872", "flags": {"diedInInfancy": True}, "verified_terminal": True},
        {"code": "14A", "name": "Lucian Guthrie", "born": "about 1872"},
        {"code": "14B", "name": "Mary Guthrie", "born": "about 1874"},
        {"code": "14C", "name": "Jane Guthrie", "verified_terminal": True},
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
        {"code": "1722", "name": "Susanna Guthrie", "born": "14 Feb 1880", "died": "14 Sep 1961", "verified_terminal": True},
        {"code": "1723", "name": "Hattie Guthrie", "born": "20 Dec 1881"},
        {"code": "1724", "name": "Norton Guthrie", "born": "13 Apr 1884", "died": "28 Feb 1966", "verified_terminal": True},
        {"code": "1725", "name": "Infant Daughter", "born": "29 Jan 1886", "died": "29 Jan 1886", "flags": {"diedInInfancy": True}, "verified_terminal": True},
        {"code": "1726", "name": "Loyd (Lloyd) Guthrie", "born": "2 Apr 1887"},
        {"code": "1727", "name": "Stella Guthrie", "born": "8 May 1889"},
        {"code": "1728", "name": "Troy Guthrie", "born": "24 Feb 1891"},
        {"code": "1729", "name": "Dellie Guthrie", "born": "17 Sep 1893", "died": "22 Jan 1895", "flags": {"diedInInfancy": True}, "verified_terminal": True},
        {"code": "172A", "name": "Ray Guthrie", "born": "17 Dec 1895", "died": "16 Jan 1976", "verified_terminal": True},
        {"code": "172B", "name": "Dessie Guthrie", "born": "6 Apr 1899"},
        {"code": "172C", "name": "Infant Son", "born": "1 Jun 1902", "died": "1 Jun 1902", "flags": {"diedInInfancy": True}, "verified_terminal": True},
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
        {"code": "192", "name": "John Guthrie", "born": "4 Feb 1869", "died": "in infancy", "flags": {"diedInInfancy": True}, "verified_terminal": True},
        {"code": "193", "name": "Henry M. Guthrie", "born": "6 Jul 1870"},
        {"code": "194", "name": "Rev. Wilbert Guthrie", "born": "1875", "died": "1934"},
        {"code": "195", "name": "Charles H. Guthrie", "born": "4 Oct 1876", "verified_terminal": True},
        {"code": "196", "name": "Ida Guthrie", "born": "1880", "born_alt": "1882"},
    ],
})

# === 2. WILLIAM GUTHRIE ===



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
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        # First marriage
        {"code": "51", "name": "Harrison Guthrie"},
        {"code": "52", "name": "Elizabeth Guthrie", "verified_terminal": True},
        # Second marriage
        {"code": "53", "name": "Stephen Guthrie", "born": "7 Apr 1827"},
        {"code": "54", "name": "Catherine Guthrie", "born": "about 1833", "verified_terminal": True, "details": "m. Mr. Dunham"},
        {"code": "55", "name": "Mary Guthrie", "born": "about 1835", "verified_terminal": True, "details": "m. William Browning"},
        {"code": "56", "name": "Amy Guthrie", "born": "20 Dec 1840", "died": "1899"},
        {"code": "57", "name": "Bell Guthrie", "born": "1843", "verified_terminal": True, "details": "m. Simon Miller"},
        {"code": "58", "name": "Israel Guthrie", "born": "1847", "verified_terminal": True, "details": "Lived at York Run, PA"},
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
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "511", "name": "Arthur Guthrie", "occupation": "Major General in the Army", "verified_terminal": True},
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
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "531", "name": "Mary Alice Guthrie", "born": "about 1855"},
        {"code": "532", "name": "Samuel Spencer Guthrie", "born": "1858"},
        {"code": "533", "name": "William A. Guthrie", "born": "1861", "verified_terminal": True},
        {"code": "534", "name": "Gertrude Guthrie", "verified_terminal": True},
        {"code": "535", "name": "Caroline Bell Guthrie", "born": "1871"},
        {"code": "536", "name": "Zana Estella Guthrie", "born": "25 Nov 1875"},
    ],
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
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "561", "name": "Edith Frankhouse", "verified_terminal": True, "details": "m. Chalmers Glover"},
        {"code": "562", "name": "Elizabeth (Lizzie) Frankhouser", "verified_terminal": True, "details": "m. Bruce Fichtner"},
        {"code": "563", "name": "Ada Frankhouser", "verified_terminal": True, "details": "m. D.E.L. (Lew) Forman"},
        {"code": "564", "name": "Truman Frankhouser", "verified_terminal": True},
        {"code": "565", "name": "Kenneth Bruce Frankhouser", "born": "5 Dec 1868"},
        {"code": "566", "name": "Homer Frankhouser", "verified_terminal": True},
    ],
})


# === 6. RACHEL GUTHRIE ===



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
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": "Direct PDF read confirmed name+dates."},
    "children": [
        {"code": "71", "name": "Alcinda J. Guthrie", "born": "8 Sep 1845"},
        {"code": "72", "name": "Sarah Ann Guthrie", "born": "21 Feb 1847"},
        {"code": "73", "name": "Ephraim Guthrie", "born": "14 Jun 1850", "died": "20 Oct 1854", "flags": {"diedInInfancy": True}, "verified_terminal": True},
        {"code": "74", "name": "Jeremiah Guthrie", "born": "10 Sep 1852"},
        {"code": "75", "name": "Mary Guthrie", "born": "15 Oct 1854", "died": "23 Dec 1872", "verified_terminal": True},
        {"code": "76", "name": "Harrison Guthrie", "born": "22 Apr 1858"},
        {"code": "77", "name": "Lucretia Guthrie", "born": "28 Apr 1860", "died": "28 Apr 1877", "verified_terminal": True},
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
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": "Direct PDF read confirmed name+dates."},
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
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": "Direct PDF read confirmed name+dates."},
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
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": "Direct PDF read confirmed name+dates."},
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
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": "Direct PDF read confirmed name+dates."},
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
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": "Direct PDF read confirmed name+dates."},
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
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "81", "name": "Isaac Armstrong Guthrie", "born": "8 Feb 1838"},
        {"code": "82", "name": "Mary Frances Guthrie", "born": "6 Feb 1840"},
        {"code": "83", "name": "Rachel Ann Guthrie", "born": "11 Feb 1843", "died": "27 Nov 1912", "verified_terminal": True},
        {"code": "84", "name": "James Marshall Guthrie", "born": "20 May 1845"},
        {"code": "85", "name": "A son", "born": "15 Sep 1847", "died": "in infancy", "flags": {"diedInInfancy": True}, "verified_terminal": True},
        {"code": "86", "name": "Isabella Guthrie", "born": "10 May 1849", "died": "1852", "flags": {"diedInInfancy": True}, "verified_terminal": True},
        {"code": "87", "name": "John Forman Guthrie", "born": "2 Nov 1851"},
        {"code": "88", "name": "Martha Bell Guthrie", "born": "15 Feb 1854"},
        {"code": "89", "name": "Virginia Alice Guthrie", "born": "6 Apr 1856", "verified_terminal": True},
        {"code": "8A", "name": "Sarah Louise Guthrie", "born": "23 Jan 1859", "verified_terminal": True, "details": "lived with Virginia, Columbus, Ohio"},
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
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "811", "name": "William Marshall Guthrie", "born": "8 Jun 1867", "died": "31 Oct 1921", "verified_terminal": True, "details": "m. 25 Dec 1895; Flora West"},
        {"code": "812", "name": "Ora Bell Guthrie", "born": "18 Dec 1868"},
    ],
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
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "821", "name": "Bruce Harned", "born": "13 Aug 1859", "died": "18 Nov 1863", "verified_terminal": True},
        {"code": "822", "name": "Annie Harned", "born": "14 Aug 1860", "died": "17 Feb 1899", "verified_terminal": True, "details": "m. 6 Feb 1889 Gus Mann b. Paulding County, Ohio; d. Mar 1899"},
        {"code": "823", "name": "Walter Harned", "born": "13 Jul 1862", "died": "31 Dec 1930"},
        {"code": "824", "name": "Edward Harned", "born": "24 Jan 1865", "died": "in infancy", "flags": {"diedInInfancy": True}, "verified_terminal": True},
        {"code": "825", "name": "Jennie Harned", "born": "6 Jun 1873"},
        {"code": "826", "name": "Lucy Harned", "born": "1 Oct 1876"},
        {"code": "827", "name": "Mary Harned", "born": "8 Feb 1879"},
    ],
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
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "871", "name": "Charles William Guthrie", "born": "31 Jan 1883", "verified_terminal": True, "details": "m. 24 Apr 1907 Mae Grey b. 26 Dec 1882 (Hocking County, Ohio)"},
        {"code": "872", "name": "Anna May Guthrie", "born": "28 Dec 1884"},
        {"code": "873", "name": "Harry Grimes Guthrie", "born": "8 Sep 1886"},
        {"code": "874", "name": "Bruce Forman Guthrie", "born": "23 Sep 1890"},
        {"code": "875", "name": "Sarah Louise Guthrie", "born": "5 Feb 1894", "verified_terminal": True, "details": "Lived in Sunbury, Ohio"},
        {"code": "876", "name": "Park Edward Guthrie", "born": "21 Dec 1895"},
        {"code": "877", "name": "John Paul Guthrie", "born": "13 Aug 1898"},
    ],
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
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "881", "name": "Mattie O'Neil", "born": "12 Jul 1877", "verified_terminal": True, "details": "m. 15 Jun 1904 R. E. Allen, b. 21 Nov 1869 (Athens County, Ohio)"},
        {"code": "882", "name": "Gracie O'Neil", "born": "6 Apr 1884", "died": "23 Oct 1900", "verified_terminal": True},
    ],
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
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": "Direct PDF read confirmed name+dates."},
    "children": [
        # First marriage
        {"code": "A1", "name": "Abner F. Guthrie", "born": "5 Feb 1840", "died": "15 May 1875"},
        {"code": "A2", "name": "Preston T. Guthrie", "born": "4 Jul 1842"},
        {"code": "A3", "name": "Persis Ann Guthrie", "born": "4 May 1844"},
        {"code": "A4", "name": "Louise Alida (Lide) Guthrie", "born": "3 Mar 1846"},
        {"code": "A5", "name": "Mary Caroline Guthrie", "born": "10 May 1847"},
        {"code": "A6", "name": "Edgar W. Guthrie", "verified_terminal": True},
        # Second marriage
        {"code": "A7", "name": "Melissa J. Guthrie", "born": "26 Oct 1848", "verified_terminal": True},
        {"code": "A8", "name": "Allen C. Guthrie", "born": "22 Nov 1849", "died": "1936", "verified_terminal": True},
        {"code": "A9", "name": "Clarissa A. Guthrie", "born": "Dec 1851", "died": "1935", "verified_terminal": True},
        {"code": "AA", "name": "Leander Kidwell Guthrie", "born": "25 Feb 1856", "died": "20 Oct 1914", "verified_terminal": True},
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
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": "Direct PDF read confirmed name+dates."},
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
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": "Direct PDF read confirmed name+dates."},
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
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": "Direct PDF read confirmed name+dates."},
})

ENTRIES.append({
    "code": "A5",
    "name": "Mary Caroline Guthrie",
    "sex": "F",
    "born": "10 May 1847",
    "died": "21 May 1915",
    "spouses": [{"name": "Nicolas Bolyard"}],
    "source": {"pdf": "Alexander_Guthrie - Five Generations.pdf", "page": 2},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": "Direct PDF read confirmed name+dates."},
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
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": "Direct PDF read confirmed name+dates."},
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
        {"code": "1221", "name": "James R. DeBerry", "born": "22 Nov 1872", "died": "13 Dec 1896", "verified_terminal": True},
        {"code": "1222", "name": "Oliver Martin DeBerry", "born": "28 Jun 1874"},
        {"code": "1223", "name": "Nancy Arletta DeBerry", "born": "7 May 1876"},
        {"code": "1224", "name": "Charles Allen DeBerry", "born": "8 Jul 1878"},
        {"code": "1225", "name": "John C. DeBerry", "born": "29 Oct 1880", "died": "11 Dec 1897", "verified_terminal": True},
        {"code": "1226", "name": "Henry R. DeBerry", "born": "5 Dec 1882"},
        {"code": "1227", "name": "Stanford Earl DeBerry", "born": "11 Dec 1884"},
        {"code": "1228", "name": "Edna (Eline) Ethel DeBerry", "born": "2 Feb 1885", "born_alt": "2 Feb 1886", "died": "24 Jul 1899", "verified_terminal": True},
        {"code": "1229", "name": "William Vance DeBerry", "born": "24 Nov 1888"},
        {"code": "122A", "name": "Ola Otis DeBerry", "born": "11 May 1891", "verified_terminal": True},
        {"code": "122B", "name": "Jasper Nelson DeBerry", "born": "17 Nov 1894", "verified_terminal": True},
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
        {"code": "123A", "name": "Jackson Deal", "born": "21 Feb 1899", "died": "16 Oct 1923", "verified_terminal": True},
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
        {"code": "13B1", "name": "William Skiles", "died": "as a child", "flags": {"diedInInfancy": True}, "verified_terminal": True},
        {"code": "13B2", "name": "Lily May Skiles", "born": "19 Aug 1883"},
        {"code": "13B3", "name": "Mary Elizabeth Skiles", "born": "23 Aug 1886", "died": "1958", "verified_terminal": True},
        {"code": "13B4", "name": "Pearl Tracy Skiles", "born": "1888", "died": "1906", "died_alt": "1911", "verified_terminal": True},
        {"code": "13B5", "name": "James Fieldon Skiles", "born": "1890", "verified_terminal": True},
        {"code": "13B6", "name": "Rosa Ola Skiles", "born": "20 Aug 1892", "verified_terminal": True},
        {"code": "13B7", "name": "Frederick Haddix", "born": "1896", "born_place": "Barbour County", "died": "1976", "verified_terminal": True},
        {"code": "13B8", "name": "Florence Haddix", "verified_terminal": True},
        {"code": "13B9", "name": "Claud Haddix", "died": "about 1924", "verified_terminal": True},
        {"code": "13BA", "name": "Denzid Haddix", "born": "1903", "died": "1909", "flags": {"diedInInfancy": True}, "verified_terminal": True},
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
        {"code": "13E6", "name": "Ruby May Nicola", "born": "5 Apr 1901", "verified_terminal": True},
        {"code": "13E7", "name": "Luara B. Nicola", "born": "1904"},
        {"code": "13E8", "name": "Dorsey E. Nicola", "verified_terminal": True},
        {"code": "13E9", "name": "Ola Ruth Nicola", "born": "1908", "verified_terminal": True},
        {"code": "13EA", "name": "Infant", "died": "in infancy", "flags": {"diedInInfancy": True}, "verified_terminal": True},
        {"code": "13EB", "name": "Infant", "died": "in infancy", "flags": {"diedInInfancy": True}, "verified_terminal": True},
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
        {"code": "13F2", "name": "Della Mae Guthrie", "born": "1891", "died": "1891", "flags": {"diedInInfancy": True}, "verified_terminal": True},
        {"code": "13F3", "name": "Infant Daughter", "born": "10 Dec 1894", "died": "1894", "flags": {"diedInInfancy": True}, "verified_terminal": True},
        {"code": "13F4", "name": "Troy McCledlon Guthrie", "born": "11 Jan 1895", "died": "31 Jul 1919", "verified_terminal": True},
        {"code": "13F5", "name": "Matila (Mammie) Mae Guthrie", "born": "9 Dec 1897"},
        {"code": "13F6", "name": "Henry Rudolph (Dolph) Guthrie", "born": "31 Dec 1899", "died": "6 Aug 1918", "verified_terminal": True},
        # Third marriage (per PDF)
        {"code": "13F7", "name": "James Quinter Guthrie", "born": "31 Dec 1902"},
        {"code": "13F8", "name": "George Robert Guthrie", "born": "12 Feb 1903"},
        {"code": "13F9", "name": "Martha Guthrie", "born": "18 Mar 1906", "verified_terminal": True},
        {"code": "13FA", "name": "Mary Elizabeth Guthrie", "born": "18 Mar 1907"},
        {"code": "13FB", "name": "Dessie Myrtle Guthrie", "born": "1 Jul 1909"},
        {"code": "13FC", "name": "Susan (Susie) Murhl Guthrie", "born": "26 May 1911"},
        {"code": "13FD", "name": "John Ray Guthrie", "born": "1 Oct 1914"},
        {"code": "13FE", "name": "Nellie Virginia Guthrie", "born": "20 Mar 1917"},
        {"code": "13FF", "name": "Alice Frances Guthrie", "born": "6 Jun 1919", "verified_terminal": True},
        {"code": "13FG", "name": "Harley Theodore Guthrie", "born": "28 Mar 1922", "died": "31 Oct 1925", "flags": {"diedInInfancy": True}, "verified_terminal": True},
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
        {"code": "1661", "name": "Homer Loid Harshbarger", "born": "27 Sep 1902", "died": "6 Apr 1927", "verified_terminal": True},
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
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": "Direct PDF read confirmed name+dates."},
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
        {"code": "16221", "name": "Beatrice Mae Moyers", "born": "7 Sep 1921", "verified_terminal": True},
        {"code": "16222", "name": "Alma Maxine Moyers", "born": "20 Oct 1925", "verified_terminal": True},
        {"code": "16223", "name": "Pauline Grace Moyers", "born": "15 Feb 1927", "verified_terminal": True},
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
        {"code": "1625", "name": "Bertha O. Moyers", "verified_terminal": True},
        {"code": "1626", "name": "Bessie L. Moyers", "born": "1 Apr 1893", "died": "27 Jan 1933", "verified_terminal": True},
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
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": "Direct PDF read confirmed name+dates."},
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
        {"code": "1613", "name": "Walter Scott Barnes", "born": "4 Jun 1886", "died": "1 Dec 1957", "verified_terminal": True},
        {"code": "1614", "name": "Russell Emerson Barnes", "born": "15 Mar 1891", "died": "3 Jan 1925", "verified_terminal": True},
        {"code": "1615", "name": "Leslie Virgil Barnes", "born": "3 Mar 1893", "died": "Dec 1959", "verified_terminal": True},
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
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": "Direct PDF read confirmed name+dates."},
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
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": "Direct PDF read confirmed name+dates."},
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
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": "Direct PDF read confirmed name+dates."},
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
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": "Direct PDF read confirmed name+dates."},
})

ENTRIES.append({
    "code": "A41",
    "name": "Lucian Emmer Frankhouser",
    "sex": "M",
    "born": "24 Mar 1866",
    "died": "17 Dec 1934",
    "spouses": [{"name": "Laura M. Deal", "born": "7 Nov 1869", "died": "11 Sep 1957", "married": "14 Feb 1895"}],
    "source": {"pdf": "Alexander_Guthrie - Five Generations.pdf", "page": 3},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": "Direct PDF read confirmed name+dates."},
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
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": "Direct PDF read confirmed name+dates."},
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
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": "Direct PDF read confirmed name+dates."},
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
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": "Direct PDF read confirmed name+dates."},
})

ENTRIES.append({
    "code": "13E4",
    "name": "Clarence Herbert Nicola",
    "sex": "M",
    "born": "28 Mar 1894",
    "died": "1971",
    "spouses": [{"name": "Lillian S. Ridenour", "born": "23 Oct 1902", "died": "1965", "married": "1920"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 23},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": "Direct PDF read confirmed name+dates."},
})

ENTRIES.append({
    "code": "13E5",
    "name": "Homer Andrew Nicola",
    "sex": "M",
    "born": "16 Oct 1896",
    "spouses": [{"name": "Dove Poling", "born": "22 Jun 1898", "married": "24 Jun 1921"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 23},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": "Direct PDF read confirmed name+dates."},
})

# === Children of Stella/Charles (7471-7474 = 16221-16224 — activates that cluster) ===
ENTRIES.append({
    "code": "7471",
    "name": "Beatrice Mae Moyers",
    "sex": "F",
    "born": "7 Sep 1921",
    "spouses": [{"name": "Lloyd Baysinger", "born": "3 Oct 1909", "married": "11 Feb 1950"}],
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 9},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": "Direct PDF read confirmed name+dates."},
})

ENTRIES.append({
    "code": "7472",
    "name": "Alma Maxine Moyers",
    "sex": "F",
    "born": "20 Oct 1925",
    "spouses": [{"name": "Urban Lavern Long", "born": "13 Sep 1929", "married": "20 Jun 1951"}],
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 9},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": "Direct PDF read confirmed name+dates."},
})

ENTRIES.append({
    "code": "7473",
    "name": "Pauline Grace Moyers",
    "sex": "F",
    "born": "15 Feb 1927",
    "died": "23 Jun 1981",
    "spouses": [{"name": "Paul Carlus Sines", "married": "Sep 1953", "details": "Son of Alvin and Anna [Guthrie] Sines."}],
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 9},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": "Direct PDF read confirmed name+dates."},
})

ENTRIES.append({
    "code": "7474",
    "name": "Charles Ray Moyers",
    "sex": "M",
    "born": "28 Jul 1931",
    "spouses": [{"name": "Dorothy (Dottie) N. Shoemaker", "born": "22 Dec 1934", "married": "12 Apr 1953"}],
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 9},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": "Direct PDF read confirmed name+dates."},
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
        {"code": "1142", "name": "Minnie M. Hartman", "born": "9 Jul 1879", "died": "12 Jan 1960", "verified_terminal": True},
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
        {"code": "1331", "name": "Frank Strawser", "verified_terminal": True},
        {"code": "1332", "name": "Lewis Strawser", "verified_terminal": True},
        {"code": "1333", "name": "Rebecca Strawser", "verified_terminal": True},
        {"code": "1334", "name": "Rena Strawser", "verified_terminal": True},
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
        {"code": "1351", "name": "Charles Howard Lewis", "born": "1873", "died": "25 Feb 1953", "verified_terminal": True},
        {"code": "1352", "name": "Melvin Lewis", "verified_terminal": True},
        {"code": "1353", "name": "Walter Cristy Lewis", "born": "14 Jun 1880", "died": "1967", "verified_terminal": True},
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
        {"code": "1361", "name": "Stephen Turney", "born": "19 Dec 1872", "died": "11 Apr 1881", "verified_terminal": True},
        {"code": "1362", "name": "Florence Iey Turney", "born": "10 May 1874", "died": "20 Jul 1953"},
        {"code": "1363", "name": "Henry R. Turney", "born": "12 May 1875", "died": "12 Oct 1953", "verified_terminal": True},
        {"code": "1364", "name": "Christian Turney", "born": "23 Jul 1877", "died": "12 Mar 1878", "flags": {"diedInInfancy": True}, "verified_terminal": True},
        {"code": "1365", "name": "Maud Turney"},
        {"code": "1366", "name": "Pearl A. Turney", "born": "10 Mar 1884"},
        {"code": "1367", "name": "Clarence I. Turney", "born": "21 Apr 1885", "died": "1885", "flags": {"diedInInfancy": True}, "verified_terminal": True},
        {"code": "1368", "name": "George Turney", "born": "24 Jan 1888", "died": "28 Dec 1910", "verified_terminal": True},
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
        {"code": "1387", "name": "Lizzie Teets", "verified_terminal": True},
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
        {"code": "13C1", "name": "Earl Guthrie", "verified_terminal": True},
        {"code": "13C2", "name": "Worley Guthrie", "died": "6 May 1949"},
        {"code": "13C3", "name": "Alvin Guthrie"},
        {"code": "13C4", "name": "Alice (Allie) S. Guthrie", "verified_terminal": True},
        {"code": "13C5", "name": "Rena K. Guthrie", "born": "26 Mar 1898"},
        {"code": "13C6", "name": "Elma Guthrie", "verified_terminal": True},
        # Second marriage
        {"code": "13C7", "name": "Russell Guthrie", "verified_terminal": True},
        {"code": "13C8", "name": "Ernest Guthrie", "verified_terminal": True},
        {"code": "13C9", "name": "Arlie Guthrie, Jr.", "born": "5 May 1908"},
        {"code": "13CA", "name": "Edna Guthrie", "verified_terminal": True},
        {"code": "13CB", "name": "Woodrow Wilson Guthrie", "verified_terminal": True},
        {"code": "13CC", "name": "Chester E. Guthrie", "born": "25 Dec 1916", "died": "24 Mar 1962", "verified_terminal": True},
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
        {"code": "13D1", "name": "Daniel Myers", "verified_terminal": True},
        {"code": "13D2", "name": "Myrtle Myers"},
        {"code": "13D3", "name": "Roy Myers", "verified_terminal": True},
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
        {"code": "1411", "name": "James L Uphold, Jr.", "born": "21 Nov 1872", "died": "10 Jun 1914", "verified_terminal": True},
        {"code": "1412", "name": "John Jacob Uphold", "born": "23 Mar 1877"},
        {"code": "1413", "name": "Mary A. Uphold", "born": "15 Jul 1881", "verified_terminal": True},
        {"code": "1414", "name": "Flemming Clyde Uphold", "born": "3 May 1883", "died": "Jan 1945", "verified_terminal": True},
        {"code": "1415", "name": "Charles Ray Uphold", "born": "19 Nov 1885"},
        {"code": "1416", "name": "David Franklin Uphold", "born": "8 Oct 1887"},
        {"code": "1417", "name": "William H. Uphold", "born": "21 May 1890", "died": "21 Nov 1890", "flags": {"diedInInfancy": True}, "verified_terminal": True},
        {"code": "1418", "name": "Ella May Uphold", "born": "2 Jul 1892"},
        {"code": "1419", "name": "Laura Bell Uphold", "verified_terminal": True},
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
        {"code": "1431", "name": "Infant", "flags": {"diedInInfancy": True}, "verified_terminal": True},
        # Second marriage
        {"code": "1432", "name": "Margaret (Maggie) Sliger", "born": "1883"},
        {"code": "1433", "name": "Sarah Ellen Sliger", "born": "14 Sep 1885"},
        {"code": "1434", "name": "Mollie Sliger", "born": "14 Nov 1888"},
        {"code": "1435", "name": "Emma Pearl Sliger", "born": "15 Aug 1895"},
        {"code": "1436", "name": "Anna Sliger", "verified_terminal": True},
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
        {"code": "1463", "name": "Rosa Mary Miller", "born": "8 May 1887", "died": "6 Sep 1907", "verified_terminal": True},
        {"code": "1464", "name": "Jammy Russie Miller", "born": "20 Jun 1891", "died": "15 Jan 1892", "flags": {"diedInInfancy": True}, "verified_terminal": True},
        {"code": "1465", "name": "Rosia Miller", "died": "1928", "verified_terminal": True},
        {"code": "1466", "name": "Howard Miller", "died": "1934", "verified_terminal": True},
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
        {"code": "14A1", "name": "William Guthrie", "verified_terminal": True},
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
        {"code": "14B1", "name": "Norman Guthrie", "born": "8 Mar 1897", "verified_terminal": True},
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
        {"code": "1646", "name": "May Thomas Harshbarger", "born": "3 Apr 1916", "died": "13 Apr 1916", "flags": {"diedInInfancy": True}, "verified_terminal": True},
        {"code": "1647", "name": "Charles Reuben Harshbarger", "born": "16 Nov 1917"},
        {"code": "1648", "name": "Pearl Catherine Harshbarger", "born": "2 Jul 1919"},
        {"code": "1649", "name": "Violet May Harshbarger", "born": "9 Jun 1921", "verified_terminal": True},
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
        {"code": "1651", "name": "Gilbert Harshbarger", "born": "10 Oct 1893", "verified_terminal": True},
        {"code": "1652", "name": "Blanche Harshbarger", "verified_terminal": True},
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
        {"name": "Susie Elizabeth Guthrie", "born": "1867", "died": "15 Apr 1886",
         "married": "25 Aug 1881", "order": 1,
         "details": "Same as #191 — daughter of his uncle Peter Guthrie (#19). First-cousin marriage."},
        {"name": "Jane Harden", "born": "15 Jan 1865", "married": "1886", "order": 2},
        {"name": "Emma Matheny", "born": "6 May 1867", "died": "16 May 1930", "order": 3},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 8},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        # First marriage
        {"code": "1421", "name": "Truman Guthrie", "born": "1 Apr 1884", "died": "26 Sep 1885", "flags": {"diedInInfancy": True}, "verified_terminal": True},
        {"code": "1422", "name": "Son", "born": "15 Apr 1886", "died": "15 Apr 1886", "flags": {"diedInInfancy": True}, "verified_terminal": True},
        # Second marriage
        {"code": "1423", "name": "Mary Guthrie", "born": "27 Aug 1886", "died": "12 Aug 1887", "flags": {"diedInInfancy": True}, "verified_terminal": True},
        {"code": "1424", "name": "a daughter", "born": "14 Apr 1887", "flags": {"diedInInfancy": True}, "verified_terminal": True},
        {"code": "1425", "name": "George Franklin Guthrie", "born": "5 Mar 1890"},
        {"code": "1426", "name": "Sarah Guthrie", "verified_terminal": True},
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
        {"code": "1444", "name": "Wilbert Thomas", "born": "14 Mar 1889", "died": "30 Sep 1905", "died_alt": "30 Oct 1905", "verified_terminal": True},
        {"code": "1445", "name": "Laura Catherine Thomas", "born": "28 Jan 1891"},
        {"code": "1446", "name": "John Marshall Thomas", "born": "1 Feb 1893"},
        {"code": "1447", "name": "James Richard Thomas", "born": "11 Mar 1896"},
        {"code": "1448", "name": "Daisy Pearl Thomas", "born": "7 Sep 1897"},
        {"code": "1449", "name": "Charles Chester Thomas", "born": "22 Aug 1900", "died": "1 Jan 1963", "verified_terminal": True},
        {"code": "144A", "name": "Alberta Thomas", "died": "in infancy", "flags": {"diedInInfancy": True}, "verified_terminal": True},
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
        {"code": "1453", "name": "Lillian A. Guthrie", "verified_terminal": True},
        {"code": "1454", "name": "Nola E. Guthrie", "born": "28 Mar 1891"},
        {"code": "1455", "name": "Daisy E. Guthrie", "born": "4 Mar 1893"},
        {"code": "1456", "name": "George Cecil Guthrie", "born": "1893", "died": "18 Jul 1982", "verified_terminal": True},
        {"code": "1457", "name": "Groover Guthrie", "born": "1893", "died": "8 Nov 1946", "verified_terminal": True},
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
        {"code": "1474", "name": "Effie Guthrie", "born": "7 Sep 1892", "died": "1895", "flags": {"diedInInfancy": True}, "verified_terminal": True},
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
        {"code": "1483", "name": "Arthur H. Guthrie", "born": "15 Apr 1896", "died": "26 Feb 1923", "verified_terminal": True},
        {"code": "1484", "name": "Walter Guthrie", "born": "1898"},
        {"code": "1485", "name": "Bessie E. Guthrie", "born": "Jul 1899"},
        {"code": "1486", "name": "Emma V. Guthrie", "born": "1903"},
        {"code": "1487", "name": "James E. Guthrie", "born": "1904"},
        {"code": "1488", "name": "Sarah E. Guthrie", "born": "14 Nov 1906"},
        {"code": "1489", "name": "Helen J. Guthrie", "born": "28 Oct 1908"},
        {"code": "148A", "name": "Charles H. Guthrie", "born": "1 May 1919", "verified_terminal": True},
        {"code": "148B", "name": "Amy B. Guthrie", "died": "in infancy", "flags": {"diedInInfancy": True}, "verified_terminal": True},
        {"code": "148C", "name": "Alice Guthrie", "died": "in infancy", "flags": {"diedInInfancy": True}, "verified_terminal": True},
        {"code": "148D", "name": "William Guthrie", "died": "in infancy", "flags": {"diedInInfancy": True}, "verified_terminal": True},
    ],
})

# === More Stephen branch depth ===


# === Alexander A3 (Persis Ann)'s children — Romesburg line ===
ENTRIES.append({
    "code": "A32",
    "name": "Alexander G. Romesburg",
    "sex": "M",
    "born": "13 Aug 1868",
    "died": "22 May 1965",
    "spouses": [{"name": "Anna Blanche Raymond", "born": "1875", "died": "11 Feb 1966"}],
    "source": {"pdf": "Alexander_Guthrie - Five Generations.pdf", "page": 3},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": "Direct PDF read confirmed name+dates."},
})

ENTRIES.append({
    "code": "A35",
    "name": "S. Walter Romesburg",
    "sex": "M",
    "born": "7 Jan 1870",
    "died": "1954",
    "spouses": [{"name": "Della M. Ridenour", "born": "3 Sep 1876", "died": "22 Aug 1940"}],
    "source": {"pdf": "Alexander_Guthrie - Five Generations.pdf", "page": 3},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": "Direct PDF read confirmed name+dates."},
})

ENTRIES.append({
    "code": "A3B",
    "name": "William Franklin Romesburg",
    "sex": "M",
    "born": "19 Nov 1871",
    "died": "7 Dec 1948",
    "spouses": [{"name": "Sarah Catherine Hileman", "born": "16 Feb 1886"}],
    "source": {"pdf": "Alexander_Guthrie - Five Generations.pdf", "page": 3},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": "Direct PDF read confirmed name+dates."},
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
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "8731", "name": "John Robert Guthrie", "born": "26 Aug 1923", "verified_terminal": True},
        {"code": "8732", "name": "Rhoda Jane Guthrie", "born": "7 Sep 1925", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "874",
    "name": "Bruce Forman Guthrie",
    "sex": "M",
    "born": "23 Sep 1890",
    "spouses": [{"name": "Elizabeth Shaws", "born": "3 Nov 1894", "married": "15 Jun 1918"}],
    "residences": ["321 Dryden Rd., Ithaca, NY"],
    "source": {"pdf": "Absalom_Guthrie - One Generation.pdf", "page": 3},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "8741", "name": "Elizabeth Ann Guthrie", "born": "22 Aug 1923", "verified_terminal": True},
    ],
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
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": "Direct PDF read confirmed name+dates."},
})

ENTRIES.append({
    "code": "714",
    "name": "Harrison Franklin Barnes",
    "sex": "M",
    "born": "17 Dec 1871",
    "died": "14 Jan 1946",
    "spouses": [{"name": "Virginia Jennie Moyers", "born": "8 Feb 1871", "died": "8 Feb 1953", "married": "17 Jun 1900"}],
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 2},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": "Direct PDF read confirmed name+dates."},
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
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": "Direct PDF read confirmed name+dates."},
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
        {"code": "11311", "name": "Cora Ellen VanSickle", "born": "5 Aug 1893", "died": "6 Feb 1896", "flags": {"diedInInfancy": True}, "verified_terminal": True},
        {"code": "11312", "name": "Walter E. VanSickle", "born": "24 Jun 1895"},
        {"code": "11313", "name": "Rosa Virginia VanSickle", "born": "9 Nov 1897"},
        {"code": "11314", "name": "Asa R. VanSickle", "born": "6 Jan 1900", "died": "19 Dec 1905", "flags": {"diedInInfancy": True}, "verified_terminal": True},
        {"code": "11315", "name": "Quinter VanSickle", "born": "14 Aug 1902"},
        {"code": "11316", "name": "Ruby VanSickle", "born": "14 Feb 1912", "verified_terminal": True},
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
        {"code": "11321", "name": "Harry Milton Guthrie", "born": "16 Mar 1899", "verified_terminal": True},
        {"code": "11322", "name": "Grace Catherine Guthrie", "born": "14 May 1903"},
        {"code": "11323", "name": "Eula Guthrie", "born": "23 May"},
        {"code": "11324", "name": "Wayne Guthrie", "born": "5 Jan", "verified_terminal": True},
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
        {"code": "11341", "name": "Winnifred Ruth VanSickle", "born": "6 Jul 1896", "died": "Apr 1978", "verified_terminal": True},
        {"code": "11342", "name": "Evelyn VanSickle", "verified_terminal": True},
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
        {"code": "1752", "name": "Blanche Nicola", "born": "6 Jan 1892", "died": "18 Jul 1972", "verified_terminal": True},
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
        {"code": "1761", "name": "Annie E. Nicola", "born": "1896", "died": "1896", "flags": {"diedInInfancy": True}, "verified_terminal": True},
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
        {"code": "1771", "name": "Clyde E. Frey", "born": "27 Apr 1890", "died": "5 Sep 1914", "verified_terminal": True},
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
        {"code": "1792", "name": "Lawrence Carol", "born": "26 Dec 1903", "verified_terminal": True},
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
        {"code": "1961", "name": "Denely Berry", "verified_terminal": True},
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
        {"code": "11111", "name": "Earl Glenn Frazee", "born": "12 Sep 1913", "died": "6 Jan 1960", "verified_terminal": True},
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
        {"code": "11122", "name": "Glenn F. Windell", "verified_terminal": True},
        {"code": "11123", "name": "Paul C. Windell", "verified_terminal": True},
        {"code": "11124", "name": "Beatrice Windell", "verified_terminal": True},
        {"code": "11125", "name": "Bivilene Windell", "verified_terminal": True},
        {"code": "11126", "name": "Faye C. Windell", "verified_terminal": True},
        {"code": "11127", "name": "Eleanor Windell", "verified_terminal": True},
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
        {"code": "11131", "name": "Madeline Guthrie", "verified_terminal": True},
        {"code": "11132", "name": "Wilda Guthrie", "verified_terminal": True},
        {"code": "11133", "name": "Lorraine Guthrie", "verified_terminal": True},
        {"code": "11134", "name": "Robert M. Guthrie", "verified_terminal": True},
        {"code": "11135", "name": "Richard D. Guthrie", "verified_terminal": True},
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
        {"code": "11141", "name": "Eleanor Bestwick", "verified_terminal": True},
        {"code": "11142", "name": "Charles Bestwick", "verified_terminal": True},
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
        {"code": "11212", "name": "Russell E. Guthrie", "born": "11 Jul 1898", "verified_terminal": True},
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
        {"code": "11221", "name": "Bessie Gertude Trembly", "born": "21 Jun 1893", "verified_terminal": True},
        {"code": "11222", "name": "Lena Ellen Trembly", "born": "29 Apr 1896"},
        {"code": "11223", "name": "Earl C. Trembly", "born": "4 Nov 1903", "died": "28 Apr 1924", "verified_terminal": True},
        {"code": "11224", "name": "Regina C. Trembly", "born": "10 Feb 1914", "verified_terminal": True},
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
        {"code": "11231", "name": "Joseph Burns", "died": "19 Jan 1967", "verified_terminal": True},
        {"code": "11232", "name": "Samuel Herbert Burns", "verified_terminal": True},
        {"code": "11233", "name": "Robert Burns", "verified_terminal": True},
        {"code": "11234", "name": "Allen Burns", "verified_terminal": True},
        {"code": "11235", "name": "Mary Burns", "verified_terminal": True},
        {"code": "11236", "name": "Edith Burns", "verified_terminal": True},
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
        {"code": "11241", "name": "Erma Cupp", "verified_terminal": True},
        {"code": "11242", "name": "Vivian Cupp", "verified_terminal": True},
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
        {"code": "11411", "name": "Wilford Hartman", "verified_terminal": True},
        {"code": "11412", "name": "Carlton Hartman", "verified_terminal": True},
        {"code": "11413", "name": "Cora Hartman", "verified_terminal": True},
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
        {"code": "12231", "name": "May Brown", "verified_terminal": True},
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
        {"code": "12245", "name": "Jessie Harold DeBerry", "born": "20 Nov 1915", "died": "22 Nov 1915", "flags": {"diedInInfancy": True}, "verified_terminal": True},
        {"code": "12246", "name": "Herbert Lee DeBerry", "born": "8 Oct 1916", "died": "8 Oct 1916", "flags": {"diedInInfancy": True}, "verified_terminal": True},
        {"code": "12247", "name": "James Oliver DeBerry", "born": "24 Aug 1917"},
        {"code": "12248", "name": "Mary Alice DeBerry", "born": "25 Nov 1919"},
        {"code": "12249", "name": "Arletta Lucille DeBerry", "born": "11 Aug 1922"},
        {"code": "1224A", "name": "Albert Ray DeBerry", "born": "8 Oct 1924", "died": "20 Nov 1968"},
        {"code": "1224B", "name": "Flory Murle Lambert", "born": "1 Jul 1903", "died": "8 Feb 1968", "flags": {"stepChild": True}, "verified_terminal": True},
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
        {"code": "12271", "name": "DeBerry child", "verified_terminal": True},
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

# === Ward Barnes Guthrie's 4th child (the other 3 are in pages 76-80 batch) ===
ENTRIES.append({
    "code": "113314",
    "name": "Stephen Byron Guthrie",
    "sex": "M",
    "born": "25 Mar 1960",
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 80},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
})

# === More Lydia/Christian Nicola kids (completes the 13E*/174* SEE_REF cluster) ===
ENTRIES.append({
    "code": "13E3",
    "name": "Fredrick R. Nicola",
    "sex": "M",
    "born": "1891",
    "died": "24 Nov 1970",
    "spouses": [
        {"name": "Edna", "married": "1914", "order": 1},
        {"name": "Ethel", "born": "1903", "order": 2},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 23},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": "Direct PDF read confirmed name+dates."},
})

ENTRIES.append({
    "code": "13E7",
    "name": "Laura Bell Nicola",
    "sex": "F",
    "born": "1904",
    "spouses": [{"name": "James Rockwell", "married": "1918"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 23},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": "Direct PDF read confirmed name+dates."},
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
        {"code": "13F11", "name": "Samuel Playford Guthrie", "verified_terminal": True},
        {"code": "13F12", "name": "Junior Walter Guthrie", "born": "16 Jun 1922", "died": "26 Jan 1994"},
        {"code": "13F13", "name": "George D. Guthrie", "born": "1925", "verified_terminal": True},
        {"code": "13F14", "name": "William Guthrie", "verified_terminal": True},
        {"code": "13F15", "name": "Clarence Robert Guthrie", "verified_terminal": True},
        {"code": "13F16", "name": "Mabel Guthrie", "verified_terminal": True},
        {"code": "13F17", "name": "Pauline Guthrie", "verified_terminal": True},
        {"code": "13F18", "name": "Sarah R. Guthrie", "born": "11 Jul 1925", "died": "11 Jul 1925", "flags": {"diedInInfancy": True}, "verified_terminal": True},
        {"code": "13F19", "name": "Daisy M. Guthrie", "born": "11 Jul 1925", "verified_terminal": True},
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
        {"code": "13F51", "name": "Freda Beatrice Ditmore", "born": "30 Dec 1916", "verified_terminal": True},
        {"code": "13F52", "name": "Ethel Marie Ditmore", "born": "8 Jul 1919", "verified_terminal": True},
        {"code": "13F53", "name": "Nellie Pauline Ditmore", "born": "1 Apr 1921", "died": "1 Jun 1939", "verified_terminal": True},
        {"code": "13F54", "name": "Calvin Ray Ditmore", "born": "8 Mar 1924", "verified_terminal": True},
        {"code": "13F55", "name": "Thelma May Ditmore", "born": "8 Aug 1925", "verified_terminal": True},
        {"code": "13F56", "name": "Samuel Walter Ditmore, Jr.", "born": "21 Nov 1927", "verified_terminal": True},
        {"code": "13F57", "name": "Beulah Dreme Ditmore", "born": "14 Dec 1929", "verified_terminal": True},
        {"code": "13F58", "name": "Thomas Dale Ditmore", "born": "27 Aug 1934", "verified_terminal": True},
        {"code": "13F59", "name": "Ronald Lee Ditmore", "born": "15 Nov 1936", "verified_terminal": True},
        {"code": "13F5A", "name": "James Franklin Ditmore", "born": "2 Jun 1942", "verified_terminal": True},
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
        {"code": "13F78", "name": "Albert Lee Guthrie", "born": "10 Apr 1950", "died": "8 Jul 1950", "flags": {"diedInInfancy": True}, "verified_terminal": True},
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
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": "Direct PDF read confirmed name+dates."},
})

ENTRIES.append({
    "code": "A21",
    "name": "Isabelle Rachel Guthrie",
    "sex": "F",
    "born": "16 Apr 1869",
    "died": "24 Jul 1940",
    "spouses": [{"name": "Truman Elsworth Frazee", "born": "1868", "died": "9 May 1942", "married": "19 Dec 1895"}],
    "source": {"pdf": "Alexander_Guthrie - Five Generations.pdf", "page": 2},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": "Direct PDF read confirmed name+dates."},
    "children": [
        {"code": "A211", "name": "Asa Ralph Frazee", "born": "17 Dec 1896"},
        {"code": "A212", "name": "Walter Guthrie Frazee", "born": "18 Oct 1898", "died": "19 Oct 1988"},
        {"code": "A213", "name": "Frank Clark Frazee", "born": "4 Aug 1902"},
        {"code": "A214", "name": "Carrie Elizabeth Frazee", "born": "27 Sep 1906", "died": "6 May 1996"},
    ],
})

ENTRIES.append({
    "code": "A212",
    "name": "Walter Guthrie Frazee",
    "sex": "M",
    "born": "18 Oct 1898",
    "died": "19 Oct 1988",
    "buried": "Shady Grove",
    "spouses": [{"name": "Ila Roberta Evans", "born": "17 Aug 1909", "died": "29 May 1978", "married": "11 Apr 1936", "details": "dau of Owen C. & Cora B. [Umbel] Evans"}],
    "source": {"pdf": "Alexander_Guthrie - Five Generations.pdf", "page": 4},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "A2121", "name": "Norma Ruth Frazee", "born": "30 Aug 1938"},
        {"code": "A2122", "name": "Glenna Belle Frazee", "born": "15 Dec 1940"},
    ],
})

ENTRIES.append({
    "code": "A214",
    "name": "Carrie Elizabeth Frazee",
    "sex": "F",
    "born": "27 Sep 1906",
    "died": "6 May 1996",
    "spouses": [{"name": "Carlus Franklin Shaffer", "born": "20 Jul 1910", "married": "20 Sep 1941", "details": "son of Ami & Mary [Jones] Shaffer"}],
    "source": {"pdf": "Alexander_Guthrie - Five Generations.pdf", "page": 4},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "A2141", "name": "Darwin Roy Shaffer", "born": "8 Aug 1944", "verified_terminal": True, "details": "m. 3 Aug 1985 Patricia Rae Thomas Lawrence"},
        {"code": "A2142", "name": "Wendell E. Shaffer", "born": "14 May 1949", "died": "20 Oct 1949", "verified_terminal": True, "flags": {"diedInInfancy": True}},
    ],
})

ENTRIES.append({
    "code": "A24",
    "name": "Elizabeth (Lizzie) Alice Guthrie",
    "sex": "F",
    "born": "11 Jan 1877",
    "died": "27 Jun 1943",
    "spouses": [{"name": "Chancy L. Miller", "married": "1906"}],
    "source": {"pdf": "Alexander_Guthrie - Five Generations.pdf", "page": 2},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": "Direct PDF read confirmed name+dates."},
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
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": "Direct PDF read confirmed name+dates."},
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
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": "Direct PDF read confirmed name+dates."},
})

# === Stephen branch — Amy Guthrie's son line (565) ===


# === James gen 4-5 chains ===
ENTRIES.append({
    "code": "741",
    "name": "James Guthrie",
    "sex": "M",
    "born": "2 Feb 1879",
    "died": "29 Apr 1965",
    "spouses": [{"name": "Caroline (Carrie) B. Maust", "born": "21 Jun 1889", "died": "9 May 1965", "married": "6 Mar 1908"}],
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 21},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": "Direct PDF read confirmed name+dates."},
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
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": "Direct PDF read confirmed name+dates."},
})

ENTRIES.append({
    "code": "765",
    "name": "Laura Guthrie",
    "sex": "F",
    "born": "19 Apr 1889",
    "spouses": [{"name": "Oliver Clark Spiker"}],
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 4},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": "Direct PDF read confirmed name+dates."},
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
        {"code": "12336", "name": "Clarence Hermon Deal", "born": "29 Aug 1916", "died": "12 Dec 1916", "flags": {"diedInInfancy": True}, "verified_terminal": True},
        {"code": "12337", "name": "Mary Mae Deal", "born": "30 Sep 1918", "died": "13 Feb 1919", "flags": {"diedInInfancy": True}, "verified_terminal": True},
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
        {"code": "12353", "name": "Mabel Ellen DeBerry", "born": "5 Jan 1915", "died": "5 Jan 1915", "flags": {"diedInInfancy": True}, "verified_terminal": True},
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
        {"code": "12362", "name": "Lena Alfreda Feather", "born": "12 Feb 1909", "died": "27 Apr 1909", "flags": {"diedInInfancy": True}, "verified_terminal": True},
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
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": "Direct PDF read confirmed name+dates."},
})


# === James Marshall Guthrie (84, Absalom)'s children ===

ENTRIES.append({
    "code": "843",
    "name": "John Clyde Guthrie",
    "sex": "M",
    "born": "11 Jun 1881",
    "spouses": [{"name": "Gertrude Simpson", "born": "31 Mar 1881", "married": "9 Jan 1913"}],
    "residences": ["Logan, OH"],
    "source": {"pdf": "Absalom_Guthrie - One Generation.pdf", "page": 3},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "8431", "name": "John Simpson Guthrie", "born": "14 Nov 1913", "died": "4 Jul 1917", "verified_terminal": True, "flags": {"diedInInfancy": True}},
        {"code": "8432", "name": "James Emerson Guthrie", "born": "5 Dec 1916", "verified_terminal": True},
        {"code": "8433", "name": "Harriet Elizabeth Guthrie", "born": "10 Dec 1920", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "845",
    "name": "Mellie Irene Guthrie",
    "sex": "F",
    "born": "14 Aug 1888",
    "spouses": [{"name": "Ernest Brown", "born": "28 May 1884", "married": "13 Oct 1906"}],
    "residences": ["155 Overwood Road, Akron, OH"],
    "source": {"pdf": "Absalom_Guthrie - One Generation.pdf", "page": 3},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "8451", "name": "Jane Guthrie Brown", "born": "30 Mar 1919", "verified_terminal": True},
        {"code": "8452", "name": "Donald Ernest Brown", "born": "3 Jun 1921", "verified_terminal": True},
    ],
})

# === Alexander gen 4 — A22's kids ===
ENTRIES.append({
    "code": "A221",
    "name": "Martha Guthrie",
    "sex": "F",
    "born": "22 May 1899",
    "spouses": [{"name": "Theodore B. Alexander", "married": "6 Jul 1922"}],
    "source": {"pdf": "Alexander_Guthrie - Five Generations.pdf", "page": 4},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": "Direct PDF read confirmed name+dates."},
})

ENTRIES.append({
    "code": "A222",
    "name": "Grace Drusilla Guthrie",
    "sex": "F",
    "born": "3 Mar 1902",
    "died": "1988",
    "spouses": [{"name": "John Franks", "married": "19 Jan 1949"}],
    "source": {"pdf": "Alexander_Guthrie - Five Generations.pdf", "page": 4},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": "Direct PDF read confirmed name+dates."},
})

ENTRIES.append({
    "code": "A225",
    "name": "Paul Johnson Guthrie",
    "sex": "M",
    "born": "1 Nov 1910",
    "died": "5 May 1977",
    "spouses": [{"name": "Mildred Catherine Sturm", "died": "1989", "married": "23 Aug 1934"}],
    "source": {"pdf": "Alexander_Guthrie - Five Generations.pdf", "page": 4},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": "Direct PDF read confirmed name+dates."},
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
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": "Direct PDF read confirmed name+dates."},
})

ENTRIES.append({
    "code": "A412",
    "name": "Ralph W. Frankhouser",
    "sex": "M",
    "born": "22 Feb 1898",
    "died": "6 Nov 1981",
    "spouses": [{"name": "Georgia Lynn", "born": "1895"}],
    "source": {"pdf": "Alexander_Guthrie - Five Generations.pdf", "page": 6},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": "Direct PDF read confirmed name+dates."},
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
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": "Direct PDF read confirmed name+dates."},
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
        {"code": "122415", "name": "Judy Lee McNear", "born": "15 Dec 1943", "verified_terminal": True},
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
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": "Direct PDF read confirmed name+dates."},
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
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": "Direct PDF read confirmed name+dates."},
})


# === Stephen branch — more depth (53x sub-line) ===
ENTRIES.append({
    "code": "531",
    "name": "Mary Alice Guthrie",
    "sex": "F",
    "born": "about 1855",
    "source": {"pdf": "Stephen_Guthrie - One Generation.pdf", "page": 2},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
})

ENTRIES.append({
    "code": "535",
    "name": "Caroline Bell Guthrie",
    "sex": "F",
    "born": "1871",
    "died": "1943",
    "spouses": [{"name": "John Maust"}],
    "source": {"pdf": "Stephen_Guthrie - One Generation.pdf", "page": 2},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "5351", "name": "Oren Maust", "verified_terminal": True},
    ],
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
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": "Direct PDF read confirmed name+dates."},
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
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": "Direct PDF read confirmed name+dates."},
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
        {"name": "Mary Virginia Cupp", "born": "1 Oct 1912", "married": "5 Feb 1970",
         "order": 2,
         "details": "Same as #A454 in Alexander's branch. Daughter of Melvin R. and Alice Pearl [Frankhouser] Cupp. (Listed as 'Mary Cupp Summers' in some sources — Summers was her first married name.)"},
    ],
    "notes": "His second marriage links James↔Alexander.",
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 2},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": "Direct PDF read confirmed name+dates."},
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
        {"code": "12321", "name": "Ross Hoffman", "verified_terminal": True},
        {"code": "12322", "name": "Henrietta Hoffman"},
        {"code": "12323", "name": "Lucy Hoffman", "verified_terminal": True},
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
        {"code": "12343", "name": "Lucille Trembly", "born": "3 Feb 1916", "died": "22 Apr 1992", "verified_terminal": True},
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
        {"code": "12383", "name": "Charles J. Liston", "born": "3 Jun 1935", "died": "2 Jan 1962", "verified_terminal": True},
        {"code": "12384", "name": "Mrs. Willard Teets", "flags": {"stepChild": True}, "verified_terminal": True},
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
        {"code": "12411", "name": "Elmer Woodrow Messenger", "born": "8 Mar 1916", "died": "1955", "verified_terminal": True},
        {"code": "12412", "name": "Blaine Messenger"},
        {"code": "12413", "name": "Claude Messenger", "verified_terminal": True},
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
        {"code": "13211", "name": "Rena Guthrie", "verified_terminal": True},
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
        {"code": "13221", "name": "Ada C. Guthrie", "born": "25 Dec 1895", "died": "10 Oct 1898", "flags": {"diedInInfancy": True}, "verified_terminal": True},
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
        {"code": "13242", "name": "Flora May Trembly", "born": "14 Feb 1894", "verified_terminal": True},
        {"code": "13243", "name": "Nellie Clove Trembly", "born": "14 Feb 1895"},
        {"code": "13244", "name": "Chester Paul Trembly", "born": "13 Jun 1900", "died": "7 Jan 1976", "verified_terminal": True},
        {"code": "13245", "name": "Martin Trembly", "born": "23 Feb 1902", "verified_terminal": True},
        {"code": "13246", "name": "Maude Trembly", "born": "23 Feb 1903", "verified_terminal": True},
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
        {"code": "13251", "name": "Ethel Marie Wilhelm", "born": "25 Aug 1907", "died": "1 Mar 1970", "verified_terminal": True},
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
        {"code": "13266", "name": "Robert G. Lawson", "born": "13 Mar 1916", "died": "1969", "verified_terminal": True},
        {"code": "13267", "name": "Clarence S. Lawson", "born": "22 Mar 1920"},
        {"code": "13268", "name": "Sheldon Lawson", "born": "30 Jun 1922", "died": "1969", "verified_terminal": True},
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
        {"code": "13542", "name": "Herbert Ray Lewis", "born": "16 Apr 1917", "verified_terminal": True},
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
        {"code": "13652", "name": "Dora Hauger", "verified_terminal": True},
        {"code": "13653", "name": "Edna Hauger", "verified_terminal": True},
        {"code": "13654", "name": "Cora Hauger", "born": "3 Nov 1899"},
        {"code": "13655", "name": "Daughter", "died": "1923", "flags": {"diedInInfancy": True}, "verified_terminal": True},
        {"code": "13656", "name": "Pauline Hauger", "verified_terminal": True},
        {"code": "13657", "name": "Lois Hauger", "verified_terminal": True},
        {"code": "13658", "name": "Lulu Hauger", "verified_terminal": True},
        {"code": "13659", "name": "Herbert Hauger", "verified_terminal": True},
        {"code": "1365A", "name": "Grace Hauger", "verified_terminal": True},
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
        {"code": "13662", "name": "Dorthy Rolls DeBerry", "verified_terminal": True},
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
        {"code": "13811", "name": "John L. Teets", "verified_terminal": True},
        {"code": "13812", "name": "Fred Teets", "verified_terminal": True},
        {"code": "13813", "name": "Claude Teets", "verified_terminal": True},
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
        {"code": "13822", "name": "Charles R. Teets", "born": "1899", "died": "1916", "verified_terminal": True},
        {"code": "13823", "name": "Cora Teets", "born": "1902"},
        {"code": "13824", "name": "Harvey Teets", "born": "Aug 1904", "died": "27 Jan 1975", "verified_terminal": True},
        {"code": "13825", "name": "Marie Teets", "born": "11 Apr 1911", "died": "12 Jan 1978", "verified_terminal": True},
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
        {"code": "13831", "name": "Elizah Alen Uphold", "born": "1 May 1897", "died": "7 May 1958", "verified_terminal": True},
        {"code": "13832", "name": "Adam E. Uphold", "died": "31 May 1980", "verified_terminal": True},
        {"code": "13833", "name": "Gertrude Uphold", "verified_terminal": True},
        {"code": "13834", "name": "Jene Uphold", "verified_terminal": True},
        {"code": "13835", "name": "Delia Uphold", "verified_terminal": True},
        {"code": "13836", "name": "Sam Uphold", "verified_terminal": True},
        {"code": "13837", "name": "Orval Uphold", "verified_terminal": True},
        {"code": "13838", "name": "Theodore Uphold", "verified_terminal": True},
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
        {"code": "13841", "name": "Theadore Teets", "verified_terminal": True},
        {"code": "13842", "name": "Arthur Paul Teet", "born": "7 Dec 1920"},
        {"code": "13843", "name": "Maude Teets", "verified_terminal": True},
        {"code": "13844", "name": "Florence F. (Flora) Teets", "born": "31 Dec 1909"},
        {"code": "13845", "name": "Esta Teets", "verified_terminal": True},
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
        {"code": "13861", "name": "Robert Uphold", "verified_terminal": True},
        {"code": "13862", "name": "Cora Uphold", "born": "1 Jan 1904"},
        {"code": "13863", "name": "Bessie Uphold"},
        {"code": "13864", "name": "Edna Uphold", "born": "1906"},
        {"code": "13865", "name": "Grace Uphold"},
        {"code": "13866", "name": "Icie Myrtle Uphold"},
        {"code": "13867", "name": "Russel Uphold", "verified_terminal": True},
        {"code": "13868", "name": "Troy Uphold", "verified_terminal": True},
        {"code": "13869", "name": "Gladys Uphold", "verified_terminal": True},
        {"code": "1386A", "name": "Infant", "buried": "Keeler Glade Cemetery", "flags": {"diedInInfancy": True}, "verified_terminal": True},
        {"code": "1386B", "name": "Infant", "buried": "Keeler Glade Cemetery", "flags": {"diedInInfancy": True}, "verified_terminal": True},
        {"code": "1386C", "name": "Infant", "buried": "Keeler Glade Cemetery", "flags": {"diedInInfancy": True}, "verified_terminal": True},
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
        {"code": "13B22", "name": "Marie Edna Sikes", "born": "23 Mar 1907", "verified_terminal": True},
        # Second marriage
        {"code": "13B23", "name": "Hazel Pearl Bee", "born": "12 Sep 1912", "verified_terminal": True},
        {"code": "13B24", "name": "Verna Jane Bee", "born": "9 Aug 1915", "died": "1952", "verified_terminal": True},
        {"code": "13B25", "name": "Ester Mae Bee", "born": "24 Jul 1917", "verified_terminal": True},
        {"code": "13B26", "name": "Mary Catherine Bee", "born": "9 Jun 1922", "verified_terminal": True},
        {"code": "13B27", "name": "Charles Paul Bee", "born": "4 Mar 1930", "verified_terminal": True},
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
        {"code": "13C21", "name": "William R. Guthrie", "born": "25 May 1939", "verified_terminal": True},
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
        {"code": "13C52", "name": "Ocelea Elizabeth Smith", "born": "1 May 1926", "died": "4 May 1926", "flags": {"diedInInfancy": True}, "verified_terminal": True},
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
        {"code": "13C91", "name": "Emma Jean Guthrie", "verified_terminal": True},
        {"code": "13C92", "name": "J. R. Guthrie", "died": "13 Jan 1993", "verified_terminal": True},
        {"code": "13C93", "name": "Harvey (Harry) Guthrie", "verified_terminal": True},
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
        {"code": "13D21", "name": "Victor Leech", "verified_terminal": True},
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
        {"code": "13F86", "name": "Samuel Franklin Guthrie", "born": "21 Aug 1953", "verified_terminal": True},
        {"code": "13F87", "name": "Dorothy Elaine Guthrie", "born": "16 Apr 1956"},
        {"code": "13F88", "name": "George Daniel Guthrie", "born": "24 Mar 1958", "verified_terminal": True},
        {"code": "13F89", "name": "Cora Rose Guthrie", "born": "7 May 1960"},
        {"code": "13F8A", "name": "Mary Maude Guthrie", "born": "21 Feb 1962"},
        {"code": "13F8B", "name": "Glenn Wesley Guthrie", "born": "21 Feb 1962", "died": "21 Feb 1962", "flags": {"diedInInfancy": True}, "verified_terminal": True},
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
        {"code": "13FA1", "name": "Ralph Conaway", "verified_terminal": True},
        {"code": "13FA2", "name": "Freda Conaway", "verified_terminal": True},
        {"code": "13FA3", "name": "Lula Conaway", "verified_terminal": True},
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
        {"code": "13FC1", "name": "William (Billy) Casteel", "details": "son of Dale Casteel", "verified_terminal": True},
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
        {"code": "13FD1", "name": "Daughter", "details": "raised by John's sister Frances Frazee", "verified_terminal": True},
        # Second marriage
        {"code": "13FD2", "name": "Shirley Guthrie"},
        {"code": "13FD3", "name": "Janey I. Guthrie", "born": "14 Sep 1952", "died": "19 Apr 1953", "flags": {"diedInInfancy": True}, "buried": "Parnell cemetery", "verified_terminal": True},
        {"code": "13FD4", "name": "Donald (Buddy) Guthrie", "born": "about 1953", "verified_terminal": True},
        {"code": "13FD5", "name": "Lucy Guthrie", "verified_terminal": True},
        {"code": "13FD6", "name": "Billy Wade Guthrie", "born": "11 Oct 1957", "died": "21 Dec 1977", "verified_terminal": True},
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
        {"code": "13FE5", "name": "James T. Noss", "born": "29 Jun 1945", "died": "3 Jul 1966", "verified_terminal": True},
        {"code": "13FE6", "name": "Shirley Noss"},
        {"code": "13FE7", "name": "Robert E. Noss", "verified_terminal": True},
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
        {"code": "14121", "name": "Franklin Uphold", "born": "11 Dec 1911", "verified_terminal": True},
        {"code": "14122", "name": "Mary Virginia Uphold", "born": "30 Jul 1914", "died": "18 Oct 1914", "flags": {"diedInInfancy": True}, "verified_terminal": True},
        {"code": "14123", "name": "Charles M. Uphold", "born": "1925", "died": "8 Jul 1946", "verified_terminal": True},
        {"code": "14124", "name": "William Uphold", "died": "1948", "verified_terminal": True},
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
        {"code": "14182", "name": "Wendell Floyd Turner", "born": "18 Oct 1918", "verified_terminal": True},
        {"code": "14183", "name": "Sarapto Marie Turner", "born": "8 Apr 1919"},
        {"code": "14184", "name": "Daisy Winona Turner", "born": "30 Nov 1922", "verified_terminal": True},
        {"code": "14185", "name": "Earl Donald Turner", "born": "4 May 1927", "verified_terminal": True},
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
        {"code": "141A1", "name": "John Uphold", "verified_terminal": True},
        {"code": "141A2", "name": "Charley Uphold", "verified_terminal": True},
        {"code": "141A3", "name": "Basel Uphold, Jr.", "verified_terminal": True},
        {"code": "141A4", "name": "Walter Uphold", "verified_terminal": True},
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
        {"code": "14251", "name": "Charles B. Guthrie", "born": "10 Nov 1910", "died": "3 Dec 1910", "flags": {"diedInInfancy": True}, "verified_terminal": True},
        {"code": "14252", "name": "Edna Grace Guthrie", "born": "23 Apr 1912"},
        {"code": "14253", "name": "John Edward Guthrie", "born": "2 Jan 1914", "died": "5 Aug 1957", "verified_terminal": True},
        {"code": "14254", "name": "Scott Franklin Guthrie", "born": "7 Mar 1917", "died": "11 Feb 1948", "verified_terminal": True},
        {"code": "14255", "name": "Blaine Austin Guthrie", "born": "24 Dec 1927", "died": "9 Nov 1942", "verified_terminal": True},
        {"code": "14256", "name": "Nellie Mae Guthrie", "born": "8 Jan 1935", "died": "8 Jan 1935", "flags": {"diedInInfancy": True}, "verified_terminal": True},
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
        {"code": "14271", "name": "Edna Mae Guthrie", "verified_terminal": True},
        {"code": "14272", "name": "Emma Ruth Guthrie", "verified_terminal": True},
        {"code": "14273", "name": "Mary Eleanor Guthrie", "verified_terminal": True},
        {"code": "14274", "name": "Goldie Marie Guthrie", "verified_terminal": True},
        {"code": "14275", "name": "Ralph Guthrie", "residences": ["Florida"], "verified_terminal": True},
        {"code": "14276", "name": "Asa B. Guthrie", "residences": ["Barton, MD"], "verified_terminal": True},
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
        {"code": "14283", "name": "Mary Elizabeth Sines", "born": "23 Jan 1926", "died": "18 Oct 1975", "verified_terminal": True},
        {"code": "14284", "name": "Robert Jackson Sines", "born": "1 Jun 1928"},
        {"code": "14285", "name": "Martha Sines", "born": "Mar 1930", "died": "15 Aug 1930", "flags": {"diedInInfancy": True}, "verified_terminal": True},
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
        {"code": "14291", "name": "Martha Guthrie", "born": "8 Sep 1914", "notes": "daughter of Myrtle", "verified_terminal": True},
        {"code": "14292", "name": "Clyde Guthrie", "born": "4 Jun 1916"},
        {"code": "14293", "name": "Dorothy Guthrie", "born": "4 Jul 1918"},
        {"code": "14294", "name": "Fred Guthrie", "born": "28 Oct 1920"},
        {"code": "14295", "name": "Jessie Guthrie", "born": "20 Aug 1922", "verified_terminal": True},
        {"code": "14296", "name": "Mabel Guthrie", "born": "1 Apr 1924", "verified_terminal": True},
        {"code": "14297", "name": "Betty Guthrie", "born": "19 Feb 1927", "verified_terminal": True},
        {"code": "14298", "name": "Earl Guthrie, Jr.", "born": "28 Mar 1928"},
        {"code": "14299", "name": "Lucy Guthrie", "born": "26 Jul 1931"},
        {"code": "1429A", "name": "Glen Guthrie", "born": "27 Mar 1933", "verified_terminal": True},
        {"code": "1429B", "name": "Jack Guthrie", "born": "2 Feb 1936", "verified_terminal": True},
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
        {"code": "14321", "name": "Vernie Myers", "verified_terminal": True},
        {"code": "14322", "name": "Hazel Myers", "verified_terminal": True},
        {"code": "14323", "name": "Edna Myers", "verified_terminal": True},
        {"code": "14324", "name": "Pearl Myers", "verified_terminal": True},
        {"code": "14325", "name": "Effie Myers", "verified_terminal": True},
        {"code": "14326", "name": "Jessie Myers", "verified_terminal": True},
        {"code": "14327", "name": "Mildred Myers", "verified_terminal": True},
        {"code": "14328", "name": "Gilbert Myers", "verified_terminal": True},
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
        {"code": "14331", "name": "Samuel Darnell", "verified_terminal": True},
        {"code": "14332", "name": "Earl Darnell", "verified_terminal": True},
        {"code": "14333", "name": "Albert Darnell", "verified_terminal": True},
        {"code": "14334", "name": "Adam Darnell", "verified_terminal": True},
        {"code": "14335", "name": "Elmer Darnell", "verified_terminal": True},
        {"code": "14336", "name": "Pearl Darnell", "verified_terminal": True},
        {"code": "14337", "name": "Dorothy Darnell", "verified_terminal": True},
        {"code": "14338", "name": "Mae Darnell", "verified_terminal": True},
        {"code": "14339", "name": "Mary Darnell", "verified_terminal": True},
        {"code": "1433A", "name": "Sarah Darnell", "verified_terminal": True},
        {"code": "1433B", "name": "Roberta Darnell", "verified_terminal": True},
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
        {"code": "14344", "name": "Harry Cuppett", "verified_terminal": True},
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
        {"code": "14371", "name": "Emma Sliger", "verified_terminal": True},
        {"code": "14372", "name": "Jane Sliger", "verified_terminal": True},
        {"code": "14373", "name": "Anna Bell Sliger", "verified_terminal": True},
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
        {"code": "14381", "name": "William Herman Sliger", "born": "1 Jun 1923", "died": "15 Jul 1992", "verified_terminal": True},
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
        {"code": "14421", "name": "Infant son", "born": "22 Aug 1909", "died": "22 Aug 1909", "flags": {"diedInInfancy": True}, "verified_terminal": True},
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
        {"code": "14451", "name": "Ethel H. Friend", "born": "7 Jun 1913", "verified_terminal": True},
        {"code": "14452", "name": "Ivan Samuel Friend", "born": "7 Mar 1915"},
        {"code": "14453", "name": "Pearl Lovine Friend", "born": "29 Nov 1916"},
        {"code": "14454", "name": "Helen Dorothy Friend", "born": "12 Apr 1918"},
        {"code": "14455", "name": "Avis Mae Friend", "born": "28 Jun 1920"},
        {"code": "14456", "name": "Charles Orval Friend", "born": "3 Apr 1923", "died": "11 Aug 1985", "verified_terminal": True},
        {"code": "14457", "name": "Virgil William Friend", "born": "17 Mar 1926", "died": "9 May 1994", "verified_terminal": True},
        {"code": "14458", "name": "Sylvia Marie Friend", "born": "23 Jul 1930", "died": "17 Jun 1935", "flags": {"diedInInfancy": True}, "verified_terminal": True},
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
        {"code": "14462", "name": "Clifford E. (Buck) Thomas", "verified_terminal": True},
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
        {"code": "14471", "name": "Infant son", "born": "11 Feb 1922", "died": "11 Feb 1922", "flags": {"diedInInfancy": True}, "verified_terminal": True},
        {"code": "14472", "name": "Jessie Mae Thomas", "born": "25 May 1923", "died": "30 Sep 1931", "buried": "Shady Grove Cemetery, WV", "verified_terminal": True},
        {"code": "14473", "name": "James Robert Thomas", "born": "2 Mar 1930", "died": "22 Jun 1933", "buried": "Shady Grove Cemetery, WV", "verified_terminal": True},
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
        {"code": "14483", "name": "Charles Ford Strawser", "born": "6 Jun 1923", "verified_terminal": True},
        {"code": "14484", "name": "Lucilla V. Strawser", "born": "16 Nov 1926", "verified_terminal": True},
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
        {"code": "14512", "name": "Charles D. H. Guthrie", "born": "18 Dec 1905", "verified_terminal": True},
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
        {"code": "14542", "name": "Rosala V. Blosser", "verified_terminal": True},
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
        {"code": "14551", "name": "Leonard G. Baily", "born": "15 Dec 1914", "verified_terminal": True},
        {"code": "14552", "name": "James Baily", "born": "12 Dec 1917", "verified_terminal": True},
        {"code": "14553", "name": "Warren H. Baily", "born": "15 Jun 1921", "verified_terminal": True},
        {"code": "14554", "name": "Betty J. Baily", "born": "28 Feb 1927", "verified_terminal": True},
        {"code": "14555", "name": "Donald Baily", "born": "24 Apr 1931", "verified_terminal": True},
        {"code": "14556", "name": "Robert D. Baily", "born": "28 Jun 1934", "verified_terminal": True},
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
        {"code": "14582", "name": "Vernice Elaine Guthrie", "born": "13 Nov 1923", "verified_terminal": True},
        {"code": "14583", "name": "Rita Guthrie", "born": "4 Mar 1926", "verified_terminal": True},
        {"code": "14584", "name": "Wallace J. Hinkle", "flags": {"adopted": True}, "verified_terminal": True},
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
        {"code": "14591", "name": "Charles Cole, Jr.", "verified_terminal": True},
        {"code": "14592", "name": "Sarah Jeremiah Cole", "verified_terminal": True},
        {"code": "14593", "name": "Robert Cole", "verified_terminal": True},
        {"code": "14594", "name": "Betty Sue Cole", "verified_terminal": True},
        {"code": "14595", "name": "Ronald Cole", "verified_terminal": True},
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
        {"code": "14611", "name": "Irene Dodid", "born": "15 Apr 1905", "died": "19 Jul 1909", "flags": {"diedInInfancy": True}, "verified_terminal": True},
        {"code": "14612", "name": "Herbert Dodid", "born": "22 Mar 1907", "died": "19 Jul 1907", "flags": {"diedInInfancy": True}, "verified_terminal": True},
        {"code": "14613", "name": "George E. Dodid", "born": "27 Mar 1909"},
        # Second marriage
        {"code": "14614", "name": "Birges (Birdie) Agnes Miller", "born": "9 Jul 1915"},
        {"code": "14615", "name": "Violet Miller", "verified_terminal": True},
        {"code": "14616", "name": "Person Miller", "verified_terminal": True},
        {"code": "14617", "name": "Mable Miller", "born": "29 Jul 1917", "verified_terminal": True},
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
        {"code": "14621", "name": "James Miller", "born": "1917", "died": "1918", "flags": {"diedInInfancy": True}, "verified_terminal": True},
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
        {"code": "14671", "name": "Betty Lou Jordon", "born": "11 Oct 1939", "verified_terminal": True},
        {"code": "14672", "name": "Floyd Jordon", "born": "12 Oct 1942", "verified_terminal": True},
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
        {"code": "14711", "name": "Emma C. Kahl", "born": "1906", "verified_terminal": True},
        {"code": "14712", "name": "Opal I. Kahl", "born": "1908", "verified_terminal": True},
        {"code": "14713", "name": "Russel R. Kahl", "born": "1910", "verified_terminal": True},
        {"code": "14714", "name": "Ralph Kahl", "born": "19 Apr 1913"},
        {"code": "14715", "name": "Edna M. Kahl", "born": "1915", "verified_terminal": True},
        {"code": "14716", "name": "Floyd R. Kahl", "born": "1917", "verified_terminal": True},
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
        {"code": "14721", "name": "Gertrude Guthrie", "verified_terminal": True},
        {"code": "14722", "name": "Ruth Guthrie", "verified_terminal": True},
        {"code": "14723", "name": "Leona Guthrie", "verified_terminal": True},
        {"code": "14724", "name": "Mildred Guthrie", "verified_terminal": True},
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
        {"code": "14814", "name": "Lillie M. McKenzie", "born": "8 Feb 1925", "verified_terminal": True},
        {"code": "14815", "name": "Alice B. McKenzie", "born": "23 Jul 1926"},
        {"code": "14816", "name": "Chester F. McKenzie", "born": "15 Jan 1928", "verified_terminal": True},
        {"code": "14817", "name": "Garnet Grace McKenzie", "born": "21 Aug 1929", "verified_terminal": True},
        {"code": "14818", "name": "James R. McKenzie", "born": "8 Jun 1931", "died": "1 Oct 1931", "flags": {"diedInInfancy": True}, "verified_terminal": True},
        {"code": "14819", "name": "Martha Jane McKenzie", "born": "29 Jul 1933", "died": "5 Dec 1933", "flags": {"diedInInfancy": True}, "verified_terminal": True},
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
        {"code": "14822", "name": "Charles H. Guthrie", "verified_terminal": True},
        {"code": "14823", "name": "Virginia Guthrie", "born": "17 Nov 1922"},
        {"code": "14824", "name": "Samuel F. Guthrie", "verified_terminal": True},
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
        {"code": "14841", "name": "Harman Guthrie", "born": "1918", "verified_terminal": True},
        # Second marriage
        {"code": "14842", "name": "Arrena Guthrie"},
        {"code": "14843", "name": "Pauline Guthrie", "verified_terminal": True},
        {"code": "14844", "name": "A. J. Guthrie", "verified_terminal": True},
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
        {"code": "14851", "name": "Delbert Guthrie", "born": "8 Jun 1928", "flags": {"adopted": True}, "notes": "nephew — son of Helen J. (#1489); see 14891", "verified_terminal": True},
        {"code": "14852", "name": "Irene McKenzie", "flags": {"adopted": True}, "notes": "niece", "verified_terminal": True},
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
        {"code": "14862", "name": "Infant", "flags": {"diedInInfancy": True}, "verified_terminal": True},
        {"code": "14863", "name": "Infant", "flags": {"diedInInfancy": True}, "verified_terminal": True},
        # Second marriage
        {"code": "14864", "name": "Irma M. Baker", "born": "13 Jan 1930", "verified_terminal": True},
        {"code": "14865", "name": "Thomas A. Baker", "born": "19 Jul 1932", "verified_terminal": True},
        {"code": "14866", "name": "Donald Franklin Baker", "born": "9 Oct 1935", "verified_terminal": True},
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
        {"code": "14872", "name": "Perry Franklin Guthrie", "born": "28 Nov 1928", "verified_terminal": True},
        {"code": "14873", "name": "Herbert Lester Guthrie", "born": "5 Jul 1933", "verified_terminal": True},
        {"code": "14874", "name": "Ray Marshall Guthrie", "born": "21 Apr 1936", "verified_terminal": True},
        {"code": "14875", "name": "Shirley Ann Guthrie", "born": "1 Feb 1943", "verified_terminal": True},
        {"code": "14876", "name": "James E. Guthrie, Jr.", "born": "24 Apr 1945", "verified_terminal": True},
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
        {"code": "14883", "name": "Marie Brandgard", "born": "29 Jan 1930", "died": "18 Feb 1930", "flags": {"diedInInfancy": True}, "verified_terminal": True},
        {"code": "14884", "name": "Pearl L. Brandgard", "born": "5 May 1934"},
        {"code": "14885", "name": "Peter Ray Brandgard, Jr.", "born": "5 Jan 1936"},
        {"code": "14886", "name": "Ralph S. Brandgard", "born": "16 Jun 1938", "verified_terminal": True},
        {"code": "14887", "name": "Walter Joseph Brandgard", "born": "5 Nov 1939", "died": "19 Dec 1951", "verified_terminal": True},
        {"code": "14888", "name": "Laura Bell Brandgard", "born": "16 Mar 1940", "died": "3 Aug 1940", "flags": {"diedInInfancy": True}, "verified_terminal": True},
        {"code": "14889", "name": "John R. Brandgard", "born": "18 Oct 1942", "verified_terminal": True},
        {"code": "1488A", "name": "Clarence R. Brandgard", "born": "7 Nov 1944", "verified_terminal": True},
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
        {"code": "14891", "name": "Delbert Guthrie", "born": "8 Jun 1928", "notes": "Raised by Rev. Oliver R. and Bessie Hart his aunt (see 14851)", "verified_terminal": True},
        {"code": "14892", "name": "Ester Leona Tate", "born": "8 May 1933"},
        {"code": "14893", "name": "Paul Kenneth Tate", "born": "14 Dec 1935", "verified_terminal": True},
        {"code": "14894", "name": "Elenor Delores Tate", "born": "7 Nov 1939", "verified_terminal": True},
        {"code": "14895", "name": "Elsie Loretta Tate", "born": "25 Jun 1941", "verified_terminal": True},
        {"code": "14896", "name": "Nancy Arlene Tate", "born": "30 May 1945", "verified_terminal": True},
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
        {"code": "16212", "name": "Thomas Ugene Moyers", "born": "16 Jan 1918", "verified_terminal": True},
        {"code": "16213", "name": "Walter Moyers, Jr.", "verified_terminal": True},
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
        {"code": "16236", "name": "Katherline Grace Moyers", "born": "21 Jan 1931", "died": "21 Jan 1931", "flags": {"diedInInfancy": True}, "verified_terminal": True},
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
        {"code": "16242", "name": "Norval G. Wright", "born": "1924", "died": "7 Jan 1944", "died_place": "Italy during WW II", "verified_terminal": True},
        {"code": "16243", "name": "Gladys Marie Wright", "born": "28 Aug 1927"},
        {"code": "16244", "name": "Vivian Wright", "verified_terminal": True},
        {"code": "16245", "name": "Naomi Irene Wright", "born": "22 Aug 1935", "died": "23 Aug 1935", "flags": {"diedInInfancy": True}, "buried": "Shady Grove Cemetery, WV", "verified_terminal": True},
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
        {"code": "16312", "name": "Earl Jackson Nicola", "born": "26 Sep 1909", "verified_terminal": True},
        {"code": "16313", "name": "Ray Judson Nicola", "born": "4 Apr 1912", "died": "4 Sep 1935", "verified_terminal": True},
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
        {"code": "16442", "name": "James Allen Harshbarger", "born": "6 Dec 1965", "verified_terminal": True},
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
        {"code": "16453", "name": "Doris Jean Fresh", "born": "4 Nov 1943", "verified_terminal": True},
        {"code": "16454", "name": "Infant Daughter", "born": "4 Nov 1943", "died": "4 Nov 1943", "flags": {"diedInInfancy": True}, "verified_terminal": True},
        {"code": "16455", "name": "Infant Daughter", "born": "4 Nov 1943", "died": "5 Nov 1943", "flags": {"diedInInfancy": True}, "verified_terminal": True},
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
        {"code": "16481", "name": "Infant son", "born": "12 Aug 1943", "died": "12 Aug 1943", "flags": {"diedInInfancy": True}, "verified_terminal": True},
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
        {"code": "164B1", "name": "Charles Marion Ressler", "born": "11 Jun 1947", "verified_terminal": True},
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
        {"code": "16632", "name": "Vernice Ann Harshbarger", "born": "20 Mar 1954", "died": "22 Mar 1954", "flags": {"diedInInfancy": True}, "buried": "Shady Grove Cemetery, WV", "verified_terminal": True},
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
        {"code": "17111", "name": "Clarence Webster Spiker", "born": "9 Jun 1906", "died": "2 Jul 1932", "verified_terminal": True},
        {"code": "17112", "name": "Ivon Theadore Spiker", "born": "12 Dec 1910", "verified_terminal": True},
        {"code": "17113", "name": "Rosa Silvia Spiker", "born": "24 May 1917", "verified_terminal": True},
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
        {"code": "17121", "name": "Floyd Sanford Spiker", "born": "8 Oct 1907", "died": "6 Jun 1944", "died_place": "France", "verified_terminal": True},
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
        {"code": "17131", "name": "Ralph Ersel Spiker", "born": "17 Jan 1910", "died": "18 Dec 1912", "flags": {"diedInInfancy": True}, "verified_terminal": True},
        {"code": "17132", "name": "Edna Mae Spiker", "born": "27 Aug 1911", "verified_terminal": True},
        {"code": "17133", "name": "Mildred Maud Spiker", "born": "13 Mar 1916", "verified_terminal": True},
        {"code": "17134", "name": "Shirel Victoria Spiker", "born": "6 Jul 1918", "verified_terminal": True},
        {"code": "17135", "name": "Thelma Olieta Spiker", "born": "2 Dec 1921"},
        {"code": "17136", "name": "Ruth Virginia Spiker", "born": "23 Apr 1923", "verified_terminal": True},
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
        {"code": "17231", "name": "Homer Loid Harshbarger", "born": "27 Sep 1902", "died": "6 Apr 1927", "verified_terminal": True},
        {"code": "17232", "name": "Emma Harshbarger", "born": "30 Jan 1906", "verified_terminal": True},
        {"code": "17233", "name": "Jeremiah Joseph Harshbarger", "born": "6 Jul 1911", "verified_terminal": True},
        {"code": "17234", "name": "David Harshbarger", "born": "9 Dec 1913", "verified_terminal": True},
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
        {"code": "17281", "name": "Robert Eugene Guthrie", "born": "6 Feb 1929", "died": "7 Feb 1929", "flags": {"diedInInfancy": True}, "verified_terminal": True},
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
        {"code": "172B1", "name": "Donald Bartholomew", "born": "4 Feb 1923", "died": "9 Feb 1923", "flags": {"diedInInfancy": True}, "verified_terminal": True},
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
        {"name": "Susannah A. Thomas", "born": "31 Jan 1881", "died": "23 Aug 1929", "married": "21 May 1903",
         "details": "Same as #1442 — daughter of Barbara Ellen Guthrie #144.", "order": 1},
        {"name": "Martha (Matt) Bishoff Ringer", "born": "14 Sep 1866", "died": "29 Dec 1944", "married": "6 May 1932",
         "details": "Widow of Noah Ringer.", "order": 2},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 34},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "17311", "name": "Infant son", "born": "22 Aug 1909", "died": "22 Aug 1909", "flags": {"diedInInfancy": True}, "verified_terminal": True},
        {"code": "17312", "name": "Chester Martin Nicola", "born": "7 Oct 1914", "verified_terminal": True},
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
        {"code": "17331", "name": "Harry C. Friend", "born": "23 May 1910", "died": "27 May 1910", "flags": {"diedInInfancy": True}, "verified_terminal": True},
        {"code": "17332", "name": "Goldie Marie Friend", "born": "24 Oct 1911"},
        {"code": "17333", "name": "Gilbert Arnold Friend", "born": "1 Aug 1914", "died": "28 Feb 1951"},
        {"code": "17334", "name": "Frank William Friend"},
        {"code": "17335", "name": "Edna Friend", "born": "2 May 1919"},
        {"code": "17336", "name": "Junior Clinton Friend", "born": "24 May 1928"},
        {"code": "17337", "name": "Thelma Grace Friend", "born": "13 Mar 1930", "verified_terminal": True},
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
        {"code": "17411", "name": "Mildred Nicola", "verified_terminal": True},
        {"code": "17412", "name": "Helen Nicola", "verified_terminal": True},
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
        {"code": "17431", "name": "Paul Nicola", "verified_terminal": True},
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
        {"code": "17441", "name": "Clarence Herbert Nicola Jr.", "born": "20 Nov 1920", "verified_terminal": True},
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
        {"code": "17451", "name": "Ruth Bertha Nicola", "born": "31 Aug 1923", "verified_terminal": True},
        {"code": "17452", "name": "Hilda Colleen Nicola", "born": "6 Oct 1925"},
        {"code": "17453", "name": "Howard Andrew Nicola", "born": "12 May 1928", "verified_terminal": True},
        {"code": "17454", "name": "Joan Nicola", "born": "23 Oct 1930", "verified_terminal": True},
        {"code": "17455", "name": "Bernald Nale Nicola", "born": "30 Jul 1937", "verified_terminal": True},
        {"code": "17456", "name": "Dorsey Eugene Nicola", "born": "5 Apr 1940", "verified_terminal": True},
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
        {"code": "17471", "name": "Son", "verified_terminal": True},
        {"code": "17472", "name": "Son", "verified_terminal": True},
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
        {"code": "17621", "name": "Robert Martin Miller", "born": "8 Aug 1920", "verified_terminal": True},
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
        {"code": "17726", "name": "James William Frey", "born": "4 Aug 1923", "died": "19 Jan 1939", "verified_terminal": True},
        {"code": "17727", "name": "Lelia Margaret Frey", "born": "6 Sep 1925"},
        {"code": "17728", "name": "George Calvin Frey", "born": "1 Mar 1927"},
        {"code": "17729", "name": "Charles Leon Frey", "born": "17 Aug 1929"},
        {"code": "1772A", "name": "Daniel Harold Frey", "born": "17 Jun 1931"},
        {"code": "1772B", "name": "Joanne Frey", "died": "in infancy", "flags": {"diedInInfancy": True}, "verified_terminal": True},
        {"code": "1772C", "name": "John Thomas Frey"},
        {"code": "1772D", "name": "Darl Eugene Frey"},
        {"code": "1772E", "name": "Donald Semmelman", "flags": {"stepChild": True}, "verified_terminal": True},
        {"code": "1772F", "name": "Lewis Semmelman", "flags": {"stepChild": True}, "verified_terminal": True},
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
        {"code": "17731", "name": "Harold Frey", "born": "12 Dec 1920", "verified_terminal": True},
        {"code": "17732", "name": "Evelyn Frey", "born": "23 Jan 1923", "verified_terminal": True},
        {"code": "17733", "name": "Ellen Frey", "born": "6 May 1927", "verified_terminal": True},
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
        {"code": "17741", "name": "Ruth Frey", "born": "14 Sep 1921", "verified_terminal": True},
        {"code": "17742", "name": "Infant son", "flags": {"diedInInfancy": True}, "verified_terminal": True},
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
        {"code": "17751", "name": "William A. Frey", "born": "15 Apr 1922", "verified_terminal": True},
        {"code": "17752", "name": "Geraldine Frey", "born": "9 Apr 1925", "verified_terminal": True},
        {"code": "17753", "name": "Don Robert Frey", "born": "28 Apr 1927"},
        {"code": "17754", "name": "Hilda L. Frey", "born": "1 Aug 1934", "verified_terminal": True},
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
        {"code": "17761", "name": "Dorothy V. Frey", "born": "28 Jun 1926", "verified_terminal": True},
        {"code": "17762", "name": "William D. Frey", "born": "30 May 1934", "verified_terminal": True},
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
        {"code": "17771", "name": "Jean Frey", "born": "9 Nov 1933", "verified_terminal": True},
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
        {"code": "17811", "name": "Vincent Lee Ball", "born": "10 Feb 1922", "verified_terminal": True},
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
        {"code": "17832", "name": "Charles William Ball", "born": "21 Aug 1923", "verified_terminal": True},
        {"code": "17833", "name": "Russell Edgar Ball", "born": "3 Dec 1924", "died_alt": "1926"},
        {"code": "17834", "name": "Leo Dennis Ball", "verified_terminal": True},
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
        {"code": "17911", "name": "Harold D. Gelhausen", "born": "13 Sep 1934", "verified_terminal": True},
        {"code": "17912", "name": "Georgie Lee Gelhausen", "born": "2 Aug 1936", "verified_terminal": True},
        {"code": "17913", "name": "Freddie Gelhausen", "verified_terminal": True},
        {"code": "17914", "name": "Sonny Gelhausen", "verified_terminal": True},
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
        {"code": "111211", "name": "Joseph Harry Windell", "verified_terminal": True},
        {"code": "111212", "name": "Jean Windell", "verified_terminal": True},
        {"code": "111213", "name": "Charlotte Windell", "verified_terminal": True},
        {"code": "111214", "name": "Bonnie Windell", "verified_terminal": True},
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
        {"code": "112111", "name": "Elizabeth J. Frankhouser", "verified_terminal": True},
        {"code": "112112", "name": "Lucile Jane Frankhouser", "verified_terminal": True},
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
        {"code": "112221", "name": "Richard A. Smith", "verified_terminal": True},
        {"code": "112222", "name": "Betty Smith", "verified_terminal": True},
        {"code": "112223", "name": "Patricia Ann Smith", "verified_terminal": True},
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
        {"code": "112431", "name": "Donald Dodge", "verified_terminal": True},
        {"code": "112432", "name": "Ronald Dodge", "verified_terminal": True},
        {"code": "112433", "name": "Marion Dodge", "verified_terminal": True},
        {"code": "112434", "name": "Dale Dodge", "verified_terminal": True},
        {"code": "112435", "name": "Michael Dodge", "verified_terminal": True},
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
        {"code": "113121", "name": "Orley D. VanSickle", "born": "8 Mar 1930", "died": "8 Mar 1930", "flags": {"diedInInfancy": True}, "verified_terminal": True},
        {"code": "113122", "name": "Ersel R. Hewitt", "born": "6 Feb 1925", "died": "6 Oct 1982", "flags": {"adopted": True}, "verified_terminal": True},
        {"code": "113123", "name": "Jessie Hewitt", "flags": {"adopted": True}, "verified_terminal": True},
        {"code": "113124", "name": "Elsie Hewitt", "born": "15 Jul 1928", "flags": {"adopted": True}, "verified_terminal": True},
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
        {"code": "113131", "name": "Inez M. Burd", "born": "3 Sep 1928", "died": "11 Nov 1928", "flags": {"diedInInfancy": True}, "verified_terminal": True},
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
        {"code": "113231", "name": "Fyock child", "verified_terminal": True},
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
        {"code": "113431", "name": "Rebecca VanSickle", "verified_terminal": True},
        {"code": "113432", "name": "David VanSickle, Jr.", "verified_terminal": True},
        {"code": "113433", "name": "John R. VanSickle", "verified_terminal": True},
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
        {"code": "113621", "name": "Jean Slaubaugh", "verified_terminal": True},
        {"code": "113622", "name": "Donald Ray Slaubaugh", "born": "3 Jan 1939", "verified_terminal": True},
        {"code": "113623", "name": "Ruth Ann Slaubaugh", "verified_terminal": True},
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
        {"code": "122421", "name": "Hugh Charles Gerken", "flags": {"stepChild": True}, "verified_terminal": True},
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
        {"code": "12244B", "name": "David Eugene DeWitt", "born": "3 Feb 1950", "flags": {"stepChild": True}, "verified_terminal": True},
        {"code": "12244C", "name": "Carolyn Sue DeWitt", "born": "15 Mar 1951", "flags": {"stepChild": True}, "verified_terminal": True},
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
        {"code": "122471", "name": "Delbert Dwain DeBerry", "born": "14 Aug 1939", "verified_terminal": True},
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
        {"code": "122481", "name": "Everett Dwight Wolfe", "born": "15 May 1936", "died": "9 Dec 1936", "flags": {"diedInInfancy": True}, "buried": "Mt. Moriah Cemetery, Valley Point, WV", "verified_terminal": True},
        {"code": "122482", "name": "Jessie Allen Hornick", "born": "14 Apr 1943", "verified_terminal": True},
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
        {"code": "122491", "name": "Lenna Italia Mary Bernabei", "born": "28 Jul 1941", "flags": {"adopted": True}, "verified_terminal": True},
        {"code": "122492", "name": "Janice Margaret Mae Bernabei", "born": "13 Jul 1943", "flags": {"adopted": True}, "verified_terminal": True},
        {"code": "122493", "name": "Arthur Umberto Charles Bernabei", "born": "31 Oct 1944", "flags": {"adopted": True}, "verified_terminal": True},
        {"code": "122494", "name": "Lorraine Jestina Arletta Bernabei", "born": "3 Jan 1946", "flags": {"adopted": True}, "verified_terminal": True},
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
        {"code": "123221", "name": "Cecil Keefover", "verified_terminal": True},
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
        {"code": "123315", "name": "Everett Clyde Deal", "born": "28 Jun 1946", "verified_terminal": True},
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
        {"code": "123327", "name": "Glenn Dale Shaffer", "born": "3 Feb 1943", "died": "3 Feb 1943", "flags": {"diedInInfancy": True}, "verified_terminal": True},
        {"code": "123328", "name": "Sharlett Shaffer", "born": "24 May 1944", "died": "3 Jun 1944", "flags": {"diedInInfancy": True}, "verified_terminal": True},
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
        {"code": "123331", "name": "Charles Bruce Deal", "born": "1 Feb 1938", "died": "25 Jan 1956", "verified_terminal": True},
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
        {"code": "123383", "name": "Donald Perry Deal", "born": "5 Mar 1952", "verified_terminal": True},
        {"code": "123384", "name": "Kay Marlene Deal", "born": "6 Dec 1958"},
        {"code": "123385", "name": "Mark Cecil Deal", "born": "8 Jun 1962", "verified_terminal": True},
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
        {"code": "123411", "name": "Carolyn", "flags": {"stepChild": True}, "verified_terminal": True},
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
        {"code": "123421", "name": "Cynthia Louise Kotchek", "born": "25 Aug 1947", "verified_terminal": True},
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
        {"code": "123514", "name": "Jack Dempsey DeBerry", "born": "4 Dec 1942", "verified_terminal": True},
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
        {"code": "123613", "name": "Harold Gene Wiles", "born": "17 Jan 1943", "born_place": "Albright, WV", "verified_terminal": True},
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
        {"code": "123661", "name": "Kathy Lynn Feather", "born": "6 Nov 1958", "verified_terminal": True},
        {"code": "123662", "name": "Mark Lee Feather", "born": "5 Oct 1962", "verified_terminal": True},
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
        {"code": "123711", "name": "Jon Max Miller", "born": "16 Oct 1939", "verified_terminal": True},
        {"code": "123712", "name": "Marvin Kay Miller", "born": "29 Apr 1945", "verified_terminal": True},
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
        {"code": "123721", "name": "Mary Romano", "verified_terminal": True},
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
        {"code": "123731", "name": "Mary Elizabeth Miller", "verified_terminal": True},
        {"code": "123732", "name": "Martha Sue Miller", "verified_terminal": True},
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
        {"code": "123811", "name": "Walter F. Addis", "born": "1936", "died": "1937", "flags": {"diedInInfancy": True}, "verified_terminal": True},
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
        {"code": "123821", "name": "Judith Ann Liston", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "12412",
    "name": "Blaine Messinger",
    "sex": "M",
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 44},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "124121", "name": "Donna Lee Messinger", "verified_terminal": True},
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
        {"code": "132122", "name": "Judith Eileen (Judy) Guthrie", "born": "19 Dec 1954", "verified_terminal": True},
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
        {"code": "132131", "name": "Kenneth Guthrie", "verified_terminal": True},
        {"code": "132132", "name": "James Guthrie", "verified_terminal": True},
        {"code": "132133", "name": "Frances Guthrie", "verified_terminal": True},
        {"code": "132134", "name": "Ralph V. Guthrie", "born": "1960", "died": "14 Jul 1979", "verified_terminal": True},
        {"code": "132135", "name": "Ernest Guthrie", "verified_terminal": True},
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
        {"code": "132153", "name": "Raymond Myers", "verified_terminal": True},
        {"code": "132154", "name": "Vickey Myers"},
        {"code": "132155", "name": "Ronald M. Myers", "born": "23 Dec 1953", "died": "16 Jun 1954", "flags": {"diedInInfancy": True}, "verified_terminal": True},
        {"code": "132156", "name": "Kieth Myers", "born": "1953", "verified_terminal": True},
        {"code": "132157", "name": "Marlene Margaret Myers"},
        {"code": "132158", "name": "Shelly Myers", "verified_terminal": True},
        {"code": "132159", "name": "Erick Myers", "verified_terminal": True},
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
        {"code": "132181", "name": "Gary Michael Smith", "verified_terminal": True},
        {"code": "132182", "name": "Tamara Lynn Smith", "born": "24 Dec 1966"},
        {"code": "132183", "name": "Kimberly Ellen Smith", "born": "1 Nov 1969", "died": "2 Nov 1969", "flags": {"diedInInfancy": True}, "verified_terminal": True},
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
        {"code": "132231", "name": "Hagan L. Guthrie", "born": "27 Mar 1930", "verified_terminal": True},
        {"code": "132232", "name": "Marlin Guthrie", "born": "20 Feb 1932", "verified_terminal": True},
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
        {"code": "132241", "name": "Myron L. VanSickle", "born": "10 Jun 1941", "verified_terminal": True},
        {"code": "132242", "name": "Mark J. VanSickle", "born": "29 Aug 1951", "verified_terminal": True},
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
        {"code": "132411", "name": "Clyde Epley, Jr.", "verified_terminal": True},
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
        {"code": "132431", "name": "Josephine Eleanor Wendell", "born": "8 Sep 1917", "verified_terminal": True},
        {"code": "132432", "name": "Betty Wendell", "verified_terminal": True},
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
        {"code": "132621", "name": "Iris Lawson", "flags": {"diedInInfancy": True}, "verified_terminal": True},
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
        {"code": "132631", "name": "Phyllis Joann Kelly", "born": "28 Nov 1950", "verified_terminal": True},
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
        {"code": "132651", "name": "Marlon Lawson", "verified_terminal": True},
        {"code": "132652", "name": "Garry E. Lawson", "verified_terminal": True},
        {"code": "132653", "name": "Larry D. Lawson", "verified_terminal": True},
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
        {"code": "132671", "name": "Eva Kay Lawson", "born": "1 Oct 1947", "verified_terminal": True},
        {"code": "132672", "name": "Janet Lawson", "verified_terminal": True},
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
        {"code": "136541", "name": "Darwin Reckart", "verified_terminal": True},
        {"code": "136542", "name": "Delbert Reckart", "verified_terminal": True},
        {"code": "136543", "name": "Dailey Reckart", "verified_terminal": True},
        {"code": "136544", "name": "Donald Reckart", "verified_terminal": True},
        {"code": "136545", "name": "Herbert Reckart", "verified_terminal": True},
        {"code": "136546", "name": "Harland Reckart", "verified_terminal": True},
        {"code": "136547", "name": "Floyd Reckart", "verified_terminal": True},
        {"code": "136548", "name": "Wayne Reckart", "verified_terminal": True},
        {"code": "136549", "name": "Playford Reckart", "verified_terminal": True},
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
        {"code": "136611", "name": "Daughter", "verified_terminal": True},
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
        {"code": "138231", "name": "Maxine Bucklew", "verified_terminal": True},
        {"code": "138232", "name": "Ruby Bucklew", "verified_terminal": True},
        {"code": "138233", "name": "Eugene Bucklew", "verified_terminal": True},
        {"code": "138234", "name": "Child", "verified_terminal": True},
        {"code": "138235", "name": "Edna Bucklew", "verified_terminal": True},
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
        {"code": "138261", "name": "Junior Cole", "verified_terminal": True},
        {"code": "138262", "name": "Mary Jean Cole", "verified_terminal": True},
        {"code": "138263", "name": "Shirley Cole", "verified_terminal": True},
        {"code": "138264", "name": "Patty Cole", "verified_terminal": True},
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
        {"code": "138271", "name": "Virginia Ellen Teets", "born": "23 Jan 1940", "died": "26 Jan 1940", "flags": {"diedInInfancy": True}, "verified_terminal": True},
        {"code": "138272", "name": "Stanley Teets", "born": "29 Aug 1943", "died": "27 Mar 1944", "flags": {"diedInInfancy": True}, "verified_terminal": True},
        {"code": "138273", "name": "Johnny Teets", "born": "Sep 1944", "verified_terminal": True},
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
        {"code": "138421", "name": "Michael Teets", "verified_terminal": True},
        {"code": "138422", "name": "Ray Teets", "verified_terminal": True},
        {"code": "138423", "name": "Timothy Teets", "verified_terminal": True},
        {"code": "138424", "name": "Linda Teets", "verified_terminal": True},
        {"code": "138425", "name": "Janice Teets", "verified_terminal": True},
        {"code": "138426", "name": "Ada Teets", "verified_terminal": True},
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
        {"code": "138441", "name": "Howard (Buss) Johnson", "verified_terminal": True},
        {"code": "138442", "name": "Everett (Chum) Johnson", "verified_terminal": True},
        {"code": "138443", "name": "Don Johnson", "verified_terminal": True},
        {"code": "138444", "name": "Burley Johnson", "verified_terminal": True},
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
        {"code": "138621", "name": "Donald DeWitt", "verified_terminal": True},
        {"code": "138622", "name": "Otis DeWitt", "verified_terminal": True},
        {"code": "138623", "name": "Marie DeWitt", "verified_terminal": True},
        {"code": "138624", "name": "Dolly DeWitt", "verified_terminal": True},
        {"code": "138625", "name": "Betty DeWitt", "verified_terminal": True},
        {"code": "138626", "name": "Norma DeWitt", "verified_terminal": True},
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
        {"code": "138631", "name": "Fred Uphold", "verified_terminal": True},
        {"code": "138632", "name": "Bud Casteel", "verified_terminal": True},
        {"code": "138633", "name": "Chum Casteel", "verified_terminal": True},
        {"code": "138634", "name": "Junior Casteel", "verified_terminal": True},
        {"code": "138635", "name": "Ger Casteel", "verified_terminal": True},
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
        {"code": "138651", "name": "Ruth Rodeheaver", "verified_terminal": True},
        {"code": "138652", "name": "Ramon Richard Rodeheaver", "verified_terminal": True},
        {"code": "138653", "name": "Willie Wilson", "verified_terminal": True},
        {"code": "138654", "name": "Joe Wilson", "verified_terminal": True},
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
        {"code": "138661", "name": "Helen Thomas", "verified_terminal": True},
        {"code": "138662", "name": "Lucilla Thomas", "verified_terminal": True},
        {"code": "138663", "name": "Paul Thomas", "verified_terminal": True},
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
        {"code": "13B216", "name": "Edward Michael Seamon", "born": "13 Jul 1938", "died": "1958", "verified_terminal": True},
        {"code": "13B217", "name": "Larry Donald Seamon", "born": "31 Jul 1945", "verified_terminal": True},
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
        {"code": "13C531", "name": "Bradley Bishoff", "verified_terminal": True},
        {"code": "13C532", "name": "Katherine Bishoff", "verified_terminal": True},
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
        {"code": "13F121", "name": "Ray Guthrie", "verified_terminal": True},
        {"code": "13F122", "name": "Linda Guthrie", "verified_terminal": True},
        {"code": "13F123", "name": "Marine Guthrie", "flags": {"stepChild": True}, "verified_terminal": True},
        {"code": "13F124", "name": "Marvin Durst", "flags": {"stepChild": True}, "verified_terminal": True},
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
        {"code": "13F714", "name": "Tammy Thomas", "born": "28 Mar 1963", "verified_terminal": True},
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
        {"code": "13F723", "name": "James Melvin Cupp", "born": "13 Oct 1957", "verified_terminal": True},
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
        {"code": "13F731", "name": "Mary Jane Guthrie", "born": "19 Jun 1966", "verified_terminal": True},
        {"code": "13F732", "name": "Walter Ray Guthrie, Jr.", "born": "13 Jun 1968", "verified_terminal": True},
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
        {"code": "13F743", "name": "Howard Dale Thomas", "born": "2 Jul 1966", "verified_terminal": True},
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
        {"code": "13F751", "name": "Patricia Ann Rosier", "born": "16 Apr 1959", "verified_terminal": True},
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
        {"code": "13F761", "name": "Lee Burdette Pratt", "born": "20 Jun 1962", "verified_terminal": True},
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
        {"code": "13F771", "name": "Judith Ann Hoffman", "born": "9 Jan 1964", "verified_terminal": True},
        {"code": "13F772", "name": "Roger Lynn Hoffman II", "born": "28 May 1967", "verified_terminal": True},
        {"code": "13F773", "name": "Rebecca Jean Hoffman", "born": "20 Oct 1973", "verified_terminal": True},
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
        {"code": "13F811", "name": "Fred Lawless", "born": "20 Dec 1964", "verified_terminal": True},
        {"code": "13F812", "name": "Vince Lawless", "born": "10 Mar 1966", "verified_terminal": True},
        {"code": "13F813", "name": "Kathy Michelle Lawless", "born": "13 Aug 1967", "died": "31 Aug 1967", "flags": {"diedInInfancy": True}, "verified_terminal": True},
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
        {"code": "13F821", "name": "Michael Guthrie", "verified_terminal": True},
        {"code": "13F822", "name": "Andrew Guthrie", "verified_terminal": True},
        {"code": "13F823", "name": "Lesley Ann Guthrie", "born": "1 Apr 1974", "verified_terminal": True},
        {"code": "13F824", "name": "Ezra Grant Guthrie, Jr.", "born": "7 Aug 1975", "died": "3 Nov 1975", "flags": {"diedInInfancy": True}, "verified_terminal": True},
        {"code": "13F825", "name": "Janice Lynn Guthrie", "born": "30 Jan 1977", "verified_terminal": True},
        {"code": "13F826", "name": "Elizabeth Ann Guthrie", "born": "11 Sep 1982", "verified_terminal": True},
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
        {"code": "13F831", "name": "Mary Sparenberg", "verified_terminal": True},
        {"code": "13F832", "name": "Joseph Sparenberg", "verified_terminal": True},
        {"code": "13F833", "name": "Faye Sparenberg", "verified_terminal": True},
        {"code": "13F834", "name": "Rita Sparenberg", "verified_terminal": True},
        {"code": "13F835", "name": "George Sparenberg", "verified_terminal": True},
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
        {"code": "13F841", "name": "Walter John Guthrie", "born": "Sep 1988", "verified_terminal": True},
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
        {"code": "13F851", "name": "Darlene Taylor", "verified_terminal": True},
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
        {"code": "13F871", "name": "Melissa", "verified_terminal": True},
        {"code": "13F872", "name": "Germainne", "verified_terminal": True},
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
        {"code": "13F891", "name": "Robert Lee Ault", "born": "23 Aug 1976", "verified_terminal": True},
        {"code": "13F892", "name": "Walter Harry Henning", "born": "12 May 1982", "verified_terminal": True},
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
        {"code": "13F8A1", "name": "Anna Marie Poling", "born": "12 Nov 1980", "verified_terminal": True},
        {"code": "13F8A2", "name": "Jason Allen Poling", "born": "23 Mar 1982", "verified_terminal": True},
        {"code": "13F8A3", "name": "Toyna Renue Poling", "born": "9 Feb 1984", "verified_terminal": True},
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
        {"code": "13FB11", "name": "Sandy Rosenberger", "verified_terminal": True},
        {"code": "13FB12", "name": "Jennie Rosenberger", "verified_terminal": True},
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
        {"code": "13FE11", "name": "Kenneth Richard Noss", "born": "14 Jan 1959", "verified_terminal": True},
        {"code": "13FE12", "name": "David Alan Noss", "born": "5 Sep 1962", "verified_terminal": True},
        {"code": "13FE13", "name": "Joy Ann Noss", "born": "16 Sep 1963", "verified_terminal": True},
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
        {"code": "13FE21", "name": "Carolyn Sue Ringer", "born": "14 Feb 1954", "verified_terminal": True},
        {"code": "13FE22", "name": "Linda Diana Ringer", "born": "5 Feb 1957", "verified_terminal": True},
        {"code": "13FE23", "name": "Sandra Kay Ringer", "born": "19 Mar 1965", "died": "17 Nov 1968", "flags": {"diedInInfancy": True}, "verified_terminal": True},
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
        {"code": "13FE31", "name": "Stephen Kent Noss", "born": "13 Aug 1970", "verified_terminal": True},
        {"code": "13FE32", "name": "Aaron Neal Noss", "born": "26 Feb 1974", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "13FE4",
    "name": "Wayne E. Noss",
    "sex": "M",
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 51},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "13FE41", "name": "Daughter", "born": "23 Jul 1963", "verified_terminal": True},
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
        {"code": "13FE61", "name": "Harry Wayne (Chipper) Evans", "verified_terminal": True},
        {"code": "13FE62", "name": "Debbie Evans", "verified_terminal": True},
        {"code": "13FE63", "name": "Randy Evans", "verified_terminal": True},
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
        {"code": "141512", "name": "Thomas J. Anderson", "born": "25 Apr 1936", "verified_terminal": True},
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
        {"code": "141521", "name": "Deborah Lee Caldwell", "born": "24 Dec 1947", "verified_terminal": True},
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
        {"code": "141532", "name": "Donetta Faye Uphold", "born": "16 Dec 1943", "verified_terminal": True},
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
        {"code": "141542", "name": "Cholly Rae Jones", "born": "18 Feb 1946", "verified_terminal": True},
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
        {"code": "141551", "name": "Connie Rae Uphold", "born": "26 Jun 1951", "verified_terminal": True},
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
        {"code": "141611", "name": "Marvin Ray Bankhead", "born": "8 Jul 1940", "verified_terminal": True},
        {"code": "141612", "name": "Lawson Lee Bankhead", "born": "16 Jul 1941", "verified_terminal": True},
        {"code": "141613", "name": "Shirley Leona Bankhead", "born": "19 Oct 1942", "verified_terminal": True},
        {"code": "141614", "name": "Geraldine Patrica Bankhead", "born": "9 May 1944", "verified_terminal": True},
        {"code": "141615", "name": "Galend Manuel Bankhead", "born": "21 Sep 1948", "verified_terminal": True},
        {"code": "141616", "name": "Melvin Jerold Bankhead", "born": "10 Apr 1950", "verified_terminal": True},
        {"code": "141617", "name": "Stanley Ray Bankhead", "born": "3 Jan 1952", "verified_terminal": True},
        {"code": "141618", "name": "David Blaine Bankhead", "born": "18 Mar 1953", "verified_terminal": True},
        {"code": "141619", "name": "Edna Diane Bankhead", "born": "19 Sep 1955", "verified_terminal": True},
        {"code": "14161A", "name": "Ruby Elain Bankhead", "born": "16 Oct 1956", "died": "16 Oct 1956", "flags": {"diedInInfancy": True}, "verified_terminal": True},
        {"code": "14161B", "name": "David Anthony Bankhead", "born": "23 Feb 1959", "died": "23 Feb 1959", "flags": {"diedInInfancy": True}, "verified_terminal": True},
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
        {"code": "141811", "name": "Velma Elaine Moats", "born": "8 Jun 1929", "verified_terminal": True},
        {"code": "141812", "name": "Daisy Geraldene Moats", "born": "3 Sep 1934", "verified_terminal": True},
        {"code": "141813", "name": "Shirley Mae Moats", "born": "3 Jul 1936", "verified_terminal": True},
        {"code": "141814", "name": "William Harold Moats", "born": "8 Oct 1939", "verified_terminal": True},
        {"code": "141815", "name": "Dortha Marlene Moats", "born": "18 Nov 1941", "verified_terminal": True},
        {"code": "141816", "name": "Beverly Charlene Moats", "born": "12 Sep", "verified_terminal": True},
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
        {"code": "141831", "name": "Vernon William Hileman", "born": "21 Feb 1938", "verified_terminal": True},
        {"code": "141832", "name": "Wendell Philip Hileman", "born": "18 Oct 1945", "verified_terminal": True},
        {"code": "141833", "name": "Carolyn June Hileman", "born": "11 Jun 1947", "verified_terminal": True},
        {"code": "141834", "name": "Linda Lou Hileman", "born": "7 Mar 1954", "verified_terminal": True},
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
        {"code": "141861", "name": "Kenneth Mitchell Turner", "born": "1 Apr 1949", "verified_terminal": True},
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
        {"code": "142521", "name": "Mary Maxine Nicola", "born": "3 Aug 1930", "died": "2 Mar 1931", "flags": {"diedInInfancy": True}, "verified_terminal": True},
        {"code": "142522", "name": "Martha Marie Nicola", "born": "3 Aug 1930", "died": "3 Aug 1930", "flags": {"diedInInfancy": True}, "verified_terminal": True},
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
        {"code": "142811", "name": "James Franklin Sines, Jr.", "verified_terminal": True},
        {"code": "142812", "name": "Barbara Sines", "verified_terminal": True},
        {"code": "142813", "name": "John Sines", "verified_terminal": True},
        {"code": "142814", "name": "Delbert Sines", "verified_terminal": True},
        {"code": "142815", "name": "Donald Sines", "verified_terminal": True},
        {"code": "142816", "name": "Carol Sue Sines", "verified_terminal": True},
        {"code": "142817", "name": "Linda Sines", "verified_terminal": True},
        {"code": "142818", "name": "Pat Sines", "verified_terminal": True},
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
        {"code": "142822", "name": "Wendy Gay Sines", "born": "13 Feb 1963", "verified_terminal": True},
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
        {"code": "142841", "name": "Sandy Sines", "verified_terminal": True},
        {"code": "142842", "name": "Mary Ann Sines", "verified_terminal": True},
        {"code": "142843", "name": "Robert Sines", "verified_terminal": True},
        {"code": "142844", "name": "James Sines", "verified_terminal": True},
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
        {"code": "142871", "name": "Eugene Sines", "verified_terminal": True},
        {"code": "142872", "name": "Died at birth", "flags": {"diedInInfancy": True}, "verified_terminal": True},
        {"code": "142873", "name": "Kevin Sines", "verified_terminal": True},
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
        {"code": "142881", "name": "Lisa Sines", "born": "1 Dec 1963", "verified_terminal": True},
        {"code": "142882", "name": "Tomothy Ray Sines", "born": "12 May 1965", "died": "1 Nov 1987", "verified_terminal": True},
        {"code": "142883", "name": "Jeannette Sines", "born": "25 Jan 1968"},
        {"code": "142884", "name": "Tiffany Sines", "born": "5 Jun 1975", "verified_terminal": True},
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
        {"code": "142921", "name": "James Guthrie", "verified_terminal": True},
        {"code": "142922", "name": "Clyde Guthrie, Jr.", "born": "Sep 1941", "died": "17 Dec 1941", "flags": {"diedInInfancy": True}, "verified_terminal": True},
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
        {"code": "142931", "name": "Robert Savage", "born": "16 Jul 1936", "verified_terminal": True},
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
        {"code": "142941", "name": "Mary Guthrie", "born": "21 Oct 1941", "verified_terminal": True},
        {"code": "142942", "name": "Paul Guthrie", "born": "10 Feb 1943", "verified_terminal": True},
        {"code": "142943", "name": "Bill Guthrie", "born": "1 May 1946", "verified_terminal": True},
        {"code": "142944", "name": "Jean Guthrie", "born": "6 Sep 1947", "verified_terminal": True},
        {"code": "142945", "name": "Joan Guthrie", "born": "11 Aug 1949", "verified_terminal": True},
        {"code": "142946", "name": "Harry Guthrie", "born": "18 Mar 1951", "verified_terminal": True},
        {"code": "142947", "name": "Larry Guthrie", "born": "18 Mar 1951", "verified_terminal": True},
        {"code": "142948", "name": "Robert Guthrie", "born": "16 Apr 1952", "verified_terminal": True},
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
        {"code": "142981", "name": "Earl Guthrie, III", "born": "22 Mar 1952", "verified_terminal": True},
        {"code": "142982", "name": "Carl Guthrie", "born": "6 Apr 1953", "verified_terminal": True},
        {"code": "142983", "name": "Sharon Guthrie", "born": "12 Jun 1955", "verified_terminal": True},
        {"code": "142984", "name": "Gerald Guthrie", "born": "21 Feb 1959", "verified_terminal": True},
        {"code": "142985", "name": "Roger Guthrie", "born": "3 Dec 1962", "verified_terminal": True},
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
        {"code": "142991", "name": "Deborah Mae Eutsey", "born": "12 Nov 1952", "verified_terminal": True},
        {"code": "142992", "name": "Shirley Ann Eutsey", "born": "5 Dec 1954", "verified_terminal": True},
        {"code": "142993", "name": "Dale Eugene Eutsey", "born": "26 Aug 1957", "verified_terminal": True},
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
        {"code": "1429C1", "name": "Paul Franklin Hartman", "born": "26 Oct 1958", "verified_terminal": True},
        {"code": "1429C2", "name": "Phyliss Jean Hartman", "born": "31 May 1963", "verified_terminal": True},
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
        {"code": "143291", "name": "Donald Myers", "born": "7 May 1947", "verified_terminal": True},
        {"code": "143292", "name": "Larry Myers", "born": "4 Feb 1951", "verified_terminal": True},
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
        {"code": "143411", "name": "Mary Collins", "verified_terminal": True},
        {"code": "143412", "name": "Raymond Collins"},
        {"code": "143413", "name": "Carl Collins"},
        {"code": "143414", "name": "William (Billy) Lee Collins", "verified_terminal": True},
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
        {"code": "143421", "name": "Glenn D. Cuppett", "verified_terminal": True},
        {"code": "143422", "name": "Paul J. Nicola", "verified_terminal": True},
        {"code": "143423", "name": "Elizabeth Mae Nicola", "born": "5 Jul 1942", "died": "25 Sep 1942", "flags": {"diedInInfancy": True}, "verified_terminal": True},
        {"code": "143424", "name": "Carl R. Nicola", "born": "9 Sep 1946"},
        {"code": "143425", "name": "Robert Martin Nicola", "born": "26 Sep 1951", "verified_terminal": True},
        {"code": "143426", "name": "Betty K. Nicola", "born": "13 Sep 1953"},
        {"code": "143427", "name": "Jacob George Nicola, Jr.", "born": "27 May 1960"},
        {"code": "143428", "name": "Infant", "flags": {"diedInInfancy": True}, "verified_terminal": True},
        {"code": "143429", "name": "Infant", "flags": {"diedInInfancy": True}, "verified_terminal": True},
        {"code": "14342A", "name": "Charles E. Nicola", "verified_terminal": True},
        {"code": "14342B", "name": "Charlotte K. Nicola", "verified_terminal": True},
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
        {"code": "143511", "name": "Ester G. Sliger", "born": "6 Jul 1938", "verified_terminal": True},
        {"code": "143512", "name": "Richard F. Sliger", "born": "23 Sep 1939", "verified_terminal": True},
        {"code": "143513", "name": "Rofelma L. Sliger", "born": "12 Jan 1941", "verified_terminal": True},
        {"code": "143514", "name": "Frank A. Sliger", "born": "4 Sep 1942", "verified_terminal": True},
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
        {"code": "144111", "name": "Betty Sisler", "verified_terminal": True},
        {"code": "144112", "name": "Lois Jean Sisler"},
        {"code": "144113", "name": "Dale Arthur Sisler", "born": "1929"},
        {"code": "144114", "name": "William Sisler", "verified_terminal": True},
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
        {"code": "144133", "name": "Delbert Jack Sisler", "born": "1939", "verified_terminal": True},
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
        {"code": "144152", "name": "William Floyd Sisler", "born": "Jan 1937", "verified_terminal": True},
        {"code": "144153", "name": "Mary Ellen Sisler", "born": "22 Oct 1940"},
        {"code": "144154", "name": "Jane Elaine Sisler", "born": "23 Jan 1944"},
        {"code": "144155", "name": "Wilma Marie Sisler", "born": "17 Feb 1946"},
        {"code": "144156", "name": "Shirley Ann Sisler", "born": "6 Jan 1949", "verified_terminal": True},
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
        {"code": "144162", "name": "John Lee Sisler", "verified_terminal": True},
        {"code": "144163", "name": "Nancy Sisler", "verified_terminal": True},
        {"code": "144164", "name": "George Ray Sisler, Jr.", "verified_terminal": True},
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
        {"code": "144521", "name": "Janet Friend", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "14453",
    "name": "Pearl Lovine Friend",
    "sex": "F",
    "born": "29 Nov 1916",
    "died": "11 Sep 1978",
    "spouses": [{"name": "Ivon Theadore Spiker", "born": "12 Dec 1910", "died": "17 Apr 1978", "married": "14 Sep 1935", "details": "Same as #17112."}],
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
        {"code": "144542", "name": "Charlotte Groves", "verified_terminal": True},
        {"code": "144543", "name": "Larry Groves", "verified_terminal": True},
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
        {"code": "144611", "name": "John Thomas", "verified_terminal": True},
        {"code": "144612", "name": "Tom Thomas", "verified_terminal": True},
        {"code": "144613", "name": "Jerry Thomas", "verified_terminal": True},
        {"code": "144614", "name": "Jackie Thomas", "verified_terminal": True},
        {"code": "144615", "name": "Kathy Thomas"},
        {"code": "144616", "name": "Fanny Thomas", "verified_terminal": True},
        {"code": "144617", "name": "Patti Thomas", "verified_terminal": True},
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
        {"code": "144631", "name": "Terry Max Strawser", "born": "14 Jul 1943", "verified_terminal": True},
        {"code": "144632", "name": "Linda Kay Strawser", "born": "13 Feb 1951", "verified_terminal": True},
        {"code": "144633", "name": "Thomas Michael Strawser", "born": "7 Dec 1953", "verified_terminal": True},
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
        {"code": "144751", "name": "Jane Elizabeth Thomas", "born": "6 May 1963", "verified_terminal": True},
        {"code": "144752", "name": "Tina Barbarella Thomas", "born": "11 Jul 1970", "verified_terminal": True},
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
        {"code": "144764", "name": "Christine Marie Thomas", "born": "2 Feb 1971", "verified_terminal": True},
        {"code": "144765", "name": "Rebecca Joanne Thomas", "born": "6 Dec 1972", "verified_terminal": True},
        {"code": "144766", "name": "Jamie Scott Thomas", "born": "23 Sep 1975", "verified_terminal": True},
        {"code": "144767", "name": "Matthew John Thomas", "born": "10 Aug 1977", "verified_terminal": True},
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
        {"code": "144811", "name": "Rev. Donald H. Reckart", "verified_terminal": True},
        {"code": "144812", "name": "Kenneth W. Reckart", "verified_terminal": True},
        {"code": "144813", "name": "Rev. Charles L. Reckart", "verified_terminal": True},
        {"code": "144814", "name": "Rev. Gary P. Reckart", "verified_terminal": True},
        {"code": "144815", "name": "Rev. Ray E. Reckart", "verified_terminal": True},
        {"code": "144816", "name": "Regina Reckart", "verified_terminal": True},
        {"code": "144817", "name": "Charlotte D. Reckart", "verified_terminal": True},
        {"code": "144818", "name": "Doris A. Reckart", "verified_terminal": True},
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
        {"code": "144851", "name": "Melanie Strawser", "born": "3 Feb 1961", "verified_terminal": True},
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
        {"code": "145111", "name": "Malon A. Harvey", "born": "3 May 1929", "verified_terminal": True},
        {"code": "145112", "name": "Myron A. Harvey", "born": "13 Mar 1934", "verified_terminal": True},
        {"code": "145113", "name": "Sheila D. Harvey", "born": "6 Oct 1943", "verified_terminal": True},
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
        {"code": "145411", "name": "Carol Lee Blosser", "born": "11 Oct 1934", "verified_terminal": True},
        {"code": "145412", "name": "John W. Blosser", "born": "1 Dec 1935", "verified_terminal": True},
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
        {"code": "145431", "name": "Beverly Lee McDaniel", "born": "11 Jan 1942", "verified_terminal": True},
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
        {"code": "145441", "name": "Judith Darlene Blosser", "born": "16 Jul 1943", "verified_terminal": True},
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
        {"code": "145811", "name": "Jeremiah W. Guthrie", "born": "8 Jan 1942", "verified_terminal": True},
        {"code": "145812", "name": "Infant", "born": "8 Oct 1943", "died": "1943", "flags": {"diedInInfancy": True}, "verified_terminal": True},
        {"code": "145813", "name": "Jean Marie Guthrie", "born": "4 May 1945", "verified_terminal": True},
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
        {"code": "146131", "name": "Eric Dodid", "born": "Aug 1945", "verified_terminal": True},
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
        {"code": "146141", "name": "Charles A. Wolf", "verified_terminal": True},
        {"code": "146142", "name": "Infant Son", "verified_terminal": True},
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
        {"code": "147141", "name": "Marcella Kahl", "verified_terminal": True},
        {"code": "147142", "name": "Dixie Lee Kahl", "verified_terminal": True},
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
        {"code": "147171", "name": "Judy Deal", "verified_terminal": True},
        {"code": "147172", "name": "Roger A. Deal", "verified_terminal": True},
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
        {"code": "147182", "name": "Edward Wallace Kahl", "born": "29 Dec 1943", "died": "26 Jan 1944", "flags": {"diedInInfancy": True}, "verified_terminal": True},
        {"code": "147183", "name": "Shirley Jean Kahl", "born": "20 Jul 1945"},
        {"code": "147184", "name": "Roy Douglas Kahl", "born": "8 Sep 1949", "verified_terminal": True},
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
        {"code": "147191", "name": "Walter Kahl", "verified_terminal": True},
        {"code": "147192", "name": "Eric Kahl", "verified_terminal": True},
        {"code": "147193", "name": "David Kahl", "verified_terminal": True},
        {"code": "147194", "name": "Everett Wade Kahl", "born": "4 Dec 1953", "died": "1 Nov 1972", "verified_terminal": True},
        {"code": "147195", "name": "Linda Kahl", "verified_terminal": True},
        {"code": "147196", "name": "Wanda Kahl", "verified_terminal": True},
        {"code": "147197", "name": "Mary Kahl", "verified_terminal": True},
        {"code": "147198", "name": "Ella Kahl", "verified_terminal": True},
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
        {"code": "147311", "name": "Albert Miller", "born": "10 Mar 1934", "died": "1934", "flags": {"diedInInfancy": True}, "verified_terminal": True},
        {"code": "147312", "name": "Russell E. Miller", "born": "28 Feb 1935", "verified_terminal": True},
        {"code": "147313", "name": "Deloris Jane Miller", "born": "11 Apr 1936", "verified_terminal": True},
        {"code": "147314", "name": "William Howard Miller", "born": "16 Apr 1938", "verified_terminal": True},
        {"code": "147315", "name": "Helen Jean Miller", "born": "12 Jun 1939", "died": "12 Jun 1939", "flags": {"diedInInfancy": True}, "verified_terminal": True},
        {"code": "147316", "name": "Douglas Paul Miller", "born": "2 Feb 1942", "verified_terminal": True},
        {"code": "147317", "name": "Caroline Miller", "born": "18 Oct 1943", "died": "18 Oct 1943", "flags": {"diedInInfancy": True}, "verified_terminal": True},
    ],
})


# === Pages 61-65 vision pass (2026-06-07): Appleby/Guthrie/McKenzie/Brandgard/Cuppett/Moyers/Nicola ===
ENTRIES.append({
    "code": "14751",
    "name": "Thomas Edward Appleby",
    "sex": "M",
    "born": "27 Sep 1911",
    "spouses": [
        {"name": "Cordelia Dennis", "born": "17 Dec 1912", "died": "8 Dec 1948", "married": "4 Jun 1932", "order": 1},
        {"name": "Joyce Bradley", "born": "10 Nov 1933", "married": "3 Feb 1950", "order": 2},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 61},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "147511", "name": "Harold Ashton Appleby", "born": "1 May 1934"},
        {"code": "147512", "name": "Richard Harland Appleby", "born": "21 May 1936"},
        {"code": "147513", "name": "Sandra Faye Appleby", "born": "24 Sep 1937"},
        {"code": "147514", "name": "Nancy Lee Appleby", "born": "1 Oct 1938"},
        {"code": "147515", "name": "Carol Ann Appleby", "born": "28 Jun 1944"},
        {"code": "147516", "name": "Thomas Edward Appleby", "born": "7 Feb 1951"},
        {"code": "147517", "name": "James William Appleby", "born": "8 Jun 1953"},
        {"code": "147518", "name": "Mark Bradley Appleby", "born": "28 Apr 1958"},
        {"code": "147519", "name": "John Henry Appleby", "born": "18 Sep 1961", "died": "14 Apr 1963", "flags": {"diedInInfancy": True}, "verified_terminal": True},
        {"code": "14751A", "name": "Darlene Lynn Appleby", "born": "24 Mar 1966", "died": "22 Sep 1967", "flags": {"diedInInfancy": True}, "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "14752",
    "name": "Margaret Irene Susan Appleby",
    "sex": "F",
    "born": "29 Sep 1914",
    "died": "22 Apr 1944",
    "spouses": [{"name": "Omer R. Cummingham"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 61},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "147521", "name": "Sharon A. Cummingham", "born": "4 Jun 1935"},
        {"code": "147522", "name": "Omer R. Cummingham", "born": "18 Jan 1941", "died": "21 Dec 1964", "verified_terminal": True},
        {"code": "147523", "name": "Darwin D. Cummingham", "born": "4 Dec 1942", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "14753",
    "name": "Ida Mae Appleby",
    "sex": "F",
    "born": "16 Oct 1926",
    "spouses": [{"name": "Carl Fisher", "born": "23 Apr 1925", "died": "18 Apr 1982", "married": "29 Jan 1945"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 61},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "147531", "name": "Robert Carl Fisher", "born": "7 Jul 1946"},
        {"code": "147532", "name": "Vanessa Gayle Fisher", "born": "14 Nov 1953"},
    ],
})

ENTRIES.append({
    "code": "14761",
    "name": "Thelma Edith Guthrie",
    "sex": "F",
    "born": "19 Jan 1921",
    "spouses": [{"name": "Archie Buchanon", "married": "24 Jan 1954"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 61},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "147611", "name": "Betty Jean Buchanon", "born": "23 Mar 1944", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "14762",
    "name": "Helen O. Guthrie",
    "sex": "F",
    "born": "30 Nov 1924",
    "spouses": [{"name": "John T. Brady", "born": "12 Feb 1920", "married": "14 Feb 1946"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 61},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "147621", "name": "Larry Brady", "born": "22 Sep 1946", "died": "27 Nov 1951", "flags": {"diedInInfancy": True}, "verified_terminal": True},
        {"code": "147622", "name": "Roger Lee Brady", "born": "22 Nov 1951", "verified_terminal": True},
        {"code": "147623", "name": "Carol Ann Brady", "born": "7 Feb 1958", "verified_terminal": True},
        {"code": "147624", "name": "David Mark Brady", "born": "6 Apr 1961", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "14763",
    "name": "Margaret Irene Guthrie",
    "sex": "F",
    "born": "24 Oct 1931",
    "spouses": [{"name": "Raymond Dice", "born": "20 Mar 1929", "married": "31 Jan 1949"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 61},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "147631", "name": "Harold Ray Dice", "born": "16 Sep 1949", "verified_terminal": True},
        {"code": "147632", "name": "Rebecca Anna Dice", "born": "28 Aug 1954", "verified_terminal": True},
        {"code": "147633", "name": "Barbara Lynn Dice", "born": "9 Apr 1958", "verified_terminal": True},
        {"code": "147634", "name": "Darlene Marie Dice", "born": "20 Aug 1959", "died": "Sep 1959", "flags": {"diedInInfancy": True}, "verified_terminal": True},
        {"code": "147635", "name": "Robert John Dice", "born": "18 Nov 1961", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "14811",
    "name": "Myrtle P. McKenzie",
    "sex": "F",
    "born": "13 Jan 1920",
    "spouses": [{"name": "Kenneth Kelly", "born": "9 Sep 1916", "married": "3 Jan 1940"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 61},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "148111", "name": "Beverly F. Kelly", "born": "20 Mar 1942", "verified_terminal": True},
        {"code": "148112", "name": "Kenneth D. Kelly", "born": "10 May 1944", "verified_terminal": True},
        {"code": "148113", "name": "Brenda G. Kelly", "born": "22 Nov 1945", "verified_terminal": True},
        {"code": "148114", "name": "Jerry L. Kelly", "born": "27 Aug 1947", "verified_terminal": True},
        {"code": "148115", "name": "Larry E. Kelly", "born": "18 May 1949", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "14812",
    "name": "Violet R. McKenzie",
    "sex": "F",
    "born": "19 Aug 1921",
    "spouses": [{"name": "Charles Bowlen", "born": "1913", "married": "8 Oct 1939"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 62},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "148121", "name": "Mary Ann Bowlen", "born": "22 Aug 1939", "verified_terminal": True},
        {"code": "148122", "name": "Charles Edward Bowlen", "born": "14 Sep 1941", "verified_terminal": True},
        {"code": "148123", "name": "Ray Lee Bowlen", "born": "9 Dec 1943", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "14813",
    "name": "Bessie Ellen McKenzie",
    "sex": "F",
    "born": "28 Oct 1923",
    "spouses": [{"name": "John Robert Bartha", "born": "1919", "married": "Feb 1946"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 62},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "148131", "name": "Nancy Diane Bartha", "born": "2 Aug 1942", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "14815",
    "name": "Alice B. McKenzie",
    "sex": "F",
    "born": "23 Apr 1926",
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 62},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "148151", "name": "James Ray McKenzie", "born": "4 Apr 1942", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "14821",
    "name": "Barbara Guthrie",
    "sex": "F",
    "born": "11 Dec 1917",
    "spouses": [{"name": "Orvil Collins", "married": "1940"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 62},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "148211", "name": "Betty Gene Collins", "born": "15 Feb 1952", "verified_terminal": True},
        {"code": "148212", "name": "Phillis Rae Guthrie", "born": "8 Jun 1952", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "14823",
    "name": "Virginia Guthrie",
    "sex": "F",
    "born": "17 Nov 1922",
    "spouses": [{"name": "John H. Kendal", "born": "1918", "married": "1937"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 62},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "148231", "name": "John H. Kendal, Jr.", "verified_terminal": True},
        {"code": "148232", "name": "Rhona Kendal", "verified_terminal": True},
        {"code": "148233", "name": "Allen Kendal", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "14842",
    "name": "Arrena Guthrie",
    "sex": "F",
    "spouses": [{"name": "Charles Kelly"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 62},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "148421", "name": "Mark Kelly", "verified_terminal": True},
        {"code": "148422", "name": "Jo Lynn Kelly", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "14861",
    "name": "Irene Kendall",
    "sex": "F",
    "born": "25 Jan 1924",
    "spouses": [{"name": "Frank Harbarger", "born": "12 Mar 1925", "married": "16 Jul 1944"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 62},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "148611", "name": "Virginia Ann Harbarger", "born": "5 Dec 1947", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "14871",
    "name": "Elsie Elizabeth Guthrie",
    "sex": "F",
    "born": "17 Jul 1926",
    "spouses": [{"name": "John Henry Riggins", "born": "26 Jul 1922", "married": "1943"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 62},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "148711", "name": "Catherine May Riggins", "born": "29 Jul 1944", "verified_terminal": True},
        {"code": "148712", "name": "John Henry Riggins, Jr.", "born": "12 Aug 1946", "verified_terminal": True},
        {"code": "148713", "name": "Cyntha Lou Riggins", "born": "1 Jun 1952", "died": "8 Jul 1952", "flags": {"diedInInfancy": True}, "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "14881",
    "name": "Edward F. Brandgard",
    "sex": "M",
    "born": "25 Dec 1923",
    "spouses": [{"name": "Nellie Moore", "born": "26 Feb 1928", "married": "1942"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 62},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "148811", "name": "Peter E. Brandgard", "born": "16 Mar 1948", "verified_terminal": True},
        {"code": "148812", "name": "James Ray Brandgard", "born": "27 Jun 1955", "died": "16 May 1960", "flags": {"diedInInfancy": True}, "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "14882",
    "name": "Evelene J. Brandgard",
    "sex": "F",
    "born": "19 Jul 1927",
    "spouses": [{"name": "Charles E. Davis", "born": "1922", "married": "1943"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 62},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "148821", "name": "Marie E. Davis", "born": "3 Oct 1946", "verified_terminal": True},
        {"code": "148822", "name": "Charles E. Davis", "born": "1 Mar 1948", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "14884",
    "name": "Pearl L. Brandgard",
    "sex": "F",
    "born": "5 May 1934",
    "spouses": [{"name": "Albert Hibbard", "married": "20 May 1952"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 62},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "148841", "name": "Ralph Paul Hibbard", "born": "5 May 1957", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "14885",
    "name": "Peter Ray Brandgard, Jr.",
    "sex": "M",
    "born": "5 Jan 1936",
    "spouses": [{"name": "Mary Catherine", "born": "14 May 1935", "married": "5 Jan 1955"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 63},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "148851", "name": "Sarah Catherine Brandgard", "born": "6 Jun 1955", "verified_terminal": True},
        {"code": "148852", "name": "Marie Louise Brandgard", "born": "15 Jun 1958", "verified_terminal": True},
        {"code": "148853", "name": "Franklin Ray Brandgard", "born": "15 Jun 1958", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "14892",
    "name": "Ester Leona Tate",
    "sex": "F",
    "born": "8 May 1933",
    "spouses": [{"name": "Charles Metheny"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 63},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "148921", "name": "Joyce Ann Metheny", "born": "17 Sep 1958", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "16111",
    "name": "Reardon Stewart Colton Cuppett",
    "sex": "M",
    "born": "29 Jan 1908",
    "died": "28 Mar 1950",
    "spouses": [{"name": "Ann Theresa Whipple", "born": "4 Oct 1908", "married": "14 Aug 1935"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 63},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "161111", "name": "Elizabeth Ann Cuppett", "born": "17 Sep 1937"},
        {"code": "161112", "name": "Reardon Stewart Colton Cuppett, Jr.", "born": "11 Jun 1939"},
        {"code": "161113", "name": "Vida Marie Cuppett", "born": "18 Apr 1943"},
        {"code": "161114", "name": "Susan Lee Cuppett", "born": "7 Nov 1945", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "16112",
    "name": "David Earl Cuppett, Jr.",
    "sex": "M",
    "born": "27 Feb 1913",
    "died": "1 May 1937",
    "spouses": [{"name": "Ruth Grant Wolverton", "born": "21 Apr 1915"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 63},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "161121", "name": "Ruth Grant Cuppett", "born": "22 Jun 1938"},
        {"code": "161122", "name": "David Earl Cuppett, III", "born": "26 Mar 1946"},
    ],
})

ENTRIES.append({
    "code": "16113",
    "name": "Mary Elizabeth Cuppett",
    "sex": "F",
    "born": "19 Jun 1921",
    "died": "1 Jan 1971",
    "spouses": [{"name": "Thomas Bryan Bickel, Jr.", "born": "24 May 1920", "married": "1 Jul 1943"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 63},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "161131", "name": "Thomas Bryan Bickel, III", "born": "26 Mar 1945", "verified_terminal": True},
        {"code": "161132", "name": "Barbara Gene Bickel", "born": "1 Dec 1947"},
        {"code": "161133", "name": "Cynthia Jane Bickel", "born": "8 Nov 1952"},
    ],
})

ENTRIES.append({
    "code": "16121",
    "name": "Grant Irwin Burner",
    "sex": "M",
    "born": "13 Aug 1908",
    "died": "15 May 1985",
    "spouses": [
        {"name": "Mary Pauline Eberhart", "born": "30 Mar 1916", "died": "2 Aug 1964", "married": "22 Aug 1935", "order": 1},
        {"name": "Leatrice Lessner Katz", "born": "14 Jun 1927", "married": "26 Dec 1970", "order": 2},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 63},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "161211", "name": "Ronald Irwin Bruner", "born": "1 Oct 1939"},
        {"code": "161212", "name": "Beverly Lou Bruner", "born": "1 Oct 1941"},
        {"code": "161213", "name": "Ilene Katz", "flags": {"stepChild": True}, "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "16211",
    "name": "Rasely B. Moyers",
    "sex": "M",
    "born": "5 Apr 1914",
    "died": "25 Mar 1977",
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 63},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "162111", "name": "Rasley Moyers", "verified_terminal": True},
        {"code": "162112", "name": "Karen Moyers", "verified_terminal": True},
        {"code": "162113", "name": "Patty Moyers", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "16231",
    "name": "Helen Margaret Moyers",
    "sex": "F",
    "born": "3 May 1913",
    "died": "16 Apr 1970",
    "spouses": [{"name": "Robert Samuel Spear", "born": "3 Dec 1913", "died": "31 Mar 1980", "married": "4 Jul 1934"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 64},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "162311", "name": "Carl R. Spear"},
        {"code": "162312", "name": "Charlotte May Spear"},
    ],
})

ENTRIES.append({
    "code": "16232",
    "name": "Juanita Ida Moyers",
    "sex": "F",
    "born": "25 Nov 1917",
    "spouses": [
        {"name": "Sherrill D. McMillen", "born": "14 Dec 1908", "died": "23 Jul 1982", "married": "1942", "order": 1},
        {"name": "Ralph Edgar Miller", "born": "8 Jul 1915", "married": "1986", "order": 2},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 64},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "162321", "name": "Judith Anna McMillen", "born": "28 Dec 1946", "verified_terminal": True},
        {"code": "162322", "name": "Joyce Ella McMillen", "born": "22 Apr 1951", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "16233",
    "name": "Irene Fay Moyers",
    "sex": "F",
    "born": "17 Nov 1921",
    "spouses": [{"name": "Donald W. Hughes", "born": "10 Mar 1917", "died": "Jan 1979", "married": "1940"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 64},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "162331", "name": "Gary Lee Hughes", "born": "2 Jan 1942", "verified_terminal": True},
        {"code": "162332", "name": "Norman M. Hughes", "born": "10 Aug 1944", "verified_terminal": True},
        {"code": "162333", "name": "Donald David Hughes", "born": "30 Jul 1947", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "16234",
    "name": "Myron Harold Moyers",
    "sex": "M",
    "born": "9 Oct 1924",
    "died": "21 Mar 1992",
    "spouses": [{"name": "Nina Nell Smith"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 64},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "162341", "name": "Todd Moyers", "verified_terminal": True},
        {"code": "162342", "name": "Lee Moyers", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "16235",
    "name": "Hubert Benton Moyers",
    "sex": "M",
    "born": "5 Feb 1929",
    "spouses": [{"name": "Glenadine Friend", "married": "24 Dec 1949"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 64},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "162351", "name": "Arthur Benton Moyers", "verified_terminal": True},
        {"code": "162352", "name": "Perry Hubert Moyers", "born": "29 Mar 1959", "verified_terminal": True},
        {"code": "162353", "name": "Clarence Wade Moyers", "born": "3 Dec 1961", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "16237",
    "name": "Dwight Lorain Moyers",
    "sex": "M",
    "born": "4 Oct 1932",
    "spouses": [{"name": "Rosellan Gray"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 65},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "162371", "name": "Kim Larain Moyers", "born": "17 Mar 1951", "verified_terminal": True},
        {"code": "162372", "name": "Stewart Allen Moyers", "born": "28 Oct 1955"},
        {"code": "162373", "name": "Nila Grace Moyers", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "16241",
    "name": "Vernon Ray Wright",
    "sex": "M",
    "born": "15 Sep 1920",
    "died": "25 Oct 1989",
    "spouses": [{"name": "Beatrice Jane Ryan", "born": "10 May 1925", "married": "19 Jun 1945"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 65},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "162411", "name": "Shirley Irene Wright", "born": "14 Jan 1946", "died": "9 Jan 1960", "flags": {"diedInInfancy": True}, "verified_terminal": True},
        {"code": "162412", "name": "Paulette Marie Wright", "born": "23 Mar 1957"},
        {"code": "162413", "name": "Jefferie Ray Wright", "born": "27 Nov 1963"},
    ],
})

ENTRIES.append({
    "code": "16243",
    "name": "Gladys Marie Wright",
    "sex": "F",
    "born": "28 Aug 1927",
    "spouses": [{"name": "Charles Q. Hook", "born": "11 Mar 1925", "married": "1946"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 65},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "162431", "name": "Barbara Jean Hook", "born": "13 Nov 1946", "verified_terminal": True},
        {"code": "162432", "name": "David Lee Hook", "born": "28 Jun 1948", "verified_terminal": True},
        {"code": "162433", "name": "Patty Elaine Hook", "born": "13 Feb 1952", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "16311",
    "name": "Rosa Ethel Nicola",
    "sex": "F",
    "born": "27 Sep 1907",
    "died": "3 May 1973",
    "spouses": [
        {"name": "Truman Taggart", "born": "7 May 1902", "died": "7 Sep 1937", "married": "15 Aug 1925", "order": 1},
        {"name": "Harold Hutchinson", "born": "4 Jan 1905", "died": "3 Oct 1987", "married": "14 Feb 1948", "order": 2},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 65},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "163111", "name": "John Robert Taggert", "born": "25 Mar 1926", "died": "3 Nov 1962", "verified_terminal": True},
        {"code": "163112", "name": "Clara Rosalie Taggert", "born": "6 Aug 1927"},
    ],
})

ENTRIES.append({
    "code": "16314",
    "name": "Pauline Lavena Nicola",
    "sex": "F",
    "born": "1 Apr 1914",
    "died": "30 Jan 1980",
    "spouses": [
        {"name": "Ralph Glover", "born": "5 Nov 1913", "married": "8 Feb 1930", "order": 1},
        {"name": "James Robert Collins", "born": "1 Oct 1914", "died": "8 Apr 1988", "married": "11 Feb 1939", "order": 2},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 65},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "163141", "name": "Infant", "born": "1930", "died": "1930", "flags": {"diedInInfancy": True}, "verified_terminal": True},
        {"code": "163142", "name": "Loretta Mae Glover", "born": "25 Jul 1933"},
        {"code": "163143", "name": "Robert M. Collins", "born": "1940", "died": "1940", "flags": {"diedInInfancy": True}, "verified_terminal": True},
        {"code": "163144", "name": "Larry Robert Collins", "born": "3 Feb 1952"},
    ],
})

ENTRIES.append({
    "code": "16315",
    "name": "Marie Pearl Nicola",
    "sex": "F",
    "born": "9 Apr 1919",
    "died": "18 Nov 1994",
    "spouses": [{"name": "Harold Clayton Greathouse", "born": "3 Aug 1914", "died": "26 May 1978", "married": "27 Mar 1937"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 65},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "163151", "name": "Harold E. Greathouse", "born": "30 Oct 1937", "died": "22 Dec 1937", "flags": {"diedInInfancy": True}, "verified_terminal": True},
        {"code": "163152", "name": "Shirley Jean Greathouse", "born": "17 May 1939"},
    ],
})

ENTRIES.append({
    "code": "16316",
    "name": "Margaret Ellen Nicola",
    "sex": "F",
    "born": "1 Jun 1923",
    "died": "6 Jul 1989",
    "spouses": [{"name": "James Robert Moody", "born": "23 Mar 1914", "married": "11 Jan 1940"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 65},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "163161", "name": "Stanley Ray Moody", "born": "9 Jun 1940"},
    ],
})


# === Pages 66-70 vision pass (2026-06-07): 163-164 Harshbarger + 166 Hileman + 171/172 gen 6 ===
ENTRIES.append({
    "code": "16317",
    "name": "Thelma Virginia Nicola",
    "sex": "F",
    "born": "24 Oct 1925",
    "spouses": [
        {"name": "Kenneth Cramer", "order": 1, "details": "Divorced."},
        {"name": "James William Conway", "born": "15 Apr 1927", "married": "25 Nov 1953", "order": 2},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 66},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "163171", "name": "Betty Carol Cramer", "born": "31 Dec 1946"},
    ],
})

ENTRIES.append({
    "code": "16318",
    "name": "Judson (Nick) Junior Nicola",
    "sex": "M",
    "born": "27 Feb 1930",
    "spouses": [{"name": "Emma Lou Haggerty", "born": "4 Feb 1928", "died": "26 Dec 1993", "married": "25 Feb 1950"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 66},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "163181", "name": "Jackie Dale Nicola", "born": "9 Mar 1951"},
        {"code": "163182", "name": "Jamie Judson Nicola", "born": "26 Jun 1954"},
        {"code": "163183", "name": "Kimberly Rae Nicola", "born": "20 Sep 1964"},
    ],
})

ENTRIES.append({
    "code": "16411",
    "name": "Beulah Mae Harshbarger",
    "sex": "F",
    "born": "7 Apr 1929",
    "spouses": [{"name": "Theodore Joseph Narivanchik", "born": "17 Jul 1925", "died": "22 Nov 1990", "married": "6 Jun 1948"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 66},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "164111", "name": "Theodore Ralph Narivanchik", "born": "7 Sep 1949"},
        {"code": "164112", "name": "Paul Joseph Narivanchik", "born": "14 Sep 1954"},
        {"code": "164113", "name": "Linda Mae Narivanchik", "born": "2 Jan 1957"},
    ],
})

ENTRIES.append({
    "code": "16421",
    "name": "Anna Marie Harshbarger",
    "sex": "F",
    "born": "5 Jun 1935",
    "spouses": [
        {"name": "Virgil John Parnell, Jr.", "order": 1},
        {"name": "Thomas Lee Moyers", "married": "1971", "order": 2},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 66},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "164211", "name": "Virgil David Parnell", "born": "11 Oct 1958", "verified_terminal": True},
        {"code": "164212", "name": "Anna Marie (Suzie) Parnell", "born": "21 Dec 1964", "verified_terminal": True},
        {"code": "164213", "name": "Thomas Lee Moyers", "born": "20 Jul 1972", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "16422",
    "name": "Mary Ellen Harshbarger",
    "sex": "F",
    "born": "6 Feb 1937",
    "spouses": [
        {"name": "Paul Fike", "order": 1},
        {"name": "Robert W. Pike", "married": "26 Apr 1968", "order": 2},
        {"name": "Kenneth Franks", "married": "3 Jun 1981", "order": 3},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 66},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "164221", "name": "Cheryl Lynne Fike", "born": "25 Feb 1964", "flags": {"adopted": True}, "verified_terminal": True},
        {"code": "164222", "name": "Ruth Ellen Pike", "born": "5 Feb 1970"},
        {"code": "164223", "name": "Robert Walter (Wallie) Pike", "born": "24 Apr 1971", "verified_terminal": True},
        {"code": "164224", "name": "Jerrold Wayne Pike", "born": "25 Jan 1974", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "16423",
    "name": "Shirley Mae Harshbarger",
    "sex": "F",
    "born": "26 Oct 1942",
    "spouses": [{"name": "Robert C. Kisasonak", "born": "3 Oct 1940", "died": "2 Apr 1988", "married": "26 Nov 1966"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 66},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "164231", "name": "Deborah Louise Kisasonak", "born": "6 May 1969"},
        {"code": "164232", "name": "Mark Alan Kisasonak", "born": "11 Sep 1970", "verified_terminal": True},
        {"code": "164233", "name": "Matthew Todd Kisasonak", "born": "16 Oct 1971", "verified_terminal": True},
        {"code": "164234", "name": "Jerone (Jerry) Scott Kisasonak", "born": "12 Oct 1973", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "16431",
    "name": "Sylvia Ionea Harshbarger",
    "sex": "F",
    "born": "8 Nov 1946",
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 66},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "164311", "name": "Lida Rose Harshbarger", "born": "21 Apr 1969", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "16432",
    "name": "Lillie Sue Harshbarger",
    "sex": "F",
    "born": "7 Jul 1954",
    "spouses": [{"name": "Lawrence (Larry) Paul Marsh", "born": "11 Feb 1923", "died": "28 Jun 1983", "married": "24 Oct 1971"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 67},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "164321", "name": "Candy Jean Harshbarger", "born": "2 Jul 1970", "flags": {"adopted": True}, "verified_terminal": True},
        {"code": "164322", "name": "Glen Paul Marsh", "born": "16 Apr 1975", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "16441",
    "name": "Harrison (Teddy) Theodore Harshbarger",
    "sex": "M",
    "born": "15 May 1963",
    "spouses": [{"name": "Ellen Stiffler", "married": "Feb 1977"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 67},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "164411", "name": "Joshua James Harshbarger", "born": "28 Mar 1994", "verified_terminal": True},
        {"code": "164412", "name": "Taylor Nicole Harshbarger", "born": "23 Apr 1996", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "16451",
    "name": "Rosetta Grace Fresh",
    "sex": "F",
    "born": "5 Sep 1937",
    "spouses": [{"name": "Gerald (Jerry) R. Craig", "born": "11 Oct 1935", "married": "21 Nov 1964"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 67},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "164511", "name": "Carol Lynn Craig", "born": "17 Jul 1966", "verified_terminal": True},
        {"code": "164512", "name": "Nancy Jean Craig", "born": "1 Jan 1970", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "16452",
    "name": "Alvin Francis Fresh",
    "sex": "M",
    "born": "21 May 1939",
    "died": "26 Dec 1993",
    "spouses": [
        {"name": "Constant (Connie) Ruth Laurenl", "born": "5 Jan 1944", "died": "5 Mar 1975", "married": "Jun 1962", "order": 1},
        {"name": "Laurel Jean Alexander", "born": "12 Apr 1936", "married": "17 Mar 1977", "order": 2},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 67},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "164521", "name": "Daisy Mae Fresh", "born": "7 Feb 1963", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "16456",
    "name": "Betty Mae Fresh",
    "sex": "F",
    "born": "10 Mar 1955",
    "spouses": [{"name": "Kenneth Lee Sager", "born": "19 Jan 1948", "married": "20 Apr 1974", "details": "Same as #164C1."}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 67},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "164561", "name": "Jennifer Lynn Sager", "born": "14 Oct 1980", "verified_terminal": True},
        {"code": "164562", "name": "David Bryan Sager", "born": "3 Dec 1982", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "16471",
    "name": "Barbara Jean Harshbarger",
    "sex": "F",
    "born": "27 Mar 1936",
    "spouses": [{"name": "Herbert Ricketts, Jr.", "married": "1 Sep 1960"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 67},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "164711", "name": "Kathleen Denise (Kathy) Harshbarger", "born": "15 Sep 1957"},
        {"code": "164712", "name": "Sharon Ricketts", "born": "5 Jan 1961", "verified_terminal": True},
        {"code": "164713", "name": "Michael Ricketts", "born": "5 May 1965", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "16482",
    "name": "Ross Carlton Miller",
    "sex": "M",
    "born": "14 Apr 1946",
    "spouses": [{"name": "Lula Evelyn Bryner", "born": "3 Sep 1947", "married": "22 Oct 1966"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 67},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "164821", "name": "Stephen Daryl Miller", "born": "15 Feb 1968", "verified_terminal": True},
        {"code": "164822", "name": "Susan Grace Miller", "born": "9 Mar 1969", "verified_terminal": True},
        {"code": "164823", "name": "Christopher Lee Miller", "born": "11 Dec 1972", "verified_terminal": True},
        {"code": "164824", "name": "Karen Elaine Miller", "born": "29 Sep 1975", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "16483",
    "name": "Norma Jean Miller",
    "sex": "F",
    "born": "6 Sep 1947",
    "died": "17 Jul 1978",
    "spouses": [{"name": "Martin Walter Stevanus", "married": "27 Jan 1967"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 67},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "164831", "name": "Martin Wayne Stevanus", "born": "17 Apr 1968", "verified_terminal": True},
        {"code": "164832", "name": "Christina Marie Stevanus", "born": "18 Aug 1969"},
        {"code": "164833", "name": "Kathleen Renee Stevanus", "born": "16 Apr 1971"},
        {"code": "164834", "name": "Linda Mae Stevanus", "born": "7 May 1978", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "164A1",
    "name": "Verl Junior Smith",
    "sex": "M",
    "born": "6 Jun 1943",
    "spouses": [{"name": "Linda Kay Moore", "born": "5 Feb 1944", "married": "16 Oct 1964"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 68},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "164A11", "name": "Michael Verl Smith", "born": "4 Jul 1970", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "164A2",
    "name": "Ronald Kenneth Smith",
    "sex": "M",
    "born": "28 Feb 1947",
    "spouses": [{"name": "Janie Weekley", "married": "14 Dec 1969"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 68},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "164A21", "name": "Douglas Kent Smith", "born": "20 Nov 1971", "verified_terminal": True},
        {"code": "164A22", "name": "Stephen Blaine Smith", "born": "11 Oct 1977", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "164A3",
    "name": "Linda Grace Smith",
    "sex": "F",
    "born": "3 Jan 1949",
    "spouses": [
        {"name": "Harold Franklin Knotts", "born": "22 Apr 1945", "married": "8 Mar 1969", "order": 1},
        {"name": "William M. Kimbrel", "born": "17 Aug 1946", "married": "14 May 1987", "order": 2},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 68},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "164A31", "name": "Matthew Loran Knotts", "born": "9 Jul 1971", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "164C1",
    "name": "Kenneth Lee Sager",
    "sex": "M",
    "born": "19 Jan 1948",
    "spouses": [{"name": "Betty Mae Fresh", "born": "10 Mar 1955", "married": "20 Apr 1974", "details": "Same as #16456."}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 68},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": "Children cross-coded 16456x."},
})

ENTRIES.append({
    "code": "164C2",
    "name": "Richard Ervin Sager",
    "sex": "M",
    "born": "7 Nov 1949",
    "spouses": [{"name": "Charann Timmerman", "married": "16 Jun 1974"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 68},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "164C21", "name": "Richard Allen Sager", "born": "1 Jan 1977", "verified_terminal": True},
        {"code": "164C22", "name": "Melonie Ann Sager", "born": "30 Jan 1982", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "164C3",
    "name": "Dolores Irene Sager",
    "sex": "F",
    "born": "21 May 1955",
    "spouses": [{"name": "Albert Watson", "born": "25 Dec 1909", "died": "Dec 1985", "married": "6 Sep 1978"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 68},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "164C31", "name": "Robert Lee Watson", "born": "6 Oct 1977", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "16621",
    "name": "Charles Ray Hileman",
    "sex": "M",
    "born": "18 Feb 1925",
    "spouses": [{"name": "Thelma Marie Barnhart", "born": "16 May 1925", "married": "15 Dec 1945"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 68},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "166211", "name": "Charlene Rae Hileman", "born": "9 Jan 1947"},
        {"code": "166212", "name": "Cynthia Lee Hileman", "born": "20 Apr 1951"},
        {"code": "166213", "name": "Charles Ray Hileman II", "born": "14 Feb 1954"},
        {"code": "166214", "name": "Susan Marie Hileman", "born": "13 Dec 1958"},
        {"code": "166215", "name": "Melissa Ann Hileman", "born": "5 Nov 1961"},
    ],
})

ENTRIES.append({
    "code": "16622",
    "name": "Playford Gail Hileman",
    "sex": "M",
    "born": "7 Jan 1929",
    "spouses": [{"name": "Geraldine Marie Churby", "born": "24 Jul 1937", "married": "17 Mar 1956"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 68},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "166221", "name": "Tami Lynn Hileman", "born": "28 Jan 1960"},
        {"code": "166222", "name": "Tera Lee Hileman", "born": "3 Apr 1963"},
    ],
})

ENTRIES.append({
    "code": "16631",
    "name": "Mary Louise Harshbarger",
    "sex": "F",
    "born": "4 Jul 1935",
    "spouses": [{"name": "Floyd Harold Summers", "born": "11 Apr 1926", "died": "26 Aug 1958", "married": "24 Dec 1953"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 68},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "166311", "name": "Terry Lea Summers", "born": "24 Nov 1955", "verified_terminal": True},
        {"code": "166312", "name": "Patricia Ann Summers", "born": "13 Apr 1957"},
    ],
})

ENTRIES.append({
    "code": "16641",
    "name": "Marvin Lee Hileman",
    "sex": "M",
    "born": "20 Sep 1942",
    "spouses": [
        {"name": "Agnes Marie Sisler", "born": "3 Aug 1945", "died": "8 May 1974", "married": "8 Apr 1967", "order": 1},
        {"name": "Joyce Lea Hoover", "born": "28 Aug 1954", "married": "9 Apr 1976", "order": 2},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 69},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "166411", "name": "Marvin Ray Hileman", "born": "24 Jan 1972", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "17122",
    "name": "Grace Evelyn Spiker",
    "sex": "F",
    "born": "5 Sep 1910",
    "died": "28 Sep 1992",
    "spouses": [{"name": "Paul Natale", "born": "1917", "married": "2 May 1942"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 69},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "171221", "name": "Laura Jean Natale", "born": "1 Dec 1944", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "17123",
    "name": "Blanche Goldie Spiker",
    "sex": "F",
    "born": "24 Dec 1913",
    "died": "24 Sep 1992",
    "spouses": [{"name": "Evertt Paul Casteel", "born": "11 Oct 1912", "died": "17 Feb 1997", "married": "27 Feb 1944"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 69},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "171231", "name": "Charolette Kay Casteel", "born": "1 Sep 1945", "verified_terminal": True},
        {"code": "171232", "name": "Everett Paul Casteel, Jr.", "born": "8 Oct 1952", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "17124",
    "name": "Dora Spiker",
    "sex": "F",
    "born": "14 Oct 1919",
    "spouses": [{"name": "Norman Brafford", "born": "19 Jun 1925", "married": "Nov 1948"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 69},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "171241", "name": "Melvin Norman Brafford", "born": "23 Sep 1949", "verified_terminal": True},
        {"code": "171242", "name": "Marvin Brafford", "born": "10 Jan 1952", "verified_terminal": True},
        {"code": "171243", "name": "Michael John Brafford", "born": "14 Oct 1955", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "17135",
    "name": "Thelma Olieta Spiker",
    "sex": "F",
    "born": "2 Dec 1921",
    "spouses": [{"name": "John William Duncan", "born": "22 May 1913", "died": "23 Jul 1980", "married": "18 Feb 1946"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 70},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "171351", "name": "Gladys Kay Duncan", "born": "7 Sep 1946"},
        {"code": "171352", "name": "Janis Ruth Duncan", "born": "21 May 1955", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "17211",
    "name": "Glenn Guthrie",
    "sex": "M",
    "born": "4 Sep 1909",
    "died": "4 Jul 1986",
    "spouses": [{"name": "Grace Pearl Sisler", "born": "22 Aug 1912", "died": "8 Oct 1990", "married": "2 Jul 1932"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 70},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "172111", "name": "Genevieve Caroline Guthrie", "born": "5 Jan 1933"},
        {"code": "172112", "name": "James Franklin Guthrie", "born": "11 Sep 1934"},
        {"code": "172113", "name": "Jeremiah Jacob Guthrie", "born": "11 Sep 1934", "died": "11 Sep 1934", "flags": {"diedInInfancy": True}, "verified_terminal": True},
        {"code": "172114", "name": "Robert Dale Guthrie", "born": "13 Jun 1936"},
        {"code": "172115", "name": "Viola Marie Guthrie", "born": "10 Jul 1937"},
        {"code": "172116", "name": "Delbert Glenn Guthrie", "born": "1 Sep 1938"},
        {"code": "172117", "name": "Floyd Ray Guthrie", "born": "16 Sep 1939", "verified_terminal": True},
        {"code": "172118", "name": "Thelma Jean Guthrie", "born": "6 Nov 1940"},
        {"code": "172119", "name": "Harvey Paul Guthrie", "born": "14 Nov 1941"},
        {"code": "17211A", "name": "Betty Ruth Guthrie", "born": "22 Jun 1943"},
        {"code": "17211B", "name": "Carl Lee Guthrie", "born": "27 Feb 1945"},
        {"code": "17211C", "name": "Mary Lou Guthrie", "born": "10 Jul 1946", "verified_terminal": True},
        {"code": "17211D", "name": "Helen Ann Guthrie", "born": "23 Oct 1949"},
        {"code": "17211E", "name": "Linda Sue Guthrie", "born": "5 Aug 1951"},
    ],
})

ENTRIES.append({
    "code": "17212",
    "name": "Ruth Guthrie",
    "sex": "F",
    "born": "3 May 1912",
    "spouses": [{"name": "Charles Henry Seese", "born": "2 Aug 1905", "died": "8 Sep 1988", "married": "8 Mar 1930"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 70},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "172121", "name": "James W. Seese", "born": "6 Aug 1930"},
        {"code": "172122", "name": "Thelma Mae Seese", "born": "1 Dec 1932"},
        {"code": "172123", "name": "Thomas Ray Seese", "born": "23 Nov 1943"},
        {"code": "172124", "name": "Dale Franklin Seese", "born": "28 May 1949"},
        {"code": "172125", "name": "David Henry Seese", "born": "3 Sep 1950"},
        {"code": "172126", "name": "Mark Lee Seese", "born": "21 Apr 1954"},
    ],
})

ENTRIES.append({
    "code": "17213",
    "name": "Ethel Guthrie",
    "sex": "F",
    "born": "18 Jan 1914",
    "spouses": [{"name": "George S. Ritchey", "born": "24 Dec 1911", "died": "26 Sep 1970", "married": "10 Feb 1934"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 70},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "172131", "name": "Frances Elaine Ritchey", "born": "19 Jun 1934"},
        {"code": "172132", "name": "Donald Ray Ritchey", "born": "3 Oct 1935"},
        {"code": "172133", "name": "Jane Louise Ritchey", "born": "11 Sep 1937"},
        {"code": "172134", "name": "Susie Alberta Ritchey", "born": "16 Sep 1939"},
        {"code": "172135", "name": "Delmore George Ritchey", "born": "17 Nov 1942"},
        {"code": "172136", "name": "Kenneth Dale Ritchey", "born": "25 Nov 1944"},
        {"code": "172137", "name": "Dennis Blaine Ritchey", "born": "18 Feb 1954"},
    ],
})


# === Pages 71-75 vision pass (2026-06-07): Guthrie/Nicola/Bartholomew gen 6/7 ===
ENTRIES.append({
    "code": "17214",
    "name": "Dora Guthrie",
    "sex": "F",
    "born": "24 Apr 1916",
    "died": "7 May 1982",
    "spouses": [{"name": "Joseph D. McNair", "born": "15 Jun 1918", "married": "13 Sep 1938"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 71},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "172141", "name": "Ralph McNair", "born": "5 Oct 1939", "verified_terminal": True},
        {"code": "172142", "name": "Ruth Irene McNair", "born": "29 Feb 1944"},
        {"code": "172143", "name": "Donald Ray McNair", "born": "5 Feb 1947"},
        {"code": "172144", "name": "Dortha Jean McNair", "born": "26 May 1948"},
        {"code": "172145", "name": "Pauline (Polly) Ann McNair", "born": "17 Apr 1951"},
    ],
})

ENTRIES.append({
    "code": "17215",
    "name": "Ada Belle Guthrie",
    "sex": "F",
    "born": "27 Sep 1921",
    "spouses": [{"name": "John W. Boyd", "born": "27 Dec 1908", "died": "10 Aug 1978", "married": "15 Mar 1937"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 71},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "172151", "name": "Shirley Jane Boyd", "born": "4 Dec 1937"},
        {"code": "172152", "name": "Betty Maxine Boyd", "born": "20 Dec 1939", "verified_terminal": True},
        {"code": "172153", "name": "Nelda Mae Boyd", "born": "5 Jul 1942"},
        {"code": "172154", "name": "Linda Rae Boyd", "born": "25 Mar 1945"},
        {"code": "172155", "name": "John H. Boyd", "born": "17 Oct 1948", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "17261",
    "name": "Clarence Edward Guthrie",
    "sex": "M",
    "born": "8 Jan 1925",
    "spouses": [{"name": "Winifred Alta Knox", "born": "7 Dec 1925", "married": "11 Sep 1949"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 71},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "172611", "name": "Wendy Ann Guthrie", "born": "3 Nov 1955"},
        {"code": "172612", "name": "Clair Edward Guthrie", "born": "22 Sep 1961"},
        {"code": "172613", "name": "Alvin Loyd Guthrie", "born": "19 Aug 1968"},
    ],
})

ENTRIES.append({
    "code": "17262",
    "name": "Ruth Dennis",
    "sex": "F",
    "born": "17 Nov 1926",
    "died": "2 Oct 1996",
    "spouses": [{"name": "Darwin H. Reckart, Sr.", "born": "16 Dec 1915", "married": "19 Mar 1949"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 71},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "172621", "name": "Darwin H. Reckart, Jr.", "born": "26 Jul 1950", "verified_terminal": True},
        {"code": "172622", "name": "Dennis Reckart", "born": "22 Jul 1953"},
    ],
})

ENTRIES.append({
    "code": "17282",
    "name": "Thelma Pearl Guthrie",
    "sex": "F",
    "born": "5 Feb 1930",
    "spouses": [
        {"name": "Junior Lewis Lightner", "born": "27 Feb 1927", "married": "30 Oct 1946", "order": 1},
        {"name": "Marion W. Penland", "born": "27 Mar 1920", "married": "30 Aug 1975", "order": 2},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 72},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "172821", "name": "Linda Joyce Lightner", "born": "9 May 1947"},
        {"code": "172822", "name": "Douglas Lightner, Jr.", "born": "25 Jan 1949"},
        {"code": "172823", "name": "Roger Dale Lightner", "born": "29 Dec 1951"},
    ],
})

ENTRIES.append({
    "code": "17283",
    "name": "Alice Mae Guthrie",
    "sex": "F",
    "born": "6 Oct 1932",
    "spouses": [{"name": "Sam Sheppard"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 72},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "172831", "name": "Gwendlyn Redeen Sheppard", "born": "31 Oct 1949"},
        {"code": "172832", "name": "Redean R. Sheppard", "born": "6 Jan 1968", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "17284",
    "name": "Dwight J. Guthrie",
    "sex": "M",
    "born": "6 May 1934",
    "spouses": [{"name": "Mabel Weaver", "born": "10 Sep 1934", "married": "7 Jun 1952"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 72},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "172841", "name": "Debra Suzanna Guthrie", "born": "30 Jun 1953"},
        {"code": "172842", "name": "Dwight David Guthrie", "born": "27 Sep 1954"},
        {"code": "172843", "name": "Michael Dane Guthrie", "born": "2 Jun 1957"},
        {"code": "172844", "name": "Darryl Lee Guthrie", "born": "7 Dec 1959"},
        {"code": "172845", "name": "Diana Gaye Guthrie", "born": "29 Feb 1964", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "172B2",
    "name": "Agnes Rosalie Bartholomew",
    "sex": "F",
    "born": "15 Mar 1924",
    "spouses": [{"name": "Thomas Raymond Lavens", "born": "23 Aug 1920", "married": "10 Jun 1944"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 72},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "172B21", "name": "Bonnie Jean Lavens", "born": "11 Jan 1946"},
        {"code": "172B22", "name": "Susan Adele Lavens", "born": "8 Mar 1953", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "172B3",
    "name": "Evelyn Irene Bartholomew",
    "sex": "F",
    "born": "24 Sep 1926",
    "spouses": [{"name": "Walter Miller", "born": "7 May 1925", "married": "16 May 1947"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 72},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "172B31", "name": "Jerry Lee Miller", "born": "16 Dec 1947", "died": "9 Feb 1994", "verified_terminal": True},
        {"code": "172B32", "name": "Joy Irene Miller", "born": "18 Apr 1952"},
        {"code": "172B33", "name": "Lori Jean Miller", "born": "29 Sep 1955"},
    ],
})

ENTRIES.append({
    "code": "172B4",
    "name": "Paul Eugene Bartholomew",
    "sex": "M",
    "born": "18 May 1928",
    "spouses": [{"name": "Thelma Marie Waggoner", "born": "11 Jan 1932", "married": "21 Jan 1950"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 73},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "172B41", "name": "Daniel Paul Bartholomew", "born": "18 Jul 1951"},
        {"code": "172B42", "name": "Karen Geniese Bartholomew", "born": "3 Aug 1953"},
        {"code": "172B43", "name": "Timothy Eugene Bartholomew", "born": "6 Jun 1957"},
    ],
})

ENTRIES.append({
    "code": "172B5",
    "name": "Dorothy May Bartholomew",
    "sex": "F",
    "born": "31 May 1930",
    "spouses": [{"name": "Frederick Vernon Habenicht", "born": "16 Jul 1930", "married": "29 Sep 1951"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 73},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "172B51", "name": "Valerie Kay Habenicht", "born": "1 Dec 1953"},
        {"code": "172B52", "name": "Bradley Phillip Habenicht", "born": "20 Sep 1956"},
    ],
})

ENTRIES.append({
    "code": "172B6",
    "name": "Mabel Viola Bartholomew",
    "sex": "F",
    "born": "27 Dec 1933",
    "died": "1 Jan 1988",
    "spouses": [{"name": "Robert S. Hale", "born": "22 Aug 1931", "married": "13 Oct 1951"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 73},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "172B61", "name": "Douglas Robert Hale", "born": "24 Oct 1952"},
        {"code": "172B62", "name": "Cindy Lou Hale", "born": "21 Feb 1959"},
        {"code": "172B63", "name": "Tina Dianne Hale", "born": "13 Jan 1971"},
    ],
})

ENTRIES.append({
    "code": "172B7",
    "name": "David Matthew Bartholomew",
    "sex": "M",
    "born": "12 Jan 1940",
    "spouses": [{"name": "Glendora Lucille Saviers", "born": "12 Sep 1945", "married": "31 Jan 1961"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 73},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "172B71", "name": "Dale Arlon Bartholomew", "born": "31 Jul 1961", "verified_terminal": True},
        {"code": "172B72", "name": "Terry Gene Bartholomew", "born": "24 Mar 1963"},
        {"code": "172B73", "name": "Deborah Annette Bartholomew", "born": "11 Jan 1967"},
        {"code": "172B74", "name": "Dwane Ira Bartholomew", "born": "18 Apr 1968"},
    ],
})

ENTRIES.append({
    "code": "17332",
    "name": "Goldie Marie Friend",
    "sex": "F",
    "born": "24 Oct 1911",
    "spouses": [
        {"name": "Floyd Willard Shaffer", "born": "29 May 1908", "died": "4 Oct 1935", "married": "15 Sep 1928", "order": 1},
        {"name": "Rufus Ray Rodeheaver", "born": "15 Apr 1905", "died": "7 May 1973", "married": "15 Apr 1942", "order": 2},
        {"name": "James Alva DeBerry", "married": "8 Apr 1942", "order": 3},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 74},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "173321", "name": "Willard Arnold Shaffer", "born": "5 Apr 1929"},
        {"code": "173322", "name": "Margaret Virginia Shaffer", "born": "22 May 1931"},
        {"code": "173323", "name": "Robert Ray Shaffer", "born": "23 Apr 1934"},
    ],
})

ENTRIES.append({
    "code": "17333",
    "name": "Gilbert Arnold Friend",
    "sex": "M",
    "born": "1 Aug 1914",
    "died": "28 Feb 1951",
    "spouses": [{"name": "Elsie Flowers", "married": "21 May 1938"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 74},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "173331", "name": "Carolyn Sue Friend", "born": "17 Feb 1939", "verified_terminal": True},
        {"code": "173332", "name": "Gerald (Jerry) Friend", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "17334",
    "name": "Frank William Friend",
    "sex": "M",
    "born": "19 May 1919",
    "spouses": [{"name": "Minnie Taylor", "married": "9 Nov 1935"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 74},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "173341", "name": "Ruth Friend", "born": "Apr 1947", "verified_terminal": True},
        {"code": "173342", "name": "Judith (Judy) Friend", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "17335",
    "name": "Edna Friend",
    "sex": "F",
    "born": "2 May 1919",
    "spouses": [{"name": "Arthur Teets", "born": "13 Mar 1910", "married": "13 Oct 1934"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 74},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "173351", "name": "Virginia Mae Teets", "born": "28 Apr 1935"},
    ],
})

ENTRIES.append({
    "code": "17336",
    "name": "Junior Clinton Friend",
    "sex": "M",
    "born": "24 May 1928",
    "died": "13 Jan 1993",
    "spouses": [
        {"name": "Grace Seese", "born": "17 Aug 1930", "died": "5 Jun 1990", "married": "28 Mar 1948", "order": 1},
        {"name": "Ruth Brown", "married": "1959", "order": 2},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 75},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "173361", "name": "Robert Clinton Friend", "born": "27 Aug 1949"},
        {"code": "173362", "name": "Timothy Friend", "verified_terminal": True},
        {"code": "173363", "name": "David Friend", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "17421",
    "name": "Hazel Moore",
    "sex": "F",
    "born": "4 Nov 1908",
    "spouses": [{"name": "Codie Ray Freeman", "born": "30 Oct 1899"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 75},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "174211", "name": "Raymond Dure Freeman", "born": "2 Dec 1925", "verified_terminal": True},
        {"code": "174212", "name": "Paul Edward Freeman", "born": "20 Aug 1927", "verified_terminal": True},
        {"code": "174213", "name": "Herbert Lee Freeman", "born": "14 Feb 1929", "verified_terminal": True},
        {"code": "174214", "name": "Robert Leo Freeman", "born": "12 Apr 1930", "verified_terminal": True},
        {"code": "174215", "name": "Doris Maralene Freeman", "born": "21 Aug 1931", "verified_terminal": True},
        {"code": "174216", "name": "Betty Louise Freeman", "born": "9 Oct 1933", "verified_terminal": True},
        {"code": "174217", "name": "Calleen May Freeman", "born": "7 Jan 1935", "verified_terminal": True},
        {"code": "174218", "name": "George Jonathan Freeman", "born": "12 Apr 1937", "verified_terminal": True},
        {"code": "174219", "name": "Tomy Ray Freeman", "born": "28 Apr 1939", "verified_terminal": True},
        {"code": "17421A", "name": "Janita Bell Freeman", "born": "22 Jun 1941", "died": "27 Jun 1941", "flags": {"diedInInfancy": True}, "verified_terminal": True},
        {"code": "17421B", "name": "Anna Lee Freeman", "born": "4 Jun 1942", "died": "7 Jun 1942", "flags": {"diedInInfancy": True}, "verified_terminal": True},
        {"code": "17421C", "name": "Kenneth Darl Freeman", "born": "30 Aug 1943", "died": "30 May 1945", "flags": {"diedInInfancy": True}, "verified_terminal": True},
        {"code": "17421D", "name": "Richard Nathan Freeman", "born": "10 May 1945", "died": "17 May 1945", "flags": {"diedInInfancy": True}, "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "17452",
    "name": "Hilda Colleen Nicola",
    "sex": "F",
    "born": "6 Oct 1925",
    "spouses": [{"name": "Dorsey Edwards", "married": "22 Jul 1941"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 75},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "174521", "name": "David Lee Edwards", "born": "19 Jan 1943", "verified_terminal": True},
        {"code": "174522", "name": "Della Louise Edwards", "born": "16 Mar 1944", "verified_terminal": True},
        {"code": "174523", "name": "Donia Lou Edwards", "born": "14 Jul 1946", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "17511",
    "name": "Martha Phillips",
    "sex": "F",
    "born": "24 Jan 1918",
    "spouses": [{"name": "Burchell (Burk) Pritchard", "born": "7 Mar 1915"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 75},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "175111", "name": "Shirley Ann Pritchard", "born": "25 Mar 1937", "verified_terminal": True},
        {"code": "175112", "name": "Carol Sue Pritchard", "born": "Jan 1944", "verified_terminal": True},
        {"code": "175113", "name": "Christina Fay Pritchard", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "17622",
    "name": "Wilson Nicola Miller",
    "sex": "M",
    "born": "3 Apr 1925",
    "spouses": [{"name": "Theo Fisher"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 75},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "176221", "name": "Patricia Ann Miller", "born": "20 Feb 1969", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "17623",
    "name": "Helen Virginia Miller",
    "sex": "F",
    "born": "11 Dec 1926",
    "spouses": [{"name": "James Paul Harr", "born": "1906", "married": "17 Jun 1956"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 75},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "176231", "name": "Nancy Ann Harr", "born": "17 Nov 1956", "verified_terminal": True},
        {"code": "176232", "name": "James Paul Harr, Jr.", "born": "29 Jan 1958", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "17721",
    "name": "Floyd Thamer Frey, Jr.",
    "sex": "M",
    "born": "7 Aug 1916",
    "spouses": [{"name": "Maydell Marsh", "born": "21 Aug 1921", "married": "6 Apr 1942"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 75},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "177211", "name": "Ronald Keith Frey", "born": "26 Dec 1948", "verified_terminal": True},
        {"code": "177212", "name": "Dorothy (Dotty) Lucy Frey", "born": "28 Nov 1949", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "17722",
    "name": "Ella Christine Frey",
    "sex": "F",
    "born": "25 Dec 1917",
    "died": "17 Mar 1964",
    "spouses": [{"name": "Howard Morris"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 75},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "177221", "name": "Armond Morris", "verified_terminal": True},
        {"code": "177222", "name": "Albert Morris", "verified_terminal": True},
        {"code": "177223", "name": "Patricia Morris", "verified_terminal": True},
    ],
})


# === Pages 76-80 vision pass (2026-06-07): Frey/Ball/Frantz/Nicola/DeBerry gen 6/7 ===
ENTRIES.append({
    "code": "17723",
    "name": "Robert Lewis Frey",
    "sex": "M",
    "born": "19 May 1919",
    "spouses": [{"name": "Sybil Osborn"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 76},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "177231", "name": "Infant", "flags": {"diedInInfancy": True}, "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "17724",
    "name": "Edythe Lucille Frey",
    "sex": "F",
    "spouses": [{"name": "James (Eb) Marsh"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 76},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "177241", "name": "Jack Marsh", "verified_terminal": True},
        {"code": "177242", "name": "Gary Marsh", "verified_terminal": True},
        {"code": "177243", "name": "Vicky Marsh", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "17725",
    "name": "Ralph Marshall Frey",
    "sex": "M",
    "spouses": [{"name": "Wilma Lee Crites"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 76},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "177251", "name": "Ralph Marshall Frey, Jr.", "verified_terminal": True},
        {"code": "177252", "name": "Sharon Frey"},
    ],
})

ENTRIES.append({
    "code": "17727",
    "name": "Lelia Margaret Frey",
    "sex": "F",
    "born": "6 Sep 1925",
    "spouses": [{"name": "Dale Marsh"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 76},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "177271", "name": "Terry Marsh", "verified_terminal": True},
        {"code": "177272", "name": "John Marsh", "verified_terminal": True},
        {"code": "177273", "name": "Libby Marsh", "verified_terminal": True},
        {"code": "177274", "name": "Kevin Marsh", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "17728",
    "name": "George Calvin Frey",
    "sex": "M",
    "born": "1 Mar 1927",
    "spouses": [{"name": "Betty Freeman"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 76},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "177281", "name": "David Frey", "verified_terminal": True},
        {"code": "177282", "name": "Steven Frey", "verified_terminal": True},
        {"code": "177283", "name": "Marsha Frey", "verified_terminal": True},
        {"code": "177284", "name": "Jeffery Frey", "verified_terminal": True},
        {"code": "177285", "name": "Angela Frey", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "17729",
    "name": "Charles Leon Frey",
    "sex": "M",
    "born": "17 Aug 1929",
    "spouses": [{"name": "Colleen Freeman"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 76},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "177291", "name": "Loretha Frey", "verified_terminal": True},
        {"code": "177292", "name": "Floyd (Butch) Frey", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1772A",
    "name": "Daniel Harold Frey",
    "sex": "M",
    "born": "17 Jun 1931",
    "spouses": [{"name": "Rose Boyles"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 76},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1772A1", "name": "Larry Frey", "verified_terminal": True},
        {"code": "1772A2", "name": "Joyce Frey", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1772C",
    "name": "John Thomas Frey",
    "sex": "M",
    "spouses": [{"name": "Noretta Pitzer"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 76},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1772C1", "name": "Michael Frey", "verified_terminal": True},
        {"code": "1772C2", "name": "Tonda Frey", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1772D",
    "name": "Darl Eugene Frey",
    "sex": "M",
    "spouses": [{"name": "Norma Carpenter"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 76},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1772D1", "name": "Deborah Frey", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "17753",
    "name": "Don Robert Frey",
    "sex": "M",
    "born": "28 Apr 1927",
    "spouses": [{"name": "Mary Louise Murphy", "married": "1950"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 76},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "177531", "name": "Brenda Sue Frey", "verified_terminal": True},
        {"code": "177532", "name": "Linda Lou Frey", "verified_terminal": True},
        {"code": "177533", "name": "Larry Duane Frey", "born": "1956", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "17812",
    "name": "Ada Catherine Ball",
    "sex": "F",
    "born": "12 Jan 1923",
    "spouses": [{"name": "Glenn I. Sapp", "born": "21 May 1920", "married": "18 Nov 1945"}],
    "notes": "PDF says only 'Had one Child'.",
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 77},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
})

ENTRIES.append({
    "code": "17813",
    "name": "Anna Bell Ball",
    "sex": "F",
    "born": "4 Sep 1925",
    "spouses": [{"name": "Allen Shandler", "married": "8 Oct 1944"}],
    "notes": "PDF says only 'Had one Son'.",
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 77},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
})

ENTRIES.append({
    "code": "17821",
    "name": "Raymond Murl Ball",
    "sex": "M",
    "born": "23 Aug 1916",
    "spouses": [{"name": "Audra Walverton", "born": "27 Apr 1923", "married": "2 Jan 1943"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 77},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "178211", "name": "Beatrice Lee Ball", "born": "18 May 1940", "verified_terminal": True},
        {"code": "178212", "name": "Raymond Murl Ball, Jr.", "born": "29 Jan 1946", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "17822",
    "name": "Evelyn Ball",
    "sex": "F",
    "born": "29 Dec 1917",
    "spouses": [{"name": "Charles Hall"}],
    "notes": "PDF says only 'Had two Children'.",
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 77},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
})

ENTRIES.append({
    "code": "17831",
    "name": "Paul Morris Ball",
    "sex": "M",
    "born": "5 May 1922",
    "spouses": [{"name": "Virginia", "married": "1 Dec 1943"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 77},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "178311", "name": "Paul Michael Ball", "verified_terminal": True},
        {"code": "178312", "name": "Joseph Ball", "born": "31 Aug 1949", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "17833",
    "name": "Russell Edgar Ball",
    "sex": "M",
    "born": "3 Dec 1924",
    "spouses": [{"name": "Rosa Mary Sheets", "born": "1927", "married": "23 Jan 1945"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 77},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "178331", "name": "Shirlean Ann Ball", "born": "25 Dec 1945", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "111121",
    "name": "James Albert Frantz",
    "sex": "M",
    "born": "24 Jan 1941",
    "spouses": [{"name": "Ruth Ann Huges"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 78},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1111211", "name": "Donna Darlene Frantz", "born": "1 Nov 1962", "verified_terminal": True},
        {"code": "1111212", "name": "William James Frantz", "born": "7 Jan 1965", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "111122",
    "name": "Elina Edna Frantz",
    "sex": "F",
    "born": "5 Feb 1947",
    "spouses": [{"name": "Garry B. DeWitt"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 78},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1111221", "name": "Garry DeWitt, Jr.", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "111123",
    "name": "Charles Elmer Frantz",
    "sex": "M",
    "born": "14 Oct 1951",
    "spouses": [{"name": "Inetta Louise Friend", "married": "12 Dec 1971"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 78},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1111231", "name": "Consueloe Frantz", "born": "18 Jun 1971", "verified_terminal": True},
        {"code": "1111232", "name": "Bryon Charles Frantz", "born": "22 Sep 1975", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "113151",
    "name": "Lois Winnifred VanSickle",
    "sex": "F",
    "spouses": [{"name": "Samuel Eugene Thomas", "born": "1925", "died": "24 Apr 1975"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 78},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1131511", "name": "Rodney E. Thomas", "verified_terminal": True},
        {"code": "1131512", "name": "Gerald W. Thomas"},
    ],
})

ENTRIES.append({
    "code": "113221",
    "name": "Doris Jean Frazee",
    "sex": "F",
    "born": "11 Jul 1928",
    "spouses": [{"name": "John Lee Western", "married": "15 May 1949"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 78},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1132211", "name": "Shirley Jean Western", "born": "1952", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "113222",
    "name": "Willard Ellsworth Frazee",
    "sex": "M",
    "born": "5 Feb 1931",
    "spouses": [{"name": "Betty Marie Fike", "born": "28 Feb 1931", "married": "14 Feb 1953"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 78},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1132221", "name": "Kathy Marie Frazee", "born": "1 Jun 1956"},
        {"code": "1132222", "name": "Brenda Kay Frazee", "born": "24 Aug 1959"},
    ],
})

ENTRIES.append({
    "code": "113223",
    "name": "Raymond Luther Frazee",
    "sex": "M",
    "born": "8 Nov 1936",
    "spouses": [{"name": "Betty Jean Ford"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 78},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1132231", "name": "Kimberly Frazee", "born": "13 Jul 1960", "verified_terminal": True},
        {"code": "1132232", "name": "Alan Frazee", "born": "3 Apr 1963", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "113311",
    "name": "Suzanna Kay Guthrie",
    "sex": "F",
    "born": "2 Dec 1942",
    "spouses": [{"name": "Glenn Duane Evenstad", "born": "25 May 1935", "married": "27 Dec 1967"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 78},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1133111", "name": "Jennifer Rachel Evenstad", "born": "21 Jun 1971", "verified_terminal": True},
        {"code": "1133112", "name": "Christopher Glenn Evenstad", "born": "1 Jun 1973", "verified_terminal": True},
        {"code": "1133113", "name": "Kurt David Evenstad", "born": "4 Dec 1975", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "113312",
    "name": "Samuel Fleming Guthrie",
    "sex": "M",
    "born": "14 Feb 1945",
    "spouses": [{"name": "Bonnie Jane Duncan", "born": "6 Apr 1947", "married": "7 Apr 1968"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 78},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1133121", "name": "Samuel Paul Guthrie", "born": "30 Jul 1976", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "113313",
    "name": "Ward David Guthrie",
    "sex": "M",
    "born": "17 Mar 1946",
    "spouses": [{"name": "Carol Ann Shaw", "born": "30 Dec 1952", "married": "21 Jan 1978"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 78},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1133131", "name": "Laura Beth Guthrie", "born": "21 Oct 1981", "verified_terminal": True},
        {"code": "1133132", "name": "Sarah Ann Guthrie", "born": "29 Feb 1984", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "113511",
    "name": "Richard Warren Nieman",
    "sex": "M",
    "born": "13 Feb 1948",
    "spouses": [{"name": "Lisa Ann Elliott", "married": "13 May 1972"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 79},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1135111", "name": "Daughter", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "113512",
    "name": "Deborah Jo Nieman",
    "sex": "F",
    "born": "19 May 1950",
    "spouses": [
        {"name": "Edgar Grant Armstrong", "born": "26 Jan 1947", "married": "28 Dec 1970", "order": 1},
        {"name": "Charles G. Koch", "order": 2},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 79},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1135121", "name": "Adam Grant Armstrong", "born": "20 Nov 1976", "verified_terminal": True},
        {"code": "1135122", "name": "Amber Ann Armstrong", "born": "10 Oct 1979", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "113611",
    "name": "Dale M. Slaubaugh",
    "sex": "M",
    "born": "13 Sep 1935",
    "spouses": [{"name": "Nancy Nieder", "married": "10 Oct 1959"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 79},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1136111", "name": "Michael Slaubaugh", "born": "20 Jul 1960", "verified_terminal": True},
        {"code": "1136112", "name": "Julie Helen Slaubaugh", "born": "17 Jul 1962", "verified_terminal": True},
        {"code": "1136113", "name": "John Slaubaugh", "born": "22 Sep 1965", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "113612",
    "name": "Terry Guthrie Slaubaugh",
    "sex": "M",
    "born": "8 May 1938",
    "spouses": [{"name": "Victoria Ann Gordon", "married": "27 Aug 1960"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 79},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1136121", "name": "Steven Scott Slaubaugh", "born": "30 Aug 1963", "verified_terminal": True},
        {"code": "1136122", "name": "Todd Slaubaugh", "born": "16 Sep 1966", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "122411",
    "name": "Glennis Hugh McNear",
    "sex": "M",
    "born": "5 Jan 1928",
    "spouses": [{"name": "Willard Louise Durr", "born": "13 Sep 1928", "married": "22 Jun 1948"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 79},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1224111", "name": "Janet Louise McNear", "born": "19 Jun 1949"},
        {"code": "1224112", "name": "Sonny Allen McNear", "born": "3 Jan 1951"},
    ],
})

ENTRIES.append({
    "code": "122412",
    "name": "Betty Mary Elizabeth McNear",
    "sex": "F",
    "born": "24 Mar 1931",
    "spouses": [{"name": "Lawrence Cecil Durr", "born": "21 Jul 1927", "married": "29 Jan 1949"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 79},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1224121", "name": "Rosa Mary Durr", "born": "8 May 1949"},
        {"code": "1224122", "name": "Lawrence Junior Durr", "born": "27 Jun 1953"},
        {"code": "1224123", "name": "Kathy Ann Durr", "born": "5 Aug 1955"},
        {"code": "1224124", "name": "Danny Ray Durr", "born": "2 May 1961", "verified_terminal": True},
        {"code": "1224125", "name": "Timmy Allen Dur", "born": "28 Jun 1962"},
    ],
})

ENTRIES.append({
    "code": "122413",
    "name": "Melvin Grey McNear",
    "sex": "M",
    "born": "2 May 1933",
    "spouses": [{"name": "Pamela Deloris Poling", "born": "6 Jun 1935", "married": "3 Jul 1956"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 79},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1224131", "name": "Rickey Dwaynne McNear", "born": "1 May 1957", "died": "26 Apr 1989", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "122414",
    "name": "Shirley Ann Durr",
    "sex": "F",
    "born": "19 Jun 1936",
    "died": "16 Jun 1997",
    "spouses": [{"name": "Albert Lee Hoover", "born": "6 May 1932"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 79},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1224141", "name": "Randy Lee Hoover", "born": "26 Mar 1956", "verified_terminal": True},
        {"code": "1224142", "name": "Steven Faye Hoover", "born": "14 Aug 1958", "died": "21 Jul 1984", "verified_terminal": True},
        {"code": "1224143", "name": "Stella Darlene Hoover", "born": "14 Aug 1958"},
        {"code": "1224144", "name": "Brenda Ann Hoover", "born": "14 Jun 1960"},
        {"code": "1224145", "name": "Deborah Belle Hoover", "born": "7 Jun 1961"},
        {"code": "1224146", "name": "Tony Ray Hoover", "born": "3 Apr 1964", "verified_terminal": True},
        {"code": "1224147", "name": "Lissa Lynn Hoover", "born": "27 Dec 1967", "verified_terminal": True},
        {"code": "1224148", "name": "David Allen Hoover", "born": "7 Mar 1972", "verified_terminal": True},
        {"code": "1224149", "name": "Katine Marie Hoover", "born": "9 Feb 1974", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "122416",
    "name": "Harold Ray McNear",
    "sex": "M",
    "born": "21 Jun 1946",
    "spouses": [{"name": "Dianna Smith"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 80},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1224161", "name": "Shannon Ray McNear", "born": "19 Jan 1971", "verified_terminal": True},
        {"code": "1224162", "name": "Kimberly Ann McNear", "born": "17 Apr 1974", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "122431",
    "name": "Kermit Nelson DeBerry",
    "sex": "M",
    "born": "6 Dec 1937",
    # died/buried + Barbara's death+burial backfilled from user submissions
    # (issues #8 and #9 — Tuscon→Tucson spelling normalised).
    "died": "19 Oct 2007",
    "died_place": "Seffner, FL",
    "buried": "Seffner, FL",
    "spouses": [{
        "name": "Barbara Ann Mary Voelker",
        "born": "1 Dec 1940",
        "died": "5 Jul 2024",
        "died_place": "Tucson, AZ",
        "buried": "Seffner, FL",
        "married": "18 Jun 1960",
    }],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 80},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-15", "notes": "Death/burial details for Kermit and Barbara added via user submissions (issues #8, #9)."},
    "children": [
        {"code": "1224311", "name": "Michael Nelson DeBerry", "born": "25 Mar 1961"},
        {"code": "1224312", "name": "William (Teddy) Dale DeBerry", "born": "6 Apr 1963"},
        {"code": "1224313", "name": "Christopher Joseph DeBerry", "born": "16 Nov 1966", "verified_terminal": True},
        {"code": "1224314", "name": "Brian Keith DeBerry", "born": "6 Feb 1973", "died": "1 Apr 1990", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "122432",
    "name": "Lois Nita DeBerry",
    "sex": "F",
    "born": "4 Apr 1944",
    "spouses": [{"name": "Kenneth Robert Shea", "born": "27 Jan 1937", "married": "2 Jun 1962"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 80},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1224321", "name": "Sherry Lynne Shea", "born": "27 Jan 1963"},
        {"code": "1224322", "name": "Kenneth Scott Shea", "born": "5 Apr 1969"},
    ],
})

ENTRIES.append({
    "code": "122441",
    "name": "Thomas Eugene DeBerry",
    "sex": "M",
    "born": "9 Nov 1935",
    "spouses": [{"name": "Betty Jane Stevenson", "born": "4 Aug 1932", "married": "16 Feb 1957"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 80},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1224411", "name": "Katrina Jane DeBerry", "born": "17 Jan 1958", "verified_terminal": True},
        {"code": "1224412", "name": "Philip Eugene DeBerry", "born": "17 Apr 1960", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "122442",
    "name": "James Franklin DeBerry",
    "sex": "M",
    "born": "11 Jan 1937",
    "died": "12 Aug 1972",
    "spouses": [{"name": "Mildred Vinate Tabor", "born": "9 May 1938", "married": "15 Nov 1958"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 80},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1224421", "name": "Douglas Mark DeBerry", "born": "5 Sep 1959", "verified_terminal": True},
        {"code": "1224422", "name": "Lance Brad DeBerry", "born": "19 Sep 1965", "verified_terminal": True},
        {"code": "1224423", "name": "Andrea Lee DeBerry", "born": "3 May 1968", "verified_terminal": True},
        {"code": "1224424", "name": "Alfred Eenge Yates", "born": "17 Mar 1966", "flags": {"adopted": True}, "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "122443",
    "name": "Robert Dale DeBerry",
    "sex": "M",
    "born": "4 Jul 1938",
    "spouses": [{"name": "Wilma Jane Conner", "born": "1 Oct 1940", "married": "31 Dec 1956"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 80},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1224431", "name": "Robin Lynn DeBerry", "born": "14 Feb 1958"},
        {"code": "1224432", "name": "Julie Lee DeBerry", "born": "1 May 1960"},
        {"code": "1224433", "name": "Debra Dale DeBerry", "born": "13 Oct 1962", "verified_terminal": True},
    ],
})


# === Pages 81-85 vision pass (2026-06-07): DeBerry/Deal/Shaffer/Livengood gen 7 ===
ENTRIES.append({
    "code": "122444",
    "name": "Ethel May DeBerry",
    "sex": "F",
    "born": "5 Jun 1940",
    "spouses": [{"name": "Marvin Ray Thomas", "born": "7 Jan 1935", "married": "22 Jan 1956"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 81},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1224441", "name": "Barbara Jean Thomas", "born": "31 Jul 1956"},
        {"code": "1224442", "name": "Wilma Lee Thomas", "born": "26 Oct 1957"},
        {"code": "1224443", "name": "Marvin Ray Thomas", "born": "27 Nov 1959", "verified_terminal": True},
        {"code": "1224444", "name": "James Oliver Thomas", "born": "11 Apr 1961", "verified_terminal": True},
        {"code": "1224445", "name": "Christopher Allen Thomas", "born": "22 Jul 1962", "verified_terminal": True},
        {"code": "1224446", "name": "Christina Alvena Thomas", "born": "22 Jul 1962", "verified_terminal": True},
        {"code": "1224447", "name": "Bryson Lynn Thomas", "born": "24 Jun 1963", "verified_terminal": True},
        {"code": "1224448", "name": "Sharry Dee Thomas", "born": "16 Sep 1964", "verified_terminal": True},
        {"code": "1224449", "name": "Terry Lee Thomas", "born": "16 Sep 1694", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "122445",
    "name": "Patty Ann DeBerry",
    "sex": "F",
    "born": "12 Sep 1941",
    "spouses": [
        {"name": "James Metz", "order": 1},
        {"name": "Allen Stephen", "order": 2},
        {"name": "Dale E. Jones", "born": "21 Jul 1942", "order": 3},
        {"name": "John Jack H. Taylor", "married": "20 Feb 1978", "order": 4},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 81},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1224451", "name": "Marcia Dawn Jones", "born": "2 Apr 1961", "verified_terminal": True},
        {"code": "1224452", "name": "John Allen Jones", "born": "8 Jan 1963", "verified_terminal": True},
        {"code": "1224453", "name": "Felicia Renee Jones", "born": "14 Feb 1964", "verified_terminal": True},
        {"code": "1224454", "name": "Brian Timothy Jones", "born": "26 Dec 1969", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "122446",
    "name": "David Carl DeBerry",
    "sex": "M",
    "born": "19 Oct 1944",
    "spouses": [
        {"name": "Linda", "order": 1},
        {"name": "Sharon Lee Ballard", "born": "9 Sep 1948", "married": "16 Feb 1976", "order": 2},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 81},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1224461", "name": "David Allen DeBerry", "verified_terminal": True},
        {"code": "1224462", "name": "Eric Allen DeBerry", "born": "2 Jun 1977", "verified_terminal": True},
        {"code": "1224463", "name": "Shawn Carl DeBerry", "born": "1 Jul 1981", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "122447",
    "name": "Terry Lee DeBerry",
    "sex": "M",
    "born": "11 Apr 1948",
    "spouses": [{"name": "Luilla Bates", "born": "29 Jul 1950", "married": "8 Jul 1967"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 81},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1224471", "name": "Ryan Lee DeBerry", "born": "12 May 1970", "verified_terminal": True},
        {"code": "1224472", "name": "James Franklin DeBerry", "born": "7 Jan 1973", "verified_terminal": True},
        {"code": "1224473", "name": "Wyatt Clark DeBerry", "born": "23 Feb 1974", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "122448",
    "name": "Ronald Junior DeBerry",
    "sex": "M",
    "born": "6 Jul 1954",
    "spouses": [{"name": "Rhonda Rose Taylor", "born": "8 May 1958", "married": "10 Jul 1976"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 81},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1224481", "name": "Regina Rose DeBerry", "born": "11 Feb 1982", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "122449",
    "name": "Sandra Dianne DeBerry",
    "sex": "F",
    "born": "12 Oct 1955",
    "spouses": [{"name": "Charles Stonebraker", "born": "26 May 1953", "married": "18 Dec 1973"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 81},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1224491", "name": "Chad Edward Stonebraker", "born": "30 Jul 1974", "verified_terminal": True},
        {"code": "1224492", "name": "Renee Yuonne Stonebraker", "born": "17 Sep 1979", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "12244A",
    "name": "Michael Dean DeBerry",
    "sex": "M",
    "born": "3 Nov 1956",
    "spouses": [{"name": "Karen Sue Carle Johnson", "married": "12 Dec 1980"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 81},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "12244A1", "name": "Valerie Dawn Johnson", "born": "21 Oct 1976", "died": "1989", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "122472",
    "name": "Margaret Mae DeBerry",
    "sex": "F",
    "born": "25 Oct 1940",
    "died": "29 Nov 1992",
    "spouses": [{"name": "Ashford Elmer Hawkins", "born": "10 Jul 1940", "married": "2 Apr 1966"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 81},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1224721", "name": "James Frederick Hawkins", "born": "15 Mar 1968", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "122473",
    "name": "Marvin Glenn DeBerry",
    "sex": "M",
    "born": "8 May 1942",
    "spouses": [
        {"name": "Joann Marie McIntyre", "born": "22 Dec 1941", "married": "17 Jun 1962", "order": 1},
        {"name": "Mrs. Norma Brewer", "born": "14 Nov 1930", "married": "3 Dec 1971", "order": 2},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 82},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1224731", "name": "Kelvin Douglas DeBerry", "born": "10 Jul 1963", "verified_terminal": True},
        {"code": "1224732", "name": "Alvin Glenn DeBerry", "born": "4 Aug 1966", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "122474",
    "name": "Judy Ann DeBerry",
    "sex": "F",
    "born": "23 Aug 1943",
    "spouses": [{"name": "Wallace Franklin Hall, Jr.", "born": "6 Apr 1943", "married": "21 Apr 1963"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 82},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1224741", "name": "Robert Lloyd Hall", "born": "26 May 1964", "verified_terminal": True},
        {"code": "1224742", "name": "Larry Franklin Hall", "born": "19 Jan 1966", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "122475",
    "name": "Gerald Wade DeBerry",
    "sex": "M",
    "born": "29 Jul 1949",
    "spouses": [{"name": "Lois Lea (Gowans) McGrew", "married": "28 Mar 1976"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 82},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1224751", "name": "Melissa Ann McGrew DeBerry", "born": "Mar 1971", "flags": {"adopted": True}, "verified_terminal": True},
        {"code": "1224752", "name": "Daniel Wade DeBerry", "born": "18 Jun 1977", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1224A1",
    "name": "Roger DeVaughn DeBerry",
    "sex": "M",
    "born": "13 Apr 1947",
    "spouses": [{"name": "Mirella"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 82},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1224A11", "name": "Timothy Roger DeBerry", "born": "7 Mar 1969", "verified_terminal": True},
        {"code": "1224A12", "name": "Pamela Christina DeBerry", "born": "22 Nov 1970", "verified_terminal": True},
        {"code": "1224A13", "name": "Stacy DeBerry", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "123111",
    "name": "Jo Annabel Kelly",
    "sex": "F",
    "born": "8 Jan 1930",
    "died": "5 Aug 1989",
    "spouses": [{"name": "James Eugene Feeney", "born": "30 Sep 1929", "married": "13 Dec 1950"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 82},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1231111", "name": "Judith Anne Feeney", "born": "13 Sep 1951", "verified_terminal": True},
        {"code": "1231112", "name": "Joseph Eugene Feeney", "born": "12 Sep 1952", "verified_terminal": True},
        {"code": "1231113", "name": "John Charles Feeney", "born": "6 Jan 1954", "verified_terminal": True},
        {"code": "1231114", "name": "James Sheridan Feeney, II", "born": "29 Nov 1956", "verified_terminal": True},
        {"code": "1231115", "name": "Jeffrey Drew Feeney", "born": "14 Nov 1959", "verified_terminal": True},
        {"code": "1231116", "name": "Jennifer Sue Feeney", "born": "6 Aug 1965", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "123121",
    "name": "Jacklyn Deal",
    "sex": "F",
    "spouses": [{"name": "Vasile Popvick"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 82},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1231211", "name": "Sonny Lyn Popvick", "verified_terminal": True},
        {"code": "1231212", "name": "Gary Ray Popvick", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "123122",
    "name": "Judy Deal",
    "sex": "F",
    "spouses": [{"name": "Larry Ludy"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 82},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1231221", "name": "Michele Judy", "verified_terminal": True},
        {"code": "1231222", "name": "Jenifer Judy", "verified_terminal": True},
        {"code": "1231223", "name": "Larry Judy", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "123311",
    "name": "William Guy Deal",
    "sex": "M",
    "born": "26 Nov 1931",
    "spouses": [{"name": "Ivy Samantha McCumber", "born": "11 Feb 1932", "married": "7 May 1955"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 82},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1233111", "name": "Patricia Diane Deal", "born": "31 May 1955", "verified_terminal": True},
        {"code": "1233112", "name": "Garry Allen Deal", "born": "8 Oct 1956", "verified_terminal": True},
        {"code": "1233113", "name": "Roger Gene Deal", "born": "21 May 1960", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "123312",
    "name": "Bruce Earl Deal",
    "sex": "M",
    "born": "22 Oct 1936",
    "spouses": [{"name": "Sandra Kaye Peach", "born": "25 Aug 1949", "married": "28 Jun 1970"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 82},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1233121", "name": "Gregory Deal", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "123313",
    "name": "Glenn Paul Deal",
    "sex": "M",
    "born": "3 Aug 1941",
    "spouses": [{"name": "Eleanor Jane Shaffer", "born": "6 Nov 1939", "married": "7 Jan 1961"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 83},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1233131", "name": "Vernon Kenneth Deal", "born": "21 Jul 1962", "verified_terminal": True},
        {"code": "1233132", "name": "Ronald Wayne Deal", "born": "12 Jan 1967", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "123314",
    "name": "Dale Allen Deal",
    "sex": "M",
    "born": "5 May 1943",
    "spouses": [{"name": "Nannie Marie Dressel", "born": "22 Jul 1951", "married": "11 Apr 1970"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 83},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1233141", "name": "Laurie Deal", "verified_terminal": True},
        {"code": "1233142", "name": "Lisa Deal", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "123321",
    "name": "Dorothy Irene Shaffer",
    "sex": "F",
    "born": "21 Feb 1926",
    "spouses": [{"name": "Frank W. Fike", "born": "26 Feb 1916", "died": "19 Feb 1982", "married": "6 Dec 1941"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 83},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1233211", "name": "Pearl Marie Fike", "born": "13 Jul 1942"},
        {"code": "1233212", "name": "William Lee Fike", "born": "20 Nov 1945"},
        {"code": "1233213", "name": "Charlotte Kay Fike", "born": "5 Feb 1948"},
        {"code": "1233214", "name": "Janet Sue Fike", "born": "28 Dec 1948"},
        {"code": "1233215", "name": "Ralph Eugene Fike", "born": "17 Jan 1950"},
        {"code": "1233216", "name": "Chester Ray Fike", "born": "3 Feb 1952"},
        {"code": "1233217", "name": "James Dale Fike", "born": "15 Apr 1953"},
    ],
})

ENTRIES.append({
    "code": "123322",
    "name": "Betty Jane Shaffer",
    "sex": "F",
    "born": "16 Feb 1928",
    "spouses": [{"name": "Glen Dale Casteel", "born": "2 Dec 1924", "died": "23 May 1990", "married": "8 Jun 1946"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 83},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1233221", "name": "Sandra Kay Casteel", "born": "9 Aug 1947"},
        {"code": "1233222", "name": "Erica Dale Casteel", "born": "10 Apr 1949", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "123323",
    "name": "Grace Pearl Shaffer",
    "sex": "F",
    "born": "19 Oct 1930",
    "died": "19 Oct 1968",
    "spouses": [{"name": "Mack Arthur Lewis", "born": "29 Aug 1929", "married": "22 Dec 1949"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 83},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1233231", "name": "Cyrus Duane Chidester", "born": "17 Jan 1949"},
        {"code": "1233232", "name": "Fred LeRoy Lewis", "born": "18 Nov 1950", "verified_terminal": True},
        {"code": "1233233", "name": "Steven Lee Lewis", "born": "26 Feb 1955", "died": "2 Apr 1956", "flags": {"diedInInfancy": True}, "verified_terminal": True},
        {"code": "1233234", "name": "Diane Lynn Lewis", "born": "22 Feb 1957"},
        {"code": "1233235", "name": "Mack Arthur Lewis, Jr.", "born": "7 Sep 1958"},
        {"code": "1233236", "name": "Paul Kevin Lewis", "born": "20 Nov 1959"},
        {"code": "1233237", "name": "William Jackson Lewis", "born": "7 Apr 1961", "died": "8 Oct 1977", "verified_terminal": True},
        {"code": "1233238", "name": "Pamela Ann Lewis", "born": "17 May 1963", "died": "16 Feb 1965", "flags": {"diedInInfancy": True}, "verified_terminal": True},
        {"code": "1233239", "name": "Crystal Sue Lewis", "born": "8 May 1964", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "123324",
    "name": "Mary Lou Shaffer",
    "sex": "F",
    "born": "5 Nov 1933",
    "spouses": [{"name": "Donald Seiby Willis", "born": "29 Nov 1927", "married": "28 Mar 1951"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 83},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1233241", "name": "Allen Martin Willis", "born": "25 Oct 1951"},
        {"code": "1233242", "name": "Edith Willis", "born": "31 Aug 1953"},
        {"code": "1233243", "name": "Bruce Edward Willis", "born": "5 Jul 1955"},
        {"code": "1233244", "name": "James Brian Willis", "born": "10 Mar 1960"},
    ],
})

ENTRIES.append({
    "code": "123325",
    "name": "Chester Junior Shaffer",
    "sex": "M",
    "born": "11 Mar 1935",
    "died": "27 Nov 1996",
    "spouses": [{"name": "Ardith June Jones", "born": "14 Jun 1933", "married": "26 Mar 1955"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 84},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1233251", "name": "Daniel J. Shaffer", "born": "28 Sep 1955"},
        {"code": "1233252", "name": "Deborah Kay Shaffer", "born": "4 Dec 1956"},
        {"code": "1233253", "name": "Barbara Louise Shaffer", "born": "20 Jul 1958", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "123326",
    "name": "William Jackson Shaffer",
    "sex": "M",
    "born": "22 Nov 1937",
    "spouses": [{"name": "Patricia Ann McLain", "born": "9 Sep 1941", "died": "18 Apr 1988", "married": "13 Dec 1958"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 84},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1233261", "name": "William Jackson Shaffer, Jr.", "born": "17 Oct 1959"},
        {"code": "1233262", "name": "Roger Lee Shaffer", "born": "21 Jan 1961"},
        {"code": "1233263", "name": "Harold Stephen Shaffer", "born": "30 Jan 1964", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "123329",
    "name": "Joyce Elaine Shaffer",
    "sex": "F",
    "born": "14 Sep 1946",
    "spouses": [{"name": "Larry Noble Galloway", "born": "28 Jun 1944", "married": "23 Nov 1961"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 84},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1233291", "name": "Joseph Dewane Galloway", "born": "5 Apr 1962"},
    ],
})

ENTRIES.append({
    "code": "123341",
    "name": "Wilma Jean Livengood",
    "sex": "F",
    "born": "1 Mar 1932",
    "spouses": [{"name": "Donald W. Bohn", "born": "26 Jun 1929", "married": "1 Jun 1957"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 84},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1233411", "name": "William Bruce Bohn", "verified_terminal": True},
        {"code": "1233412", "name": "Robert Bohn", "verified_terminal": True},
        {"code": "1233413", "name": "Donna Bohn", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "123342",
    "name": "Lester Ray Livengood",
    "sex": "M",
    "born": "14 Jun 1935",
    "spouses": [{"name": "Joretta Delphia Uphold", "born": "14 Sep 1938", "married": "8 Jun 1957"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 84},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1233421", "name": "Kathy Livengood", "verified_terminal": True},
        {"code": "1233422", "name": "Donna Livengood", "verified_terminal": True},
        {"code": "1233423", "name": "Linda Livengood", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "123343",
    "name": "Dorothy Marie Livengood",
    "sex": "F",
    "born": "15 May 1937",
    "spouses": [{"name": "William M. Murphy"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 84},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1233431", "name": "Ann Marie Murphy", "verified_terminal": True},
        {"code": "1233432", "name": "Billie Sue Murphy", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "123344",
    "name": "Robert Glenn Livengood",
    "sex": "M",
    "born": "15 Feb 1939",
    "spouses": [{"name": "Bonnie Mae Maust", "born": "16 Aug 1943", "married": "21 Oct 1961"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 84},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1233441", "name": "Douglas Livengood", "verified_terminal": True},
        {"code": "1233442", "name": "Barbara Livengood", "verified_terminal": True},
        {"code": "1233443", "name": "Brenda Livengood", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "123351",
    "name": "Russell Ray Deal",
    "sex": "M",
    "born": "18 Dec 1937",
    "spouses": [
        {"name": "Virginia Ruth Guthrie", "born": "6 Oct 1939", "died": "27 Sep 1987", "details": "Same as #13217.", "order": 1},
        {"name": "Janet Yost", "born": "19 Apr 1940", "order": 2},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 84},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": "Children cross-coded 132171-4."},
})

ENTRIES.append({
    "code": "123352",
    "name": "Junior Glenn Deal",
    "sex": "M",
    "born": "6 Jun 1945",
    "spouses": [{"name": "Carol Vivian Moyers", "born": "30 May 1947", "married": "29 Jul 1965"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 85},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1233521", "name": "Judith Deal", "born": "20 Feb 1966", "verified_terminal": True},
        {"code": "1233522", "name": "Dennis Lee Deal", "born": "23 May 1977", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "123381",
    "name": "Paul Franklin Deal",
    "sex": "M",
    "born": "30 May 1947",
    "spouses": [{"name": "Bonita Joy Chidester", "born": "30 Nov 1946", "married": "2 Sep 1967"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 85},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1233811", "name": "Beverly Ann Deal", "born": "25 Mar 1969", "verified_terminal": True},
        {"code": "1233812", "name": "Sherilyn Kay Deal", "born": "29 Sep 1972", "verified_terminal": True},
        {"code": "1233813", "name": "Joy Christine Deal", "born": "27 Mar 1975", "verified_terminal": True},
        {"code": "1233814", "name": "Janette Marie Deal", "born": "23 Nov 1976", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "123382",
    "name": "Larry Guy Deal",
    "sex": "M",
    "born": "17 Jun 1949",
    "spouses": [{"name": "Patricia Ann Lyons", "born": "15 Apr 1951", "married": "31 Jul 1971"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 85},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1233821", "name": "Anthony Glenn Deal", "born": "2 Jun 1972", "verified_terminal": True},
        {"code": "1233822", "name": "Brian Duane Deal", "born": "16 Jun 1977", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "123384",
    "name": "Kay Marlene Deal",
    "sex": "F",
    "born": "6 Jun 1958",
    "spouses": [{"name": "David Gail Golden", "born": "27 Jun 1956", "married": "22 Oct 1976"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 85},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1233841", "name": "Hope Renee Golden", "born": "14 Jun 1977", "verified_terminal": True},
        {"code": "1233842", "name": "Samuel Ray Golden", "born": "6 Dec 1978", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "123422",
    "name": "Patricia Lee Kotchek",
    "sex": "F",
    "born": "9 Jun 1949",
    "spouses": [{"name": "Michael S. Buric", "born": "14 May 1950", "married": "30 Dec 1976"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 85},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1234221", "name": "Simon Andrew Buric", "born": "4 Aug 1984", "verified_terminal": True},
        {"code": "1234222", "name": "Ariel Elizabeth Buric", "born": "12 Sep 1988", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "123511",
    "name": "Lillian Ruth DeBerry",
    "sex": "F",
    "born": "11 Jan 1936",
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 85},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1235111", "name": "Lisa Dawn DeBerry", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "123512",
    "name": "Janet Sue DeBerry",
    "sex": "F",
    "spouses": [{"name": "Samuel Robert Casteel"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 85},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1235121", "name": "Laura Sue Casteel", "verified_terminal": True},
        {"code": "1235122", "name": "Samuel Robert Casteel, Jr.", "verified_terminal": True},
        {"code": "1235123", "name": "Pamela Casteel", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "123513",
    "name": "Nancy Kay DeBerry",
    "sex": "F",
    "spouses": [{"name": "Edward Spencer"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 85},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1235131", "name": "Anita Spencer", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "123515",
    "name": "Don Everett DeBerry",
    "sex": "M",
    "born": "11 May 1946",
    "spouses": [{"name": "Lorriane Miller"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 85},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1235151", "name": "Michael Ernest DeBerry", "verified_terminal": True},
        {"code": "1235152", "name": "Travis", "flags": {"stepChild": True}, "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "123516",
    "name": "Karen Diane DeBerry",
    "sex": "F",
    "spouses": [{"name": "Samuel Post"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 85},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1235161", "name": "Sheri Post", "verified_terminal": True},
        {"code": "1235162", "name": "Samuel Post, Jr.", "verified_terminal": True},
    ],
})


# === Pages 86-90 vision pass (2026-06-07): DeBerry/Feather/Guthrie/Lawson/Shafer gen 7/8 ===
ENTRIES.append({
    "code": "123517",
    "name": "Duane Chester DeBerry",
    "sex": "M",
    "spouses": [
        {"name": "Evelyn Stiles", "order": 1},
        {"name": "Brenda Smith", "order": 2},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 86},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1235171", "name": "Rachel DeBerry", "verified_terminal": True},
        {"code": "1235172", "name": "Tracy DeBerry", "verified_terminal": True},
        {"code": "1235173", "name": "Brian DeBerry", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "123518",
    "name": "Rita Bevelyn DeBerry",
    "sex": "F",
    "spouses": [{"name": "Michael Fay"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 86},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1235181", "name": "Deija Fay", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "123521",
    "name": "Ronald Prentice DeBerry",
    "sex": "M",
    "born": "29 Sep 1932",
    "spouses": [{"name": "Ruth Kelly", "born": "11 Dec 1933", "married": "6 Jun 1953"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 86},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1235211", "name": "Patrick Keith DeBerry", "born": "14 Sep 1954", "verified_terminal": True},
        {"code": "1235212", "name": "Michael Kelly DeBerry", "born": "8 Jan 1957", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "123611",
    "name": "Loren Dwight Wiles, Jr.",
    "sex": "M",
    "born": "1 Jul 1928",
    "spouses": [{"name": "Ruth Braham"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 86},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1236111", "name": "Loren Brent Wiles", "born": "12 Apr 1953", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "123612",
    "name": "Elizabeth Rosalie Wiles",
    "sex": "F",
    "born": "6 Jun 1933",
    "spouses": [{"name": "Kenneth Walter Friend"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 86},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1236121", "name": "Jay Allen Friend", "born": "26 Jul 1956", "verified_terminal": True},
        {"code": "1236122", "name": "Mark Todd Friend", "born": "27 Feb 1959", "verified_terminal": True},
        {"code": "1236123", "name": "Joe Beth Friend", "born": "28 Feb 1960", "verified_terminal": True},
        {"code": "1236124", "name": "Holly Denise Friend", "born": "26 Nov 1961", "verified_terminal": True},
        {"code": "1236125", "name": "Tamra Lynn Friend", "born": "23 Dec 1962", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "123631",
    "name": "Patricia Ann Shirley",
    "sex": "F",
    "born": "22 Nov 1936",
    "spouses": [{"name": "Robert Morgan Knight"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 86},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1236311", "name": "Kimberly Kay Knight", "born": "23 Feb 1958", "verified_terminal": True},
        {"code": "1236312", "name": "Robert Scott Knight", "born": "20 Aug 1961", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "123632",
    "name": "Elizabeth Sue Shirley",
    "sex": "F",
    "born": "14 Dec 1941",
    "spouses": [{"name": "Danny Lee Morris", "born": "Dec 1941"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 86},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1236321", "name": "Deanna Lee Morris", "born": "6 Nov 1973", "verified_terminal": True},
        {"code": "1236322", "name": "Tex Lambert Morris", "born": "21 Mar 1978", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "123641",
    "name": "William Edward Henry",
    "sex": "M",
    "born": "19 Jul 1942",
    "spouses": [{"name": "Helen Sue Mahaffee", "born": "3 Sep 1943"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 86},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1236411", "name": "Amy Colleen Henry", "born": "8 May 1963", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "123642",
    "name": "Sharon Kay Henry",
    "sex": "F",
    "born": "13 Dec 1946",
    "spouses": [{"name": "Patrick McCormley", "born": "10 Aug 1943"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 86},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1236421", "name": "Melanie Christena McCormley", "born": "28 Oct 1971", "verified_terminal": True},
        {"code": "1236422", "name": "Daniel Zachary McCormley", "born": "3 Feb 1978", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "123651",
    "name": "Robert Lynn Feather",
    "sex": "M",
    "born": "17 Dec 1945",
    "spouses": [
        {"name": "Cathy Hoffman", "order": 1},
        {"name": "Lelia Lowe", "order": 2},
        {"name": "Jerri Frankhouser", "order": 3},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 87},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1236511", "name": "Wendy Feather", "born": "1965", "verified_terminal": True},
        {"code": "1236512", "name": "Robbie Lynn Feather", "born": "9 Oct 1968", "verified_terminal": True},
        {"code": "1236513", "name": "Season Feather", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "123652",
    "name": "Mary Ann Feather",
    "sex": "F",
    "born": "30 May 1947",
    "spouses": [{"name": "Richard Lee McCabe", "born": "22 Sep 1939", "married": "18 Jun 1967"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 87},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1236521", "name": "Richette Ann McCabe", "born": "10 Jun 1969", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "123653",
    "name": "Ella Lee Feather",
    "sex": "F",
    "born": "7 Sep 1949",
    "spouses": [{"name": "Stanley Ward Livengood", "born": "18 Aug 1943", "married": "24 Aug 1968"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 87},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1236531", "name": "Stoney Lee Livengood", "born": "24 Jun 1969", "verified_terminal": True},
        {"code": "1236532", "name": "Ralph Scott Livengood", "born": "3 Nov 1970", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "123654",
    "name": "Linda Joy Feather",
    "sex": "F",
    "born": "27 May 1951",
    "spouses": [{"name": "Max Fries Elliott", "born": "20 May 1951", "married": "24 Jun 1971"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 87},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1236541", "name": "Trampas J. Elliott", "born": "11 Jan 1973", "verified_terminal": True},
        {"code": "1236542", "name": "Cody D. Elliott", "born": "6 Mar 1975", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "123713",
    "name": "Marion Fay Miller",
    "sex": "F",
    "born": "29 Apr 1945",
    "spouses": [{"name": "Joseph Ronald Feather", "born": "8 Jun 1946", "married": "14 Feb 1970"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 87},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1237131", "name": "Veronica Joy Feather", "born": "10 Jun 1970", "died": "13 Jun 1970", "flags": {"diedInInfancy": True}, "verified_terminal": True},
        {"code": "1237132", "name": "Lesa Jean Feather", "born": "19 Jul 1972", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "132121",
    "name": "Mary Ann Guthrie",
    "sex": "F",
    "born": "1937",
    "spouses": [{"name": "Kenneth Frazee"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 87},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1321211", "name": "Kenneth Frazee, Jr.", "born": "1958"},
        {"code": "1321212", "name": "Eddie Frazee", "born": "1960"},
        {"code": "1321213", "name": "Randy Frazee", "born": "5 Oct 1962", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "132141",
    "name": "Candice Rae Guthrie",
    "sex": "F",
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 87},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1321411", "name": "Laura Kay Guthrie", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "132151",
    "name": "Ruth Myers",
    "sex": "F",
    "spouses": [{"name": "Maraio"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 87},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1321511", "name": "Wesley Myers", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "132152",
    "name": "Sandy Myers",
    "sex": "F",
    "spouses": [{"name": "Elvin Conaway"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 87},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1321521", "name": "Melissa Myers Conaway", "born": "27 Aug 1971", "verified_terminal": True},
        {"code": "1321522", "name": "Willis S. Conaway", "verified_terminal": True},
        {"code": "1321523", "name": "Wendy Conaway", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "132154",
    "name": "Vickey Myers",
    "sex": "F",
    "spouses": [{"name": "Martinko"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 87},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1321541", "name": "A daughter", "born": "Nov 1972", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "132157",
    "name": "Marlene Margaret Myers",
    "sex": "F",
    "spouses": [{"name": "Roger Lee Cupp", "born": "13 Mar 1955", "married": "3 Jul 1976", "details": "Same as #13F722."}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 88},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1321571", "name": "Erica Marie Myers", "born": "29 Jun 1971", "verified_terminal": True},
        {"code": "1321572", "name": "Meghan Cortney Cupp", "born": "26 Jun 1978", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "132171",
    "name": "Debra Joyce Deal",
    "sex": "F",
    "born": "27 Feb 1959",
    "spouses": [{"name": "Ronald Edward Shafer", "born": "11 Jan 1961", "married": "21 Jul 1979", "details": "Same as #13651A4."}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 88},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1321711", "name": "Shawn Edward Shafer", "born": "18 May 1980", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "132172",
    "name": "Pamela Deal",
    "sex": "F",
    "spouses": [{"name": "Glenn Dwain Walls, Jr.", "married": "1976"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 88},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1321721", "name": "Tammy Marie Walls", "born": "8 Feb 1982", "verified_terminal": True},
        {"code": "1321722", "name": "Brittany Eletta Walls", "born": "21 Jul 1988", "verified_terminal": True},
        {"code": "1321723", "name": "Glen Dwain Walls III", "born": "2 Apr 1990", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "132173",
    "name": "Randy Paul Deal",
    "sex": "M",
    "born": "7 Feb 1962",
    "spouses": [{"name": "Patricia Haselue", "married": "6 Mar 1981"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 88},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1321731", "name": "Bradley Paul Deal", "born": "29 Mar 1981", "verified_terminal": True},
        {"code": "1321132", "name": "Randi Lee Deal", "born": "17 Feb 1984", "verified_terminal": True},
        {"code": "1321733", "name": "Rusty Ray Deal", "born": "1 Aug 1985", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "132174",
    "name": "Michael (Mike) Ray Deal",
    "sex": "M",
    "born": "25 May 1963",
    "spouses": [{"name": "Nancy Rosenberger", "born": "5 May 1970", "married": "17 Jun 1988"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 88},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1321741", "name": "Nicole Deal", "born": "13 Jan 1989", "verified_terminal": True},
        {"code": "1321742", "name": "Trisha Deal", "born": "26 Apr 1990", "verified_terminal": True},
        {"code": "1321743", "name": "Michael Ray Deal, Jr.", "born": "18 Jun 1991", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "132182",
    "name": "Tamara Lynn Smith",
    "sex": "F",
    "born": "24 Dec 1966",
    "spouses": [{"name": "Richard Wittman", "married": "1 Apr 1989"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 88},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1321821", "name": "Joseph Wittman", "born": "Nov 1992", "verified_terminal": True},
        {"code": "1321822", "name": "Raellen Wittman", "born": "Nov 1995", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "132221",
    "name": "Geraldine Rita Strawser",
    "sex": "F",
    "born": "29 May 1927",
    "spouses": [{"name": "Rudolph Havrilla, Jr.", "born": "1 Jan 1927"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 88},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1322211", "name": "Debra Havrilla", "born": "24 May 1951", "verified_terminal": True},
        {"code": "1322212", "name": "Diana Havrilla", "born": "6 Mar 1954", "verified_terminal": True},
        {"code": "1322213", "name": "Timothy Havrilla", "born": "19 Dec 1962", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "132233",
    "name": "Audrey Jean Guthrie",
    "sex": "F",
    "born": "20 Dec 1937",
    "spouses": [{"name": "Clarence Savage, Jr.", "married": "11 Oct 1958"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 88},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1322331", "name": "Eddie Savage", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "132234",
    "name": "Wendell Ray Guthrie",
    "sex": "M",
    "born": "21 Sep 1940",
    "spouses": [{"name": "Helen Adelia Kelley", "born": "2 Jan 1938", "married": "27 May 1961"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 88},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1322341", "name": "Infant", "flags": {"diedInInfancy": True}, "verified_terminal": True},
        {"code": "1322342", "name": "Denzel Ray Guthrie", "born": "22 Sep 1962"},
        {"code": "1322343", "name": "Denise Rene Guthrie", "born": "22 Sep 1962"},
        {"code": "1322344", "name": "Dana Len Guthrie", "born": "14 Jan 1968", "died": "1 Feb 1968", "flags": {"diedInInfancy": True}, "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "132611",
    "name": "Donley Blaine Lawson",
    "sex": "M",
    "born": "18 Mar 1928",
    "spouses": [
        {"name": "Norma Friend", "born": "26 Feb 1930", "order": 1},
        {"name": "Cathy Voyten", "order": 2},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 89},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1326111", "name": "Dawn Lawson", "born": "9 Jan 1948"},
        {"code": "1326112", "name": "Kerry Blaine Lawson", "born": "22 Apr 1949"},
        {"code": "1326113", "name": "Leah Lawson", "born": "17 Jun 1950"},
        {"code": "1326114", "name": "Nina Lawson", "born": "28 Jan 1953"},
        {"code": "1326115", "name": "Rena Mae Lawson", "born": "14 Oct 1968", "verified_terminal": True},
        {"code": "1326116", "name": "Sherry Lawson", "flags": {"adopted": True}, "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "132612",
    "name": "Gayle Owens Lawson",
    "sex": "F",
    "born": "9 Oct 1930",
    "spouses": [{"name": "Betty Jane Rudd", "born": "6 Sep 1929", "married": "16 Feb 1948"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 89},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1326121", "name": "Larry Owens Larson", "born": "28 Aug 1948"},
    ],
})

ENTRIES.append({
    "code": "132613",
    "name": "Wahneta Jean Lawson",
    "sex": "F",
    "born": "11 Jun 1935",
    "spouses": [{"name": "Mervin Wade Friend", "born": "21 Mar 1931"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 89},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1326131", "name": "Sandi Frend", "born": "13 May 1952"},
    ],
})

ENTRIES.append({
    "code": "132614",
    "name": "Chester Kent Lawson",
    "sex": "M",
    "born": "20 Nov 1949",
    "died": "20 Jul 1994",
    "spouses": [{"name": "Patrica Betty Armstrong", "born": "17 Nov 1951", "married": "28 May 1972"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 89},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1326141", "name": "Shawn Lawson", "born": "5 Sep 1973", "verified_terminal": True},
        {"code": "1326142", "name": "Tonya Marie Lawson", "born": "4 Oct 1975"},
    ],
})

ENTRIES.append({
    "code": "132622",
    "name": "Caroline Lawson",
    "sex": "F",
    "spouses": [{"name": "Lee Butcher"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 89},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1326221", "name": "Lace Ann Butcher", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "132623",
    "name": "Greg Lawson",
    "sex": "M",
    "spouses": [{"name": "Fay Attenucio"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 89},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1326231", "name": "Katrina Lawson", "verified_terminal": True},
        {"code": "1326232", "name": "Christina Lawson", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "132624",
    "name": "David Lawson",
    "sex": "M",
    "spouses": [{"name": "Lila Miller"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 89},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1326241", "name": "Alice Kay Lawson", "born": "about 1975", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "132641",
    "name": "Thomas Robert (Bobby) Lawson",
    "sex": "M",
    "spouses": [{"name": "Annabelle Sypolt"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 89},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1326411", "name": "Michael Lyn Lawson", "verified_terminal": True},
        {"code": "1326412", "name": "Bradley Lawson", "verified_terminal": True},
        {"code": "1326413", "name": "Marlin Robert Lawson", "born": "25 Oct 1954"},
        {"code": "1326414", "name": "Linda Lawson", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "132642",
    "name": "Jackson Paul Lawson",
    "sex": "M",
    "born": "29 Oct 1934",
    "spouses": [{"name": "Shirley Katherine Reckart", "born": "1940", "married": "8 Jun 1957"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 89},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1326421", "name": "Steven Lynn Lawson", "born": "27 Jan 1959", "verified_terminal": True},
        {"code": "1326422", "name": "Christa Lynnette Lawson", "born": "17 Jul 1971", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "136511",
    "name": "Alva Lester Shafer",
    "sex": "M",
    "born": "26 Dec 1917",
    "spouses": [{"name": "Virginia Alice Guseman", "born": "9 Apr 1919", "married": "19 Jun 1941"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 90},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1365111", "name": "Judith Ann Shafer", "born": "29 Jan 1942"},
        {"code": "1365112", "name": "Janet Louise Shafer", "born": "12 Jun 1943"},
        {"code": "1365113", "name": "James Harold Shafer", "born": "9 Mar 1946"},
        {"code": "1365114", "name": "Infant", "born": "30 Jan 1947", "died": "30 Jan 1947", "flags": {"diedInInfancy": True}, "verified_terminal": True},
        {"code": "1365115", "name": "Emily Ruth Shafer", "born": "20 Jan 1948", "verified_terminal": True},
        {"code": "1365116", "name": "Margaret Jane Shafer", "born": "5 Jan 1949"},
        {"code": "1365117", "name": "Robert Gay Shafer", "born": "3 Nov 1950"},
        {"code": "1365118", "name": "Mary Alice Shafer", "born": "1 Jul 1952"},
        {"code": "1365119", "name": "Linda June Shafer", "born": "1 Jun 1953"},
    ],
})

ENTRIES.append({
    "code": "136512",
    "name": "Glenna Adra Shafer",
    "sex": "F",
    "born": "24 Feb 1919",
    "spouses": [{"name": "David Hershell McCarty", "born": "1 Oct 1913", "died": "13 Mar 1981", "married": "21 Nov 1945"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 90},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1365121", "name": "Wilma Ruth McCarty", "born": "7 Nov 1946"},
        {"code": "1365122", "name": "Ina Grace McCarty", "born": "21 Jun 1949"},
        {"code": "1365123", "name": "Charles Richard McCarty", "born": "8 Jun 1952"},
        {"code": "1365124", "name": "David Ward McCarty", "born": "20 Sep 1958"},
    ],
})

ENTRIES.append({
    "code": "136513",
    "name": "Thelma Maxine Shafer",
    "sex": "F",
    "born": "18 Dec 1920",
    "spouses": [{"name": "Hubert Martin Sisler", "born": "5 May 1916", "died": "24 Apr 1977", "married": "27 Apr 1940"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 90},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1365131", "name": "Rosella Grace Sisler", "born": "7 Aug 1941"},
        {"code": "1365132", "name": "Mary Ann Sisler", "born": "2 Sep 1943", "died": "3 Jul 1990", "verified_terminal": True},
        {"code": "1365133", "name": "Hubert Martin Sisler, Jr.", "born": "7 Mar 1958"},
    ],
})

ENTRIES.append({
    "code": "136514",
    "name": "Herbert David Shafer",
    "sex": "M",
    "born": "24 Feb 1922",
    "spouses": [{"name": "Vertrude Leah Thomas", "born": "25 May 1926", "married": "4 Sep 1943"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 90},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1365141", "name": "Vivian Leah Shafer", "born": "2 Nov 1946"},
        {"code": "1365142", "name": "Corel Elizabeth Shafer", "born": "15 Oct 1947", "verified_terminal": True},
        {"code": "1365143", "name": "Hannah Darlene Shafer", "born": "26 Jan 1953"},
    ],
})

ENTRIES.append({
    "code": "136515",
    "name": "Fredy Junior Shafer",
    "sex": "M",
    "born": "13 Mar 1924",
    "died": "17 Nov 1973",
    "spouses": [{"name": "Rita Torrissi", "born": "3 May 1930", "died": "13 Apr 1996", "married": "18 Dec 1948"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 90},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1365151", "name": "Dallas Basil Shafer", "born": "5 Mar 1951"},
        {"code": "1365152", "name": "Anthony Thomas Shafer", "born": "10 Mar 1952"},
        {"code": "1365153", "name": "Debra June Shafer", "born": "4 Jan 1955"},
        {"code": "1365154", "name": "Dennis Vaughn Shafer", "born": "26 Apr 1957", "died": "20 May 1957", "flags": {"diedInInfancy": True}, "verified_terminal": True},
        {"code": "1365155", "name": "Dessie Carmellia Shafer", "born": "10 Mar 1960"},
        {"code": "1365156", "name": "Amelia Jane Shafer", "born": "18 Mar 1961"},
        {"code": "1365157", "name": "Fredy Junior Shafer, Jr.", "born": "1 Nov 1962", "verified_terminal": True},
        {"code": "1365158", "name": "Franklin David Shafer", "born": "2 Feb 1959", "died": "2 Feb 1959", "flags": {"diedInInfancy": True}, "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "136516",
    "name": "Paul Eugene Shafer",
    "sex": "M",
    "born": "26 Feb 1926",
    "spouses": [{"name": "Mary Catherine Bellman", "born": "5 Jun 1931", "married": "5 Jun 1948"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 90},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1365161", "name": "Paula Jean Shafer", "born": "4 Jun 1949"},
        {"code": "1365162", "name": "George McKinley Shafer", "born": "23 Jul 1954"},
        {"code": "1365163", "name": "Kathy Lynn Shafer", "born": "11 Mar 1969", "verified_terminal": True},
    ],
})


# === Pages 91-95 vision pass (2026-06-07): Shafer/Wilburn/Teets/Seamon/Smith/Cupp/Thomas/Anderson gen 7/8 ===
ENTRIES.append({
    "code": "136517",
    "name": "Ada Mae Shafer",
    "sex": "F",
    "born": "18 Apr 1929",
    "spouses": [{"name": "Joseph J. Krimpel", "married": "27 Jun 1953"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 91},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1365171", "name": "Marshall William Eugene Krimpel", "born": "25 Jul 1945"},
        {"code": "1365172", "name": "Ronald Tracy Beam Krimpel", "born": "10 Feb 1947", "died": "16 May 1955", "flags": {"diedInInfancy": True}, "verified_terminal": True},
        {"code": "1365173", "name": "Kenneth Lawrence Krimpel", "born": "8 Aug 1949"},
        {"code": "1365174", "name": "Robert McKinley Krimpel", "born": "1 May 1951"},
        {"code": "1365175", "name": "Lathan Carr Krimpel", "born": "2 Aug 1952"},
        {"code": "1365176", "name": "Joseph J. Krimpel, Jr.", "born": "27 May 1954", "died": "28 May 1957", "flags": {"diedInInfancy": True}, "verified_terminal": True},
        {"code": "1365177", "name": "Alice Mae Krimpel", "born": "18 Nov 1956"},
        {"code": "1365178", "name": "Cheryl Leigh Krimpel", "born": "10 Jan 1968", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "136518",
    "name": "Walter Franklin Shafer",
    "sex": "M",
    "born": "27 Mar 1931",
    "spouses": [{"name": "Betty Jean Casteel", "born": "29 Jan 1935", "married": "13 Jul 1952"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 91},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1365181", "name": "Randy Lee Casteel", "born": "18 Sep 1956"},
        {"code": "1365182", "name": "William Hansel Shafer", "born": "22 Nov 1968", "verified_terminal": True},
        {"code": "1365183", "name": "Tracy Wade Shafer", "born": "29 Dec 1970", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "136519",
    "name": "Lou Anna Shafer",
    "sex": "F",
    "born": "19 Oct 1932",
    "spouses": [{"name": "Stanley Paul Sisler", "born": "6 Nov 1928", "married": "20 Feb 1948"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 91},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1365191", "name": "Roy Lee Sisler", "born": "21 Oct 1948"},
        {"code": "1365192", "name": "Richard David Sisler", "born": "17 Oct 1949"},
        {"code": "1365193", "name": "Adra Ann Sisler", "born": "2 Oct 1950"},
        {"code": "1365194", "name": "Linda Lou Sisler", "born": "13 Apr 1952"},
        {"code": "1365195", "name": "Jerry Lynn Sisler", "born": "10 Mar 1953", "died": "19 Jul 1953", "flags": {"diedInInfancy": True}, "verified_terminal": True},
        {"code": "1365196", "name": "Paul Edward Sisler", "born": "2 Jul 1956"},
    ],
})

ENTRIES.append({
    "code": "13651A",
    "name": "Olaf Hugh (Buddy) Shafer",
    "sex": "M",
    "born": "22 May 1934",
    "spouses": [{"name": "Helen Feather", "born": "29 Feb 1936", "died": "16 Apr 1990", "married": "4 Mar 1956"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 91},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "13651A1", "name": "Dwight Hugh Shafer", "born": "22 Oct 1956"},
        {"code": "13651A2", "name": "Olaf Dwayne Shafer", "born": "19 Sep 1957"},
        {"code": "13651A3", "name": "Donald Franklin Shafer", "born": "11 Jan 1961"},
        {"code": "13651A4", "name": "Ronald Edward Shafer", "born": "11 Jan 1961", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "13651B",
    "name": "Martha Elizabeth Shafer",
    "sex": "F",
    "born": "7 Sep 1936",
    "spouses": [{"name": "James I. Smith", "married": "27 Aug 1954"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 91},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "13651B1", "name": "Elizabeth Ann Smith", "born": "2 May 1955", "verified_terminal": True},
        {"code": "13651B2", "name": "Jr. Smith", "born": "Mar 1960", "verified_terminal": True},
        {"code": "13651B3", "name": "Ca Smith", "born": "Jan 1962", "verified_terminal": True},
        {"code": "13651B4", "name": "Paula Sue Smith", "born": "Jul 1964", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "13651C",
    "name": "Russell Lee Shafer",
    "sex": "M",
    "born": "7 Sep 1939",
    "spouses": [
        {"name": "Doris Sann", "born": "19 Aug 1939", "order": 1},
        {"name": "Mary Francis Redmond", "born": "25 Oct 1961", "married": "31 Dec 1978", "order": 2},
        {"name": "Christina Greene", "order": 3},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 91},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "13651C1", "name": "Monika Crystal Shafer", "born": "12 Mar 1960"},
        {"code": "13651C2", "name": "Anita Marie Shafer", "born": "5 Feb 1961"},
        {"code": "13651C3", "name": "Frank McKinley Shafer", "born": "7 Oct 1962"},
        {"code": "13651C4", "name": "Allen Lee Shafer"},
        {"code": "13651C5", "name": "Jerry Joe Shafer", "born": "2 Feb 1966", "verified_terminal": True},
        {"code": "13651C6", "name": "Karen Marie Shafer", "born": "17 Apr 1972", "verified_terminal": True},
        {"code": "13651C7", "name": "Alisa Marie Shafer", "born": "21 Jan 1980", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "138211",
    "name": "Wayne Wilburn",
    "sex": "M",
    "born": "2 Feb 1917",
    "died": "3 Dec 1979",
    "spouses": [{"name": "Arlene Mock"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 92},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1382111", "name": "David Michael Wilburn", "born": "4 Dec 1955", "verified_terminal": True},
        {"code": "1382112", "name": "William Lee Wilburn", "born": "3 Dec 1960", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "138212",
    "name": "Eleanor Virginia Wilburn",
    "sex": "F",
    "spouses": [{"name": "Stanley A. Ringer", "born": "22 May 1917", "died": "27 Aug 1971"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 92},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1382121", "name": "Paul Michael Sisler", "flags": {"stepChild": True}, "verified_terminal": True},
        {"code": "1382122", "name": "Donald Ringer", "verified_terminal": True},
        {"code": "1382123", "name": "Susan Ringer", "verified_terminal": True},
        {"code": "1382124", "name": "Son", "verified_terminal": True},
        {"code": "1382125", "name": "Son", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "138274",
    "name": "Clarence Cecil Teets",
    "sex": "M",
    "born": "24 Oct 1947",
    "spouses": [{"name": "Judy Diane Fike", "married": "26 Oct 1968"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 92},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1382741", "name": "Jeffery Bruce Teets", "born": "25 Jan 1975"},
        {"code": "1382742", "name": "Andrew Teets", "born": "17 Feb 1983", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "138275",
    "name": "Rollin Eugene Teets",
    "sex": "M",
    "born": "16 Jan 1951",
    "spouses": [{"name": "Ronna June Forman", "born": "29 Jun 1952", "married": "10 Apr 1971"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 92},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1382751", "name": "Kristie Lynn Teets", "born": "9 Oct 1972", "verified_terminal": True},
        {"code": "1382752", "name": "Pamela Teets", "born": "1977", "died": "14 Apr 1977", "flags": {"diedInInfancy": True}, "verified_terminal": True},
        {"code": "1382753", "name": "Amy Teets", "born": "28 Mar 1978", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "138276",
    "name": "Allen Ray Teets",
    "sex": "M",
    "born": "7 Feb 1960",
    "spouses": [
        {"name": "Nancy Lee Uphold", "born": "1960", "married": "8 Jan 1978", "order": 1},
        {"name": "Pamela Louise Benson", "born": "23 Nov 1967", "married": "12 Jun 1986", "order": 2},
        {"name": "Kristy Lynn Harris", "born": "1965", "married": "1996", "order": 3},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 92},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1382761", "name": "Jeremy Allen Teets", "born": "27 Aug 1978", "verified_terminal": True},
        {"code": "1382762", "name": "Katie Lynn Jackenheimer", "born": "1 Apr 1987", "flags": {"stepChild": True}, "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "138445",
    "name": "Shirley Johnson",
    "sex": "F",
    "spouses": [{"name": "Philips", "died": "1975"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 92},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1384451", "name": "Melisha Philips", "born": "10 Dec 1971", "verified_terminal": True},
        {"code": "1384452", "name": "Machella Philips", "born": "Jul 1968", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "138641",
    "name": "Vernon Rodeheaver",
    "sex": "M",
    "spouses": [{"name": "Christine McDougle"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 92},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1386411", "name": "Nancy Rodeheaver", "verified_terminal": True},
        {"code": "1386412", "name": "Rita Rodeheaver", "verified_terminal": True},
        {"code": "1386413", "name": "Thomas Rodeheaver", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "138642",
    "name": "Mildred Rodeheaver",
    "sex": "F",
    "spouses": [{"name": "Ward Sisler", "died": "Jun 1976"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 92},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1386421", "name": "Patty Sisler", "verified_terminal": True},
        {"code": "1386422", "name": "Sandra Sisler", "verified_terminal": True},
        {"code": "1386423", "name": "Jane Sisler", "verified_terminal": True},
        {"code": "1386424", "name": "Sharen Sisler", "verified_terminal": True},
        {"code": "1386425", "name": "Brenda Sisler", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "13B211",
    "name": "Freda Agnes Seamon",
    "sex": "F",
    "born": "10 Apr 1923",
    "spouses": [{"name": "William Lee Sines", "born": "27 Feb 1922", "married": "13 Aug 1945"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 93},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "13B2111", "name": "Gary Seamon", "born": "16 Apr 1942", "verified_terminal": True},
        {"code": "13B2112", "name": "William Ronald Sines", "born": "26 Jul 1946"},
        {"code": "13B2113", "name": "Rita Lynn Sines", "born": "10 Sep 1949"},
        {"code": "13B2114", "name": "Thomas Eugene Sines", "born": "1 Aug 1951", "verified_terminal": True},
        {"code": "13B2115", "name": "Cathy Ann Sines", "born": "22 Dec 1952"},
    ],
})

ENTRIES.append({
    "code": "13B212",
    "name": "Charles Joseph Seamon",
    "sex": "M",
    "born": "18 Mar 1925",
    "spouses": [{"name": "Janice Ruth Rauenswinter", "born": "18 Dec 1930", "married": "1 Jan 1955"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 93},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "13B2121", "name": "Sharon Ruth Seamon", "born": "24 Oct 1950", "verified_terminal": True},
        {"code": "13B2122", "name": "Robert Scott Seamon", "born": "25 Apr 1955", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "13B213",
    "name": "Mildred Elizabeth Seamon",
    "sex": "F",
    "born": "11 Feb 1929",
    "spouses": [{"name": "Joseph J. Abbey", "born": "8 May 1925", "married": "14 Sep 1948"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 93},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "13B2131", "name": "Joseph J. Abbey, Jr.", "born": "21 Jul 1949", "died": "16 Apr 1967", "verified_terminal": True},
        {"code": "13B2132", "name": "Richard Allen Abbey", "born": "22 Oct 1950", "verified_terminal": True},
        {"code": "13B2133", "name": "Melva Susan Abbey", "born": "26 Dec 1953"},
        {"code": "13B2134", "name": "Carol Lee Abbey", "born": "27 Jul 1955", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "13B214",
    "name": "Oliver George Seamon",
    "sex": "M",
    "born": "15 Dec 1930",
    "spouses": [{"name": "June McMillian", "born": "30 Dec", "married": "1954"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 93},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "13B2141", "name": "Gregory McMillian Seamon", "born": "7 Jun 1955"},
        {"code": "13B2142", "name": "Randy Allen Seamon", "born": "18 Jan 1960", "verified_terminal": True},
        {"code": "13B2143", "name": "Timothy Brian Seamon", "born": "26 Jul 1962", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "13B215",
    "name": "Carl Steven Seamon",
    "sex": "M",
    "born": "4 Mar 1933",
    "spouses": [{"name": "Nancy Lois Edmundston", "born": "23 Apr 1938", "married": "5 Dec 1958"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 93},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "13B2151", "name": "Edward Lee Seamon", "born": "11 Jan 1960"},
        {"code": "13B2152", "name": "Michael Steven Seamon", "born": "4 Oct 1962", "verified_terminal": True},
        {"code": "13B2153", "name": "Tracy Ann Seamon", "born": "10 Apr 1966", "verified_terminal": True},
        {"code": "13B2154", "name": "Eric Donald Seamon", "born": "10 Jul 1970"},
    ],
})

ENTRIES.append({
    "code": "13C511",
    "name": "Darwin Wayne Smith",
    "sex": "M",
    "born": "17 May 1943",
    "spouses": [
        {"name": "Teressa Bucklew", "order": 1},
        {"name": "Edma Edelberg", "born": "29 Apr 1948", "married": "29 Mar 1989", "order": 2},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 93},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "13C5111", "name": "Steven W. Smith", "born": "16 Jul 1964", "verified_terminal": True},
        {"code": "13C5112", "name": "Allen D. Smith", "born": "19 Jun 1966"},
        {"code": "13C5113", "name": "James F. Smith", "born": "17 Jan 1968", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "13C512",
    "name": "Gary Ray Smith",
    "sex": "M",
    "born": "21 Jan 1945",
    "spouses": [{"name": "Connie Ellen Guthrie", "born": "1 Oct 1944", "married": "12 Oct 1962", "details": "Same as #13218."}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 93},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": "Children cross-coded 132181-132183."},
})

ENTRIES.append({
    "code": "13C513",
    "name": "James Ward Smith",
    "sex": "M",
    "born": "14 Mar 1949",
    "spouses": [{"name": "Kay Hevner"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 93},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "13C5131", "name": "Tricia Marie Smith", "born": "16 Jan 1977", "verified_terminal": True},
        {"code": "13C5132", "name": "Kenneth Smith", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "13C514",
    "name": "Stanley Aldren Smith",
    "sex": "M",
    "born": "3 Nov 1955",
    "spouses": [{"name": "Carolyn"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 94},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "13C5141", "name": "Jennifer Smith", "verified_terminal": True},
        {"code": "13C5142", "name": "Dana Smith", "born": "10 Mar", "verified_terminal": True},
        {"code": "13C5143", "name": "Stwart Smith", "born": "18 Dec", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "13C515",
    "name": "Connie Smith",
    "sex": "F",
    "born": "10 Feb 1959",
    "spouses": [{"name": "Richard Kyle"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 94},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "13C5151", "name": "Zack Kyle", "born": "30 May 1982", "verified_terminal": True},
        {"code": "13C5152", "name": "Nick Kyle", "born": "1 Aug", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "13F711",
    "name": "Linda Ray Rishel",
    "sex": "F",
    "born": "11 Mar 1950",
    "spouses": [
        {"name": "Roy Stanton", "born": "1943", "order": 1},
        {"name": "George Hardesty", "order": 2},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 94},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "13F7111", "name": "Donald Ray Stanton", "born": "4 Dec 1967", "verified_terminal": True},
        {"code": "13F7112", "name": "Loretta Stanton", "born": "7 Dec 1970", "verified_terminal": True},
        {"code": "13F7113", "name": "Renna Stanton", "born": "2 Jun 1972", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "13F712",
    "name": "Ward Ray Thomas",
    "sex": "M",
    "born": "2 Sep 1954",
    "spouses": [{"name": "Joyce Savage", "born": "15 Jul 1961", "married": "9 Oct 1982"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 94},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "13F7121", "name": "Jay Lynn Thomas", "born": "8 Apr 1981", "verified_terminal": True},
        {"code": "13F7122", "name": "Ward Ray Thomas, Jr.", "born": "12 Jan 1983", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "13F713",
    "name": "Crystel Lou Thomas",
    "sex": "F",
    "born": "8 Dec 1961",
    "spouses": [{"name": "Gary Savage"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 94},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "13F7131", "name": "Gary Edward (Jake) Savage", "born": "17 Jul 1980", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "13F715",
    "name": "Henry Thomas",
    "sex": "M",
    "born": "20 Mar 1969",
    "spouses": [{"name": "Sherrie Jones"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 94},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "13F7151", "name": "Branden Lee Jones", "born": "Sep 1990", "verified_terminal": True},
        {"code": "13F7152", "name": "Heather Lynn Jones", "born": "1 May 1992", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "13F721",
    "name": "Martin Edward Cupp",
    "sex": "M",
    "born": "30 Dec 1953",
    "spouses": [
        {"name": "Darlene Louise Moyers", "born": "24 Feb 1959", "married": "7 Jul 1979", "order": 1},
        {"name": "Joyce Casteel", "order": 2},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 94},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "13F7211", "name": "Kevin Murphy", "flags": {"stepChild": True}, "verified_terminal": True},
        {"code": "13F7212", "name": "Michelle Cupp", "flags": {"adopted": True}, "verified_terminal": True},
        {"code": "13F7213", "name": "Harold Cupp", "flags": {"adopted": True}, "verified_terminal": True},
        {"code": "13F7214", "name": "Cortney Cupp", "flags": {"adopted": True}, "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "13F722",
    "name": "Roger Lee Cupp",
    "sex": "M",
    "born": "13 Mar 1955",
    "spouses": [{"name": "Marlene Margaret Myers", "married": "3 Jul 1976", "details": "Same as #132157."}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 94},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": "Children cross-coded 1321571-2."},
})

ENTRIES.append({
    "code": "13F724",
    "name": "Marvin Dale Cupp",
    "sex": "M",
    "born": "18 Dec 1959",
    "spouses": [{"name": "Carmen Michelle Reckart", "born": "2 Apr 1962", "married": "4 Mar 1985"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 94},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "13F7241", "name": "Nathan Dale Cupp", "born": "4 Oct 1980", "verified_terminal": True},
        {"code": "13F7242", "name": "Shelby Elizabeth Cupp", "born": "9 Oct 1991", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "13F725",
    "name": "Charles Wesley Cupp",
    "sex": "M",
    "born": "13 Jul 1961",
    "spouses": [{"name": "Dolly Varndell"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 95},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "13F7251", "name": "Cristina Marie Cupp", "verified_terminal": True},
        {"code": "13F7252", "name": "Tracy Varndell", "flags": {"stepChild": True}, "verified_terminal": True},
        {"code": "13F7253", "name": "Thomas (Tommy) Varndell", "flags": {"stepChild": True}, "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "13F726",
    "name": "Richard Glenn Cupp",
    "sex": "M",
    "born": "17 Sep 1963",
    "spouses": [{"name": "Donna Casteel"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 95},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "13F7261", "name": "Christopher Glenn Cupp", "verified_terminal": True},
        {"code": "13F7262", "name": "Amy Lynn Cupp", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "13F727",
    "name": "Sharon Louise Cupp",
    "sex": "F",
    "born": "12 Dec 1965",
    "spouses": [
        {"name": "Adam Franklin Reckart", "born": "18 Oct 1962", "order": 1},
        {"name": "Donald Everly", "married": "28 May 1994", "order": 2},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 95},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "13F7271", "name": "Jennifer Dawn Cupp", "born": "8 Mar 1979", "verified_terminal": True},
        {"code": "13F7272", "name": "Tiffany Jo Reckart", "born": "11 May 1983", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "13F741",
    "name": "Anna Pearl Thomas",
    "sex": "F",
    "born": "5 May 1958",
    "spouses": [{"name": "Gary Spreng", "born": "12 Nov 1947", "married": "4 Jul 1981"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 95},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "13F7411", "name": "Angela Virginia Spreng", "born": "22 Jun 1978"},
        {"code": "13F7412", "name": "Melissa Spreng", "born": "5 Mar 1983", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "13F742",
    "name": "James Franklin Thomas",
    "sex": "M",
    "born": "21 Jun 1960",
    "spouses": [{"name": "Kimberly Romes", "married": "14 Feb 1981"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 95},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "13F7421", "name": "Hillary Thomas", "born": "29 Sep 1985", "verified_terminal": True},
        {"code": "13F7422", "name": "Vranna Thomas", "born": "30 Apr 1994", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "13F752",
    "name": "Peggy Sue Rosier",
    "sex": "F",
    "born": "2 Feb 1962",
    "spouses": [{"name": "Haller"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 95},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "13F7521", "name": "Jamnis Haller", "verified_terminal": True},
        {"code": "13F7522", "name": "Randy Haller", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "13FD21",
    "name": "Tammy Silbaugh",
    "sex": "F",
    "born": "9 Sep 1961",
    "spouses": [{"name": "Bradley Eugene Summers", "born": "26 Mar 1957", "married": "3 Jan 1983"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 95},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "13FD211", "name": "Nicki Lynn Summers", "born": "23 Mar 1983", "verified_terminal": True},
        {"code": "13FD212", "name": "Vicki Lee Summers", "born": "23 Mar 1983", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "141511",
    "name": "Janet P. Anderson",
    "sex": "F",
    "born": "4 May 1935",
    "died": "1 Sep 1964",
    "spouses": [{"name": "Robert Maxwell", "born": "26 Oct 1921", "married": "14 Dec 1957"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 95},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1415111", "name": "Susan Maxwell", "born": "30 Sep 1961", "verified_terminal": True},
        {"code": "1415112", "name": "Robert Rathvon Maxwell, II", "born": "4 Oct 1964", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "141513",
    "name": "Clyde Lloyd Anderson",
    "sex": "M",
    "born": "11 Aug 1937",
    "spouses": [{"name": "Rachel Shields Butcher", "born": "7 Oct 1936", "married": "26 Jan 1965"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 95},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1415131", "name": "Michael Butcher", "born": "17 Jan 1955", "verified_terminal": True},
        {"code": "1415132", "name": "Mark Butcher", "born": "1 Nov 1957", "verified_terminal": True},
        {"code": "1415133", "name": "Stephan Butcher", "born": "8 Jan 1959", "verified_terminal": True},
        {"code": "1415134", "name": "John Butcher", "born": "4 Sep 1960", "verified_terminal": True},
    ],
})


# === Pages 96-100 vision pass (2026-06-07): Anderson/Uphold/Jones/Nicola/Sines/Sisler/Frazee gen 8 ===
ENTRIES.append({
    "code": "141514",
    "name": "Charles Robert Anderson",
    "sex": "M",
    "born": "8 Jan 1939",
    "spouses": [{"name": "Julia K. Zsiros", "born": "29 Sep 1939", "married": "29 Aug 1964"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 96},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1415141", "name": "Amy Lynn Anderson", "born": "21 Jun 1966", "verified_terminal": True},
        {"code": "1415142", "name": "Charles R. Anderson", "born": "16 Apr 1969", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "141531",
    "name": "Ronald D. Uphold",
    "sex": "M",
    "born": "22 Sep 1938",
    "spouses": [{"name": "Sandra", "married": "Aug 1960"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 96},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1415311", "name": "Cheryl Uphold", "born": "27 Jan 1961", "verified_terminal": True},
        {"code": "1415312", "name": "Brenda Uphold", "born": "24 Feb 1963", "verified_terminal": True},
        {"code": "1415313", "name": "Donald Uphold", "born": "5 Nov 1966", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "141541",
    "name": "Robert E. Jones, Jr.",
    "sex": "M",
    "born": "4 Apr 1940",
    "spouses": [
        {"name": "Carol Robinson", "born": "3 Feb 1938", "married": "14 Feb 1964", "order": 1},
        {"name": "Mary Ellen Helmick", "born": "16 Sep 1948", "married": "May 1979", "order": 2},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 96},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1415411", "name": "Scott Jones", "born": "23 Nov 1960", "verified_terminal": True},
        {"code": "1415412", "name": "Marti Jones", "born": "18 Nov 1964", "died": "19 Nov 1969", "flags": {"diedInInfancy": True}, "verified_terminal": True},
        {"code": "1415413", "name": "Robert E. Jones III", "born": "5 Feb 1980", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "141552",
    "name": "Bonnie Lynn Uphold",
    "sex": "F",
    "born": "20 Feb 1957",
    "spouses": [{"name": "Ricky Marchi", "born": "18 Nov 1956"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 96},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1415521", "name": "Michelle Ray Marchi", "born": "10 Jun 1978", "verified_terminal": True},
        {"code": "1415522", "name": "Stephanie Marchi", "born": "14 Jul 1979", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "142523",
    "name": "Robert Eugene Nicola",
    "sex": "M",
    "born": "26 Mar 1934",
    "spouses": [
        {"name": "Tressie Arveta White", "born": "6 Dec 1934", "married": "20 Dec 1952", "order": 1, "details": "Divorced 1984."},
        {"name": "Betty Moody Croft", "born": "30 Jun", "died": "11 Jul 1990", "married": "16 Mar 1985", "order": 2},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 96},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1425231", "name": "Arveta Louise Nicola", "born": "16 Sep 1953"},
        {"code": "1425232", "name": "Catherine Ann Nicola", "born": "10 Dec 1954"},
        {"code": "1425233", "name": "Barbara Grace Nicola", "born": "13 Oct 1956"},
        {"code": "1425234", "name": "Robert Eugene Nicola, Jr.", "born": "29 Aug 1962"},
    ],
})

ENTRIES.append({
    "code": "142524",
    "name": "Dorothy Jean Nicola",
    "sex": "F",
    "born": "6 Oct 1937",
    "spouses": [{"name": "William (Bill) Donald Whipkey", "born": "1 Mar 1934", "married": "30 Jun 1956"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 96},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1425241", "name": "Daniel (Danny) George Whipkey", "born": "31 Mar 1963", "died": "1988"},
        {"code": "1425242", "name": "Tamra Lynn Whipkey", "born": "9 Jan 1968"},
    ],
})

ENTRIES.append({
    "code": "142821",
    "name": "Catherine Louise Sines",
    "sex": "F",
    "born": "28 Feb 1954",
    "spouses": [
        {"name": "Oakey Stanley", "married": "15 May 1971", "order": 1},
        {"name": "Kenneth Frankenberry", "married": "24 Jul 1986", "order": 2},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 96},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1428211", "name": "Tamara (Tammy) Lynn Stanley", "born": "18 Apr 1972", "verified_terminal": True},
        {"code": "1428212", "name": "Rachel Louise Frankenberry", "born": "6 Jul 1988", "verified_terminal": True},
        {"code": "1428213", "name": "Kimberlet Ann Frankenberry", "born": "Mar 1990", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "142861",
    "name": "Harold Glen (Hump) Rosenberger",
    "sex": "M",
    "born": "6 May 1950",
    "spouses": [{"name": "Sandra Brynor"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 97},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1428611", "name": "Jason Rosenberger", "verified_terminal": True},
        {"code": "1428612", "name": "Kevin Rosenberger", "verified_terminal": True},
        {"code": "1428613", "name": "Stephen Rosenberger", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "142862",
    "name": "Melvin Lee Rosenberger",
    "sex": "M",
    "born": "27 Jul 1952",
    "spouses": [{"name": "Barbara Wade"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 97},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1428621", "name": "Tommy Rosenberger", "verified_terminal": True},
        {"code": "1428622", "name": "Jimmy Rosenberger", "verified_terminal": True},
        {"code": "1428623", "name": "Bethany Rosenberger", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "142883",
    "name": "Jeanette Sines",
    "sex": "F",
    "born": "25 Jan 1968",
    "spouses": [{"name": "Matthew Lonergan"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 97},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1428831", "name": "Joshua Lonergan", "born": "8 Apr 1989", "verified_terminal": True},
        {"code": "1428832", "name": "Zachary Lonergan", "born": "1 Sep 1991", "verified_terminal": True},
        {"code": "1428833", "name": "Benjamin Lonergan", "born": "23 Nov 1995", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "143293",
    "name": "Linda Myers",
    "sex": "F",
    "born": "4 Jun 1955",
    "spouses": [
        {"name": "Kenneth Seese", "born": "7 Aug 1947", "order": 1},
        {"name": "David Harman", "born": "5 Sep 1952", "order": 2},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 97},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1432931", "name": "Dwain Seese", "born": "21 Aug 1980", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "143412",
    "name": "Raymond Collins",
    "sex": "M",
    "spouses": [{"name": "Pearl Marie Fike", "born": "13 Jul 1942", "married": "1 Feb 1959"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 97},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1434121", "name": "Ronald Lee Collins", "born": "9 Aug 1959"},
        {"code": "1434122", "name": "Tammie Sue Collins", "born": "27 Jun 1963", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "143413",
    "name": "Carl Collins",
    "sex": "M",
    "spouses": [{"name": "Wilma Ruth McCarty", "born": "7 Nov 1946", "married": "5 May 1963"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 97},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1434131", "name": "Michael Ray Collins", "born": "28 Aug 1963"},
        {"code": "1434132", "name": "Kenneth Lynn Collins", "born": "21 Nov 1968", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "143424",
    "name": "Carl R. Nicola",
    "sex": "M",
    "born": "9 Sep 1946",
    "spouses": [{"name": "Betty", "born": "19 Oct 1950"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 97},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1434241", "name": "Carl R. Nicola, Jr.", "born": "10 Nov 1972", "verified_terminal": True},
        {"code": "1434242", "name": "Carlo Nicola", "born": "14 Dec 1973", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "143426",
    "name": "Betty K. Nicola",
    "sex": "F",
    "born": "13 Sep 1953",
    "spouses": [{"name": "Thomas C. Zweyer", "born": "31 Jul 1951"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 97},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1434261", "name": "Patrick Zweyer", "born": "23 Aug 1979", "verified_terminal": True},
        {"code": "1434262", "name": "Tyra C. Zweyer", "born": "31 Jul 1981", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "143427",
    "name": "Jacob George Nicola, Jr.",
    "sex": "M",
    "born": "27 May 1960",
    "spouses": [{"name": "Nancy Lynn Matthews", "born": "1962", "married": "24 Apr 1980"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 97},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1434271", "name": "Child", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "144112",
    "name": "Lois Jean Sisler",
    "sex": "F",
    "spouses": [{"name": "William Kostelnik"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 98},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1441121", "name": "William Kostelnik", "verified_terminal": True},
        {"code": "1441122", "name": "Janet Kostelnik", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "144113",
    "name": "Dale Arthur Sisler",
    "sex": "M",
    "born": "1929",
    "spouses": [{"name": "Lucinda Ann Baker", "born": "1928"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 98},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1441131", "name": "William Dale Sisler", "born": "1956", "verified_terminal": True},
        {"code": "1441132", "name": "David Arthur Sisler", "born": "1964", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "144121",
    "name": "Dwight Marcus Sisler",
    "sex": "M",
    "born": "May 1935",
    "spouses": [{"name": "Ruth Kermish", "born": "May 1935"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 98},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1441211", "name": "David Dwight Sisler", "born": "1956", "verified_terminal": True},
        {"code": "1441212", "name": "Richard Allen Sisler", "born": "1958", "verified_terminal": True},
        {"code": "1441213", "name": "Stephen Douglas Sisler", "born": "1964", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "144122",
    "name": "Robert Clayton Sisler",
    "sex": "M",
    "born": "1937",
    "spouses": [{"name": "Dorthy Richards", "born": "1940"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 98},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1441221", "name": "Robert Clayton Sisler, Jr.", "born": "1958", "verified_terminal": True},
        {"code": "1441222", "name": "Thomas Troy Sisler", "born": "1960", "verified_terminal": True},
        {"code": "1441223", "name": "Myra Ann Sisler", "born": "1962", "verified_terminal": True},
        {"code": "1441224", "name": "James Edward Sisler", "born": "1966", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "144123",
    "name": "Virginia Faye Sisler",
    "sex": "F",
    "born": "1944",
    "spouses": [{"name": "James Larry Stump", "married": "1966"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 98},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1441231", "name": "Wendy Leigh Stump", "born": "1967", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "144131",
    "name": "Donald Ray Sisler",
    "sex": "M",
    "born": "1932",
    "spouses": [{"name": "Jean"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 98},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1441311", "name": "Donald Ray Sisler, Jr.", "born": "1966", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "144132",
    "name": "Dorthy Jean Sisler",
    "sex": "F",
    "born": "Jul 1935",
    "spouses": [{"name": "William Biro", "married": "1965"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 98},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1441321", "name": "Tia Ann Biro", "born": "1967", "verified_terminal": True},
        {"code": "1441322", "name": "William Biro, Jr.", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "144134",
    "name": "Delores Ann Sisler",
    "sex": "F",
    "born": "8 Aug 1947",
    "spouses": [{"name": "Ward Cecil Moyers", "born": "1939"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 98},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1441341", "name": "Mark Cecil Moyers", "born": "14 Jul 1966", "verified_terminal": True},
        {"code": "1441342", "name": "Michael Lynn Moyers", "born": "19 Jul 1968", "died": "25 Aug 1983", "verified_terminal": True},
        {"code": "1441343", "name": "Gregory Douglas Moyers", "born": "6 Mar 1977", "verified_terminal": True},
        {"code": "1441344", "name": "Daniel Joe Moyers", "born": "7 Nov 1978", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "144141",
    "name": "Audrey Frazee",
    "sex": "F",
    "born": "20 Mar 1932",
    "spouses": [
        {"name": "William Wesley Sorrells", "born": "30 Jul", "order": 1},
        {"name": "William Renner", "born": "22 Oct 1927", "order": 2},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 98},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1441411", "name": "Larry Sorrells", "born": "2 Feb 1951", "verified_terminal": True},
        {"code": "1441412", "name": "Barbara Darlene Renner", "born": "15 Aug 1954", "verified_terminal": True},
        {"code": "1441413", "name": "Brenda Renner", "born": "1 Oct 1957", "verified_terminal": True},
        {"code": "1441414", "name": "Brian Renner", "born": "17 Aug 1959", "verified_terminal": True},
        {"code": "1441415", "name": "Bradley Renner", "born": "25 Oct 1961", "verified_terminal": True},
        {"code": "1441416", "name": "Lori Renner", "born": "26 Jan 1964", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "144151",
    "name": "Benjamin Paul Sisler",
    "sex": "M",
    "born": "19 Apr 1933",
    "spouses": [{"name": "Janice Cale", "born": "21 May 1935", "married": "24 Oct 1953"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 99},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1441511", "name": "Anita Louise Sisler", "born": "15 Oct 1965", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "144153",
    "name": "Mary Ellen Sisler",
    "sex": "F",
    "born": "22 Oct 1940",
    "spouses": [{"name": "Lowell Maynard Mayle", "born": "19 Sep 1941", "married": "24 Jul 1960"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 99},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1441531", "name": "Lowell M. Mayle, Jr.", "born": "29 Jul 1961", "verified_terminal": True},
        {"code": "1441532", "name": "Crystal Lucinda Mayle", "born": "24 Jul 1962", "verified_terminal": True},
        {"code": "1441533", "name": "Thomas Douglas Mayle", "born": "27 Jun 1973", "verified_terminal": True},
        {"code": "1441534", "name": "Timothy Dwight Mayle", "born": "13 Jul 1975", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "144154",
    "name": "Jane Elaine Sisler",
    "sex": "F",
    "born": "23 Jan 1944",
    "spouses": [{"name": "Harold Emerson Kronk", "born": "31 Jan 1941", "married": "6 Aug 1962"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 99},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1441541", "name": "Harold E. Kronk, Jr.", "born": "4 May 1963"},
        {"code": "1441542", "name": "David Dee Kronk", "born": "21 Jun 1964", "verified_terminal": True},
        {"code": "1441543", "name": "Keith D. Kronk", "born": "Aug 1966", "verified_terminal": True},
        {"code": "1441544", "name": "Kevin D. Kronk", "born": "Aug 1966", "verified_terminal": True},
        {"code": "1441545", "name": "Janie Lonelle Kronk", "born": "22 Dec 1979", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "144155",
    "name": "Wilma Marie Sisler",
    "sex": "F",
    "born": "17 Feb 1946",
    "spouses": [{"name": "Richard Paris Dalton", "born": "21 Aug 1937", "married": "29 Jul 1967"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 99},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1441551", "name": "Richard Paul Dalton", "born": "6 Oct 1969", "verified_terminal": True},
        {"code": "1441552", "name": "Nancy Jane Dalton", "born": "7 Nov 1973", "verified_terminal": True},
        {"code": "1441553", "name": "Lydia Marie Dalton", "born": "3 Jun 1979", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "144161",
    "name": "Norma Jean Sisler",
    "sex": "F",
    "born": "12 Apr 1939",
    "spouses": [{"name": "Milton Means"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 99},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1441611", "name": "Patrick Sean Means", "born": "1963", "verified_terminal": True},
        {"code": "1441612", "name": "Kathleen Dawn Means", "born": "Mar 1967", "verified_terminal": True},
    ],
})


# === Pages 101-105 vision pass (2026-06-07): Spiker/Carpenter/Groves/Evans/Thomas/Kahl/Appleby/Cuppett/Burner gen 7/8 ===
ENTRIES.append({
    "code": "144531",
    "name": "Stanley Ray Spiker",
    "sex": "M",
    "born": "2 Jun 1936",
    "died": "1 Apr 1995",
    "spouses": [{"name": "Hazel Lucinda Schnopp", "born": "23 Aug 1941", "married": "16 Oct 1959"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 101},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1445311", "name": "Steven Lee Spiker", "born": "6 May 1961"},
        {"code": "1445312", "name": "Randy Dale Spiker", "born": "25 Jul 1968"},
    ],
})

ENTRIES.append({
    "code": "144532",
    "name": "Glenna Catherine Spiker",
    "sex": "F",
    "born": "20 Sep 1941",
    "spouses": [{"name": "Eura Jennings Carpenter", "married": "21 Oct 1964"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 102},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1445321", "name": "Teresa Lynn Carpenter", "born": "9 Nov 1967", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "144533",
    "name": "Ruby Lovine Spiker",
    "sex": "F",
    "born": "21 Dec 1945",
    "spouses": [
        {"name": "Ronald David Fike", "born": "30 Oct 1943", "married": "30 Sep 1965", "order": 1},
        {"name": "Jack Radford", "born": "13 Apr 1935", "order": 2},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 102},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1445331", "name": "Michael Lynn Fike", "born": "25 Nov 1967", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "144541",
    "name": "Donald Groves",
    "sex": "M",
    "spouses": [{"name": "Jean Howdershelt"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 102},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1445411", "name": "Greg Paul Groves", "born": "26 Jun 1960"},
        {"code": "1445412", "name": "Tammy Groves", "born": "1 Jul 1961", "verified_terminal": True},
        {"code": "1445413", "name": "Crystal Dawn Groves", "born": "20 Feb 1967"},
    ],
})

ENTRIES.append({
    "code": "144551",
    "name": "Roy Evans",
    "sex": "M",
    "spouses": [{"name": "Patricia (Patty) Smith"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 102},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1445511", "name": "Chad Steward Evans", "verified_terminal": True},
        {"code": "1445512", "name": "Tony Lynn Evans", "born": "29 Mar 1979", "died": "15 Apr 1979", "flags": {"diedInInfancy": True}, "verified_terminal": True},
        {"code": "1445513", "name": "Cassie Ann Evans", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "144615",
    "name": "Kathy Thomas",
    "sex": "F",
    "spouses": [{"name": "Weber"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 102},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1446151", "name": "Steven Weber", "verified_terminal": True},
        {"code": "1446152", "name": "Jennifer Weber", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "144761",
    "name": "Kenneth Dewight Thomas",
    "sex": "M",
    "born": "20 Oct 1962",
    "spouses": [{"name": "Samantha Jo Wilson", "born": "27 Nov 1965", "married": "24 Jul 1980"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 102},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1447611", "name": "Steven Paul Thomas", "born": "25 Mar 1980", "verified_terminal": True},
        {"code": "1447612", "name": "Wesley Andrew Thomas", "born": "12 Jan 1987", "verified_terminal": True},
        {"code": "1447613", "name": "Corey Scott Thomas", "born": "6 Jul 1988", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "144762",
    "name": "Jeffery Dale Thomas",
    "sex": "M",
    "born": "22 Aug 1963",
    "spouses": [{"name": "Denise Marie Nemeth", "born": "27 May 1965", "married": "17 Mar 1985"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 102},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1447621", "name": "Debra Ann Thomas", "born": "28 Jul 1985", "verified_terminal": True},
        {"code": "1447622", "name": "Danielle Marie Thomas", "born": "28 Feb 1987", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "144763",
    "name": "Michelle Dawn Thomas",
    "sex": "F",
    "born": "11 Dec 1968",
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 103},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1447631", "name": "Jessica Lee Thomas", "born": "24 Nov 1986", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "144821",
    "name": "Bonnie Kay Strawser",
    "sex": "F",
    "spouses": [{"name": "Eugene Hully Malone, Jr.", "married": "31 Dec 1971"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 103},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1448211", "name": "Meredith K. Malone", "verified_terminal": True},
        {"code": "1448212", "name": "Eric Malone", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "144822",
    "name": "Judy Rae Strawser",
    "sex": "F",
    "spouses": [
        {"name": "Robert Michael Boylan, Jr.", "married": "1971", "order": 1},
        {"name": "Selden O. Pratt", "order": 2},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 103},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1448221", "name": "Aaron M. Boylan", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "144823",
    "name": "Gary Paul Strawser",
    "sex": "M",
    "born": "1 Jul 1948",
    "died": "27 Jun 1996",
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 103},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1448231", "name": "Chandel Strawser"},
    ],
})

ENTRIES.append({
    "code": "144824",
    "name": "Joy Ann Strawser",
    "sex": "F",
    "spouses": [{"name": "William Galliford"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 103},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1448241", "name": "Alaina J. Galliford", "verified_terminal": True},
        {"code": "1448242", "name": "Nathaniel R. Galliford", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "147181",
    "name": "Donna Louise Kahl",
    "sex": "F",
    "born": "18 Jun 1942",
    "spouses": [
        {"name": "Charles Dewey Williams", "married": "23 Jan 1960", "order": 1},
        {"name": "Joseph Harold Martin", "born": "7 Feb 1944", "married": "18 Feb 1967", "order": 2},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 103},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1471811", "name": "Darla Joy Williams", "born": "3 Aug 1960", "verified_terminal": True},
        {"code": "1471812", "name": "Deborah Jean Williams", "born": "1 Oct 1961", "verified_terminal": True},
        {"code": "1471813", "name": "Charles Dewey Williams", "born": "25 Oct 1963", "verified_terminal": True},
        {"code": "1471814", "name": "Ronald Douglas Williams", "born": "14 Dec 1964", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "147183",
    "name": "Shirley Jean Kahl",
    "sex": "F",
    "born": "20 Jul 1945",
    "spouses": [{"name": "Alfred Richard Brauns", "born": "7 Aug 1944", "married": "30 Nov 1963"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 103},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1471831", "name": "Eric Benton Brauns", "born": "15 Apr 1969", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "147511",
    "name": "Harold Ashton Appleby",
    "sex": "M",
    "born": "1 May 1934",
    "spouses": [{"name": "Mary Scott", "born": "21 Jun 1937", "married": "30 Jun 1956"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 103},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1475111", "name": "Donna Rae Appleby", "born": "17 Oct 1957"},
        {"code": "1475112", "name": "Kathy Marie Appleby", "born": "2 Jul 1959"},
        {"code": "1475113", "name": "Scott Harold Appleby", "born": "30 Dec 1961", "verified_terminal": True},
        {"code": "1475114", "name": "George Robinson Appleby", "born": "14 Dec 1962", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "147512",
    "name": "Richard Harland Appleby",
    "sex": "M",
    "born": "21 May 1936",
    "spouses": [{"name": "Ruth Plum", "born": "24 Apr 1940", "married": "3 Nov 1958"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 103},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1475121", "name": "Tammy Lee Appleby", "born": "13 Apr 1958", "verified_terminal": True},
        {"code": "1475122", "name": "Terri Lynn Appleby", "born": "2 Jun 1960"},
        {"code": "1475123", "name": "Gary Allen Appleby", "born": "9 Apr 1963", "verified_terminal": True},
        {"code": "1475124", "name": "Allen Dale Appleby", "born": "9 Dec 1968", "verified_terminal": True},
        {"code": "1475125", "name": "Tracy Ann Appleby", "born": "1 Sep 1971", "verified_terminal": True},
        {"code": "1475126", "name": "Trina Rae Appleby", "born": "26 Oct 1972", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "147513",
    "name": "Sandra Faye Appleby",
    "sex": "F",
    "born": "24 Sep 1937",
    "spouses": [{"name": "Charles Roy Wolfe", "born": "20 Sep 1936", "married": "10 Dec 1955"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 104},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1475131", "name": "Linda Carol Wolfe", "born": "23 Jun 1957"},
        {"code": "1475132", "name": "Shelda Lee Wolfe", "born": "26 May 1961"},
        {"code": "1475133", "name": "Sheila Lynn Wolfe", "born": "26 May 1961"},
        {"code": "1475134", "name": "Charles Roy Wolfe, II", "born": "27 Apr 1970"},
    ],
})

ENTRIES.append({
    "code": "147514",
    "name": "Nancy Lee Appleby",
    "sex": "F",
    "born": "1 Oct 1938",
    "spouses": [{"name": "Nathan Gregory", "married": "14 Aug 1956"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 104},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1475141", "name": "Christopher David Gregory", "born": "8 Apr 1959", "verified_terminal": True},
        {"code": "1475142", "name": "Deborah Ann Gregory", "born": "24 Apr 1960"},
        {"code": "1475143", "name": "Barbara Ann Gregory", "born": "4 Apr 1962"},
        {"code": "1475144", "name": "Claudette Ann Gregory", "born": "8 Sep 1965", "verified_terminal": True},
        {"code": "1475145", "name": "Dawn Ann Gregory", "born": "20 Apr 1970", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "147515",
    "name": "Carol Ann Appleby",
    "sex": "F",
    "born": "28 Jun 1944",
    "spouses": [{"name": "Max Miller", "born": "16 Oct 1939", "married": "25 Sep 1965"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 104},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1475151", "name": "Steve Miller", "born": "21 Feb 1966", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "147516",
    "name": "Thomas Edward Appleby, II",
    "sex": "M",
    "born": "7 Feb 1951",
    "died": "4 Jun 1972",
    "spouses": [{"name": "Vicki Guthrie", "married": "6 Feb 1972"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 104},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1475161", "name": "Jason Edward Appleby", "born": "17 Aug 1972", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "147517",
    "name": "James William Appleby",
    "sex": "M",
    "born": "8 Jun 1953",
    "spouses": [{"name": "Sandra Gates"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 104},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1475171", "name": "James William Appleby, II", "born": "11 Oct 1975", "verified_terminal": True},
        {"code": "1475172", "name": "Paul Edward Appleby", "born": "14 Oct 1977", "verified_terminal": True},
        {"code": "1475173", "name": "Dorothy Jean Appleby", "born": "21 Sep 1981", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "147518",
    "name": "Mark Bradley Appleby",
    "sex": "M",
    "born": "28 Apr 1958",
    "spouses": [{"name": "Anita Louise Trout"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 104},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1475181", "name": "Heather Lynn Appleby", "born": "1 Apr 1978", "verified_terminal": True},
        {"code": "1475182", "name": "Mark Bradley Appleby", "born": "24 May 1980", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "147521",
    "name": "Sharon A. Cunningham",
    "sex": "F",
    "born": "4 Jun 1935",
    "spouses": [{"name": "Robert Myers", "born": "22 Jan 1933", "married": "13 Jan 1952"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 104},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1475211", "name": "Robert Myers, Jr.", "born": "14 Nov 1953", "verified_terminal": True},
        {"code": "1475212", "name": "Kevin Myers", "born": "1 Oct 1955", "verified_terminal": True},
        {"code": "1475213", "name": "Keith Myers", "born": "1 Oct 1955", "verified_terminal": True},
        {"code": "1475214", "name": "Jerry Myers", "born": "10 Apr 1962", "verified_terminal": True},
        {"code": "1475215", "name": "Renee Myers", "born": "10 Jan 1966", "verified_terminal": True},
        {"code": "1475216", "name": "Darin Myers", "born": "26 Nov 1966", "verified_terminal": True},
        {"code": "1475217", "name": "Ron Myers", "born": "20 Sep 1969", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "147531",
    "name": "Robert Carl Fisher, Jr.",
    "sex": "M",
    "born": "7 Jul 1946",
    "spouses": [{"name": "Karen McCoy", "married": "16 Feb 1970"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 104},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1475311", "name": "Robert Carl Fisher III", "born": "26 Sep 1970", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "147532",
    "name": "Vanessa Gayle Fisher",
    "sex": "F",
    "born": "14 Nov 1953",
    "spouses": [{"name": "Harry McCormick", "married": "27 Sep 1974"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 105},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1475321", "name": "Adam Michael McCormick", "born": "10 Apr 1985", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "161111",
    "name": "Elizabeth Ann Cuppett",
    "sex": "F",
    "born": "17 Sep 1937",
    "spouses": [{"name": "Robert Francis Fanto", "born": "19 Sep 1931", "married": "8 Jun 1957"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 105},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1611111", "name": "Mark Stephen Fanto", "born": "24 Mar 1958", "verified_terminal": True},
        {"code": "1611112", "name": "Stephen Michael Fanto", "born": "21 Dec 1960", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "161112",
    "name": "Reardon Stewart Colton Cuppett, Jr.",
    "sex": "M",
    "born": "11 Jun 1939",
    "spouses": [{"name": "Catherine Ann Stanhagen", "born": "5 Jun 1942", "married": "7 Oct 1961"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 105},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1611121", "name": "Michael Shawn Cuppett", "born": "23 Oct 1964", "verified_terminal": True},
        {"code": "1611122", "name": "Patrick Shennon Cuppett", "born": "22 Sep 1966", "verified_terminal": True},
        {"code": "1611123", "name": "Kevin Shane Cuppett", "born": "19 Feb 1969", "verified_terminal": True},
        {"code": "1611124", "name": "Brandon Shea Cuppett", "born": "12 Aug 1971", "verified_terminal": True},
        {"code": "1611125", "name": "Erin Shelean Cuppett", "born": "5 Jun 1977", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "161113",
    "name": "Vida Marie Cuppett",
    "sex": "F",
    "born": "18 Apr 1943",
    "spouses": [{"name": "Nicholas Thomas Simon", "born": "12 Dec 1942", "married": "13 May 1972"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 105},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1611131", "name": "Nicholas Thomas Simon, Jr.", "born": "18 Apr 1973", "verified_terminal": True},
        {"code": "1611132", "name": "Marie Theresa Simon", "born": "30 Mar 1976", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "161121",
    "name": "Ruth Grant Cuppett",
    "sex": "F",
    "born": "22 Jun 1938",
    "spouses": [{"name": "John Allison Buchanan", "born": "19 Dec 1931", "married": "18 Jul 1959"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 105},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1611211", "name": "Anne Allison Buchanan", "born": "2 May 1960"},
        {"code": "1611212", "name": "Kerra Cresap Buchanan", "born": "21 Aug 1962", "verified_terminal": True},
        {"code": "1611213", "name": "James Grant Buchanan", "born": "12 Sep 1964"},
        {"code": "1611214", "name": "Jill Luise Buchanan", "born": "27 Mar 1966"},
    ],
})

ENTRIES.append({
    "code": "161122",
    "name": "David Earl Cuppett III",
    "sex": "M",
    "born": "26 Mar 1946",
    "spouses": [{"name": "Karen Ann Sites", "born": "27 Apr 1947", "married": "15 Apr 1967"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 105},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1611221", "name": "David Earl Cuppett IV", "born": "1 Dec 1967", "verified_terminal": True},
        {"code": "1611222", "name": "Bryan Scott Cuppett", "born": "17 Oct 1970", "verified_terminal": True},
        {"code": "1611223", "name": "Christopher Jason Cuppett", "born": "2 Sep 1977", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "161132",
    "name": "Barbara Gene Bickel",
    "sex": "F",
    "born": "1 Dec 1947",
    "spouses": [{"name": "Richard Allan Trotter", "married": "4 Sep 1971"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 105},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1611321", "name": "Sarah Beth Trotter", "born": "31 May 1979", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "161133",
    "name": "Cynthia Jane Bickel",
    "sex": "F",
    "born": "8 Nov 1952",
    "spouses": [{"name": "Russell Lee Shannon", "born": "13 Oct 1950", "married": "27 Sep 1969"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 105},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1611331", "name": "Christopher Scott Shannon", "born": "12 Mar 1971", "verified_terminal": True},
        {"code": "1611332", "name": "Melissa Lynn Shannon", "born": "2 Apr 1977", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "161211",
    "name": "Ronald Irwin Burner",
    "sex": "M",
    "born": "1 Oct 1939",
    "spouses": [
        {"name": "Paulette Carole Greene", "born": "1 Jul 1941", "married": "22 Jul 1966", "order": 1},
        {"name": "Diana Papa Lazoras", "born": "31 May 1960", "married": "22 Apr 1983", "order": 2},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 105},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1612111", "name": "Terra Ann Burner", "born": "20 Jun 1968", "verified_terminal": True},
        {"code": "1612112", "name": "Scott Irwin Burner", "born": "15 Jul 1969", "verified_terminal": True},
    ],
})


# === Pages 106-110 vision pass (2026-06-07): Burner/Baysinger/Long/Moyers/Spear/Wright/Taggart/Glover/Nicola/Narivanchik/Hileman gen 7/8 ===
ENTRIES.append({
    "code": "161212",
    "name": "Beverly Lou Burner",
    "sex": "F",
    "born": "1 Oct 1941",
    "spouses": [{"name": "Robert Dunlap", "born": "2 Feb 1939", "married": "25 Feb 1966"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 106},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1612121", "name": "Sherry Dunlap", "born": "4 Aug 1970", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "162211",
    "name": "Lawrence Keith Baysinger",
    "sex": "M",
    "born": "28 Aug 1954",
    "spouses": [{"name": "Barbara Avis Green", "born": "6 Mar 1946", "married": "4 Jul 1973"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 106},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1622111", "name": "Stephanie Lynn Baysinger", "born": "26 Oct 1970", "verified_terminal": True},
        {"code": "1622112", "name": "Elizabeth Ann Baysinger", "born": "9 Jul 1976", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "162212",
    "name": "Rebecca Jane Baysinger",
    "sex": "F",
    "born": "15 Sep 1954",
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 106},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1622121", "name": "Andrew Lee Baysinger", "born": "4 Mar 1983", "verified_terminal": True},
        {"code": "1622122", "name": "Timothy Allen Baysinger", "born": "26 Apr 1987", "verified_terminal": True},
        {"code": "1622123", "name": "Ryan Michael Gressler", "born": "7 Aug 1989", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "162221",
    "name": "Doyle Wayne Long",
    "sex": "M",
    "born": "3 Aug 1952",
    "spouses": [{"name": "Lynn Ann Dilts", "married": "5 Oct 1974"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 106},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1622211", "name": "Adam Heath Long", "born": "19 Mar 1975", "verified_terminal": True},
        {"code": "1622212", "name": "Abigail Mae Long", "born": "7 Apr 1979", "verified_terminal": True},
        {"code": "1622213", "name": "Seth Raymond Lawrence Long", "born": "15 Jul 1982", "verified_terminal": True},
        {"code": "1622214", "name": "Alyse Marquerite", "born": "30 Sep 1985", "verified_terminal": True},
        {"code": "1622215", "name": "Simon Henry", "born": "24 Jul 1993", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "162222",
    "name": "Nolan Wade Long",
    "sex": "M",
    "born": "16 Mar 1956",
    "spouses": [{"name": "Lillian Fay Miller", "born": "4 Dec 1953", "married": "5 Aug 1978"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 106},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1622221", "name": "Jordan Tobias Long", "born": "15 Jul 1983", "verified_terminal": True},
        {"code": "1622222", "name": "Nelson Levi Long", "born": "5 Nov 1985", "verified_terminal": True},
        {"code": "1622223", "name": "Kiersten Donnastella", "born": "6 May 1988", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "162241",
    "name": "Diana Sue Moyers",
    "sex": "F",
    "born": "5 Jul 1954",
    "spouses": [{"name": "Dana Ray Hewitt", "born": "31 Dec 1950", "married": "6 Oct 1973"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 106},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1622411", "name": "Daniel Arron Hewitt", "born": "24 Jul 1977", "verified_terminal": True},
        {"code": "1622412", "name": "David Allen Hewitt", "born": "5 Oct 1978", "verified_terminal": True},
        {"code": "1622413", "name": "Daryl Andrew Hewitt", "born": "26 May 1980", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "162242",
    "name": "Charles Howard Moyers",
    "sex": "M",
    "born": "29 Jul 1957",
    "spouses": [{"name": "Winnie Renee Bucklew", "born": "26 Feb 1957", "married": "3 Feb 1979"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 106},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1622421", "name": "Charles Junior (CJ) Moyers", "born": "12 Oct 1982", "verified_terminal": True},
        {"code": "1622422", "name": "Amy Renee Moyers", "born": "4 Mar 1987", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "162243",
    "name": "William Ray Moyers",
    "sex": "M",
    "born": "19 Dec 1961",
    "spouses": [{"name": "Judith (Judy) Lynn Deal", "born": "20 Feb 1966", "married": "19 Oct 1995", "details": "Same as #1233521."}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 107},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1622431", "name": "William Treavis Moyers", "born": "11 Dec 1996", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "162311",
    "name": "Carl R. Spear",
    "sex": "M",
    "born": "12 Feb",
    "spouses": [
        {"name": "Nancy L. Valisko", "born": "12 Feb 1936", "died": "2 Oct 1985", "order": 1},
        {"name": "Mrs. Carol Sherrill", "married": "1988", "order": 2},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 107},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1623111", "name": "Mark Spear", "born": "28 Feb"},
        {"code": "1623112", "name": "Sean Spear", "born": "9 Jan 1969", "verified_terminal": True},
        {"code": "1623113", "name": "Keith Spear", "born": "23 Jan 1970", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "162312",
    "name": "Charlotte May Spear",
    "sex": "F",
    "spouses": [
        {"name": "James Walls", "order": 1},
        {"name": "David Wilson", "order": 2},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 107},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1623121", "name": "Child", "verified_terminal": True},
        {"code": "1623122", "name": "Child", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "162372",
    "name": "Stewart Allen Moyers",
    "sex": "M",
    "born": "28 Oct 1955",
    "spouses": [
        {"name": "Susan Catherine Lipscomb", "married": "17 Aug 1974", "order": 1},
        {"name": "Darlene Bolyard", "married": "24 Jun 1978", "order": 2},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 107},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1623721", "name": "Scott Moyers", "born": "1975", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "162412",
    "name": "Paulette Marie Wright",
    "sex": "F",
    "born": "23 Mar 1957",
    "spouses": [{"name": "Paul Yucha"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 107},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1624121", "name": "Shirley Ann Yucha", "born": "Jun 1985", "verified_terminal": True},
        {"code": "1624122", "name": "Michael Ray Yucha", "born": "Apr 1987", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "162413",
    "name": "Jefferie Ray Wright",
    "sex": "M",
    "born": "27 Nov 1963",
    "spouses": [{"name": "Pamela Youst"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 107},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1624131", "name": "Jeffrey Ray Wright", "born": "Aug 1985", "verified_terminal": True},
        {"code": "1624132", "name": "Jedehiah Wright", "born": "Nov 1987", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "163112",
    "name": "Clara Rosalie Taggart",
    "sex": "F",
    "born": "6 Aug 1927",
    "spouses": [{"name": "Charles Weaver", "born": "15 Oct 1926", "married": "15 Jul 1950"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 107},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1631121", "name": "Robert Kyle Weaver", "born": "20 Aug 1951"},
        {"code": "1631122", "name": "Thomas William Weaver", "born": "6 Dec 1954"},
    ],
})

ENTRIES.append({
    "code": "163142",
    "name": "Loretta Mae Glover",
    "sex": "F",
    "born": "25 Jul 1933",
    "spouses": [
        {"name": "Willard (Monk) Blaine Moyers", "born": "21 Mar 1921", "died": "21 Feb 1988", "married": "20 Mar 1951", "order": 1},
        {"name": "Lloyd (Red) Jackson Hall, Jr.", "born": "11 Sep 1923", "died": "16 Jan 1990", "order": 2},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 108},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1631421", "name": "Richard Blaine Moyers", "born": "24 Aug 1951"},
        {"code": "1631422", "name": "Randy Wayne Moyers", "born": "12 Nov 1952"},
        {"code": "1631423", "name": "Keith Alan Moyers", "born": "29 Jul 1954"},
        {"code": "1631424", "name": "Darlene Louise Moyers", "born": "24 Feb 1959"},
    ],
})

ENTRIES.append({
    "code": "163144",
    "name": "Larry Robert Collins",
    "sex": "M",
    "born": "3 Feb 1952",
    "spouses": [{"name": "Dott Guseman", "born": "6 Dec 1950", "married": "29 May 1976"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 108},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1631441", "name": "Carly Ann Collins", "born": "30 Oct 1978", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "163152",
    "name": "Shirley Jean Greathouse",
    "sex": "F",
    "born": "17 May 1939",
    "spouses": [{"name": "Harold L. Smith", "born": "7 Apr 1940", "married": "11 Jul 1959"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 108},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1631521", "name": "Julia Marie Smith", "born": "15 Sep 1963"},
    ],
})

ENTRIES.append({
    "code": "163161",
    "name": "Stanley Ray Moody",
    "sex": "M",
    "born": "9 Jun 1940",
    "spouses": [
        {"name": "Margaret Catherine Shoof", "married": "Dec 1962", "order": 1, "details": "Divorced."},
        {"name": "Lorraine Myers", "born": "1 May 1941", "married": "18 Dec 1972", "order": 2},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 108},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1631611", "name": "Stanley Ray Moody, Jr.", "born": "24 Jun 1963", "verified_terminal": True},
        {"code": "1631612", "name": "Debra Lynn Moody", "born": "27 Oct 1964", "verified_terminal": True},
        {"code": "1631613", "name": "James Harold Moody", "born": "22 Feb 1971", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "163171",
    "name": "Betty Carol Cramer",
    "sex": "F",
    "born": "31 Dec 1946",
    "spouses": [{"name": "Lewis (Sonny) Thomas Jr.", "born": "28 Dec 1946", "married": "15 May 1966"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 108},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1631711", "name": "Virginia (Ginger) Sue Thomas", "born": "18 Oct 1966"},
    ],
})

ENTRIES.append({
    "code": "163181",
    "name": "Jackie Dale Nicola",
    "sex": "M",
    "born": "9 Mar 1951",
    "spouses": [{"name": "Michelle Ghrist", "born": "23 Aug 1953", "married": "25 Aug 1973"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 108},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1631811", "name": "Brandi Nicola", "born": "26 Dec 1975", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "163182",
    "name": "Jamie Judson Nicola",
    "sex": "M",
    "born": "26 Jun 1954",
    "spouses": [{"name": "Irene Balaban", "born": "15 Aug 1954", "married": "28 Oct 1972"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 108},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1631821", "name": "James J. Nicola", "born": "16 May 1973", "verified_terminal": True},
        {"code": "1631822", "name": "Jason Nicola", "born": "23 May 1976", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "163183",
    "name": "Kimberly Rae Nicola",
    "sex": "F",
    "born": "20 Sep 1964",
    "spouses": [{"name": "Raymond R. Thompson", "married": "26 May 1990"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 108},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1631831", "name": "Rachael Nicole Thompson", "born": "9 May 1991", "verified_terminal": True},
        {"code": "1631832", "name": "Lauren Marie Tompson", "born": "28 Oct 1993", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "164111",
    "name": "Theodore Ralph Narivanchik",
    "sex": "M",
    "born": "7 Sep 1949",
    "spouses": [
        {"name": "Sandra Rose Chavis", "born": "19 Feb 1952", "married": "18 Dec 1970", "order": 1},
        {"name": "Belinda Jean Fails", "born": "12 Feb 1951", "married": "10 Mar 1982", "order": 2},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 108},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1641111", "name": "Sabrina Louise Narivanchik", "born": "6 Sep 1971"},
        {"code": "1641112", "name": "Theodore (Teddy) Ralph Narivanchik Jr.", "born": "4 Apr 1973"},
        {"code": "1641113", "name": "William (Billy) Ralph Narivanchik", "born": "30 Jul 1979", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "164112",
    "name": "Paul Joseph Narivanchik",
    "sex": "M",
    "born": "14 Sep 1954",
    "spouses": [{"name": "Patricia (Pat) Ann Ruckle Sonntag", "born": "26 Oct 1942", "married": "9 May 1981"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 109},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1641121", "name": "Kara Elizabeth Sonntag", "born": "2 Jul 1962", "flags": {"stepChild": True}, "verified_terminal": True},
        {"code": "1641122", "name": "Alicia Marie Sonntag", "born": "1 Jul 1963", "flags": {"stepChild": True}, "verified_terminal": True},
        {"code": "1641123", "name": "Adam Edward Sonntag", "born": "4 Aug 1970", "flags": {"stepChild": True}, "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "164113",
    "name": "Linda Mae Narivanchik",
    "sex": "F",
    "born": "2 Jan 1957",
    "spouses": [
        {"name": "Robert (Bob) Joseph Yingling Jr.", "born": "10 Jan 1945", "married": "17 Oct 1965", "order": 1},
        {"name": "Donald Edwards", "born": "17 Oct 1942", "married": "17 Apr 1980", "order": 2},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 109},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1641131", "name": "Robert Joseph Yingling III", "born": "28 May 1976", "verified_terminal": True},
        {"code": "1641132", "name": "Kimberlie Mae Edwards", "born": "13 Feb 1979", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "164222",
    "name": "Ruth Ellen Pike",
    "sex": "F",
    "born": "5 Feb 1970",
    "spouses": [{"name": "Larry Lee"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 109},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1642221", "name": "Jessica Lee", "born": "1988", "verified_terminal": True},
        {"code": "1642222", "name": "Larry Travis Lee", "born": "2 Nov 1992", "verified_terminal": True},
        {"code": "1642223", "name": "Anthony Dale Ranson", "born": "12 Oct 1993", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "164231",
    "name": "Deborah Louise Kisasonak",
    "sex": "F",
    "born": "6 May 1969",
    "spouses": [{"name": "Harry James Peterman", "born": "10 Jan 1970", "married": "20 Aug 1989"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 109},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1642311", "name": "Joel Joseph Peterman", "born": "17 Apr 1989", "verified_terminal": True},
        {"code": "1642312", "name": "Shelley Peterman", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "164711",
    "name": "Kathleen (Kathy) Denise Harshbarger",
    "sex": "F",
    "born": "15 Sep 1957",
    "spouses": [{"name": "Randall Ray Myers", "born": "27 Sep 1954", "married": "28 Oct 1978"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 109},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1647111", "name": "Anessa Teanne Myers", "born": "25 Aug 1985", "verified_terminal": True},
        {"code": "1647112", "name": "Thomas Chisholm (TC) Myers", "born": "2 Jan 1988", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "164832",
    "name": "Christina Marie Stevanus",
    "sex": "F",
    "born": "18 Aug 1969",
    "spouses": [
        {"name": "Romesbery", "order": 1},
        {"name": "Suter", "order": 2},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 109},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1648321", "name": "William James Romesbery", "verified_terminal": True},
        {"code": "1648322", "name": "Kelsey Renee Suter", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "164833",
    "name": "Kathleen Renee Stevanus",
    "sex": "F",
    "born": "16 Apr 1971",
    "spouses": [{"name": "Robert Ohler"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 109},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1648331", "name": "Amber Dawn Ohler", "born": "13 May 1987", "verified_terminal": True},
        {"code": "1648332", "name": "Robert Ohler", "born": "11 Mar 1989", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "166211",
    "name": "Charlene Rea Hileman",
    "sex": "F",
    "born": "9 Jan 1947",
    "spouses": [{"name": "Allen M. Bunda", "born": "14 Sep 1945", "married": "12 Jul 1966"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 109},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1662111", "name": "Jeffrey Allen Bunda", "born": "8 Dec 1980", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "166212",
    "name": "Cynthia Lee Hileman",
    "sex": "F",
    "born": "20 Apr 1951",
    "spouses": [{"name": "John Andrew Balogh", "born": "23 Jul 1949", "married": "23 Jun 1973"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 109},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1662121", "name": "Jennifer Lee Balogh", "born": "28 Jul 1985", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "166213",
    "name": "Charles Ray Hileman II",
    "sex": "M",
    "born": "14 Feb 1954",
    "spouses": [
        {"name": "Diane Marie Haky", "born": "30 Nov 1954", "married": "2 Jun 1973", "order": 1},
        {"name": "Susan L. Marks", "married": "28 Nov 1980", "order": 2},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 110},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1662131", "name": "Laura Nicole Hileman", "born": "2 Dec 1975", "verified_terminal": True},
        {"code": "1662132", "name": "Jillian Jo Hileman", "born": "8 May 1981", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "166214",
    "name": "Susan Marie Hileman",
    "sex": "F",
    "born": "13 Dec 1958",
    "spouses": [
        {"name": "Joseph Edward Cindric", "born": "9 Aug 1959", "married": "26 Aug 1978", "order": 1},
        {"name": "Charles (Chuck) E. Nichols Jr.", "married": "2 May 1987", "order": 2},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 110},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1662141", "name": "Heather Marie Cindric", "born": "12 Jun 1980", "verified_terminal": True},
        {"code": "1662142", "name": "Matthew Edward Nichols", "born": "21 Feb 1990", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "166215",
    "name": "Melissa Ann Hileman",
    "sex": "F",
    "born": "5 Nov 1961",
    "spouses": [
        {"name": "Amos Lewis", "born": "10 Sep 1958", "married": "4 Jun 1977", "order": 1},
        {"name": "James Smallwood", "order": 2},
        {"name": "Brady Walker", "order": 3},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 110},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1662151", "name": "Rochelle Marie Lewis", "born": "12 Nov 1977"},
        {"code": "1662152", "name": "Amos Lewis", "born": "5 Oct 1979", "verified_terminal": True},
        {"code": "1662153", "name": "Shannon Lee Smallwood", "born": "5 Jul 1985", "verified_terminal": True},
        {"code": "1662154", "name": "James Ray Smallwood", "born": "19 Feb 1988", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "166221",
    "name": "Tami Lynn Hileman",
    "sex": "F",
    "born": "28 Jan 1960",
    "spouses": [{"name": "Michael Richard Messner", "born": "11 May 1957", "married": "21 Jul 1979"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 110},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1662211", "name": "Mirelle Tiffany Messner", "born": "22 May 1982", "verified_terminal": True},
        {"code": "1662212", "name": "Teal Michelle Messner", "born": "26 Aug 1987", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "166222",
    "name": "Terah Lee Hileman",
    "sex": "F",
    "born": "3 Apr 1963",
    "spouses": [{"name": "Seephen E. Reed", "born": "27 Dec 1961", "married": "3 Sep 1988"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 110},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1662221", "name": "Garrett Steven Reed", "born": "2 Aug 1993", "verified_terminal": True},
        {"code": "1662222", "name": "Savannah Lee Reed", "born": "3 Jun 1995", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "166312",
    "name": "Patricia Ann Summers",
    "sex": "F",
    "born": "13 Apr 1957",
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 110},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1663121", "name": "Chad David Summers", "born": "23 Mar 1977", "verified_terminal": True},
    ],
})


# === Pages 111-115 vision pass (2026-06-07): 172xxx Guthrie/Seese/Ritchey gen 7/8 ===
ENTRIES.append({
    "code": "171351",
    "name": "Gladys Kay Duncan",
    "sex": "F",
    "born": "7 Sep 1946",
    "spouses": [
        {"name": "Thomas H. Mosher", "married": "22 Nov 1969", "order": 1},
        {"name": "Carlos Spears", "married": "23 Mar 1975", "order": 2},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 112},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1713511", "name": "Timothy Thomas Mosher", "born": "14 Jul 1970"},
    ],
})

ENTRIES.append({
    "code": "172111",
    "name": "Genevieve Caroline Guthrie",
    "sex": "F",
    "born": "5 Jan 1933",
    "spouses": [{"name": "Charles I. Swauger", "born": "2 Apr 1913", "married": "1 Jul 1950"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 112},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1721111", "name": "Carol Ann Swauger", "born": "4 Sep 1951", "verified_terminal": True},
        {"code": "1721112", "name": "Betty Jo Swauger", "born": "21 Jan 1954"},
        {"code": "1721113", "name": "Marilyn Sue Swauger", "born": "17 Apr 1955"},
        {"code": "1721114", "name": "Delma Louise Swauger", "born": "9 Dec 1957"},
    ],
})

ENTRIES.append({
    "code": "172112",
    "name": "James Franklin Guthrie",
    "sex": "M",
    "born": "11 Sep 1934",
    "spouses": [{"name": "Lillian Durst", "born": "7 Apr 1945", "married": "11 May 1963"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 112},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1721121", "name": "Dale Eugene Guthrie", "born": "11 Nov 1963"},
        {"code": "1721122", "name": "Cheryl Ann Guthrie", "born": "19 Nov 1964"},
        {"code": "1721123", "name": "James Franklin Guthrie, Jr.", "born": "19 Feb 1966", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "172114",
    "name": "Robert Dale Guthrie",
    "sex": "M",
    "born": "13 Jun 1936",
    "spouses": [{"name": "Elsie Mae Spiker", "born": "18 May 1939", "married": "25 Nov 1960"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 112},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1721141", "name": "William Dale Guthrie", "born": "31 Jul 1962", "verified_terminal": True},
        {"code": "1721142", "name": "Gladys May Guthrie", "born": "19 May 1964", "verified_terminal": True},
        {"code": "1721143", "name": "George Glenn Guthrie", "verified_terminal": True},
        {"code": "1721144", "name": "Kimberly Jean Guthrie", "verified_terminal": True},
        {"code": "1721145", "name": "Rebecca Lynn Guthrie", "born": "15 Oct 1970", "died": "11 Jul 1980", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "172115",
    "name": "Viola Marie Guthrie",
    "sex": "F",
    "born": "10 Jul 1937",
    "spouses": [{"name": "Herbert Blaine (Buck) Hixon", "born": "20 Feb 1926", "married": "27 May 1954"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 112},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1721151", "name": "Peggy Marie Hixon", "born": "10 Jul 1955"},
        {"code": "1721152", "name": "Donna June Hixon", "born": "6 Nov 1956", "died": "20 Jan 1957", "flags": {"diedInInfancy": True}, "verified_terminal": True},
        {"code": "1721153", "name": "Gary Blaine Hixon", "born": "12 Jun 1958", "died": "13 Jun 1958", "flags": {"diedInInfancy": True}, "verified_terminal": True},
        {"code": "1721154", "name": "Robert Ray (Bobby) Hixon", "born": "23 Sep 1961", "verified_terminal": True},
        {"code": "1721155", "name": "Pamela Sue Hixon", "born": "11 Oct 1963", "verified_terminal": True},
        {"code": "1721156", "name": "Jeffrey Lee Hixon", "born": "6 Oct 1966"},
        {"code": "1721157", "name": "David Lynn Hixon", "born": "24 Oct 1968", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "172116",
    "name": "Delbert Glenn Guthrie",
    "sex": "M",
    "born": "1 Sep 1938",
    "spouses": [{"name": "Rita Ann Garlitz"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 113},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1721161", "name": "Tammie Guthrie", "born": "11 Oct 1967", "died": "11 Nov 1967", "flags": {"diedInInfancy": True}, "verified_terminal": True},
        {"code": "1721162", "name": "Tina Marie Guthrie", "born": "5 Dec 1968"},
        {"code": "1721163", "name": "Amy Sue Guthrie", "born": "27 Dec 1969"},
    ],
})

ENTRIES.append({
    "code": "172118",
    "name": "Thelma Jean Guthrie",
    "sex": "F",
    "born": "6 Nov 1940",
    "spouses": [{"name": "Donald Russell", "married": "7 Mar 1959"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 113},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1721181", "name": "Donald Lee Russell, Jr.", "born": "26 Aug 1959", "verified_terminal": True},
        {"code": "1721182", "name": "Gary DeWayne Russell", "born": "28 Oct 1961"},
        {"code": "1721183", "name": "Melissa Ellen Russell", "born": "14 Nov 1973", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "172119",
    "name": "Harvey Paul Guthrie",
    "sex": "M",
    "born": "14 Nov 1941",
    "spouses": [
        {"name": "Rosie McKenzie", "married": "1965", "order": 1},
        {"name": "Shawn Ann Fewster", "married": "24 Dec 1976", "order": 2},
        {"name": "Terri Miller", "born": "11 Oct 1963", "married": "27 Jul 1983", "order": 3},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 113},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1721191", "name": "Charles Ray Guthrie", "born": "21 May 1966", "verified_terminal": True},
        {"code": "1721192", "name": "Patricia Ann Guthrie", "verified_terminal": True},
        {"code": "1721193", "name": "John Henry Guthrie", "verified_terminal": True},
        {"code": "1721194", "name": "Harvey Paul Guthrie, Jr.", "verified_terminal": True},
        {"code": "1721195", "name": "Nicole Ann Guthrie", "born": "14 Jan 1984", "verified_terminal": True},
        {"code": "1721196", "name": "Rebecca Marie Guthrie", "born": "25 Jan 1985", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "17211A",
    "name": "Betty Ruth Guthrie",
    "sex": "F",
    "born": "22 Jun 1943",
    "died": "15 Dec 1988",
    "spouses": [{"name": "Samuel Isabel"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 113},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "17211A1", "name": "Roger Allen Guthrie", "born": "4 Sep 1959", "died": "19 Dec 1978", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "17211B",
    "name": "Carl Lee Guthrie",
    "sex": "M",
    "born": "27 Feb 1945",
    "spouses": [{"name": "Jo Ann Bowser", "born": "27 Aug 1949", "married": "9 Mar 1968"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 113},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "17211B1", "name": "Carl Joseph Guthrie", "born": "31 Jan 1968", "verified_terminal": True},
        {"code": "17211B2", "name": "Christina Lynn Guthrie", "born": "11 May 1971", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "17211D",
    "name": "Helen Ann Guthrie",
    "sex": "F",
    "born": "23 Oct 1949",
    "spouses": [{"name": "Robert Ray Fike", "married": "29 Jun 1979"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 113},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "17211D1", "name": "Susan Michella Fike", "born": "25 Jun 1977", "verified_terminal": True},
        {"code": "17211D2", "name": "Beth Ann Fike", "born": "3 Jan 1979", "verified_terminal": True},
        {"code": "17211D3", "name": "Samantha Mae Fike", "born": "29 Dec 1980", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "17211E",
    "name": "Linda Sue Guthrie",
    "sex": "F",
    "born": "5 Aug 1951",
    "spouses": [{"name": "Keith Galloway", "married": "22 Dec 1975"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 113},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "17211E1", "name": "Julia Pearl Galloway", "born": "23 Jun 1978", "verified_terminal": True},
        {"code": "17211E2", "name": "Myron Scott Galloway", "born": "18 May 1982", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "172121",
    "name": "James W. Seese",
    "sex": "M",
    "born": "6 Aug 1930",
    "spouses": [{"name": "Roberta Louise Goldsborough", "born": "10 Apr 1937", "married": "27 Feb 1957"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 113},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1721211", "name": "Anita Ann Seese", "born": "15 Aug 1957"},
        {"code": "1721212", "name": "Kevin Luke Seese", "born": "31 Jan 1959"},
    ],
})

ENTRIES.append({
    "code": "172122",
    "name": "Thelma Mae Seese",
    "sex": "F",
    "born": "1 Dec 1932",
    "spouses": [{"name": "Curtis Hoover Wolfe", "born": "2 Apr 1929", "married": "20 Oct 1952"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 114},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1721221", "name": "Cindy Diane Wolfe", "born": "23 Nov 1953"},
        {"code": "1721222", "name": "Christine Mae Wolfe", "born": "7 Jan 1955", "died": "7 Jan 1955", "flags": {"diedInInfancy": True}, "verified_terminal": True},
        {"code": "1721223", "name": "Steven Curtis Wolfe", "born": "27 Sep 1956", "verified_terminal": True},
        {"code": "1721224", "name": "Daniel Thurman Wolfe", "born": "8 Jan 1965"},
        {"code": "1721225", "name": "Misty Ruth Wolfe", "born": "20 Oct 1970", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "172123",
    "name": "Thomas Ray Seese",
    "sex": "M",
    "born": "23 Nov 1943",
    "spouses": [{"name": "Sheila (Cookie) Savage", "born": "5 Feb 1948", "married": "5 Jun 1965"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 114},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1721231", "name": "Thomas Ray Seese, Jr.", "born": "11 May 1966", "died": "15 Oct 1994", "verified_terminal": True},
        {"code": "1721232", "name": "Jeffrey Howard Seese", "born": "14 Sep 1969", "verified_terminal": True},
        {"code": "1721233", "name": "Brian Lee Seese", "born": "11 Mar 1972", "died": "15 Oct 1994", "verified_terminal": True},
        {"code": "1721234", "name": "Susan Rae Seese", "born": "5 Feb 1978", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "172124",
    "name": "Dale Franklin Seese",
    "sex": "M",
    "born": "28 May 1949",
    "spouses": [
        {"name": "Margaret Ann Jordan", "married": "15 Jun 1974", "order": 1},
        {"name": "Bonnie Marie Riffle", "born": "1956", "married": "Sep 1977", "order": 2},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 114},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1721241", "name": "Justin William Seese", "born": "10 Dec 1979", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "172125",
    "name": "David Henry Seese",
    "sex": "M",
    "born": "3 Sep 1950",
    "spouses": [{"name": "Sheila Jean Pretzel", "born": "23 Dec 1955"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 114},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1721251", "name": "David Shawn Seese", "born": "16 Nov 1973"},
        {"code": "1721252", "name": "Gregory Alan Seese", "born": "3 May 1976", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "172126",
    "name": "Mark Lee Seese",
    "sex": "M",
    "born": "21 Apr 1954",
    "spouses": [
        {"name": "Laura Lee Niner", "born": "1959", "married": "2 Jan 1976", "order": 1},
        {"name": "Ellen Bucklew", "born": "19 Apr 1965", "married": "8 Dec 1984", "order": 2},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 114},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1721261", "name": "Christopher Lee Seese", "born": "14 Jun 1976", "verified_terminal": True},
        {"code": "1721262", "name": "Joseph Bryson Seese", "born": "4 Aug 1977", "verified_terminal": True},
        {"code": "1721263", "name": "Courtney Nicole Seese", "born": "15 Jul 1986", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "172131",
    "name": "Frances Elaine Ritchey",
    "sex": "F",
    "born": "19 Jun 1934",
    "spouses": [{"name": "Ralph Rucinski", "born": "17 Jun 1932", "died": "4 Apr 1977", "married": "19 Sep 1957"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 114},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1721311", "name": "Faye Diana Rucinski", "born": "29 Apr 1960"},
    ],
})

ENTRIES.append({
    "code": "172132",
    "name": "Donald Ray Ritchey",
    "sex": "M",
    "born": "3 Oct 1935",
    "spouses": [{"name": "Delma Summers", "born": "3 Oct 1935", "married": "30 Jun 1957"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 114},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1721321", "name": "Donald Ray Ritchey, Jr.", "born": "7 May 1958", "verified_terminal": True},
        {"code": "1721322", "name": "Rodney Wayne Ritchey", "born": "27 Dec 1959"},
        {"code": "1721323", "name": "Andrea Sue Ritchey", "born": "10 Jan 1964", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "172133",
    "name": "Jane Louise Ritchey",
    "sex": "F",
    "born": "11 Sep 1937",
    "died": "24 Oct 1995",
    "spouses": [{"name": "William Moore", "married": "30 Mar 1957"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 114},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1721331", "name": "Roger Lee Moore", "born": "1 Jul 1959", "verified_terminal": True},
        {"code": "1721332", "name": "William Dean Moore", "born": "16 Oct 1962", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "172134",
    "name": "Susie Alberta Ritchey",
    "sex": "F",
    "born": "16 Sep 1939",
    "spouses": [{"name": "Donald Hogue", "married": "29 Sep 1959"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 115},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1721341", "name": "Donna Sue Hogue", "born": "21 Dec 1965", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "172135",
    "name": "Delmore George Ritchey",
    "sex": "M",
    "born": "17 Nov 1942",
    "spouses": [{"name": "Lillian Hannah Curry", "born": "17 Jan 1943", "married": "19 Jun 1964"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 115},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1721351", "name": "Sherri Lee Ritchey", "born": "28 Mar 1965"},
    ],
})

ENTRIES.append({
    "code": "172136",
    "name": "Kenneth Dale Ritchey",
    "sex": "M",
    "born": "25 Nov 1944",
    "spouses": [{"name": "Brenda Gail Silcox", "born": "19 Oct 1948", "married": "6 May 1967"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 115},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1721361", "name": "Michael Dale Ritchey", "born": "16 Sep 1968"},
        {"code": "1721362", "name": "Adam Shane Ritchey", "born": "7 Aug 1972", "verified_terminal": True},
        {"code": "1721363", "name": "Eric Mathew Ritchey", "born": "27 May 1977", "verified_terminal": True},
        {"code": "1721364", "name": "Amy Michelle Ritchey", "born": "9 Oct 1979", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "172137",
    "name": "Dennis Blaine Ritchey",
    "sex": "M",
    "born": "18 Feb 1954",
    "spouses": [{"name": "Mary Putaturo", "born": "22 Aug 1955", "married": "18 Jan 1974"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 115},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1721371", "name": "David Christopher Ritchey", "born": "12 Mar 1982", "verified_terminal": True},
        {"code": "1721372", "name": "Daniel Patrick Ritchey", "born": "4 Sep 1984", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "172142",
    "name": "Ruth Irene McNair",
    "sex": "F",
    "born": "29 Feb 1944",
    "spouses": [
        {"name": "John Robert Childers", "born": "21 Jan 1944", "married": "25 Jan 1963", "order": 1},
        {"name": "James David Sweeney", "born": "12 May 1945", "married": "15 Jun 1976", "order": 2},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 115},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1721421", "name": "Teresa Jane Childers", "born": "14 Dec 1965", "verified_terminal": True},
        {"code": "1721422", "name": "Cathleen Marie Childers", "born": "7 Mar 1967", "verified_terminal": True},
        {"code": "1721423", "name": "Deborah Louise Childers", "born": "19 Jun 1968", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "172143",
    "name": "Donald Ray McNair",
    "sex": "M",
    "born": "5 Feb 1947",
    "spouses": [{"name": "Kathy Butler", "married": "31 May 1975"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 115},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1721431", "name": "Andrew James McNair", "born": "15 Aug 1977", "verified_terminal": True},
        {"code": "1721432", "name": "Randall Ray McNair", "born": "15 Aug 1977", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "172144",
    "name": "Dortha Jean McNair",
    "sex": "F",
    "born": "26 May 1948",
    "spouses": [
        {"name": "Roy Butler", "order": 1},
        {"name": "David Glisan", "born": "17 Jan 1955", "married": "14 Jul 1990", "order": 2},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 115},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1721441", "name": "Roger Lee Butler", "born": "15 Sep 1967", "verified_terminal": True},
        {"code": "1721442", "name": "Roy Lee Butler", "born": "9 Sep 1968", "died": "30 Oct 1988", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "172145",
    "name": "Pauline (Polly) Ann McNair",
    "sex": "F",
    "born": "17 Apr 1951",
    "spouses": [
        {"name": "Ralph Butler", "born": "12 Oct 1948", "married": "1969", "order": 1},
        {"name": "James William Ulderich", "born": "23 May 1942", "married": "30 May 1977", "order": 2},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 115},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1721451", "name": "Sue Ann Butler", "born": "17 Apr 1969", "verified_terminal": True},
        {"code": "1721452", "name": "Karen Lynn Butler", "born": "23 Jul 1970", "verified_terminal": True},
        {"code": "1721453", "name": "Kelley Sue Butler", "born": "20 Dec 1975", "verified_terminal": True},
        {"code": "1721454", "name": "Donald James Ulderich", "born": "19 Mar 1978", "verified_terminal": True},
        {"code": "1721455", "name": "Joseph Roy Ulderich", "born": "8 Jan 1980", "verified_terminal": True},
        {"code": "1721456", "name": "Fred Allen Ulderich", "born": "5 Feb 1983", "verified_terminal": True},
        {"code": "1721457", "name": "Samantha", "born": "23 Jul 1987", "verified_terminal": True},
    ],
})


# === Pages 116-120 vision pass (2026-06-07): Boyd/Lightner/Sheppard/Guthrie/Lavens/Miller/Bartholomew/Habenicht/Hale ===
ENTRIES.append({
    "code": "172151",
    "name": "Shirley Jane Boyd",
    "sex": "F",
    "born": "4 Dec 1937",
    "spouses": [{"name": "Harry David Harawitz", "born": "9 Apr 1939", "married": "4 May 1962"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 116},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1721511", "name": "Sharon Elaine Harawitz", "born": "31 May 1963", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "172153",
    "name": "Nelda Mae Boyd",
    "sex": "F",
    "born": "5 Jul 1942",
    "spouses": [{"name": "Gerald Martin Mauthe", "born": "24 Sep 1937", "married": "29 Jul 1961"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 116},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1721531", "name": "Gerald Mark Mauthe", "born": "1 Feb 1962", "verified_terminal": True},
        {"code": "1721532", "name": "Kathy Ann Mauthe", "born": "1 Jun 1965", "verified_terminal": True},
        {"code": "1721533", "name": "Wesley Robert Mauthe", "born": "8 Nov 1968", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "172154",
    "name": "Linda Rae Boyd",
    "sex": "F",
    "born": "25 Mar 1945",
    "spouses": [{"name": "Donald Stewer", "married": "23 Jan 1964"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 116},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1721541", "name": "Donald Joseph Stewer", "born": "24 Aug 1957", "verified_terminal": True},
        {"code": "1721542", "name": "Rodney Lee Stewer", "born": "7 Sep 1965", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "172611",
    "name": "Wendy Ann Guthrie",
    "sex": "F",
    "born": "3 Nov 1956",
    "spouses": [{"name": "Richard Preston Jefferies", "born": "20 Dec 1957", "married": "21 May 1983"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 116},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1726111", "name": "Timothy Preston Jefferies", "born": "3 Mar 1987", "verified_terminal": True},
        {"code": "1726112", "name": "Amanda Marie Jefferies", "born": "28 Feb 1990", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "172612",
    "name": "Clair Edward Guthrie",
    "sex": "M",
    "born": "22 Sep 1961",
    "spouses": [{"name": "Brenda Eileen Wertz", "born": "5 Feb 1968", "married": "23 Jul 1993"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 116},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1726121", "name": "Clair (CJ) Edward Guthrie, Jr.", "born": "19 Jul 1996", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "172613",
    "name": "Alvin Loyd Guthrie",
    "sex": "M",
    "born": "19 Aug 1968",
    "spouses": [{"name": "Wandy Kay Fraizer", "born": "23 Jul 1968", "married": "20 Apr 1996"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 116},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1726131", "name": "Cody Lewis Lacy", "born": "15 Dec 1992", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "172622",
    "name": "Dennis Reckart",
    "sex": "M",
    "born": "22 Jul 1953",
    "spouses": [{"name": "Katherine Sypolt", "married": "8 Sep 1973"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 117},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1726221", "name": "Lisa Dawn Reckart", "born": "4 Jan 1974", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "172821",
    "name": "Linda Joyce Lightner",
    "sex": "F",
    "born": "9 May 1947",
    "spouses": [
        {"name": "James W. Pickett", "married": "7 May 1966", "order": 1},
        {"name": "Robert James", "married": "27 Sep 1985", "order": 2},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 118},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1728211", "name": "Lincoln Lewis Pickett", "born": "7 Apr 1968", "verified_terminal": True},
        {"code": "1728212", "name": "Ashleigh Nicole James", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "172822",
    "name": "Douglas Lightner, Jr.",
    "sex": "M",
    "born": "25 Jan 1949",
    "spouses": [{"name": "Judy", "married": "16 Sep 1974"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 118},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1728221", "name": "Christina Alexandra Lightner", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "172823",
    "name": "Roger Dale Lightner",
    "sex": "M",
    "born": "29 Dec 1951",
    "died": "31 May 1987",
    "spouses": [{"name": "Sheryl Knotts"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 118},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1728231", "name": "Roxanna Kay Lightner", "born": "15 Nov 1969", "verified_terminal": True},
        {"code": "1728232", "name": "Rodger Dale Lightner", "born": "6 Oct 1971", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "172831",
    "name": "Gwendlyn Redeen Sheppard",
    "sex": "F",
    "born": "31 Oct 1949",
    "spouses": [
        {"name": "Gary Evans", "order": 1},
        {"name": "Randy Wayne Moyers", "born": "12 Nov 1952", "order": 2},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 118},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1728311", "name": "Renee Michelle Evans", "born": "21 Nov 1969", "verified_terminal": True},
        {"code": "1728312", "name": "Aaron Troy Moyers, Jr.", "born": "23 Jul 1977", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "172841",
    "name": "Debra Suzanna Guthrie",
    "sex": "F",
    "born": "30 Jun 1953",
    "spouses": [{"name": "Kerry D. Uber", "married": "9 Jun 1973"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 118},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1728411", "name": "Grant Andrew Uber", "born": "7 Jul 1983", "verified_terminal": True},
        {"code": "1728412", "name": "Bethany Elizabeth Uber", "born": "Feb 1992", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "172842",
    "name": "Dwight David Guthrie",
    "sex": "M",
    "born": "27 Sep 1954",
    "spouses": [
        {"name": "Patricia Ann Buckner", "married": "1976", "order": 1},
        {"name": "Diane Theresa Bukouac", "born": "6 Dec 1955", "married": "12 Aug 1983", "order": 2},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 118},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1728421", "name": "Christie Brooke Guthrie", "born": "4 Jul 1985", "verified_terminal": True},
        {"code": "1728422", "name": "David Justin Guthrie", "born": "9 Sep 1986", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "172843",
    "name": "Michael Dane Guthrie",
    "sex": "M",
    "born": "2 Jun 1957",
    "occupation": "Free Methodist Minister",
    "spouses": [{"name": "Catherine (Kathy) Wight", "born": "15 Jan 1958", "married": "24 Jun 1978"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 118},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1728431", "name": "Joshua Aaron Guthrie", "born": "3 Jun 1981", "verified_terminal": True},
        {"code": "1728432", "name": "Rebekah Joy Guthrie", "born": "11 Nov 1986", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "172844",
    "name": "Darryl Lee Guthrie",
    "sex": "M",
    "born": "7 Dec 1959",
    "spouses": [{"name": "Jill Heintz"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 118},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1728441", "name": "Troy Jacob Guthrie", "born": "3 Jun 1987", "verified_terminal": True},
        {"code": "1728442", "name": "Taylor Leigh Guthrie", "born": "4 Jul 1990", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "172B21",
    "name": "Bonnie Jean Lavens",
    "sex": "F",
    "born": "11 Jan 1946",
    "spouses": [
        {"name": "Ronald Lee Gaines", "married": "16 Apr 1966", "order": 1},
        {"name": "Walter Reiling", "order": 2},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 118},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "172B211", "name": "Jeanette Lee Gaines", "born": "9 Mar 1972", "verified_terminal": True},
        {"code": "172B212", "name": "Jeffrey Thomas Gaines", "born": "17 Dec 1974", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "172B32",
    "name": "Joy Irene Miller",
    "sex": "F",
    "born": "18 Apr 1952",
    "spouses": [{"name": "Patrick E. Thompson", "born": "7 Apr 1945", "married": "18 Mar 1973"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 119},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "172B321", "name": "Andrea May Thompson", "born": "31 May 1974", "verified_terminal": True},
        {"code": "172B322", "name": "Jamie Nicholas Thompson", "born": "21 Feb 1976", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "172B33",
    "name": "Lori Jean Miller",
    "sex": "F",
    "born": "29 Sep 1955",
    "spouses": [
        {"name": "Frad Hall", "order": 1},
        {"name": "William Keith Lemieux, Jr.", "born": "24 Feb 1965", "married": "28 Jun 1986", "order": 2},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 119},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "172B331", "name": "J. Trevor Hall", "born": "14 Aug 1991", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "172B41",
    "name": "Daniel Paul Bartholomew",
    "sex": "M",
    "born": "18 Jul 1951",
    "spouses": [{"name": "Donna Lea Thorpe", "born": "17 Jan 1953", "married": "1 Jun 1974"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 119},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "172B411", "name": "Aaron Eugene Bartholomew", "born": "28 Nov 1979", "verified_terminal": True},
        {"code": "172B412", "name": "Elizabeth Ann Bartholomew", "born": "19 Jun 1982", "verified_terminal": True},
        {"code": "172B413", "name": "Sarah Sun Hee Bartholomew", "born": "12 Jun 1984", "verified_terminal": True},
        {"code": "172B414", "name": "Leah Hoo Hee Bartholomew", "born": "12 Jun 1984", "verified_terminal": True},
        {"code": "172B415", "name": "Rachelle Rockelle Bartholomew", "born": "9 Dec 1986", "verified_terminal": True},
        {"code": "172B416", "name": "Noah Rocky Daniel Bartholomew", "born": "9 Dec 1986", "verified_terminal": True},
        {"code": "172B417", "name": "Rebekah Rocklene Bartholomew", "born": "9 Dec 1986", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "172B42",
    "name": "Karen Geniese Bartholomew",
    "sex": "F",
    "born": "3 Aug 1953",
    "spouses": [{"name": "Neil Dennis Lindquist", "born": "17 Oct 1951", "married": "13 Jan 1978"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 119},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "172B421", "name": "Kyle Don Lindquist", "born": "6 Apr 1979", "verified_terminal": True},
        {"code": "172B422", "name": "Adam Paul Lindquist", "born": "24 Jul 1981", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "172B43",
    "name": "Timothy Eugene Bartholomew",
    "sex": "M",
    "born": "6 Jun 1957",
    "spouses": [{"name": "Donna J. DiMaggio", "married": "17 Aug 1979"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 119},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "172B431", "name": "Danielle M. Bartholomew", "born": "13 Apr 1983", "verified_terminal": True},
        {"code": "172B432", "name": "Zachary J. Bartholomew", "born": "28 Sep 1985", "verified_terminal": True},
        {"code": "172B433", "name": "Breanna Lannelle Bartholomew", "born": "5 Oct 1990", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "172B51",
    "name": "Valerie Kay Habenicht",
    "sex": "F",
    "born": "1 Dec 1953",
    "spouses": [{"name": "Roger Paul Busse", "born": "1 Mar 1953", "married": "8 Jun 1974"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 119},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "172B511", "name": "Katherine Ann Busse", "born": "14 Feb 1978", "verified_terminal": True},
        {"code": "172B512", "name": "Kelty Elizabeth Busse", "born": "25 Apr 1980", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "172B52",
    "name": "Bradley Phillip Habenicht",
    "sex": "M",
    "born": "20 Sep 1956",
    "spouses": [{"name": "Marla Jo Flynn", "born": "1 May 1956", "married": "16 May 1980"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 119},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "172B521", "name": "Lauren Flynn Habenicht", "born": "17 Apr 1984", "verified_terminal": True},
        {"code": "172B522", "name": "Kristie Micolle Habenicht", "born": "26 Sep 1987", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "172B61",
    "name": "Douglas Robert Hale",
    "sex": "M",
    "born": "24 Oct 1952",
    "spouses": [{"name": "Linda L. Welskop", "born": "18 Apr 1952", "married": "19 Aug 1972"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 119},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "172B611", "name": "Raynee Sue Hale", "born": "17 Apr 1978", "verified_terminal": True},
        {"code": "172B612", "name": "Benjamen Robert Hale", "born": "2 Mar 1981", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "172B62",
    "name": "Cindy Lou Hale",
    "sex": "F",
    "born": "21 Feb 1959",
    "spouses": [{"name": "Daniel Joseph Klein", "born": "14 Aug 1943", "married": "29 Mar 1980"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 120},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "172B621", "name": "Jeffrey Daniel Klein", "born": "16 May 1983", "verified_terminal": True},
        {"code": "172B622", "name": "William Peter Klein", "born": "5 Jul 1985", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "172B63",
    "name": "Tina Dianne Hale",
    "sex": "F",
    "born": "13 Jan 1971",
    "spouses": [{"name": "Todd Odis Fogelberg", "married": "8 Sep 1990"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 120},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "172B631", "name": "Jacob McKenzie Fogelberg", "born": "2 May 1992", "verified_terminal": True},
        {"code": "172B632", "name": "Jordan Taylor Fogelberg", "born": "3 Jun 1993", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "172B72",
    "name": "Terry Gene Bartholomew",
    "sex": "M",
    "born": "24 May 1963",
    "spouses": [{"name": "Michelle Ray Chipman", "born": "10 Apr 1968", "married": "16 Mar 1985"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 120},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "172B721", "name": "Summer Michelle Bartholomew", "born": "26 Jun 1985", "died": "26 Jun 1985", "flags": {"diedInInfancy": True}, "verified_terminal": True},
        {"code": "172B722", "name": "Tabitha Michelle Bartholomew", "born": "9 Dec 1987", "verified_terminal": True},
        {"code": "172B723", "name": "Nicole Casey Bartholomew", "born": "14 Jul 1989", "verified_terminal": True},
        {"code": "172B724", "name": "Victoria Anne Bartholomew", "born": "22 Apr 1991", "verified_terminal": True},
        {"code": "172B725", "name": "Joshua Walter Edward Bartholomew", "born": "4 Dec 1992", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "172B73",
    "name": "Deborah Annette Bartholomew",
    "sex": "F",
    "born": "11 Jan 1967",
    "spouses": [{"name": "Rod Thomas Jones", "born": "20 Jul 1964", "married": "19 Sep 1987"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 120},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "172B731", "name": "Thomas David Jones", "born": "28 Nov 1990", "verified_terminal": True},
        {"code": "172B732", "name": "Terrance Magnum Jones", "born": "27 May 1993", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "172B74",
    "name": "Dwane Ira Bartholomew",
    "sex": "M",
    "born": "18 Apr 1968",
    "spouses": [{"name": "Carolyn Eileen Berti", "born": "25 Jul 1968", "married": "7 Feb 1988"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 120},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "172B741", "name": "Serena Caress Bartholomew", "born": "25 Nov 1986", "verified_terminal": True},
        {"code": "172B742", "name": "Julia Bliss Bartholomew", "born": "11 May 1989", "verified_terminal": True},
    ],
})


# === Pages 121-125 vision pass (2026-06-07): Shaffer/Friend + JOHN gen 7 (Thomas/Frazee/McNear/Durr/Hoover/DeBerry/Shea/Thomas/Fike) ===
ENTRIES.append({
    "code": "173321",
    "name": "Willard Arnold Shaffer",
    "sex": "M",
    "born": "5 Apr 1929",
    "died": "10 Mar 1964",
    "spouses": [{"name": "Irene Donna Kozlovich", "born": "16 Nov 1930"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 121},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1733211", "name": "Arnold Lee Shaffer", "born": "27 Mar 1951"},
        {"code": "1733212", "name": "Sandra Lee Shaffer", "born": "17 Jul 1952", "verified_terminal": True},
        {"code": "1733213", "name": "Diana Lynn Shaffer", "born": "9 Jul 1958", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "173322",
    "name": "Margaret Virginia Shaffer",
    "sex": "F",
    "born": "22 May 1931",
    "spouses": [
        {"name": "Paul William Early", "born": "4 May 1924", "died": "20 May 1967", "married": "21 Jun 1947", "order": 1},
        {"name": "Willard Harned", "married": "1969", "order": 2},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 121},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1733221", "name": "Kenneth Paul Early", "born": "17 Jun 1949"},
        {"code": "1733222", "name": "Linda Diane Early", "born": "8 Apr 1951"},
        {"code": "1733223", "name": "Robert Jay Early", "born": "12 Jul 1956", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "173323",
    "name": "Robert Ray Shaffer",
    "sex": "M",
    "born": "23 Apr 1934",
    "spouses": [{"name": "Shirley Yvonne Shaffer", "born": "15 Feb 1937", "married": "21 Dec 1953"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 122},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1733231", "name": "Gregory Ray Shaffer", "born": "30 Jul 1955"},
        {"code": "1733232", "name": "James Edward Shaffer", "born": "13 Mar 1957"},
        {"code": "1733233", "name": "Robert Floyd Shaffer", "born": "11 Sep 1960"},
        {"code": "1733234", "name": "Twyla Jean Shaffer", "born": "13 Mar 1962"},
        {"code": "1733235", "name": "Sharon Yvonne Shaffer", "born": "24 Oct 1963", "verified_terminal": True},
        {"code": "1733236", "name": "Ruth Marie Shaffer", "born": "20 Jun 1968", "verified_terminal": True},
        {"code": "1733237", "name": "Charles Allen Shaffer", "born": "23 Oct 1971", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "173351",
    "name": "Virginia Mae Teets",
    "sex": "F",
    "born": "28 Apr 1935",
    "spouses": [{"name": "James Roy (Bud) Jones", "married": "1959"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 122},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1733511", "name": "Susan Diane Jones", "born": "16 Aug 1959", "verified_terminal": True},
        {"code": "1733512", "name": "Phyllis Yvonna Jones", "born": "5 Mar 1961", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "173361",
    "name": "Robert Clinton Friend",
    "sex": "M",
    "born": "27 Aug 1949",
    "spouses": [
        {"name": "Mary Sumpta", "born": "17 Jun 1952", "married": "21 Dec 1974", "order": 1},
        {"name": "Bonnie", "married": "19 Apr 1996", "order": 2},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 122},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1733611", "name": "Robert Clinton Delmar Friend", "born": "17 Feb 1977", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "177252",
    "name": "Sharon Frey",
    "sex": "F",
    "spouses": [{"name": "Roger Keene"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 122},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "1772521", "name": "Kenny Keene", "verified_terminal": True},
    ],
})

# === JOHN - SEVENTH GENERATION starts ===
ENTRIES.append({
    "code": "1131512",
    "name": "Gerald W. Thomas",
    "sex": "M",
    "spouses": [{"name": "Linda Hinebaugh"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 123},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "11315121", "name": "Stephanie DeShea Thomas", "verified_terminal": True},
        {"code": "11315122", "name": "Aaron Samuel Thomas", "born": "17 Jun 1979", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1132221",
    "name": "Kathy Marie Frazee",
    "sex": "F",
    "born": "1 Jun 1956",
    "spouses": [{"name": "Richard James Komanecky", "born": "20 Feb 1956", "married": "5 Sep 1981"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 123},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "11322211", "name": "Andrea Marie Komanecky", "born": "7 Mar 1987", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1132222",
    "name": "Brenda Kay Frazee",
    "sex": "F",
    "born": "24 Aug 1959",
    "spouses": [{"name": "Fred Allen Balsley", "born": "7 Sep 1952"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 123},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "11322221", "name": "Jamie Lynn Balsley", "born": "15 Jun 1985", "verified_terminal": True},
        {"code": "11322222", "name": "Brad Allan Balsley", "born": "26 May 1988", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1224111",
    "name": "Janet Louise McNear",
    "sex": "F",
    "born": "19 Jun 1949",
    "spouses": [{"name": "Roger Lee Livengood", "born": "14 Jun 1948", "married": "14 Jun 1968"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 123},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "12241111", "name": "Sharon LaVonne Livengood", "born": "28 Mar 1971", "verified_terminal": True},
        {"code": "12241112", "name": "Tonya Lea Livengood", "born": "24 Mar 1976", "verified_terminal": True},
        {"code": "12241113", "name": "Roger Lee (RJ) Livengood, Jr.", "born": "11 Jun 1987", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1224112",
    "name": "Sonny Allen McNear",
    "sex": "M",
    "born": "3 Jan 1951",
    "spouses": [{"name": "Judy Lynn Christian", "married": "12 Jun 1970"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 123},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "12241121", "name": "Elizabeth Ellen McNear", "born": "10 May 1971", "verified_terminal": True},
        {"code": "12241122", "name": "Christina Lynn McNear", "born": "7 Dec 1973", "verified_terminal": True},
        {"code": "12241123", "name": "Melanie Jane McNear", "born": "27 Jun 1977", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1224121",
    "name": "Rosa Mary Durr",
    "sex": "F",
    "born": "8 May 1949",
    "spouses": [{"name": "Terry DeVall"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 123},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "12241211", "name": "Bradley Vaughn DeVall", "born": "15 Dec 1969", "verified_terminal": True},
        {"code": "12241212", "name": "Traci Dawn DeVall", "born": "19 Jun 1973", "verified_terminal": True},
        {"code": "12241213", "name": "Tami Ann DeVall", "born": "6 May 1976", "died": "31 Jul 1977", "flags": {"diedInInfancy": True}, "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1224122",
    "name": "Lawrence Junior Durr",
    "sex": "M",
    "born": "27 Jun 1953",
    "died": "19 Dec 1975",
    "spouses": [{"name": "Irene Riley", "married": "Dec 1972"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 123},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "12241221", "name": "Brandy Kay Durr", "born": "9 Oct 1973", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1224123",
    "name": "Kathy Ann Durr",
    "sex": "F",
    "born": "5 Aug 1955",
    "spouses": [{"name": "Victor Selby", "born": "8 Sep 1949", "married": "8 Dec 1973"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 123},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "12241231", "name": "Rebecca Jean Selby", "born": "25 Jun 1974", "verified_terminal": True},
        {"code": "12241232", "name": "Michael Glenn Selby", "born": "22 Mar 1979", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1224125",
    "name": "Timmy Allen Durr",
    "sex": "M",
    "born": "28 Jun 1962",
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 123},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "12241251", "name": "Dusty Durr", "born": "23 Apr 1981", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1224143",
    "name": "Stella Darlene Hoover",
    "sex": "F",
    "born": "14 Aug 1958",
    "spouses": [{"name": "David A. Shaffer", "born": "4 Sep 1955", "married": "29 Oct 1977"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 124},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "12241431", "name": "David S. Shaffer", "born": "11 Feb 1978", "verified_terminal": True},
        {"code": "12241432", "name": "Jessica Shaffer", "born": "11 Oct 1980", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1224144",
    "name": "Brenda Ann Hoover",
    "sex": "F",
    "born": "14 Jun 1960",
    "died": "30 Aug 1990",
    "spouses": [{"name": "William Braham", "married": "11 Sep 1977"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 124},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "12241441", "name": "Shawna Braham", "born": "23 Jan 1978", "verified_terminal": True},
        {"code": "12241442", "name": "Tara Jean Braham", "born": "5 Oct 1983", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1224145",
    "name": "Deborah Belle Hoover",
    "sex": "F",
    "born": "7 Jun 1961",
    "spouses": [{"name": "Marvin Lee Feather", "born": "1 Nov 1961", "married": "15 Jun 1979"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 124},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "12241451", "name": "Christy Dawn Feather", "born": "3 Aug 1979", "verified_terminal": True},
        {"code": "12241452", "name": "Jennifer Rose Feather", "born": "15 May 1982", "verified_terminal": True},
        {"code": "12241453", "name": "Son", "born": "8 Dec 1988", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1224311",
    "name": "Michael Nelson DeBerry",
    "sex": "M",
    "born": "25 Mar 1961",
    "spouses": [{"name": "Carol Ann Frederick", "born": "29 Apr 1962", "married": "29 Dec 1981"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 124},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "12243111", "name": "Jennifer Leanne DeBerry", "born": "21 Nov 1982", "verified_terminal": True},
        {"code": "12243112", "name": "Melissa Sue DeBerry", "born": "27 Feb 1987", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1224312",
    "name": "William (Teddy) Dale DeBerry",
    "sex": "M",
    "born": "6 Apr 1963",
    # Birth place + death/place backfilled from user submission (issue #10).
    "born_place": "HI",
    "died": "26 Apr 2019",
    "died_place": "FL",
    "spouses": [{
        "name": "Kelli Louise Hughs",
        "born": "13 Apr 1965",
        "married": "25 May 1985",
        "married_place": "Wahiawa, Hawaii",
        # Kelli's parents added via issue #7, then enriched and corrected
        # across issues #11, #13, #14–#19. Each ancestor dict can declare:
        #   born/born_place, died/died_place, buried, married/married_place,
        #   father, mother. build.py recursively materializes the lot and
        #   links marriages between paired parents.
        "father": {
            "name": "Ralph Edward Hughs",
            "born": "5 Nov 1924",
            "born_place": "Lucerne, MO",
            "died": "11 Jul 2007",
            "died_place": "Brandon, FL",
            "buried": "Brandon, FL",
            "married": "26 Jun 1947",
            "married_place": "Alexandria, VA",
            # Issue #16 corrected the original "Edward Roland Hughs
            # (1856–1937)" to the right person: William Edward Hughs
            # (1886–1965) of Ravanna / Princeton, MO. Issue #20 then
            # placed Edward Roland Hughs + Flora Jobe one generation up
            # as William Edward's parents (great-great-grandparents of
            # William Teddy's kids). Issues #28 + #29 enriched both
            # those grandparents and added their own parents — the
            # great-great-great-grandparents.
            "father": {
                "name": "William Edward Hughs",
                "born": "10 May 1886",
                "born_place": "Ravanna, MO",
                "died": "25 Jun 1965",
                "died_place": "Princeton, MO",
                "father": {
                    "name": "Edward Roland Hughs",
                    "born": "29 Apr 1856",
                    "born_place": "Lancaster, MO",
                    "died": "31 Mar 1937",
                    "died_place": "Newtown, MO",
                    "married": "1884",
                    # Issue #33 enriched James Moses Hughs and added his
                    # own parents Hudson Hughes + Margaret Robertson
                    # Balfour.
                    "father": {
                        "name": "James Moses Hughs",
                        "born": "1811",
                        "born_place": "VA",
                        "died": "2 Mar 1861",
                        "died_place": "St Louis, MO",
                        "father": {"name": "Hudson Hughes", "born": "1775", "died": "1841"},
                        "mother": {"name": "Margaret Mary Robertson Balfour", "born": "1775", "died": "1820"},
                    },
                    # Issue #32 enriched Elizabeth Betsy Bradburn and
                    # added her parents. Joseph Bradburn's submitted
                    # birth year (1817) is incompatible with Elizabeth's
                    # (1810), so it's omitted until a corrected year is
                    # submitted; Ann Mackley's year stands.
                    "mother": {
                        "name": "Elizabeth Betsy Bradburn",
                        "born": "1810",
                        "born_place": "TN",
                        "died": "1889",
                        "married": "16 Jun 1831",
                        "married_place": "Vermillion, IN",
                        "father": {"name": "Joseph Bradburn", "died": "1881"},
                        "mother": {"name": "Ann Mackley", "born": "1793", "died": "1845"},
                    },
                },
                "mother": {
                    "name": "Florence Elizabeth 'Flora' Jobe",
                    "born": "7 Jan 1865",
                    "born_place": "Newtown, MO",
                    "died": "10 Jan 1910",
                    "died_place": "Newtown, MO",
                    # Issue #31 enriched Joseph W Jobe's dates and #30
                    # enriched Catharine Buress + added her parents.
                    "father": {
                        "name": "Joseph W Jobe",
                        "born": "20 Mar 1838",
                        "born_place": "Cole, MO",
                        "died": "1 Dec 1925",
                        "died_place": "Trenton, MO",
                    },
                    "mother": {
                        "name": "Catharine Buress",
                        "born": "4 Dec 1834",
                        "born_place": "Campbell, TN",
                        "died": "22 Oct 1912",
                        "died_place": "Trenton, MO",
                        "buried": "Newtown, MO",
                        "married": "4 May 1856",
                        "married_place": "Mercer, MO",
                        "father": {"name": "William Burris", "born": "1792", "died": "1840"},
                        "mother": {"name": "Elizabeth Matilda Taylor", "born": "1794", "died": "1862"},
                    },
                },
            },
            # Issue #17 corrected the original "Florence Elizabeth 'Flora'
            # Jobe (1865–1910)" to Alma Lorraine Stout (1887–1942).
            # Issue #21 then added Alma's parents.
            "mother": {
                "name": "Alma Lorraine Stout",
                "born": "30 Nov 1887",
                "born_place": "Newtown, MO",
                "died": "25 Nov 1942",
                "died_place": "Lucerne, MO",
                "father": {"name": "John Stout", "born": "1849", "died": "1935"},
                "mother": {"name": "Laura J Vencil", "born": "1860", "died": "1925"},
            },
        },
        "mother": {
            "name": "Betty Laura Sellman",
            "born": "5 Apr 1925",
            "born_place": "Springfield, OH",
            "died": "25 Oct 1990",
            "died_place": "Brandon, FL",
            "buried": "Brandon, FL",
            "father": {
                "name": "Francis Allen Sellman",
                "born": "9 Jun 1904",
                "born_place": "Luray, VA",
                "died": "28 Feb 1990",
                "died_place": "Bowling Green, OH",
                "buried": "Bowling Green, OH",
                "married": "16 Jun 1924",
                "married_place": "Clark, OH",
                # Issue #22 added Francis's parents. Issue #25 enriched
                # Elizabeth Lee Aleshire and added her own parents (no
                # equivalent enrichment for Oliver Selman yet).
                "father": {"name": "Oliver Selman", "born": "1876", "died": "1916"},
                "mother": {
                    "name": "Elizabeth Lee Aleshire",
                    "born": "13 Oct 1878",
                    "born_place": "Luray, VA",
                    "died": "28 Jan 1965",
                    "died_place": "Baltimore, MD",
                    "buried": "Page, VA",
                    "father": {"name": "Isaac N Short", "born": "1852", "died": "1939"},
                    "mother": {"name": "Arbelia Angeline Aleshire", "born": "1849", "died": "1932"},
                },
            },
            "mother": {
                "name": "Dorothy E Develvis",
                "born": "25 Apr 1903",
                "born_place": "Rosewood, OH",
                "died": "3 May 1953",
                # Issue #19 added Dorothy's parents. Issues #26 + #27
                # enriched Earl and Mary and added their own parents.
                "father": {
                    "name": "Earl Isaac Develvis",
                    "born": "18 Oct 1882",
                    "born_place": "Perry, OH",
                    "died": "9 Jun 1945",
                    "died_place": "Springfield, OH",
                    "married": "11 Jun 1903",
                    "married_place": "Shelby, OH",
                    "father": {"name": "William Francis Develvis", "born": "1850", "died": "1918"},
                    "mother": {"name": "Mollie Reeder"},
                },
                "mother": {
                    "name": "Mary Nancy Hall",
                    "born": "5 May 1885",
                    "born_place": "Springfield, OH",
                    "died": "12 May 1912",
                    "died_place": "Springfield, OH",
                    "father": {"name": "John Hall"},
                    "mother": {"name": "Dorothy Venrich"},
                },
            },
        },
    }],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 124},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-15", "notes": "Updated via user submissions: William Teddy's HI birth + FL death (issue #10), Kelli's parents (issue #7)."},
    "children": [
        # William Dale and Crystal both have their own ENTRIES below for the
        # marriages they carry; we keep the children stubs only to establish
        # the parent→child relationship.
        {"code": "12243121", "name": "William Dale DeBerry", "born": "14 Sep 1986"},
        {"code": "12243122", "name": "Crystal Nicole DeBerry", "born": "12 Jun 1990"},
    ],
})

# ── User submission via family.sudoservers.com (issues #1, #34–#37) ──────────
ENTRIES.append({
    "code": "12243122",
    "name": "Crystal Nicole DeBerry",
    "sex": "F",
    "born": "12 Jun 1990",
    "born_place": "Brandon, FL",
    "spouses": [{
        "name": "David Michael Holloway",
        "born": "11 Aug 1991",
        "born_place": "Salisbury, MD",
        "married": "16 May 2015",
    }],
    "source": {"pdf": "user-submission", "page": None},
    "verification": {
        "status": "verified",
        "source": "user-submission",
        "lastChecked": "2026-06-16",
        "notes": "Submitted by Will DeBerry via family.sudoservers.com (issue #1); spouse details and marriage date added via Crystal Holloway submissions (issues #36, #37); children added via issues #34, #35.",
    },
    "children": [
        {"code": "122431221", "name": "Kayden Michael Holloway", "born": "12 Jul 2012"},
        {"code": "122431222", "name": "Kole Jax Holloway", "born": "10 Feb 2017"},
    ],
})

ENTRIES.append({
    "code": "122431221",
    "name": "Kayden Michael Holloway",
    "sex": "M",
    "born": "12 Jul 2012",
    "born_place": "Brandon, FL",
    "source": {"pdf": "user-submission", "page": None},
    "verification": {
        "status": "verified",
        "source": "user-submission",
        "lastChecked": "2026-06-16",
        "notes": "Submitted by Crystal Holloway via family.sudoservers.com (issue #34).",
    },
})

ENTRIES.append({
    "code": "122431222",
    "name": "Kole Jax Holloway",
    "sex": "M",
    "born": "10 Feb 2017",
    "born_place": "Brandon, FL",
    "source": {"pdf": "user-submission", "page": None},
    "verification": {
        "status": "verified",
        "source": "user-submission",
        "lastChecked": "2026-06-16",
        "notes": "Submitted by Crystal Holloway via family.sudoservers.com (issue #35).",
    },
})

# ── User submissions via family.sudoservers.com (issues #2, #3) ──────────────
# William Dale's two marriages: Janelle Harriette Holdridge (1, deceased) and
# Cassila Batista Carvalho (2).
ENTRIES.append({
    "code": "12243121",
    "name": "William Dale DeBerry",
    "sex": "M",
    "born": "14 Sep 1986",
    "spouses": [
        {
            "name": "Janelle Harriette Holdridge",
            "born": "11 Sep 1976",
            "born_place": "St. Petersburg, FL",
            "died": "26 May 2020",
            "died_place": "Frederick, MD",
            "father": "Kim Holdridge",
            "mother": "Sandy Mastry",
            "married": "21 Dec 2013",
            "married_place": "FL",
            "order": 1,
        },
        {
            "name": "Cassila Batista Carvalho",
            "born": "30 May 1982",
            "born_place": "Brazil",
            "married": "23 Dec 2024",
            "married_place": "Raleigh, NC",
            "order": 2,
            # Cassila's parents added via issues #23 (Jorge) and #24
            # (Rita). Jorge's own parents (Mauro + Alice) were declared
            # in #23 as his parents and recurse one generation up as
            # Cassila's paternal grandparents.
            "father": {
                "name": "Jorge De Carvalho",
                "father": {"name": "Mauro De Carvalho"},
                "mother": {"name": "Alice Nunes Duarte"},
            },
            "mother": {
                "name": "Rita De Cassia Antunes Batista",
            },
        },
    ],
    "source": {"pdf": "user-submission", "page": None},
    "verification": {
        "status": "verified",
        "source": "user-submission",
        "lastChecked": "2026-06-15",
        "notes": "Submitted by Will DeBerry via family.sudoservers.com (issues #2, #3).",
    },
    # Logan is William Dale's bio son with Janelle (issue #5). Joshua (#4) and
    # James Carvalho Sterley (#6) are NOT in this list — they're stepchildren
    # via Janelle's and Cassila's prior relationships, recorded with their
    # accurate biological parents in EXTERNAL_ENTRIES below.
    "children": [
        {"code": "122431211", "name": "Logan Pierce DeBerry", "born": "17 Jul 2011"},
    ],
})

ENTRIES.append({
    "code": "122431211",
    "name": "Logan Pierce DeBerry",
    "sex": "M",
    "born": "17 Jul 2011",
    "born_place": "Safety Harbor, FL",
    "source": {"pdf": "user-submission", "page": None},
    "verification": {
        "status": "verified",
        "source": "user-submission",
        "lastChecked": "2026-06-15",
        "notes": "Submitted by Will DeBerry via family.sudoservers.com (issue #5).",
    },
})


# ─────────────────────────────────────────────────────────────────────────────
# External entries — people whose biological parents we want recorded
# accurately, but who have no place in the Guthrie lineage-code sibling
# system (typically stepchildren via a spouse's prior relationship). Their
# parent_refs match by name (and birth year if given) against existing
# people; unmatched refs are materialized as new "loose" Person records.
# ─────────────────────────────────────────────────────────────────────────────
EXTERNAL_ENTRIES = []

# Issue #4: Joshua Paul Paterno — Janelle Holdridge's son with James Paul
# Paterno, born before her marriage to William Dale DeBerry.
EXTERNAL_ENTRIES.append({
    "name": "Joshua Paul Paterno",
    "sex": "M",
    "born": "14 May 2006",
    "born_place": "Safety Harbor, FL",
    "parent_refs": [
        {"name": "Janelle Harriette Holdridge", "born": "11 Sep 1976"},
        {"name": "James Paul Paterno", "sex": "M", "born": "1974"},
    ],
    "source": {"pdf": "user-submission", "page": None},
    "verification": {
        "status": "verified",
        "source": "user-submission",
        "lastChecked": "2026-06-15",
        "notes": "Submitted by Will DeBerry via family.sudoservers.com (issue #4).",
    },
})

# Issue #6: James Carvalho Sterley — Cassila Batista Carvalho's son with
# Andre Sterley, born before her marriage to William Dale DeBerry.
EXTERNAL_ENTRIES.append({
    "name": "James Carvalho Sterley",
    "born": "1 Aug 2014",
    "born_place": "Stellenbosch, South Africa",
    "parent_refs": [
        {"name": "Cassila Batista Carvalho", "born": "30 May 1982"},
        {"name": "Andre Sterley", "sex": "M", "born": "1982"},
    ],
    "source": {"pdf": "user-submission", "page": None},
    "verification": {
        "status": "verified",
        "source": "user-submission",
        "lastChecked": "2026-06-15",
        "notes": "Submitted by Will DeBerry via family.sudoservers.com (issue #6).",
    },
})

ENTRIES.append({
    "code": "1224321",
    "name": "Sherry Lynne Shea",
    "sex": "F",
    "born": "27 Jan 1963",
    "spouses": [{"name": "Joseph Paul Kanosky", "born": "3 Jul 1955", "married": "22 Jun 1985"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 124},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "12243211", "name": "Kayla Marie Kanosky", "born": "18 May 1988", "verified_terminal": True},
        {"code": "12243212", "name": "Marcie Lynne Kanosky", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1224322",
    "name": "Kenneth Scott Shea",
    "sex": "M",
    "born": "5 Apr 1969",
    "spouses": [{"name": "Peggy Darlene Cadiere", "married": "24 Apr 1993"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 124},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "12243221", "name": "Kristin Marie Shea", "born": "3 Apr 1995", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1224431",
    "name": "Robin Lynn DeBerry",
    "sex": "F",
    "born": "14 Feb 1958",
    "spouses": [
        {"name": "John Bishop", "married": "16 Apr 1976", "order": 1},
        {"name": "Douglas Smith", "born": "29 Mar 1959", "married": "31 Aug 1979", "order": 2},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 124},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "12244311", "name": "Jason Robert Smith", "born": "5 Dec 1979", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1224432",
    "name": "Julie Lee DeBerry",
    "sex": "F",
    "born": "1 May 1960",
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 124},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "12244321", "name": "Brandie Christionna DeBerry", "born": "2 Aug 1980", "verified_terminal": True},
        {"code": "12244322", "name": "Chase Douglas DeBerry", "born": "30 Dec 1983", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1224441",
    "name": "Barbara Jean Thomas",
    "sex": "F",
    "born": "31 Jul 1956",
    "spouses": [{"name": "Robert Eugene Goff", "married": "1 Sep 1973"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 124},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "12244411", "name": "Robert Eugene Goff, Jr.", "born": "12 Nov 1974", "verified_terminal": True},
        {"code": "12244412", "name": "Connie Sue Goff", "born": "14 Feb 1978", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1224442",
    "name": "Wilma Lee Thomas",
    "sex": "F",
    "born": "26 Oct 1957",
    "spouses": [{"name": "Ernest Lee Sargent"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 125},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "12244421", "name": "Ernest Jay Sargent", "born": "21 Aug 1975", "verified_terminal": True},
        {"code": "12244422", "name": "James Lee Sargent", "born": "26 Jun 1977", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1233211",
    "name": "Pearl Marie Fike",
    "sex": "F",
    "born": "13 Jul 1942",
    "spouses": [
        {"name": "Raymond Collins", "married": "1 Feb 1959", "details": "Same as #143412.", "order": 1},
        {"name": "Wallace Blake Clark", "born": "16 Jan 1924", "married": "2 Nov 1974", "order": 2},
        {"name": "William Korbish", "order": 3},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 125},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "12332111", "name": "Ronald Lee Collins", "born": "9 Aug 1959", "verified_terminal": True},
        {"code": "12332112", "name": "Tammie Sue Collins", "born": "27 Jun 1963", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1233212",
    "name": "William Lee Fike",
    "sex": "M",
    "born": "20 Nov 1945",
    "spouses": [
        {"name": "Iona Sherry Heater", "married": "18 Apr 1965", "order": 1},
        {"name": "Bonnie Jean Johnson", "married": "Jul 1966", "order": 2},
        {"name": "Lisa Lynn Damson", "married": "6 Jun 1976", "order": 3},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 125},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "12332121", "name": "Sheryl Ann Fike"},
        {"code": "12332122", "name": "Monica Lee Fike", "verified_terminal": True},
        {"code": "12332123", "name": "Michael G. Fike", "born": "23 Nov 1969", "flags": {"adopted": True}, "verified_terminal": True},
        {"code": "12332124", "name": "William Lee Fike", "born": "2 Jul 1977", "verified_terminal": True},
        {"code": "12332125", "name": "Scott Nicholas Fike", "born": "31 Aug 1983", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1233213",
    "name": "Charlotte Kay Fike",
    "sex": "F",
    "born": "5 Feb 1948",
    "spouses": [
        {"name": "Randy B. Thomas", "order": 1},
        {"name": "Bill Cramfield", "order": 2},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 125},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "12332131", "name": "Terry Lynn Fike", "born": "16 Dec 1965", "verified_terminal": True},
        {"code": "12332132", "name": "Colita Sue Thomas", "born": "10 Apr 1972", "verified_terminal": True},
        {"code": "12332133", "name": "Bryan Sharpe Thomas", "born": "21 Mar 1976", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1233214",
    "name": "Janet Sue Fike",
    "sex": "F",
    "born": "28 Dec 1948",
    "spouses": [
        {"name": "Gerald Valentine", "order": 1},
        {"name": "Michael Thomas", "order": 2},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 125},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "12332141", "name": "Jerry Allen Valentine, Jr.", "flags": {"diedInInfancy": True}, "verified_terminal": True},
        {"code": "12332142", "name": "Sharlene Sue Valentine", "flags": {"diedInInfancy": True}, "verified_terminal": True},
        {"code": "12332143", "name": "Gerald Allen Valentine, Jr.", "verified_terminal": True},
        {"code": "12332144", "name": "John Wesley Valentine", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1233215",
    "name": "Ralph Eugene Fike",
    "sex": "M",
    "born": "17 Jan 1950",
    "spouses": [
        {"name": "Loraine Miller", "order": 1},
        {"name": "Billie Elaine Baker", "order": 2},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 125},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "12332151", "name": "Travis Fike", "verified_terminal": True},
        {"code": "12332152", "name": "Kimberly Ann Fike", "born": "24 Aug 1974", "verified_terminal": True},
        {"code": "12332153", "name": "Ralph William Fike", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1233216",
    "name": "Chester Ray Fike",
    "sex": "M",
    "born": "3 Feb 1952",
    "spouses": [{"name": "Teresa Ann Nieman", "born": "28 May 1955", "married": "27 May 1972"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 125},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-07", "notes": None},
    "children": [
        {"code": "12332161", "name": "Stephanie Ray Fike", "born": "23 Oct 1972", "died": "24 Nov 1972", "flags": {"diedInInfancy": True}, "verified_terminal": True},
        {"code": "12332162", "name": "Buffie Rae Fike", "born": "1 Apr 1974"},
        {"code": "12332163", "name": "Brandy Sue Fike", "born": "25 Feb 1976", "verified_terminal": True},
    ],
})


# === Pages 126-130 vision pass (2026-06-08): JOHN gen 7 continued — Fike/Casteel/Chidester/Lewis/Willis/Shaffer/Lawson/McCarty/Sisler ===
ENTRIES.append({
    "code": "1233217",
    "name": "James Dale Fike",
    "sex": "M",
    "born": "15 Apr 1953",
    "spouses": [
        {"name": "Susan Mae Patterson", "married": "2 Mar 1973", "order": 1},
        {"name": "Patricia Ann Sigmon", "order": 2},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 126},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "12332171", "name": "James Dale Fike", "born": "10 Jun 1975", "verified_terminal": True},
        {"code": "12332172", "name": "Anthony Paul Fike", "born": "3 Aug 1979", "verified_terminal": True},
        {"code": "12332173", "name": "Stephanie Fike", "verified_terminal": True},
        {"code": "12332174", "name": "Dale Lee Fike", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1233221",
    "name": "Sandra Kay Casteel",
    "sex": "F",
    "born": "9 Aug 1947",
    "spouses": [{"name": "Arthur Paul Strattan, Jr.", "born": "26 Jan 1945", "died": "9 Dec 1996", "married": "9 Feb 1969"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 126},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "12332211", "name": "Eric Paul Strattan", "born": "11 Nov 1969", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1233231",
    "name": "Cyrus Duane Chidester",
    "sex": "M",
    "born": "17 Jan 1949",
    "spouses": [
        {"name": "Linda Joyce Graham", "born": "6 Mar 1951", "married": "22 Mar 1969", "order": 1},
        {"name": "Patty Livengood", "married": "Aug 1992", "order": 2},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 126},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "12332311", "name": "Howard Duane Chidester", "born": "9 May 1970"},
        {"code": "12332312", "name": "Brenda Lou Chidester", "born": "5 Mar 1972"},
    ],
})

ENTRIES.append({
    "code": "1233234",
    "name": "Diane Lynn Lewis",
    "sex": "F",
    "born": "22 Feb 1957",
    "spouses": [
        {"name": "Ed Martinko", "married": "26 Jun 1977", "order": 1},
        {"name": "Daniel Ray Marks", "born": "18 Aug 1954", "married": "21 May 1983", "order": 2},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 126},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "12332341", "name": "Dylon Justin Marks", "born": "1 Jun 1984", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1233235",
    "name": "Mack Arthur Lewis, Jr.",
    "sex": "M",
    "born": "7 Sep 1958",
    "spouses": [{"name": "Sherry Lynn Darby", "born": "14 Feb 1959", "married": "21 Oct 1978"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 126},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "12332351", "name": "Rhonda Lynn Lewis", "born": "16 Apr 1979", "verified_terminal": True},
        {"code": "12332352", "name": "Alicia Lee Lewis", "born": "5 Aug 1981", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1233236",
    "name": "Paul Kevin Lewis",
    "sex": "M",
    "born": "20 Nov 1959",
    "spouses": [{"name": "Vicky Sue Evans", "born": "15 Aug 1957", "married": "16 Nov 1979"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 126},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "12332361", "name": "Nickolas Paul Lewis", "born": "13 Sep 1987", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1233241",
    "name": "Alan Martin Willis",
    "sex": "M",
    "born": "25 Oct 1951",
    "spouses": [{"name": "Ruth Ellen Wallace", "born": "9 Apr 1953", "married": "21 Sep 1974"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 126},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "12332411", "name": "Andrew Martin Willis", "born": "26 May 1978", "verified_terminal": True},
        {"code": "12332412", "name": "Aaron Matthew Willis", "born": "19 May 1983", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1233242",
    "name": "Edith Willis",
    "sex": "F",
    "born": "31 Aug 1953",
    "spouses": [
        {"name": "Harry Michael Hensley", "married": "27 May 1972", "order": 1},
        {"name": "Lynn Allen Pickerill", "born": "14 May 1952", "married": "22 Mar 1975", "order": 2},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 126},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "12332421", "name": "Sussann Kay Pickerill", "born": "10 Apr 1976", "verified_terminal": True},
        {"code": "12332422", "name": "Nathan Lynn Pickerill", "born": "16 Dec 1977", "verified_terminal": True},
        {"code": "12332423", "name": "Emily Fay Pickerill", "born": "16 Jul 1981", "verified_terminal": True},
        {"code": "12332424", "name": "Samual Jacob Pickerill", "born": "5 Jul 1984", "verified_terminal": True},
        {"code": "12332425", "name": "Jesse William Pickerill", "born": "6 Mar 1988", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1233243",
    "name": "Bruce Edward Willis",
    "sex": "M",
    "born": "5 Jul 1955",
    "spouses": [{"name": "Darlene Kay Arnett", "born": "12 Aug 1958", "married": "5 Feb 1977"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 127},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "12332431", "name": "Jason Michael Willis", "born": "11 Jul 1977", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1233244",
    "name": "James Brian Willis",
    "sex": "M",
    "born": "10 Mar 1960",
    "spouses": [{"name": "Glennis Ilene Barker", "born": "14 Dec 1961", "married": "1 May 1981"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 127},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "12332441", "name": "James Brian Willis, II", "born": "22 Nov 1982", "verified_terminal": True},
        {"code": "12332442", "name": "Cassandra Lynn Willis", "born": "30 Jun 1984", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1233251",
    "name": "Daniel J. Shaffer",
    "sex": "M",
    "born": "28 Sep 1955",
    "spouses": [{"name": "Debbi Kaye Bolinger", "born": "19 Dec 1955", "married": "1 May 1976"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 127},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "12332511", "name": "Danielle Nicole Shaffer", "born": "17 Jul 1985", "verified_terminal": True},
        {"code": "12332512", "name": "Jared Brook Shaffer", "born": "9 Jun 1988", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1233252",
    "name": "Deborah Kay Shaffer",
    "sex": "F",
    "born": "4 Dec 1956",
    "spouses": [
        {"name": "Richard Lee Harbaugh", "married": "12 Jul 1974", "order": 1},
        {"name": "Stanley Ray Shaffer", "married": "26 May 1984", "order": 2},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 127},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "12332521", "name": "Jennifer Renee Shaffer", "born": "26 Apr 1986", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1233261",
    "name": "William Jackson Shaffer Jr.",
    "sex": "M",
    "born": "17 Oct 1959",
    "spouses": [{"name": "Nancy Ilene Bowers", "born": "17 Jun 1961", "married": "21 Jul 1979"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 127},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "12332611", "name": "Kurtis Jackson Shaffer", "born": "13 Aug 1980", "verified_terminal": True},
        {"code": "12332612", "name": "Lori Beth Shaffer", "born": "3 Aug 1981", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1233262",
    "name": "Roger Lee Shaffer",
    "sex": "M",
    "born": "21 Jan 1961",
    "spouses": [{"name": "Connie Marie Dikerson", "born": "27 Nov 1962", "married": "28 Jun 1980"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 127},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "12332621", "name": "Carla Marie Shaffer", "born": "16 Nov 1980", "verified_terminal": True},
        {"code": "12332622", "name": "Terra Lee Shaffer", "born": "2 Jul 1983", "verified_terminal": True},
        {"code": "12332623", "name": "Ashley Diane Shaffer", "born": "8 Dec 1988", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1233291",
    "name": "Joseph Dewane Galloway",
    "sex": "M",
    "born": "5 Apr 1962",
    "spouses": [{"name": "Tammy Reckart", "born": "18 Jul 1965"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 127},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "12332911", "name": "Tabitha Galloway", "born": "8 Feb 1984", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1321211",
    "name": "Kenneth Frazee Jr.",
    "sex": "M",
    "born": "19 Feb 1958",
    "died": "20 Jan 1996",
    "spouses": [{"name": "Debra Wass"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 128},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "13212111", "name": "Bridget Marie Frazee", "born": "Dec 1978", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1321212",
    "name": "Eddie Frazee",
    "sex": "M",
    "born": "1960",
    "spouses": [{"name": "Fike", "married": "29 Sep 1979"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 128},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "13212121", "name": "Carrie Yvonne Frazee", "born": "Mar 1980", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1322342",
    "name": "Denzel Ray Guthrie",
    "sex": "M",
    "born": "22 Sep 1962",
    "spouses": [{"name": "Shelley Lynn Urie", "born": "21 Jan 1962", "married": "24 Sep 1983"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 128},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "13223421", "name": "Seth Andrew Guthrie", "born": "4 Feb 1987", "verified_terminal": True},
        {"code": "13223422", "name": "Jenna Mariah Guthrie", "born": "23 Oct 1989", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1322343",
    "name": "Denise Rene Guthrie",
    "sex": "F",
    "born": "22 Sep 1962",
    "spouses": [{"name": "Ronald Jay Clark", "born": "21 Feb 1957", "married": "16 Jun 1984"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 128},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "13223431", "name": "Jamie Nicole Clark", "born": "27 Mar 1988", "verified_terminal": True},
        {"code": "13224332", "name": "Jessica Rae Clark", "born": "6 Jul 1992", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1326111",
    "name": "Dawn Lawson",
    "sex": "F",
    "born": "9 Jan 1948",
    "spouses": [{"name": "Joseph Anthony Kochtan", "born": "30 Jun 1947", "married": "14 Sep 1968"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 128},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "13261111", "name": "Matthew Frank Kochtan", "born": "28 Dec 1973", "verified_terminal": True},
        {"code": "13261112", "name": "Kyle Joseph Kocktan", "born": "12 Nov 1977", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1326112",
    "name": "Kerry Blaine Lawson",
    "sex": "M",
    "born": "22 Apr 1949",
    "spouses": [
        {"name": "Peggy Whitaker", "born": "10 Dec 1949", "order": 1},
        {"name": "Linda Jean Smith", "born": "5 Sep 1953", "married": "4 Jan 1975", "order": 2},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 128},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "13261121", "name": "Amy Heather Lawson", "born": "30 Jan 1970"},
        {"code": "13261122", "name": "Sarah Elizabeth Lawson", "born": "16 Jun 1986", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1326113",
    "name": "Leah Lawson",
    "sex": "F",
    "born": "17 Jun 1950",
    "spouses": [
        {"name": "Gary Hennig", "born": "3 Feb 1969", "order": 1},
        {"name": "Bill Baldwin", "born": "31 Jan 1943", "order": 2},
        {"name": "Maun Hardy", "order": 3},
        {"name": "Marvin Lefebre", "born": "9 Jan 1947", "order": 4},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 128},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "13261131", "name": "Jeffry Allen Hennig", "born": "3 Feb 1969", "verified_terminal": True},
        {"code": "13261132", "name": "Billy Baldwin", "born": "3 Jan 1971", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1326114",
    "name": "Nina Lawson",
    "sex": "F",
    "born": "28 Jan 1953",
    "spouses": [
        {"name": "Michael G. Gorman", "order": 1},
        {"name": "Michael Thompson", "born": "8 Apr 1954", "order": 2},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 128},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "13261141", "name": "Chris Thompson", "born": "7 Jul 1988", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1326121",
    "name": "Larry Owens Lawson",
    "sex": "M",
    "born": "28 Aug 1948",
    "spouses": [{"name": "Ann Dacey", "born": "30 May 1948", "married": "16 Jul 1981"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 128},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "13261211", "name": "Seth Augustus Lawson", "born": "27 Dec 1982", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1326131",
    "name": "Sandi Friend",
    "sex": "F",
    "born": "13 May 1952",
    "spouses": [{"name": "Larry Wakefield", "born": "Nov 1948", "married": "15 Aug 1970"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 129},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "13261311", "name": "Lori Jean Wakefield", "born": "5 Jun 1971"},
        {"code": "13261312", "name": "Amanda Fay Wakefield", "born": "2 Nov 1972"},
        {"code": "13261313", "name": "Larry William Wakefield", "born": "9 Sep 1974", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1326142",
    "name": "Tonya Marie Lawson",
    "sex": "F",
    "born": "4 Oct 1975",
    "spouses": [{"name": "Todd Bednarz"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 129},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "13261421", "name": "Chester Kent Bednarz", "born": "12 Nov 1995", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1326413",
    "name": "Marlin Robert Lawson",
    "sex": "M",
    "born": "25 Oct 1954",
    "spouses": [{"name": "Rosemary Feather", "born": "21 Oct 1958", "married": "12 Jun 1976"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 129},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "13264131", "name": "Amie Beth Lawson", "born": "21 Jan 1978", "verified_terminal": True},
        {"code": "13264132", "name": "Nicholas Paul Lawson", "born": "14 Jul 1982", "verified_terminal": True},
        {"code": "13264133", "name": "Todd Allen Lawson", "born": "22 Jul 1987", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1365111",
    "name": "Judith Ann Shafer",
    "sex": "F",
    "born": "29 Jan 1942",
    "spouses": [{"name": "Franklin Forest Wilhelm", "born": "11 Oct 1940", "married": "30 Jun 1963"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 129},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "13651111", "name": "Kelly Ann Wilhelm", "born": "14 Oct 1967", "verified_terminal": True},
        {"code": "13651112", "name": "Jeffrey Frank Wilhelm", "born": "13 Jul 1971", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1365112",
    "name": "Janet Louise Shafer",
    "sex": "F",
    "born": "12 Jun 1943",
    "spouses": [{"name": "Alvin Robert McKee", "born": "16 Jun 1947", "married": "21 Dec 1968"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 129},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "13651121", "name": "Lisa Ann McKee", "born": "22 Aug 1971", "verified_terminal": True},
        {"code": "13651122", "name": "Robert Alva McKee", "born": "28 Apr 1973", "verified_terminal": True},
        {"code": "13651123", "name": "Charles Alvin McKee", "born": "2 Mar 1975", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1365113",
    "name": "James Harold Shafer",
    "sex": "M",
    "born": "9 Mar 1946",
    "spouses": [{"name": "Darby Eileen Handlen", "born": "8 Feb 1946", "married": "24 Nov 1969"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 129},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "13651131", "name": "Janene Lynn Shafer", "born": "31 May 1975", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1365116",
    "name": "Margaret Jane Shafer",
    "sex": "F",
    "born": "5 Jan 1949",
    "spouses": [
        {"name": "Wilford Dale Jeffers", "born": "18 Jan 1934", "married": "10 Jan 1970", "order": 1},
        {"name": "Dennis Lee Bolyard", "born": "26 Jun 1946", "married": "20 Aug 1983", "order": 2},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 129},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "13651161", "name": "Randy Lee Bolyard", "born": "23 Feb 1973", "flags": {"adopted": True}},
        {"code": "13651162", "name": "Jamie Lynn Bolyard", "born": "28 Oct 1974", "flags": {"adopted": True}, "verified_terminal": True},
        {"code": "13651163", "name": "Aimee Bolyard", "flags": {"stepChild": True}, "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1365117",
    "name": "Robert Gay Shafer",
    "sex": "M",
    "born": "3 Nov 1950",
    "spouses": [{"name": "Joyce Ellen Metheny", "born": "11 Jan 1952", "married": "9 Aug 1974"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 129},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "13651171", "name": "Joseph Arthur Lewis", "born": "14 Dec 1969", "flags": {"stepChild": True}, "verified_terminal": True},
        {"code": "13651172", "name": "Christina Marie Shafer", "born": "2 Oct 1975", "verified_terminal": True},
        {"code": "13651173", "name": "Jamie Roberta Shafer", "born": "28 Oct 1977", "verified_terminal": True},
        {"code": "13651174", "name": "Lester Grant Shafer", "born": "29 Oct 1981", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1365118",
    "name": "Mary Alice Shafer",
    "sex": "F",
    "born": "1 Jul 1952",
    "spouses": [{"name": "Rodney Lee Nieman", "born": "8 Oct 1953", "married": "10 Mar 1972"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 130},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "13651181", "name": "Susan Jo Nieman", "born": "6 Dec 1969", "verified_terminal": True},
        {"code": "13651182", "name": "Tony Lee Nieman", "born": "29 Aug 1972", "verified_terminal": True},
        {"code": "13651183", "name": "Amy Jo Nieman", "born": "27 Nov 1975", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1365119",
    "name": "Linda June Shafer",
    "sex": "F",
    "born": "1 Jun 1953",
    "spouses": [{"name": "Roger Lowry", "born": "24 Jun 1952", "married": "19 Jun 1971"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 130},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "13651191", "name": "Robert Lee Lowry", "born": "17 Dec 1972", "verified_terminal": True},
        {"code": "13651192", "name": "Timothy Playford Lowry", "born": "6 Jun 1976", "verified_terminal": True},
        {"code": "13651193", "name": "Ronald Lynn Lowry", "born": "6 Sep 1980", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1365121",
    "name": "Wilma Ruth McCarty",
    "sex": "F",
    "born": "7 Nov 1946",
    "spouses": [{"name": "Carl Collins", "married": "5 May 1963", "details": "Same as #143413."}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 130},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": "Children cross-coded with 1434131-2."},
})

ENTRIES.append({
    "code": "1365122",
    "name": "Ina Grace McCarty",
    "sex": "F",
    "born": "21 Jun 1949",
    "spouses": [{"name": "John Friend", "married": "27 Jun 1967"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 130},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "13651221", "name": "Eric Lee Friend", "born": "10 Aug 1967", "verified_terminal": True},
        {"code": "13651222", "name": "Nicole Susan Friend", "born": "27 Nov 1972", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1365123",
    "name": "Charles Richard McCarty",
    "sex": "M",
    "born": "8 May 1952",
    "spouses": [
        {"name": "Karen Dutton", "married": "18 Dec 1977", "order": 1},
        {"name": "Sandra Thomas", "married": "4 Nov 1981", "order": 2},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 130},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "13651231", "name": "James Edward McCarty", "born": "1 Dec 1977", "verified_terminal": True},
        {"code": "13651232", "name": "Amber Leann McCarty", "born": "10 Jun 1982", "verified_terminal": True},
        {"code": "13651233", "name": "David McCarty", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1365124",
    "name": "David Ward McCarty",
    "sex": "M",
    "born": "20 Sep 1958",
    "died": "3 Sep 1985",
    "spouses": [
        {"name": "Yvette Rexroad", "order": 1},
        {"name": "Sylvia Lee", "married": "20 Jul 1984", "order": 2},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 130},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "13651241", "name": "Jonathon Robert McCarty", "born": "11 May 1978", "verified_terminal": True},
        {"code": "13651242", "name": "Dailey Rae Kellie McCarty", "born": "30 Mar 1982", "verified_terminal": True},
        {"code": "13651243", "name": "Chrissie Lynn McCarty", "born": "3 Jun 1985", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1365131",
    "name": "Rosella Grace Sisler",
    "sex": "F",
    "born": "7 Aug 1941",
    "spouses": [{"name": "Wayne Burgess"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 130},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "13651311", "name": "Joyce Burgess", "verified_terminal": True},
        {"code": "13651312", "name": "Grace Catherine Burgess"},
        {"code": "13651313", "name": "Shirley Burgess"},
    ],
})

ENTRIES.append({
    "code": "1365133",
    "name": "Hubert Martin Sisler, Jr.",
    "sex": "M",
    "born": "7 Mar 1958",
    "spouses": [{"name": "Shelley Maureen"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 130},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "13651331", "name": "Thelma Lou Sisler", "born": "2 Dec 1980", "verified_terminal": True},
        {"code": "13651332", "name": "Hubert Martin Sisler, III", "born": "19 Apr 1984", "verified_terminal": True},
    ],
})


# === James PDF pages 6-10 vision pass (2026-06-08): gen 4-5 Barnes/Frazee/Thornton/Slavins families ===
ENTRIES.append({
    "code": "71311",
    "name": "Elaine Virginia Seese",
    "sex": "F",
    "born": "12 Oct 1932",
    "spouses": [{"name": "Raymond Thomas Barbour", "married": "23 Aug 1953"}],
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 15},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "713111", "name": "Daphney Elaine Barbour", "born": "6 Jun 1954"},
        {"code": "713112", "name": "Jason Thomas Barbour", "born": "15 Apr 1956", "verified_terminal": True},
        {"code": "713113", "name": "Taimi Rena Barbour", "born": "22 Nov 1957", "verified_terminal": True},
        {"code": "713114", "name": "Melinda Dawn Barbour", "born": "2 Dec 1959", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "71312",
    "name": "Joann Vivian Seese",
    "sex": "F",
    "born": "3 Dec 1933",
    "spouses": [{"name": "Dr. Richard (Ricky) Fiorini", "born": "27 May 1929", "married": "12 Oct 1957"}],
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 15},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "713121", "name": "Belinda Fiorini", "born": "17 Jan 1960", "verified_terminal": True},
        {"code": "713122", "name": "Jennifer Fiorini", "born": "27 Feb 1961", "verified_terminal": True},
        {"code": "713123", "name": "Cynthia Fiorini", "born": "26 Nov 1963", "verified_terminal": True},
        {"code": "713124", "name": "Jude Fiorini", "born": "9 Sep 1965", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "71331",
    "name": "James Freeland Cale",
    "sex": "M",
    "born": "15 Apr 1945",
    "spouses": [{"name": "Sandy Kay Dennis", "born": "24 Mar 1955", "married": "11 Apr 1974"}],
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 15},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": "Married in Oakland, MD"},
    "children": [
        {"code": "713311", "name": "Spencer James Cale", "born": "4 Feb 1975", "verified_terminal": True},
        {"code": "713312", "name": "Ryan Clay Cale", "born": "16 Sep 1984", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "71441",
    "name": "Wendell C. Barnes",
    "sex": "M",
    "born": "17 Aug 1931",
    "spouses": [{"name": "Virginia Friend", "born": "15 Dec 1931", "married": "28 Oct 1950"}],
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 15},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "714411", "name": "Roxanne Barnes", "born": "1 Feb 1953"},
        {"code": "714412", "name": "Randy Dale Barnes", "born": "2 Jul 1955", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "71442",
    "name": "Wilda Lee Barnes",
    "sex": "F",
    "born": "17 Aug 1935",
    "spouses": [{"name": "Charles (Bud) Dailey"}],
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 15},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": "Husband from Alum Bank, PA"},
    "children": [
        {"code": "714421", "name": "Darrell Vaughn Dailey", "verified_terminal": True},
        {"code": "714422", "name": "Dana Vance Dailey"},
        {"code": "714423", "name": "Dale Vincent Dailey"},
        {"code": "714424", "name": "Nina Marie Dailey", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "71451",
    "name": "Delora Audrey Wolfe",
    "sex": "F",
    "spouses": [{"name": "Arthur Lewis Forman", "born": "23 Dec 1927", "married": "31 Dec 1950"}],
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 15},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "714511", "name": "Clinton L. Forman"},
        {"code": "714512", "name": "Ronna June Forman"},
    ],
})

ENTRIES.append({
    "code": "71452",
    "name": "Loretta Wolfe",
    "sex": "F",
    "spouses": [{"name": "Wilford (Woody) Glenn Cuppett", "born": "14 Jan 1928", "died": "30 Jun 1997", "married": "7 Apr 1949"}],
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 15},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "714521", "name": "Clifford Cuppett"},
        {"code": "714522", "name": "Terry Cuppett", "verified_terminal": True},
        {"code": "714523", "name": "Debra Sue Cuppett", "born": "10 Aug 1951"},
    ],
})

ENTRIES.append({
    "code": "71453",
    "name": "Delbert R. Wolfe",
    "sex": "M",
    "born": "7 Mar 1933",
    "died": "2 Jun 1986",
    "spouses": [{"name": "Ethel Savage", "married": "7 Apr 1951"}],
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 16},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "714531", "name": "Roger Lee Wolfe, Sr."},
        {"code": "714532", "name": "Stanley Wolfe"},
        {"code": "714533", "name": "Edwin Wolfe"},
        {"code": "714534", "name": "Cheryl Wolfe", "born": "9 Aug 1957", "verified_terminal": True},
        {"code": "714535", "name": "Duncan Eric Wolfe", "born": "1964"},
        {"code": "714536", "name": "Keith Wolfe", "born": "6 Apr 1968", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "71454",
    "name": "Alda Mae Wolfe",
    "sex": "F",
    "born": "2 May 1935",
    "spouses": [{"name": "Elvidore Gilbert Everly", "born": "18 Apr 1932", "married": "22 Jan 1952"}],
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 16},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": "Married at Asher Glade, MD"},
    "children": [
        {"code": "714541", "name": "Sherry Louise Everly", "born": "29 May 1952"},
        {"code": "714542", "name": "Karen Kay Everly", "born": "26 Oct 1954"},
        {"code": "714543", "name": "James Spencer Everly", "born": "30 May 1961"},
    ],
})

ENTRIES.append({
    "code": "71455",
    "name": "Dwain Edwin Wolfe",
    "sex": "M",
    "born": "24 Aug 1936",
    "died": "9 Sep 1979",
    "spouses": [{"name": "Ina May Wayne"}],
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 16},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "714551", "name": "Brenda Lee Wolfe", "died": "1962", "verified_terminal": True},
        {"code": "714552", "name": "Connie Sue Wolfe", "verified_terminal": True},
        {"code": "714553", "name": "Joy Lynn Wolfe"},
    ],
})

ENTRIES.append({
    "code": "71461",
    "name": "Phyllis Jean Barnes",
    "sex": "F",
    "born": "3 Oct 1942",
    "spouses": [{"name": "Lowell Feather Thomas", "born": "10 Jul 1941", "married": "21 May 1967"}],
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 16},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "714611", "name": "Jeffrey Ward Thomas", "born": "5 Jan 1969"},
        {"code": "714612", "name": "Gregory Clark Thomas", "born": "1 Jun 1971", "verified_terminal": True},
        {"code": "714613", "name": "Melinda Jean Thomas", "born": "5 Oct 1979", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "71762",
    "name": "Lane Bradley Fike",
    "sex": "M",
    "born": "17 Jul 1947",
    "spouses": [{"name": "Denise Cavelrie", "married": "Jul 1971"}],
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 16},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "717621", "name": "Hunter Lane Fike", "born": "14 Apr 1982", "verified_terminal": True},
        {"code": "717622", "name": "Tyler Keith Fike", "born": "7 Jul 1985", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "71721",
    "name": "Van Anderson",
    "sex": "M",
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 7},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
})

ENTRIES.append({
    "code": "71761",
    "name": "Connie Maurine Fike",
    "sex": "F",
    "born": "17 Jul 1947",
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 7},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
})

ENTRIES.append({
    "code": "71763",
    "name": "Gary Lee Fike",
    "sex": "M",
    "born": "23 Sep 1954",
    "spouses": [{"name": "Margaret Ann Scott", "married": "Jul 1980"}],
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 16},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "717631", "name": "Emily Scott Fike", "born": "11 Mar 1983", "verified_terminal": True},
        {"code": "717632", "name": "Adam Scott Fike", "born": "30 Dec 1986", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "722111",
    "name": "Sharon Elizabeth Thornton",
    "sex": "F",
    "born": "15 Jan 1959",
    "spouses": [{"name": "Michael Clifton Weber III", "married": "10 Oct 1981"}],
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 16},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
})

ENTRIES.append({
    "code": "722112",
    "name": "Robert Barnes Thornton Jr",
    "sex": "M",
    "born": "24 Jun 1961",
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 16},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
})

ENTRIES.append({
    "code": "722113",
    "name": "Marilyn Anderson Thornton",
    "sex": "F",
    "born": "15 Jun 1963",
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 16},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
})

ENTRIES.append({
    "code": "722121",
    "name": "Jeff David Thornton",
    "sex": "M",
    "born": "15 Apr 1973",
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 16},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
})

ENTRIES.append({
    "code": "722122",
    "name": "Chandler Campbell Thornton",
    "sex": "M",
    "born": "2 May 1975",
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 16},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
})

ENTRIES.append({
    "code": "722131",
    "name": "James Hogg Rogers III",
    "sex": "M",
    "born": "22 Jul 1963",
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 16},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
})

ENTRIES.append({
    "code": "722132",
    "name": "Clint Thornton Rogers",
    "sex": "M",
    "born": "20 Feb 1966",
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 16},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
})

ENTRIES.append({
    "code": "722133",
    "name": "Charlotte Elizabeth Rogers",
    "sex": "F",
    "born": "7 Aug 1967",
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 16},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
})

ENTRIES.append({
    "code": "723111",
    "name": "Sharon Leigh Shelton",
    "sex": "F",
    "born": "9 Sep 1961",
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 16},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
})

ENTRIES.append({
    "code": "723112",
    "name": "Joseph Vanderbilt Shelton, Jr.",
    "sex": "M",
    "born": "10 Mar 1964",
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 16},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
})

ENTRIES.append({
    "code": "723113",
    "name": "Suzanne Lynn Shelton",
    "sex": "F",
    "born": "18 Sep 1965",
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 16},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
})

ENTRIES.append({
    "code": "723121",
    "name": "Gwendolyn Elaine Seaton",
    "sex": "F",
    "born": "28 Jun 1971",
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 16},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
})

ENTRIES.append({
    "code": "723122",
    "name": "Michael Wayne Seaton",
    "sex": "M",
    "born": "10 Jun 1974",
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 16},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
})

ENTRIES.append({
    "code": "723123",
    "name": "Lori Katherine Seaton",
    "sex": "F",
    "born": "20 Jan 1978",
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 16},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
})

ENTRIES.append({
    "code": "723311",
    "name": "Lee Robert Barnes",
    "sex": "M",
    "born": "7 Apr 1982",
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 16},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
})

ENTRIES.append({
    "code": "723321",
    "name": "James Ronald Barnes Jr.",
    "sex": "M",
    "born": "3 Jul 1981",
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 16},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
})

ENTRIES.append({
    "code": "723331",
    "name": "Michele Carolyn Wilde",
    "sex": "F",
    "born": "23 Aug 1982",
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 16},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
})

ENTRIES.append({
    "code": "723521",
    "name": "Amy Laura Dutterer",
    "sex": "F",
    "born": "9 Mar 1982",
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 17},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
})


# === Absalom + William + Rachel PDFs vision pass (2026-06-08): completes all small PDFs ===
ENTRIES.append({
    "code": "84",
    "name": "James Marshall Guthrie",
    "sex": "M",
    "born": "20 May 1845",
    "died": "7 Jan 1917",
    "spouses": [{"name": "Elizabeth Jane Linton", "born": "26 Jan 1856", "married": "2 Nov 1875"}],
    "source": {"pdf": "Absalom_Guthrie - One Generation.pdf", "page": 1},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "841", "name": "Myrta Belle Guthrie", "born": "9 Feb 1877"},
        {"code": "842", "name": "Harley Urias Guthrie", "born": "16 Jan 1879"},
        {"code": "843", "name": "John Clyde Guthrie", "born": "11 Jun 1881"},
        {"code": "844", "name": "Louisiana Guthrie", "born": "8 Sep 1886", "died": "in infancy", "flags": {"diedInInfancy": True}, "verified_terminal": True},
        {"code": "845", "name": "Mellie Irene Guthrie", "born": "14 Aug 1888"},
    ],
})

ENTRIES.append({
    "code": "8B",
    "name": "William Nolan Guthrie",
    "sex": "M",
    "born": "27 Dec 1861",
    "died": "30 Nov 1918",
    "spouses": [{"name": "Jennie Aiken", "married": "10 Apr 1895"}],
    "source": {"pdf": "Absalom_Guthrie - One Generation.pdf", "page": 2},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": "Wife from Pittsburgh, PA"},
    "children": [
        {"code": "8B1", "name": "Donald Spencer Guthrie", "born": "31 Jul 1901", "verified_terminal": True, "details": "lived with Mother, Columbus OH"},
        {"code": "8B2", "name": "William Norman Guthrie", "born": "29 Oct 1908", "verified_terminal": True, "details": "m. 26 Jul 1930 Kirkpatrick (lived at Grandville, Ohio)"},
    ],
})

ENTRIES.append({
    "code": "841",
    "name": "Myrta Belle Guthrie",
    "sex": "F",
    "born": "9 Feb 1877",
    "spouses": [{"name": "George Hengst", "born": "7 Mar 1870", "married": "29 Sep 1897"}],
    "residences": ["Logan, OH"],
    "source": {"pdf": "Absalom_Guthrie - One Generation.pdf", "page": 2},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "8411", "name": "Raymond Guthrie Hengst", "born": "2 Aug 1898", "verified_terminal": True, "details": "Lived in Cleveland, OH"},
    ],
})

ENTRIES.append({
    "code": "842",
    "name": "Harley Urias Guthrie",
    "sex": "M",
    "born": "16 Jan 1879",
    "died": "4 Feb 1918",
    "spouses": [{"name": "Marcella Lanker", "born": "27 Nov 1881", "married": "5 May 1905"}],
    "source": {"pdf": "Absalom_Guthrie - One Generation.pdf", "page": 2},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "8421", "name": "Marcella Jane Guthrie", "born": "11 Feb 1914", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "872",
    "name": "Anna May Guthrie",
    "sex": "F",
    "born": "28 Dec 1884",
    "died": "10 Feb 1916",
    "spouses": [{"name": "Francis Clark", "born": "27 Jun 1882", "married": "27 Jun 1906"}],
    "source": {"pdf": "Absalom_Guthrie - One Generation.pdf", "page": 3},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "8721", "name": "Hannah Marie Clark", "born": "18 Dec 1906", "verified_terminal": True},
        {"code": "8722", "name": "Clarence Irving Clark", "born": "1 Jan 1909", "verified_terminal": True},
        {"code": "8723", "name": "Lawrence Arthur Clark", "born": "19 Aug 1910", "verified_terminal": True},
        {"code": "8724", "name": "Ida Louise Clark", "born": "31 Mar 1914", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "876",
    "name": "Park Edward Guthrie",
    "sex": "M",
    "born": "21 Dec 1895",
    "spouses": [{"name": "June Roberts", "born": "11 Mar 1902", "married": "24 Dec 1925"}],
    "residences": ["980 Stelzer Rd. Columbus, OH"],
    "source": {"pdf": "Absalom_Guthrie - One Generation.pdf", "page": 3},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": "Child code 9861 reproduces the PDF's numbering anomaly."},
    "children": [
        {"code": "9861", "name": "Maurice Edward Guthrie", "born": "7 Jan 1930", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "877",
    "name": "John Paul Guthrie",
    "sex": "M",
    "born": "13 Aug 1898",
    "spouses": [{"name": "Marjorie Wheeler", "married": "8 Apr 1928"}],
    "residences": ["541 E. 105th St. Cleveland, OH"],
    "source": {"pdf": "Absalom_Guthrie - One Generation.pdf", "page": 3},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "8771", "name": "George Paul Guthrie", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "812",
    "name": "Ora Bell Guthrie",
    "sex": "F",
    "born": "18 Dec 1868",
    "spouses": [{"name": "Edwin D. Frost", "born": "17 Apr 1865", "died": "2 Sep 1929", "married": "2 Oct 1889"}],
    "source": {"pdf": "Absalom_Guthrie - One Generation.pdf", "page": 2},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "8121", "name": "Berlin Earl Frost", "born": "4 Apr 1898", "died": "7 Jan 1919", "verified_terminal": True},
        {"code": "8122", "name": "Mary Genevieve Frost", "born": "7 May 1904"},
    ],
})

ENTRIES.append({
    "code": "825",
    "name": "Jennie Harned",
    "sex": "F",
    "born": "6 Jun 1873",
    "spouses": [{"name": "Edward Alexander", "born": "12 Mar 1872", "married": "10 May 1896"}],
    "source": {"pdf": "Absalom_Guthrie - One Generation.pdf", "page": 2},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": "Lived in Epping, ND"},
    "children": [
        {"code": "8251", "name": "Walter Harned Alexander", "born": "16 Feb 1898"},
        {"code": "8252", "name": "Mary Frances Alexander", "born": "9 Feb 1900"},
        {"code": "8253", "name": "Charles Edward Alexander", "born": "2 Feb 1902", "verified_terminal": True, "details": "m. 31 May 1928 Mary Kemp"},
        {"code": "8254", "name": "Ruth Alice Alexander", "born": "3 Dec 1904"},
        {"code": "8255", "name": "Christine Mae Alexander", "born": "12 Jun 1906"},
        {"code": "8256", "name": "Joseph William Alexander", "born": "12 May 1908", "verified_terminal": True},
        {"code": "8257", "name": "Alma V. Alexander", "born": "26 Jun 1910", "verified_terminal": True},
        {"code": "8258", "name": "Marjorie L. Alexander", "born": "6 Nov 1913", "verified_terminal": True},
        {"code": "8259", "name": "Claire Esther Alexander", "born": "13 Dec 1915", "verified_terminal": True},
        {"code": "825A", "name": "Jean Isabel Alexander", "born": "4 Aug 1919", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "8122",
    "name": "Mary Genevieve Frost",
    "sex": "F",
    "born": "7 May 1904",
    "spouses": [{"name": "Otto Jesse Hill", "married": "10 Jun 1925"}],
    "residences": ["Berlin Heights, OH"],
    "source": {"pdf": "Absalom_Guthrie - One Generation.pdf", "page": 3},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "81221", "name": "Robert Edwin Hill", "born": "16 Jan 1928", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "8251",
    "name": "Walter Harned Alexander",
    "sex": "M",
    "born": "16 Feb 1898",
    "spouses": [{"name": "Cora Glaus", "married": "12 Jun 1928"}],
    "source": {"pdf": "Absalom_Guthrie - One Generation.pdf", "page": 3},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "82511", "name": "Walter Cirtus Alexander", "born": "10 Jul 1929", "verified_terminal": True},
        {"code": "82512", "name": "Avis Ardele Alexander", "born": "8 Sep 1930", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "8252",
    "name": "Mary Frances Alexander",
    "sex": "F",
    "born": "9 Feb 1900",
    "spouses": [{"name": "Paul Miller", "married": "8 May 1921"}],
    "source": {"pdf": "Absalom_Guthrie - One Generation.pdf", "page": 4},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "82521", "name": "Phyllis Miller", "born": "28 Feb 1922", "verified_terminal": True},
        {"code": "82522", "name": "Rita Miller", "born": "11 Nov 1923", "verified_terminal": True},
        {"code": "82523", "name": "Melba Miller", "born": "15 Nov 1924", "verified_terminal": True},
        {"code": "82524", "name": "Patricia Miller", "born": "6 Aug 1926", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "8254",
    "name": "Ruth Alice Alexander",
    "sex": "F",
    "born": "3 Dec 1904",
    "spouses": [{"name": "Arthur Grau", "married": "17 Mar 1928"}],
    "source": {"pdf": "Absalom_Guthrie - One Generation.pdf", "page": 4},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "82541", "name": "William Arthur Grau", "born": "15 Jul 1929", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "8255",
    "name": "Christine Mae Alexander",
    "sex": "F",
    "born": "12 Jun 1906",
    "spouses": [{"name": "Frank E. Prim", "married": "1925"}],
    "source": {"pdf": "Absalom_Guthrie - One Generation.pdf", "page": 4},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "82551", "name": "Wayne Prim", "born": "26 Oct 1926", "verified_terminal": True},
        {"code": "82552", "name": "Fae Prim", "born": "18 Mar 1928", "verified_terminal": True},
        {"code": "82553", "name": "Virginia Prim", "born": "20 Jan 1930", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "826",
    "name": "Lucy Harned",
    "sex": "F",
    "born": "1 Oct 1876",
    "spouses": [{"name": "Hammond Hardesty"}],
    "residences": ["Paulding, OH"],
    "source": {"pdf": "Absalom_Guthrie - One Generation.pdf", "page": 2},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "8261", "name": "Harry Hardesty", "born": "1894"},
    ],
})

ENTRIES.append({
    "code": "827",
    "name": "Mary Harned",
    "sex": "F",
    "born": "8 Feb 1879",
    "spouses": [{"name": "Homer Hardesty", "married": "Sep 1898"}],
    "residences": ["Piggott, Ark."],
    "source": {"pdf": "Absalom_Guthrie - One Generation.pdf", "page": 2},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "8271", "name": "Dale Hardesty", "born": "about 1900"},
        {"code": "8272", "name": "Died in Infancy", "verified_terminal": True, "flags": {"diedInInfancy": True}},
    ],
})

ENTRIES.append({
    "code": "8261",
    "name": "Harry Hardesty",
    "sex": "M",
    "born": "1894",
    "source": {"pdf": "Absalom_Guthrie - One Generation.pdf", "page": 4},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "82611", "name": "One Child", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "8271",
    "name": "Dale Hardesty",
    "sex": "M",
    "born": "about 1900",
    "source": {"pdf": "Absalom_Guthrie - One Generation.pdf", "page": 4},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "82711", "name": "One Son", "verified_terminal": True},
    ],
})

# William branch
ENTRIES.append({
    "code": "2",
    "name": "William Guthrie",
    "sex": "M",
    "born": "10 Sep 1794",
    "died": "12 Jul 1873",
    "buried": "Shady Grove Cemetery",
    "spouses": [{"name": "Rebecca Jefferys", "born": "9 Mar 1801", "died": "15 Apr 1869"}],
    "source": {"pdf": "William_Guthrie - One Generation.pdf", "page": 1},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": "Wife dau of Benjamin and Elizabeth (Smith) Jefferys"},
    "children": [
        {"code": "21", "name": "Ruth G. Guthrie", "born": "22 May 1838"},
        {"code": "22", "name": "Eleanor Jane Guthrie", "born": "28 Aug 1840"},
        {"code": "23", "name": "Elnor Guthrie", "born": "1841", "died": "1927", "verified_terminal": True},
        {"code": "24", "name": "Eugenus Guthrie", "born": "16 Mar 1844", "died": "24 Feb 1857", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "21",
    "name": "Ruth G. Guthrie",
    "sex": "F",
    "born": "22 May 1838",
    "died": "6 Dec 1933",
    "spouses": [{"name": "Jonas Frankhouser", "born": "20 Sep 1833", "died": "3 Feb 1920"}],
    "source": {"pdf": "William_Guthrie - One Generation.pdf", "page": 1},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": "Husband son of Daniel and Elizabeth (Movers) Frankhouser"},
    "children": [
        {"code": "211", "name": "George Frankhouser", "died": "1945", "verified_terminal": True},
        {"code": "212", "name": "Wilbur Finley Frankhouser", "born": "12 Sep 1870"},
        {"code": "213", "name": "Minnie P. Frankhouser", "born": "26 Jul 1873", "died": "25 Feb 1963", "verified_terminal": True, "details": "m. T. W. Kinnan"},
        {"code": "214", "name": "Effie Jane Frankhouser", "verified_terminal": True, "details": "m. 27 Jan 1904 to Silas Beerbower"},
        {"code": "215", "name": "Walter Frankhouser", "born": "19 Jan 1880"},
    ],
})

ENTRIES.append({
    "code": "22",
    "name": "Eleanor Jane Guthrie",
    "sex": "F",
    "born": "28 Aug 1840",
    "died": "26 Nov 1913",
    "spouses": [{"name": "Abner Gaines Harshbarger", "born": "1836", "died": "1919", "married": "27 Oct 1859"}],
    "source": {"pdf": "William_Guthrie - One Generation.pdf", "page": 1},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": "Husband son of Jacob and Nancy (Rankin) Harshbarger"},
    "children": [
        {"code": "221", "name": "Felicia Irene Harshbarger", "born": "16 Dec 1860", "verified_terminal": True, "details": "m. 1905 to Simon S. Hartman"},
        {"code": "222", "name": "William Asbury Harshbarger", "born": "1 Sep 1862"},
        {"code": "223", "name": "Emma Rebecca Harshbarger", "born": "1864"},
        {"code": "224", "name": "Isaac Hebron Harshbarger", "born": "11 Oct 1866"},
        {"code": "225", "name": "Jeremiah Wesley Harshbarger", "born": "29 Nov 1870", "died": "1 Feb 1872", "verified_terminal": True},
        {"code": "226", "name": "George Crosfield Harshbarger", "born": "18 Dec 1878"},
        {"code": "227", "name": "Jennie Lavina Harshbarger", "born": "18 May 1883", "died": "15 May 1974", "verified_terminal": True, "details": "b. at Tunnelton, WV"},
    ],
})

ENTRIES.append({
    "code": "212",
    "name": "Wilber Finley Frankhouser",
    "sex": "M",
    "born": "12 Sep 1870",
    "died": "11 Mar 1957",
    "spouses": [{"name": "(Dot) Malinda Jane Mosser", "born": "1 Apr 1871", "died": "22 Feb 1961"}],
    "source": {"pdf": "William_Guthrie - One Generation.pdf", "page": 1},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "2121", "name": "Ometa Blanch Frankhouser", "born": "3 Mar 1905", "died": "11 Sep 1905", "verified_terminal": True},
        {"code": "2122", "name": "Carl Frankhouser", "verified_terminal": True},
        {"code": "2123", "name": "Chester Frankhouser", "verified_terminal": True},
        {"code": "2124", "name": "Iva Frankhouser"},
    ],
})

ENTRIES.append({
    "code": "215",
    "name": "Walter C. Frankhouser",
    "sex": "M",
    "born": "19 Jan 1880",
    "died": "3 May 1958",
    "spouses": [{"name": "Lula P. Younkin", "born": "30 Nov 1886", "died": "23 Nov 1935"}],
    "source": {"pdf": "William_Guthrie - One Generation.pdf", "page": 1},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": "Wife dau of Winfield Scott and Henrietta Younkin"},
    "children": [
        {"code": "2151", "name": "Scott Frankhouser", "born": "22 Sep 1911", "died": "22 Sep 1911", "verified_terminal": True, "flags": {"diedInInfancy": True}},
    ],
})

ENTRIES.append({
    "code": "2124",
    "name": "Iva Frankhouser",
    "sex": "F",
    "spouses": [{"name": "James R. Griffith", "born": "26 Jan 1887", "died": "2 Feb 1977", "details": "son of Andrew and Mariah [Barbour] Griffin"}],
    "source": {"pdf": "William_Guthrie - One Generation.pdf", "page": 2},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "21241", "name": "Doris Frankhouser", "verified_terminal": True, "details": "m. Wilbur Dale Hartley"},
    ],
})

ENTRIES.append({
    "code": "222",
    "name": "William Asbury Harshbarger",
    "sex": "M",
    "born": "1 Sep 1862",
    "died": "17 Jul 1942",
    "spouses": [{"name": "Lucy Platt", "born": "16 Aug 1866", "died": "27 Jul 1953", "married": "22 Jun 1888"}],
    "source": {"pdf": "William_Guthrie - One Generation.pdf", "page": 1},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": "Dr Harshbarger was a math professor at Washburn College, Topeka, KS for 50 yrs"},
    "children": [
        {"code": "2221", "name": "Eugene Lee Harshbarger", "born": "12 Dec 1889"},
        {"code": "2222", "name": "Frank Victor Harshbarger", "born": "23 Oct 1893"},
        {"code": "2223", "name": "Ralph Platt Harshbarger", "died": "in infancy", "flags": {"diedInInfancy": True}, "verified_terminal": True},
        {"code": "2224", "name": "Ray Stratton Harshbarger", "born": "24 Jul 1903", "died": "7 Jul 1955", "verified_terminal": True, "details": "m. Rachel Scott, b. 24 Dec 1900"},
    ],
})

ENTRIES.append({
    "code": "223",
    "name": "Emma Rebecca Harshbarger",
    "sex": "F",
    "born": "1864",
    "died": "May 1935",
    "spouses": [{"name": "J. Hood Whetsell", "died": "1945"}],
    "source": {"pdf": "William_Guthrie - One Generation.pdf", "page": 2},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "2231", "name": "Mabelle (Mable) Whetsell", "verified_terminal": True, "details": "m. Arthur T. Hopwood; lived in Morgantown, WV"},
    ],
})

ENTRIES.append({
    "code": "224",
    "name": "Isaac Hebron (Heb) Harshbarger",
    "sex": "M",
    "born": "11 Oct 1866",
    "died": "20 Mar 1936",
    "died_place": "Jacksonville, FL",
    "occupation": "Railroad mail clerk",
    "spouses": [{"name": "Hattie Derring"}],
    "source": {"pdf": "William_Guthrie - One Generation.pdf", "page": 2},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "2241", "name": "Helen Harshbarger", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "226",
    "name": "George Crosfield Harshbarger",
    "sex": "M",
    "born": "18 Dec 1878",
    "spouses": [{"name": "Olive Twig"}],
    "source": {"pdf": "William_Guthrie - One Generation.pdf", "page": 2},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": "Lived in South Cumberland, MD"},
    "children": [
        {"code": "2261", "name": "Eleanor Harshbarger"},
        {"code": "2262", "name": "Mary Louise Harshbarger", "born": "17 Apr 1913"},
        {"code": "2263", "name": "William Lee Harshbarger", "born": "24 Jun 1915"},
        {"code": "2264", "name": "Emma Lucille Harshbarger", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "2221",
    "name": "Eugene Lee Harshbarger",
    "sex": "M",
    "born": "12 Dec 1889",
    "died": "14 Jun 1965",
    "spouses": [{"name": "Thirza"}],
    "source": {"pdf": "William_Guthrie - One Generation.pdf", "page": 2},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "22211", "name": "Eugene Lee Harshbarger, Jr."},
        {"code": "22212", "name": "Carolyn Harshbarger"},
    ],
})

ENTRIES.append({
    "code": "2222",
    "name": "Frank Victor Harshbarger",
    "sex": "M",
    "born": "23 Oct 1893",
    "died": "1 Apr 1944",
    "spouses": [{"name": "Wilma Perry", "born": "12 Jan 1896", "died": "11 Jan 1985"}],
    "source": {"pdf": "William_Guthrie - One Generation.pdf", "page": 2},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "22221", "name": "Frank Victor Harshbarger, Jr.", "born": "1 Nov 1923"},
        {"code": "22222", "name": "Marjorie Harshbarger", "born": "13 Feb 1930"},
    ],
})

ENTRIES.append({
    "code": "2261",
    "name": "Eleanor Harshbarger",
    "sex": "F",
    "spouses": [{"name": "Douglas Stevans"}],
    "source": {"pdf": "William_Guthrie - One Generation.pdf", "page": 2},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "22611", "name": "Patricia", "verified_terminal": True},
        {"code": "22612", "name": "Charles", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "2262",
    "name": "Mary Louise Harshbarger",
    "sex": "F",
    "born": "17 Apr 1913",
    "spouses": [
        {"name": "Paul Brower", "order": 1},
        {"name": "George Keller", "order": 2},
    ],
    "source": {"pdf": "William_Guthrie - One Generation.pdf", "page": 2},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "22621", "name": "Karen Lee Brower", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "2263",
    "name": "William Lee Harshbarger",
    "sex": "M",
    "born": "24 Jun 1915",
    "spouses": [{"name": "Mary", "born": "9 Dec 1914"}],
    "source": {"pdf": "William_Guthrie - One Generation.pdf", "page": 2},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "22631", "name": "James William Harshbarger", "born": "18 Oct 1941", "verified_terminal": True},
        {"code": "22632", "name": "George Harshbarger", "born": "31 May 1944", "verified_terminal": True, "details": "m. Margaret"},
        {"code": "22633", "name": "Anne Harshbarger", "born": "4 Dec 1947"},
    ],
})

ENTRIES.append({
    "code": "22211",
    "name": "Eugene Lee Harshbarger, Jr.",
    "sex": "M",
    "spouses": [{"name": "Gladys"}],
    "source": {"pdf": "William_Guthrie - One Generation.pdf", "page": 2},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "222111", "name": "Douglas Harshbarger", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "22212",
    "name": "Carolyn Harshbarger",
    "sex": "F",
    "spouses": [{"name": "A. B. C. (Gus) Johns"}],
    "source": {"pdf": "William_Guthrie - One Generation.pdf", "page": 3},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "222121", "name": "Elizabeth Thirza Johns", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "22221",
    "name": "Frank Victor Harshbarger, Jr.",
    "sex": "M",
    "born": "1 Nov 1923",
    "spouses": [{"name": "Mary Lois Collins", "born": "7 Jun 1933", "married": "2 Dec 1956"}],
    "source": {"pdf": "William_Guthrie - One Generation.pdf", "page": 3},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "222211", "name": "Sharon Marie Harshbarger", "born": "24 Sep 1957"},
        {"code": "222212", "name": "Frank Victor Harshbarger, III", "born": "9 Sep 1958", "verified_terminal": True},
        {"code": "222213", "name": "Mary Patricia Harshbarger", "born": "6 Dec 1959"},
        {"code": "222214", "name": "Linda Ann Harshbarger", "born": "2 Sep 1961", "verified_terminal": True},
        {"code": "222215", "name": "Raymond Stephan Harshbarger", "born": "18 Jul 1966", "verified_terminal": True},
        {"code": "222216", "name": "Diane Harshbarger", "born": "16 Oct 1967", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "22222",
    "name": "Marjorie Harshbarger",
    "sex": "F",
    "born": "13 Feb 1930",
    "spouses": [{"name": "Joseph Latms", "born": "14 Jan 1930"}],
    "source": {"pdf": "William_Guthrie - One Generation.pdf", "page": 3},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "222221", "name": "Karen Latms", "born": "2 Aug 1954", "verified_terminal": True},
        {"code": "222222", "name": "Janet Kay Latms", "born": "14 Jun 1955", "died": "13 May 1984", "verified_terminal": True, "details": "m. Garry Mitchell"},
        {"code": "222223", "name": "Nancy Jo Latms", "born": "8 Oct 1964", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "22633",
    "name": "Anne Harshbarger",
    "sex": "F",
    "born": "4 Dec 1947",
    "spouses": [{"name": "Dennis Dunn"}],
    "source": {"pdf": "William_Guthrie - One Generation.pdf", "page": 3},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "226331", "name": "Roger Dunn", "born": "26 Jul 1976", "verified_terminal": True},
        {"code": "226332", "name": "Lindsay Dunn", "born": "19 Feb 1979", "verified_terminal": True},
        {"code": "226333", "name": "Sarah Elizabeth Dunn", "born": "6 Jan 1981", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "222211",
    "name": "Sharon Marie Harshbarger",
    "sex": "F",
    "born": "24 Sep 1957",
    "spouses": [
        {"name": "Rich Bankhrad", "order": 1},
        {"name": "William Anderson", "order": 2},
    ],
    "source": {"pdf": "William_Guthrie - One Generation.pdf", "page": 3},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "2222111", "name": "Joshua Jo Bankhead", "born": "21 Apr 1977", "verified_terminal": True},
        {"code": "2222112", "name": "Daniel Anderson", "born": "17 Jul 1986", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "222213",
    "name": "Mary Patricia Harshbarger",
    "sex": "F",
    "born": "6 Dec 1959",
    "spouses": [
        {"name": "Edward Moomau", "order": 1},
        {"name": "Shawn Peters", "married": "1 May 1988", "order": 2},
    ],
    "source": {"pdf": "William_Guthrie - One Generation.pdf", "page": 3},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "2222131", "name": "Lori Marie Moomau", "born": "2 Jun 1978", "verified_terminal": True},
        {"code": "2222132", "name": "Denise Nicole Moomau", "born": "4 Sep 1980", "verified_terminal": True},
        {"code": "2222133", "name": "Jed Vincent Moomua", "born": "10 Oct 1981", "verified_terminal": True},
        {"code": "2222134", "name": "Derick Peters", "born": "23 Aug 1989", "verified_terminal": True},
    ],
})

# Rachel branch
ENTRIES.append({
    "code": "6",
    "name": "Rachel Guthrie",
    "sex": "F",
    "born": "16 Apr 1804",
    "died": "28 Sep 1874",
    "buried": "Shady Grove Cemetery",
    "spouses": [{"name": "James G. Crawford", "born": "25 Jun 1815", "died": "22 Feb 1902", "married": "1827"}],
    "source": {"pdf": "Rachel_Guthrie - One Generation.pdf", "page": 1},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": "Husband son of James and Maragret Hamilton [Gills] Crawford"},
    "children": [
        {"code": "61", "name": "Absalom G. Crawford", "born": "27 Jul 1842", "died": "19 Jan 1848", "verified_terminal": True},
        {"code": "62", "name": "Isabel Crawford"},
        {"code": "63", "name": "Rachel Jane Crawford", "born": "1847"},
        {"code": "64", "name": "Virginia Crawford", "verified_terminal": True, "details": "m. William Gillis"},
        {"code": "65", "name": "Mary Ann Crawford", "verified_terminal": True, "details": "m. Calvin Smith"},
    ],
})

ENTRIES.append({
    "code": "62",
    "name": "Isabel Crawford",
    "sex": "F",
    "spouses": [{"name": "Hamilton Gillis"}],
    "source": {"pdf": "Rachel_Guthrie - One Generation.pdf", "page": 1},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "621", "name": "Allie Gillis", "verified_terminal": True},
        {"code": "622", "name": "James Gillis", "verified_terminal": True},
        {"code": "623", "name": "Lydia Gillis", "verified_terminal": True},
        {"code": "624", "name": "Maggie Gillis", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "63",
    "name": "Rachel Jane Crawford",
    "sex": "F",
    "born": "1847",
    "died": "28 Nov 1919",
    "spouses": [{"name": "William F. Thomas", "born": "16 Apr 1853", "died": "19 Feb 1930"}],
    "source": {"pdf": "Rachel_Guthrie - One Generation.pdf", "page": 1},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "631", "name": "James Thomas", "died": "1952"},
        {"code": "632", "name": "Mary (Maggie) Thomas", "died": "1948"},
    ],
})

ENTRIES.append({
    "code": "631",
    "name": "James Thomas",
    "sex": "M",
    "died": "1952",
    "spouses": [{"name": "Estelle Seese", "details": "sister of Bryce Seese"}],
    "source": {"pdf": "Rachel_Guthrie - One Generation.pdf", "page": 1},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "6311", "name": "Paul Thomas", "verified_terminal": True},
        {"code": "6312", "name": "Rachel Thomas", "verified_terminal": True},
        {"code": "6313", "name": "Viola Thomas", "verified_terminal": True},
        {"code": "6314", "name": "Fred Thomas", "verified_terminal": True, "flags": {"adopted": True}},
    ],
})

ENTRIES.append({
    "code": "632",
    "name": "Mary (Maggie) Thomas",
    "sex": "F",
    "died": "1948",
    "spouses": [{"name": "Albert Meyers", "details": "Meyers or Myers"}],
    "source": {"pdf": "Rachel_Guthrie - One Generation.pdf", "page": 1},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "6321", "name": "Viola Meyers", "verified_terminal": True},
        {"code": "6322", "name": "William Meyers", "verified_terminal": True, "flags": {"diedInInfancy": True}, "died": "in infancy"},
    ],
})


# === Stephen PDF pages 1-6 vision pass (2026-06-08): full branch detail ===
ENTRIES.append({
    "code": "5A",
    "name": "Florence Guthrie",
    "sex": "F",
    "born": "1854",
    "died": "1887",
    "source": {"pdf": "Stephen_Guthrie - One Generation.pdf", "page": 1},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
})

ENTRIES.append({
    "code": "532",
    "name": "Samuel Spencer Guthrie",
    "sex": "M",
    "born": "1858",
    "died": "1927",
    "spouses": [{"name": "Julia D. Deahl", "born": "1860", "died": "1928", "married": "10 Apr 1884"}],
    "source": {"pdf": "Stephen_Guthrie - One Generation.pdf", "page": 2},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "5321", "name": "William H. Guthrie", "born": "8 Mar 1885", "died": "1894", "verified_terminal": True},
        {"code": "5322", "name": "Mary Alice Guthrie", "born": "6 Nov 1887"},
        {"code": "5323", "name": "Rosa F. Guthrie", "born": "1889", "died": "24 Jan 1905", "verified_terminal": True},
        {"code": "5324", "name": "Julia Carolyn Guthrie", "born": "1892", "died": "1892", "verified_terminal": True},
        {"code": "5325", "name": "Roy Leslie Guthrie", "born": "18 Feb 1894"},
        {"code": "5326", "name": "Russell Guthrie"},
        {"code": "5327", "name": "Ruby Guthrie", "born": "1898"},
        {"code": "5328", "name": "Grace Guthrie", "born": "1900", "verified_terminal": True, "details": "m. Jasper McCrobie, b. 1897, d. 1982"},
        {"code": "5329", "name": "Elizabeth Guthrie", "born": "1902", "died": "1955", "verified_terminal": True},
        {"code": "532A", "name": "Lee Guthrie"},
    ],
})

ENTRIES.append({
    "code": "5322",
    "name": "Mary Alice Guthrie",
    "sex": "F",
    "born": "6 Nov 1887",
    "died": "Mar 1952",
    "spouses": [{"name": "Chester Victor Cupp", "born": "1878", "died": "1955"}],
    "source": {"pdf": "Stephen_Guthrie - One Generation.pdf", "page": 3},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "53221", "name": "Alberta Cupp", "verified_terminal": True, "details": "m. Mr. Beatty"},
        {"code": "53222", "name": "Woodrow W. Cupp", "born": "25 Sep 1912", "died": "1935", "verified_terminal": True},
        {"code": "53223", "name": "Elizabeth Cupp", "born": "1914", "died": "1933", "verified_terminal": True},
        {"code": "53224", "name": "Mary Grace Cupp", "verified_terminal": True},
        {"code": "53225", "name": "Virginia Cupp", "verified_terminal": True},
        {"code": "53226", "name": "John Cupp", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "5325",
    "name": "Roy Leslie Guthrie",
    "sex": "M",
    "born": "18 Feb 1894",
    "died": "1969",
    "spouses": [{"name": "Elizabeth V. Ramsey", "born": "1895", "died": "1976"}],
    "source": {"pdf": "Stephen_Guthrie - One Generation.pdf", "page": 4},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "53251", "name": "Julia Maragret Guthrie", "born": "1917", "died": "1974", "verified_terminal": True},
        {"code": "53252", "name": "Charles S. Guthrie", "born": "1918", "died": "1971", "verified_terminal": True},
        {"code": "53253", "name": "Leslie Hadden Guthrie", "born": "24 Oct 1920"},
        {"code": "53254", "name": "Helen Virginia Guthrie", "born": "1924", "died": "1986", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "53253",
    "name": "Leslie Hadden Guthrie",
    "sex": "M",
    "born": "24 Oct 1920",
    "spouses": [{"name": "Ruth B. Nightingale", "married": "27 Dec 1941"}],
    "source": {"pdf": "Stephen_Guthrie - One Generation.pdf", "page": 5},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "532531", "name": "Linda Ruth Guthrie", "born": "1 Nov 1946"},
        {"code": "532532", "name": "Colleen K. Guthrie", "born": "2 Nov 1951"},
    ],
})

ENTRIES.append({
    "code": "532531",
    "name": "Linda Ruth Guthrie",
    "sex": "F",
    "born": "1 Nov 1946",
    "source": {"pdf": "Stephen_Guthrie - One Generation.pdf", "page": 6},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "5325311", "name": "Kimberley Ann Pettey", "born": "1964"},
        {"code": "5325312", "name": "Michael Andrew Soland", "born": "1969", "verified_terminal": True},
        {"code": "5325313", "name": "Kelly Vallencourt", "born": "1979", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "532532",
    "name": "Colleen Kay Guthrie",
    "sex": "F",
    "born": "2 Nov 1951",
    "spouses": [{"name": "Randal Worley"}],
    "source": {"pdf": "Stephen_Guthrie - One Generation.pdf", "page": 6},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "5325321", "name": "Deanna Worley", "born": "1980", "verified_terminal": True},
        {"code": "5325322", "name": "Nathan Leslie Worley", "born": "1982", "verified_terminal": True},
        {"code": "5325323", "name": "Mathew Worley", "born": "1985", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "5325311",
    "name": "Kimberly Ann Pettey",
    "sex": "F",
    "born": "1964",
    "spouses": [{"name": "Timmothy McKenzie", "born": "1960"}],
    "source": {"pdf": "Stephen_Guthrie - One Generation.pdf", "page": 6},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "53253111", "name": "James Hadden McKenzie", "born": "Mar 1990", "verified_terminal": True},
        {"code": "53253112", "name": "Candice McKenzie", "born": "1992", "verified_terminal": True},
        {"code": "53253113", "name": "Christina Bell McKenzie", "born": "Jan 1994", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "536",
    "name": "Zana Estella Guthrie",
    "sex": "F",
    "born": "25 Nov 1875",
    "died": "3 Nov 1941",
    "spouses": [
        {"name": "William H. G. Strawser", "born": "1859", "married": "16 Feb 1892", "order": 1},
        {"name": "Joshua Grant Bishop", "died": "1951", "married": "22 Mar 1903", "order": 2},
    ],
    "source": {"pdf": "Stephen_Guthrie - One Generation.pdf", "page": 2},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "5361", "name": "Henry Stephen Bishop", "born": "9 Jan 1904"},
        {"code": "5362", "name": "Frederick William Bishop", "born": "9 May 1907"},
        {"code": "5363", "name": "Edgar Wayne Bishop", "born": "1 Sep 1909", "died": "6 Nov 1985", "verified_terminal": True},
        {"code": "5364", "name": "Ivan Paul Bishop", "verified_terminal": True, "details": "foster daughter Elizabeth Carol Bishop"},
    ],
})

ENTRIES.append({
    "code": "5361",
    "name": "Henry Stephen Bishop",
    "sex": "M",
    "born": "9 Jan 1904",
    "died": "15 Mar 1980",
    "spouses": [{"name": "Goldie Marie Radabaugh", "born": "30 Aug 1909", "married": "24 Jun 1928"}],
    "source": {"pdf": "Stephen_Guthrie - One Generation.pdf", "page": 4},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": "Wife dau of James Abram and Lucinda Delilah [Christopher] Radabaugh"},
    "children": [
        {"code": "53611", "name": "Virginia Maxine Bishop", "born": "17 Nov 1931"},
        {"code": "53612", "name": "Marvin Paul Bishop"},
        {"code": "53613", "name": "Willis Kay Bishop", "born": "5 Sep 1943"},
    ],
})

ENTRIES.append({
    "code": "5362",
    "name": "Frederick William Bishop",
    "sex": "M",
    "born": "9 May 1907",
    "died": "5 Dec 1976",
    "spouses": [{"name": "Vernace Burl Gibson", "born": "21 Jun 1913"}],
    "source": {"pdf": "Stephen_Guthrie - One Generation.pdf", "page": 4},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": "Wife dau of Thomas Hall and Alta May [Christopher] Gibson"},
    "children": [
        {"code": "53621", "name": "Willis Ray Bishop", "born": "21 Apr 1929", "died": "21 Apr 1929", "verified_terminal": True},
        {"code": "53622", "name": "Everett Clayton Bishop", "born": "23 Aug 1930"},
        {"code": "53623", "name": "Lula Berlene Bishop", "born": "1 Mar 1933"},
        {"code": "53624", "name": "Violet Rosalee Bishop", "born": "15 Jul 1935"},
        {"code": "53625", "name": "Robert Allen Bishop"},
        {"code": "53626", "name": "Alfred Lee Bishop", "born": "18 Oct 1942"},
        {"code": "53627", "name": "Joyce Lynne Bishop", "born": "16 Nov 1948", "verified_terminal": True, "details": "m. 21 Apr 1973 Christopher Columbus Tatham Jr."},
        {"code": "53628", "name": "Judy Anne Bishop", "born": "16 Nov 1948", "verified_terminal": True, "details": "m. 7 Mar 1970 Robert Z. O'Connor"},
    ],
})

ENTRIES.append({
    "code": "53611",
    "name": "Virginia Maxine Bishop",
    "sex": "F",
    "born": "17 Nov 1931",
    "spouses": [{"name": "Russell Lee (Wege) Sliger", "born": "23 Sep 1930", "married": "18 Nov 1950"}],
    "source": {"pdf": "Stephen_Guthrie - One Generation.pdf", "page": 5},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": "Husband son of Samuel R. and Freda M. [Duffner] Sliger"},
    "children": [
        {"code": "536111", "name": "Iva Lucinda Sliger", "born": "10 Dec 1951", "verified_terminal": True, "details": "m. 20 Jun 1970 James Edward Cummings"},
        {"code": "536112", "name": "Vivetta Sue Sliger", "born": "11 Feb 1956", "verified_terminal": True},
        {"code": "536113", "name": "Brindley Lee Sliger", "born": "14 Oct 1960", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "53612",
    "name": "Marvin Paul Bishop",
    "sex": "M",
    "spouses": [{"name": "Charlotte Ella Sanders", "born": "2 May 1937", "married": "14 Nov 1955"}],
    "source": {"pdf": "Stephen_Guthrie - One Generation.pdf", "page": 5},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": "Wife dau of Franklin W. and Ellen E. [Albright] Sanders"},
    "children": [
        {"code": "536121", "name": "James Marvin Bishop", "born": "17 Jul 1958", "verified_terminal": True},
        {"code": "536122", "name": "Philip Brent Bishop", "born": "26 Mar 1963"},
    ],
})

ENTRIES.append({
    "code": "53613",
    "name": "Willis Kay Bishop",
    "sex": "M",
    "born": "16 Sep 1943",
    "spouses": [{"name": "Carolyn Sue Bolinger", "born": "2 Aug 1947", "married": "16 Sep 1967"}],
    "source": {"pdf": "Stephen_Guthrie - One Generation.pdf", "page": 5},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": "Wife dau of Lloyd and Alma [Davis] Bolinger"},
    "children": [
        {"code": "536131", "name": "Eric Willis Bishop", "born": "7 Jan 1969", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "53622",
    "name": "Everett Clayton Bishop",
    "sex": "M",
    "born": "23 Aug 1930",
    "spouses": [{"name": "Francis Linn Williams", "born": "30 Apr 1937", "married": "2 Jun 1957"}],
    "source": {"pdf": "Stephen_Guthrie - One Generation.pdf", "page": 5},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": "Wife dau of Robert Kenneth and Gail Mildred [Torry] Williams"},
    "children": [
        {"code": "536221", "name": "Michael Jay Bishop", "born": "19 Oct 1959", "verified_terminal": True},
        {"code": "536222", "name": "Beth Ann Bishop", "born": "28 Apr 1962", "verified_terminal": True},
        {"code": "536223", "name": "Lynn Ann Bishop", "born": "28 Jul 1963", "verified_terminal": True},
        {"code": "536224", "name": "Patrick Everett Bishop", "born": "16 Aug 1966", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "53623",
    "name": "Lula Berlene Bishop",
    "sex": "F",
    "born": "1 Mar 1933",
    "spouses": [{"name": "Richard (Dick) Marvin Miller", "born": "15 Jul 1932", "married": "21 Jun 1952"}],
    "source": {"pdf": "Stephen_Guthrie - One Generation.pdf", "page": 5},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": "Husband son of Loyd T. (Red) and Dortha [Frankhouser] Miller"},
    "children": [
        {"code": "536231", "name": "Trudy Renell Miller", "born": "6 Nov 1954"},
        {"code": "536232", "name": "Gregory Marvin Miller", "born": "7 May 1956"},
    ],
})

ENTRIES.append({
    "code": "53624",
    "name": "Violet Rosalee Bishop",
    "sex": "F",
    "born": "15 Jul 1935",
    "spouses": [{"name": "Perry Wendell Rhodes", "born": "27 Nov 1934", "married": "11 Feb 1956"}],
    "source": {"pdf": "Stephen_Guthrie - One Generation.pdf", "page": 5},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": "Husband son of Lester Valentine and Hilda Catherine [Weaver] Rhodes"},
    "children": [
        {"code": "536241", "name": "Randal Alan Rhodes", "born": "11 Feb 1957", "verified_terminal": True},
        {"code": "536242", "name": "Robin Lynn Rhodes", "born": "23 Oct 1961", "verified_terminal": True},
        {"code": "536243", "name": "Rhonda Jo Rhodes", "born": "2 Feb 1963", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "53625",
    "name": "Robert Allen Bishop",
    "sex": "M",
    "spouses": [{"name": "Lela Elaine Thompson", "born": "9 Dec 1938", "details": "dau of Harry Babe and Lela Erma [Wright] Thompson"}],
    "source": {"pdf": "Stephen_Guthrie - One Generation.pdf", "page": 5},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "536251", "name": "Robin Lynn Bishop", "born": "17 Jan 1962", "verified_terminal": True},
        {"code": "536252", "name": "Dawn Renee Bishop", "born": "20 Feb 1965", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "53626",
    "name": "Alfred Lee Bishop",
    "sex": "M",
    "born": "18 Oct 1942",
    "spouses": [{"name": "Shirley Lee Maxwell", "born": "7 Jul 1941", "married": "30 Apr 1963", "details": "dau of Nelson and Pearl Elizabeth [Brooks] Maxwell"}],
    "source": {"pdf": "Stephen_Guthrie - One Generation.pdf", "page": 6},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "536261", "name": "Frederick Nelson Bishop", "born": "4 May 1963", "verified_terminal": True},
        {"code": "536262", "name": "Stephanie Lee Bishop", "born": "6 Nov 1967", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "536122",
    "name": "Philip Brent Bishop",
    "sex": "M",
    "born": "26 Mar 1963",
    "spouses": [{"name": "Barbara Annette Dietz", "born": "16 Apr 1962", "married": "4 Nov 1981", "details": "dau of John and Betty (Summers) Dietz"}],
    "source": {"pdf": "Stephen_Guthrie - One Generation.pdf", "page": 6},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "5361221", "name": "Brandon Philip Bishop", "born": "30 Dec 1981", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "536231",
    "name": "Trudy Renell Miller",
    "sex": "F",
    "born": "6 Nov 1954",
    "spouses": [{"name": "John Mitchell Humberson", "details": "son of John W. and Algene (Mitchell) Humberson"}],
    "source": {"pdf": "Stephen_Guthrie - One Generation.pdf", "page": 6},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "5362311", "name": "Stacy Renell Humberson", "born": "20 Oct 1977", "verified_terminal": True},
        {"code": "5362312", "name": "Arron Humberson", "verified_terminal": True},
        {"code": "5362313", "name": "Abby Nicole Humberson", "born": "13 Jul 1988", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "536232",
    "name": "Gregory Marvin Miller",
    "sex": "M",
    "born": "7 May 1956",
    "spouses": [{"name": "Renita Jo Bishoff", "details": "dau of George David and Helen Y. (Savage) Bishoff"}],
    "source": {"pdf": "Stephen_Guthrie - One Generation.pdf", "page": 6},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "5362321", "name": "Chasity Jo Bishoff", "born": "7 May 1975", "verified_terminal": True},
        {"code": "5362322", "name": "Justin Michael Bishoff", "born": "31 Dec 1978", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "565",
    "name": "Kenneth Bruce Frankhouser",
    "sex": "M",
    "born": "5 Dec 1868",
    "died": "12 Oct 1941",
    "spouses": [{"name": "Sarah E. Felton", "born": "28 Mar 1865", "died": "1 Sep 1928"}],
    "source": {"pdf": "Stephen_Guthrie - One Generation.pdf", "page": 2},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "5651", "name": "Hazel Grace Frankhouser", "born": "20 Jul 1900", "verified_terminal": True},
        {"code": "5652", "name": "Orlando Felton Frankhouser", "born": "1901"},
        {"code": "5653", "name": "Daniel Henry Frankhouser", "born": "1902", "died": "1963", "verified_terminal": True},
        {"code": "5654", "name": "Edith Mae Frankhouser", "born": "1904", "died": "1947", "verified_terminal": True, "details": "m. Freeland"},
        {"code": "5655", "name": "Kenneth Bruce Frankhouser", "born": "1907", "verified_terminal": True},
        {"code": "5656", "name": "Mary Ruth Frankhouser", "born": "1908", "verified_terminal": True, "details": "m. Roth"},
    ],
})

ENTRIES.append({
    "code": "5652",
    "name": "Orlando Felton Frankhouser",
    "sex": "M",
    "born": "1901",
    "died": "1971",
    "spouses": [{"name": "Mary Taylor", "married": "10 Jun 1942"}],
    "source": {"pdf": "Stephen_Guthrie - One Generation.pdf", "page": 4},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "56521", "name": "Kenneth W. Frankhouser", "born": "5 Oct 1942", "verified_terminal": True},
        {"code": "56522", "name": "Sarah Frances Frankhouser", "born": "19 Jan 1945"},
    ],
})

ENTRIES.append({
    "code": "56522",
    "name": "Sarah Frances Frankhouser",
    "sex": "F",
    "born": "19 Jan 1945",
    "spouses": [{"name": "Ronnie Metheny", "married": "11 Jun 1968"}],
    "source": {"pdf": "Stephen_Guthrie - One Generation.pdf", "page": 6},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "565221", "name": "Allen Lynn Metheny", "born": "9 Dec 1971", "verified_terminal": True},
        {"code": "565222", "name": "Rhonda Sue Metheny", "born": "11 Feb 1975", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "59",
    "name": "Absalom Guthrie",
    "sex": "M",
    "died": "1899",
    "buried": "Kansas",
    "spouses": [{"name": "Demaris Denham", "died": "11 Sep 1916"}],
    "source": {"pdf": "Stephen_Guthrie - One Generation.pdf", "page": 1},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": "Stephen's son who died in Kansas (distinct from 8 Absalom)"},
    "children": [
        {"code": "591", "name": "Belle Guthrie"},
        {"code": "592", "name": "Jennie Guthrie"},
        {"code": "593", "name": "Ezra Guthrie"},
        {"code": "594", "name": "Stephen Dudley Guthrie"},
        {"code": "595", "name": "Harrison H. Guthrie", "verified_terminal": True},
        {"code": "596", "name": "Thomas Harlic Guthrie"},
        {"code": "597", "name": "Alva Arthur Guthrie"},
        {"code": "598", "name": "Gadi Gilford Guthrie"},
        {"code": "599", "name": "Mary Jane Guthrie"},
        {"code": "59A", "name": "Levi Leroy Guthrie"},
        {"code": "59B", "name": "Gertrude Guthrie"},
    ],
})

ENTRIES.append({
    "code": "592",
    "name": "Jennie Guthrie",
    "sex": "F",
    "spouses": [{"name": "James Corbin"}],
    "source": {"pdf": "Stephen_Guthrie - One Generation.pdf", "page": 2},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "5921", "name": "Lewis Corbin", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "593",
    "name": "Ezra Guthrie",
    "sex": "M",
    "spouses": [{"name": "Lillie Hightower", "died": "1913"}],
    "source": {"pdf": "Stephen_Guthrie - One Generation.pdf", "page": 2},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "5931", "name": "Ida Guthrie", "verified_terminal": True},
        {"code": "5932", "name": "Edna Guthrie", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "598",
    "name": "Gadi Gilford Guthrie",
    "sex": "M",
    "spouses": [{"name": "Edna Graves"}],
    "source": {"pdf": "Stephen_Guthrie - One Generation.pdf", "page": 3},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "5981", "name": "Frances Guthrie", "verified_terminal": True},
        {"code": "5982", "name": "Hoyland Menette Guthrie", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "599",
    "name": "Mary Jane Guthrie",
    "sex": "F",
    "spouses": [{"name": "Edward Stevens"}],
    "source": {"pdf": "Stephen_Guthrie - One Generation.pdf", "page": 3},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "5991", "name": "Neva Stevens", "verified_terminal": True},
        {"code": "5992", "name": "Nola Stevens", "verified_terminal": True},
        {"code": "5993", "name": "Gertrude Stevens", "verified_terminal": True},
        {"code": "5994", "name": "Edna Stevens", "verified_terminal": True},
        {"code": "5995", "name": "Dayton Stevens", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "59A",
    "name": "Levi Leroy Guthrie",
    "sex": "M",
    "spouses": [{"name": "Adeline Wylie"}],
    "source": {"pdf": "Stephen_Guthrie - One Generation.pdf", "page": 3},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "59A1", "name": "Lavina Guthrie", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "59B",
    "name": "Gertrude Guthrie",
    "sex": "F",
    "spouses": [{"name": "William Wylie"}],
    "source": {"pdf": "Stephen_Guthrie - One Generation.pdf", "page": 3},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "59B1", "name": "Bertram Wylie", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "594",
    "name": "Stephen Dudley Guthrie",
    "sex": "M",
    "spouses": [{"name": "Lillie May Whithorn", "born": "1873", "married": "1893"}],
    "source": {"pdf": "Stephen_Guthrie - One Generation.pdf", "page": 3},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "5941", "name": "Oma Gertrude Guthrie", "born": "26 Dec 1894"},
        {"code": "5942", "name": "Leon Eugene Guthrie", "born": "16 Feb 1897"},
        {"code": "5943", "name": "Stephen Leroy Guthrie", "born": "1900", "died": "in infancy", "flags": {"diedInInfancy": True}, "verified_terminal": True},
        {"code": "5944", "name": "Edna Victoria Guthrie", "born": "1904", "verified_terminal": True, "details": "m. 1926 to Lylie Munn"},
        {"code": "5945", "name": "Cyrus Sylvester Guthrie", "born": "14 May 1909", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "5941",
    "name": "Oma Gertrude Guthrie",
    "sex": "F",
    "born": "26 Dec 1894",
    "spouses": [{"name": "Guy D. Hadley", "married": "Jul 1916"}],
    "source": {"pdf": "Stephen_Guthrie - One Generation.pdf", "page": 4},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "59411", "name": "Eileen Hadley", "verified_terminal": True},
        {"code": "59412", "name": "Keith Hadley", "verified_terminal": True},
        {"code": "59413", "name": "Bryce Hadley", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "5942",
    "name": "Leon Eugene Guthrie",
    "sex": "M",
    "born": "16 Feb 1897",
    "spouses": [{"name": "Ethel May Garrison", "born": "30 Aug 1902", "married": "28 Mar 1920"}],
    "source": {"pdf": "Stephen_Guthrie - One Generation.pdf", "page": 5},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "59421", "name": "Welsley B. Garrison", "verified_terminal": True, "details": "m. Valotta Jane Nicholson"},
        {"code": "59422", "name": "Delmar Denzel Garrison", "born": "10 Oct 1923", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "596",
    "name": "Thomas Harlic Guthrie",
    "sex": "M",
    "spouses": [{"name": "Myrtle Wright"}],
    "source": {"pdf": "Stephen_Guthrie - One Generation.pdf", "page": 3},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "5961", "name": "Juanita Guthrie", "verified_terminal": True},
        {"code": "5962", "name": "Bernice Guthrie", "verified_terminal": True},
        {"code": "5963", "name": "Alta Guthrie", "verified_terminal": True},
        {"code": "5964", "name": "Ivalee Guthrie", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "597",
    "name": "Alva Arthur Guthrie",
    "sex": "M",
    "spouses": [{"name": "Eleen Geary"}],
    "source": {"pdf": "Stephen_Guthrie - One Generation.pdf", "page": 3},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "5971", "name": "Arthur Guthrie", "verified_terminal": True},
        {"code": "5972", "name": "Blanche Guthrie", "verified_terminal": True},
        {"code": "5973", "name": "Gifford Guthrie", "verified_terminal": True},
        {"code": "5974", "name": "Frances Guthrie", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "591",
    "name": "Belle Guthrie",
    "sex": "F",
    "spouses": [{"name": "Alva Russell"}],
    "source": {"pdf": "Stephen_Guthrie - One Generation.pdf", "page": 2},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "5911", "name": "Arley Russell", "verified_terminal": True},
        {"code": "5912", "name": "Ira Russell", "verified_terminal": True},
        {"code": "5913", "name": "Pat Russell", "verified_terminal": True},
        {"code": "5914", "name": "Herman Russell", "verified_terminal": True},
        {"code": "5915", "name": "Minnie Russell", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "5326",
    "name": "Russell Guthrie",
    "sex": "M",
    "spouses": [{"name": "Edna Sullivan"}],
    "source": {"pdf": "Stephen_Guthrie - One Generation.pdf", "page": 4},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "53261", "name": "Walter Guthrie", "verified_terminal": True},
        {"code": "53262", "name": "Julia Guthrie", "verified_terminal": True},
        {"code": "53263", "name": "Gladys Guthrie", "verified_terminal": True},
        {"code": "53264", "name": "Russell Guthrie Jr.", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "5327",
    "name": "Ruby Guthrie",
    "sex": "F",
    "born": "1898",
    "died": "6 Sep 1963",
    "spouses": [{"name": "Edward Mason Browning"}],
    "source": {"pdf": "Stephen_Guthrie - One Generation.pdf", "page": 4},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "53271", "name": "Donald Browning", "verified_terminal": True},
        {"code": "53272", "name": "Wilma Browning", "verified_terminal": True, "details": "m. D.P. Stalmaker"},
    ],
})

ENTRIES.append({
    "code": "532A",
    "name": "Lee Guthrie",
    "sex": "M",
    "spouses": [{"name": "Clara Brooks"}],
    "source": {"pdf": "Stephen_Guthrie - One Generation.pdf", "page": 4},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "532A1", "name": "Robert Guthrie", "verified_terminal": True},
        {"code": "532A2", "name": "Carolyn Guthrie", "verified_terminal": True},
    ],
})



# === Alexander PDF pages 7-11 vision pass (2026-06-08): Cupp/Frankhouser/Evans/Frazee gen 5-6 ===
ENTRIES.append({
    "code": "A456",
    "name": "Martin Luther Cupp",
    "sex": "M",
    "born": "9 May 1918",
    "spouses": [{"name": "Mary Jean Guthrie", "born": "29 Aug 1934", "married": "9 May 1953"}],
    "source": {"pdf": "Alexander_Guthrie - Five Generations.pdf", "page": 7},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": "Wife dau of James and Anna [Braham] Guthrie — cross-marriage 13F72"},
    "children": [
        {"code": "A4561", "name": "Martin Edward Cupp", "born": "30 Dec 1953", "verified_terminal": True},
        {"code": "A4562", "name": "Roger Lee Cupp", "born": "13 Mar 1955", "verified_terminal": True},
        {"code": "A4563", "name": "James Melvin Cupp", "born": "13 Oct 1957", "verified_terminal": True},
        {"code": "A4564", "name": "Marvin Dale Cupp", "born": "18 Dec 1959", "verified_terminal": True},
        {"code": "A4565", "name": "Charles Wesley Cupp", "born": "13 Jul 1961"},
        {"code": "A4566", "name": "Richard Glenn Cupp", "born": "17 Sep 1963", "verified_terminal": True},
        {"code": "A4567", "name": "Sharon Louise Cupp", "born": "12 Dec 1965", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "A457",
    "name": "Ray Darwin Cupp",
    "sex": "M",
    "born": "7 Apr 1921",
    "spouses": [{"name": "Joann DeWitt"}],
    "source": {"pdf": "Alexander_Guthrie - Five Generations.pdf", "page": 7},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "A4571", "name": "Rhoda Joann Cupp", "born": "3 Oct 1950", "verified_terminal": True},
        {"code": "A4572", "name": "Luann Rae Cupp", "born": "2 Dec 1953", "verified_terminal": True},
        {"code": "A4573", "name": "Allen Bruce Cupp", "born": "2 May 1956", "verified_terminal": True},
        {"code": "A4574", "name": "Kellye Sue Cupp", "born": "3 Apr 1959", "verified_terminal": True},
        {"code": "A4575", "name": "Darwin DeWitt Cupp", "born": "20 Feb 1961", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "A459",
    "name": "Alma Pearl Cupp",
    "sex": "F",
    "born": "8 Apr 1926",
    "spouses": [{"name": "Clayton Edwin King", "born": "30 Aug 1925", "married": "8 Feb 1947"}],
    "source": {"pdf": "Alexander_Guthrie - Five Generations.pdf", "page": 7},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "A4591", "name": "Sherrie Kay King", "born": "12 Jul 1952"},
    ],
})

ENTRIES.append({
    "code": "AB21",
    "name": "Vesty D. Meyers",
    "sex": "F",
    "spouses": [{"name": "Curlin"}],
    "source": {"pdf": "Alexander_Guthrie - Five Generations.pdf", "page": 7},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "AB211", "name": "Pearly Meyers", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "AB22",
    "name": "Massereen Evans",
    "sex": "F",
    "spouses": [{"name": "Clyde Coates", "died": "1974"}],
    "source": {"pdf": "Alexander_Guthrie - Five Generations.pdf", "page": 7},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "AB221", "name": "Buster Evans", "verified_terminal": True},
        {"code": "AB222", "name": "Harry Coates", "verified_terminal": True},
        {"code": "AB223", "name": "Violet Coates", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "AB23",
    "name": "Wanda M. Evans",
    "sex": "F",
    "spouses": [{"name": "Charles Friend", "born": "3 Apr 1922", "died": "11 Aug 1985"}],
    "source": {"pdf": "Alexander_Guthrie - Five Generations.pdf", "page": 7},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "AB231", "name": "Sylvia Friend", "verified_terminal": True},
        {"code": "AB232", "name": "Shirley Friend", "verified_terminal": True},
        {"code": "AB233", "name": "Kathern Friend", "verified_terminal": True},
        {"code": "AB234", "name": "Vernon Ray Friend", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "AB24",
    "name": "Stanley Regis Evans",
    "sex": "M",
    "born": "23 Oct 1926",
    "spouses": [{"name": "Hazel Fike"}],
    "source": {"pdf": "Alexander_Guthrie - Five Generations.pdf", "page": 7},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "AB241", "name": "Darlene Fike Evans", "verified_terminal": True},
        {"code": "AB242", "name": "Richard Lee Evans", "born": "2 May 1955", "died": "9 Aug 1974", "verified_terminal": True},
        {"code": "AB243", "name": "Terry Lynn Evans", "born": "1956", "verified_terminal": True},
        {"code": "AB244", "name": "Wendy Jo Evans", "born": "12 Nov 1991", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "A2121",
    "name": "Norma Ruth Frazee",
    "sex": "F",
    "born": "30 Aug 1938",
    "spouses": [{"name": "Paul Oliver Frazee", "born": "30 Dec 1927", "died": "20 Feb 1989", "married": "20 Sep 1956"}],
    "source": {"pdf": "Alexander_Guthrie - Five Generations.pdf", "page": 8},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "A21211", "name": "Barbara Ann Frazee", "born": "9 Sep 1957", "verified_terminal": True},
        {"code": "A21212", "name": "Gail Darlene Frazee", "born": "30 Oct 1958", "verified_terminal": True},
        {"code": "A21213", "name": "Paula Sue Frazee", "born": "1 May 1960", "verified_terminal": True},
        {"code": "A21214", "name": "Shirley Jean Frazee", "born": "27 May 1962", "verified_terminal": True},
        {"code": "A21215", "name": "William Owen Frazee", "born": "13 Jan 1975", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "A2122",
    "name": "Glenna Belle Frazee",
    "sex": "F",
    "born": "15 Dec 1940",
    "spouses": [{"name": "Charles Edward Eisentrout", "married": "25 Dec 1958"}],
    "source": {"pdf": "Alexander_Guthrie - Five Generations.pdf", "page": 8},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "A21221", "name": "James Walter Eisentrout", "born": "8 Jan 1960", "verified_terminal": True},
        {"code": "A21222", "name": "Donna Sue Eisentrout", "born": "28 Mar 1962", "verified_terminal": True},
        {"code": "A21223", "name": "Nancy Marie Eisentrout", "born": "3 Oct 1966", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "A2131",
    "name": "Mary Louise Frazee",
    "sex": "F",
    "born": "27 Apr 1941",
    "died": "7 Jan 1966",
    "spouses": [
        {"name": "Robert Carroll Hager Jr.", "born": "18 Aug 1934", "married": "26 Sep 1959", "order": 1},
        {"name": "William Albert Knight", "married": "1 Sep 1967", "order": 2},
    ],
    "source": {"pdf": "Alexander_Guthrie - Five Generations.pdf", "page": 8},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "A21311", "name": "Robert Carroll Hager III", "born": "24 Sep 1960", "verified_terminal": True},
        {"code": "A21312", "name": "Jonathan Allen Hager", "born": "21 Jun 1964", "verified_terminal": True},
        {"code": "A21313", "name": "William Albert Knight", "born": "16 Nov 1967", "verified_terminal": True},
        {"code": "A21314", "name": "Sheri Lynn Knight", "born": "24 Jun 1970", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "A4112",
    "name": "Darwin Hankins Frankhouser",
    "sex": "M",
    "born": "23 Mar 1926",
    "spouses": [{"name": "Elaine Bierer"}],
    "source": {"pdf": "Alexander_Guthrie - Five Generations.pdf", "page": 8},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "A41121", "name": "Darwin Hankins Frankhouser, Jr.", "born": "28 Mar 1957", "verified_terminal": True},
        {"code": "A41122", "name": "Susan Elaine Frankhouser", "born": "14 Nov 1962", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "A4113",
    "name": "Joanne Madelon Frankhouser",
    "sex": "F",
    "born": "7 Jul 1939",
    "spouses": [{"name": "Robert Endsley"}],
    "source": {"pdf": "Alexander_Guthrie - Five Generations.pdf", "page": 8},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "A41131", "name": "Mark Christian Endsley", "born": "10 Oct 1959", "verified_terminal": True},
        {"code": "A41132", "name": "Pamela Anne Endsley", "born": "12 May 1967", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "A4131",
    "name": "John Springer Clark, Jr.",
    "sex": "M",
    "born": "22 Dec 1920",
    "spouses": [{"name": "Dorothy Eicher", "born": "4 Aug 1921"}],
    "source": {"pdf": "Alexander_Guthrie - Five Generations.pdf", "page": 8},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "A41311", "name": "Donna Lee Clark", "born": "16 Jan 1946", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "A4141",
    "name": "Rita Frankhouser",
    "sex": "F",
    "spouses": [{"name": "Charles Bosley"}],
    "source": {"pdf": "Alexander_Guthrie - Five Generations.pdf", "page": 8},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "A41411", "name": "Barbara Bosley", "verified_terminal": True},
        {"code": "A41412", "name": "Brenda Bosley", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "A4151",
    "name": "Geraldine Lorraine Frankhouser",
    "sex": "F",
    "born": "26 Apr 1933",
    "spouses": [{"name": "Roy Chuck", "born": "11 Dec 1924"}],
    "source": {"pdf": "Alexander_Guthrie - Five Generations.pdf", "page": 8},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "A41511", "name": "Diane L. Chuck", "born": "1 Dec 1961", "verified_terminal": True},
        {"code": "A41512", "name": "Douglas Chuck", "born": "23 Sep 1963", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "A4152",
    "name": "Thomas Lee Frankhouser",
    "sex": "M",
    "born": "6 Apr 1934",
    "spouses": [{"name": "Roberta Zaucha", "born": "21 Feb 1936"}],
    "source": {"pdf": "Alexander_Guthrie - Five Generations.pdf", "page": 9},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "A41521", "name": "Lee Alan Frankhouser", "born": "2 Feb 1958", "verified_terminal": True},
        {"code": "A41522", "name": "Gary J. Frankhouser", "born": "15 Nov 1959", "verified_terminal": True},
        {"code": "A41523", "name": "Lisa Beth Frankhouser", "born": "2 May 1961", "verified_terminal": True},
        {"code": "A41524", "name": "Tami Linn Frankhouser", "born": "17 Aug 1962", "verified_terminal": True},
        {"code": "A41525", "name": "Thomas Todd Frankhouser", "born": "2 Sep 1964", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "A4153",
    "name": "Lawrence Emmer Frankhouser",
    "sex": "M",
    "born": "27 Jun 1938",
    "spouses": [{"name": "Dorothy Markutsa", "born": "27 Sep 1937"}],
    "source": {"pdf": "Alexander_Guthrie - Five Generations.pdf", "page": 9},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": "Both children adopted"},
    "children": [
        {"code": "A41531", "name": "Eric Joseph Frankhouser", "born": "10 Nov 1971", "flags": {"adopted": True}, "verified_terminal": True},
        {"code": "A41532", "name": "Jennifer Lynette Frankhouser", "born": "28 Oct 1974", "flags": {"adopted": True}, "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "A4154",
    "name": "Francis G. Frankhouser",
    "sex": "M",
    "born": "22 Sep 1939",
    "spouses": [
        {"name": "Patsy Bryan", "order": 1},
        {"name": "Sarah Thomas", "born": "21 Apr 1956", "order": 2},
    ],
    "source": {"pdf": "Alexander_Guthrie - Five Generations.pdf", "page": 9},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "A41541", "name": "Tina Frankhouser", "born": "21 Apr 1961", "verified_terminal": True},
        {"code": "A41542", "name": "Jennifer Frankhouser", "born": "26 Apr 1976", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "A4512",
    "name": "Jean Elizabeth Cupp",
    "sex": "F",
    "born": "12 Oct 1935",
    "spouses": [{"name": "Ray Underwood", "born": "5 May 1925", "married": "10 Feb 1960"}],
    "source": {"pdf": "Alexander_Guthrie - Five Generations.pdf", "page": 9},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "A45121", "name": "Eileen Patricia Underwood", "born": "8 May 1961", "verified_terminal": True},
        {"code": "A45122", "name": "Lloyd Charles Underwood", "born": "20 May 1963", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "A4513",
    "name": "Darvin Eugene Cupp",
    "sex": "M",
    "born": "28 Jun 1939",
    "spouses": [{"name": "Rose Marie Bettencourt", "born": "19 May 1941", "married": "5 Sep 1959"}],
    "source": {"pdf": "Alexander_Guthrie - Five Generations.pdf", "page": 9},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "A45131", "name": "Ronald Eugene Cupp", "born": "4 Jan 1961", "verified_terminal": True},
        {"code": "A45132", "name": "Rodney Ernest Cupp", "born": "5 Oct 1962", "verified_terminal": True},
        {"code": "A45133", "name": "Renee Elisa Cupp", "born": "23 Jun 1964", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "A4515",
    "name": "Shirley Mae Cupp",
    "sex": "F",
    "born": "2 Jun 1942",
    "spouses": [
        {"name": "David Anderson", "born": "5 Mar 1939", "married": "10 Oct 1959", "order": 1},
        {"name": "Jack Davenport", "born": "23 Aug 1937", "married": "17 Mar 1968", "order": 2},
    ],
    "source": {"pdf": "Alexander_Guthrie - Five Generations.pdf", "page": 9},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "A45151", "name": "Diana Lynn Anderson", "born": "12 May 1960", "verified_terminal": True},
        {"code": "A45152", "name": "Debbie Lou Anderson", "born": "19 May 1961", "verified_terminal": True},
        {"code": "A45153", "name": "Charles Phillip Anderson", "born": "4 Sep 1964", "verified_terminal": True},
        {"code": "A45154", "name": "Tammy Davenport", "born": "23 Aug 1968", "verified_terminal": True},
        {"code": "A45155", "name": "Kimberly Davenport", "born": "21 May 1969", "verified_terminal": True},
        {"code": "A45156", "name": "Keith Davenport", "born": "4 Jun 1972", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "A4551",
    "name": "Ronald Eugene Cupp",
    "sex": "M",
    "born": "8 Jun 1940",
    "spouses": [{"name": "Bonnie Vitez", "born": "26 Oct 1943", "married": "20 Feb 1965"}],
    "source": {"pdf": "Alexander_Guthrie - Five Generations.pdf", "page": 10},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "A45511", "name": "Shelley Cupp", "born": "11 Jul 1965", "died": "25 Jul 1965", "verified_terminal": True},
        {"code": "A45512", "name": "Shawn Cupp", "born": "11 Jul 1965", "died": "25 Jul 1965", "verified_terminal": True},
        {"code": "A45513", "name": "Ronald Scott Cupp", "born": "21 Nov 1968", "verified_terminal": True},
        {"code": "A45514", "name": "Michael Eugene Cupp", "born": "3 Apr 1975", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "A4591",
    "name": "Sherrie Kay King",
    "sex": "F",
    "born": "12 Jul 1952",
    "spouses": [{"name": "John David Smith", "born": "6 Jun 1950", "married": "12 Jul 1975"}],
    "source": {"pdf": "Alexander_Guthrie - Five Generations.pdf", "page": 10},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": "Husband son of Forrest & Ella [Thompson] Smith"},
    "children": [
        {"code": "A44911", "name": "Ryan David Smith", "born": "27 Apr 1984", "verified_terminal": True},
        {"code": "A44912", "name": "Eric Paul Smith", "born": "27 Apr 1984", "verified_terminal": True},
    ],
})


# === Alexander PDF pages 1-6 vision pass (2026-06-08): A founder + gen 2-4 detail ===

ENTRIES.append({
    "code": "A23",
    "name": "Lindley (Lynn) David Guthrie",
    "sex": "M",
    "born": "4 Apr 1873",
    "source": {"pdf": "Alexander_Guthrie - Five Generations.pdf", "page": 1},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": "Lived with brother Abner"},
})

ENTRIES.append({
    "code": "A31",
    "name": "John H. Romesburg",
    "sex": "M",
    "spouses": [{"name": "Myrtle"}],
    "source": {"pdf": "Alexander_Guthrie - Five Generations.pdf", "page": 2},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "A311", "name": "Millie R. Romesburg", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "A33",
    "name": "Lewis F. Romesburg",
    "sex": "M",
    "died": "25 Mar 1952",
    "spouses": [{"name": "Elizabeth"}],
    "source": {"pdf": "Alexander_Guthrie - Five Generations.pdf", "page": 1},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
})

ENTRIES.append({
    "code": "A34",
    "name": "Nicolas O. Romesburg",
    "sex": "M",
    "died": "23 Dec 1953",
    "spouses": [{"name": "Jessie Kennedy", "died": "20 Mar 1952"}],
    "source": {"pdf": "Alexander_Guthrie - Five Generations.pdf", "page": 3},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "A341", "name": "Ellen Romesburg", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "A36",
    "name": "Martha Romesburg",
    "sex": "F",
    "born": "1873",
    "died": "1928",
    "spouses": [{"name": "J.E. Williams", "died": "1951"}],
    "source": {"pdf": "Alexander_Guthrie - Five Generations.pdf", "page": 1},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
})

ENTRIES.append({
    "code": "A37",
    "name": "Bruce S. Romesburg",
    "sex": "M",
    "born": "20 May 1875",
    "died": "4 Dec 1957",
    "source": {"pdf": "Alexander_Guthrie - Five Generations.pdf", "page": 1},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
})

ENTRIES.append({
    "code": "A38",
    "name": "Mary Alice Romesburg",
    "sex": "F",
    "born": "29 Aug 1876",
    "died": "23 Jan 1971",
    "source": {"pdf": "Alexander_Guthrie - Five Generations.pdf", "page": 1},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
})

ENTRIES.append({
    "code": "A39",
    "name": "Charles K. Romesburg",
    "sex": "M",
    "born": "12 Jun 1882",
    "died": "15 Dec 1962",
    "source": {"pdf": "Alexander_Guthrie - Five Generations.pdf", "page": 1},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
})

ENTRIES.append({
    "code": "A3A",
    "name": "Persis Ann Romesburg",
    "sex": "F",
    "born": "23 Apr 1885",
    "died": "18 Mar 1977",
    "source": {"pdf": "Alexander_Guthrie - Five Generations.pdf", "page": 1},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
})

ENTRIES.append({
    "code": "A3C",
    "name": "Robert P. Romesburg",
    "sex": "M",
    "born": "9 Feb 1888",
    "died": "2 Jul 1953",
    "source": {"pdf": "Alexander_Guthrie - Five Generations.pdf", "page": 1},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
})




ENTRIES.append({
    "code": "A413",
    "name": "Edna Frankhouser",
    "sex": "F",
    "born": "16 Jan 1900",
    "died": "30 Nov 1983",
    "spouses": [
        {"name": "John Springer Clark", "order": 1},
        {"name": "Dennis Hurley", "order": 2},
    ],
    "source": {"pdf": "Alexander_Guthrie - Five Generations.pdf", "page": 6},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "A4131", "name": "John Springer Clark, Jr.", "born": "22 Dec 1920"},
    ],
})

ENTRIES.append({
    "code": "A414",
    "name": "Henry Andrew Frankhouser",
    "sex": "M",
    "born": "1907",
    "died": "1970",
    "spouses": [{"name": "Cecelia Bonchosky", "born": "1905", "died": "1974"}],
    "source": {"pdf": "Alexander_Guthrie - Five Generations.pdf", "page": 6},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "A4141", "name": "Rita Frankhouser"},
    ],
})

ENTRIES.append({
    "code": "A415",
    "name": "Guy Frankhouser",
    "sex": "M",
    "born": "22 Apr 1911",
    "died": "30 May 1972",
    "spouses": [{"name": "Frances V. Pence", "born": "12 Nov 1913", "died": "17 Jul 1982"}],
    "source": {"pdf": "Alexander_Guthrie - Five Generations.pdf", "page": 6},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "A4151", "name": "Geraldine Lorraine Frankhouser", "born": "26 Apr 1933"},
        {"code": "A4152", "name": "Thomas Lee Frankhouser", "born": "6 Apr 1934"},
        {"code": "A4153", "name": "Lawrence Emmer Frankhouser", "born": "27 Jun 1938"},
        {"code": "A4154", "name": "Francis G. Frankhouser", "born": "22 Sep 1939"},
        {"code": "A4155", "name": "Donald D. Frankhouser", "born": "30 Jul 1942", "verified_terminal": True},
    ],
})


ENTRIES.append({
    "code": "A455",
    "name": "Robert Eugene Cupp",
    "sex": "M",
    "born": "31 Jan 1915",
    "spouses": [
        {"name": "Hazel Harned", "order": 1},
        {"name": "June (Herring) Hileman", "born": "3 Apr 1923", "married": "15 Oct 1950", "order": 2},
    ],
    "source": {"pdf": "Alexander_Guthrie - Five Generations.pdf", "page": 6},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "A4551", "name": "Ronald Eugene Cupp", "born": "8 Jun 1940"},
    ],
})


ENTRIES.append({
    "code": "AB2",
    "name": "Ruby Pearl Guthrie",
    "sex": "F",
    "born": "18 Jan 1893",
    "died": "18 Oct 1979",
    "spouses": [
        {"name": "Hosea Meyers", "born": "21 Sep 1892", "died": "7 Dec 1924", "order": 1},
        {"name": "Edwin Ross Evans", "born": "14 Jul 1879", "died": "13 Aug 1964", "order": 2},
    ],
    "source": {"pdf": "Alexander_Guthrie - Five Generations.pdf", "page": 4},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "AB21", "name": "Vesty D. Meyers"},
        {"code": "AB22", "name": "Massereen Evans"},
        {"code": "AB23", "name": "Wanda M. Evans"},
        {"code": "AB24", "name": "Stanley Regis Evans"},
        {"code": "AB25", "name": "Infant Son", "verified_terminal": True},
    ],
})


# === Cleanup pass: Alexander PDF entries that needed own full entries ===
ENTRIES.append({
    "code": "A213",
    "name": "Frank Clark Frazee",
    "sex": "M",
    "born": "4 Aug 1902",
    "died": "24 Jan 1979",
    "spouses": [{"name": "Dorothy Lenora Myers", "born": "2 Nov 1913", "married": "1940", "details": "dau of Walter & Fanny [Frazee] Myers"}],
    "source": {"pdf": "Alexander_Guthrie - Five Generations.pdf", "page": 4},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "A2131", "name": "Mary Louise Frazee", "born": "27 Apr 1941"},
    ],
})

ENTRIES.append({
    "code": "A227",
    "name": "Sarah Ellen Guthrie",
    "sex": "F",
    "born": "14 Jun 1916",
    "died": "23 Sep 1968",
    "spouses": [{"name": "Darwin Leo Fearer", "married": "8 Aug 1940"}],
    "source": {"pdf": "Alexander_Guthrie - Five Generations.pdf", "page": 5},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "A2271", "name": "Cindy Fearer", "verified_terminal": True},
        {"code": "A2272", "name": "Sue Fearer", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "A242",
    "name": "Martha Leona Miller",
    "sex": "F",
    "born": "29 Sep 1913",
    "spouses": [{"name": "Carl Hinebaugh", "married": "6 Jul 1942"}],
    "source": {"pdf": "Alexander_Guthrie - Five Generations.pdf", "page": 5},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "A2421", "name": "Carl A. Hinebaugh", "born": "5 Sep 1943", "verified_terminal": True},
        {"code": "A2422", "name": "Alice Elizabeth Hinebaugh", "born": "14 Sep 1944", "verified_terminal": True},
        {"code": "A2423", "name": "Son", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "A353",
    "name": "Mary Blanche Romesburg",
    "sex": "F",
    "born": "29 Feb 1904",
    "spouses": [{"name": "Nathan G. Wright", "married": "1924"}],
    "source": {"pdf": "Alexander_Guthrie - Five Generations.pdf", "page": 5},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "A3531", "name": "Walter Wright", "verified_terminal": True},
        {"code": "A3532", "name": "Herbert Wright", "verified_terminal": True},
        {"code": "A3533", "name": "Carol Wright", "verified_terminal": True},
        {"code": "A3534", "name": "Ralph Wright", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "A354",
    "name": "Millie A. Romesburg",
    "sex": "F",
    "born": "19 Feb 1906",
    "spouses": [{"name": "Alva Hamilton", "married": "1929"}],
    "source": {"pdf": "Alexander_Guthrie - Five Generations.pdf", "page": 5},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "A3541", "name": "Marvin Hamilton", "born": "29 May 1930", "verified_terminal": True},
        {"code": "A3542", "name": "Theodore Hamilton", "verified_terminal": True},
        {"code": "A3543", "name": "Joy Lee Hamilton", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "A355",
    "name": "Lucy May Romesburg",
    "sex": "F",
    "born": "9 Aug 1907",
    "spouses": [{"name": "Frank Gleason", "married": "1929"}],
    "source": {"pdf": "Alexander_Guthrie - Five Generations.pdf", "page": 5},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "A3551", "name": "Patricia Louise Gleason", "verified_terminal": True},
        {"code": "A3552", "name": "John P. Gleason", "verified_terminal": True},
        {"code": "A3553", "name": "Constance Gleason", "verified_terminal": True},
        {"code": "A3554", "name": "Ray Gleason", "born": "13 Apr 1945", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "A356",
    "name": "Myrtle P. Romesburg",
    "sex": "F",
    "born": "8 Apr 1912",
    "spouses": [{"name": "Darwin Gibson", "married": "1937"}],
    "source": {"pdf": "Alexander_Guthrie - Five Generations.pdf", "page": 5},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "A3561", "name": "Wanda Lou Gibson", "born": "Sep 1940", "verified_terminal": True},
        {"code": "A3562", "name": "Darwin Gibson, Jr.", "born": "1943", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "A357",
    "name": "Samuel M. Romesburg",
    "sex": "M",
    "born": "22 May 1917",
    "spouses": [{"name": "Helen Murey", "married": "1938"}],
    "source": {"pdf": "Alexander_Guthrie - Five Generations.pdf", "page": 6},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "A3571", "name": "Louis Martin Romesburg", "born": "1941", "verified_terminal": True},
    ],
})


# === Cleanup pass: gen 5 entries from James PDF pages 5-8 that needed own entries ===
ENTRIES.append({
    "code": "7171",
    "name": "James Blaine Frazee",
    "sex": "M",
    "born": "15 Oct 1911",
    "died": "5 Mar 1979",
    "spouses": [{"name": "Kathleen Nordeck", "died": "1973"}],
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 5},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
})

ENTRIES.append({
    "code": "7231",
    "name": "Howard Emerson Barnes",
    "sex": "M",
    "born": "2 Apr 1913",
    "spouses": [{"name": "Pauline Virginia Wilson", "born": "9 Feb 1915", "married": "25 Dec 1937", "details": "dau of Victor and Ida [Ditmore] Wilson"}],
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 8},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "72311", "name": "Bonnie Betty Barnes", "born": "9 Jul 1940"},
        {"code": "72312", "name": "Carolyn Virginia Barnes", "born": "23 May 1943"},
        {"code": "72313", "name": "Howard Wilson Barnes", "born": "23 Jul 1949"},
        {"code": "72314", "name": "Ruth Ida Barnes", "born": "30 Aug 1950"},
        {"code": "72315", "name": "David Lee Barnes", "born": "11 Jun 1955"},
    ],
})

ENTRIES.append({
    "code": "7233",
    "name": "James Quinter Barnes, Jr.",
    "sex": "M",
    "born": "23 Dec 1916",
    "died": "3 Jul 1969",
    "spouses": [{"name": "Elizabeth Carolyn Beeghly", "born": "22 May 1919", "married": "8 Aug 1942"}],
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 8},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "72331", "name": "Jack Lloyd Barnes", "born": "23 Feb 1953"},
        {"code": "72332", "name": "James Ronald Barnes", "born": "25 Aug 1955"},
        {"code": "72333", "name": "Nancy Carolyn Barnes", "born": "25 Apr 1957"},
    ],
})

ENTRIES.append({
    "code": "7234",
    "name": "Laura Cole Barnes",
    "sex": "F",
    "born": "16 Dec 1918",
    "died": "15 Nov 1977",
    "spouses": [{"name": "Ward Barnes Guthrie", "born": "29 Jul 1916", "died": "11 Jul 1982", "married": "29 Jun 1939"}],
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 8},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": "Husband is 11331 in John branch (SEE_REF); their children appear under both 7234x and 11331x codes"},
    "children": [
        {"code": "72341", "name": "Suzanne Kay Guthrie", "born": "2 Dec 1942", "verified_terminal": True},
        {"code": "72342", "name": "Samuel Fleming Guthrie", "born": "14 Feb 1945", "verified_terminal": True},
        {"code": "72343", "name": "Ward David Guthrie", "born": "17 Mar 1946", "verified_terminal": True},
        {"code": "72344", "name": "Stephen Byron Guthrie", "born": "25 Mar 1960", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "7251",
    "name": "Ralph Mosser Barnes",
    "sex": "M",
    "born": "17 Oct 1900",
    "died": "5 Nov 1984",
    "spouses": [{"name": "Mary Ward Goodykoontz", "born": "25 Oct 1904", "died": "12 Mar 1964", "married": "13 Jun 1931", "details": "m. (2) Aileen Barger Thompson, b. 13 Sep 1903"}],
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 8},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "72511", "name": "Elizabeth Carolyn Barnes", "born": "11 Sep 1932"},
        {"code": "72512", "name": "Carolyn Martha Barnes", "born": "10 Jun 1941"},
    ],
})

ENTRIES.append({
    "code": "7252",
    "name": "Edith Barnes",
    "sex": "F",
    "born": "10 Aug 1902",
    "died": "29 Oct 1996",
    "spouses": [{"name": "John Joseph Slavins", "born": "29 Aug 1898", "died": "18 Apr 1981", "married": "1 Sep 1926"}],
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 8},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "72521", "name": "William Edgar Slavins", "born": "6 Aug 1927"},
        {"code": "72522", "name": "Frances Ann Slavins", "born": "23 Oct 1933"},
    ],
})


# === James PDF pages 27-32 vision pass (2026-06-08): gen 7 grandchildren (Blankenship/Wotring/Dailey/Forman/Teets/Cuppett/Walls/Wolfe/Kisner/Reckart/Everly/Simpson/Thomas/Schutzendorf/Slavins/Robichaud) ===
ENTRIES.append({
    "code": "713111",
    "name": "Daphney Elaine Barbour",
    "sex": "F",
    "born": "6 Jun 1954",
    "spouses": [{"name": "Thomas Edward Blankenship", "married": "12 May 1973"}],
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 27},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": "Expanded from page 27"},
    "children": [
        {"code": "7131111", "name": "Erin Jennifer Blankenship", "born": "7 Dec 1975", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "714411",
    "name": "Roxanne Barnes",
    "sex": "F",
    "born": "1 Feb 1953",
    "spouses": [{"name": "Martin Dale (Bud) Wotring", "born": "18 Sep 1951", "married": "1 Apr 1972"}],
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 27},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": "Expanded from page 27"},
    "children": [
        {"code": "7144111", "name": "Gregory Martin Wotring", "born": "14 Aug 1972", "verified_terminal": True},
        {"code": "7144112", "name": "Matthew Lane Worting", "born": "29 Jan 1977", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "714422",
    "name": "Dana Vance Dailey",
    "sex": "M",
    "spouses": [{"name": "Sarah Naranjo"}],
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 27},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": "Expanded from page 27"},
    "children": [
        {"code": "7144221", "name": "Jesse Dailey", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "714423",
    "name": "Dale Vincent Dailey",
    "sex": "M",
    "spouses": [{"name": "Georgia Dickson"}],
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 27},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": "Expanded from page 27"},
    "children": [
        {"code": "7144231", "name": "Daniell Dailey", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "714511",
    "name": "Clinton L. Forman",
    "sex": "M",
    "spouses": [{"name": "Susan Kay Benson", "born": "26 May 1960", "married": "26 May 1979"}],
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 27},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": "Married at Marklesburg, PA Union Church"},
    "children": [
        {"code": "7145111", "name": "Timothy Forman", "born": "15 Feb 1980", "verified_terminal": True},
        {"code": "7145112", "name": "Tiffany Lynn Forman", "born": "8 Jun 1984", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "714512",
    "name": "Ronna June Forman",
    "sex": "F",
    "spouses": [{"name": "Rollin Eugene Teets", "born": "16 Jan 1951", "married": "10 Apr 1971"}],
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 27},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": "Expanded from page 27"},
    "children": [
        {"code": "7145121", "name": "Kristi Teets", "born": "Oct 1972", "verified_terminal": True},
        {"code": "7145122", "name": "Pamela Teets", "died": "14 Apr 1977", "verified_terminal": True},
        {"code": "7145123", "name": "Amy Teets", "born": "1978", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "714521",
    "name": "Clifford Cuppett",
    "sex": "M",
    "spouses": [{"name": "Linda Schnopp"}],
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 27},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": "Expanded from page 27"},
    "children": [
        {"code": "7145211", "name": "Carrie Lynn Cuppett", "born": "18 Oct 1988", "verified_terminal": True},
        {"code": "7145212", "name": "Jesse Cuppett", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "714523",
    "name": "Debra Sue Cuppett",
    "sex": "F",
    "born": "10 Aug 1951",
    "spouses": [{"name": "Orval Lee Walls", "born": "30 Jan 1953", "married": "14 Aug 1970"}],
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 27},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": "Married at Pisgah, WV"},
    "children": [
        {"code": "7145231", "name": "Robby Lee Walls", "born": "31 Jan 1974", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "714531",
    "name": "Roger Lee Wolfe Sr.",
    "sex": "M",
    "spouses": [{"name": "Wanda Fike"}],
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 27},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": "Expanded from page 27"},
    "children": [
        {"code": "7145311", "name": "Ronda Wolfe", "born": "1971", "verified_terminal": True},
        {"code": "7145312", "name": "Roger Lee Wolfe, Jr.", "born": "30 Aug 1974", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "714532",
    "name": "Stanley Wolfe",
    "sex": "M",
    "spouses": [{"name": "Joyce"}],
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 28},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": "Expanded from page 28"},
    "children": [
        {"code": "7145321", "name": "a son", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "714533",
    "name": "Edwin Wolfe",
    "sex": "M",
    "spouses": [{"name": "Debbie Lewis"}],
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 28},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": "Wife from Pisgah"},
    "children": [
        {"code": "7145331", "name": "Heidi Rae Wolfe", "born": "8 Jan 1974", "verified_terminal": True},
        {"code": "7145332", "name": "Renee Wolfe", "verified_terminal": True},
        {"code": "7145333", "name": "Bethany Ann Wolfe", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "714535",
    "name": "Duncan Eric Wolfe",
    "sex": "M",
    "born": "1964",
    "spouses": [{"name": "Roberta Metheny"}],
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 28},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": "Expanded from page 28"},
    "children": [
        {"code": "7145351", "name": "Heather Wolfe", "born": "Jul 1980", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "714541",
    "name": "Sherry Louise Everly",
    "sex": "F",
    "born": "29 May 1952",
    "spouses": [{"name": "Richard Kisner", "married": "19 Jun 1970"}],
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 28},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": "Born Uniontown, PA; married Oakland, MD"},
    "children": [
        {"code": "7145411", "name": "Jeffery Scott Kisner", "born": "14 Oct 1973", "verified_terminal": True},
        {"code": "7145412", "name": "Shane Richard Kisner", "born": "28 Nov 1976", "verified_terminal": True},
        {"code": "7145413", "name": "Angela Dawn Kisner", "born": "15 Mar 1979", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "714542",
    "name": "Karen Kay Everly",
    "sex": "F",
    "born": "26 Oct 1954",
    "spouses": [{"name": "Dallas Eugene Reckart Jr.", "born": "6 Mar 1951", "married": "27 Feb 1971"}],
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 28},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": "Divorced 1987"},
    "children": [
        {"code": "7145421", "name": "Karmon Kay Reckart", "born": "23 Oct 1973", "verified_terminal": True},
        {"code": "7145422", "name": "Brandon Eugene Reckart", "born": "25 Aug 1976", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "714543",
    "name": "James Spencer Everly",
    "sex": "M",
    "born": "30 May 1961",
    "spouses": [{"name": "Wendy Jo Evans", "born": "12 Nov 1961", "married": "14 Jul 1979"}],
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 28},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": "Married at Asher Glade, MD"},
    "children": [
        {"code": "7145431", "name": "Chastity Dawn Everly", "born": "21 Jan 1980", "verified_terminal": True},
        {"code": "7145432", "name": "Katie Jo Everly", "born": "17 Jul 1989", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "714553",
    "name": "Joy Lynn Wolfe",
    "sex": "F",
    "spouses": [{"name": "Randall Wensel (Randy) Simpson", "born": "11 Apr 1963"}],
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 28},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": "Expanded from page 28"},
    "children": [
        {"code": "7145531", "name": "Nathan Dwain Simpson", "born": "19 Dec 1989", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "714611",
    "name": "Jeffrey Ward Thomas",
    "sex": "M",
    "born": "5 Jan 1969",
    "spouses": [{"name": "Julia Wolfe", "married": "14 Jul 19"}],
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 28},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": "Expanded from page 28"},
    "children": [
        {"code": "7146111", "name": "Brandon Lowell Thomas", "born": "9 Jul 1995", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "725211",
    "name": "Patricia Sue Slavins",
    "sex": "F",
    "born": "28 Oct 1951",
    "spouses": [{"name": "Dudley Steven Schutzendorf", "born": "10 Sep 1949", "married": "30 Jun 1973"}],
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 29},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": "Expanded from page 29"},
    "children": [
        {"code": "7252111", "name": "Eric Von Schutzendorf", "born": "24 May 1978", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "725212",
    "name": "William Edgar Slavins, Jr.",
    "sex": "M",
    "born": "27 Jun 1954",
    "spouses": [{"name": "Laura Lee Robichaud", "born": "20 Aug 1954", "married": "26 Jun 1976"}],
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 29},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": "Expanded from page 29"},
    "children": [
        {"code": "7252121", "name": "Jessica Lee Slavins", "born": "15 Apr 1981", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "725111",
    "name": "Kathryn Diana Parks",
    "sex": "F",
    "born": "7 Jun 1960",
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 17},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
})

ENTRIES.append({
    "code": "725112",
    "name": "Matthew David Parks",
    "sex": "M",
    "born": "16 Oct 1963",
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 17},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
})

ENTRIES.append({
    "code": "725221",
    "name": "Jane Carolyn (Adams) Welch",
    "sex": "F",
    "born": "11 Jan 1959",
    "spouses": [{"name": "Samuel Cooper McMillan III", "born": "7 Mar 1957", "married": "24 Jul 1982"}],
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 17},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": "Adopted by Welch (stepfather)"},
})

ENTRIES.append({
    "code": "725222",
    "name": "Thomas Conley (Adams) Welch",
    "sex": "M",
    "born": "15 Feb 1960",
    "spouses": [{"name": "Nancy Gaye Vaughn", "born": "21 May 1960", "married": "14 Aug 1982"}],
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 17},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": "Adopted by Welch (stepfather)"},
})

ENTRIES.append({
    "code": "725223",
    "name": "Sally Ann Welch",
    "sex": "F",
    "born": "2 Feb 1969",
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 17},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
})

ENTRIES.append({
    "code": "72211",
    "name": "Robert Barnes Thornton",
    "sex": "M",
    "born": "25 Jul 1934",
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 8},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
})

ENTRIES.append({
    "code": "72212",
    "name": "David Campbell Thornton",
    "sex": "M",
    "born": "4 Mar 1939",
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 8},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
})

ENTRIES.append({
    "code": "72213",
    "name": "Gloria Margaret Thornton",
    "sex": "F",
    "born": "10 Dec 1941",
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 8},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
})

ENTRIES.append({
    "code": "72311",
    "name": "Bonnie Betty Barnes",
    "sex": "F",
    "born": "9 Jul 1940",
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 8},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
})

ENTRIES.append({
    "code": "72312",
    "name": "Carolyn Virginia Barnes",
    "sex": "F",
    "born": "23 May 1943",
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 8},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
})

ENTRIES.append({
    "code": "72313",
    "name": "Howard Wilson Barnes",
    "sex": "M",
    "born": "23 Jul 1949",
    "spouses": [{"name": "Darlene Elizabeth Lynch", "born": "4 Aug 1958", "married": "23 Apr 1983"}],
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 8},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
})

ENTRIES.append({
    "code": "72314",
    "name": "Ruth Ida Barnes",
    "sex": "F",
    "born": "30 Aug 1950",
    "spouses": [{"name": "Gordon C. Perry", "born": "11 Mar 1950", "married": "10 Jun 1972"}],
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 8},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
})

ENTRIES.append({
    "code": "72315",
    "name": "David Lee Barnes",
    "sex": "M",
    "born": "11 Jun 1955",
    "spouses": [{"name": "Joan Elizabeth Meserve", "born": "12 Jun 1955", "married": "21 Nov 1981"}],
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 8},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
})

ENTRIES.append({
    "code": "72331",
    "name": "Jack Lloyd Barnes",
    "sex": "M",
    "born": "23 Feb 1953",
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 8},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
})

ENTRIES.append({
    "code": "72332",
    "name": "James Ronald Barnes",
    "sex": "M",
    "born": "25 Aug 1955",
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 8},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
})

ENTRIES.append({
    "code": "72333",
    "name": "Nancy Carolyn Barnes",
    "sex": "F",
    "born": "25 Apr 1957",
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 8},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
})

ENTRIES.append({
    "code": "72351",
    "name": "Robert Paul Barnes, Jr.",
    "sex": "M",
    "born": "19 Feb 1948",
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 8},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
})

ENTRIES.append({
    "code": "72352",
    "name": "Linda Dianne Barnes",
    "sex": "F",
    "born": "11 Feb 1954",
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 8},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
})

ENTRIES.append({
    "code": "72353",
    "name": "Edward Monroe Barnes",
    "sex": "M",
    "born": "24 Mar 1957",
    "spouses": [{"name": "Sharon Weese", "born": "13 Jun 1956", "married": "11 Dec 1976"}],
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 8},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
})

ENTRIES.append({
    "code": "72354",
    "name": "Warren Leroy Barnes",
    "sex": "M",
    "born": "5 Apr 1960",
    "spouses": [{"name": "Terri Fowler", "born": "19 Mar 1960", "married": "16 Oct 1982"}],
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 8},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
})

ENTRIES.append({
    "code": "72511",
    "name": "Elizabeth Carolyn Barnes",
    "sex": "F",
    "born": "11 Sep 1932",
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 8},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
})

ENTRIES.append({
    "code": "72512",
    "name": "Carolyn Martha Barnes",
    "sex": "F",
    "born": "10 Jun 1941",
    "spouses": [{"name": "Robert Bruce Lemm", "born": "19 Jul 1941", "married": "18 Jul 1964"}],
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 8},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
})

ENTRIES.append({
    "code": "72521",
    "name": "William Edgar Slavins",
    "sex": "M",
    "born": "6 Aug 1927",
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 8},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
})

ENTRIES.append({
    "code": "72522",
    "name": "Frances Ann Slavins",
    "sex": "F",
    "born": "23 Oct 1933",
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 8},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
})


# === James PDF pages 1-5 vision pass (2026-06-08): Barnes/Guthrie gen 3-5 ===
ENTRIES.append({
    "code": "716",
    "name": "Dora Belle Barnes",
    "sex": "F",
    "born": "6 Aug 1880",
    "died": "4 Dec 1952",
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 1},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": "Lived with her sister Rosa in Hazelton, WV"},
})

ENTRIES.append({
    "code": "717",
    "name": "Pearlie Grace Barnes",
    "sex": "F",
    "born": "24 Apr 1886",
    "died": "21 Feb 1967",
    "spouses": [{"name": "Walter Frazee", "born": "29 May 1886", "died": "17 May 1925", "married": "30 Jun 1911"}],
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 2},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "7171", "name": "James Blaine Frazee", "born": "15 Oct 1911", "died": "5 Mar 1979"},
        {"code": "7172", "name": "Dorothy Frazee", "verified_terminal": True},
        {"code": "7173", "name": "Keith Ellsworth Frazee", "born": "25 Mar 1914", "died": "16 Apr 1993", "verified_terminal": True},
        {"code": "7174", "name": "Richard Frazee", "born": "22 Oct 1915", "died": "11 Oct 1989", "verified_terminal": True},
        {"code": "7175", "name": "Virginia Frazee", "verified_terminal": True},
        {"code": "7176", "name": "June Grace Frazee", "born": "10 Jun 1924", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "7131",
    "name": "Evelyn Virginia Barnes",
    "sex": "F",
    "born": "16 Dec 1904",
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 2},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
})

ENTRIES.append({
    "code": "7132",
    "name": "Mildren Grace Barnes",
    "sex": "F",
    "born": "14 Nov 1909",
    "died": "28 Dec 1922",
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 2},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
})

ENTRIES.append({
    "code": "7133",
    "name": "Mabel May Barnes",
    "sex": "F",
    "born": "23 Aug 1912",
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 2},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
})

ENTRIES.append({
    "code": "7141",
    "name": "Hugh Ercil Barnes",
    "sex": "M",
    "born": "5 Oct 1901",
    "died": "19 Nov 1990",
    "spouses": [{"name": "Marie Minerva White", "born": "25 Nov 1896", "died": "15 Feb 1990", "married": "29 Jun 1936"}],
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 2},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": "Wife dau of Thomas B. and Cora (Armstrong) White"},
})

ENTRIES.append({
    "code": "7142",
    "name": "Infant Barnes",
    "sex": "M",
    "born": "12 Aug 1903",
    "died": "12 Aug 1903",
    "flags": {"diedInInfancy": True},
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 2},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
})

ENTRIES.append({
    "code": "7143",
    "name": "Ethel Barnes",
    "sex": "F",
    "born": "26 Jul 1904",
    "died": "28 Apr 1982",
    "spouses": [{"name": "Dailey J. Kelly", "born": "2 Jul 1907", "died": "11 Feb 1980", "married": "22 Sep 19"}],
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 2},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
})

ENTRIES.append({
    "code": "7145",
    "name": "Ina Winifred Barnes",
    "sex": "F",
    "born": "13 Jan 1908",
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 2},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
})

ENTRIES.append({
    "code": "7146",
    "name": "Fleming Clark Barnes",
    "sex": "M",
    "born": "28 Nov 1912",
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 2},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
})

ENTRIES.append({
    "code": "721",
    "name": "Lillian Irene Barnes",
    "sex": "F",
    "born": "5 Jun 1869",
    "died": "30 Oct 1954",
    "spouses": [
        {"name": "Baltus DeWitt", "born": "1 Aug 1859", "died": "10 Sep 1900", "married": "17 Sep 1895", "order": 1},
        {"name": "George E. Wolfe", "born": "2 Jul 1863", "died": "13 Jun 1949", "married": "3 Jun 1918", "order": 2},
    ],
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 2},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "7211", "name": "Lillian DeWitt", "born": "20 Jun 1896", "died": "Jun 1900", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "722",
    "name": "Virginia Barbara Barnes",
    "sex": "F",
    "born": "12 Feb 1871",
    "died": "17 Apr 1946",
    "spouses": [{"name": "William H. Thornton", "born": "10 Dec 1864", "died": "22 Mar 1929", "married": "14 or 20 Jun 1898"}],
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 4},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "7221", "name": "Raymond Barnes Thornton", "born": "9 Oct 1900", "verified_terminal": True},
        {"code": "7222", "name": "Helen Lucille Thornton", "born": "28 Dec 1902", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "723",
    "name": "James Quinter Barnes",
    "sex": "M",
    "born": "7 May 1873",
    "died": "20 Sep 1956",
    "spouses": [{"name": "Laura Cole", "born": "16 Oct 1887", "died": "20 May 1971", "married": "26 Jun 1912"}],
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 4},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "7231", "name": "Howard Emerson Barnes", "born": "2 Apr 1913"},
        {"code": "7232", "name": "Genevieve Lillian Barnes", "born": "22 Sep 1914", "died": "15 Jun 1932", "verified_terminal": True},
        {"code": "7233", "name": "James Quinter Barnes, Jr.", "born": "23 Dec 1916"},
        {"code": "7234", "name": "Laura Cole Barnes", "born": "16 Dec 1918"},
        {"code": "7235", "name": "Robert Paul Barnes", "born": "3 Oct 1923", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "724",
    "name": "William H. Barnes",
    "sex": "M",
    "born": "2 May 1875",
    "died": "11 Apr 1948",
    "spouses": [{"name": "Ada M. Simpson", "born": "1872", "died": "1942", "married": "7 Feb 1940"}],
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 1},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": "Wife from Kansas"},
})

ENTRIES.append({
    "code": "725",
    "name": "John Jacob Barnes",
    "sex": "M",
    "born": "22 Oct 1877",
    "died": "30 Sep 1963",
    "spouses": [{"name": "Mattie Ann Mosser", "born": "2 Nov 1875", "died": "13 Nov 1962", "married": "25 Oct 1899"}],
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 4},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "7251", "name": "Ralph Mosser Barnes", "born": "17 Oct 1900"},
        {"code": "7252", "name": "Edith Barnes", "born": "10 Aug 1902"},
    ],
})

ENTRIES.append({
    "code": "726",
    "name": "Sara Alice Barnes",
    "sex": "F",
    "born": "23 Jan 1880",
    "died": "9 Nov 1948",
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 1},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
})

ENTRIES.append({
    "code": "74C",
    "name": "Infant son",
    "sex": "M",
    "born": "1 Jun 1902",
    "died": "1 Jun 1902",
    "flags": {"diedInInfancy": True},
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 1},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
})

ENTRIES.append({
    "code": "761",
    "name": "Cora Guthrie",
    "sex": "F",
    "born": "15 Jan 1883",
    "died": "17 Aug 1924",
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 2},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
})

ENTRIES.append({
    "code": "762",
    "name": "Alcinda Guthrie",
    "sex": "F",
    "born": "5 Aug 1884",
    "died": "23 Feb 1962",
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 2},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
})

ENTRIES.append({
    "code": "764",
    "name": "Hosea Guthrie",
    "sex": "M",
    "born": "19 Nov 1887",
    "died": "2 Sep 1954",
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 2},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
})

ENTRIES.append({
    "code": "766",
    "name": "Lester Guthrie",
    "sex": "M",
    "born": "8 Sep 1890",
    "died": "16 Apr 1974",
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 2},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
})

ENTRIES.append({
    "code": "767",
    "name": "Roy Guthrie",
    "sex": "M",
    "born": "15 Dec 1892",
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 2},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
})

ENTRIES.append({
    "code": "768",
    "name": "Grace Guthrie",
    "sex": "F",
    "born": "15 Dec 1892",
    "died": "14 Feb 1893",
    "flags": {"diedInInfancy": True},
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 2},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
})

ENTRIES.append({
    "code": "769",
    "name": "Walter Guthrie",
    "sex": "M",
    "born": "11 Jul 1895",
    "died": "1 Jul 1959",
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 2},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
})

ENTRIES.append({
    "code": "76A",
    "name": "Infant son",
    "sex": "M",
    "born": "11 Jul 1895",
    "died": "11 Jul 1895",
    "flags": {"diedInInfancy": True},
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 2},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
})

ENTRIES.append({
    "code": "7651",
    "name": "Ralph Ersel Spiker",
    "sex": "M",
    "born": "17 Jan 1910",
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 5},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": "Also coded 17131 (cross-branch via John 17)"},
})

ENTRIES.append({
    "code": "7656",
    "name": "Ruth Virginia Spiker",
    "sex": "F",
    "born": "23 Apr 1923",
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 5},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": "Also coded 17136 (cross-branch via John 17)"},
})

ENTRIES.append({
    "code": "7631",
    "name": "Robert Delmer Seese",
    "sex": "M",
    "born": "13 Sep 1909",
    "source": {"pdf": "James_Guthrie - Seven Generations.pdf", "page": 5},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": "Foster son"},
})


# === Pages 146-147 vision pass (2026-06-08): John gen 8 final — Fike/Chidester/Lawson/Wakefield/Bolyard/Burgess/Ryan/Krimpel/Rosenberger ===
ENTRIES.append({
    "code": "12332121",
    "name": "Sheryl Ann Fike",
    "sex": "F",
    "spouses": [{"name": "Randy Lee Parnell", "married": "6 Sep 1986"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 146},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "123321211", "name": "Child 1", "verified_terminal": True},
        {"code": "123321212", "name": "Child 2", "verified_terminal": True},
        {"code": "123321213", "name": "Child 3", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "12332162",
    "name": "Buffie Rae Fike",
    "sex": "F",
    "born": "1 Apr 1974",
    "spouses": [{"name": "Thomas Rosenberger"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 146},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "123321621", "name": "Tyler Lee Rosenberger", "born": "1993", "verified_terminal": True},
        {"code": "123321622", "name": "Whitney Ray Rosenberger", "born": "10 Sep 1944", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "12332311",
    "name": "Howard Duane Chidester",
    "sex": "M",
    "born": "9 May 1970",
    "spouses": [{"name": "Melanie Tasker"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 146},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "123323111", "name": "Bryanna Noel Chidester", "born": "22 Dec 1992", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "12332312",
    "name": "Brenda Lou Chidester",
    "sex": "F",
    "born": "5 Mar 1972",
    "spouses": [{"name": "Brian Gibson"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 146},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "123323121", "name": "Cody Ray Gibson", "born": "Mar 1993", "verified_terminal": True},
        {"code": "123323122", "name": "Lindsey Kay Gibson", "born": "10 Feb 1994", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "13261121",
    "name": "Amy Heather Lawson",
    "sex": "F",
    "born": "30 Jan 1970",
    "spouses": [{"name": "Rodney Allen Surratt", "married": "22 Jun 1991"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 146},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "132611211", "name": "Nicholas Blaine Surratt", "born": "3 Dec 1994", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "13261311",
    "name": "Lori Jean Wakefield",
    "sex": "F",
    "born": "5 Jun 1971",
    "spouses": [
        {"name": "Jimmie A. (Ben) Sisler", "born": "9 Sep 1966", "married": "24 Oct 1989", "order": 1},
        {"name": "Craig Turner", "married": "Aug 1994", "order": 2},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 146},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "132613111", "name": "Holly E. Sisler", "born": "31 May 1987", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "13261312",
    "name": "Amanda Fay Wakefield",
    "sex": "F",
    "born": "2 Nov 1972",
    "spouses": [{"name": "Jason Martin"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 146},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "132613121", "name": "Devon Lloyd Martin", "born": "12 Nov 1992", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "13651161",
    "name": "Randy Lee Bolyard",
    "sex": "M",
    "born": "23 Feb 1973",
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 146},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "136511611", "name": "Wade Lee Bolyard", "born": "17 May 1996", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "13651312",
    "name": "Grace Catherine Burgess",
    "sex": "F",
    "spouses": [{"name": "Ray"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 146},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "136513121", "name": "Child 1", "verified_terminal": True},
        {"code": "136513122", "name": "Child 2", "verified_terminal": True},
        {"code": "136513123", "name": "Child 3", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "13651313",
    "name": "Shirley Burgess",
    "sex": "F",
    "spouses": [{"name": "Phillip"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 147},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "136513131", "name": "Justin", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "13651411",
    "name": "Nancy Lynn Ryan",
    "sex": "F",
    "born": "3 Jun 1965",
    "spouses": [{"name": "Jon Mark Lilly", "born": "9 Dec 1961", "married": "8 Apr 1984"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 147},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "136514111", "name": "Mary Beth Lilly", "born": "17 Oct 1984", "verified_terminal": True},
        {"code": "136514112", "name": "Megan Elizabeth Lilly", "born": "12 Jun 1988", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "13651412",
    "name": "Patricia Daeleen Ryan",
    "sex": "F",
    "born": "17 Feb 1970",
    "spouses": [{"name": "Timothy Miller"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 147},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "136514121", "name": "Simon Clay Miller", "born": "8 Jul 1994", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "13651711",
    "name": "William Eugene Krimpel",
    "sex": "M",
    "born": "10 Sep 1965",
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 147},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "136517111", "name": "Jessica Lynn Sheeks", "born": "18 Mar 1983", "verified_terminal": True},
        {"code": "136517112", "name": "Joseph William Smith", "born": "29 Aug 1983", "verified_terminal": True},
        {"code": "136517113", "name": "Heather Nicole Krimpel", "born": "29 Mar 1985", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "13651712",
    "name": "Robin Ann Krimpel",
    "sex": "F",
    "born": "13 Jan 1967",
    "spouses": [{"name": "Robert Lee Sheeks", "born": "31 Dec 1964", "married": "25 Jan 1985"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 147},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "136517121", "name": "Robert Lee Sheeks", "born": "26 Nov 1986", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "13651741",
    "name": "Michelle Lynn Krimpel",
    "sex": "F",
    "born": "17 Jun 1970",
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 147},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "136517411", "name": "Paul Edward", "born": "Sep 1985", "verified_terminal": True},
    ],
})


# === Pages 141-145 vision pass (2026-06-08): Swauger/Guthrie/Hixon/Russell/Seese/Wolfe/Rucinski/Ritchey/Shaffer/Early gen 7 ===
ENTRIES.append({
    "code": "1721113",
    "name": "Marylin Sue Swauger",
    "sex": "F",
    "born": "17 Apr 1955",
    "spouses": [
        {"name": "Terry Garlitz", "married": "29 Mar 1978", "order": 1},
        {"name": "Gary William Warnick", "born": "1 Sep 1955", "married": "24 Sep 1983", "order": 2},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 141},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "17211131", "name": "Todd William Garlitz", "born": "30 Dec 1978", "verified_terminal": True},
        {"code": "17211132", "name": "Jason Lee Garlitz", "born": "27 May 1980", "verified_terminal": True},
        {"code": "17211133", "name": "Jaclyn Warnick", "born": "19 May 1989", "verified_terminal": True},
        {"code": "17211134", "name": "Jessica Michelle Warnick", "born": "7 May 1991", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1721114",
    "name": "Delma Louise Swauger",
    "sex": "F",
    "born": "9 Dec 1957",
    "spouses": [
        {"name": "Louis Dean Savage", "married": "21 Aug 1976", "order": 1},
        {"name": "Roger B. Murray", "born": "18 Mar 1951", "married": "25 Feb 1984", "order": 2},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 141},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "17211141", "name": "Kelli Dawn Murray", "born": "7 Sep 1984", "verified_terminal": True},
        {"code": "17211142", "name": "Lori Ann Murray", "born": "17 Jul 1974", "verified_terminal": True},
        {"code": "17211143", "name": "Jodi Nicole Murray", "born": "29 Nov 1991", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1721121",
    "name": "Dale Eugene Guthrie",
    "sex": "M",
    "born": "11 Nov 1963",
    "spouses": [
        {"name": "Jewell Kaye Adkins", "order": 1},
        {"name": "Ronda Femi", "order": 2},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 141},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": "Kerry is Ronda's son by previous marriage"},
    "children": [
        {"code": "17211211", "name": "Dale Eugene Guthrie, Jr.", "born": "13 Jun 1987", "verified_terminal": True},
        {"code": "17211212", "name": "Brittany Guthrie", "born": "14 Oct 1988", "verified_terminal": True},
        {"code": "17211213", "name": "Kerry", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1721122",
    "name": "Cheryl Ann Guthrie",
    "sex": "F",
    "born": "19 Nov 1964",
    "spouses": [{"name": "Jeffery Darren Emmart", "born": "12 Aug 1963", "married": "4 Oct 1982"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 141},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "17211221", "name": "Jessica Ann Emmart", "born": "13 Mar 1983", "verified_terminal": True},
        {"code": "17211222", "name": "Crystal Lynn Emmart", "born": "11 Jun 1984", "verified_terminal": True},
        {"code": "17211223", "name": "Nicolas Robert Emmart", "born": "4 Jan 1995", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1721151",
    "name": "Peggy Marie Hixon",
    "sex": "F",
    "born": "10 Jul 1955",
    "spouses": [
        {"name": "Rex Allen Galloway", "married": "11 May 1974", "order": 1},
        {"name": "Larry Blosser", "order": 2},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 141},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": "First marriage in Shady Grove Church"},
    "children": [
        {"code": "17211511", "name": "Heather Lynn Galloway", "born": "25 Sep 1974", "verified_terminal": True},
        {"code": "17211512", "name": "Hollye Marie Galloway", "born": "25 Mar 1977", "verified_terminal": True},
        {"code": "17211513", "name": "Kristen Richelle Blosser", "born": "10 Jul 1984", "verified_terminal": True},
        {"code": "17211514", "name": "Matthew Ray Blosser", "born": "30 Jul 1987", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1721156",
    "name": "Jeffrey Lynn Hixon",
    "sex": "M",
    "born": "6 Oct 1966",
    "spouses": [{"name": "Deborah Dawn Friend", "born": "14 Nov 1968", "married": "4 Sep 1986"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 141},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": "Married in Oakland, MD"},
    "children": [
        {"code": "17211561", "name": "Heidi Dawn Hixon", "born": "4 Mar 1987", "verified_terminal": True},
        {"code": "17211562", "name": "Joshua Blaine Hixon", "born": "7 Oct 1991", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1721162",
    "name": "Tina Marie Guthrie",
    "sex": "F",
    "born": "5 Dec 1968",
    "spouses": [{"name": "Brian"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 141},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "17211621", "name": "Trevor", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1721163",
    "name": "Amy Sue Guthrie",
    "sex": "F",
    "born": "27 Dec 1969",
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 141},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "17211631", "name": "Randi Guthrie", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1721182",
    "name": "Gary DeWayne Russell",
    "sex": "M",
    "born": "28 Oct 1961",
    "died": "6 May 1993",
    "spouses": [{"name": "Debra Ann Hyde", "married": "Jul 1981"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 142},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "17211821", "name": "Jamie Lee Russell", "born": "22 Nov 1981", "verified_terminal": True},
        {"code": "17211822", "name": "Shane Russell", "born": "8 Jun 1983", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1721211",
    "name": "Anita Ann Seese",
    "sex": "F",
    "born": "15 Aug 1957",
    "spouses": [{"name": "Jimmy Roger Clark", "born": "30 Jun 1963", "married": "4 Oct 1975"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 142},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "17212111", "name": "Chad Eric Clark", "born": "11 Apr 1976", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1721212",
    "name": "Kevin Luke Seese",
    "sex": "M",
    "born": "31 Jan 1959",
    "spouses": [{"name": "Brenda Sue Feather", "married": "15 Nov 1980"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 142},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": "Married in Shady Grove Church"},
    "children": [
        {"code": "17212121", "name": "Casey Marie Seese", "born": "18 Mar 1987", "verified_terminal": True},
        {"code": "17212122", "name": "Carla Renee Seese", "born": "10 Jul 1990", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1721221",
    "name": "Cindy Diane Wolfe",
    "sex": "F",
    "born": "23 Nov 1953",
    "spouses": [{"name": "Michael Lee Wilson", "born": "6 Dec 1954", "married": "3 Mar 1975"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 142},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "17212211", "name": "Rebecca Marie Wolfe", "born": "29 Apr 1974", "died": "29 Apr 1974", "verified_terminal": True},
        {"code": "17212212", "name": "Michael Curtis Wilson", "born": "29 Nov 1975", "verified_terminal": True},
        {"code": "17212213", "name": "Jeremy Lee Wilson", "born": "13 Mar 1977", "verified_terminal": True},
        {"code": "17212214", "name": "Julie Marie Wilson", "born": "1 Jul 1980", "died": "10 Aug 1980", "verified_terminal": True},
        {"code": "17212215", "name": "Andrew Scott Wilson", "born": "10 Jun 1981", "verified_terminal": True},
        {"code": "17212216", "name": "Sally Anne Wilson", "born": "17 Jun 1982", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1721224",
    "name": "Daniel Thurman Wolfe",
    "sex": "M",
    "born": "8 Jan 1965",
    "spouses": [{"name": "Amy Sue Bates", "born": "20 Oct 1972", "married": "29 May 1993"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 142},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "17212241", "name": "Daniel (Aaron) Wolfe", "born": "19 Mar 1993", "verified_terminal": True},
        {"code": "17212242", "name": "Amanda Kathleen Wolfe", "born": "14 Feb 1995", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1721251",
    "name": "David Shawn Seese",
    "sex": "M",
    "born": "16 Nov 1973",
    "spouses": [{"name": "Julia Mae Durschlag", "born": "5 Feb 1976", "married": "1994"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 142},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "17212511", "name": "Zachary David Seese", "born": "22 Sep 1994", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1721311",
    "name": "Faye Diana Rucinski",
    "sex": "F",
    "born": "29 Apr 1960",
    "spouses": [{"name": "Gary Richards", "born": "1 Jul 1949", "married": "8 Feb 1992"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 142},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "17213111", "name": "Janice Richards", "born": "18 Jan 1994", "verified_terminal": True},
        {"code": "17213112", "name": "Paul Richards", "born": "18 Oct 1994", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1721322",
    "name": "Rodney Wayne Ritchey",
    "sex": "M",
    "born": "27 Dec 1959",
    "spouses": [{"name": "Regina Lea Hurst", "born": "8 May 1968", "married": "6 Jun 1987"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 142},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "17213221", "name": "Joseph Alan Ritchey", "born": "8 Jul 1988", "verified_terminal": True},
        {"code": "17213222", "name": "Julia Mae Ritchey", "born": "10 Oct 1992", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1721351",
    "name": "Sherri Lee Ritchey",
    "sex": "F",
    "born": "28 Mar 1965",
    "spouses": [{"name": "Martin Dean Jones", "married": "20 Jun 1987"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 142},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "17213511", "name": "Tori Jones", "born": "18 May 1994", "verified_terminal": True},
        {"code": "17213512", "name": "Bandi Jones", "born": "24 Sep 1995", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1721361",
    "name": "Michael Dale Ritchey",
    "sex": "M",
    "born": "16 Sep 1968",
    "spouses": [{"name": "Melody Warrington"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 143},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "17213611", "name": "Scott Ritchey", "born": "9 Jan 1989", "verified_terminal": True},
        {"code": "17213612", "name": "Taylor Ritchey", "born": "30 Mar 1993", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1733211",
    "name": "Arnold Lee Shaffer",
    "sex": "M",
    "born": "27 Mar 1951",
    "spouses": [{"name": "Roxann Marie Palabchalk", "born": "9 Jun 1954", "married": "20 Oct 1979"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 144},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "17332111", "name": "Travis Benjamin Shaffer", "born": "16 Apr 1983", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1733221",
    "name": "Kenneth Paul Early",
    "sex": "M",
    "born": "17 Jun 1949",
    "spouses": [{"name": "Cindy"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 144},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "17332211", "name": "Maria Early", "born": "23 Jan 1981", "verified_terminal": True},
        {"code": "17332212", "name": "Brandon Early", "born": "26 Jan 1983", "verified_terminal": True},
        {"code": "17332213", "name": "Lorrine Elizabeth Early", "born": "10 Feb 1986", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1733222",
    "name": "Linda Diane Early",
    "sex": "F",
    "born": "8 Apr 1951",
    "spouses": [{"name": "Paul Edward Rosenberger", "married": "6 Sep 1969"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 145},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "17332221", "name": "Paula Diane Rosenberger", "born": "13 Nov 1970", "verified_terminal": True},
        {"code": "17332222", "name": "Chastity Dawn Rosenberger", "born": "5 Sep 1974", "verified_terminal": True},
        {"code": "17332223", "name": "Chad Edward Rosenberger", "born": "5 Sep 1974", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1733231",
    "name": "Gregory Ray Shaffer",
    "sex": "M",
    "born": "30 Jul 1955",
    "spouses": [{"name": "Barbara Georsomer", "married": "9 Oct 1976"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 145},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "17332311", "name": "Gregory Shaffer", "born": "7 Jun 1981", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1733232",
    "name": "James Edward Shaffer",
    "sex": "M",
    "born": "13 Mar 1957",
    "spouses": [{"name": "Vicky Shepherd", "married": "12 Jun 1976"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 145},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "17332321", "name": "Dawn Shaffer", "born": "10 May 1977", "verified_terminal": True},
        {"code": "17332322", "name": "James Shaffer", "born": "18 Nov 1981", "verified_terminal": True},
        {"code": "17332323", "name": "Jennifer Shaffer", "born": "5 Jun 1983", "verified_terminal": True},
        {"code": "17332324", "name": "Robert Shaffer", "born": "11 Dec 1985", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1733233",
    "name": "Robert Floyd Shaffer",
    "sex": "M",
    "born": "11 Sep 1960",
    "spouses": [{"name": "Lisa Calvert", "married": "16 Aug 1980"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 145},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "17332331", "name": "Crystal Shaffer", "born": "14 Apr 1982", "verified_terminal": True},
        {"code": "17332332", "name": "Erin Shaffer", "born": "12 Jun 1985", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1733234",
    "name": "Twyla Jean Shaffer",
    "sex": "F",
    "born": "13 Mar 1962",
    "spouses": [{"name": "Timothy White", "married": "24 Apr 1981"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 145},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "17332341", "name": "Christopher White", "born": "13 Oct 1982", "verified_terminal": True},
    ],
})


# === Pages 136-140 vision pass (2026-06-08): Narivanchik/Spiker/Groves/Strawser/Appleby/Wolfe/Gregory/Buchanan/Spear/Weaver/Moyers/Smith/Thomas/Lewis/DeBerry/Shea/Mosher/Swauger gen 7 ===
ENTRIES.append({
    "code": "1443111",
    "name": "Theodore Ralph Narivanchik",
    "sex": "M",
    "born": "7 Sep 1949",
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 136},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": "Also coded 164111 (cross-branch)"},
    "children": [
        {"code": "14431111", "name": "Sabrina Louise Narivanchik", "born": "6 Sep 1971", "verified_terminal": True},
        {"code": "14431112", "name": "Theodore (Teddy) Ralph Narivanchik, Jr.", "born": "4 Apr 1973", "verified_terminal": True},
        {"code": "14431113", "name": "William (Billy) Ralph Narivanchik", "born": "30 Jul 1979", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1443112",
    "name": "Paul Joseph Narivanchik",
    "sex": "M",
    "born": "14 Sep 1954",
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 136},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": "Also coded 164112; listed children are step-children"},
    "children": [
        {"code": "14431121", "name": "Kara Elizabeth Sonntag", "born": "2 Jul 1962", "verified_terminal": True},
        {"code": "14431122", "name": "Alicia Marie Sonntag", "born": "1 Jul 1963", "verified_terminal": True},
        {"code": "14431123", "name": "Adam Edward Sonntag", "born": "4 Aug 1970", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1443113",
    "name": "Linda Mae Narivanchik",
    "sex": "F",
    "born": "2 Jan 1957",
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 136},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": "Also coded 164113"},
    "children": [
        {"code": "14431131", "name": "Robert Joseph Yingling III", "born": "28 May 1976", "verified_terminal": True},
        {"code": "14431132", "name": "Kimberlie Mae Edwards", "born": "13 Feb 1979", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1445311",
    "name": "Steven Lee Spiker",
    "sex": "M",
    "born": "6 May 1961",
    "spouses": [{"name": "Sheryl Ann LaMarche", "born": "13 Sep 1959", "married": "2 Feb 1980"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 136},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": "Also coded 1711211"},
    "children": [
        {"code": "14453111", "name": "Nicholas Ray Spiker", "born": "9 Aug 1980", "verified_terminal": True},
        {"code": "14453112", "name": "Jennifer Alynn Spiker", "born": "8 Jul 1983", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1445312",
    "name": "Randy Dale Spiker",
    "sex": "M",
    "born": "25 Jul 1968",
    "spouses": [{"name": "Tammy Sue Wolfe", "born": "24 Aug 1968", "married": "5 Aug 1988"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 136},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": "Also coded 1711212"},
    "children": [
        {"code": "14453121", "name": "Ryan Dale Spiker", "born": "23 Feb 1990", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1445411",
    "name": "Greg Paul Groves",
    "sex": "M",
    "born": "26 Jun 1960",
    "spouses": [{"name": "Debra Jean Groves", "married": "20 Mar 1981"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 136},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "14454111", "name": "Sheresha Marie Groves", "born": "1 Oct 1981", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1445413",
    "name": "Crystal Dawn Groves",
    "sex": "F",
    "born": "20 Feb 1967",
    "spouses": [{"name": "Timothy Allan Monroe", "married": "8 Aug 1985"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 136},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "14454131", "name": "Joshua Charles Monroe", "born": "25 Sep 1992", "verified_terminal": True},
        {"code": "14454132", "name": "Seth Allan Monroe", "born": "5 Jun 1994", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1448231",
    "name": "Chandel Strawser",
    "sex": "F",
    "spouses": [{"name": "Larry Hawley"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 136},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "11182311", "name": "Kayla Hawley", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1475111",
    "name": "Donna Rae Appleby",
    "sex": "F",
    "born": "17 Oct 1957",
    "spouses": [{"name": "Kenneth Grayson Wotring", "born": "5 Sep 1957", "married": "10 Jul 1976"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 136},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "14751111", "name": "Timothy Grayson Wotring", "born": "2 Feb 1977", "verified_terminal": True},
        {"code": "14751112", "name": "Jennifer Lynn Wotring", "born": "12 Feb 1981", "verified_terminal": True},
        {"code": "14751113", "name": "Tiffany Rae Wotring", "born": "13 Jan 1983", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1475112",
    "name": "Kathy Marie Appleby",
    "sex": "F",
    "born": "2 Jul 1959",
    "spouses": [{"name": "William Spindler", "born": "26 Mar 1957", "married": "8 Jul 1978"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 136},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "14751121", "name": "Ashley Marie Spindler", "born": "23 Sep 1984", "verified_terminal": True},
        {"code": "14751122", "name": "Nicole Elizabeth Spindler", "born": "31 Jul 1994", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1475122",
    "name": "Terri Lynn Appleby",
    "sex": "F",
    "born": "2 Jun 1960",
    "spouses": [{"name": "William Bloom", "married": "4 Feb 1980"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 137},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "14751221", "name": "Amy Jo Bloom", "born": "23 Nov 1971", "verified_terminal": True},
        {"code": "14751222", "name": "Chad Allen Bloom", "born": "17 Dec 1986", "verified_terminal": True},
        {"code": "14751223", "name": "Curtis Edward Bloom", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1475131",
    "name": "Linda Carol Wolfe",
    "sex": "F",
    "born": "23 Jun 1957",
    "spouses": [
        {"name": "Keith Cuppett", "born": "27 Oct 1955", "died": "4 Jun 1990", "married": "16 Aug 1975", "order": 1},
        {"name": "Howard Lewis", "order": 2},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 137},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "14751311", "name": "Brian Keith Cuppett", "born": "11 Mar 1976", "verified_terminal": True},
        {"code": "14751312", "name": "Chad Emerson Cuppett", "born": "2 Apr 1981", "verified_terminal": True},
        {"code": "14751313", "name": "Amy Renee Cuppett", "born": "26 Jan 1985", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1475132",
    "name": "Shelda Lee Wolfe",
    "sex": "F",
    "born": "26 May 1961",
    "spouses": [{"name": "Dana Glenn Wotring", "born": "5 Jul 1979", "married": "21 Jul 1979"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 137},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "14751321", "name": "Holly Ann Wotring", "born": "2 Jan 1980", "verified_terminal": True},
        {"code": "14751322", "name": "Megan Lee Wotring", "born": "16 Jun 1983", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1475133",
    "name": "Sheila Lynn Wolfe",
    "sex": "F",
    "born": "26 May 1961",
    "spouses": [
        {"name": "Michael Glenn Gibson", "born": "13 Feb 1960", "married": "19 Apr 1980", "order": 1},
        {"name": "Roger Griffin", "order": 2},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 137},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "14751331", "name": "Christi Lynn Gibson", "born": "16 Aug 1986", "verified_terminal": True},
        {"code": "14751332", "name": "Chelsea Mikel Gibson", "born": "24 Aug 1989", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1475134",
    "name": "Charles Roy (Chuck) Wolfe",
    "sex": "M",
    "born": "27 Apr 1970",
    "spouses": [{"name": "Kellie Friend"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 137},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "14751341", "name": "Wyatt Christopher Wolfe", "born": "21 Feb 1995", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1475142",
    "name": "Deborah Ann Gregory",
    "sex": "F",
    "born": "24 Apr 1960",
    "spouses": [{"name": "Gregg Kinkaid", "married": "28 Aug 1982"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 137},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "14751421", "name": "Alexis Kinkaid", "born": "28 Aug 1982", "verified_terminal": True},
        {"code": "14751422", "name": "Ashley Kinkaid", "born": "11 Jan 1984", "verified_terminal": True},
        {"code": "14751423", "name": "Nicole Kinkaid", "born": "29 Oct 1986", "verified_terminal": True},
        {"code": "14751424", "name": "Christopher Kinkaid", "born": "27 Jan 1988", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1475143",
    "name": "Barbara Ann Gregory",
    "sex": "F",
    "born": "4 Apr 1962",
    "spouses": [{"name": "Jeff Parobek", "married": "20 Jul 1986"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 137},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "14751431", "name": "Stephen Gregory Parobek", "born": "20 Dec 1989", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1611211",
    "name": "Anne Allison Buchanan",
    "sex": "F",
    "born": "2 May 1960",
    "spouses": [{"name": "Henry Theodore (Ted) Inman", "born": "1955"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 137},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "116112111", "name": "Henry Theodore Inmam IV", "born": "1990", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1611213",
    "name": "James Grant Buchanan",
    "sex": "M",
    "born": "12 Sep 1964",
    "spouses": [{"name": "Kristen Tagg"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 137},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "16112131", "name": "Kelsey Anne Buchanan", "born": "1991", "verified_terminal": True},
        {"code": "16112132", "name": "Lindsey Ruth Buchanan", "born": "1993", "verified_terminal": True},
        {"code": "16112133", "name": "Jesse Grant Buchanan", "born": "1995", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1611214",
    "name": "Jill Luise Buchanan",
    "sex": "F",
    "born": "27 Mar 1966",
    "spouses": [
        {"name": "David Roy Sinclair", "order": 1},
        {"name": "Tom Bunn", "born": "1965", "order": 2},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 138},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "16112141", "name": "Brittany Luise Sinclair", "born": "1984", "verified_terminal": True},
        {"code": "16112142", "name": "Allison Elizabeth Bunn", "born": "1996", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1623111",
    "name": "Mark Spear",
    "sex": "M",
    "born": "28 Feb",
    "spouses": [{"name": "Bobbie Jean Mattericci", "married": "1988"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 138},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "16231111", "name": "Daughter", "verified_terminal": True},
        {"code": "16231112", "name": "Emily Marie Spear", "born": "15 Dec 1994", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1631121",
    "name": "Robert Kyle Weaver",
    "sex": "M",
    "born": "20 Aug 1951",
    "spouses": [{"name": "Joyce Campasini", "born": "16 Aug 1951", "married": "16 Oct 1971"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 138},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "16311211", "name": "Bryan Weaver", "born": "13 Sep 1977", "verified_terminal": True},
        {"code": "16311212", "name": "Melissa Weaver", "born": "4 Jun 1980", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1631122",
    "name": "Thomas William Weaver",
    "sex": "M",
    "born": "6 Dec 1954",
    "spouses": [{"name": "Lorraine Petitimaire", "married": "6 Sep 1986"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 138},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "16311221", "name": "Justin Fellix Weaver", "born": "13 Oct 1987", "verified_terminal": True},
        {"code": "16311222", "name": "Jesse Charles Weaver", "born": "13 Oct 1987", "verified_terminal": True},
        {"code": "16311223", "name": "A son", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1631421",
    "name": "Richard Blaine Moyers",
    "sex": "M",
    "born": "24 Aug 1951",
    "spouses": [{"name": "Mary Lou Ditmore Parnell", "married": "23 Apr 1974"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 139},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": "Mary Lou is ex-wife of Charles Lloyd Parnell"},
    "children": [
        {"code": "16314211", "name": "Christine Lloyd Parnell", "born": "3 Mar 1970", "verified_terminal": True},
        {"code": "16314212", "name": "Richard Blaine Moyers, Jr.", "born": "1 Apr 1978", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1631422",
    "name": "Randy Wayne Moyers",
    "sex": "M",
    "born": "12 Nov 1952",
    "spouses": [
        {"name": "Gwendlyn Redeen Sheppard", "born": "31 Oct 1949", "married": "17 May 1975", "order": 1},
        {"name": "Sandra Lynn Wolfe", "order": 2},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 139},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "16314221", "name": "Aaron Troy Moyers", "born": "23 Jul 1977", "verified_terminal": True},
        {"code": "16314222", "name": "Derek Scott Moyers", "born": "19 Mar 1985", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1631423",
    "name": "Keith Alan Moyers",
    "sex": "M",
    "born": "29 Jul 1954",
    "spouses": [{"name": "Yvonne Larosa Moreland", "born": "12 Nov 1961", "married": "5 Apr 1980"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 139},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": "Married in Shady Grove Church"},
    "children": [
        {"code": "16314231", "name": "Dean Alan Moyers", "born": "25 Sep 1980", "verified_terminal": True},
        {"code": "16314232", "name": "Jeremy Colt Moyers", "born": "23 Sep 1982", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1631424",
    "name": "Darlene Louise Moyers",
    "sex": "F",
    "born": "24 Feb 1959",
    "spouses": [
        {"name": "Martin Edward Cupp", "born": "30 Dec 1953", "married": "7 Jul 1979", "order": 1},
        {"name": "Frank Soccorsi", "born": "30 Nov", "married": "4 Apr 1986", "order": 2},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 139},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": "Divorced from first husband"},
    "children": [
        {"code": "16314241", "name": "Tasha Nicole Soccorsi", "born": "7 Apr 1987", "verified_terminal": True},
        {"code": "16314242", "name": "Tali Jo Soccorsi", "born": "7 Nov 1991", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1631521",
    "name": "Julie Marie Smith",
    "sex": "F",
    "born": "15 Sep 1963",
    "spouses": [{"name": "John Walters", "married": "1 Aug 1981"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 139},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "16315211", "name": "Jarrett John Walters", "born": "28 Oct 1990", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1631711",
    "name": "Virginia (Ginger) Thomas",
    "sex": "F",
    "born": "18 Oct 1966",
    "spouses": [{"name": "Jon McCoy", "married": "21 May 1988"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 139},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "16317111", "name": "Joshua Lewis McCoy", "born": "27 Sep 1992", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1641111",
    "name": "Sabrina Louise Narivanchik",
    "sex": "F",
    "born": "6 Sep 1971",
    "spouses": [{"name": "Michael Edward Martin", "born": "19 Jan 1965", "married": "12 Feb 1993"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 139},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": "Also coded 14431111"},
    "children": [
        {"code": "16411111", "name": "Casey Cayenne Martin", "born": "16 Feb 1993", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1641112",
    "name": "Theodore (Teddy) Ralph Narivanchik, Jr.",
    "sex": "M",
    "born": "4 Apr 1973",
    "spouses": [{"name": "Catrina", "married": "31 Dec 1994"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 139},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": "Also coded 14431112; child by Jennifer"},
    "children": [
        {"code": "16411121", "name": "Ashley Renee Narivanchik", "born": "24 Feb 1993", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1662151",
    "name": "Rochelle Marie Lewis",
    "sex": "F",
    "born": "12 Nov 1977",
    "spouses": [{"name": "Eric Todd Bittinger", "born": "10 Nov 1970", "married": "10 Apr 1993"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 139},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "16621511", "name": "Eric Todd Bittinger, Jr.", "born": "13 Jul 1994", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1713312",
    "name": "Patricia Ann Summers",
    "sex": "F",
    "born": "13 Apr 1957",
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 140},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "17133121", "name": "Chad David Summers", "born": "23 Mar 1977", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1713411",
    "name": "Michael Nelson DeBerry",
    "sex": "M",
    "born": "25 Mar 1961",
    "spouses": [{"name": "Carol Ann Frederick", "born": "29 Apr 1962", "married": "29 Dec 1981"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 140},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": "Also coded 1224311 (cross-branch via DeBerry)"},
    "children": [
        {"code": "17134111", "name": "Jennifer Leanne DeBerry", "born": "21 Nov 1982", "verified_terminal": True},
        {"code": "17134112", "name": "Melissa Sue DeBerry", "born": "27 Feb 1987", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1713412",
    "name": "William Dale DeBerry",
    "sex": "M",
    "born": "6 Apr 1963",
    "spouses": [{"name": "Kelli Louise Hughs", "born": "13 Apr 1965", "married": "25 May 1985"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 140},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": "Also coded 1224312 (cross-branch via DeBerry)"},
    "children": [
        {"code": "17134121", "name": "William Dale DeBerry", "born": "14 Sep 1986", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1713511",
    "name": "Timothy Thomas Mosher",
    "sex": "M",
    "born": "14 Jul 1970",
    "spouses": [{"name": "Sue Ellen Foltz", "married": "20 Dec 1990"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 140},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "17135111", "name": "Timothy James Mosher", "born": "22 Aug 1991", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1721112",
    "name": "Betty Jo Swauger",
    "sex": "F",
    "born": "21 Jan 1954",
    "spouses": [{"name": "Randall (Randy) R. Wiley", "married": "3 Jun 1978"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 140},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "17211121", "name": "Jennifer Lynne Wiley", "born": "25 Mar 1980", "verified_terminal": True},
        {"code": "17211122", "name": "Wade Charles Wiley", "born": "12 Jul 1983", "verified_terminal": True},
        {"code": "17211123", "name": "Lauren Wiley", "born": "6 May 1986", "verified_terminal": True},
    ],
})


# === Pages 131-135 vision pass (2026-06-08): Shafer/Krimpel/Sisler/Sines/Seamon/Nicola/Collins/Kronk gen 8 ===
ENTRIES.append({
    "code": "1365141",
    "name": "Vivian Leah Shafer",
    "sex": "F",
    "born": "2 Nov 1946",
    "spouses": [{"name": "Kenneth Earl Ryan", "born": "10 Mar 1945", "married": "5 Sep 1964"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 131},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "13651411", "name": "Nancy Lynn Ryan", "born": "3 Jun 1965"},
        {"code": "13651412", "name": "Patricia Darleen Ryan", "born": "17 Feb 1970"},
        {"code": "13651413", "name": "Cindy Dawn Ryan", "born": "11 Jun 1973", "verified_terminal": True},
        {"code": "13651414", "name": "Katie Leah Ryan", "born": "29 Oct 1981", "verified_terminal": True},
        {"code": "13651415", "name": "Rebekah Jane Ryan", "born": "5 Jul 1983", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1365143",
    "name": "Hannah Darlene Shafer",
    "sex": "F",
    "born": "26 Jan 1953",
    "spouses": [{"name": "William Lynn Reese", "married": "1 Aug 1971"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 131},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "13651431", "name": "Sarah Elizabeth Reese", "born": "1 Jun 1973", "verified_terminal": True},
        {"code": "13651432", "name": "David Lee Reese", "born": "5 Apr 1975", "verified_terminal": True},
        {"code": "13651433", "name": "Rebekah Darlene Reese", "born": "9 Jul 1976", "verified_terminal": True},
        {"code": "13651434", "name": "Jeremy Edward Reese", "born": "2 Jul 1984", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1365151",
    "name": "Dallas Basil Shafer",
    "sex": "M",
    "born": "5 Mar 1951",
    "spouses": [{"name": "Anna", "married": "23 Aug 1968"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 131},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "13651511", "name": "Surena Sue Shafer", "born": "14 Jan 1970", "verified_terminal": True},
        {"code": "13651512", "name": "Dallas Basil Shafer, Jr.", "born": "15 Mar 1971", "verified_terminal": True},
        {"code": "13651513", "name": "Keith Scott Shafer", "born": "21 Oct 1972", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1365152",
    "name": "Anthony Thomas Shafer",
    "sex": "M",
    "born": "10 Mar 1952",
    "spouses": [{"name": "Sarah Everett", "born": "28 Jan 1954", "married": "5 Feb 1972"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 131},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "13651521", "name": "Dawn Machelle Shafer", "born": "26 Nov 1972", "verified_terminal": True},
        {"code": "13651522", "name": "Anthony Thomas Shafer II", "born": "1 Mar 1974", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1365153",
    "name": "Debra June Shafer",
    "sex": "F",
    "born": "4 Jan 1955",
    "spouses": [{"name": "Dennis Gibson", "married": "11 Jun 1972"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 131},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "13651531", "name": "Matthew Wayne Gibson", "born": "18 Sep 1974", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1365155",
    "name": "Dessie Carmellia Shafer",
    "sex": "F",
    "born": "10 Mar 1960",
    "spouses": [{"name": "Charles Mousdale", "married": "24 Dec 1981"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 131},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "13651551", "name": "Charles Mousdale, Jr.", "born": "11 Jun 1985", "verified_terminal": True},
        {"code": "13651552", "name": "William Charles Mousdale", "born": "Jan 1987", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1365156",
    "name": "Amelia Jane Shafer",
    "sex": "F",
    "born": "18 Mar 1961",
    "spouses": [{"name": "Robert Oldewurtel", "married": "20 Oct 1981"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 131},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "13651561", "name": "Frank Lewis Oldewurtel", "born": "4 May 1983", "verified_terminal": True},
        {"code": "13651562", "name": "Stephanie Jean Oldewurtel", "born": "2 Oct 1986", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1365161",
    "name": "Paula Jean Shafer",
    "sex": "F",
    "born": "4 Jun 1949",
    "spouses": [{"name": "Robert Eugene Buckanan", "born": "14 May 1946", "married": "7 Jul 1971"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 131},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "13651611", "name": "Robert Alexander Buckanan", "born": "12 Mar 1972", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1365162",
    "name": "George McKinley Shafer",
    "sex": "M",
    "born": "23 Jul 1954",
    "spouses": [
        {"name": "Windy Johnson", "married": "23 Jun 1973", "order": 1},
        {"name": "Karen Ann Sherbondy", "born": "12 Aug 1956", "married": "31 Dec 1979", "order": 2},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 131},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "13651621", "name": "Jeremy Ryan Shafer", "born": "16 Mar 1981", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1365171",
    "name": "Marshall William Eugene Krimpel",
    "sex": "M",
    "born": "25 Jul 1945",
    "spouses": [{"name": "Georgia Ellen Owens", "born": "11 Jul 1948", "married": "11 Jul 1964"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 132},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "13651711", "name": "William Eugene Krimpel", "born": "10 Sep 1965"},
        {"code": "13651712", "name": "Robin Ann Krimpel", "born": "13 Jan 1967"},
        {"code": "13651713", "name": "Donna Leigh Krimpel", "born": "14 Nov 1969", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1365173",
    "name": "Kenneth Lawrence Krimpel",
    "sex": "M",
    "born": "8 Aug 1949",
    "spouses": [{"name": "Mary Frances Castle", "born": "31 Mar 1951", "married": "13 Jun 1970"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 132},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "13651731", "name": "Dawn Marie Krimpel", "born": "10 Feb 1972", "verified_terminal": True},
        {"code": "13651732", "name": "Kerry Ann Krimpel", "born": "9 Oct 1974", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1365174",
    "name": "Robert McKinley Krimpel",
    "sex": "M",
    "born": "1 May 1951",
    "spouses": [
        {"name": "Teresa Burnley", "married": "25 Oct 1969", "order": 1},
        {"name": "Nancy Biddison", "born": "11 Aug 1956", "married": "3 Dec 1977", "order": 2},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 132},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "13651741", "name": "Michelle Lynn Krimpel", "born": "17 Jun 1970"},
    ],
})

ENTRIES.append({
    "code": "1365175",
    "name": "Lathan Carr Krimpel",
    "sex": "M",
    "born": "2 Aug 1952",
    "spouses": [{"name": "Penelope Candice Fitzgerald", "born": "9 Aug 1956", "married": "8 Dec 1979"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 132},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "13651751", "name": "Bryan Keith Krimpel", "born": "12 Oct 1980", "verified_terminal": True},
        {"code": "13651752", "name": "Bradley Michael Krimpel", "born": "12 Oct 1980", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1365177",
    "name": "Alice Mae Krimpel",
    "sex": "F",
    "born": "18 Nov 1956",
    "spouses": [{"name": "John Joseph Redmond", "married": "15 Dec 1973"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 132},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "13651771", "name": "Alice Marie Redmond", "born": "13 Nov 1974", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1365181",
    "name": "Randy Lee Casteel",
    "sex": "M",
    "born": "18 Sep 1956",
    "spouses": [{"name": "Candy Reckner"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 132},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "13651811", "name": "Anthony Allen Casteel", "born": "30 Dec 1982", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1365191",
    "name": "Roy Lee Sisler",
    "sex": "M",
    "born": "21 Oct 1948",
    "died": "22 Jul 1972",
    "spouses": [{"name": "Diane Lee Bowser", "born": "8 Apr 1952", "married": "20 Jan 1970"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 132},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "13651911", "name": "Wayne Lee Sisler", "born": "30 Oct 1970", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1365192",
    "name": "Richard David Sisler",
    "sex": "M",
    "born": "17 Oct 1949",
    "spouses": [{"name": "Shirley Loring Dumire", "born": "25 Aug 1953", "married": "23 Sep 1971"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 132},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "13651921", "name": "David Roy Sisler", "born": "26 Oct 1972", "verified_terminal": True},
        {"code": "13651922", "name": "Daniel Ray Sissler", "born": "25 Sep 1973", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1365193",
    "name": "Adra Ann Sisler",
    "sex": "F",
    "born": "2 Oct 1950",
    "spouses": [{"name": "Buddy Joe Lewis", "born": "25 Sep 1949", "married": "4 Sep 1971"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 132},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "13651931", "name": "April Joann Lewis", "born": "10 Apr 1972", "verified_terminal": True},
        {"code": "13651932", "name": "Scott Christian Lewis", "born": "10 Jan 1974", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1365194",
    "name": "Linda Lou Sisler",
    "sex": "F",
    "born": "13 Apr 1952",
    "spouses": [{"name": "Lawrence Wibler Michaels", "married": "5 Jul 1970"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 133},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "13651941", "name": "Karell Lawrence Michaels", "born": "10 Feb 1973", "verified_terminal": True},
        {"code": "13651942", "name": "Loren Stanley Michaels", "born": "30 Mar 1975", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1365196",
    "name": "Paul Edward Sisler",
    "sex": "M",
    "born": "2 Jul 1956",
    "spouses": [{"name": "Connie Sines", "born": "4 May 1955", "married": "4 Jun 1975"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 133},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "13651961", "name": "John Paul Sisler", "born": "9 Feb 1976", "verified_terminal": True},
        {"code": "13651962", "name": "Douglas Eugene Sisler", "born": "17 May 1978", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "13651A1",
    "name": "Dwight Hugh Shafer",
    "sex": "M",
    "born": "22 Oct 1956",
    "spouses": [{"name": "Audrey B. Chance", "born": "14 Nov 1955", "married": "2 Jul 1982"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 133},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "13651A11", "name": "James Edward Kalbaugh", "born": "27 Jul 1973", "verified_terminal": True},
        {"code": "13651A12", "name": "Michelle Ann Kalbaugh", "born": "24 Jul 1975", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "13651A2",
    "name": "Olaf Dwayne Shafer",
    "sex": "M",
    "born": "19 Sep 1957",
    "spouses": [{"name": "Sharon Kay Lawson", "born": "29 Jan 1958", "married": "31 Jul 1982"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 133},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "13651A21", "name": "Tamya Sue Mety", "born": "28 Aug 1973", "verified_terminal": True},
        {"code": "13651A22", "name": "Liberty Starr Mety", "born": "30 Jan 1976", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "13651A3",
    "name": "Donald Franklin Shafer",
    "sex": "M",
    "born": "11 Jan 1961",
    "spouses": [{"name": "Rebecca Ann Soltis", "born": "2 Jul 1959", "married": "31 Jul 1980"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 133},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "13651A31", "name": "Donald Franklin Shafer", "born": "18 Oct 1988", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "13651C1",
    "name": "Monika Crystal Shafer",
    "sex": "F",
    "born": "12 Mar 1960",
    "spouses": [{"name": "Michael Anthony Perez", "born": "22 Jan 1960", "married": "28 Jun 1980"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 133},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "13651C11", "name": "J. R. Anthony Perez", "born": "23 Apr 1980", "verified_terminal": True},
        {"code": "13651C12", "name": "Pebbles Alice Perez", "born": "30 Oct 1981", "verified_terminal": True},
        {"code": "13651C13", "name": "Joshua Michael Perez", "born": "10 May 1983", "verified_terminal": True},
        {"code": "13651C14", "name": "Brandi Marie Perez", "born": "5 Apr 1985", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "13651C2",
    "name": "Anita Marie Shafer",
    "sex": "F",
    "born": "5 Feb 1961",
    "spouses": [
        {"name": "Joseph Mark Treas", "married": "28 Jul 1980", "order": 1},
        {"name": "Brian Edward Butts", "married": "20 Sep 1986", "order": 2},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 133},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "13651C21", "name": "Tami Marie Treas", "born": "4 Apr 1981", "verified_terminal": True},
        {"code": "13651C22", "name": "Jennifer Lynn Treas", "born": "4 Apr 1982", "verified_terminal": True},
        {"code": "13651C23", "name": "Brian Edward Butts, Jr.", "born": "Aug", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "13651C3",
    "name": "Frank McKinley Shafer",
    "sex": "M",
    "born": "7 Oct 1962",
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 133},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "13651C31", "name": "Frank McKinley Shafer, Jr.", "born": "3 Apr 1985", "verified_terminal": True},
        {"code": "13651C32", "name": "Kimberly Shafer", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "13651C4",
    "name": "Allen Lee Shafer",
    "sex": "M",
    "born": "28 Mar",
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 134},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "13651C41", "name": "Kimberly Shafer", "verified_terminal": True},
        {"code": "13651C42", "name": "Crystal Shafer", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1382741",
    "name": "Jeffery Bruce Teets",
    "sex": "M",
    "born": "25 Jan 1975",
    "spouses": [{"name": "Melanie Jo Till", "born": "7 Nov 1973"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 134},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "13827411", "name": "Jessica Teets", "born": "3 Jun 1993", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "13B2112",
    "name": "William Ronald Sines",
    "sex": "M",
    "born": "26 Jul 1946",
    "spouses": [{"name": "Diane Jensen", "born": "8 Jun 1946", "married": "16 Jun 1972"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 134},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "13B21121", "name": "Rebecca Sines", "born": "4 May 1973", "verified_terminal": True},
        {"code": "13B21122", "name": "Matthew William Sines", "born": "25 Sep 1975", "verified_terminal": True},
        {"code": "13B21123", "name": "Linda Sines", "born": "May 1978", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "13B2113",
    "name": "Rita Lynn Sines",
    "sex": "F",
    "born": "10 Oct 1949",
    "spouses": [{"name": "Jay Melynchek", "married": "20 Feb 1970"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 134},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "13B21131", "name": "Jason Aaron Melynchek", "born": "10 Jan 1975", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "13B2115",
    "name": "Cathy Ann Sines",
    "sex": "F",
    "born": "22 Dec 1952",
    "spouses": [{"name": "Kenneth Fisch", "married": "7 Oct 1972"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 134},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "13B21151", "name": "Brian Fisch", "born": "27 Jul 1974", "verified_terminal": True},
        {"code": "13B21152", "name": "Christopher Fisch", "born": "4 Sep 1976", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "13B2133",
    "name": "Melva Susan Abbey",
    "sex": "F",
    "born": "26 Dec 1953",
    "spouses": [{"name": "Charles Ervin", "married": "2 Sep 1972"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 134},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "13B21331", "name": "Melissa Dawn Ervin", "born": "6 May 1974", "verified_terminal": True},
        {"code": "13B21332", "name": "Cora Robin Ervin", "born": "8 May 1976", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "13B2141",
    "name": "Gregory McMillian Seamon",
    "sex": "M",
    "born": "7 Jun 1955",
    "spouses": [{"name": "Debra"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 134},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "13B21411", "name": "Craig Allen Seamon", "born": "29 Sep 1974", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "13B2151",
    "name": "Edward Lee Seamon",
    "sex": "M",
    "born": "11 Jan 1960",
    "spouses": [{"name": "Aline Ali"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 134},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "13B21511", "name": "Catherine Seamon", "born": "10 Apr 1990", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "13B2154",
    "name": "Eric Donald Seamon",
    "sex": "M",
    "born": "10 Jul 1970",
    "spouses": [{"name": "Tera Hall"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 134},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "13B21541", "name": "Shame Seamon", "born": "20 Jul 1994", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "13C5112",
    "name": "Allen D. Smith",
    "sex": "M",
    "born": "19 Jun 1966",
    "spouses": [{"name": "Dawn Forte", "married": "10 Oct 1992"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 134},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "13C51121", "name": "Nicole Marie Smith", "born": "8 Oct 1995", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "13F7411",
    "name": "Angela Virginia Spreng",
    "sex": "F",
    "born": "22 Jun 1978",
    "spouses": [{"name": "Alexis Aponte", "born": "Jul 1978", "married": "10 Aug 1996"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 134},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "13F74111", "name": "E-Sid Alexis Aponte", "born": "3 Jan 1997", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1425231",
    "name": "Arveta Louise Nicola",
    "sex": "F",
    "born": "16 Sep 1953",
    "spouses": [{"name": "Floyd Elton Hammons", "born": "16 Oct 1950", "married": "28 Aug 1971"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 135},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "14252311", "name": "Amy Noel Hammons", "born": "23 Dec 1974", "verified_terminal": True},
        {"code": "14252312", "name": "Jillian Jean Hammons", "born": "12 Oct 1978", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1425232",
    "name": "Catherine Ann Nicola",
    "sex": "F",
    "born": "10 Dec 1954",
    "spouses": [{"name": "Richard Joseph Dudziak", "born": "10 Mar 1952", "married": "23 Feb 1973"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 135},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "14252321", "name": "Adam Lee Dudziak", "born": "4 Sep 1973", "verified_terminal": True},
        {"code": "14252322", "name": "Nathan James Dudziak", "born": "7 Aug 1975", "verified_terminal": True},
        {"code": "14252323", "name": "Joshua John Dudziak", "born": "26 May 1981", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1425233",
    "name": "Barbara Grace Nicola",
    "sex": "F",
    "born": "13 Oct 1956",
    "spouses": [
        {"name": "Michael Turner", "married": "10 Aug 1974", "order": 1},
        {"name": "David Lee Bauer", "married": "17 Mar 1979", "order": 2},
    ],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 135},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "14252331", "name": "Amanda Sue Bauer", "born": "17 Sep 1981", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1425234",
    "name": "Robert Eugene Nicola, Jr.",
    "sex": "M",
    "born": "29 Aug 1962",
    "spouses": [{"name": "Sheri Lynn", "born": "2 Nov", "married": "24 Apr 1981"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 135},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "14252341", "name": "Robert Theodore (Teddy) Nicola", "born": "20 Oct 1981", "verified_terminal": True},
        {"code": "14252342", "name": "Jonathan David Nicola", "born": "15 Mar 1988", "verified_terminal": True},
        {"code": "14252343", "name": "Holly Ann Nicola", "born": "28 Nov 1989", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1425241",
    "name": "Daniel (Danny) Whipkey",
    "sex": "M",
    "born": "31 Mar 1963",
    "spouses": [{"name": "Lydia Jean Riffle", "born": "17 May 1962", "married": "25 Jun 1988"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 135},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "14252411", "name": "Samantha Hope Whipkey", "born": "9 Oct 1991", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1425242",
    "name": "Tamra Lynn Whipkey",
    "sex": "F",
    "born": "9 Jan 1968",
    "spouses": [{"name": "Bradley Allan Gatian", "born": "17 Dec 1967", "married": "28 Dec 1988"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 135},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "14252421", "name": "Travis Cody Gatian", "born": "19 Oct 1985", "flags": {"adopted": True}, "verified_terminal": True},
        {"code": "14252422", "name": "Ashley Nicole Gatian", "born": "23 Nov 1989", "verified_terminal": True},
        {"code": "14252423", "name": "Christina Mariw Gatian", "born": "6 Sep 1996", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1434121",
    "name": "Ronald Lee Collins",
    "sex": "M",
    "born": "9 Aug 1959",
    "spouses": [{"name": "Mary Katherine Jenkins", "married": "2 Aug 1980"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 135},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "14341211", "name": "Eric Lee Collins", "verified_terminal": True},
        {"code": "14341212", "name": "Amber Dawn Collins", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1434131",
    "name": "Michael Ray Collins",
    "sex": "M",
    "born": "28 Aug 1963",
    "spouses": [{"name": "Kimberly Johnson", "married": "6 Nov 1985"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 135},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "14341311", "name": "Kaylie Dawn Collins", "born": "16 Dec 1988", "verified_terminal": True},
    ],
})

ENTRIES.append({
    "code": "1441541",
    "name": "Harold Emerson Kronk, Jr.",
    "sex": "M",
    "born": "4 May 1963",
    "spouses": [{"name": "Karen Denise Skabla", "born": "21 Jan 1966", "married": "28 Nov 1983"}],
    "source": {"pdf": "John_Guthrie - Eight Generations.pdf", "page": 135},
    "verification": {"status": "verified", "source": "vision", "lastChecked": "2026-06-08", "notes": None},
    "children": [
        {"code": "14415411", "name": "Jessica Elaine Kronk", "born": "4 Oct 1984", "verified_terminal": True},
        {"code": "14415412", "name": "Harold Paul Kronk", "born": "2 Mar 1986", "verified_terminal": True},
    ],
})


# === Drafts extracted from rachel.txt by draft_from_ocr.py ===


# === Drafts extracted from william.txt by draft_from_ocr.py ===



















# === Drafts extracted from absalom.txt by draft_from_ocr.py ===







# === Drafts extracted from stephen.txt by draft_from_ocr.py ===















# === Drafts extracted from alexander.txt by draft_from_ocr.py ===












































































# === Drafts extracted from james.txt by draft_from_ocr.py ===







































































































# === Drafts extracted from john.txt by draft_from_ocr.py ===
























































































































































































































































































































































