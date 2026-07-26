# BEST SOLUTION APP SUITE, FULL AUDIT REPORT
Audit date: July 26, 2026. Auditor: Claude Code. Read-only audit. **Zero lines of app code were changed.**

---

## EXECUTIVE SUMMARY

**The good news: your math engine is honest.** I ran your live app's own code in a test harness against your real Washington County Fair data, and every core formula computes exactly what it claims. Your inventory counting system with the lock, the change log, and the reconciliation flags is genuinely strong, better than most small business tools.

**The bad news: real money never makes it into "profit."** Square fees (about $88 at WCF so far), gas (about $117), and the extra $9 you paid on the booth are all invisible to the profit number. Ronny's pay shows as $0 until you type it in. **Your WCF profit is overstated by at least $214 right now, more once Ronny is paid.**

**The surprise: COGS is NOT missing.** Your real per-bottle costs are hardcoded in the app and used correctly in every show P&L. What is broken is that you cannot see or edit them, and break-even ignores them and uses a flat 30% guess.

**The one that changes your decisions: your price table is stale.** You collected 21% MORE money than the app thinks your product sells for, every single day at WCF. Until the prices match what you actually charge, the capture gauge, cash checks, and per-unit stats are noise.

Everything below is ranked. Nothing has been fixed yet. **You pick, I fix.**

---

## THE FOUR APPS (INVENTORY)

All four live apps are generated from ONE codebase, so one audit covers all four. Isaiah's and Anthony's are byte-identical except for the name. I verified this with a diff.

```
1. best-solution-app (Froggy's personal app)
   BEST_SOLUTION_APP.html ........ 4,149 lines. THE app: Home dashboard, Stock, Shows w/ daily
                                   counts + money + expenses, Reps + day pay, Calendar, Supplies,
                                   P&L, Settings, Supabase cloud sync. Seeded with your real 2026
                                   season and 2025 history.
   index.html .................... 13 lines. Redirect stub to the file above. Fine.
   planner.html .................. 573 lines. Separate printable "2026 Event Planner" document
                                   (light theme, print styles). Static content, no data link to the app.
   BEST_SOLUTION_APP_BLANK.html .. 2,702 lines. ⚠️ A STALE OLD COPY of the app, still live at its
                                   public URL, with the old math. Should be a redirect (see finding 14).

2. best-solution-blank (Batman)
   index.html .................... 4,055 lines. Same core app PLUS Batman-only features Froggy's app
                                   does not have: freight/shipping ledger, EDITABLE per-product costs
                                   (setCost/getCost), master vs at-show inventory split, transfer
                                   nodes, an audit bar, and a mini calendar.
   guide.html .................... 168 lines. Plain-English how-to guide. Good.
   BEST_SOLUTION_APP_BLANK.html .. 18 lines. Proper redirect stub to index.html. Good.
   README.md ..................... 2 lines. Fine.

3. best-solution-isaiah
   index.html .................... 3,680 lines. Crew copy, empty data, storage slug "isaiah".

4. best-solution-anthony
   index.html .................... 3,680 lines. Byte-identical to Isaiah's except name/slug.

Source workspace: greco-household/best-solution/
   froggy-personal.html .......... The rebuild "master" (4,272 lines). ⚠️ Has features the live app
                                   does NOT have (crew launcher, pre-show calculator markers), and
                                   the live app has newer work this master lacks. The "one master,
                                   generated blanks" pipeline is broken by drift (finding 15).
   gen_blank.py .................. Generator that builds the 3 blanks from the master.
   batman/isaiah/anthony html .... Generated blanks (older than what is live).
   deploy/ ....................... The 4 files deployed to the live repos on Jul 26 (this session).
   HANDOFF.md, README.md ......... Docs.

Supabase (project ylotwhvkrlobrpdmngul "froggy-money"):
   app_data .......... 17 rows, RLS ON, keyed by user + data_key. Your bs_state (32 shows, synced
                       this morning), Batman bs_state_blank (4 shows), Isaiah + Anthony rows exist
                       (0 shows), plus your household-app keys. Crew sync is provisioned and working.
   blank_app_state ... 1 row. The OLD no-login shared model. Batman's old cloud copy lives here.
   app_state ......... 0 rows. Unused leftover.
   app_items ......... 130 rows. Used by the household app, not Best Solution.
```

**None of the four apps is missing, empty, or broken.** All four parse cleanly (I verified all inline scripts with Node).

