let heldScopeImage=null;
let heldScopeAt=0;
const originalDrawScope=drawScope;

function drawHeldScopeGrid(){
  const w=canvas.width,h=canvas.height;
  g.clearRect(0,0,w,h);
  g.fillStyle='rgba(13,15,20,.96)';
  g.fillRect(0,0,w,h);
  g.strokeStyle='rgba(143,167,196,.16)';
  g.lineWidth=1;
  for(let x=0;x<=w;x+=w/8){g.beginPath();g.moveTo(x,0);g.lineTo(x,h);g.stroke()}
  for(let y=0;y<=h;y+=h/4){g.beginPath();g.moveTo(0,y);g.lineTo(w,y);g.stroke()}
  g.strokeStyle='rgba(202,160,106,.28)';
  g.beginPath();g.moveTo(0,h/2);g.lineTo(w,h/2);g.stroke();
}

function findLockedStart(data){
  let lo=255,hi=0;
  for(const v of data){lo=Math.min(lo,v);hi=Math.max(hi,v)}
  const span=hi-lo;
  if(span<8)return null;
  const mid=(lo+hi)/2;
  const minSlope=Math.max(3,span*.12);
  for(let i=12;i<data.length-900;i++){
    const rising=data[i-1]<mid&&data[i]>=mid;
    const slope=data[i+2]-data[i-2];
    if(rising&&slope>=minSlope)return i;
  }
  return null;
}

function drawLockedScope(){
  drawHeldScopeGrid();
  if(!analyser||!scopeData){
    g.strokeStyle='rgba(242,240,234,.92)';
    g.beginPath();g.moveTo(0,canvas.height/2);g.lineTo(canvas.width,canvas.height/2);g.stroke();
    return;
  }
  analyser.getByteTimeDomainData(scopeData);
  const start=findLockedStart(scopeData);
  if(start===null){
    if(heldScopeImage)g.putImageData(heldScopeImage,0,0);
    return;
  }
  const w=canvas.width,h=canvas.height,visible=640;
  const points=[];
  for(let x=0;x<w;x++){
    const sample=start+Math.floor((x/w)*visible);
    const y=(h/2)-((scopeData[sample]-128)/128)*h*.42;
    points.push([x,y]);
  }
  g.strokeStyle='rgba(242,240,234,.92)';
  g.lineWidth=2;
  g.beginPath();
  points.forEach(([x,y],i)=>i?g.lineTo(x,y):g.moveTo(x,y));
  g.stroke();
  heldScopeImage=g.getImageData(0,0,w,h);
  heldScopeAt=performance.now();
}

drawScope=function patchedDrawScope(){
  const active=Object.values(voices).some(voice=>voice&&!voice.released);
  if(active){
    drawLockedScope();
    requestAnimationFrame(drawScope);
    return;
  }
  heldScopeImage=null;
  originalDrawScope();
};
