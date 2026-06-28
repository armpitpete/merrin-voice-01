const rawMidiMonitorStyle=document.createElement('style');
rawMidiMonitorStyle.textContent=`
.raw-midi-monitor{max-height:420px;overflow:auto;}
.raw-midi-monitor[hidden]{display:none!important;}
.raw-midi-monitor pre{white-space:pre-wrap;margin:.5rem 0 0;font:11px/1.35 ui-monospace,SFMono-Regular,Consolas,monospace;color:var(--muted);background:rgba(0,0,0,.24);border:1px solid var(--line);border-radius:10px;padding:8px;max-height:300px;overflow:auto;}
@media(min-width:900px) and (orientation:landscape){.app>.raw-midi-monitor{grid-column:1/-1!important;width:100%!important;max-width:100%!important;min-width:0!important;max-height:360px;overflow:auto;}}
`;
document.head.appendChild(rawMidiMonitorStyle);

let rawMidiAccess=null;
let rawMidiOutput=null;
let rawMidiPanel=null;
let rawMidiStartButton=null;
let rawMidiCount=0;
let rawMidiRealtimeCount=0;
let rawMidiLog=[];
let rawMidiUpdateScheduled=false;
let rawMidiMonitoring=false;
const rawMidiAttachedInputs=new Set();

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

function rawMidiIsRealtimeMessage(data){
  const status=data?.[0];
  return status>=0xf8;
}

function ensureRawMidiMonitor(){
  if(rawMidiOutput)return;
  const existing=document.querySelector('.midi-debug-panel')||document.querySelector('.oscilloscope-panel')||document.querySelector('.top-controls');
  if(!existing)return;
  const panel=document.createElement('section');
  panel.className='strip raw-midi-monitor';
  panel.hidden=window.midiDiagnosticsVisible!==true;
  panel.innerHTML='<strong>Raw MIDI monitor</strong><p class="status">This logs note/control MIDI events independently of the synth code. MIDI clock and active-sensing spam are counted but not logged.</p><div class="row" style="margin-top:6px"><button class="btn test" id="rawMidiStart" type="button">Start raw MIDI monitor</button><button class="btn test" id="rawMidiClear" type="button">Clear raw log</button><button class="btn test" id="rawMidiCopy" type="button">Copy raw log</button></div><pre id="rawMidiOutput">Raw MIDI monitor ready.</pre>';
  existing.insertAdjacentElement('afterend',panel);
  rawMidiPanel=panel;
  rawMidiOutput=document.getElementById('rawMidiOutput');
  rawMidiStartButton=document.getElementById('rawMidiStart');
  rawMidiStartButton?.addEventListener('click',()=>{
    if(rawMidiMonitoring)stopRawMidiMonitor('raw monitor stopped');
    else startRawMidiMonitor();
  });
  document.getElementById('rawMidiClear')?.addEventListener('click',()=>{rawMidiLog=[];rawMidiCount=0;rawMidiRealtimeCount=0;updateRawMidiOutput();});
  document.getElementById('rawMidiCopy')?.addEventListener('click',async()=>{
    try{
      await navigator.clipboard.writeText(rawMidiOutput?.textContent||'');
      rawMidiLogLine('COPIED',[],'raw log copied');
    }catch(error){
      rawMidiLogLine('COPY-FAILED',[],error?.message||'copy failed');
    }
  });
  updateRawMidiStartButton();
  updateRawMidiOutput();
}

function updateRawMidiStartButton(){
  if(!rawMidiStartButton)return;
  rawMidiStartButton.textContent=rawMidiMonitoring?'Stop raw MIDI monitor':'Start raw MIDI monitor';
  rawMidiStartButton.setAttribute('aria-pressed',String(rawMidiMonitoring));
}

function updateRawMidiOutput(){
  if(!rawMidiOutput||rawMidiPanel?.hidden)return;
  rawMidiOutput.textContent=[
    `Raw MIDI monitor: ${rawMidiMonitoring?'on':'off'}`,
    `Raw MIDI count: ${rawMidiCount}`,
    `Filtered real-time MIDI count: ${rawMidiRealtimeCount}`,
    rawMidiVoiceState(),
    '--- raw MIDI trace ---',
    ...rawMidiLog.slice(-80)
  ].join('\n');
}

