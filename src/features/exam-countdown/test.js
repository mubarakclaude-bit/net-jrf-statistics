module.exports = async function (t) {
  const { page, expect } = t;
  await t.open();
  const text = sel => page.textContent(sel);
  const dateOf = days => page.evaluate(n => { const d = new Date(); d.setDate(d.getDate() + n); return [d.getFullYear(), String(d.getMonth() + 1).padStart(2, "0"), String(d.getDate()).padStart(2, "0")].join("-"); }, days);
  const wait = fn => page.waitForFunction(fn, null, { timeout: 10000 });

  expect("renders the exam date input", await page.locator("#examCountdownDate").count() === 1);
  expect("starts with a helpful prompt", (await text("#examCountdownResult")).includes("Choose a date"));

  const future = await dateOf(10);
  await page.locator("#examCountdownDate").fill(future);
  await page.locator("#examCountdownDate").dispatchEvent("change");
  await wait(() => document.querySelector("#examCountdownResult").textContent.includes("10 days remaining"));
  expect("counts days to the selected exam date", (await text("#examCountdownResult")).includes("10 days remaining"));

  // One exam date for the whole app: the same value the Settings page and the header chip use.
  expect("the date is the app's own exam date setting", await page.evaluate(d => S.cfg.exam === d, future));
  const days = await page.evaluate(() => examDays());
  expect("the header chip shows the same date (" + days + " days to exam)", (await text("#hdDays")).includes(days + " days to exam"));

  await page.reload(); await t.open();
  await wait(() => document.querySelector("#examCountdownDate").value !== "");
  expect("restores the selected date after reload", await page.locator("#examCountdownDate").inputValue() === future);
  expect("restores the countdown after reload", (await text("#examCountdownResult")).includes("10 days remaining"));

  // A change made anywhere else in the app shows here too.
  const other = await dateOf(20);
  await page.evaluate(d => FEATURES["exam-countdown"].ctx.app.settings.set({ exam: d }), other);
  await page.waitForFunction(d => document.querySelector("#examCountdownDate").value === d, other, { timeout: 10000 });
  expect("a date set from elsewhere in the app appears here", (await text("#examCountdownResult")).includes("20 days remaining"));

  await page.click("#examCountdownClear");
  await wait(() => document.querySelector("#examCountdownDate").value === "");
  expect("clears the exam date everywhere and resets the prompt",
    (await text("#examCountdownResult")).includes("Choose a date") && (await page.evaluate(() => S.cfg.exam)) === "" && (await text("#hdDays")).includes("set exam date"));

  // Version 1.0.0 kept its own copy at its own storage key. A date saved there is carried over once, then removed.
  await page.evaluate(() => FEATURES["exam-countdown"].ctx.store.set("exam_date", "2031-05-04"));
  await page.reload(); await t.open();
  await wait(() => document.querySelector("#examCountdownDate").value === "2031-05-04");
  expect("a date saved by version 1.0.0 is carried over into the shared setting", await page.evaluate(() => S.cfg.exam === "2031-05-04"));
  expect("and its old storage key is removed afterwards", (await page.evaluate(() => FEATURES["exam-countdown"].ctx.store.get("exam_date"))) === null);

  // The settings interface refuses bad values, with a reason, and changes nothing.
  const bad = await page.evaluate(() => { const s = FEATURES["exam-countdown"].ctx.app.settings, out = {}; for (const [k, v] of [["date", { exam: "next week" }], ["unknown", { colour: "red" }], ["target", { target: "high" }]]) { try { s.set(v); out[k] = "accepted"; } catch (e) { out[k] = String(e.message); } } return out; });
  expect("settings.set refuses a bad date, an unknown setting and a bad target", /exam must be/.test(bad.date) && /unknown setting 'colour'/.test(bad.unknown) && /target must be a number/.test(bad.target), JSON.stringify(bad));
  expect("a refused change leaves the date as it was", await page.evaluate(() => S.cfg.exam === "2031-05-04"));
};
