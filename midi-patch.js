const midiConnect=document.getElementById('midiConnect');
const midiStatus=document.getElementById('midiStatus');
let midiAccess=null;
const midiHeld={};

function setMidiStatus(message){
  if(midiStatus)midiStatus.textContent=message;
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

const originalMidiReleaseAllNotes=releaseAllNotes;
releaseAllNotes=function midiAwareReleaseAllNotes(message){
  Object.keys(midiHeld).forEach(noteNumber=>{
    stopNote(`midi-${noteNumber}`);
    setMidiVisualActive(Number(noteNumber),false);
    delete midiHeld[noteNumber];
  });
  Object.keys(heldKeys).forEach(key=>delete heldKeys[key]);
  Object.keys(voices).forEach(index=>stopNote(index));
  keyboard.querySelectorAll('.key').forEach(key=>key.dataset.active='false');
  if(message)playStatus.textContent=message;
};

const originalMidiStartNote=startNote;
startNote=async function midiVelocityStartNote(note){
  await originalMidiStartNote(note);
  const voice=voices[note.index];
  if(voice?.master&&note.velocityGain!==undefined&&ctx){
    const base=state.amplitude??.72;
    voice.master.gain.setValueAtTime(base*note.velocityGain,ctx.currentTime);
  }
};

function handleMidiMessage(event){
  const [status,noteNumber,velocity]=event.data;
  const command=status&0xf0;

  if(command===0x90&&velocity>0){
    const key=String(noteNumber);
    if(midiHeld[key])return;
    const note=midiNoteObject(noteNumber,velocity);
    midiHeld[key]=note.index;
    startNote(note);
    setMidiVisualActive(noteNumber,true);
    setMidiStatus(`MIDI connected: ${event.currentTarget?.name||'keyboard'}`);
    return;
  }

  if(command===0x80||(command===0x90&&velocity===0)){
    const key=String(noteNumber);
    if(midiHeld[key]){
      stopNote(midiHeld[key]);
      setMidiVisualActive(noteNumber,false);
      delete midiHeld[key];
    }
  }
}

function connectMidiInputs(){
  if(!midiAccess)return;
  const inputs=[...midiAccess.inputs.values()];

  if(!inputs.length){
    setMidiStatus('MIDI: no input device found. Plug in keyboard, then press again.');
    return;
  }

  inputs.forEach(input=>{
    input.onmidimessage=handleMidiMessage;
  });

  const names=inputs.map(input=>input.name||'Unnamed MIDI input').join(', ');
  setMidiStatus(`MIDI connected: ${names}`);
}

async function connectMidiKeyboard(){
  if(!midiConnect)return;

  if(!navigator.requestMIDIAccess){
    setMidiStatus('MIDI not supported in this browser. Use Chrome or Edge desktop.');
    return;
  }

  try{
    midiConnect.disabled=true;
    setMidiStatus('MIDI: requesting access...');
    midiAccess=await navigator.requestMIDIAccess({sysex:false});
    connectMidiInputs();
    midiAccess.onstatechange=()=>connectMidiInputs();
  }catch(error){
    setMidiStatus('MIDI access blocked or unavailable.');
  }finally{
    midiConnect.disabled=false;
  }
}

if(midiConnect){
  midiConnect.addEventListener('click',connectMidiKeyboard);
  setMidiStatus(navigator.requestMIDIAccess?'MIDI: not connected.':'MIDI not supported in this browser.');
}
