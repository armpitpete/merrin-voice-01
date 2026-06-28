const midiLayoutFix=document.createElement('style');
midiLayoutFix.textContent=`
@media(min-width:900px) and (orientation:landscape){
  .top-controls .row{
    display:grid!important;
    grid-template-columns:max-content max-content max-content max-content minmax(0,1fr)!important;
    width:100%!important;
    align-items:center!important;
  }
  .app>.top-controls,
  .app>.midi-debug-panel,
  .app>.raw-midi-monitor,
  .app>.landscape-columns,
  .app>.oscilloscope-panel{
    grid-column:1/-1!important;
    width:100%!important;
    max-width:100%!important;
    min-width:0!important;
  }
  #playStatus{
    min-width:0!important;
    white-space:nowrap!important;
    overflow:hidden!important;
    text-overflow:ellipsis!important;
  }
  #midiStatus{
    grid-column:1/-1!important;
    min-width:0!important;
    max-width:100%!important;
    white-space:nowrap!important;
    overflow:hidden!important;
    text-overflow:ellipsis!important;
  }
  .midi-debug-panel{max-height:170px;overflow:auto;}
}
.midi-debug-panel pre{white-space:pre-wrap;margin:.5rem 0 0;font:12px/1.35 ui-monospace,SFMono-Regular,Consolas,monospace;color:var(--muted);}
`;
document.head.appendChild(midiLayoutFix);

const midiConnect=document.getElementById('midiConnect');
const midiStatus=document.getElementById('midiStatus');
let midiAccess=null;
const midiHeld={};
const midiPendingOff={};
const midiLog=[];
let midiDebugOutput=null;
let midiDebugUpdateScheduled=false;
let lastMidiInputStatus='';

function isMidiRealtimeMessage(data){
  const status=data?.[0];
  return status>=0xf8;
}

function ensureMidiDebugPanel(){
  if(midiDebugOutput)return;
  const topControls=document.querySelector('.top-controls');
  const insertAfter=document.querySelector('.oscilloscope-panel')||topControls;
  if(!topControls||!insertAfter)return;
  const panel=document.createElement('section');
  panel.className='strip midi-debug-panel';
  panel.innerHTML='<strong>MIDI diagnostics</strong><div class="row" style="margin-top:6px"><button class="btn test" id="midiPanic" type="button">MIDI panic: all notes off</button><button class="btn test" id="midiClearLog" type="button">Clear MIDI log</button></div><pre id="midiDebugOutput">MIDI diagnostics ready.</pre>';
  insertAfter.insertAdjacentElement('afterend',panel);
  midiDebugOutput=document.getElementById('midiDebugOutput');
  document.getElementById('midiPanic')?.addEventListener('click',()=>{
    releaseAllNotes('MIDI panic. Released all notes.');
    midiLogEvent('PANIC',[], 'all notes off');
  });
  document.getElementById('midiClearLog')?.addEventListener('click',()=>{
    midiLog.length=0;
    updateMidiDebugOutput();
  });
  updateMidiDebugOutput();
}

function midiSnapshot(){
  return `held=[${Object.keys(midiHeld).join(',')||'none'}] pendingOff=[${Object.keys(midiPendingOff).join(',')||'none'}] voices=[${Object.keys(voices).join(',')||'none'}] active=[${activeVoiceIndexes().join(',')||'none'}]`;
}

function updateMidiDebugOutput(){
  if(!midiDebugOutput)return;
  const lines=[`Status: ${midiSnapshot()}`,...midiLog.slice(-18)];
  midiDebugOutput.textContent=lines.join('\n');
}

function scheduleMidiDebugOutput(){
  if(midiDebugUpdateScheduled)return;
  midiDebugUpdateScheduled=true;
  setTimeout(()=>{
    midiDebugUpdateScheduled=false;
    updateMidiDebugOutput();
  },100);
}

function midiLogEvent(type,data,note){
  const time=new Date().toLocaleTimeString();
  const bytes=Array.from(data||[]).join(' ');
  midiLog.push(`${time} ${type}${note?` ${note}`:''}${bytes?` | ${bytes}`:''} | ${midiSnapshot()}`);
  if(midiLog.length>80)midiLog.shift();
  scheduleMidiDebugOutput();
}

function setMidiStatus(message){
  if(midiStatus)midiStatus.textContent=message;
  scheduleMidiDebugOutput();
}

function setMidiInputStatus(message){
  if(message===lastMidiInputStatus)return;
  lastMidiInputStatus=message;
  setMidiStatus(message);
}

function midiNoteName(noteNumber){
  const names=['C','C#','D','Eb','E','F','F#','G','Ab','A','Bb','B'];
  const name=names[noteNumber%12]||String(noteNumber);
  const octave=Math.floor(noteNumber/12)-1;
  return `${name}${octave}`;
}

