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
