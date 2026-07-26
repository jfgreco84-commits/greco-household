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
   (qty × price) and **potential over product cost** (volume − COGS), plus
   units and cost of goods — before you log a single count. Falls back to the
   packed inventory if you haven't entered a separate plan.
3. **Collected vs Full Price — redesigned** — a modern capture-rate gauge (big %
   + gradient bar) over per-show cards with mini progress bars, replacing the old
   plain list.
4. **Master Inventory button** — now the first and biggest control on Home: a
   full-width gold hero button above everything else.
5. **Rep pay is per day (Jul 2026)** — commission percentages are GONE, and so
   is per-rep sales tracking. The day's money is ONE total (the Money column),
   and each rep gets a flat dollar amount per day, entered daily (💵 Day Pay on
   the day screen, the day closeout, or per rep from the show's rep list — all
   write `day.repPay`). The app tracks earned vs paid vs owed from those day
   entries. Legacy data (`sh.repPayout` payouts, old `d.repSales`) is still
   read on old shows so history reconciles.

## Personal-app-only

- **Crew Apps launcher** (`froggy-personal.html` only): a "Crew Apps · Team
  Tracker" card with three new-tab buttons — Batman (live URL wired up), Isaiah
  and Anthony (placeholders). Update the two placeholder `href="#"` values once
  those repos go live — search the file for `ISAIAH_URL` and `ANTHONY_URL`.

## What "blank" strips from the master

`gen_blank.py` removes Froggy's personal data while keeping every feature:
seeded inventory → 0, 2025 history → empty, prior-year comparison → 0, product
debt → empty, the named "Borrowed from Batman" dashboard card, the seeded crew
roster (replaced with a single owner rep named for that app), and the Crew Apps
launcher. To regenerate the blanks after editing the master:

```
python3 gen_blank.py
```
