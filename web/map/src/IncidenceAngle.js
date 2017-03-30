$('#slider-range').slider({
    range: true,
    min: 0,
    max: 90,
    values: [ 0, 90 ],
    create: function() {
      $('#min').appendTo($('#slider-range a').get(0));
      $('#max').appendTo($('#slider-range a').get(1));
    },
    slide: function( event, ui ) {
      $( "#amount" ).val( "$" + ui.values[ 0 ] + " - $" + ui.values[ 1 ] );
      $(ui.handle).find('span').html(ui.value);
    },
    stop: function( event, ui ) {
     $(ui.handle).find('span').html(ui.value);
     $.ajax({
       //I can't make an ajax call because the database doesn't work
     });
    }
  });
});
    
$('#min').html($('#slider-range').slider('values', 0)).position({
  my: 'center top',
  at: 'center bottom',
  of: $('#slider-range a:eq(0)'),
  offset: "0, 10"
});

$('#max').html($('#slider-range').slider('values', 1)).position({
    my: 'center top',
    at: 'center bottom',
    of: $('#slider-range a:eq(1)'),
    offset: "0, 10"
});
