import re, sys

master = open(__import__('os').path.join(__import__('os').path.dirname(__file__),'froggy-personal.html'), encoding='utf-8').read()

MINIMAL_AOTU = '''function applyOneTimeUpdates(d){
  d._applied=d._applied||{};
  // Blank / crew copy: NO pre-filled personal data. Structural seeding only.
  (d.shows||[]).forEach(sh=>{
    if(!sh.boothPayments)sh.boothPayments=[];
    if(sh.confirmed===undefined)sh.confirmed=sh.status==='completed';
    if(!sh.workers)sh.workers=[];
    if(!sh.repPayMeta)sh.repPayMeta={};
    if(!sh.repIds)sh.repIds=[];
    if(sh.repOnlyShow===undefined)sh.repOnlyShow=false;
    if(!sh.showExpenses)sh.showExpenses=[];
    (sh.days||[]).forEach(day=>{ if(!day.repSales)day.repSales=[]; if(day.payments&&day.payments.debit===undefined)day.payments.debit=0; });
  });
  if(!d._applied['supplies_seed_v1']){
    if(!d.supplies||d.supplies.length===0)d.supplies=JSON.parse(JSON.stringify(DEFAULT_SUPPLIES));
    d._applied['supplies_seed_v1']=true;
  }
  if(!d._applied['reps_seed_v1']){
    if(!d.reps)d.reps=[];
    if(!d.reps.length)d.reps.push({id:'rep_owner',name:'__OWNER__',isSelf:true,active:true,payments:[]});
    d._applied['reps_seed_v1']=true;
  }
  if(!Array.isArray(d.freight))d.freight=[];
  if(!d.costs||typeof d.costs!=='object')d.costs={};
}
function buildPlannedShow('''

def make(slug, owner, title):
    h = master

    # 1. Replace the big personal applyOneTimeUpdates with a minimal generic one
    start = h.index('function applyOneTimeUpdates(d){')
    end = h.index('function buildPlannedShow(', start)
    h = h[:start] + MINIMAL_AOTU.replace('__OWNER__', owner) + h[end+len('function buildPlannedShow('):]

    # 2. Zero starting inventory
    h = re.sub(r"inventory:\{'32oz':\d+,'16oz':\d+,'8oz':\d+,'2oz':\d+,'c5s':\d+,'c5l':\d+\}",
               "inventory:{'32oz':0,'16oz':0,'8oz':0,'2oz':0,'c5s':0,'c5l':0}", h)

    # 3. Empty product debt in INIT + genericize its section-header comment (supplier name is personal)
    h = h.replace("productDebt:{supplier:'Mark Martone',originalBalance:10000,payments:[]},",
                  "productDebt:{supplier:'',originalBalance:0,payments:[]},")
    h = h.replace("// PRODUCT DEBT (MARK MARTONE)", "// PRODUCT DEBT (SUPPLIER)")

    # 4. Empty 2025 history + prior-year comparison
    h = re.sub(r"const SHOWS_2025=\[.*?\n\];", "const SHOWS_2025=[];", h, flags=re.S)
    h = re.sub(r"const PREV_YEAR=\{[^}]*\};",
               "const PREV_YEAR={gross:0,cogs:0,booth:0,otherExp:0,net:0,shows:0,bestShow:'',bestProfit:0};", h)

    # 5. Remove the "Borrowed from Batman" quick-access button + section-map entry (personal)
    h = re.sub(r"  /\*BATMAN_BTN_START\*/.*?  /\*BATMAN_BTN_END\*/\n", "", h, flags=re.S)
    h = h.replace(
        "    best:{t:'Best Shows This Season',f:secBest},\n    batman:{t:'Borrowed from Batman',f:secBatman}\n",
        "    best:{t:'Best Shows This Season',f:secBest}\n")

    # 6. Remove the Crew Apps launcher (personal app only)
    h = re.sub(r"  /\*CREW_START\*/.*?  /\*CREW_END\*/\n", "", h, flags=re.S)

    # 7. De-personalize rep-only show label
    h = h.replace("Rep-only show</strong> — Justin not attending",
                  "Rep-only show</strong> — owner not attending")

    # 8. Namespace storage + cloud keys for data isolation
    h = h.replace("dd_bs_", "dd_bs_%s_" % slug)
    h = h.replace("'bs_state'", "'bs_state_%s'" % slug)

    # 9. Title
    h = h.replace("<title>Best Solution | Dot Dynasty LLC</title>",
                  "<title>%s</title>" % title)
    return h

apps = [
    ('blank',   'Batman',  'Best Solution — Batman',  'batman-blank.html'),
    ('isaiah',  'Isaiah',  'Best Solution — Isaiah',  'isaiah-wojo.html'),
    ('anthony', 'Anthony', 'Best Solution — Anthony', 'anthony-wojo.html'),
]
for slug, owner, title, fname in apps:
    out = make(slug, owner, title)
    open(fname, 'w', encoding='utf-8', newline='').write(out)
    # sanity assertions
    assert 'martone' not in out.lower(), fname+': Martone leaked'
    assert 'Froggy' not in out, fname+': Froggy leaked'
    assert "name:'Justin (Froggy)'" not in out, fname+': Justin rep leaked'
    assert 'CREW_START' not in out and 'Crew Apps'.lower() not in out.lower() or slug, None
    assert "label:'Borrowed from Batman'" not in out, fname+': batman card leaked'
    assert "inventory:{'32oz':0" in out, fname+': inventory not zeroed'
    assert 'dd_bs_%s_v7'%slug in out, fname+': storage key not namespaced'
    print(fname, 'OK', len(out), 'bytes')
