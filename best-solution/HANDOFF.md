# HANDOFF — Best Solution App Rebuild

> **⚠️ RETIRED (Jul 26 2026):** deployment is done and v8.0 audit fixes shipped. The live source of truth is now `best-solution/live/`. This handoff is kept for history only. Do not run gen_blank.py against these files.

**Read this top to bottom. It contains everything needed to finish and ship the work.**
Generated from a Claude Code web session. The main remaining work is **deployment**,
which the web session could not do (its GitHub access was scoped to one repo only).
On a home PC with full `gh` auth, you can finish it.

---

## 0. TL;DR — what's done vs. what's left

**DONE (committed & pushed):**
- All 4 apps built and verified, on branch `claude/best-solution-rebuild-2ayf4w`
  in repo `jfgreco84-commits/greco-household`, folder `best-solution/`.
- Draft PR: https://github.com/jfgreco84-commits/greco-household/pull/1
- All 5 requested feature changes implemented across all apps.

**LEFT TO DO (this is your job, next thread):**
1. Deploy each of the 4 HTML files to its GitHub Pages repo (2 existing, 2 new).
2. Create the two new repos (Isaiah, Anthony) and enable Pages.
3. Put the two real URLs into the personal app's "Crew Apps" launcher and redeploy it.
4. (Verify) Supabase cloud sync works for the crew apps — see §7.
5. Merge PR #1 (or keep the source-of-truth in `greco-household`, your call — see §8).

---

## 1. Where everything lives

- **Repo:** `jfgreco84-commits/greco-household`
- **Branch:** `claude/best-solution-rebuild-2ayf4w`
- **Folder:** `best-solution/`

