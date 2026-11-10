// A study log. A second, independently authored feature with different behaviour from the checklist: it validates input,
// keeps one entry per day, and shows totals.

function render(ctx) {
  return '<div class="card"><h3>Study log</h3>' +
    '<p><input id="studyLogMinutes" type="number" min="1" max="600" placeholder="Minutes studied today"> ' +
    '<button class="btn sm" id="studyLogAdd">Log it</button></p>' +
    '<p class="note" id="studyLogMessage"></p>' +
    '<p class="kv"><span>Total minutes</span><b id="studyLogTotal">0</b></p>' +
    '<p class="kv"><span>Days logged</span><b id="studyLogDays">0</b></p></div>';
}

function wire(ctx, el) {
  const msg = el.querySelector("#studyLogMessage");
  let entries = [];
  const draw = () => {
    el.querySelector("#studyLogTotal").textContent = String(entries.reduce((a, e) => a + e.minutes, 0));
    el.querySelector("#studyLogDays").textContent = String(entries.length);
  };
  el.querySelector("#studyLogAdd").onclick = async () => {
    const m = Number(el.querySelector("#studyLogMinutes").value);
    if (!Number.isInteger(m) || m < 1 || m > 600) { msg.textContent = "Enter a whole number of minutes from 1 to 600."; return; }
    msg.textContent = "";
    const today = new Date().toISOString().slice(0, 10), found = entries.find(e => e.date === today);
    if (found) found.minutes += m; else entries.push({ date: today, minutes: m });
    try { await ctx.store.set("entries", entries); } catch (e) { ctx.toast("Could not save: " + (e && e.message || e)); }
    el.querySelector("#studyLogMinutes").value = ""; draw();
  };
  ctx.store.get("entries").then(v => { entries = Array.isArray(v) ? v : []; draw(); });
}

return { render, wire };