function midiFrequency(noteNumber){
  return 440*Math.pow(2,(noteNumber-69)/12);
}

function midiNoteObject(noteNumber,velocity){
  const safeVelocity=Math.max(1,Math.min(127,velocity||64));
  const velocityGain=.35+((safeVelocity/127)*.65);
  return {
    name:midiNoteName(noteNumber),
    freq:midiFrequency(noteNumber),
    index:`midi-${noteNumber}`,
    midiNote:noteNumber,
    velocityGain
  };
}

function activeVoiceIndexes(){
  return Object.keys(voices).filter(index=>voices[index]&&!voices[index].released);
}

function releaseOldestHeldNote(){
  const held=activeVoiceIndexes().sort((a,b)=>voices[a].startedAt-voices[b].startedAt);
  if(held.length>=maxHeldNotes)stopNote(held[0]);
}

function setMidiVisualActive(noteNumber,value){
  const pitchClass=noteNumber%12;
  const currentNotes=scaleNotes[state.scale]||[];
  const match=currentNotes.findIndex(([,freq])=>{
    const midi=Math.round(69+(12*Math.log2(freq/440)));
    return ((midi%12)+12)%12===pitchClass;
  });
  if(match>=0)setActiveNote(match,value);
}

function disconnectVoicePart(part){
  if(part&&typeof part.disconnect==='function'){
    try{part.disconnect();}catch(error){}
  }
}

function disposeReleasedVoiceForRetrigger(index){
  const voice=voices[index];
  if(!voice||!voice.released)return false;

  const now=ctx?.currentTime||0;

  try{
    if(voice.amp?.gain&&ctx){
      const gain=Math.max(.0001,currentAmpGain(voice,now));
      voice.amp.gain.cancelScheduledValues(now);
      voice.amp.gain.setValueAtTime(gain,now);
      voice.amp.gain.exponentialRampToValueAtTime(.0001,now+.06);
    }
  }catch(error){}

  (voice.oscillators||[]).forEach(oscillator=>{
    try{oscillator.stop(now+.08);}catch(error){}
  });

  setTimeout(()=>{
    (voice.oscillators||[]).forEach(disconnectVoicePart);
    ['amp','master','filter','subGain','overGain','delay','feedback','wet','dry','output','panner','driftGain','driftOsc'].forEach(name=>disconnectVoicePart(voice[name]));
  },180);

  delete voices[index];
  midiLogEvent('RETRIGGER-DISPOSE',[],String(index));
  return true;
}

function allowReleasedVoiceRetrigger(index){
  disposeReleasedVoiceForRetrigger(index);
}

stopNote=function midiSafeStopNote(index){
  const voice=voices[index];
  if(!voice||voice.released||!ctx){
    midiLogEvent('STOP-MISS',[],String(index));
    return;
  }

  voice.released=true;
  clearHeldKeyForIndex(index);

  const now=ctx.currentTime;
  const rel=releaseTime();
  const startGain=Math.max(.0001,currentAmpGain(voice,now));

  try{
    voice.amp.gain.cancelAndHoldAtTime(now);
  }catch(error){
    voice.amp.gain.cancelScheduledValues(now);
  }

  voice.amp.gain.setValueAtTime(startGain,now);
  voice.amp.gain.exponentialRampToValueAtTime(.0001,now+rel);

  voice.oscillators.forEach(oscillator=>{
    try{
      oscillator.stop(now+rel+2.1);
    }catch(error){}
  });

  setActiveNote(index,false);
  midiLogEvent('STOP',[],String(index));

  setTimeout(()=>{
    if(voices[index]===voice){
      delete voices[index];
      setActiveNote(index,false);
      midiLogEvent('CLEANUP',[],String(index));
    }
  },Math.max(120,rel*1000+120));

  playStatus.textContent=`Released ${voice.note.name}. Release: ${ms(rel)}.`;
};

releaseAllNotes=function midiAwareReleaseAllNotes(message){
  Object.keys(midiHeld).forEach(noteNumber=>{
    stopNote(`midi-${noteNumber}`);
    setMidiVisualActive(Number(noteNumber),false);
    delete midiHeld[noteNumber];
    delete midiPendingOff[noteNumber];
  });
  Object.keys(midiPendingOff).forEach(noteNumber=>delete midiPendingOff[noteNumber]);
  Object.keys(heldKeys).forEach(key=>delete heldKeys[key]);
  Object.keys(voices).forEach(index=>stopNote(index));
  keyboard.querySelectorAll('.key').forEach(key=>key.dataset.active='false');
  midiLogEvent('RELEASE-ALL',[],message||'');
  if(message)playStatus.textContent=message;
};

