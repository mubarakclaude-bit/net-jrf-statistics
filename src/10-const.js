const BUILD="2026-11-05 18:03 UTC";
/* ===================== constants ===================== */
const TABS=[["home","Home"],["learn","Learn"],["bank","Question bank"],["mock","Mock tests"],["progress","Progress"],["admin","Admin"]];
const FMT={
  single:{n:"Single concept",s:"Single",mix:50,base:[18,50],hint:"One fact or formula. Say it before you look at the options."},
  numeric:{n:"Numerical",s:"Numeric",mix:21,base:[4,21],hint:"Compute, then check you are reporting the quantity actually asked."},
  multi:{n:"Multi-statement",s:"Multi",mix:19,base:[2,19],hint:"A separate true/false verdict on every statement, before the options."},
  match:{n:"Match the list",s:"Match",mix:7,base:[5,7],hint:"Match every row yourself first, then look for the option that agrees."},
  order:{n:"Arrange in order",s:"Order",mix:3,base:[2,3],hint:"Fix the two extremes first, then order the middle."}
};
const FORDER=["single","numeric","multi","match","order"];
const EXT={Derive:{c:"bad",d:"Derive it on paper from scratch"},Apply:{c:"mid",d:"Apply the result to a problem"},Recall:{c:"ac",d:"Recall statement and conditions"},State:{c:"dim",d:"Recognise the name and the claim"}};
// Exam weight. The module's marks are real; the split within a module is editorial.
const IMP={3:{n:"Core",s:"★★★",c:"bad",d:"Heavily examined — expect it on every paper"},
           2:{n:"Important",s:"★★",c:"mid",d:"Appears regularly"},
           1:{n:"Supporting",s:"★",c:"dim",d:"Occasional, or needed to understand the rest"}};
const DIFF={easy:{n:"Easy",c:"ok"},moderate:{n:"Moderate",c:"mid"},hard:{n:"Hard",c:"bad"}};
const ERRT=[["quantity","Right working, reported the wrong quantity"],["term","Dropped or added a term"],["df","Wrong df / n vs n−1 / wrong parameter slot"],["sign","Sign or inequality direction"],["misread","Misread the statement or the question"],["formula","Recalled the formula wrongly"],["gap","Concept genuinely not known"],["rush","Careless under exam pace"]];
const PACE=48; // seconds per question in the real paper (150 questions, 2 hours)
const SHRINK=8; // pseudo-counts pulling an under-sampled module toward its June 2026 accuracy
const SCHEMA=4;

const REQKIND=[["detail","More detail"],["example","Worked example"],["visual","Diagram"],
  ["practice","Practice questions"],["real","Real-world use"],["bug","Something is wrong"]];
