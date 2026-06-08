state.shape='pure';
labels.pure='Pure';
labels.hollow='Hollow';
labels.pressed='Pressed';

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
