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
    shaped.sine=base.sine*.92;
    shaped.sub=base.sub*.95;
    shaped.over=base.over+0.055;
  }

  if(shape==='pressed'){
    shaped.sine=base.sine*.84;
    shaped.sub=base.sub*.9;
    shaped.over=base.over+0.11;
  }

  return shaped;
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
