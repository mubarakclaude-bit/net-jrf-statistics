// Reference feature: a counter that remembers its value per learner and profile.
// This file runs inside its own private scope. It must end with:  return { render, wire };
//   render(ctx) -> an HTML string, drawn into this feature's section
//   wire(ctx, el) -> attach behaviour to the drawn HTML (el is the section)
// Learner data goes through ctx.store, and only for keys declared in feature.json ("count" here).

function render(ctx) {
  return '<div class="card"><h3>Counter</h3>' +
    '<p class="note">A reference feature. The value is stored for this learner and profile.</p>' +
    '<p><b id="refCounterValue">…</b></p>' +
    '<button class="btn sm" id="refCounterAdd">Add one</button> <button class="btn sm" id="refCounterReset">Reset</button></div>';
}

function wire(ctx, el) {
  const show = async () => {
    const v = await ctx.store.get("count");
    el.querySelector("#refCounterValue").textContent = String(v === null ? 0 : v);
  };
  const guard = fn => async () => { try { await fn(); } catch (e) { ctx.toast("Could not save: " + (e && e.message || e)); } };
  el.querySelector("#refCounterAdd").onclick = guard(async () => { const v = (await ctx.store.get("count")) || 0; await ctx.store.set("count", v + 1); await show(); });
  el.querySelector("#refCounterReset").onclick = guard(async () => { await ctx.store.remove("count"); await show(); });
  show();
}

return { render, wire };
