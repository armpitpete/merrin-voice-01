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

function triangleWave(phase){
  return (2/Math.PI)*Math.asin(Math.sin(phase));
}

function drawStableDryVoiceScope(){
  const activeVoices=Object.values(voices).filter(voice=>voice&&!voice.released);
  if(!activeVoices.length){
    originalDrawScope();
    return;
  }

  drawHeldScopeGrid();

  const w=canvas.width,h=canvas.height;
  const currentTone=tone();
  const subWeight=weightLevel();
  const minFreq=Math.max(55,Math.min(...activeVoices.map(voice=>voice.note.freq)));
  const visibleCycles=4;
  const duration=visibleCycles/minFreq;
  const samples=[];
  let peak=0;

  for(let x=0;x<w;x++){
    const t=(x/w)*duration;
    let v=0;

    activeVoices.forEach(voice=>{
      const f=voice.note.freq;
      v+=Math.sin(2*Math.PI*f*t)*currentTone.sine;
      if(effects.sub)v+=Math.sin(2*Math.PI*(f*.5)*t)*currentTone.sub*subWeight;
      if(effects.overtone)v+=triangleWave(2*Math.PI*(f*2)*t)*currentTone.over;
      if(effects.filter&&!effects.sub&&!effects.overtone)v+=triangleWave(2*Math.PI*(f*3)*t)*.14;
    });

    v/=Math.max(1,activeVoices.length);
    samples.push(v);
    peak=Math.max(peak,Math.abs(v));
  }

  const displayScale=(h*.36)/Math.max(.05,peak);
  g.strokeStyle='rgba(242,240,234,.92)';
  g.lineWidth=2;
  g.beginPath();

  samples.forEach((v,x)=>{
    const y=Math.max(4,Math.min(h-4,(h/2)-(v*displayScale)));
    if(x===0)g.moveTo(x,y);
    else g.lineTo(x,y);
  });

  g.stroke();
}

drawScope=function patchedDrawScope(){
  const active=Object.values(voices).some(voice=>voice&&!voice.released);
  if(active){
    drawStableDryVoiceScope();
    requestAnimationFrame(drawScope);
    return;
  }
  originalDrawScope();
};
