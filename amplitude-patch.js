const scopeHeightFix=document.createElement('style');
scopeHeightFix.textContent=`
@media(min-width:900px) and (orientation:landscape){
  html,body{overflow-y:auto!important;}
  .app{gap:5px;height:auto!important;min-height:100dvh;padding-bottom:14px!important;align-items:start!important;}
  .app>section:nth-of-type(1) .row{display:grid;grid-template-columns:max-content max-content max-content minmax(0,1fr);width:100%;}
  #playStatus{display:block;min-width:0;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
  .scope{height:118px;}
  .app>section:nth-of-type(6){min-height:150px;margin-bottom:12px;}
  .app>section:nth-of-type(2),
  .app>section:nth-of-type(3),
  .app>section:nth-of-type(4),
  .app>section:nth-of-type(5){align-self:start!important;}
  .app>section:nth-of-type(4) .control{padding:5px;}
  .app>section:nth-of-type(4) .btn{padding:3px 6px;font-size:.78rem;}
  .app>section:nth-of-type(5){align-self:start;}
}
`;
document.head.appendChild(scopeHeightFix);

const amplitudeControl=document.getElementById('amplitude');
const amplitudeLabel=document.getElementById('amplitudeLabel');

function applyAmplitude(value){
  const amp=Math.max(0,Math.min(1,value));
  state.amplitude=amp;
  if(amplitudeLabel)amplitudeLabel.textContent=`Amplitude: ${Math.round(amp*100)}%`;
  const now=ctx?.currentTime||0;
  Object.values(voices).forEach(voice=>{
    if(voice?.master&&!voice.released){
      voice.master.gain.setTargetAtTime(amp,now,.025);
    }
  });
}

if(amplitudeControl){
  state.amplitude=Number(amplitudeControl.value)/100;
  applyAmplitude(state.amplitude);
  amplitudeControl.addEventListener('input',event=>applyAmplitude(Number(event.target.value)/100));
}

const originalStartNote=startNote;
startNote=async function patchedStartNote(note){
  await originalStartNote(note);
  applyAmplitude(state.amplitude??.72);
};
