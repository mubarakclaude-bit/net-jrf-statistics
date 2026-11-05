#!/usr/bin/env python3
# Re-skin the app in Airbnb's design language: Cereal-like geometric sans, the Rausch /
# Babu palette darkened to clear WCAG AA, 8/12/16px radii, soft lift-on-hover cards,
# black selected pills, 12px-radius buttons, bordered inputs with a black focus ring,
# and Airbnb's bottom-sheet-on-mobile modal. Token names are unchanged so every
# existing rule keeps working.
import io, sys

H = "src/00-head.html"
W = "src/02-ws.css"
h = io.open(H, encoding="utf-8").read()
orig = h

def span(start, end, s):
    a = s.index(start); b = s.index(end, a)
    return s[a:b]

# ------------------------------------------------------------------ typefaces
h = h.replace(
'<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Source+Serif+4:opsz,wght@8..60,400;8..60,600;8..60,700&family=IBM+Plex+Mono:wght@400;500&display=swap">',
'<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Figtree:wght@400;500;600;700;800&family=IBM+Plex+Mono:wght@400;500&display=swap">')

# --------------------------------------------------------------------- tokens
LIGHT = """  --bg:#f7f7f7; --surface:#fff; --surface2:#f7f7f7; --surface3:#ebebeb;
  --line:#dddddd; --line2:#b0b0b0;
  --fg:#222222; --fg2:#5e5e5e; --fg3:#6a6a6a;
  --accent:#d70466; --accent2:#b0184a; --accent-soft:#fff0f4;
  --brand:#ff385c; --brand2:#e61e4d;
  --ochre:#8a5b00; --ochre-soft:#fdf3e2;
  --ok:#007a7f; --ok-soft:#e6f4f4; --mid:#8a5b00; --mid-soft:#fdf3e2;
  --bad:#c13515; --bad-soft:#fdeeea; --dim:#6a6a6a; --dim-soft:#f0f0f0;
  --btnfg:#fff;
  --rail:#fff; --canvas:#fff;
  --shadow:0 1px 2px rgba(0,0,0,.06), 0 4px 12px rgba(0,0,0,.05);
  --shadow-lg:0 6px 16px rgba(0,0,0,.12), 0 16px 32px rgba(0,0,0,.10);
  --lift:0 6px 16px rgba(0,0,0,.12);
  --scrim:rgba(0,0,0,.5);
"""
DARK = """  --bg:#121212; --surface:#1c1c1c; --surface2:#222222; --surface3:#2e2e2e;
  --line:#363636; --line2:#4f4f4f;
  --fg:#f7f7f7; --fg2:#c7c7c7; --fg3:#ababab;
  --accent:#ff7a96; --accent2:#ffa0b4; --accent-soft:#3a1420;
  --brand:#ff5a76; --brand2:#ff7a96;
  --ochre:#e3a94f; --ochre-soft:#3a2a12;
  --ok:#4ecdc4; --ok-soft:#10312f; --mid:#e3a94f; --mid-soft:#3a2a12;
  --bad:#ff8a6b; --bad-soft:#3a1c13; --dim:#ababab; --dim-soft:#262626;
  --btnfg:#121212;
  --rail:#171717; --canvas:#1c1c1c;
  --shadow:0 1px 2px rgba(0,0,0,.5), 0 4px 12px rgba(0,0,0,.4);
  --shadow-lg:0 6px 16px rgba(0,0,0,.55), 0 16px 32px rgba(0,0,0,.5);
  --lift:0 6px 16px rgba(0,0,0,.6);
  --scrim:rgba(0,0,0,.68);
  color-scheme:dark;
"""
SHAPE = """  --r:16px; --r2:12px; --r3:999px; --rsm:8px;
  --ui:'Figtree',system-ui,-apple-system,'Segoe UI',sans-serif;
  --serif:'Figtree',system-ui,-apple-system,'Segoe UI',sans-serif;
  --mono:'IBM Plex Mono',ui-monospace,'SF Mono',Menlo,monospace;
  --ease:cubic-bezier(.2,.8,.3,1);
"""

