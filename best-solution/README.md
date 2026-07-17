# Best Solution — App Rebuild (4 apps)

All four apps share **one codebase** (App 1 is the master). The three blank/crew
copies are generated from the master with `gen_blank.py`, so they stay
feature-identical — only the seeded personal data differs.

## The four apps

| File | Owner | Status | Deploy target |
|------|-------|--------|---------------|
| `froggy-personal.html` | Froggy (Justin) | Master — keeps all personal data | `best-solution-app` repo → `BEST_SOLUTION_APP.html` |
| `batman-blank.html` | Batman | Blank (keeps Batman's existing local data via storage key `dd_bs_blank_*`) | `best-solution-blank` repo → `index.html` |
| `isaiah-wojo.html` | Isaiah Wojo | Completely empty | **new** repo, e.g. `best-solution-isaiah` → `index.html` |
| `anthony-wojo.html` | Anthony Wojo | Completely empty | **new** repo, e.g. `best-solution-anthony` → `index.html` |

Each app uses its own `localStorage` namespace (`dd_bs_<slug>_v7`) and its own
Supabase cloud `data_key` (`bs_state_<slug>`), so no two apps ever collide —
even in the same browser or signed into the same account.

## What changed across all 4 apps

1. **Dashboard stats, front and center** — at the very top of Home, in this exact
   order: Total Sales Volume, Total Booth Rents, Total Other Expenses, Total Tax
   Reserve, Total COGs, Total Profit, Avg Show, Biggest Show, Avg Show Profit, Net.
   They reconcile by construction: `Sales − COGS − Booth − Other = Profit`,
   `Profit − Tax = Net`.
2. **Pre-show inventory calculator** — a card near the top of every show entry.
   Enter the stock you're bringing and it projects **potential sales volume**
   (qty × price) and **potential commission** (at the default 30% rate), plus
   units and cost of goods — before you log a single count. Falls back to the
   packed inventory if you haven't entered a separate plan.
3. **Collected vs Full Price — redesigned** — a modern capture-rate gauge (big %
   + gradient bar) over per-show cards with mini progress bars, replacing the old
   plain list.
4. **Master Inventory button** — now the first and biggest control on Home: a
   full-width gold hero button above everything else.

## Dashboard redesign + new features (v7.4)

Made in the master and regenerated into all blanks. All apps get these.

1. **Home dashboard reordered around tracking, not stats.** New top-to-bottom order:
   1. 🔔 **Notification / audit bar** (see below) — pinned at the very top.
   2. ⭐ **Quick Access** — the four most-used buttons: **Stock, Shows,
      Borrowed from Batman, Product Debt**. (Batman is personal — stripped from blanks.)
   3. 🔴 **Happening Now** — every active show, no cap; if two or more run at once
      they ALL show, with a staffing warning.
   4. 🎪 **On Deck** — the next few upcoming shows with a TODAY / TOMORROW / in-N-days chip.
   5. 📅 **This Month calendar** — a live mini month grid right on the dashboard
      (double-booked days flagged), taps through to the full calendar.
   6. 📊 **Season Performance Stats** — all the completed-season numbers, now
      **collapsed behind a Show/Hide button** so they're out of the way.
   7. Dashboard Sections grid, Crew Apps (personal only), Quick Actions.
   8. 🧮 **The Bottom Line** — a fully reconciled Sales → COGS → Booth → Freight →
      Other → Profit → Tax → **NET** card, pinned at the very bottom.
2. **Constant audit + notifications.** `runAudit()` scans on every render and never
   changes data — it only reports. Red = fix now, gold = review. Catches: inventory
   mismatches, impossible counts, broken stock values, unpaid booths on shows coming
   up, low stock, double-booked days, unconfirmed shows, reps owed, missed shows. The
   top bar shows a live count and expands to a tap-to-jump list.
3. **Editable cost of goods (COGS).** `S.costs` + `getCost(k)` (falls back to each
   SKU's built-in default). Edit the polish sizes and C5 costs in **Settings →
   Cost of Goods**, or tap **Adjust cost of goods** on any Stock card. Drives every
   COGS/profit number live, same model as prices.
4. **Freight & shipping ledger.** `S.freight` + a full manage/add/edit/delete modal
   (`openFreight` / `secFreight`), its own **🚚 Freight & Shipping** dashboard section,
   and a **Log Freight** quick action. Totals roll into Other Expenses / P&L / the
   bottom line but stay on their own line.

## Personal-app-only

- **Crew Apps launcher** (`froggy-personal.html` only): a "Crew Apps · Team
  Tracker" card with three new-tab buttons — Batman (live URL wired up), Isaiah
  and Anthony (placeholders). Update the two placeholder `href="#"` values once
  those repos go live — search the file for `ISAIAH_URL` and `ANTHONY_URL`.
- **Borrowed from Batman** now lives as a Quick Access button (was a dashboard
  section card). It's gated by `/*BATMAN_BTN_START*/…/*BATMAN_BTN_END*/` markers
  that `gen_blank.py` strips from the blanks.

## What "blank" strips from the master

`gen_blank.py` removes Froggy's personal data while keeping every feature:
seeded inventory → 0, 2025 history → empty, prior-year comparison → 0, product
debt → empty, the named "Borrowed from Batman" dashboard card, the seeded crew
roster (replaced with a single owner rep named for that app), and the Crew Apps
launcher. To regenerate the blanks after editing the master:

```
python3 gen_blank.py
```
