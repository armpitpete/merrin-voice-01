let heldScopeImage=null;
let heldScopeAt=0;
let lastLockedStart=0;
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

function scopeStats(data){
  let lo=255,hi=0;
  for(const v of data){lo=Math.min(lo,v);hi=Math.max(hi,v)}
  return {lo,hi,span:hi-lo,mid:(lo+hi)/2};
}

function findLockedStart(data,stats,visible){
  if(stats.span<2)return null;
  const minSlope=Math.max(1,stats.span*.05);
  const limit=Math.max(16,data.length-visible-4);
  for(let i=12;i<limit;i++){
    const rising=data[i-1]<stats.mid&&data[i]>=stats.mid;
    const slope=data[Math.min(i+2,data.length-1)]-data[Math.max(i-2,0)];
    if(rising&&slope>=minSlope){
      lastLockedStart=i;
      return i;
    }
  }
  return lastLockedStart||0;
}

function drawLockedScope(){
  drawHeldScopeGrid();
  if(!analyser||!scopeData){
    g.strokeStyle='rgba(242,240,234,.92)';
    g.beginPath();g.moveTo(0,canvas.height/2);g.lineTo(canvas.width,canvas.height/2);g.stroke();
    return;
  }
  analyser.getByteTimeDomainData(scopeData);
  const stats=scopeStats(scopeData);
  const w=canvas.width,h=canvas.height,visible=640;
  const start=findLockedStart(scopeData,stats,visible);
  if(start===null){
    g.strokeStyle='rgba(242,240,234,.92)';
    g.beginPath();g.moveTo(0,h/2);g.lineTo(w,h/2);g.stroke();
    return;
  }
  const targetHalfHeight=h*.34;
  const displayGain=Math.min(10,Math.max(1,targetHalfHeight/Math.max(1,stats.span/2)));
  const points=[];
  for(let x=0;x<w;x++){
    const sample=Math.min(scopeData.length-1,start+Math.floor((x/w)*visible));
    const y=(h/2)-((scopeData[sample]-stats.mid)*displayGain);
    points.push([x,Math.max(4,Math.min(h-4,y))]);
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
