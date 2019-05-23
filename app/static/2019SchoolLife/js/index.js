$(document).ready(function(){
  $('.bar').each(function(i, elem){
    drawBar(elem);
  });
  
  $('.measure').each(function(i, elem){
    drawMeasure(elem);
  });
  
  $('a.redraw').click(function(e){
    e.preventDefault();
    $('.bar').each(function(i, elem){
      randomiseBar(elem);
    });
    $('.measure').each(function(i, elem){
      randomiseMeasure(elem);
    });
  
  });
  
  function drawBar(bar) {
    var percentage = $(bar).data('percentage');
    if(percentage > 100){
      percentage = 100;
    }
    $(bar).animate({'width': percentage + '%'}, 'slow');
  }
  
  function randomiseBar(bar) {
    var width =  Math.floor(Math.random() * (100 - 20 + 1)) + 20;
    $(bar).animate({'width': width + '%'}, 'slow');
    $(bar).attr('data-percentage', width);
  }
  
  function drawMeasure(measure) {
    var percentage = $(measure).data('percentage');
    if(percentage > 100){
      percentage = 100;
    }
    $(measure).animate({'width': percentage + '%'}, 'slow');
  }
  
  function randomiseMeasure(measure) {
    var width =  Math.floor(Math.random() * (100 - 20 + 1)) + 20;
    $(measure).animate({'width': width + '%'}, 'slow');
    $(measure).attr('data-percentage', width);
  }
  
  
});