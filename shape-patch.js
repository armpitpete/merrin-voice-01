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
    shaped.sine=base.sine*.84;
    shaped.sub=base.sub*.84;
    shaped.over=base.over+0.1;
    shaped.cut=base.cut*1.04;
  }

  if(shape==='pressed'){
    shaped.sine=base.sine*.74;
    shaped.sub=base.sub*.74;
    shaped.over=base.over+0.18;
    shaped.cut=base.cut*1.1;
    shaped.q=base.q*.92;
  }

  return shaped;
};

function addShapeSourceToVoice(voice){
  if(!ctx||!voice||!voice.amp||voice.shapeSourceAdded)return;
  const shape=state.shape||'pure';
  if(shape==='pure')return;

  const now=ctx.currentTime;
  const osc=ctx.createOscillator();
  const gain=ctx.createGain();
  const upper=null;

  osc.type='triangle';
  osc.frequency.setValueAtTime(voice.note.freq,now);
  gain.gain.setValueAtTime(shape==='hollow'?0.16:0.24,now);
  osc.connect(gain);
  gain.connect(voice.amp);
  osc.start(now);
  try{osc.stop(now+12)}catch(e){}
  voice.oscillators.push(osc);

  if(shape==='pressed'){
    const ache=ctx.createOscillator();
    const acheGain=ctx.createGain();
    ache.type='triangle';
    ache.frequency.setValueAtTime(voice.note.freq*2,now);
    acheGain.gain.setValueAtTime(0.07,now);
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
