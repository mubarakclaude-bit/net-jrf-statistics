module.exports = async function (t) {
  const { page, expect } = t;
  await t.open();
  const view = "#v-progress";

  expect("shows the Progress heading and both paper cards",
    (await page.textContent(view + " .hd h1")).trim() === "Progress" && (await page.locator(view + " .grid.g2").first().locator(".card").count()) === 2);

  // The table has one row per module, taken from the app's own numbers rather than a hard-coded count.
  const want = await page.evaluate(() => overall(2).ms.length + overall(1).ms.length);
  expect("the module table has one row for every module (" + want + ")", want > 0 && (await page.locator(view + " .tbl tbody tr").count()) === want);

  const p2 = await page.evaluate(() => Math.round(overall(2).proj));
  expect("the Paper 2 card shows the app's own projection", (await page.textContent(view + " .card h3")).includes(p2 + " of 200 projected"));

  expect("before loading, the format panel asks for the bank to be loaded", (await page.textContent(view)).includes("Hit “Load every module”"));
  await page.click("#loadAllBtn");
  // The button says "Loaded" and the view redraws in the same instant, so wait for the redraw, not for the word.
  await page.waitForFunction(() => !document.querySelector("#v-progress").textContent.includes("Hit “Load every module”"), null, { timeout: 120000 });
  await page.waitForTimeout(500);
  expect("Load every module fills in accuracy by question format", !(await page.textContent(view)).includes("Hit “Load every module”") && (await page.locator(view + " .bar.sm").count()) > 5);

  // The error profile: it appears once there are errors, offers the Ask box from six on, and clears only on a second press.
  expect("with no errors logged it says so", (await page.textContent(view)).includes("Nothing logged yet"));
  await page.evaluate(() => {
    S.errs = Array.from({ length: 7 }, (_, i) => ({ type: ERRT[i % ERRT.length][0], fmt: FORDER[i % FORDER.length], stem: "test stem " + i }));
    render();
  });
  await page.waitForSelector("#errClear");
  expect("logged errors are counted", (await page.textContent(view)).includes("7 logged"));
  expect("six or more errors offer the Ask box", (await page.locator("#ask-err").count()) === 1);
  await page.click("#errClear");
  expect("the first press asks for confirmation and clears nothing",
    /Press again to clear 7/.test(await page.textContent("#errClear")) && (await page.evaluate(() => S.errs.length)) === 7);
  await page.click("#errClear");
  await page.waitForFunction(() => S.errs.length === 0);
  expect("the second press clears the log and the view says so", (await page.textContent(view)).includes("Nothing logged yet"));

  expect("its tab is the built-in Progress tab and is the current one",
    (await page.locator('#nav [data-tab="progress"]').count()) === 1 && (await page.getAttribute('#nav [data-tab="progress"]', "aria-current")) === "true");
};
