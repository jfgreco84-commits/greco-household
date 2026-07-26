# BEST SOLUTION, FIX PLAN
Every fix from the audit, ranked in the order I recommend doing them. **Nothing here is done yet.** Finding numbers refer to BS_AUDIT_REPORT.md.

**Supabase note: NOT ONE fix below needs a schema change.** Everything is app-code only. Your data model is fine.

---

## FIX TODAY (under an hour total, all tiny, all safe)

| # | Fix | Finding | Effort |
|---|-----|---------|--------|
| 1 | Add `debit:0` to the payment totals initializer so your $256 of debit money shows up in the split | 7 | 2 min |
| 2 | Relabel the active-show "Potential" tile to use the real potential number | 13 | 2 min |
| 3 | Local-time date helper so shows stop flipping to "missed" at 7pm and evening exports get the right date | 11 | 15 min |
| 4 | Replace the stale `BEST_SOLUTION_APP_BLANK.html` in the personal-app repo with the redirect stub | 14 | 5 min |
| 5 | Disable save buttons on first tap on the six append-style modals (no more double-logged expenses) | 16 | 20 min |

**Also today, zero code:** answer the four questions at the bottom of the audit report (tax, real prices, bundles, Ronny's rate). Two of the biggest distortions (findings 3 and 5) are blocked on your answers, and the price fix might be a 2-minute Settings edit with no deploy at all.

## FIX THIS WEEK (the profit-truth package)

These four make the profit number honest. Do them together and re-verify WCF as the test case.

| # | Fix | Finding | Effort |
|---|-----|---------|--------|
| 6 | Deduct card fees (3% x Square+Debit) in every show P&L, shown as its own line | 1 | 2-3 hrs |
| 7 | Auto-include gas in show profit (skip when day gas was hand-entered, never double count) | 2 | 2-3 hrs |
| 8 | Book booth expense as what you actually PAID when it differs from sticker (WCF $589 vs $580) | 6 | 1-2 hrs |
| 9 | "Staffed day, no pay entered" red badge + closeout nag, so Ronny is never free labor | 10 | 2-3 hrs |
| 10 | Warning chip when a day has money logged but missing counts (profit ignores COGS that day) | 12 | 1-2 hrs |

Definition of done: the app's WCF profit matches my corrected recompute within pennies, fees and gas visible as their own lines.

## FIX BEFORE CRANBERRY FEST (Sep 25, the big one)

| # | Fix | Finding | Effort |
|---|-----|---------|--------|
| 11 | Sales tax split: per-show tax rate, collected money divides into yours vs state's, running "owed to WI" total | 3 | half day, after your answer |
| 12 | Real break-even: show's own COGS ratio + fees, displayed in dollars AND units | 8 | half day |
| 13 | Port Batman's editable per-product costs to all four apps | 9 | 2-3 hrs |
| 14 | Price snapshot per show (changing Settings prices stops rewriting history) + per-show price override if your prices vary by show | 5 | half day |
| 15 | End-show inventory return fix: return packed + restock minus consumed with a confirmation showing the math | 4a | 2-3 hrs |
| 16 | Cloud-sync guard: warn before adopting a cloud copy that would discard newer local day entries | 4b | 2-3 hrs |
| 17 | Quick-sale entry in the booth (the redesign, see BS_REDESIGN_PROPOSAL.md) | friction #1 | 1-2 days |
| 18 | Home dashboard hero number + hierarchy pass (see BS_REDESIGN_PROPOSAL.md) | friction #6 | 1 day |
| 19 | Readability pass: kill 8-9px text, brighten muted gray, 5-step type scale | visual | 2-3 hrs |

## PARK IT (not worth it now)

- Integer-cents money storage (finding 17). Float dust never reaches a penny at your volumes.
- True day-level cloud merge (finding 4b full version). The warning (fix 16) covers the real risk at your team size.
- Confetti and best-day delight moments. Cheap, fun, do them with fix 18 if you want.

## PROCESS FIX (decide, then 30 minutes)

- **Finding 15:** declare the LIVE code the one master. I regenerate the greco-household copies from it and update HANDOFF.md so the next session cannot accidentally undo the July overhaul. Needs your one-word go-ahead.

---

## HOW EACH FIX SHIPS (per your rules)

1. Backup first: dated copies of all four live HTML files into `best-solution/AUDIT/backup_YYYY-MM-DD/` before any edit.
2. One fix = one commit, tested with the harness (real WCF data) before and after, and I show you the before/after numbers.
3. Deploys go to the four Pages repos the same way as the Jul 26 deploy, with a fresh cache-bust URL for you to open.
4. No Supabase schema changes are needed for any of this; if that ever changes you approve the specific change first.
