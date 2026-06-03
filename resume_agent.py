import re
from collections import Counter


COMMON_WORDS = {
    "the", "and", "or", "a", "an", "to", "of", "in", "for", "with", "on", "by",
    "as", "is", "are", "be", "this", "that", "you", "your", "we", "our", "will",
    "from", "at", "it", "all", "can", "have", "has", "must", "should", "about",
    "who", "where", "their", "help", "canadian", "tire", "commitment",
    "committed", "believe", "people", "culture", "environment", "business"
}


IMPORTANT_SECTIONS = [
    "education",
    "experience",
    "projects",
    "skills",
    "certifications",
    "summary"
]


MULTI_WORD_KEYWORDS = [
    "data visualization",
    "project management",
    "machine learning",
    "power bi",
    "data analysis",
    "business intelligence",
    "stakeholder management",
    "problem solving",
    "cross functional",
    "customer service",
    "software development",
    "product management",
    "digital marketing",
    "social media",
    "financial analysis",
    "data governance",
    "data management",
    "data quality",
    "data integrity",
    "data stewardship",
    "data profiling",
    "data discovery",
    "data models",
    "data glossaries",
    "data catalogues",
    "data mappings",
    "data lineage",
    "data classifications",
    "data lifecycle",
    "data integration",
    "reference data",
    "microsoft office",
    "oracle databases",
    "sql queries",
    "structured relational databases",
    "shell scripting",
    "linux commands",
    "ibm knowledge catalog"
]


def clean_text(text: str) -> str:
    return text.lower()


def extract_words(text: str) -> list[str]:
    text = clean_text(text)
    words = re.findall(r"[a-zA-Z][a-zA-Z0-9+#.-]*", text)
    return [word for word in words if word not in COMMON_WORDS and len(word) > 2]


def extract_multi_word_keywords(job_description: str) -> list[str]:
    job_text = clean_text(job_description)
    found_keywords = []

    for keyword in MULTI_WORD_KEYWORDS:
        if keyword in job_text:
            found_keywords.append(keyword)

    return found_keywords


def extract_keywords(job_description: str, top_n: int = 40) -> list[str]:
    multi_word_keywords = extract_multi_word_keywords(job_description)
    words = extract_words(job_description)
    counts = Counter(words)
    single_word_keywords = [word for word, _ in counts.most_common(top_n)]

    return multi_word_keywords + [
        keyword for keyword in single_word_keywords
        if keyword not in multi_word_keywords
    ]


def find_missing_keywords(resume: str, job_description: str) -> list[str]:
    resume_text = clean_text(resume)
    job_keywords = extract_keywords(job_description)

    missing = []
    for keyword in job_keywords:
        if keyword not in resume_text:
            missing.append(keyword)

    return missing


def estimate_score(resume: str, job_description: str) -> int:
    resume_text = clean_text(resume)
    job_keywords = extract_keywords(job_description)

    if not job_keywords:
        return 0

    matched = sum(1 for keyword in job_keywords if keyword in resume_text)
    keyword_score = matched / len(job_keywords)

    section_score = 0
    for section in IMPORTANT_SECTIONS:
        if section in resume_text:
            section_score += 1
    section_score = section_score / len(IMPORTANT_SECTIONS)

    has_numbers = bool(re.search(r"\d+%|\$\d+|\d+\+", resume))
    impact_score = 1 if has_numbers else 0

    final_score = (
        keyword_score * 70
        + section_score * 20
        + impact_score * 10
    )

    return round(final_score)


def formatting_feedback(resume: str) -> list[str]:
    feedback = []

    if "|" in resume:
        feedback.append("Avoid tables or column-like formatting using `|`; ATS tools may parse them poorly.")

    if len(resume.splitlines()) < 10:
        feedback.append("Resume looks very short. Add more detail under experience, projects, or skills.")

    if not re.search(r"\d+%|\$\d+|\d+\+", resume):
        feedback.append("Add measurable impact, such as percentages, dollar amounts, user counts, time saved, or performance improvements.")

    lower_resume = clean_text(resume)
    for section in ["experience", "education", "skills"]:
        if section not in lower_resume:
            feedback.append(f"Add a clear `{section.title()}` section heading.")

    return feedback


def extract_resume_bullets(resume: str) -> list[str]:
    bullets = []

    for line in resume.splitlines():
        line = line.strip()
        if line.startswith(("•", "-", "*")):
            bullets.append(line.lstrip("•-* ").strip())

    return bullets


def find_keywords_for_bullet(bullet: str, missing_keywords: list[str]) -> list[str]:
    bullet_text = clean_text(bullet)
    keyword_matches = []

    keyword_hints = {
        "data governance": ["documentation", "approved", "guardrails", "quality", "integrity"],
        "data management": ["data", "database", "schema", "workflow", "documents"],
        "data quality": ["testing", "quality", "validated", "consistency", "defects"],
        "data integrity": ["schema", "database", "validated", "consistency", "integrity"],
        "metadata": ["documents", "fields", "catalog", "lineage"],
        "reference data": ["database", "schema", "mapping", "fields"],
        "data stewardship": ["stakeholder", "documentation", "teams", "communication"],
        "data profiling": ["analyze", "analysis", "sql", "queries", "datasets"],
        "data discovery": ["analyze", "analysis", "sql", "queries", "datasets"],
        "data models": ["schema", "schemas", "er diagrams", "database"],
        "data mappings": ["schema", "schemas", "fields", "documents"],
        "data lineage": ["workflow", "pipeline", "process", "documents"],
        "data integration": ["integrate", "integration", "pipelines", "workflow"],
        "stakeholders": ["stakeholder", "teams", "communication", "user guides"],
        "sql": ["sql", "database", "query", "queries", "schema"],
        "excel": ["excel", "macro"],
        "power bi": ["power bi", "powerbi", "dashboard"],
        "python": ["python", "pandas", "pytorch", "scikit-learn"],
    }

    for keyword in missing_keywords:
        keyword_text = clean_text(keyword)
        hints = keyword_hints.get(keyword_text, [])
        if any(hint in bullet_text for hint in hints):
            keyword_matches.append(keyword)

    return keyword_matches[:3]


