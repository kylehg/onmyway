/**
 * OnMyWay Frontend JS
 */

'use strict';
$(function() {

  var omw = omw || {
    lat: null,
		lng: null
	};

  omw.init = function() {

		omw.getLoc(function(position) {		// If we can get the location
      var lat = omw.lat = position.coords.latitude,
        lng = omw.lng = position.coords.longitude;
      $('#loading-loc').hide();
  		$('#from').hide();
      $('#cur-loc').show().attr('title', lat + ',' + lng);
    });

    // Attach event handlers
    // ---------------------

    // On form submit
    $('#omw-form').submit(omw.formSubmitHandler);

		// Cancel geolocation finding if asked
    $('#cur-loc a').click(function(event) {
      $(this).parent().hide();
      $('#from').show();
    });

	};

	omw.formSubmitHandler =	function(event) {
      event.preventDefault(); // Don't actually submit
      var data = {
				'to': $('#to').val(),
        'onmyway': $('#onmyway').val()
			};
      var from = $('#from').val().trim();
      if (from) {
				data['from'] = from;
			} else if (omw.lat && omw.lng) {
				data['from_lat'] = omw.lat;
				data['from_lng'] = omw.lng;
			} else {
				alert("Need a from!");
			}
      $('#loading').show();
      console.log('Submitting form with the following data:');
      console.log(data);
      $.get('/findway', data, omw.resultsHandler, omw.requestErrorHandler);
  };

  omw.getLoc = function(cb, error) {
		navigator.geolocation.getCurrentPosition(function(position) {
      omw.position = position;
      cb(position);
    }, (error || function(msg) { console.log(msg); }));
	};

  omw.resultsHandler = function(data) {
		$('#loading').hide();
    console.log('Received following results');
		console.log(data);
	};

  // Kick things off
  omw.init();

});