const originalMidiStartNote=startNote;
startNote=async function midiVelocityStartNote(note){
  allowReleasedVoiceRetrigger(note.index);
  await originalMidiStartNote(note);

  const voice=voices[note.index];

  if(voice?.master&&note.velocityGain!==undefined&&ctx){
    const base=state.amplitude??.72;
    voice.master.gain.setValueAtTime(base*note.velocityGain,ctx.currentTime);
  }

  midiLogEvent('START',[],String(note.index));

  if(note.midiNote!==undefined&&midiPendingOff[note.midiNote]){
    stopNote(note.index);
    setMidiVisualActive(note.midiNote,false);
    delete midiPendingOff[note.midiNote];
    midiLogEvent('PENDING-OFF-APPLIED',[],String(note.index));
  }
};

function handleMidiControlChange(controller,value,data){
  if(controller===64&&value<64){
    midiLogEvent('CC-SUSTAIN-OFF',data,''+value);
    return;
  }

  if(controller===120||controller===123){
    releaseAllNotes(`MIDI all-notes-off received. CC ${controller}.`);
    midiLogEvent('CC-ALL-NOTES-OFF',data,''+controller);
    return;
  }

  midiLogEvent('CC',data,`${controller}=${value}`);
}

function handleMidiMessage(event){
  const [status,noteNumber,velocity]=event.data;
  if(isMidiRealtimeMessage(event.data))return;

  const command=status&0xf0;
  const key=String(noteNumber);

  if(command===0xb0){
    handleMidiControlChange(noteNumber,velocity,event.data);
    return;
  }

  if(command===0x90&&velocity>0){
    if(midiHeld[key]){
      midiLogEvent('ON-DUPLICATE-IGNORED',event.data,midiNoteName(noteNumber));
      return;
    }
    const note=midiNoteObject(noteNumber,velocity);
    allowReleasedVoiceRetrigger(note.index);
    delete midiPendingOff[key];
    midiHeld[key]=note.index;
    startNote(note);
    setMidiVisualActive(noteNumber,true);
    setMidiInputStatus(`MIDI connected: ${event.currentTarget?.name||'keyboard'}`);
    midiLogEvent('ON',event.data,note.name);
    return;
  }

  if(command===0x80||(command===0x90&&velocity===0)){
    const heldIndex=midiHeld[key];

    if(heldIndex){
      if(voices[heldIndex]){
        stopNote(heldIndex);
      }else{
        midiPendingOff[key]=true;
        midiLogEvent('OFF-PENDING-NO-VOICE-YET',event.data,midiNoteName(noteNumber));
      }
      setMidiVisualActive(noteNumber,false);
      delete midiHeld[key];
      midiLogEvent('OFF',event.data,midiNoteName(noteNumber));
      return;
    }

    midiPendingOff[key]=true;
    setMidiVisualActive(noteNumber,false);
    midiLogEvent('OFF-NOT-HELD',event.data,midiNoteName(noteNumber));
    return;
  }

  midiLogEvent('MIDI-OTHER',event.data,'');
}

function connectMidiInputs(){
  if(!midiAccess)return;
  ensureMidiDebugPanel();
  const inputs=[...midiAccess.inputs.values()];

  if(!inputs.length){
    releaseAllNotes('MIDI input lost. Released held notes safely.');
    setMidiStatus('MIDI: no input device found. Plug in keyboard, then press again.');
    midiLogEvent('NO-INPUTS',[], '');
    return;
  }

  inputs.forEach(input=>{
    input.onmidimessage=handleMidiMessage;
  });

  const names=inputs.map(input=>input.name||'Unnamed MIDI input').join(', ');
  lastMidiInputStatus=`MIDI connected: ${names}`;
  setMidiStatus(lastMidiInputStatus);
  midiLogEvent('CONNECTED',[],names);
}

async function connectMidiKeyboard(){
  if(!midiConnect)return;
  ensureMidiDebugPanel();

  if(!navigator.requestMIDIAccess){
    setMidiStatus('MIDI not supported in this browser. Use Chrome or Edge desktop.');
    midiLogEvent('UNSUPPORTED',[], '');
    return;
  }

  try{
    releaseAllNotes('Connecting MIDI. Released held notes safely.');
    midiConnect.disabled=true;
    setMidiStatus('MIDI: requesting access...');
    midiLogEvent('REQUEST',[], '');
    midiAccess=await navigator.requestMIDIAccess({sysex:false});
    connectMidiInputs();
    midiAccess.onstatechange=()=>connectMidiInputs();
  }catch(error){
    setMidiStatus('MIDI access blocked or unavailable.');
    midiLogEvent('ACCESS-ERROR',[],error?.message||'unknown');
  }finally{
    midiConnect.disabled=false;
  }
}

if(midiConnect){
  midiConnect.addEventListener('click',connectMidiKeyboard);
  setMidiStatus(navigator.requestMIDIAccess?'MIDI: not connected.':'MIDI not supported in this browser.');
}
