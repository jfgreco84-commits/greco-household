# READY-TO-SHIP live app files — per-day rep pay overhaul (Jul 2026)

These 4 files are the LIVE apps with the day-pay overhaul ported onto them.
They were built from each live repo's current main (not from froggy-personal.html),
so every live-only feature survives: Froggy's app keeps its layout + Dave,
Batman's keeps freight tracking / cost overrides / per-day payout history,
the crew apps keep their dashboard redesign.

All 4 pass node --check and a 60+ assertion smoke test.

To deploy, copy each file over the target and push (from any machine with push
access to the Pages repos):

| File here | Target repo | Target filename |
|---|---|---|
| best-solution-app--BEST_SOLUTION_APP.html | best-solution-app | BEST_SOLUTION_APP.html |
| best-solution-blank--index.html | best-solution-blank | index.html |
| best-solution-isaiah--index.html | best-solution-isaiah | index.html |
| best-solution-anthony--index.html | best-solution-anthony | index.html |

Then open each app with a fresh cache-bust, e.g. ...BEST_SOLUTION_APP.html?v=19

NOTE: the live repos have diverged from froggy-personal.html (they have newer UI
work that was never synced back here). Do NOT deploy froggy-personal.html or the
generated blanks to the live repos — deploy THESE files.
