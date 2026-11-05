/* ===================== state ===================== */
const S={db:null,user:null,uid:null,sampleFn:null,dl:null,
  catalog:null,index:null,app:null,bank:{},notes:{},loading:{},
  lessonIdx:null,lessons:{},sets:{},mastery:{},personal:null,syl:null,
  att:{},mocks:[],topics:{},errs:[],cfg:{},
  users:null,profile:"me",authed:false,askPass:"",passVal:"",authErr:"",ownerName:"",
  ready:false,topH:0,focus:true,dbMsg:"",boot:"",perm:null,permState:null,readErr:"",diag:null,gen:null,route:"home",open:{},pickMod:"",
  mode:"pyq",paper:2,navW:286,aideW:300,reqs:[],reqUI:{},notes:{},noteUI:{},reqModal:null,asks:[],ask:null,askChip:null,isAdmin:false,fb:null,fbErr:"",
  mode2:null,navOpen:((typeof window!=="undefined"&&window.innerWidth)||1200)>980,
  aideOpen:((typeof window!=="undefined"&&window.innerWidth)||1200)>980,
  learn:{topicId:null,lessonId:null,i:-1,seen:{},viz:{},steps:{},reveal:{},blanks:{},
         hints:{},verd:{},solShown:{},said:{},nudge:{},flip:{},scen:{},found:{},quiz:null,showRev:false},
  filt:{mod:"",fmt:"",src:"",st:"",paper:""},drill:null,mock:null};
function resetLearn(tid){
  S.learn={topicId:tid||null,lessonId:null,i:-1,seen:{},viz:{},steps:{},reveal:{},blanks:{},
    hints:{},verd:{},solShown:{},said:{},nudge:{},flip:{},scen:{},found:{},quiz:null,showRev:false};
  if(tid){const st=S.topics[tid]||{};(st.seen||[]).forEach(id=>{S.learn.seen[id]=1})}
}