h = h.replace(span(":root{\n", "}\n@media (prefers-color-scheme:dark)", h),
              ":root{\n" + LIGHT + SHAPE)
h = h.replace(span('@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){',
                   '}}\n:root[data-theme="dark"]{', h),
              '@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){\n' + DARK)
h = h.replace(span(':root[data-theme="dark"]{', "}\n*{box-sizing:border-box}", h),
              ':root[data-theme="dark"]{\n' + DARK)

# ---------------------------------------------------------------- type ramp
h = h.replace(
"""body{background:var(--bg);color:var(--fg);font-family:var(--ui);font-size:15px;line-height:1.5;-webkit-text-size-adjust:100%}
h1,h2,h3,h4{font-family:var(--serif);font-weight:600;margin:0;text-wrap:balance;letter-spacing:-.01em}
h1{font-size:1.5rem}h2{font-size:1.2rem}h3{font-size:1.02rem}h4{font-size:.93rem}
p{margin:0 0 .6em}
a{color:var(--accent)}""",
"""body{background:var(--bg);color:var(--fg);font-family:var(--ui);font-size:15px;line-height:1.5;
  -webkit-text-size-adjust:100%;-webkit-font-smoothing:antialiased}
h1,h2,h3,h4{font-family:var(--serif);font-weight:700;margin:0;text-wrap:balance;letter-spacing:-.022em}
h1{font-size:1.62rem;line-height:1.2}h2{font-size:1.28rem;line-height:1.25}
h3{font-size:1.04rem;line-height:1.3}h4{font-size:.93rem;letter-spacing:-.01em}
p{margin:0 0 .6em}
a{color:var(--fg);text-decoration:underline;text-underline-offset:2px;font-weight:600}
a:hover{color:var(--accent)}
/* Airbnb's focus treatment: a dark 2px ring on anything reachable by keyboard */
:focus-visible{outline:2px solid var(--fg);outline-offset:2px;border-radius:4px}""")

# ------------------------------------------------------------------ controls
h = h.replace(
""".chip{display:inline-flex;align-items:center;gap:5px;font-size:.73rem;font-weight:600;padding:2px 8px;border-radius:999px;background:var(--surface2);color:var(--fg2);white-space:nowrap}""",
""".chip{display:inline-flex;align-items:center;gap:5px;font-size:.73rem;font-weight:600;padding:3px 9px;border-radius:999px;background:var(--surface2);color:var(--fg2);white-space:nowrap}""")

