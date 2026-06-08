const originalDrawScope=drawScope;
let lastScopeStart=0;

function drawHeldScopeGrid(){
  const w=canvas.width,h=canvas.height;
  g.clearRect(0,0,w,h);
  g.fillStyle='rgba(13,15,20,.96)';
  g.fillRect(0,0,w,h);
  g.strokeStyle='rgba(143,167,196,.16)';
  g.lineWidth=1;
  for(let x=0;x<=w;x+=w/8){g.beginPath();g.moveTo(x,0);g.lineTo(x,h);g.stroke()}
  for(let y=0;y<=h;y+=h/4){g.beginPath();g.moveTo(0,y);g.lineTo(w,h);g.stroke()}
  g.strokeStyle='rgba(202,160,106,.28)';
  g.beginPath();g.moveTo(0,h/2);g.lineTo(w,h/2);g.stroke();
}

function liveStats(data){
  let lo=255,hi=0;
  for(const v of data){lo=Math.min(lo,v);hi=Math.max(hi,v)}
  return {lo,hi,span:hi-lo,mid:(lo+hi)/2};
}

function findLiveTrigger(data,stats,visible){
  if(stats.span<3)return 0;
  const limit=Math.max(24,data.length-visible-2);
  let best=-1;
  let bestDistance=Infinity;
  for(let i=16;i<limit;i++){
    const rising=data[i-1]<stats.mid&&data[i]>=stats.mid;
    const slope=data[Math.min(i+2,data.length-1)]-data[Math.max(i-2,0)];
    if(rising&&slope>0){
      const distance=Math.abs(i-lastScopeStart);
      if(distance<bestDistance){best=i;bestDistance=distance}
    }
  }
  if(best>=0){lastScopeStart=best;return best}
  return lastScopeStart||0;
}

function drawTrueLiveScope(){
  if(!analyser||!scopeData){originalDrawScope();return}
  analyser.getByteTimeDomainData(scopeData);
  const w=canvas.width,h=canvas.height;
  const visible=Math.min(scopeData.length-32,Math.max(256,Math.round((ctx?.sampleRate||48000)*.018)));
  const stats=liveStats(scopeData);
  const start=findLiveTrigger(scopeData,stats,visible);
  const gain=(h*.34)/Math.max(4,stats.span/2);

  drawHeldScopeGrid();
  g.strokeStyle='rgba(242,240,234,.92)';
  g.lineWidth=2;
  g.beginPath();

  for(let x=0;x<w;x++){
    const idx=Math.min(scopeData.length-1,start+Math.floor((x/w)*visible));
    const y=Math.max(4,Math.min(h-4,(h/2)-((scopeData[idx]-stats.mid)*gain)));
    if(x===0)g.moveTo(x,y);else g.lineTo(x,y);
  }

  g.stroke();
}

drawScope=function patchedDrawScope(){
  const active=Object.values(voices).some(voice=>voice&&!voice.released);
  if(active){
    drawTrueLiveScope();
    requestAnimationFrame(drawScope);
    return;
  }
  originalDrawScope();
};
