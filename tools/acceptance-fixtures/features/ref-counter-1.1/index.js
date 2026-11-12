// Reference feature, version 1.1: a counter with a selectable step size. Both the value and the step are remembered per
// learner and profile. This file runs inside its own private scope. It must end with:  return { render, wire };

function render(ctx) {
  return '<div class="card"><h3>Counter</h3>' +
    '<p class="note">A reference feature. The value and the step are stored for this learner and profile.</p>' +
    '<p><label>Step <select id="refCounterStep"><option value="1">1</option><option value="5">5</option><option value="10">10</option></select></label></p>' +
    '<p><b id="refCounterValue">…</b></p>' +
    '<button class="btn sm" id="refCounterAdd">Add</button> <button class="btn sm" id="refCounterReset">Reset</button></div>';
}

function wire(ctx, el) {
  const stepEl = el.querySelector("#refCounterStep");
  const show = async () => {
    const v = await ctx.store.get("count");
    el.querySelector("#refCounterValue").textContent = String(v === null ? 0 : v);
  };
  const guard = fn => async () => { try { await fn(); } catch (e) { ctx.toast("Could not save: " + (e && e.message || e)); } };
  el.querySelector("#refCounterAdd").onclick = guard(async () => {
    const step = Number(stepEl.value) || 1, v = (await ctx.store.get("count")) || 0;
    await ctx.store.set("count", v + step); await show();
  });
  el.querySelector("#refCounterReset").onclick = guard(async () => { await ctx.store.remove("count"); await show(); });
  stepEl.onchange = guard(async () => { await ctx.store.set("step", Number(stepEl.value) || 1); });
  ctx.store.get("step").then(s => { if (s) stepEl.value = String(s); });
  show();
}

return { render, wire };
