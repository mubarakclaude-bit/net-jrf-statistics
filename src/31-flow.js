/* ===================== flow diagrams =====================
   Declarative, theme-aware, no library. The author gives nodes on a grid and the
   edges between them; layout is explicit so a diagram cannot come out tangled.
     nodes: [{id, r, c, w?, label, kind?: step|decision|start|end|note}]
     edges: [{from, to, label?, side?: "l"|"r"}]
*/
const FW={cell:168,gapx:26,rowh:66,gapy:34,pad:14};
function flowSVG(d){
  const nodes=d.nodes||[],edges=d.edges||[];
  if(!nodes.length)return"";
  let maxR=0,maxC=0;
  nodes.forEach(n=>{maxR=Math.max(maxR,n.r);maxC=Math.max(maxC,n.c+(n.w||1)-1)});
  const W=FW.pad*2+(maxC+1)*FW.cell+maxC*FW.gapx;
  const H=FW.pad*2+(maxR+1)*FW.rowh+maxR*FW.gapy;
  const box=n=>{
    const w=(n.w||1)*FW.cell+((n.w||1)-1)*FW.gapx;
    return{x:FW.pad+n.c*(FW.cell+FW.gapx),y:FW.pad+n.r*(FW.rowh+FW.gapy),w:w,h:FW.rowh,
           cx:FW.pad+n.c*(FW.cell+FW.gapx)+w/2,cy:FW.pad+n.r*(FW.rowh+FW.gapy)+FW.rowh/2};
  };
  const byId={};nodes.forEach(n=>{byId[n.id]=box(n)});
  const wrap=(t,per)=>{
    const words=String(t).split(/\s+/),out=[];let line="";
    words.forEach(w=>{if((line+" "+w).trim().length>per){out.push(line.trim());line=w}else line+=" "+w});
    if(line.trim())out.push(line.trim());return out.slice(0,3);
  };
  const path=(a,b)=>{
    // down, or across then down — always orthogonal so nothing crosses a label
    if(Math.abs(a.cx-b.cx)<2)return"M"+a.cx+" "+(a.y+a.h)+" L"+b.cx+" "+(b.y-7);
    const my=(a.y+a.h+b.y)/2;
    return"M"+a.cx+" "+(a.y+a.h)+" L"+a.cx+" "+my+" L"+b.cx+" "+my+" L"+b.cx+" "+(b.y-7);
  };
  const ed=edges.map(e=>{
    const a=byId[e.from],b=byId[e.to];if(!a||!b)return"";
    const mid=Math.abs(a.cx-b.cx)<2?{x:a.cx+9,y:(a.y+a.h+b.y)/2}:{x:(a.cx+b.cx)/2,y:(a.y+a.h+b.y)/2-6};
    return'<path d="'+path(a,b)+'" class="fe" marker-end="url(#fa)"/>'+
      (e.label?'<text class="fel" x="'+mid.x+'" y="'+mid.y+'" text-anchor="middle">'+richText(e.label)+'</text>':"");
  }).join("");
  const nd=nodes.map(n=>{
    const b=byId[n.id],k=n.kind||"step";
    const lines=wrap(n.label,k==="decision"?22:24);
    const y0=b.cy-(lines.length-1)*8;
    const shape=k==="decision"
      ?'<path class="fn fd" d="M'+b.cx+' '+b.y+' L'+(b.x+b.w)+' '+b.cy+' L'+b.cx+' '+(b.y+b.h)+' L'+b.x+' '+b.cy+' Z"/>'
      :'<rect class="fn f-'+k+'" x="'+b.x+'" y="'+b.y+'" width="'+b.w+'" height="'+b.h+'" rx="'+(k==="start"||k==="end"?FW.rowh/2:9)+'"/>';
    return shape+lines.map((t,i)=>
      '<text class="fnt" x="'+b.cx+'" y="'+(y0+i*16)+'" text-anchor="middle" dominant-baseline="middle">'+esc(t)+'</text>').join("");
  }).join("");
  return'<svg class="flow" viewBox="0 0 '+W+' '+H+'" role="img" aria-label="'+esc(d.alt||d.title||"flow diagram")+'">'+
    '<defs><marker id="fa" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'+
      '<path d="M0 0 L10 5 L0 10 z" class="fam"/></marker></defs>'+ed+nd+'</svg>';
}
function flowBlock(d){
  if(!d||!(d.nodes||[]).length)return"";
  return'<figure class="flowbox">'+(d.title?'<figcaption>'+esc(d.title)+'</figcaption>':"")+
    '<div class="flowscroll">'+flowSVG(d)+'</div>'+
    (d.note?'<p class="vnote">'+richText(d.note)+'</p>':"")+'</figure>';
}