---

## HOW I PROVED THE MATH

I did not eyeball formulas. I extracted the live app's JavaScript, ran it in Node with a stubbed browser, injected your REAL Washington County Fair data pulled read-only from your Supabase cloud row, and compared the app's outputs against my own independent recomputation, line by line. The full side-by-side table is in **BS_MATH_VERIFICATION.xlsx**, with a worked WCF example tab.

Washington County Fair, days 1 through 5 (day 6 was in progress at audit time):

| Number | App says | Independent recompute | Verdict |
|---|---|---|---|
| Money collected (gross) | $6,086.00 | $6,086.00 | MATCH |
| Units sold value at full price | $5,015.00 | $5,015.00 | MATCH |
| COGS | $1,652.00 | $1,652.00 | MATCH |
| Card sales (Square+Debit) | $2,927.00 | $2,927.00 | MATCH |
| Gas estimate | $117.26 | $117.26 | MATCH |
| Inventory identity (packed 746 = booth 384 + restocks 362) | holds | holds | MATCH |
| Day-to-day count continuity | 0 breaks | 0 breaks | MATCH |
| **Show profit** | **$3,785.60** | **$3,571.53** | **OFF by $214.07** (fees + gas + booth, see findings 1, 2, 6) |

Your counting discipline at WCF was excellent. The identity morning + restock − evening = sold holds perfectly across all 5 days, and your two count mistakes (Jul 21 evening, Jul 25 evening) were caught and corrected using the app's own unlock-with-reason flow. That system works.

---

## FINDINGS

Severity: **P0** = numbers are wrong or data can be lost. **P1** = leads to bad decisions or wasted time. **P2** = friction and confusion. **P3** = polish.

---

### FINDING 1 | SEVERITY: P0
**What is wrong:** Card processing fees are NEVER deducted. The Settings screen has a "Square Fee %" field (set to 3%) that is not used by a single calculation. It is a dead knob.
**Where exactly:** `BEST_SOLUTION_APP.html` line 345 (setting exists), line 3805 (UI edits it), `calcShow()` line 1106 (never reads it).
**Why it matters:** Every dollar of Square/card money is booked as if you keep 100% of it. You do not.
**Dollar impact:** WCF alone: 3% x $2,927 = **$87.81** missing so far. Season to date, roughly 3% of ALL card sales, likely a few hundred dollars.
**The fix:** In `calcShow()`, add `fees = cardSales x sqFee` to expenses, show it as its own line in the show P&L.
**Effort:** Hours.

### FINDING 2 | SEVERITY: P0
**What is wrong:** Gas is in break-even but NOT in profit. `calcBreakEven()` includes the computed gas cost. `calcShow()` (the profit number) only counts gas if you manually open the Day Expenses modal and save it, and at WCF every day's gas is $0. Two different answers to "did I make money."
**Where exactly:** `calcShow()` line 1106 (no gas), `calcBreakEven()` line 2199 (includes gas), `showExpModal()` line 3145 (pre-fills the estimate but only saves if you open it).
**Why it matters:** You drive home every night. A 6-day show at 38 miles one-way is 456 miles of real cost that profit ignores.
**Dollar impact:** WCF: **$117.26** missing from profit (456 mi at 17.5 MPG and $4.50/gal). Every show with miles entered has this gap unless you hand-logged gas.
**The fix:** Include `showGas(sh)` in `calcShow()` automatically, and skip it when day-level gas was manually entered so it never double counts.
**Effort:** Hours.

### FINDING 3 | SEVERITY: P0 (needs your answer before fixing)
**What is wrong:** Sales tax is treated as your money. Collected payments include whatever tax you charged; nothing splits out what belongs to the state of Wisconsin. There is a "Sales Tax" category in show expenses, but nothing is logged there and nothing computes it.
**Where exactly:** `showActualRev()` line 1136 (all collected money = revenue), `SHOW_EXP_CATS` line 2211 (a manual category only).
**Why it matters:** If your prices are tax-inclusive, part of the $6,086 collected at WCF is owed to the WI DOR and is not revenue.
**Dollar impact:** If WCF prices include 5.5% tax: roughly **$317** of the WCF money is not yours. Season-wide this is thousands.
**The fix:** I need one answer from you: **do your booth prices include sales tax, and at what rate do you file?** Then I add a per-show tax rate that splits collected money into revenue vs tax owed, with a running "tax owed to state" total.
**Effort:** Hours, once you answer.

