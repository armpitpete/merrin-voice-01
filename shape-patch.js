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
    shaped.sub=base.sub*.78;
    shaped.over=base.over+0.16;
    shaped.cut=base.cut*1.08;
  }

  if(shape==='pressed'){
    shaped.sine=base.sine*.58;
    shaped.sub=base.sub*.66;
    shaped.over=base.over+0.28;
    shaped.cut=base.cut*1.18;
    shaped.q=base.q*.88;
  }

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
  bodyGain.gain.setValueAtTime(shape==='hollow'?0.34:0.42,now);
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
    hollowGain.gain.setValueAtTime(0.08,now);
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
    acheGain.gain.setValueAtTime(0.18,now);
    ache.connect(acheGain);
    acheGain.connect(voice.amp);
    ache.start(now);
    try{ache.stop(now+12)}catch(e){}
    voice.oscillators.push(ache);
  }

  voice.shapeSourceAdded=true;
}

const originalShapeStartNote=startNote;
startNote=async function shapedStartNote(note){
  await originalShapeStartNote(note);
  addShapeSourceToVoice(voices[note.index]);
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
