// The feature's own browser test. tests/features.test.js runs it against the built site, in strict storage-path mode,
// and fails the feature on any page error. t = { page, open, expect, id }.
module.exports = async function (t) {
  const { page, expect } = t;
  await t.open();
  expect("draws its view", await page.locator("#refCounterAdd").count() === 1);
  expect("starts at 0", (await page.textContent("#refCounterValue")).trim() === "0");
  await page.click("#refCounterAdd"); await page.click("#refCounterAdd");
  await page.waitForFunction(() => document.querySelector("#refCounterValue").textContent.trim() === "2");
  expect("counts", (await page.textContent("#refCounterValue")).trim() === "2");

  const U = await page.evaluate(() => localStorage.getItem("njuid"));
  const stored = await page.evaluate(u => localStorage.getItem("njdb:data/users/" + u + "/features/ref-counter/count"), U);
  expect("stores at the contract path data/users/<uid>/features/ref-counter/count", !!stored && JSON.parse(stored).value === 2, stored);

  await page.reload(); await t.open();
  await page.waitForFunction(() => document.querySelector("#refCounterValue").textContent.trim() !== "…");
  expect("the value survives a reload", (await page.textContent("#refCounterValue")).trim() === "2");

  const undeclared = await page.evaluate(async () => { try { await FEATURES["ref-counter"].ctx.store.set("not_declared", 1); return "accepted"; } catch (e) { return e.message; } });
  expect("a storage key not declared in feature.json is refused", /not declared/.test(undeclared), undeclared);

  const scoped = await page.evaluate(async () => {   // another profile gets its own copy at the profile path
    const old = S.profile; S.profile = "demo";
    try { await FEATURES["ref-counter"].ctx.store.set("count", 7); } finally { S.profile = old; }
    return localStorage.getItem("njdb:data/users/" + localStorage.getItem("njuid") + "/p/demo/features/ref-counter/count");
  });
  expect("a non-default profile is stored under p/<profile>/ and does not touch the default", !!scoped && JSON.parse(scoped).value === 7 && (await page.textContent("#refCounterValue")).trim() === "2", scoped);

  await page.click("#refCounterReset");
  await page.waitForFunction(() => document.querySelector("#refCounterValue").textContent.trim() === "0");
  expect("reset clears the stored value", (await page.evaluate(u => localStorage.getItem("njdb:data/users/" + u + "/features/ref-counter/count"), U)) === null);
};