### FINDING 4 | SEVERITY: P0
**What is wrong:** Two ways to silently lose inventory or sales data.
(a) `endShow()` returns only the LAST evening count to master stock. Packed units that never got counted into a day (still in the truck) vanish from master inventory forever. At WCF this reconciled perfectly, but only because you restocked everything into the booth. A show where you bring 300 and only ever count 200 into the booth will eat 100 units on close.
(b) Cloud sync is last-write-wins on the WHOLE state. Two devices editing offline (you on the phone, someone on the tablet), the later save wins and the earlier device's entries are gone. There is a local backup (last 3), so it is recoverable if caught, but nothing warns you.
**Where exactly:** `endShow()` line 3182, `cloudHydrate()` line 4065, `cloudPush()` line 4028.
**Why it matters:** These are the only two paths I found where entered data can disappear without a warning.
**Dollar impact:** Unbounded when it hits. Zero if it never does.
**The fix:** (a) On end-show, return `packed + restocks not consumed`, not just last evening count, and show a "returning N units" confirmation with the math. (b) At minimum, warn when adopting a cloud copy would discard newer local day entries; proper day-level merge is a bigger project.
**Effort:** (a) hours. (b) warning: hours; true merge: a real project.

### FINDING 5 | SEVERITY: P0 (needs your answer before fixing)
**What is wrong:** The app's price table does not match what you actually charge. Every WCF day collected 20 to 22% MORE than the sold units are worth at app prices ($6,086 vs $5,015, a **$1,071** gap in 5 days). The cash check said "over" all 5 days, and the Collected vs Full Price gauge reads over 100%, which makes both meaningless.
**Where exactly:** `S.prices` seeded at line 344 (32oz $22.50, 16oz $15, 8oz $10, 2oz $5, C5S $10, C5L $20), used by `calcRev()` line 1091 everywhere.
**Why it matters:** Potential revenue, discounts detection, cash-drawer check, per-unit stats, and the capture gauge all price units at these numbers. Wrong prices = every one of those is noise.
**Dollar impact:** No cash is lost, but a 21% distortion sits on every analytical number.
**The fix:** Tell me **what you actually charged at WCF per size** (and whether that includes tax, see finding 3). If prices vary by show, the fix is a per-show price override; if you simply raised prices, it is a 2-minute Settings update, no code at all.
**Effort:** Minutes to hours depending on your answer.
**One more thing:** changing a price in Settings silently re-prices HISTORY too (`calcRev` always uses current prices). Past shows' potential revenue changes retroactively. The fix is to snapshot prices onto each show when it starts.

### FINDING 6 | SEVERITY: P1
**What is wrong:** Booth expense uses the sticker price, not what you actually paid. WCF: you paid **$589** (logged), app books **$580**. Pewaukee: you paid $425 of $450; the completed show books $450.
**Where exactly:** `calcShow()` line 1107 uses `sh.boothCost`; `boothPaid()` line 1247 knows the truth.
**Dollar impact:** $9 under at WCF, $25 over at Pewaukee. Small dollars, but it means the expense line cannot be tied to your bank statement.
**The fix:** Book `max(boothCost, boothPaid)` for completed shows, or add a visible "paid vs cost" delta line so overpays and unpaid balances are explicit.
**Effort:** Hours.

### FINDING 7 | SEVERITY: P1
**What is wrong:** Debit money disappears from the payment breakdown. `calcYTD()` initializes the payment totals WITHOUT a debit key, so debit sums into `undefined`, becomes NaN, and every display that reads it falls back to $0.
**Where exactly:** line 1215: `let pmtTotals={cash:0,square:0,venmo:0,paypal:0,cashapp:0,zelle:0};` (no `debit`). I proved it in the harness: added $256 of debit, gross went up, the split section total did not move.
**Why it matters:** You have **$256 of real debit money right now** that the Payment Breakdown section pretends does not exist, and every percentage in that section is computed against the wrong total. (Gross/profit are NOT affected; they sum payments correctly elsewhere.)
**Dollar impact:** $256 invisible today; grows with every debit sale.
**The fix:** One line: add `debit:0` to the initializer.
**Effort:** Minutes. This is the cheapest real fix in the whole audit.

