# LIVE MASTERS (v8.0, Jul 26 2026)

These four files ARE the source of truth. They are exact copies of what is
deployed to the four GitHub Pages repos after the audit-fix release (v8.0).

The old pipeline (froggy-personal.html + gen_blank.py, one folder up) is
RETIRED. It predates the July day-pay overhaul and the v8.0 audit fixes.
Do NOT run gen_blank.py or deploy the old files, they will undo live features.

To make a change: edit the file here for the app you are changing (the shared
core code is identical across all four; apply shared changes to all four),
verify with node --check on the extracted script, copy to the matching Pages
repo, push, and open the app with a fresh cache-bust (?v=N).

v8.0 shipped: card fees + auto gas + booth-paid in profit, card-only sales tax
split, real street prices w/ per-show snapshots, editable unit costs, ADD SALE
two-tap flow w/ bundles + undo, honest end-of-show stock return, break-even in
dollars AND units, debit in payment split, local dates, dup-tap guards,
closeout/no-count warnings, cloud overwrite warning, readability pass.
