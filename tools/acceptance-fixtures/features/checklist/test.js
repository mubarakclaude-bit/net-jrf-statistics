module.exports = async function (t) {
  const { page, expect } = t;
  const text = sel => page.textContent(sel).then(s => s.trim());
  const remaining = async want => { await page.waitForFunction(w => document.querySelector("#checklistRemaining").textContent.trim() === w, want); return text("#checklistRemaining"); };
  await t.open();
  expect("starts with nothing to do", (await remaining("0 remaining of 0")) === "0 remaining of 0");
  for (const item of ["Read the chapter", "Verify the figures", "Do the mastery test"]) { await page.fill("#checklistText", item); await page.click("#checklistAdd"); }
  expect("adds items and counts them", (await remaining("3 remaining of 3")) === "3 remaining of 3");
  await page.check('input[data-checklist-tick="1"]');
  expect("ticking an item lowers the remaining count", (await remaining("2 remaining of 3")) === "2 remaining of 3");
  await page.fill("#checklistText", "<b>not bold</b>"); await page.press("#checklistText", "Enter");
  expect("an item typed with HTML is shown as text, not interpreted", (await page.innerHTML("#checklistList")).indexOf("&lt;b&gt;not bold") >= 0);
  await page.reload(); await t.open();
  expect("the list persists across a reload", (await remaining("3 remaining of 4")) === "3 remaining of 4" && await page.isChecked('input[data-checklist-tick="1"]'));
  await page.click('button[data-checklist-del="0"]');
  expect("removing an item updates the count", (await remaining("2 remaining of 3")) === "2 remaining of 3");
  const U = await page.evaluate(() => localStorage.getItem("njuid"));
  const stored = await page.evaluate(u => localStorage.getItem("njdb:data/users/" + u + "/features/checklist/items"), U);
  expect("saves at the contract path data/users/<uid>/features/checklist/items", !!stored && JSON.parse(stored).value.length === 3, stored && stored.slice(0, 80));
  const undeclared = await page.evaluate(async () => { try { await FEATURES["checklist"].ctx.store.set("not_declared", 1); return "accepted"; } catch (e) { return e.message; } });
  expect("a key it did not declare is refused", /not declared/.test(undeclared));
};
