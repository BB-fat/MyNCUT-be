
function drawBar(bar) {
  var percentage = $(bar).data('percentage');
  if (percentage > 100) {
    percentage = 100;
  }
  $(bar).animate({ 'width': percentage + '%' }, 'slow');
}

function randomiseBar(bar) {
  var width = Math.floor(Math.random() * (100 - 20 + 1)) + 20;
  $(bar).animate({ 'width': width + '%' }, 'slow');
  $(bar).attr('data-percentage', width);
}

function drawMeasure(measure) {
  var percentage = $(measure).data('percentage');
  if (percentage > 100) {
    percentage = 100;
  }
  $(measure).animate({ 'width': percentage + '%' }, 'slow');
}

function randomiseMeasure(measure) {
  var width = Math.floor(Math.random() * (100 - 20 + 1)) + 20;
  $(measure).animate({ 'width': width + '%' }, 'slow');
  $(measure).attr('data-percentage', width);
}