const rawMidiMonitorStyle=document.createElement('style');
rawMidiMonitorStyle.textContent=`
.raw-midi-monitor{max-height:420px;overflow:auto;}
.raw-midi-monitor pre{white-space:pre-wrap;margin:.5rem 0 0;font:11px/1.35 ui-monospace,SFMono-Regular,Consolas,monospace;color:var(--muted);background:rgba(0,0,0,.24);border:1px solid var(--line);border-radius:10px;padding:8px;max-height:300px;overflow:auto;}
@media(min-width:900px) and (orientation:landscape){.app>.raw-midi-monitor{grid-column:1/-1!important;width:100%!important;max-width:100%!important;min-width:0!important;max-height:360px;overflow:auto;}}
`;
document.head.appendChild(rawMidiMonitorStyle);

let rawMidiAccess=null;
let rawMidiOutput=null;
let rawMidiCount=0;
let rawMidiLog=[];

function rawMidiVoiceState(){
  try{
    const voiceList=Object.keys(voices).map(index=>{
      const voice=voices[index];
      if(!voice)return `${index}:missing`;
      return `${index}:${voice.note?.name||'unknown'}:${voice.released?'released':'held'}`;
    }).join(' | ')||'none';
    return `voices=${voiceList}`;
  }catch(error){
    return 'voices=unavailable';
  }
}

function ensureRawMidiMonitor(){
  if(rawMidiOutput)return;
  const existing=document.querySelector('.midi-debug-panel')||document.querySelector('.oscilloscope-panel')||document.querySelector('.top-controls');
  if(!existing)return;
  const panel=document.createElement('section');
  panel.className='strip raw-midi-monitor';
  panel.innerHTML='<strong>Raw MIDI monitor</strong><p class="status">This logs every raw MIDI event independently of the synth code.</p><div class="row" style="margin-top:6px"><button class="btn test" id="rawMidiStart" type="button">Start raw MIDI monitor</button><button class="btn test" id="rawMidiClear" type="button">Clear raw log</button><button class="btn test" id="rawMidiCopy" type="button">Copy raw log</button></div><pre id="rawMidiOutput">Raw MIDI monitor ready.</pre>';
  existing.insertAdjacentElement('afterend',panel);
  rawMidiOutput=document.getElementById('rawMidiOutput');
  document.getElementById('rawMidiStart')?.addEventListener('click',startRawMidiMonitor);
  document.getElementById('rawMidiClear')?.addEventListener('click',()=>{rawMidiLog=[];rawMidiCount=0;updateRawMidiOutput();});
  document.getElementById('rawMidiCopy')?.addEventListener('click',async()=>{
    try{
      await navigator.clipboard.writeText(rawMidiOutput?.textContent||'');
      rawMidiLogLine('COPIED',[],'raw log copied');
    }catch(error){
      rawMidiLogLine('COPY-FAILED',[],error?.message||'copy failed');
    }
  });
  updateRawMidiOutput();
}

function updateRawMidiOutput(){
  if(!rawMidiOutput)return;
  rawMidiOutput.textContent=[
    `Raw MIDI count: ${rawMidiCount}`,
    rawMidiVoiceState(),
    '--- raw MIDI trace ---',
    ...rawMidiLog.slice(-80)
  ].join('\n');
}

function rawMidiCommandName(command,velocity){
  if(command===0x90&&velocity>0)return 'NOTE-ON';
  if(command===0x80||(command===0x90&&velocity===0))return 'NOTE-OFF';
  if(command===0xb0)return 'CONTROL-CHANGE';
  return `COMMAND-${command}`;
}

function rawMidiNoteName(noteNumber){
  const names=['C','C#','D','Eb','E','F','F#','G','Ab','A','Bb','B'];
  return `${names[noteNumber%12]||noteNumber}${Math.floor(noteNumber/12)-1}`;
}

function rawMidiLogLine(type,data,extra){
  const time=new Date().toLocaleTimeString();
  const bytes=Array.from(data||[]);
  const byteText=bytes.join(' ');
  const line=`${time} ${type}${extra?` ${extra}`:''}${byteText?` | bytes=${byteText}`:''} | ${rawMidiVoiceState()}`;
  rawMidiLog.push(line);
  if(rawMidiLog.length>300)rawMidiLog.shift();
  updateRawMidiOutput();
}

function handleRawMidiEvent(event){
  rawMidiCount+=1;
  const [status,data1,data2]=event.data;
  const command=status&0xf0;
  const type=rawMidiCommandName(command,data2);
  const noteInfo=(command===0x90||command===0x80)?`${rawMidiNoteName(data1)} note=${data1} velocity=${data2}`:`data1=${data1} data2=${data2}`;
  rawMidiLogLine(type,event.data,noteInfo);
}

function attachRawMidiInputs(){
  if(!rawMidiAccess)return;
  const inputs=[...rawMidiAccess.inputs.values()];
  if(!inputs.length){
    rawMidiLogLine('NO-INPUTS',[],'no raw MIDI inputs found');
    return;
  }
  inputs.forEach(input=>{
    input.addEventListener('midimessage',handleRawMidiEvent);
    rawMidiLogLine('RAW-INPUT-ATTACHED',[],input.name||'Unnamed MIDI input');
  });
}

async function startRawMidiMonitor(){
  ensureRawMidiMonitor();
  if(!navigator.requestMIDIAccess){
    rawMidiLogLine('UNSUPPORTED',[],'Web MIDI not supported');
    return;
  }
  try{
    rawMidiLogLine('REQUEST',[],'raw monitor requesting MIDI access');
    rawMidiAccess=await navigator.requestMIDIAccess({sysex:false});
    attachRawMidiInputs();
    rawMidiAccess.onstatechange=()=>{
      rawMidiLogLine('STATE-CHANGE',[],'raw monitor saw MIDI state change');
      attachRawMidiInputs();
    };
  }catch(error){
    rawMidiLogLine('ACCESS-ERROR',[],error?.message||'raw MIDI access error');
  }
}

ensureRawMidiMonitor();
setInterval(updateRawMidiOutput,500);