### FINDING 8 | SEVERITY: P1
**What is wrong:** Break-even is a guess wearing a suit. `calcBreakEven()` = fixed costs / (1 − 0.30), a hardcoded "COGS is about 30% of sales" from the 2025 average. Your ACTUAL WCF ratio is **27.1%**. It also excludes card fees and any rep pay not yet entered, and it answers only in dollars, never units.
**Where exactly:** `calcBreakEven()` line 2199 (the `0.30` literal is line 2209). Shown on every show card at line 2229.
**Dollar impact:** WCF break-even shown about $1,039; with your real product mix it is about $998, and with fees included about $1,031. Wrong in both directions depending on the show.
**The fix:** Use the show's own COGS ratio (from its packed mix, falling back to season actuals), include card fees at the season card ratio, and display "$X or about N units" using the show's average unit price.
**Effort:** Hours.

### FINDING 9 | SEVERITY: P1
**What is wrong:** COGS is invisible and locked in Froggy's app. Your real unit costs ARE in the code (32oz $6.00, 16oz $4.50, 8oz $4.00, 2oz $2.25, C5S $3.00, C5L $6.00) and used correctly, but you cannot see them or change them anywhere in the UI. **Batman's app already has the fix**: editable per-product costs (`setCost`/`getCost`) with defaults. Your app never got that feature. Also: no bundle pricing exists (a "2 for $18" deal just shows up as a cash-check "short/over").
**Where exactly:** `SKUS` line 265 (hardcoded), Batman's `index.html` lines 487, 492, 3785 (the editable-cost feature to port).
**Why it matters:** When Mark Martone's pricing changes or you buy a different size run, your COGS silently stays wrong until someone edits source code.
**The fix:** Port Batman's cost editor into the shared codebase (all 4 apps get it). Bundle pricing is a separate design decision, tell me if you actually sell bundles.
**Effort:** Hours.

### FINDING 10 | SEVERITY: P1
**What is wrong:** Labor cost is $0 until you remember to type it. Ronny worked WCF all week; until day pay is entered, profit pretends he is free. The day closeout flow does prompt for it, but it is skippable and nothing flags "5 staffed days, $0 pay entered."
**Where exactly:** `repDayPay()` line 1268, `calcShow()` includes only entered amounts; `openCloseout()` line 3012 has the prompt.
**Dollar impact:** Whatever you owe Ronny for 5 days, invisible in the current $3,785.60 "profit."
**The fix:** A red "staffed day, no pay entered" badge on any day with assigned reps and money logged but `repPay` empty, plus a nightly nag in closeout.
**Effort:** Hours.

### FINDING 11 | SEVERITY: P1
**What is wrong:** The app's clock runs on London time. `_todayKey()` and `_stamp()` use `toISOString()`, which is UTC. From 6 or 7pm Central onward, "today" is tomorrow.
**Where exactly:** `_todayKey()` line 1146, `_stamp()` line 2616.
**Why it matters:** A planned show flips to "Missed / Did Not Do" on the evening of its own last day while you are still in the booth (active shows are protected, but planned ones are not). Evening CSV exports and backups get tomorrow's date.
**Dollar impact:** No dollars, but false "missed" states and mislabeled files cost trust and time.
**The fix:** One local-date helper used in both places.
**Effort:** Minutes.

### FINDING 12 | SEVERITY: P1
**What is wrong:** A day with money but no evening count books revenue with ZERO COGS. `calcShow` only counts COGS on days where BOTH counts exist. Log $800 of payments, skip the evening count, and the app shows $800 of pure profit for the day.
**Where exactly:** `calcShow()` line 1109 (`if(d.morningCount&&d.eveningCount)` gate).
**Dollar impact:** WCF day 6 is in this state right now (day open, $0 logged yet, count pending). Any historical day with payments and missing counts overstated profit by that day's entire COGS.
**The fix:** A warning chip on any day with payments > 0 and missing counts: "profit for this day ignores product cost until you count."
**Effort:** Hours.

### FINDING 13 | SEVERITY: P2
**What is wrong:** On the Home active-show banner, the tile labeled "Potential" actually displays COLLECTED money (`t.gross`), the same number as the tile next to it labeled "Collected."
**Where exactly:** `rHome()` line 1434 (`fmt(t.gross)` under the label "Potential"; should be `t.potential`).
**The fix:** One word.
**Effort:** Minutes.

