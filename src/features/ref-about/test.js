module.exports = async function (t) {
  const { page, expect } = t;
  await t.open();
  expect("shows the build stamp", /^\d{4}-\d{2}-\d{2}/.test((await page.textContent("#refAboutBuild")).trim()), await page.textContent("#refAboutBuild"));
  expect("shows the selected profile", (await page.textContent("#refAboutProfile")).trim() === "me");
  expect("shows the feature version from its manifest", (await page.textContent("#refAboutVersion")).trim() === "1.0.0");
  const wrote = await page.evaluate(() => Object.keys(localStorage).filter(k => k.indexOf("features/ref-about") >= 0));
  expect("writes nothing to storage (it declares no keys)", wrote.length === 0, wrote.join(","));
};
