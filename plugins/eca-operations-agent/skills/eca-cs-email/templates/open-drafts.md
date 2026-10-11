# Open drafts

What this skill has drafted and not yet seen sent. Reconciled against `list_drafts` at the
start of every run.

**It exists because a run has no memory of the last one.** Without it, a second run cannot
tell its own draft from one the member wrote by hand, cannot tell an untouched draft from
an edited one, and will cheerfully write a second draft on a thread that already has one.

Do not edit by hand. Lines are cleared once a draft is sent or discarded.

| thread_id | draft_id | written | category | opening |
|---|---|---|---|---|
| | | | | |

## Reconciling

| What you see | Meaning | Do |
|---|---|---|
| On the thread, not in this file | The member wrote it | Leave it alone |
| Here, `date` unchanged, unsent | Yours, untouched | Leave it, report it as waiting |
| Here, `date` has moved | They edited it | Leave it, and reset that category's unchanged run |
| Here, customer wrote after the draft | Stale | Replace it and say so |
| Here, gone from `list_drafts` | Sent or discarded | Feed to the learning step, clear the line |

`written` is the draft's own `date` at the time it was created, so a later edit shows as a
changed date. `opening` is the first 80 characters of the body, for when the date alone is
not conclusive.

**When it cannot be resolved, treat the draft as the member's and leave it.** The cost of
leaving a draft alone is that it waits. The cost of overwriting theirs is their work.
