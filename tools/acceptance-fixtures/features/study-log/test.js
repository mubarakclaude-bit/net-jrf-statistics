module.exports = async function (t) {
  const { page, expect } = t;
  const total = async want => { await page.waitForFunction(w => document.querySelector("#studyLogTotal").textContent.trim() === w, want); return (await page.textContent("#studyLogTotal")).trim(); };
  await t.open();
  expect("starts at zero", (await total("0")) === "0");
  await page.fill("#studyLogMinutes", "25"); await page.click("#studyLogAdd");
  expect("logging minutes raises the total", (await total("25")) === "25");
  await page.fill("#studyLogMinutes", "35"); await page.click("#studyLogAdd");
  expect("a second entry on the same day adds to that day, not a new day", (await total("60")) === "60" && (await page.textContent("#studyLogDays")).trim() === "1");
  await page.fill("#studyLogMinutes", "0"); await page.click("#studyLogAdd");
  expect("an invalid amount is refused with a message and changes nothing", /1 to 600/.test(await page.textContent("#studyLogMessage")) && (await total("60")) === "60");
  await page.reload(); await t.open();
  expect("the log persists across a reload", (await total("60")) === "60");
  const other = await page.evaluate(async () => {   // another profile keeps its own log, at the profile path
    const old = S.profile; S.profile = "demo";
    try { await FEATURES["study-log"].ctx.store.set("entries", [{ date: "2026-01-01", minutes: 5 }]); } finally { S.profile = old; }
    return localStorage.getItem("njdb:data/users/" + localStorage.getItem("njuid") + "/p/demo/features/study-log/entries");
  });
  expect("another profile is stored separately and the default log is untouched", !!other && (await page.textContent("#studyLogTotal")).trim() === "60");
};
