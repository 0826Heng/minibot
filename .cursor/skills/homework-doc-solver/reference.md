# Homework Document Solver Reference

## Recommended Output Formats

### A. Short-answer assignment

```markdown
# 作业答案

## Q1
Answer: ...

## Q2
Answer: ...
```

### B. Explanation-heavy assignment

```markdown
## Q1
Answer: ...
Reasoning: ...
```

### C. Code assignment

~~~markdown
## Q1
Answer:
```python
# code
```

Complexity: ...
Edge cases: ...
~~~

## Completeness Check Template

```markdown
Coverage Report
- Total questions: <n>
- Answered: <n>
- Missing: <list or None>
- Assumptions: <list or None>
- Needs confirmation: <list or None>
```

## Integration Rules by File Type

- `.md` / `.txt`: edit directly and keep heading hierarchy.
- `.docx`: preserve heading levels and list numbering; avoid collapsing paragraphs.
- `.pdf`: if direct edit is unreliable, generate `.md` or `.docx` derivative and keep section mapping.