function scheduleRawMidiOutput(){
  if(rawMidiPanel?.hidden||rawMidiUpdateScheduled)return;
  rawMidiUpdateScheduled=true;
  setTimeout(()=>{
    rawMidiUpdateScheduled=false;
    updateRawMidiOutput();
  },100);
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
  if(rawMidiPanel?.hidden)return;
  const time=new Date().toLocaleTimeString();
  const bytes=Array.from(data||[]);
  const byteText=bytes.join(' ');
  const line=`${time} ${type}${extra?` ${extra}`:''}${byteText?` | bytes=${byteText}`:''} | ${rawMidiVoiceState()}`;
  rawMidiLog.push(line);
  if(rawMidiLog.length>300)rawMidiLog.shift();
  scheduleRawMidiOutput();
}

function handleRawMidiEvent(event){
  if(!rawMidiMonitoring)return;

  if(rawMidiIsRealtimeMessage(event.data)){
    rawMidiRealtimeCount+=1;
    scheduleRawMidiOutput();
    return;
  }

  rawMidiCount+=1;
  const [status,data1,data2]=event.data;
  const command=status&0xf0;
  const type=rawMidiCommandName(command,data2);
  const noteInfo=(command===0x90||command===0x80)?`${rawMidiNoteName(data1)} note=${data1} velocity=${data2}`:`data1=${data1} data2=${data2}`;
  rawMidiLogLine(type,event.data,noteInfo);
}

function attachRawMidiInputs(){
  if(!rawMidiAccess||!rawMidiMonitoring)return;
  const inputs=[...rawMidiAccess.inputs.values()];
  if(!inputs.length){
    rawMidiLogLine('NO-INPUTS',[],'no raw MIDI inputs found');
    return;
  }
  inputs.forEach(input=>{
    if(rawMidiAttachedInputs.has(input))return;
    input.addEventListener('midimessage',handleRawMidiEvent);
    rawMidiAttachedInputs.add(input);
    rawMidiLogLine('RAW-INPUT-ATTACHED',[],input.name||'Unnamed MIDI input');
  });
}

function detachRawMidiInputs(){
  rawMidiAttachedInputs.forEach(input=>{
    try{input.removeEventListener('midimessage',handleRawMidiEvent);}catch(error){}
  });
  rawMidiAttachedInputs.clear();
}

function stopRawMidiMonitor(reason='raw monitor stopped'){
  detachRawMidiInputs();
  if(rawMidiAccess)rawMidiAccess.onstatechange=null;
  rawMidiMonitoring=false;
  updateRawMidiStartButton();
  if(!rawMidiPanel?.hidden)rawMidiLogLine('RAW-MONITOR-OFF',[],reason);
  updateRawMidiOutput();
}

async function startRawMidiMonitor(){
  ensureRawMidiMonitor();
  if(rawMidiPanel)rawMidiPanel.hidden=false;
  if(!navigator.requestMIDIAccess){
    rawMidiLogLine('UNSUPPORTED',[],'Web MIDI not supported');
    return;
  }
  try{
    rawMidiMonitoring=true;
    updateRawMidiStartButton();
    rawMidiLogLine('REQUEST',[],'raw monitor requesting MIDI access');
    rawMidiAccess=await navigator.requestMIDIAccess({sysex:false});
    attachRawMidiInputs();
    rawMidiAccess.onstatechange=()=>{
      if(!rawMidiMonitoring)return;
      rawMidiLogLine('STATE-CHANGE',[],'raw monitor saw MIDI state change');
      attachRawMidiInputs();
    };
  }catch(error){
    rawMidiMonitoring=false;
    updateRawMidiStartButton();
    rawMidiLogLine('ACCESS-ERROR',[],error?.message||'raw MIDI access error');
  }
}

function setRawMidiMonitorVisible(value){
  if(value){
    ensureRawMidiMonitor();
    if(rawMidiPanel)rawMidiPanel.hidden=false;
    updateRawMidiOutput();
    return;
  }

  stopRawMidiMonitor('diagnostics hidden; raw MIDI listeners detached');
  rawMidiLog=[];
  rawMidiUpdateScheduled=false;
  if(rawMidiPanel)rawMidiPanel.hidden=true;
}

window.setRawMidiMonitorVisible=setRawMidiMonitorVisible;
window.stopRawMidiMonitor=stopRawMidiMonitor;

if(window.midiDiagnosticsVisible===true)setRawMidiMonitorVisible(true);
setInterval(()=>{if(rawMidiOutput&&!rawMidiPanel?.hidden)updateRawMidiOutput();},500);
