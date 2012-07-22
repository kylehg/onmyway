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
    directionsService: new google.maps.DirectionsService(),
    directionsRenderer: new google.maps.DirectionsRenderer(),
	stepDisplay: new google.maps.InfoWindow()
  };

  omw.init = function() {

    omw.getLoc(function(position) {   // If we can get the location
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


    // Testing: DELETE ME
    $('#to').val('535 west 112th street, new york');
    $('#onmyway').val('ice cream');

  };


  omw.formSubmitHandler = function(event) {
      event.preventDefault(); // Don't actually submit
      var data = {
        'destination_text': $('#to').val(),
        'query': $('#onmyway').val(),
        'method': 'onmyway'
      };
      
      var from = $('#from').val().trim();
      if (!from && !(omw.lat || omw.lng)) {
        alert("Need a origin!");
        return;
      }

      if (from) {
        data['origin_text'] = from;
      }

      if (omw.lat && omw.lng) {
        data['origin_lat'] = omw.lat;
        data['origin_lng'] = omw.lng;
      }

      $('#loading').show();
      console.log('Submitting form with the following data:');
      console.log(data);
      $.get('/find', data, omw.resultsHandler, omw.requestErrorHandler, 'json');
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
    console.log(data);

    var directionsRenderer = omw.directionsRenderer,
      orig = data.origin,
      dest = data.destination,
	  display = data.stepDisplay,
	  recs = data.recommendations,
      origMarker = omw.markerInit(orig.lat, orig.lng),
      destMarker = omw.markerInit(dest.lat, dest.lng);
    var mapOptions = {
      mapTypeId: google.maps.MapTypeId.ROADMAP
    };
    var map = new google.maps.Map($('#map-canvas').get()[0], mapOptions);

    // Plot the markers
    recs.forEach(function(rec) {
      var marker = omw.markerInit(rec.location.latitude, rec.location.longitude).setMap(map);
	  attachText(marker, rec.name + "\n" +rec.formatted_address);
    });

	 function attachText(marker, text) {
		 google.maps.event.addListener(marker, 'click', function() {
		   display.setContent(text);
		   display.open(map, marker);
		});
	 }

    // Plot the directions
    directionsRenderer.setMap(map);
    var request = {
      origin: new google.maps.LatLng(orig.lat, orig.lng),
      destination: new google.maps.LatLng(dest.lat, dest.lng),
      travelMode: google.maps.TravelMode.DRIVING
    };
    omw.directionsService.route(request, function(result, status) {
      if (status == google.maps.DirectionsStatus.OK) {
        directionsRenderer.setDirections(result);
      }
    });

    // UI magic
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