| File | Owner | State | Final deploy target |
|------|-------|-------|---------------------|
| `froggy-personal.html` | Froggy (Justin) | **master** — keeps all his real data | repo `best-solution-app`, filename `BEST_SOLUTION_APP.html` |
| `batman-blank.html` | Batman | blank (keeps Batman's existing local data) | repo `best-solution-blank`, filename `index.html` |
| `isaiah-wojo.html` | Isaiah Wojo | completely empty | **NEW** repo (e.g. `best-solution-isaiah`), filename `index.html` |
| `anthony-wojo.html` | Anthony Wojo | completely empty | **NEW** repo (e.g. `best-solution-anthony`), filename `index.html` |
| `gen_blank.py` | — | generator: builds the 3 blanks from the master | keep in `greco-household` only |
| `README.md` | — | short overview | keep |
| `HANDOFF.md` | — | this file | keep |

Current live URLs (before your deploy):
- App 1 (Froggy): https://jfgreco84-commits.github.io/best-solution-app/BEST_SOLUTION_APP.html
- App 2 (Batman): https://jfgreco84-commits.github.io/best-solution-blank/

---

## 2. Architecture — ONE codebase, generated blanks

There is **one source of truth: `froggy-personal.html` (the master)**. The other
three apps are **generated** from it by `gen_blank.py`, which strips personal data
but keeps every feature. This is why the apps are guaranteed feature-identical.

**Golden rule:** make feature changes in `froggy-personal.html`, then run
`python3 gen_blank.py` to regenerate the three blanks. Never hand-edit the blanks.

```
cd best-solution
python3 gen_blank.py      # rewrites batman-blank.html, isaiah-wojo.html, anthony-wojo.html
```

The blanks regenerate **byte-identical**, so the generator is deterministic.

---

## 3. What `gen_blank.py` strips/changes for each blank

(So you understand it and don't accidentally undo it.)
- Seeded inventory → all zeros.
- The entire personal `applyOneTimeUpdates()` (restocks, specific 2026 shows,
  Mark Martone debt seeding, hard audits, the seeded crew roster) → replaced with
  a minimal generic version that only seeds structural fields + a **single owner rep**
  named for that app (`Batman` / `Isaiah` / `Anthony`).
- `SHOWS_2025` historical array → `[]`.
- `PREV_YEAR` prior-year comparison → all zeros (its card hides itself).
- `productDebt` → empty supplier, 0 balance (the Product-Debt feature stays).
- The named **"Borrowed from Batman"** dashboard card → removed (personal).
- The **Crew Apps launcher** → removed (personal app only).
- "Rep-only show — Justin not attending" → "…owner not attending".
- Storage isolation: `dd_bs_` → `dd_bs_<slug>_`, and cloud `data_key`
  `'bs_state'` → `'bs_state_<slug>'`. Slugs: Batman=`blank`, Isaiah=`isaiah`,
  Anthony=`anthony`. (Batman keeps `blank` on purpose so his existing
  `localStorage` data still loads.)
- `<title>` set per app.

---

## 4. The 5 feature changes (all apps)

1. **Dashboard stats, front & center** — top of Home, exact order:
   Total Sales Volume, Total Booth Rents, Total Other Expenses, Total Tax Reserve,
   Total COGs, Total Profit, Avg Show, Biggest Show, Avg Show Profit, Net.
   They reconcile: `Sales − COGS − Booth − Other = Profit`, `Profit − Tax = Net`.
   (Code: `rHome()`, look for `// ---- DASHBOARD STATS`.)
2. **Pre-show inventory calculator** — a card near the top of every show entry.
   Enter the stock you're bringing → projects potential sales volume + potential
   over product cost + units + COGS. Falls back to packed
   inventory if no separate plan entered.
   (Code: `preShowCalcHTML()`, `openPreShowStock()`, `preShowTotals()`; rendered in `rShow()`.)
   *(Jul 2026: the "potential commission" stat was replaced when commission
   percentages were removed — reps are now paid a flat $ per day, entered daily
   as `day.repPay`.)*
3. **Collected vs Full Price — redesigned** — modern capture-rate gauge (big % +
   gradient bar) over per-show cards with mini progress bars.
   (Code: `secCollected()`.)
4. **Master Inventory button** — promoted to the first and largest control on Home
   (full-width gold hero button above everything).
   (Code: `rHome()`, look for `// ---- MASTER INVENTORY`.)
5. **Crew Apps launcher (personal app only)** — "Crew Apps · Team Tracker" card with
   3 new-tab buttons: Batman (live URL wired), Isaiah & Anthony (placeholders).
   (Code: `rHome()`, between `/*CREW_START*/` and `/*CREW_END*/`.)

---

## 5. DEPLOYMENT — step by step (do this on the home PC)

Prereqs: `gh auth status` shows you're logged in as `jfgreco84-commits`, and you've
checked out this branch:
```
git fetch origin
git checkout claude/best-solution-rebuild-2ayf4w
cd best-solution
```

### 5a. Froggy → existing repo `best-solution-app`
Replace the live file (keep the same filename so the URL keeps working):
```
git clone https://github.com/jfgreco84-commits/best-solution-app.git /tmp/bs-app
cp froggy-personal.html /tmp/bs-app/BEST_SOLUTION_APP.html
cd /tmp/bs-app && git add BEST_SOLUTION_APP.html && git commit -m "Rebuild: dashboard stats, pre-show calculator, redesigned Collected view, Master Inventory hero, Crew Apps launcher" && git push
cd -
```
URL stays: https://jfgreco84-commits.github.io/best-solution-app/BEST_SOLUTION_APP.html

### 5b. Batman → existing repo `best-solution-blank`
```
git clone https://github.com/jfgreco84-commits/best-solution-blank.git /tmp/bs-blank
cp batman-blank.html /tmp/bs-blank/index.html
cd /tmp/bs-blank && git add index.html && git commit -m "Rebuild to match master (feature parity), blank data" && git push
cd -
```
URL stays: https://jfgreco84-commits.github.io/best-solution-blank/

### 5c. Isaiah → NEW repo
```
gh repo create best-solution-isaiah --public --clone
cp isaiah-wojo.html best-solution-isaiah/index.html
cd best-solution-isaiah && git add index.html && git commit -m "Isaiah's Best Solution app" && git push
gh api -X POST repos/jfgreco84-commits/best-solution-isaiah/pages -f source[branch]=main -f source[path]=/ || \
  echo "If that fails, enable Pages in repo Settings → Pages → Branch: main / root"
cd -
```
URL will be: https://jfgreco84-commits.github.io/best-solution-isaiah/

### 5d. Anthony → NEW repo
```
gh repo create best-solution-anthony --public --clone
cp anthony-wojo.html best-solution-anthony/index.html
cd best-solution-anthony && git add index.html && git commit -m "Anthony's Best Solution app" && git push
gh api -X POST repos/jfgreco84-commits/best-solution-anthony/pages -f source[branch]=main -f source[path]=/ || \
  echo "If that fails, enable Pages in repo Settings → Pages → Branch: main / root"
cd -
```
URL will be: https://jfgreco84-commits.github.io/best-solution-anthony/

### 5e. Wire the real crew URLs into the personal app, then redeploy 5a
In `best-solution/froggy-personal.html`, find the two markers and replace `href="#"`:
- `<!-- ISAIAH_URL ... -->` → set the next `<a … href="#"` to
  `href="https://jfgreco84-commits.github.io/best-solution-isaiah/"` and delete the
  `onclick="if(...)..."` guard on that link.
- `<!-- ANTHONY_URL ... -->` → same with the Anthony URL.

Then regenerate blanks (the crew launcher isn't in them, but keep the pipeline clean),
commit to this branch, and re-run step 5a:
```
python3 gen_blank.py
git add froggy-personal.html batman-blank.html isaiah-wojo.html anthony-wojo.html
git commit -m "Wire real crew launcher URLs"
git push
# then redo 5a to push froggy-personal.html → best-solution-app
```

> If you prefer not to hardcode and edit later, the launcher already shows a friendly
> toast ("URL not set yet") until you set the URLs — it won't break.

---

## 6. Verification (run after any edit to the master)

```
cd best-solution
# 1) JS syntax of all 4
for f in froggy-personal batman-blank isaiah-wojo anthony-wojo; do
  python3 -c "import re;open('/tmp/c.js','w').write(';\n'.join(re.findall(r'<script(?![^>]*\bsrc=)[^>]*>(.*?)</script>',open('$f.html').read(),re.S)))"
  node --check /tmp/c.js && echo "$f OK"
done
# 2) regenerate blanks and confirm deterministic
python3 gen_blank.py
```
The original web session also ran a DOM smoke test (rendered Home / Show / Section
for all 4 with a stubbed DOM) and asserted: stat order correct, Master Inventory is
the first button, crew launcher only in the personal app, and no personal-data leaks
(no "Martone"/"Froggy"/seeded crew/Batman card/2025 history) in the blanks. If you
want that harness again, ask the next Claude to recreate `/tmp/smoke.js` — it's quick.

---

## 7. Data isolation & cloud sync — IMPORTANT to verify

**Local storage** (per app, never collides):
- Froggy: `dd_bs_v7`  · Batman: `dd_bs_blank_v7` · Isaiah: `dd_bs_isaiah_v7` · Anthony: `dd_bs_anthony_v7`

**Cloud sync (Supabase):** all apps now use the **master's login-based model** —
table `app_data`, rows keyed by `user_id` + a per-app `data_key`:
- Froggy `bs_state` · Batman `bs_state_blank` · Isaiah `bs_state_isaiah` · Anthony `bs_state_anthony`
- Supabase project URL is in the file (`SB_URL`), anon key is `SB_KEY`.

**Two things to confirm:**
1. **Crew need to sign in** for cloud sync (the app works fully offline via
   localStorage without it). Each crew member signs in with their own account →
   their data is isolated by `user_id` AND `data_key`. Verify the Supabase `app_data`
   table + RLS policies allow a signed-in user to read/write their own row. (Froggy's
   app already works, so the table exists; just confirm crew logins work.)
2. **Batman's old cloud data won't auto-migrate.** The previous blank used a
   different, no-login shared model (table `blank_app_state`, id `shared`). The new
   app uses the login model. Batman's **local** data carries over (same
   `dd_bs_blank_v7` key); his old *cloud* copy does not. If he had important
   data only in the old cloud, export/import it before he clears that browser.
   (There's an export/backup in Settings.)

If you'd rather keep Batman on the old no-login shared cloud model, that's a
deliberate divergence from "match the master" — only do it if the user asks.

---

## 8. Source-of-truth decision (ask the user)

The 4 files currently live in `greco-household/best-solution/` on the branch.
`greco-household`'s own `index.html` is a DIFFERENT app (the Greco Household Finance
Manager) — **do not touch it.** Options for the user:
- **A:** Keep `greco-household/best-solution/` as the dev/source-of-truth (master +
  generator), and treat the 4 Pages repos as deploy targets. Merge PR #1 to preserve
  the source. (Recommended — keeps the generator + handoff versioned.)
- **B:** Don't merge; just use the branch as a staging area and deploy from it.

Either way, the live apps are the 4 Pages repos in §5.

---

## 9. Known decisions / rationale (don't "fix" these unintentionally)

- **"Total Other Expenses"** = everything in YTD expenses except booth rents
  (gas, hotel, supplies, commissions, worker pay, misc, planned deposits). Chosen so
  the headline stats reconcile to Profit. If the user wants it to mean only the
  global "Other Expenses" ledger, that's a one-line change in `rHome()`.
- **Rep pay model (Jul 2026):** commission percentages were removed entirely.
  Reps get a flat $ per day (`day.repPay = {repId: $}`), entered daily. Legacy
  per-show payouts (`sh.repPayout`) still count as "earned" on old shows when
  no day pay exists, so logged payments reconcile. Do not resurrect
  `DEFAULT_COMM_RATE` / `commCash` / `commCard` — they are gone on purpose.
- **Batman's "Borrowed from Batman" card** was removed from the blanks (it names a
  specific person = personal data) but kept in Froggy's master. The borrow *feature*
  code still exists; it's just not surfaced in the blanks' dashboard grid.
- **Crew launcher** is gated by `/*CREW_START*/…/*CREW_END*/` markers that the
  generator strips — keep those markers if you move that block.

---

## 10. One-paragraph prompt you can paste into the new thread

> I'm continuing the "Best Solution app rebuild." Read `best-solution/HANDOFF.md` in
> repo `jfgreco84-commits/greco-household` (branch `claude/best-solution-rebuild-2ayf4w`)
> in full first. The code is done; I need you to do the deployment in §5: push
> `froggy-personal.html` to the `best-solution-app` repo as `BEST_SOLUTION_APP.html`,
> `batman-blank.html` to `best-solution-blank` as `index.html`, create new repos for
> Isaiah and Anthony with their files as `index.html`, enable GitHub Pages on the new
> ones, then wire the real Isaiah/Anthony URLs into the Crew Apps launcher in the
> personal app (§5e) and redeploy it. Verify with §6 and confirm cloud sync per §7.
> Make feature changes only in the master and regenerate blanks with `gen_blank.py` —
> never hand-edit the blanks.
