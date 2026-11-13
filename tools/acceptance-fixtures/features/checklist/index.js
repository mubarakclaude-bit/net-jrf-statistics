// A study checklist. Authored from scratch as an independent contribution: it has its own behaviour, its own storage
// key and its own tests, and touches nothing outside this folder.

function render(ctx) {
  return '<div class="card"><h3>Checklist</h3>' +
    '<p><input id="checklistText" type="text" maxlength="80" placeholder="Add an item"> ' +
    '<button class="btn sm" id="checklistAdd">Add</button></p>' +
    '<ul id="checklistList" style="list-style:none;padding:0"></ul>' +
    '<p class="note" id="checklistRemaining"></p></div>';
}

function wire(ctx, el) {
  const list = el.querySelector("#checklistList"), remaining = el.querySelector("#checklistRemaining"), input = el.querySelector("#checklistText");
  let items = [];
  const draw = () => {
    list.innerHTML = items.map((it, i) =>
      '<li><label><input type="checkbox" data-checklist-tick="' + i + '"' + (it.done ? " checked" : "") + '> <span>' + ctx.esc(it.text) + '</span></label> ' +
      '<button class="btn sm" data-checklist-del="' + i + '">Remove</button></li>').join("");
    remaining.textContent = items.filter(x => !x.done).length + " remaining of " + items.length;
  };
  const save = async () => { try { await ctx.store.set("items", items); } catch (e) { ctx.toast("Could not save: " + (e && e.message || e)); } draw(); };
  el.querySelector("#checklistAdd").onclick = async () => {
    const text = input.value.trim(); if (!text) { ctx.toast("Type something to add"); return; }
    items.push({ text: text, done: false }); input.value = ""; await save();
  };
  input.onkeydown = e => { if (e.key === "Enter") el.querySelector("#checklistAdd").click(); };
  list.onchange = async e => { const i = e.target.getAttribute("data-checklist-tick"); if (i === null) return; items[+i].done = e.target.checked; await save(); };
  list.onclick = async e => { const i = e.target.getAttribute("data-checklist-del"); if (i === null) return; items.splice(+i, 1); await save(); };
  ctx.store.get("items").then(v => { items = Array.isArray(v) ? v : []; draw(); });
}

return { render, wire };
