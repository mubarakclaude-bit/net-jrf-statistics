/* ===================== front door =====================
   A profile gate, not a security boundary. The artifact is already private to the
   people it is shared with; this decides WHOSE progress you are looking at, and keeps
   a guest's answers out of yours. Said plainly on the screen itself.
*/
const OWNER_P = {id:"me", name:"My own progress", kind:"owner",
  note:"Everything you have already answered, read and been scored on."};

async function loadUsers(){
  if(S.users!==null||!S.db)return S.users;
  try{const s=await S.db.doc("meta/users").get();
    S.users=s.exists?((s.data()||{}).users||[]):[]}
  catch(e){S.users=[]}
  return S.users;
}
function profileName(){
  if(S.profile==="me")return OWNER_P.name;
  const u=(S.users||[]).find(x=>x.id===S.profile);
  return u?u.name:S.profile;
}
function rememberProfile(id){try{localStorage.setItem("njprof",id||"")}catch(e){}}
function recallProfile(){try{return localStorage.getItem("njprof")||""}catch(e){return ""}}

function vAuth(){
  const us=S.users||[];
  const err=S.authErr;
  return '<div class="gatewrap"><div class="gatecard">'+
    '<div class="gatebrand"><span class="gw">NET JRF</span><span class="gs">Statistics · Paper 1 + 2</span></div>'+
    '<p class="gatelede">Pick whose progress to open. Lessons and the question bank are shared; answers, scores and mastery are kept apart per profile.</p>'+
    (!S.db?'<div class="banner bad" style="margin:0 0 14px"><div>This view has no database, so nothing can be loaded or saved. Open the page signed in to the account that owns it.</div></div>':
     !S.uid?'<div class="banner" style="margin:0 0 14px"><div><b>You are not signed in.</b> You can read the lessons, but nothing you answer will be saved anywhere.</div></div>':"")+
    '<button class="plogin owner" data-login="me">'+
      '<span class="pav">'+esc((S.ownerName||"You").slice(0,1).toUpperCase())+'</span>'+
      '<span class="pt"><b>'+esc(S.ownerName?("Continue as "+S.ownerName):"Continue as yourself")+'</b>'+
      '<span class="note">'+esc(OWNER_P.note)+'</span></span>'+
      '<span class="pgo">→</span></button>'+
    (us.length?'<div class="gatesep"><span>or sign in as a test profile</span></div>'+
      us.map(u=>{
        const open=S.askPass===u.id;
        return '<div class="pwrap">'+
          '<button class="plogin" data-login="'+esc(u.id)+'">'+
            '<span class="pav alt">'+esc((u.name||u.id).slice(0,1).toUpperCase())+'</span>'+
            '<span class="pt"><b>'+esc(u.name||u.id)+'</b><span class="note">'+esc(u.note||"Test profile")+'</span></span>'+
            '<span class="pgo">'+(open?"▾":"→")+'</span></button>'+
          (open?'<div class="passrow">'+
            '<input type="password" id="passBox" inputmode="numeric" autocomplete="off" placeholder="passcode" value="'+esc(S.passVal||"")+'">'+
            '<button class="btn p" id="passGo">Open</button></div>'+
            (err?'<p class="note" style="color:var(--bad);margin:6px 0 0">'+esc(err)+'</p>':
                 (u.hint?'<p class="note" style="margin:6px 0 0">Hint: '+esc(u.hint)+'</p>':""))
           :"")+
        '</div>'}).join("")
     :'<p class="note" style="margin-top:14px">No test profiles exist yet. Admin → Test profiles creates one.</p>')+
    '<p class="gatefoot">This gate decides which profile you open, nothing more. It is not a security control — the passcode is stored with the app, so treat anyone who can open this link as able to open any profile on it. Real privacy comes from who the artifact is shared with.</p>'+
  '</div></div>';
}
async function doLogin(id,pass){
  S.authErr="";
  if(id==="me"){S.profile="me";S.authed=true;rememberProfile("me");await loadProfileData();
    await loadFeedback();migrateFeedback();render();return}
  const u=(S.users||[]).find(x=>x.id===id);
  if(!u){S.authErr="That profile no longer exists.";render();return}
  if(u.pass&&String(pass||"")!==String(u.pass)){
    S.authErr="That passcode does not match.";S.passVal="";render();return}
  S.profile=id;S.authed=true;S.passVal="";rememberProfile(id);
  await loadProfileData();await loadFeedback();migrateFeedback();render();
}
function signOut(){
  S.authed=false;S.askPass="";S.passVal="";S.authErr="";
  rememberProfile("");
  S.att={};S.mocks=[];S.topics={};S.errs=[];S.mastery={};S.cfg=Object.assign({},S.cfg);
  resetLearn(null);S.drill=null;S.mock=null;S.route="home";
  render();
}
