// Reference feature: a read-only view with no storage. It must end with:  return { render, wire };

function render(ctx) {
  return '<div class="card"><h3>About this build</h3>' +
    '<p class="kv"><span>Build</span><b id="refAboutBuild">' + ctx.esc(BUILD) + '</b></p>' +
    '<p class="kv"><span>Profile</span><b id="refAboutProfile">' + ctx.esc(ctx.profile) + '</b></p>' +
    '<p class="kv"><span>Feature version</span><b id="refAboutVersion">' + ctx.esc(ctx.version) + '</b></p></div>';
}

return { render };
