// Version 1.1 of the feature's own test: every behaviour of 1.0 still holds, plus the new step size.
module.exports = async function (t) {
  const { page, expect } = t;
  const value = async want => { await page.waitForFunction(w => document.querySelector("#refCounterValue").textContent.trim() === w, want); return (await page.textContent("#refCounterValue")).trim(); };
  await t.open();
  expect("draws its view", await page.locator("#refCounterAdd").count() === 1);
  expect("starts at 0", (await value("0")) === "0");
  await page.click("#refCounterAdd"); await page.click("#refCounterAdd");
  expect("counts by the default step of 1", (await value("2")) === "2");

  await page.selectOption("#refCounterStep", "5"); await page.click("#refCounterAdd");
  expect("counts by the chosen step of 5", (await value("7")) === "7");

  const U = await page.evaluate(() => localStorage.getItem("njuid"));
  const at = k => page.evaluate(([u, key]) => localStorage.getItem("njdb:data/users/" + u + "/features/ref-counter/" + key), [U, k]);
  expect("stores the value at the contract path .../features/ref-counter/count", JSON.parse(await at("count")).value === 7);
  expect("stores the step at its own declared key .../features/ref-counter/step", JSON.parse(await at("step")).value === 5);

  await page.reload(); await t.open();
  expect("the value survives a reload", (await value("7")) === "7");
  await page.waitForFunction(() => document.querySelector("#refCounterStep").value === "5");
  expect("the chosen step survives a reload", (await page.inputValue("#refCounterStep")) === "5");

  const undeclared = await page.evaluate(async () => { try { await FEATURES["ref-counter"].ctx.store.set("not_declared", 1); return "accepted"; } catch (e) { return e.message; } });
  expect("a storage key not declared in feature.json is still refused", /not declared/.test(undeclared), undeclared);

  const scoped = await page.evaluate(async () => {
    const old = S.profile; S.profile = "demo";
    try { await FEATURES["ref-counter"].ctx.store.set("count", 3); } finally { S.profile = old; }
    return localStorage.getItem("njdb:data/users/" + localStorage.getItem("njuid") + "/p/demo/features/ref-counter/count");
  });
  expect("a non-default profile is stored under p/<profile>/ and does not touch the default", !!scoped && (await value("7")) === "7");

  await page.click("#refCounterReset");
  expect("reset clears the stored value but keeps the step", (await value("0")) === "0" && (await at("count")) === null && JSON.parse(await at("step")).value === 5);
};
