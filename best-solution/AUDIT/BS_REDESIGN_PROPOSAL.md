# REDESIGN PROPOSAL, THE TWO WORST SCREENS
One page. Words plus simple wireframes. **Nothing is built yet.**

---

## Screen 1: The Day view money entry (Isaiah's screen)

**The problem.** Money is entered as running totals per payment method. Adding one $20 cash sale mid-day means: remember the current cash total, add 20 in your head, retype the whole number. One-handed, in the sun, with a customer waiting, that is arithmetic homework. It is also the #1 generator of "cash short/over" noise.

**The idea.** Keep the totals (they are the source of truth), but add sales instead of retyping them. One big ADD SALE button opens a two-tap flow: tap the method, tap the amount. Preset amount chips come from YOUR price list, because almost every sale is one of six numbers or a simple combo.

```
+--------------------------------------------------+
|  DAY 3 · Jul 23           🟢 counts reconciled   |
|                                                  |
|          TODAY SO FAR:  $1,315                   |
|      cash $605 · square $710 · other $0          |
|                                                  |
|  +--------------------------------------------+  |
|  |            💵  ADD SALE  (big, gold)       |  |
|  +--------------------------------------------+  |
|                                                  |
|  [🌅 Morning count ✓]   [🌙 Evening count  ]     |
|  [±  Restock/Lost   ]   [💸 Day expenses   ]     |
|  [💰 Fix totals     ]   [🌙 Close out day  ]     |
+--------------------------------------------------+

ADD SALE sheet (two taps and done):
+--------------------------------------------------+
|  How were you paid?                              |
|  [💵 CASH]  [⬛ SQUARE]  [💳 DEBIT]  [more...]   |
|                                                  |
|  How much?                                       |
|  [$5] [$10] [$15] [$20] [$22.50] [$25]           |
|  [$30] [$40] [custom______]                      |
|                                                  |
|  CASH  +$20   ->  today's cash: $625             |
|  [    UNDO LAST SALE    ]                        |
+--------------------------------------------------+
```

- Every added sale appends to a tiny in-day log, so **UNDO LAST SALE** is one tap (fixes the "no undo" defect at the moment it matters most).
- "Fix totals" keeps the old modal for corrections, so nothing you know today goes away.
- Works offline exactly like everything else (saved locally instantly).
- Bonus: the sale log gives per-hour sales for free, which feeds "best hour" stats later if you ever want them.

---

## Screen 2: Home dashboard (your screen)

**The problem.** Twelve near-equal stat boxes. No single number answers "am I actually winning this year" in one glance, and the number you care most about (what you KEEP) sits in a same-size box labeled CLEAN P.

**The idea.** One hero number: **KEEP** (completed net minus tax reserve, minus overhead shown right below it so the honesty is visible). Everything else demotes into three labeled rows that match how you actually think: Money, Shows, Work. The section grid and quick actions stay as they are.

```
+--------------------------------------------------+
|  🔴 ACTIVE: Washington County Fair    -> open    |
|  collected $6,086 · profit $3,572 · day 6/6      |
|                                                  |
|  2026 SO FAR, YOURS TO KEEP                      |
|          $ 12,4XX        (40px, green)           |
|  after COGS, fees, gas, tax reserve, overhead    |
|  ── progress vs 2025 ($9,088) ────────█────░──   |
|                                                  |
|  MONEY   gross $XX,XXX · tax set-aside $X,XXX    |
|  SHOWS   9 done · avg profit $XXX · best: WCF    |
|  WORK    XX days · XXX hrs · $XX/hr              |
|                                                  |
|  [ MASTER INVENTORY  (gold hero button) ]        |
|  [ section grid, unchanged ]                     |
|  [ quick actions, unchanged ]                    |
+--------------------------------------------------+
```

- The "vs 2025" progress bar is the delight moment: you beat $9,088 last year; watching the bar close on it is the reason to open the app after a good show.
- The hero number only becomes honest AFTER the profit-truth fixes (fees, gas, rep pay, tax) land. Sequence matters: fix the math first, then promote the number.

---

**Which fixes do you want me to implement?**
