# Resume Agent Project Instructions

## Goal
Build a simple resume feedback agent that reviews a resume against a job description and gives practical feedback to improve the estimated ATS match score toward 90+.

## Scope
The agent should only provide resume feedback. It should not apply to jobs, write cover letters, scrape job sites, message recruiters, or make claims that a score guarantees interviews.

## Core behavior
When given a resume and job description, the agent should return:

1. Estimated ATS match score from 0 to 100
2. Short explanation of the score
3. Missing keywords from the job description
4. Weak or underrepresented skills
5. Resume formatting issues
6. Bullet-by-bullet improvement suggestions
7. A prioritized action plan to reach 90+
8. Warnings about keyword stuffing or dishonest changes

## Scoring rules

Score should be based on:
- Job title alignment
- Hard skills match
- Tools and technologies match
- Responsibilities match
- Education/certification match
- Measurable impact in bullet points
- ATS-friendly formatting

The score is only an estimate, not a real ATS guarantee.

## Output style
Use clear markdown.
Be direct and specific.
Do not rewrite the entire resume unless explicitly asked.
Suggest keywords only when they appear in the job description or are strongly implied by the role.
Never suggest adding skills, experience, education, or certifications the candidate does not actually have.

## Technical preferences
Start with a simple Python CLI.
Keep the code beginner-friendly.
Avoid unnecessary frameworks.
Use functions with clear names.
Include comments where helpful.

## Synchronous review workflow

The resume agent should suggest improvements for user review instead of automatically modifying the resume.

When rewriting bullets:
- Keep the rewritten bullet close to the original meaning.
- Do not invent tools, metrics, companies, certifications, or outcomes.
- Do not add keywords unless they are supported by the original resume or the user confirms them.
- Mark uncertain additions with "Only add if true."
- Output suggestions in a review-friendly Markdown table.
- Never overwrite the original resume file unless the user explicitly approves.

## Report readability rule

Avoid large Markdown tables when cells contain long text.

For bullet rewrite suggestions, use review cards instead of tables.

Each card should include:
- Original bullet
- Issue
- Suggested rewrite
- Keywords included
- Honesty check
- Decision checkboxes

The output should be easy to read in plain Markdown.