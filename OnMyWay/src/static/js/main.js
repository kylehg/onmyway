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
    greenMarker: 'http://maps.google.com/mapfiles/ms/icons/green-dot.png',
    blueMarker: 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png',
    redMarker: 'http://maps.google.com/mapfiles/ms/icons/red-dot.png'
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

  omw.markerInit = function(title, lat, lng, color) {
    return (new google.maps.Marker({
      title: title,
      position: new google.maps.LatLng(lat, lng),
      icon: new google.maps.MarkerImage(color)
    }));
  };


  omw.resultsHandler = function(data) {
    console.log(data);

    var directionsRenderer = omw.directionsRenderer,
      orig = data.origin,
      dest = data.destination,
		  recs = data.recommendations,
      origMarker = omw.markerInit('Origin', orig.lat, orig.lng, omw.greenMarker),
      destMarker = omw.markerInit('Destination', dest.lat, dest.lng, omw.redMarker);
    var mapOptions = {
      mapTypeId: google.maps.MapTypeId.ROADMAP
    };
    var map = new google.maps.Map($('#map-canvas').get()[0], mapOptions);

    // Plot the markers
    recs.forEach(function(rec) {
      omw.markerInit(rec.name, rec.location.latitude, rec.location.longitude, omw.blueMarker).setMap(map);
    });

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