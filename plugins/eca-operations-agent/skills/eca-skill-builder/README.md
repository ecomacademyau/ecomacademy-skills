# Skill Builder — the TEACH framework

A Claude skill that helps a member turn one repeatable task in their business into a **reusable skill** they can run again and again. Ships as **`eca-skill-builder`** inside the **ECA Operations Coworker**.

## What it does
It pulls a task out of the member's head and structures it with **TEACH**, then — once they approve the brief — generates a ready-to-use skill packaged for one-click install.

- **T — Task:** the one repeatable job
- **E — Explain:** when it should fire (the trigger) + what a good result looks like
- **A — Actions:** the steps, briefed like day one
- **C — Connect:** the tools, templates, and examples it needs
- **H — Hone:** test on real work, then tune

## How it works
```
skill-builder/
├── SKILL.md                     # The two-phase flow: build the TEACH brief → approve → generate the skill
├── README.md                    # This file
├── references/
│   └── teach-framework.md       # What good looks like for each letter, with examples + how to write the trigger
└── templates/
    └── skill-template.md         # The SKILL.md scaffold the builder fills in
```

**Phase 1** captures the TEACH brief by asking the member questions (filling gaps with flagged suggestions, never inventing business facts). **A gate** has them approve the brief. **Phase 2** generates the `SKILL.md` (with a trigger-rich description), adds any templates/examples, and packages the skill as a `.skill` file the member can install in one click — then tells them how to Hone it on real work.

## Reusing
Business- and brand-agnostic: the same flow builds a skill for any task in any business. Nothing to configure.
