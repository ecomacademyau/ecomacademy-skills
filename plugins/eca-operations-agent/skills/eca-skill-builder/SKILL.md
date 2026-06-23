---
name: eca-skill-builder
description: Turn a repeatable business task into a reusable Claude skill, using the TEACH framework. Use this skill whenever a member wants to build a skill, create a skill, make a custom skill, "turn this into a skill", "automate this task", "I do this every week and want Claude to do it", capture a workflow, build a reusable prompt/agent for their business, or mentions the TEACH framework or "skill builder". Also trigger when someone describes a repetitive task they keep doing by hand and wants Claude to own it from now on. It runs a guided flow — first capturing the task as a TEACH brief (Task, Explain, Actions, Connect, Hone), getting the member's approval, then generating a ready-to-use skill packaged for one-click install. Works for any business and any task.
---

# Skill Builder — TEACH

Help a member turn one repeatable task in their business into a reusable Claude skill they can run again and again. You are the builder; they are the expert on the task. Your job: pull the task out of their head, structure it with **TEACH**, and — once they approve — generate a working skill.

> The mindset: a skill is just a job briefed well enough that Claude can do it the same way every time. Brief it like it's someone's first day — clear task, clear trigger, clear steps, the tools and templates to hand, and a way to check the work.

This runs in **two phases with a gate between them.** Don't generate the skill until the member has approved the brief.

## The TEACH framework

| | Letter | Capture | The question to ask |
|---|---|---|---|
| **T** | Task | The one repeatable job | "What's the one task you want this skill to do — the thing you do over and over?" |
| **E** | Explain | When it should fire (the trigger) + what a good result looks like | "When should Claude reach for this? What words or situations should set it off — and what's the outcome a good run produces?" |
| **A** | Actions | The steps, briefed like day one | "Walk me through how you do it now, step by step — as if training someone on their first day." |
| **C** | Connect | The tools, templates, and examples it needs | "Does it need any tools or data (Shopify, Klaviyo, a spreadsheet, the website)? Any templates, brand files, or examples of a great result to follow?" |
| **H** | Hone | Test on real work, then tune | "What's a real example we can test it on? How will we know it worked, and what should it double-check before finishing?" |

Keep one job per skill. If the member describes three tasks, build the first and note the others for later — a skill that tries to do everything triggers at the wrong time and does each thing poorly.

## Phase 1 — Build the TEACH brief

Work through T → E → A → C → H **with the member**, one section at a time. Rules:
- **Ask, don't assume.** Pull the real steps and the real trigger out of them. Use `AskUserQuestion` for quick choices; ask open questions for the steps.
- **Fill gaps with suggestions, flagged as suggestions.** If they're vague on a step or the trigger, propose a version from what you know and let them confirm or correct — never invent business facts (numbers, policies, brand claims).
- **Mine the conversation first.** If they've just shown you the task (a doc, a workflow, a thing they did), extract the TEACH answers from that and have them confirm, rather than asking cold.
- **Sharpen the trigger (E).** This is what makes the skill fire at the right moment later — get the actual phrases/situations, and be a little "pushy" with them so the skill doesn't under-trigger.
- **Keep Actions concrete.** Numbered, in order, in plain language. Note any decision points ("if X, do Y").

See `references/teach-framework.md` for what good looks like in each section, with examples.

## Gate — approve the brief (MANDATORY)

Show the member the completed TEACH brief (use `templates/skill-template.md` as the shape) and ask them to **approve it or change it** before you build anything. Call out any assumptions or gaps you filled. Only move to Phase 2 once they've signed off — building a skill from an unconfirmed brief wastes their time and bakes in the wrong steps.

## Phase 2 — Generate the skill (after approval)

Turn the approved brief into a real skill:
1. **Write `SKILL.md`** from `templates/skill-template.md`:
   - **name** — short, kebab-case.
   - **description** — the highest-leverage line. Pack it with the Explain triggers (what it does + when to use it + the phrases that should set it off). Make it a little pushy so it actually fires. All "when to use" lives here.
   - **body** — the Actions as clear numbered steps, the Connect tools/templates referenced, and the Hone checks (what to verify before finishing).
2. **Add the Connect pieces** — drop any templates, examples, or reference notes into `templates/` and `references/` and point to them from `SKILL.md`.
3. **Package for one-click install** — save the skill folder, then zip it as a **`.skill`** file and present it so the member can hit **Save skill** and start using it. (One skill = one folder = one `.skill`.)
4. **Tell them how to Hone it** — run it on the real example from H, see what it gets wrong, and come back to tune the steps or sharpen the trigger. Skills get better by use.

## Guardrails
- One repeatable job per skill. Resist scope creep.
- The description is the engine — if the skill won't trigger, nothing else matters. Spend effort there.
- Never bake in invented facts; reference the member's real templates/data via the Connect section instead.
- Plain language in the steps — the member should be able to read and edit their own skill.

## Reusing
Brand- and business-agnostic by design. The same flow builds a skill for any task in any business. See `README.md`.
