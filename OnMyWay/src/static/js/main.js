/**
 * OnMyWay Frontend JS
 */

'use strict';
$(function() {

  var omw = window.omw = omw || {
    lat: null,
		lng: null,
		orig: null,
		dest: null,
		dirService: new google.maps.DirectionsService(),
		dirRenderer: new google.maps.DirectionsRenderer()
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
				'destination_text': $('#to').val(),
        'query': $('#onmyway').val()
			};
      
      var from = $('#from').val().trim();
      if (!from && !(omw.lat || omw.lng)) {
        alert("Need a origin!");
        return false;
      }

      if (from) {
				data['origin_text'] = from;
			}

      if (omw.lat && omw.lng) {
				data['origin_lat'] = omw.lat;
				data['origin_lng'] = omw.lng;
			}

      data['method'] = 'onmyway';

      $('#loading').show();
      console.log('Submitting form with the following data:');
      console.log(data);
      $.get('/find', data, omw.resultsHandler, omw.requestErrorHandler);
  };

  omw.getLoc = function(cb, error) {
		navigator.geolocation.getCurrentPosition(function(position) {
      omw.lat = position.coords.latitude;
      omw.lng = position.coords.longitude;
      cb(position);
    }, (error || function(msg) { console.log(msg); }));
	};

  omw.markerInit = function(lat, lng) {
    return (new google.maps.Marker({
      position: new google.maps.LatLng(lat, lng)
    }));
  };


  omw.resultsHandler = function(data) {

    console.log('Received following results');
    console.log(data);

		var orig = data.results.origin,
		  dest = data.results.destination,
      origMarker = omw.markerInit(orig.lat, orig.lng),
      destMarker = omw.markerInit(dest.lat, dest.lng);

    var mapOpts = {
      mapTypeId: google.maps.MapTypeId.ROADMAP
    };

		// Draw the preliminary map
    var map = new google.maps.Map($('#map-canvas').get(), mapOpts);
    omw.dirRenderer.setMap(map);

    var dirRequest = {
      origin: new google.maps.LatLng(orig.lat, orig.lng),
      destination: new google.maps.LatLng(dest.lat, dest.lng),
      travelMode: google.maps.TravelMode.DRIVING
    };

    omw.dirService.route(dirRequest, function(result, status) {
      console.log("this seems to be the problem");
      if (status == google.maps.DirectionsStatus.OK) {
				dirRenderer.setDirections(result);
			} else {
				 console.log("Directions request with status:");
				 console.log(status);
			}
    });

		$('#loading').hide();
    $('#home').hide();
    $('#results').show();
	};


  // Kick things off
  omw.init();
  // omw.resultsHandler({
  //   results: {
  //     origin: {
  //       lat: 40.80510,
  //       lng: -73.96487
  //     },
  //     destination: {
  //       lat: 40.75377,
  //       lng: -73.97855  
  //     },
  //     recommendations: [
  //       {
  //         lat: 40.77176,
  //         lng: -73.97529 
  //       },
  //       {
  //         lat: 40.76903,
  //         lng: -73.97031
  //       },
  //       {
  //         lat: 40.79935,
  //         lng: -73.97146
  //       },
  //       {
  //         lat: 40.78010,
  //         lng: -73.96956
  //       },
  //       {
  //         lat: 40.79176,
  //         lng: -73.97825
  //       }
  //     ]
  //   }
  // });

});