def describe_bullet_issue(bullet: str, keywords: list[str]) -> str:
    issues = []

    if not re.search(r"\d+%|\$\d+|\d+\+|\d+,\d+", bullet):
        issues.append("No clear metric or scale")

    if keywords:
        issues.append("Could better reflect job description language")

    if len(bullet.split()) > 35:
        issues.append("Long bullet; may be harder to scan")

    if not issues:
        issues.append("Mostly strong; review for role alignment")

    return "; ".join(issues)


def suggest_bullet_rewrite(bullet: str, keywords: list[str]) -> str:
    if not keywords:
        return f"{bullet} Add a measurable result or job-specific context if true."

    keyword_phrase = ", ".join(keywords)
    return f"{bullet} If accurate, connect this work to {keyword_phrase} using the same facts already in the bullet."


def honesty_check_for_bullet(keywords: list[str]) -> str:
    if not keywords:
        return "Confirm any added metric or context before using."

    return "Only add if true. User should confirm the keyword accurately describes the work."


def bullet_rewrite_suggestion_agent(
    resume: str,
    job_description: str,
    missing_keywords: list[str]
) -> str:
    bullets = extract_resume_bullets(resume)

    if not bullets:
        return (
            "### Suggestion 1\n\n"
            "**Original bullet**\n"
            "- No bullets found\n\n"
            "**Issue**\n"
            "Resume may need bullet points under experience or projects.\n\n"
            "**Suggested rewrite**\n"
            "- Add clear achievement bullets before using this agent.\n\n"
            "**Keywords included**\n"
            "None\n\n"
            "**Honesty check**\n"
            "User should manually add truthful bullets.\n\n"
            "**Decision**\n"
            "[ ] Accept\n"
            "[ ] Edit\n"
            "[ ] Reject"
        )

    review_cards = []

    for number, bullet in enumerate(bullets, start=1):
        keywords = find_keywords_for_bullet(bullet, missing_keywords)
        issue = describe_bullet_issue(bullet, keywords)
        suggestion = suggest_bullet_rewrite(bullet, keywords)
        keyword_text = ", ".join(keywords) if keywords else "None"
        honesty_check = honesty_check_for_bullet(keywords)

        review_cards.append(
            f"### Suggestion {number}\n\n"
            "**Original bullet**\n"
            f"- {bullet}\n\n"
            "**Issue**\n"
            f"{issue}\n\n"
            "**Suggested rewrite**\n"
            f"- {suggestion}\n\n"
            "**Keywords included**\n"
            f"{keyword_text}\n\n"
            "**Honesty check**\n"
            f"{honesty_check}\n\n"
            "**Decision**\n"
            "[ ] Accept\n"
            "[ ] Edit\n"
            "[ ] Reject"
        )

    return "\n\n".join(review_cards)


def generate_report(resume: str, job_description: str) -> str:
    score = estimate_score(resume, job_description)
    missing_keywords = find_missing_keywords(resume, job_description)
    formatting_issues = formatting_feedback(resume)
    bullet_suggestions = bullet_rewrite_suggestion_agent(
        resume,
        job_description,
        missing_keywords
    )

    report = []

    report.append("# Resume ATS Feedback Report")
    report.append("")
    report.append(f"## Estimated ATS Match Score: {score}/100")
    report.append("")
    report.append("This is an estimated score based on keyword overlap, basic section structure, and measurable impact. It is not a guarantee of passing a real ATS.")
    report.append("")

    report.append("## Missing Keywords")
    if missing_keywords:
        for keyword in missing_keywords[:25]:
            report.append(f"- {keyword}")
    else:
        report.append("- No major missing keywords found from the top job description terms.")
    report.append("")

    report.append("## Formatting / Structure Issues")
    if formatting_issues:
        for issue in formatting_issues:
            report.append(f"- {issue}")
    else:
        report.append("- No major formatting issues detected.")
    report.append("")

    report.append("## Bullet Rewrite Suggestions")
    report.append("Review and approve these manually. Do not add keywords unless they truthfully describe your experience.")
    report.append("")
    report.append(bullet_suggestions)
    report.append("")

    report.append("## Priority Actions To Reach 90+")
    report.append("1. Add the missing keywords only where they truthfully match your experience.")
    report.append("2. Mirror the job title and core skills from the job description in your summary or skills section.")
    report.append("3. Add measurable results to your bullets.")
    report.append("4. Use standard headings like Skills, Experience, Projects, Education.")
    report.append("5. Avoid tables, graphics, text boxes, and overly designed layouts.")
    report.append("")

    report.append("## Suggested Keyword Strategy")
    report.append("Do not keyword-stuff. Add keywords naturally inside bullets, skills, and project descriptions.")
    report.append("")

    return "\n".join(report)


def read_file(path: str) -> str:
    with open(path, "r", encoding="utf-8") as file:
        return file.read()


def write_report(path: str, report: str) -> None:
    with open(path, "w", encoding="utf-8") as file:
        file.write(report)


def main():
    resume = read_file("examples/resume.txt")
    job_description = read_file("examples/job_description.txt")

    report = generate_report(resume, job_description)
    write_report("report.md", report)
    print(report)
    print("\nReport saved to report.md")


if __name__ == "__main__":
    main()
