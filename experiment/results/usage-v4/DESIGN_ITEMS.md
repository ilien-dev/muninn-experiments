# usage-v4: what an implementer may read

The pre-registration splits every labelled set by `sha256("usage-v4:" + id)`: even first byte is
design, odd is held-out. Implementers read design items only. Held-out items are read by the
scoring scripts in this directory and by nobody writing a fix.

## Ids (committed, in `splits/`)

| set | id form | design | held-out | files |
|---|---|---|---|---|
| precision (typed records) | `STORE:record id` | 63 | 46 | `precision_{design,heldout}_ids.txt` |
| recall (sampled messages) | `STORE:session8:byte offset` | 152 | 148 | `recall_{design,heldout}_ids.txt` |
| delivery (prompts; every block of a prompt goes with it) | `Pnnn` | 82 | 68 | `delivery_{design,heldout}_ids.txt` |
| session starts (C4) | `Snn` | 21 | 18 | `session_start_{design,heldout}_ids.txt` |

`quarantined_design_ids.txt` lists 20 design items whose text is also the text of a held-out item
of the other extraction set: a precision record whose source turn is a held-out recall message,
or a recall message that is the source turn of a held-out precision record. They stay in the
design split for scoring and are left out of the design views, so reading the views never shows
held-out text.

## Private files an implementer may open (under `$MUNINN_USAGE_FIXTURES`)

- `out/usage-v4/design_views/precision_design.txt`: the design typed records, their source
  message and final label (quarantined items left out).
- `out/usage-v4/design_views/recall_design.txt`: the design messages, the previous assistant
  text, final label, kind and anchor phrases (quarantined items left out).
- `out/usage-v4/design_views/delivery_design.txt`: the design prompts with every delivered and
  cut block and its final label.
- `out/usage-v4/design_views/session_start_design.txt`: the design session starts, block and
  catalogue slots with their labels.
- The four analysis reports (`out/readpath.md`, `out/writepath.md`, `out/extract.md`,
  `out/delivery.md`): they give totals and name a few records by id, as the plan already allows.
- Store copies under `stores/` for reproducing a defect on a throwaway copy, and the analysis
  scripts under `scripts/`. A store copy holds the held-out records too: run code against it,
  but do not read the text of a record whose id is in a held-out list.

## Private files an implementer must not open

Everything that mixes the two splits or holds held-out text or labels:

- `out/usage-v4/labels/*` (the frozen labels of both splits, and the anchor phrases);
- `out/extract/*_items.jsonl`, `out/extract/items/`, `out/extract/*_labels.jsonl`,
  `out/extract/precision_joined.json`, `out/extract/second_pass*`, `out/extract/stats.json`;
- `out/delivery/sample_*.jsonl`, `out/delivery/pairs.jsonl`, `out/delivery/label_in/`,
  `out/delivery/labels/`, `out/delivery/*replay*.json`, `out/delivery/g1_rows.json`;
- `label2/` (the second labeller's reading views, raw passes, disagreements and adjudication);
- `work/usage-v4/` (scratch copies the harness writes, including replayed stores and dumps).

When a fix needs more than the design views show, ask for a new design view rather than opening
one of these.