h = h.replace(
""".btn{border:1px solid var(--line2);background:var(--surface);color:var(--fg);border-radius:var(--r2);padding:7px 12px;font-size:.85rem;font-weight:500;display:inline-flex;align-items:center;gap:6px}
.btn:hover{border-color:var(--accent);color:var(--accent)}
.btn.p{background:var(--accent);border-color:var(--accent);color:var(--btnfg)}
.btn.p:hover{background:var(--accent2);border-color:var(--accent2);color:var(--btnfg)}
.btn.sm{padding:4px 9px;font-size:.78rem}
.btn.gh{border-color:transparent;background:none;color:var(--fg2);padding-inline:7px}
.btn.gh:hover{background:var(--surface3);color:var(--fg);border-color:transparent}
.btn.g{background:var(--ok);border-color:var(--ok);color:var(--btnfg)}
.btn:disabled{opacity:.42;cursor:not-allowed}
.btn:disabled:hover{border-color:var(--line2);color:var(--fg)}
.tog{border:1px solid var(--line2);background:var(--surface);color:var(--fg2);border-radius:999px;padding:4px 11px;font-size:.78rem;font-weight:500}
.tog[aria-pressed="true"]{background:var(--accent);border-color:var(--accent);color:var(--btnfg)}
select,input[type=text],input[type=date],input[type=number],textarea{font:inherit;font-size:.85rem;background:var(--surface);color:var(--fg);border:1px solid var(--line2);border-radius:var(--r2);padding:6px 8px;max-width:100%}""",
"""/* Buttons: 12px radius, 600 weight, a secondary that outlines in ink rather than
   tinting, and a ghost that reads as Airbnb's underlined text link. */
.btn{border:1px solid var(--fg);background:var(--surface);color:var(--fg);border-radius:var(--r2);
  padding:9px 15px;font-size:.85rem;font-weight:600;display:inline-flex;align-items:center;gap:6px;
  transition:background .2s var(--ease),border-color .2s var(--ease),color .2s var(--ease),transform .12s var(--ease)}
.btn:hover{background:var(--surface3);border-color:var(--fg);color:var(--fg)}
.btn:active{transform:scale(.97)}
.btn.p{background:var(--accent);border-color:var(--accent);color:var(--btnfg)}
.btn.p:hover{background:var(--accent2);border-color:var(--accent2);color:var(--btnfg)}
.btn.sm{padding:6px 11px;font-size:.78rem;border-radius:var(--rsm)}
.btn.gh{border-color:transparent;background:none;color:var(--fg);padding-inline:8px;text-decoration:underline;text-underline-offset:3px}
.btn.gh:hover{background:var(--surface3);color:var(--fg);border-color:transparent}
.btn.g{background:var(--ok);border-color:var(--ok);color:var(--btnfg)}
.btn.g:hover{background:var(--ok);border-color:var(--ok);filter:brightness(.92)}
.btn:disabled{opacity:.42;cursor:not-allowed}
.btn:disabled:hover{background:var(--surface);border-color:var(--fg);color:var(--fg);transform:none}
/* Filter pills. Selected is ink, not brand — brand red is kept for the one primary action. */
.tog{border:1px solid var(--line);background:var(--surface);color:var(--fg);border-radius:999px;
  padding:7px 14px;font-size:.78rem;font-weight:600;
  transition:border-color .2s var(--ease),background .2s var(--ease),color .2s var(--ease)}
.tog:hover{border-color:var(--fg)}
.tog[aria-pressed="true"]{background:var(--fg);border-color:var(--fg);color:var(--surface)}
select,input[type=text],input[type=date],input[type=number],textarea{font:inherit;font-size:.85rem;
  background:var(--surface);color:var(--fg);border:1px solid var(--line2);border-radius:var(--rsm);
  padding:9px 11px;max-width:100%;transition:border-color .15s var(--ease),box-shadow .15s var(--ease)}
select:focus,input[type=text]:focus,input[type=date]:focus,input[type=number]:focus,textarea:focus{
  outline:none;border-color:var(--fg);box-shadow:0 0 0 1px var(--fg)}""")

h = h.replace(
""".card{background:var(--surface);border:1px solid var(--line);border-radius:var(--r);padding:14px;box-shadow:var(--shadow)}
.card.flat{box-shadow:none}""",
"""/* Airbnb cards sit flat and lift on hover; only the interactive ones lift. */
.card{background:var(--surface);border:1px solid var(--line);border-radius:var(--r);padding:16px;box-shadow:none}
.card.flat{box-shadow:none;border-color:var(--line)}
.card.lift{transition:box-shadow .2s var(--ease),transform .2s var(--ease)}
.card.lift:hover{box-shadow:var(--lift);transform:translateY(-2px)}""")

h = h.replace(
""".st3 button[aria-pressed="true"]{background:var(--accent);color:var(--btnfg)}""",
""".st3 button[aria-pressed="true"]{background:var(--fg);color:var(--surface)}""")

h = h.replace(
""".qrow{display:flex;gap:10px;align-items:flex-start;width:100%;text-align:left;background:var(--surface);border:1px solid var(--line);border-radius:var(--r2);padding:9px 11px;color:inherit;margin-bottom:6px}
.qrow:hover{border-color:var(--accent)}""",
""".qrow{display:flex;gap:10px;align-items:flex-start;width:100%;text-align:left;background:var(--surface);
  border:1px solid var(--line);border-radius:var(--r2);padding:12px 14px;color:inherit;margin-bottom:8px;
  transition:box-shadow .2s var(--ease),border-color .2s var(--ease),transform .2s var(--ease)}
.qrow:hover{border-color:var(--line2);box-shadow:var(--lift);transform:translateY(-1px)}""")