### FINDING 14 | SEVERITY: P2
**What is wrong:** An old copy of the app with the OLD math is still live: `best-solution-app/BEST_SOLUTION_APP_BLANK.html` (2,702 lines, pre-overhaul). The blank repo got a proper "this is an old copy" redirect; this one never did. Anyone with the old bookmark is running retired math.
**The fix:** Replace it with the same 18-line redirect stub used in the blank repo.
**Effort:** Minutes.

### FINDING 15 | SEVERITY: P2
**What is wrong:** The "ONE codebase" rule is broken. The rebuild master (`greco-household/best-solution/froggy-personal.html`) has features the live app lacks (Crew Apps launcher, pre-show calculator markers), and the live apps have newer work the master lacks (the July day-pay overhaul was built on live main, not the master). Right now there are effectively TWO masters.
**Why it matters:** The next "make a change and regenerate the blanks" will silently undo live features.
**The fix:** Declare the deployed live code the master, regenerate the greco-household copies from it (or retire them), and update HANDOFF.md.
**Effort:** Hours.

### FINDING 16 | SEVERITY: P2
**What is wrong:** Double-tap can double-log on every list-append save: show expenses, booth payments, rep payments logged, discounts, transfers, other expenses. The modals close on success, which mostly protects you, but a slow tap or laggy phone can fire twice before the close.
**Where exactly:** `addShowExp` 2337, `saveBoothPmt` 3231, `saveRepPmt` 3755, `saveDiscount` 2548, `saveTransfer` 2582, `saveOtherExpense` 3262.
**The fix:** Disable the button on first tap. Counts and payments are safe (they overwrite, not append).
**Effort:** Minutes each.

### FINDING 17 | SEVERITY: P3
**What is wrong:** Money lives in floating point. Every amount is a JS float; display rounds to cents at the end. I measured the worst case: errors stay far below one cent for your volumes (0.1+0.2 style dust), and the $0.50 tolerance in the cash check absorbs it. This is a "someday, if ever" cleanup to integer cents, not a today problem. Rounding happens once at display, which is the right place.
**Effort:** A real project. Not recommended now.

### FINDING 18 | SEVERITY: P3
**What is wrong:** Divide-by-zero and blank-input handling are actually GOOD. I checked every average and percentage: `avgShowProfit`, per-hour, per-mile, keep %, payment % are all guarded. Blank number fields consistently become 0 via `parseFloat(x)||0`, which is "silent zero" by design; the one place it misleads is finding 12. No fix needed beyond that.

---

## USABILITY AUDIT (the four personas)

The app is one page with 8 tabs: **Home, Stock, Shows, Reps, Calendar, Supply, P&L, Setup.** All data entry is modals. Feedback is toast messages, which is good: every save visibly confirms.

**Screen: Home.** For the owner: strong. Active show banner with live numbers, next up, season stats, section grid, quick actions. Primary action (open active show) is obvious in 2 seconds. Problem: TWELVE stat boxes of near-equal size fight for attention, and no single number answers "am I winning this year." See redesign proposal.

**Screen: Show detail.** This is the workhorse and it is dense: pre-show pack, per-day grid, reconciliation, reps, supplies, expenses, exports. For a stranger, the day grid needs no manual, which is a win. Break-even chip is dollars only (finding 8). Edit/undo exists everywhere via unlock-with-reason. Strong screen, slightly overloaded.

**Screen: Day view (the booth screen).** This is where Isaiah lives, and it is the weakest for him:
- **Logging money = typing running totals per payment method.** There is no "+1 sale" action. Mid-day, adding a $20 cash sale means: know the current cash total, add 20 in your head, retype it. That is mental math with a customer standing there, exactly what you said is a defect. Current: 3 taps + arithmetic + typing. Ideal: 2 taps (tap "cash," tap "$20 preset"). **This is friction point #1** and one of my two redesign screens.
- Counts are excellent: steppers, previous-evening prefill, continuity warnings, lock.
- Offline: everything saves to the device instantly (localStorage first), cloud syncs when signal returns. **No data is lost offline.** Verified in code. The status text is subtle though; a crew member cannot easily tell "saved locally, will sync later" from "synced."

**Screen: Stock.** Clear. Steppers + set-all + restock. Cannot go negative anywhere (all writes clamp at 0, verified). Batman-borrow tally is correctly walled off from P&L (verified in code comments and math).

**Screen: Reps.** Day-pay model is simple and the earned/paid/owed math verifies to the penny (`repShowPay` correctly prefers day entries and never double counts legacy payouts, I traced all three fallback tiers). Weakness is finding 10: nothing shouts when pay was never entered.

