module.exports = async function (t) {
  const { page, expect } = t;
  await t.open();

  expect("renders the exam date input", await page.locator("#examCountdownDate").count() === 1);
  expect("starts with a helpful prompt", (await page.textContent("#examCountdownResult")).includes("Choose a date"));

  const future = await page.evaluate(() => {
    const d = new Date();
    d.setDate(d.getDate() + 10);
    return [d.getFullYear(), String(d.getMonth() + 1).padStart(2, "0"), String(d.getDate()).padStart(2, "0")].join("-");
  });
  await page.locator("#examCountdownDate").fill(future);
  await page.locator("#examCountdownDate").dispatchEvent("change");
  await page.waitForFunction(() => document.querySelector("#examCountdownResult").textContent.includes("10 days remaining"));
  expect("counts days to the selected exam date", (await page.textContent("#examCountdownResult")).includes("10 days remaining"));

  const stored = await page.evaluate(() => {
    const uid = localStorage.getItem("njuid");
    const raw = localStorage.getItem("njdb:data/users/" + uid + "/features/exam-countdown/exam_date");
    return raw ? JSON.parse(raw).value : null;
  });
  expect("stores the learner's selected date at the feature contract path", stored === future, stored);

  await page.reload();
  await t.open();
  await page.waitForFunction(() => document.querySelector("#examCountdownDate").value !== "");
  expect("restores the selected date after reload", await page.locator("#examCountdownDate").inputValue() === future);
  expect("restores the countdown after reload", (await page.textContent("#examCountdownResult")).includes("10 days remaining"));

  await page.click("#examCountdownClear");
  await page.waitForFunction(() => document.querySelector("#examCountdownDate").value === "");
  expect("clears the saved date and resets the prompt", (await page.textContent("#examCountdownResult")).includes("Choose a date"));
};
