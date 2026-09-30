DISCLAIMER = (
    "⚠️ AI-generated result based on SAMPLE/static data for demonstration. It is not official. "
    "Verify all requirements against the latest official COMSATS University Islamabad admission policies (cuiislamabad.edu.pk)."
)

BACKGROUNDS = [
    "FSc Pre-Engineering",
    "FSc Pre-Medical",
    "ICS (Computer Science)",
    "I.Com / Commerce",
    "FA / Humanities",
    "A-Level",
    "DAE (Diploma)",
    "Other",
]

# SAMPLE general requirements – update as needed
GENERAL_REQUIREMENTS = [
    "Minimum 12 years of education (Intermediate/A-Level/equivalent); appearing students may apply conditionally.",
    "Valid CUI/NTS entry test score (sample: test weightage ~50%, Intermediate ~40%, Matric ~10% in merit).",
    "O/A-Level candidates need IBCC equivalence certificate.",
    "Documents: CNIC/B-Form, Matric & Intermediate results, domicile, photographs.",
    "Admission is merit-based and subject to seat availability and current CUI policy.",
]

_CS_BG = ["FSc Pre-Engineering", "ICS (Computer Science)", "A-Level"]
_ENG_BG = ["FSc Pre-Engineering", "A-Level"]

# SAMPLE program data – edit freely (name, field, backgrounds, subjects, min %, test, notes)
PROGRAMS = [
    {"name": "BS Computer Science", "field": "Computing", "backgrounds": _CS_BG,
     "subjects": "Mathematics required", "min_matric": 60, "min_inter": 60, "min_test": 50,
     "notes": "Pre-Medical students may need deficiency Mathematics courses."},
    {"name": "BS Software Engineering", "field": "Computing", "backgrounds": _CS_BG,
     "subjects": "Mathematics required", "min_matric": 60, "min_inter": 60, "min_test": 50,
     "notes": "Focus on software design and development."},
    {"name": "BS Artificial Intelligence", "field": "Computing/AI", "backgrounds": _CS_BG,
     "subjects": "Mathematics required", "min_matric": 60, "min_inter": 60, "min_test": 50,
     "notes": "Strong maths and programming aptitude recommended."},
    {"name": "BS Data Science", "field": "Computing/Data", "backgrounds": _CS_BG,
     "subjects": "Mathematics required; Statistics helpful", "min_matric": 60, "min_inter": 60, "min_test": 50,
     "notes": "Statistics and programming interest helpful."},
    {"name": "BS Cyber Security", "field": "Computing/Security", "backgrounds": _CS_BG,
     "subjects": "Mathematics required", "min_matric": 60, "min_inter": 60, "min_test": 50,
     "notes": "Networking and systems interest helpful."},
    {"name": "BS Electrical Engineering", "field": "Engineering", "backgrounds": _ENG_BG,
     "subjects": "Mathematics, Physics, Chemistry/CS", "min_matric": 60, "min_inter": 60, "min_test": 50,
     "notes": "PEC registration/accreditation rules apply."},
    {"name": "BS Computer Engineering", "field": "Engineering", "backgrounds": _ENG_BG,
     "subjects": "Mathematics, Physics, Chemistry/CS", "min_matric": 60, "min_inter": 60, "min_test": 50,
     "notes": "PEC rules apply; hardware + software focus."},
    {"name": "BBA", "field": "Business", "backgrounds": ["FSc Pre-Engineering", "FSc Pre-Medical", "ICS (Computer Science)",
                                                          "I.Com / Commerce", "FA / Humanities", "A-Level"],
     "subjects": "Any Intermediate group", "min_matric": 50, "min_inter": 50, "min_test": 40,
     "notes": "Interest in management, marketing, finance."},
    {"name": "BS Accounting & Finance", "field": "Business", "backgrounds": ["I.Com / Commerce", "FSc Pre-Engineering",
                                                                            "ICS (Computer Science)", "FA / Humanities", "A-Level"],
     "subjects": "Accounting/Maths helpful", "min_matric": 50, "min_inter": 50, "min_test": 40,
     "notes": "Suitable for commerce students."},
    {"name": "BS Mathematics", "field": "Sciences", "backgrounds": ["FSc Pre-Engineering", "ICS (Computer Science)", "A-Level"],
     "subjects": "Mathematics required", "min_matric": 50, "min_inter": 50, "min_test": 40,
     "notes": "Good for analytical/research careers."},
    {"name": "BS Biosciences", "field": "Sciences", "backgrounds": ["FSc Pre-Medical", "A-Level"],
     "subjects": "Biology, Chemistry required", "min_matric": 55, "min_inter": 55, "min_test": 45,
     "notes": "Pre-Medical background preferred."},
    {"name": "BS Psychology", "field": "Humanities", "backgrounds": ["FSc Pre-Medical", "FA / Humanities", "I.Com / Commerce",
                                                                     "ICS (Computer Science)", "FSc Pre-Engineering", "A-Level"],
     "subjects": "Any Intermediate group", "min_matric": 50, "min_inter": 50, "min_test": 40,
     "notes": "Interest in human behavior and research."},
]


def _full(p):
    return (f"- {p['name']} [{p['field']}] | Accepted groups: {', '.join(p['backgrounds'])} | "
            f"Subjects: {p['subjects']} | Min Matric/O-Level: {p['min_matric']}% | "
            f"Min Inter/A-Level: {p['min_inter']}% | Entry test: CUI/NTS test, sample min {p['min_test']}% | "
            f"Notes: {p['notes']}")


def _brief(p):
    return (f"- {p['name']} [{p['field']}] groups: {', '.join(p['backgrounds'])}; {p['subjects']}; "
            f"min {p['min_matric']}%/{p['min_inter']}%/test {p['min_test']}%")


def general_requirements_text():
    return "\n".join(f"- {r}" for r in GENERAL_REQUIREMENTS)


def target_programs_text(preferred, background):
    """Full requirements for the preferred program, or all programs accepting the student's group."""
    if preferred:
        chosen = [p for p in PROGRAMS if p["name"] == preferred]
    else:
        chosen = [p for p in PROGRAMS if background in p["backgrounds"]] or PROGRAMS
    return "\n".join(_full(p) for p in chosen)


def all_programs_text():
    return "\n".join(_brief(p) for p in PROGRAMS)