h = h.replace(
""".opt:hover{border-color:var(--accent)}""",
""".opt{transition:border-color .15s var(--ease),background .15s var(--ease),box-shadow .15s var(--ease)}
.opt:hover{border-color:var(--fg);box-shadow:inset 0 0 0 1px var(--fg)}""")
h = h.replace(
""".opt[aria-pressed="true"]{border-color:var(--accent);background:var(--accent-soft)}""",
""".opt[aria-pressed="true"]{border-color:var(--fg);background:var(--surface3);box-shadow:inset 0 0 0 1px var(--fg)}""")
h = h.replace(
""".opt[aria-pressed="true"] .ol{color:var(--accent)}""",
""".opt[aria-pressed="true"] .ol{color:var(--fg)}""")

# header: Airbnb's white bar, generous height, tabs underlined in ink
h = h.replace(
"""#top{position:sticky;top:env(safe-area-inset-top,0px);z-index:80;background:var(--bg);border-bottom:1px solid var(--line)}""",
"""#top{position:sticky;top:env(safe-area-inset-top,0px);z-index:80;background:var(--surface);
  border-bottom:1px solid var(--line)}""")
h = h.replace(
"""nav button{background:none;border:0;border-bottom:2px solid transparent;color:var(--fg2);padding:7px 10px 9px;font-size:.86rem;font-weight:500;white-space:nowrap;display:flex;align-items:center;gap:6px}
nav button[aria-current="true"]{color:var(--fg);border-bottom-color:var(--accent)}
nav .dot{width:6px;height:6px;border-radius:50%;background:var(--accent)}""",
"""nav button{background:none;border:0;border-bottom:2px solid transparent;color:var(--fg2);
  padding:11px 12px 13px;font-size:.86rem;font-weight:600;white-space:nowrap;display:flex;align-items:center;gap:6px;
  transition:color .15s var(--ease),border-color .15s var(--ease)}
nav button:hover{color:var(--fg)}
nav button[aria-current="true"]{color:var(--fg);border-bottom-color:var(--fg)}
nav .dot{width:6px;height:6px;border-radius:50%;background:var(--brand)}""")

# decorative fills carry the brand red, where nothing is read off them
h = h.replace(""".bar>i{display:block;height:100%;border-radius:999px;background:var(--accent);transition:width .4s ease}""",
              """.bar{background:var(--surface3)}
.bar>i{display:block;height:100%;border-radius:999px;background:var(--brand);transition:width .5s var(--ease)}""")
h = h.replace(""".gauge>i{position:absolute;inset:0 auto 0 0;background:linear-gradient(90deg,var(--accent),var(--accent2));transition:width .5s ease}""",
              """.gauge>i{position:absolute;inset:0 auto 0 0;background:linear-gradient(90deg,var(--brand),var(--accent));transition:width .6s var(--ease)}""")

# ------------------------------------------------- Airbnb patterns, appended
PATTERNS = """
/* ===================== Airbnb patterns ===================== */
/* A section header that states the thing and then one quiet line about it. */
.hd h1,.hd h2{letter-spacing:-.025em}
.hd{margin-bottom:18px;align-items:baseline}
.hd p{font-size:.9rem;color:var(--fg2)}

/* Horizontally scrolling category row, the way Airbnb carries its filters:
   no scrollbar, edge-to-edge on a phone, pills that fade in from the right. */
.pills{display:flex;gap:8px;overflow-x:auto;scrollbar-width:none;padding:2px 0 4px;
  margin-inline:calc(-1 * var(--pg,0px));padding-inline:var(--pg,0px);scroll-snap-type:x proximity}
.pills::-webkit-scrollbar{display:none}
.pills>*{flex:0 0 auto;scroll-snap-align:start}

/* Star rating, inline and tabular so columns of them line up. */
.xw,.stars{font-variant-numeric:tabular-nums;letter-spacing:.02em}

/* The sticky action bar: a quiet summary on the left, one filled action on the right. */
.actbar{position:sticky;bottom:0;z-index:40;display:flex;gap:12px;align-items:center;
  background:var(--surface);border-top:1px solid var(--line);
  padding:12px 16px calc(12px + env(safe-area-inset-bottom,0px));
  margin-inline:calc(-1 * var(--pg,16px));box-shadow:0 -4px 12px rgba(0,0,0,.05)}
.actbar .sum{flex:1;min-width:0;font-size:.84rem;color:var(--fg2)}
.actbar .sum b{display:block;color:var(--fg);font-size:.95rem;font-weight:700}

/* Larger tap targets than a desktop app would use — Airbnb holds 44px on touch. */
@media (hover:none){
  .btn{padding:11px 16px}
  .tog{padding:9px 15px}
  .pal button{width:38px;height:38px}
  select,input[type=text],input[type=date],input[type=number]{padding:11px 12px;font-size:.9rem}
}
@media (max-width:560px){
  h1{font-size:1.42rem}
  .card{padding:14px;border-radius:14px}
}
@media (prefers-reduced-motion:reduce){
  *,*::before,*::after{transition-duration:.01ms!important;animation-duration:.01ms!important}
}
"""
h = h.replace("\n</style>", PATTERNS + "\n</style>")

