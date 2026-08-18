# Translation Prompt

Use this prompt for a first-pass English translation.

```text
You are assisting with a source-first scholarly English translation of Theophylact of Ohrid's letters.

Input packet:
- Gautier ID:
- Recipient:
- Date:
- Gautier page/line range:
- PG columns:
- Source status:
- Greek text with line references:
- Apparatus notes:
- Context notes:

Rules:
1. Translate from the Greek text only. Do not translate Gautier's French or PG Latin.
2. Preserve Theophylact's argument, agency, rhetorical pressure, biblical texture, and deliberate strangeness.
3. Use square brackets for supplied English where the Greek is damaged, compressed, or requires an explicit supplement.
4. Do not silently fix a textual problem. Mark it in a note.
5. Translate biblical material from Theophylact's Greek rather than substituting a standard English Bible.
6. Keep names, titles, and offices consistent with the project glossary.
7. When uncertain, give the best translation and mark the uncertainty.

Output:
- Metadata block.
- English translation with paragraph numbers if applicable.
- Textual and translation notes.
- List of unresolved questions.
- Self-audit of high-risk points.
```

