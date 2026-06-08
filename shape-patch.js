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
    shaped.sine=base.sine*.78;
    shaped.sub=base.sub*.82;
    shaped.over=base.over+0.16;
    shaped.cut=base.cut*1.08;
  }

  if(shape==='pressed'){
    shaped.sine=base.sine*.66;
    shaped.sub=base.sub*.72;
    shaped.over=base.over+0.28;
    shaped.cut=base.cut*1.16;
    shaped.q=base.q*.9;
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