if h == orig:
    sys.exit("head.html unchanged — an anchor did not match")
io.open(H, "w", encoding="utf-8").write(h)

# --------------------------------------------------- workspace shell overrides
w = io.open(W, encoding="utf-8").read()
WS = """
/* ===================== Airbnb pass — workspace ===================== */
/* Selected rail rows read as ink on a tint, not as a coloured stripe. */
.navt{padding:10px 12px 10px 14px;border-radius:0}
.navt.cur{background:var(--surface3);border-left-color:var(--fg)}
.navt.cur .tn{font-weight:700}
.steprow{padding:9px 14px 9px 16px;transition:background .15s var(--ease)}
.steprow.cur>.snode{background:var(--fg);border-color:var(--fg);color:var(--surface);box-shadow:0 0 0 4px var(--surface3)}
.steprow.cur .stx b{color:var(--fg)}
.steprow.cur.done .stx b{color:var(--fg)}
.steprow>.snode:hover{border-color:var(--fg);color:var(--fg)}

/* Content cards lift on hover like a listing card. */
.modcard{transition:box-shadow .2s var(--ease),transform .2s var(--ease),border-color .2s var(--ease)}
.modcard:hover{box-shadow:var(--lift);border-color:var(--line2)}
.modcard.open{box-shadow:var(--shadow);transform:none}
.fcard,.rcard,.scenbtn{transition:box-shadow .2s var(--ease),transform .2s var(--ease),border-color .2s var(--ease)}
.scenbtn:hover,.fcard:hover,.rcard:hover{box-shadow:var(--lift);transform:translateY(-1px);border-color:var(--line2)}

/* The start block is the page's one primary action — give it the filled treatment. */
.startblk{border-color:var(--line);border-radius:var(--r);box-shadow:var(--shadow)}
.nextup{border-radius:var(--r)}

/* The scene bar behaves like Airbnb's sticky sub-header: white, hairline, no tint. */
.scbar{background:var(--surface);border-bottom:1px solid var(--line);padding-block:10px}

/* Modal: a centred dialog on a desktop, a bottom sheet with a drag handle on a phone. */
.modalwrap{background:var(--scrim);backdrop-filter:saturate(1.1) blur(2px)}
.modal{border-radius:var(--r);box-shadow:var(--shadow-lg)}
.modalhd{padding:16px 18px}
.modalhd b{font-weight:700;letter-spacing:-.02em}
.modalft{padding:14px 18px;gap:10px}
@media (max-width:620px){
  .modalwrap{padding:0;align-items:flex-end}
  .modal{max-width:none;border-radius:16px 16px 0 0;max-height:92vh;animation:sheet .26s var(--ease)}
  .modal::before{content:"";display:block;width:36px;height:4px;border-radius:999px;
    background:var(--line2);margin:8px auto 0;flex:0 0 auto}
  .modalft{position:sticky;bottom:0;background:var(--surface);
    padding-bottom:calc(14px + env(safe-area-inset-bottom,0px))}
}
@keyframes sheet{from{transform:translateY(14px);opacity:.6}to{transform:none;opacity:1}}
"""
if "Airbnb pass — workspace" not in w:
    io.open(W, "w", encoding="utf-8").write(w + WS)
print("design pass applied to %s and %s" % (H, W))
