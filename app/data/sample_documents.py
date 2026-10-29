"""Indian Legal Knowledge Base.

Contains curated reference documents rooted in Indian jurisprudence, Central and State Acts,
and landmark Supreme Court precedents used by the Legal Research Agent.
"""

from typing import Any, Dict, List

SAMPLE_LEGAL_DOCUMENTS: List[Dict[str, Any]] = [
    {
        "id": "IN-DOC-TENANCY-001",
        "title": "Tenancy & Security Deposits Framework (Model Tenancy Act & State Rent Laws)",
        "category": "Tenancy & Property Law (India)",
        "keywords": [
            "tenant", "landlord", "rent", "security deposit", "model tenancy act",
            "rent control", "wear and tear", "notice to quit", "eviction", "transfer of property act"
        ],
        "summary": "Rules under Model Tenancy Act, 2021, Transfer of Property Act, 1882, and State Rent Control Acts.",
        "content": (
            "1. Security Deposit Limits (Model Tenancy Act, 2021, Sec 11):\n"
            "   Security deposit for residential premises is capped at a maximum of 2 months' rent. "
            "   For non-residential premises, it is capped at up to 6 months' rent.\n"
            "2. Return Timeline & Deductions:\n"
            "   The security deposit must be refunded to the tenant within 30 days of vacating the premises, "
            "   after adjusting for genuine rent arrears or agreed structural damages. Landlords cannot deduct "
            "   for reasonable / normal wear and tear.\n"
            "3. Termination & Notice to Quit (Transfer of Property Act, 1882, Sec 106):\n"
            "   In the absence of a written contract, lease of immovable property for residential purpose is terminable "
            "   by 15 days' written notice expiring with the end of a month of tenancy.\n"
            "4. Eviction Protections:\n"
            "   Landlords cannot arbitrarily evict tenants or cut off essential supplies (water, electricity). "
            "   Eviction requires orders from the designated Rent Authority / Rent Court."
        )
    },
    {
        "id": "IN-DOC-CONTRACT-002",
        "title": "Commercial Contracts & Non-Disclosure Agreements (Indian Contract Act, 1872)",
        "category": "Contract & Commercial Law (India)",
        "keywords": [
            "nda", "confidentiality", "contract act", "section 27", "trade secret",
            "non-disclosure", "injunction", "specific relief act", "exclusions"
        ],
        "summary": "Confidentiality obligations, permissible exceptions, and remedies under Indian Contract Act, 1872.",
        "content": (
            "1. Enforceability of Confidentiality (Indian Contract Act, 1872, Sec 10 & 27):\n"
            "   Non-Disclosure Agreements (NDAs) are valid and enforceable contracts in India. While negative covenants "
            "   during contract subsistence are valid, they must not act as an unlawful restraint of trade.\n"
            "2. Standard Exclusions from Confidentiality:\n"
            "   Information is exempt from confidentiality if:\n"
            "   (a) It is already in the public domain without breach of agreement;\n"
            "   (b) It was lawfully in the recipient's possession prior to disclosure;\n"
            "   (c) It is independently developed without reference to proprietary data;\n"
            "   (d) It is required to be disclosed pursuant to a court summons or statutory notice (e.g. under CrPC/BNSS).\n"
            "3. Legal Remedies for Breach:\n"
            "   Under the Specific Relief Act, 1963 (Sections 38 & 39), an aggrieved party can seek interim and "
            "   permanent injunctions to prevent unauthorized disclosure, alongside damages under Section 73 of the Contract Act."
        )
    },
    {
        "id": "IN-DOC-LABOR-003",
        "title": "Employment Restrictive Covenants & Section 27 Indian Contract Act, 1872",
        "category": "Labor & Employment Law (India)",
        "keywords": [
            "employment", "non-compete", "section 27", "contract act", "restraint of trade",
            "at-will", "termination", "severance", "percept d'mark", "zaheer khan"
        ],
        "summary": "Statutory invalidity of post-employment non-compete agreements under Indian law.",
        "content": (
            "1. Statutory Prohibition of Non-Competes (Indian Contract Act, 1872, Sec 27):\n"
            "   Section 27 explicitly states: 'Every agreement by which anyone is restrained from exercising a lawful "
            "   profession, trade or business of any kind, is to that extent void.' Indian law recognizes NO reasonableness exception.\n"
            "2. Landmark Supreme Court Precedents:\n"
            "   In Percept D'Mark (India) Pvt. Ltd. v. Zaheer Khan (2006) and Niranjan Shankar Golikari (1967), "
            "   the Supreme Court established that restrictive covenants extending beyond the term of employment are wholly void.\n"
            "   A company cannot legally restrain an ex-employee from joining a competitor or starting a rival business.\n"
            "3. Permissible vs Void Covenants:\n"
            "   - VALID: Non-disclosure of proprietary trade secrets, non-solicitation of clients/employees (for reasonable periods).\n"
            "   - VOID: Total ban on working for competitors after resignation or termination.\n"
            "4. Termination Notice:\n"
            "   Under state Shops & Establishments Acts, 30 days' written notice or salary in lieu thereof is customary."
        )
    },
    {
        "id": "IN-DOC-CONSUMER-004",
        "title": "Consumer Protection Act, 2019 & E-Commerce Consumer Rules",
        "category": "Consumer Protection Law (India)",
        "keywords": [
            "consumer", "consumer protection act", "deficiency in service", "refund", "unfair trade practice",
            "district commission", "e-commerce rules", "product liability"
        ],
        "summary": "Rights against deficiency of service, mandatory refund guidelines, and consumer dispute redressal.",
        "content": (
            "1. Core Consumer Rights (Consumer Protection Act, 2019, Sec 2(9)):\n"
            "   Consumers possess statutory rights to safety, information, choice, hearing, and redressal against unfair "
            "   or restrictive trade practices and deficiency in services.\n"
            "2. Deficiency in Service & Unfair Trade Practices:\n"
            "   Refusing refund for defective goods, charging above MRP, misleading advertisements, and non-compliance "
            "   with warranty constitutes deficiency in service under Section 2(11).\n"
            "3. Dispute Resolution Hierarchy:\n"
            "   - District Commission: Claims up to ₹50 Lakhs (e-filing via e-Daakhil portal).\n"
            "   - State Commission: Claims from ₹50 Lakhs to ₹2 Crores.\n"
            "   - National Commission (NCDRC): Claims exceeding ₹2 Crores.\n"
            "4. Limitation Period:\n"
            "   Complaints must be filed within 2 years from the date on which the cause of action arose (Sec 69)."
        )
    },
    {
        "id": "IN-DOC-IP-005",
        "title": "Software Copyright & Digital Data Governance (Copyright Act & IT Act)",
        "category": "Intellectual Property & Cyber Law (India)",
        "keywords": [
            "copyright act", "it act", "software", "open source", "mit", "gpl",
            "section 43a", "digital personal data protection", "dpdp", "intermediary"
        ],
        "summary": "Software licensing, copyright protection, and data privacy framework in India.",
        "content": (
            "1. Software as Literary Work (Copyright Act, 1957, Sec 2(o)):\n"
            "   Computer software, source code, and program manuals are protected as 'literary works'. "
            "   Unauthorized commercial reproduction or distribution without a license constitutes copyright infringement.\n"
            "2. Open Source Licensing in India:\n"
            "   Permissive licenses (MIT, Apache 2.0) are enforceable contracts granting commercial rights provided original "
            "   copyright and warranty disclaimers are preserved. Copyleft licenses (GPL v3) require distribution of derivative source code.\n"
            "3. Information Technology Act, 2000 & DPDP Act, 2023:\n"
            "   Section 43A of the IT Act mandates reasonable security practices for sensitive personal data. "
            "   The Digital Personal Data Protection Act, 2023 establishes consent-based data processing rules and penalties "
            "   up to ₹250 Crores for significant data breaches."
        )
    }
]