**Screen: P&L.** Honest and reconciles: season total = sum of show P&Ls plus other expenses, no double counting (I traced completed vs planned paths; they are disjoint). Quarterly tax estimate splits the reserve evenly, labeled as an estimate. Good.

**Screen: Calendar / Supply / Setup.** Functional, no math issues. Supply auto-bags (1 lacy bag per unit sold at $0.20) plus flat $30 candy/paper per show flows into show P&L correctly (verified: $68.40 at WCF = 192 units x $0.20 + $30).

**Crew apps for the crew personas:** identical UX, empty data, so everything above applies. Isaiah's and Anthony's cloud rows exist and sync (verified in Supabase). Batman's extra features are HIS app only, so the crew experience is inconsistent across the team (finding 15 relative).

### Top 10 friction points, worst first

1. **No quick-sale entry in the booth** (running-total mental math). Cost: seconds per sale x hundreds of sales, plus wrong totals when arithmetic slips = the #1 source of "cash short" noise.
2. **Rep pay silently $0 until typed** (finding 10). Cost: profit wrong by a labor week at a time.
3. **Price table stale** (finding 5). Cost: every analytical readout distorted 21%.
4. **Break-even not in units** (finding 8). "Sell 89 more units" is actionable in a booth; "$1,039" is not.
5. **Gas/fees missing from profit** (findings 1, 2). Cost: $200+ per big show of phantom profit.
6. **12 equal stat boxes on Home.** Cost: 30 seconds of hunting every time you open the app.
7. **Sync state ambiguity on bad wifi.** Cost: crew re-enters data that already saved, or panics.
8. **Sales tax invisible** (finding 3). Cost: a surprise bill at filing time.
9. **Old app copy still reachable** (finding 14). Cost: someone runs retired math.
10. **Double-tap dupes on list saves** (finding 16). Cost: occasional phantom expense you must find and delete.

---

## VISUAL AND FEEL AUDIT

- **Hierarchy:** the biggest number on Home is 28px; body text runs 9 to 12px with FIFTY+ uses of 9 and 10px. The most important number of each screen does not dominate. Recommendation: one hero number per screen at 34 to 40px, everything else two clear steps down.
- **Touch targets:** buttons (44px tall) and steppers (38px) are fine. The bottom nav labels are **8px font**, borderline in a hurry. Recommendation: 10px labels, larger icons.
- **Outdoor readability:** gold-on-near-black is high contrast and honestly reads well in sun, but muted gray `#8a8a8a`-class text at 9 to 10px will wash out. Recommendation: bump muted text one shade lighter and 1px bigger app-wide. One CSS variable change.
- **Color meaning:** consistent and correct. Green = money in/good, red = money out/alert, gold = brand/action. The reconciliation dot system (green/yellow/red) is genuinely great.
- **Typography scale:** currently ~12 ad-hoc sizes. Recommendation: collapse to 5 steps (9 is too small to keep at all).
- **Density:** Show detail and Home are cramped; Calendar and Stock breathe fine.
- **Consistency across the 4 apps:** identical design system (same generated code), so they feel like one product. Exceptions: Batman's extra sections, and planner.html which is a deliberately different print document (fine).
- **Loading/saving states:** local saves are instant with toasts, good. Cloud states exist ("Syncing/Synced/error") but are buried in Settings. Recommendation: a tiny persistent sync dot in the header.
- **Delight, two ideas:** (1) when a show's collected passes break-even, fire a one-time confetti burst and a "BOOTH PAID FOR 🎉" toast; (2) when a day beats your best-ever day, say so at closeout. Cheap, and they hit exactly when you feel good anyway.

---

## WHAT I NEED FROM YOU (blockers, per your rule "never guess")

1. **Finding 3:** Do your booth prices include sales tax? What rate do you file at?
2. **Finding 5:** What did you actually charge per size at WCF? Did prices change for the season?
3. **Finding 9:** Do you sell bundles ("2 for $X")? If yes, which combos and prices?
4. **Ronny's day rate** for WCF so the labor gap can be quantified and entered.

---

*Companion files: BS_MATH_VERIFICATION.xlsx (full formula table + WCF worked example), BS_FIX_PLAN.md (ranked fixes), BS_REDESIGN_PROPOSAL.md (two worst screens).*
