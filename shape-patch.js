state.shape='pure';
labels.pure='Pure';
labels.hollow='Hollow';
labels.pressed='Pressed';

const originalTone=tone;
tone=function shapedTone(){
  const base=originalTone();
  const shape=state.shape||'pure';
  const shaped={...base};

  if(shape==='hollow'){
    shaped.sine=base.sine*.72;
    shaped.sub=base.sub*.68;
    shaped.over=base.over+0.13;
    shaped.cut=base.cut*(effects.overtone?0.96:1.08);
    shaped.q=base.q*.96;
  }

  if(shape==='pressed'){
    shaped.sine=base.sine*.58;
    shaped.sub=base.sub*.48;
    shaped.over=base.over+0.22;
    shaped.cut=base.cut*(effects.overtone?0.92:1.12);
    shaped.q=base.q*.84;
  }

  if(effects.overtone){
    shaped.over*=shape==='pressed'?0.92:0.86;
    shaped.cut*=state.tone==='bright'?0.82:0.92;
  }

  return shaped;
};

const originalWeightLevel=weightLevel;
weightLevel=function shapedWeightLevel(){
  const base=originalWeightLevel();
  const shape=state.shape||'pure';
  const heldCount=Object.values(voices).filter(voice=>voice&&!voice.released).length;
  let shaped=base;

  if(shape==='hollow')shaped*=0.9;
  if(shape==='pressed')shaped*=0.72;
  if(heldCount>=2)shaped*=0.82;
  if(heldCount>=3)shaped*=0.72;

  return shaped;
};

function addShapeSourceToVoice(voice){
  if(!ctx||!voice||!voice.amp||voice.shapeSourceAdded)return;
  const shape=state.shape||'pure';
  if(shape==='pure')return;

  const now=ctx.currentTime;
  const body=ctx.createOscillator();
  const bodyGain=ctx.createGain();

  body.type='triangle';
  body.frequency.setValueAtTime(voice.note.freq,now);
  bodyGain.gain.setValueAtTime(shape==='hollow'?0.55:0.68,now);
  body.connect(bodyGain);
  bodyGain.connect(voice.amp);
  body.start(now);
  try{body.stop(now+12)}catch(e){}
  voice.oscillators.push(body);

  if(shape==='hollow'){
    const hollow=ctx.createOscillator();
    const hollowGain=ctx.createGain();
    hollow.type='sine';
    hollow.frequency.setValueAtTime(voice.note.freq*1.5,now);
    hollowGain.gain.setValueAtTime(0.16,now);
    hollow.connect(hollowGain);
    hollowGain.connect(voice.amp);
    hollow.start(now);
    try{hollow.stop(now+12)}catch(e){}
    voice.oscillators.push(hollow);
  }

  if(shape==='pressed'){
    const ache=ctx.createOscillator();
    const acheGain=ctx.createGain();
    ache.type='triangle';
    ache.frequency.setValueAtTime(voice.note.freq*2,now);
    acheGain.gain.setValueAtTime(0.28,now);
    ache.connect(acheGain);
    acheGain.connect(voice.amp);
    ache.start(now);
    try{ache.stop(now+12)}catch(e){}
    voice.oscillators.push(ache);
  }

  voice.shapeSourceAdded=true;
}

function addSlightDriftToVoice(voice){
  if(!ctx||!voice||voice.driftAdded)return;
  const shape=state.shape||'pure';
  const now=ctx.currentTime;
  const depth=shape==='pressed'?1.6:shape==='hollow'?1.1:0.7;
  const rate=shape==='pressed'?0.18:shape==='hollow'?0.13:0.09;

  voice.oscillators.forEach((osc,index)=>{
    if(!osc||!osc.frequency||index>2)return;
    const drift=ctx.createOscillator();
    const driftGain=ctx.createGain();
    drift.type='sine';
    drift.frequency.setValueAtTime(rate+(index*.017),now);
    driftGain.gain.setValueAtTime(depth/(index===1?2:1),now);
    drift.connect(driftGain);
    driftGain.connect(osc.frequency);
    drift.start(now);
    try{drift.stop(now+12)}catch(e){}
    voice.oscillators.push(drift);
  });

  voice.driftAdded=true;
}

const originalShapeStartNote=startNote;
startNote=async function shapedStartNote(note){
  await originalShapeStartNote(note);
  const voice=voices[note.index];
  addShapeSourceToVoice(voice);
  addSlightDriftToVoice(voice);
};

const originalShapeHandleControlChange=handleControlChange;
handleControlChange=function shapeAwareControlChange(key,value){
  if(key==='shape'&&state.shape!==value){
    releaseAllNotes('Shape changed. Press a note again to hear the new source shape.');
  }
  originalShapeHandleControlChange(key,value);
};

const hasShapeControl=playDefs.some(([key])=>key==='shape');
if(!hasShapeControl){
  playDefs.unshift([
    'shape',
    'Shape',
    'Voice source character',
    [['pure','Pure'],['hollow','Hollow'],['pressed','Pressed']]
  ]);
  renderAll();
}
