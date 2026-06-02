import re
from collections import Counter


COMMON_WORDS = {
    "the", "and", "or", "a", "an", "to", "of", "in", "for", "with", "on", "by",
    "as", "is", "are", "be", "this", "that", "you", "your", "we", "our", "will",
    "from", "at", "it", "all", "can", "have", "has", "must", "should", "about"
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
    "financial analysis"
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


def generate_report(resume: str, job_description: str) -> str:
    score = estimate_score(resume, job_description)
    missing_keywords = find_missing_keywords(resume, job_description)
    formatting_issues = formatting_feedback(resume)

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
