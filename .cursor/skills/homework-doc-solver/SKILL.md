---
name: homework-doc-solver
description: Solve homework from user-provided documents and integrate answers back into the original file structure. Use when the user uploads assignment documents, asks to generate answers, fill homework, or merge responses into Word/PDF/Markdown/text files.
---

# Homework Document Solver

## Goal

When a user provides a homework document, generate high-quality answers and write them back into a deliverable document while preserving structure and readability.

## Trigger Signals

Use this skill when the user mentions:
- "作业文档"
- "生成答案"
- "填到文档里"
- "整合回原文件"
- "批改/完成题目"

## Workflow

Copy this checklist and keep it updated:

```markdown
Progress
- [ ] Step 1: Inspect input document type and structure
- [ ] Step 2: Extract questions and constraints
- [ ] Step 3: Draft answers with explicit assumptions
- [ ] Step 4: Integrate answers into the target document
- [ ] Step 5: Run completeness and quality checks
```

### Step 1: Inspect input document

1. Detect document type:
   - Text-like: `.md`, `.txt`
   - Office-like: `.docx`
   - PDF-like: `.pdf`
2. Identify sections, numbering, question boundaries, and required output language.
3. Preserve original heading and numbering style.

### Step 2: Extract questions and constraints

1. Build a question list with stable IDs:
   - `Q1`, `Q2`, ... or original numbers.
2. Record each question's required format:
   - short answer / explanation / code / proof / calculation.
3. Capture hard constraints:
   - word limit, language, formulas, citation style, forbidden tools.

### Step 3: Generate answers

1. Answer each question directly first, then add concise reasoning when needed.
2. If information is missing, state assumptions explicitly.
3. Keep terminology consistent with the source document.
4. For computation or code answers, include verifiable intermediate steps.

Answer block template:

```markdown
### Q{n}
**Answer:** <final answer>

**Reasoning (concise):** <key steps>

**Assumptions (if any):** <assumptions or "None">
```

### Step 4: Integrate answers into document

Default rule: keep original content and append answer immediately after each question.

Integration modes:
- Inline mode: insert `Answer:` below each question.
- End-of-section mode: keep question area untouched and add `Answers` section at the end with mapping.

Format rules:
1. Do not remove original problem statements.
2. Keep existing numbering unchanged.
3. Keep answer labels consistent (`Answer`, `解答`, etc.).
4. If conversion is needed (for example PDF to editable format), create an editable derivative and explain why.

### Step 5: Quality checks

Before final output, verify:

- Every question has one mapped answer.
- No contradictions across answers.
- Units, formulas, and code snippets are valid.
- Language style is consistent with user request.
- Document structure remains readable and complete.

## Output Contract

Return:
1. Edited output file path.
2. Coverage summary:
   - total questions
   - answered questions
   - unanswered questions (if any)
3. Risk notes:
   - assumptions
   - low-confidence answers
   - sections that need user confirmation

## Safety and Academic Policy

1. Do not fabricate citations or experimental data.
2. Mark uncertain content clearly.
3. If the user asks for strict "only final answers", still keep an internal mapping to ensure completeness.

## Additional Resources

- For reusable response structures, see [reference.md](reference.md).
