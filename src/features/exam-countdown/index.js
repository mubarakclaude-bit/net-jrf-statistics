// A learner-configurable countdown. The official exam date is not assumed;
// each learner enters the date relevant to their exam cycle.

function render() {
  return '<div class="card">' +
    '<h3>NET JRF exam countdown</h3>' +
    '<p class="note">Choose your exam date to see how much preparation time remains.</p>' +
    '<label for="examCountdownDate">Your exam date</label>' +
    '<input id="examCountdownDate" type="date" />' +
    '<p id="examCountdownResult" class="note" aria-live="polite">Choose a date to start your countdown.</p>' +
    '<button class="btn sm" id="examCountdownClear" type="button">Clear date</button>' +
    '</div>';
}

function wire(ctx, el) {
  const dateInput = el.querySelector("#examCountdownDate");
  const result = el.querySelector("#examCountdownResult");

  function updateResult(value) {
    if (!value) {
      result.textContent = "Choose a date to start your countdown.";
      return;
    }
    const parts = value.split("-").map(Number);
    if (parts.length !== 3 || !parts.every(Number.isFinite)) {
      result.textContent = "Please choose a valid exam date.";
      return;
    }
    const target = Date.UTC(parts[0], parts[1] - 1, parts[2]);
    const now = new Date();
    const today = Date.UTC(now.getFullYear(), now.getMonth(), now.getDate());
    const days = Math.round((target - today) / 86400000);
    if (days > 1) result.textContent = days + " days remaining. Keep preparing!";
    else if (days === 1) result.textContent = "1 day remaining. You are almost there!";
    else if (days === 0) result.textContent = "Your exam is today. Best of luck!";
    else result.textContent = "This exam date has passed. You can choose a new date.";
  }

  const guard = fn => async () => {
    try { await fn(); }
    catch (e) { ctx.toast("Could not save: " + (e && e.message || e)); }
  };

  guard(async () => {
    const saved = await ctx.store.get("exam_date");
    if (typeof saved === "string") dateInput.value = saved;
    updateResult(dateInput.value);
  })();

  dateInput.addEventListener("change", guard(async () => {
    const value = dateInput.value;
    if (value) await ctx.store.set("exam_date", value);
    else await ctx.store.remove("exam_date");
    updateResult(value);
  }));

  el.querySelector("#examCountdownClear").onclick = guard(async () => {
    await ctx.store.remove("exam_date");
    dateInput.value = "";
    updateResult("");
  });
}

return { render, wire };
