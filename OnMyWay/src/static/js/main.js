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
    stepDisplay: new google.maps.InfoWindow(),
    curDirStep: 0
  };

  omw.init = function() {

    omw.getLoc(function(position) {   // If we can get the location
      var lat = omw.lat = position.coords.latitude,
        lng = omw.lng = position.coords.longitude;
      $('#loading-loc').hide();
      $('#from').hide();
      $('#cur-loc').show().attr('title', lat + ',' + lng);

      // DELETE ME:
      // var e = document.createEvent('Events');
      // e.initEvent('click', true, false);
      // $('#submit').get()[0].dispatchEvent(e);      
    });

    // Attach event handlers
    // ---------------------

    // On form submit
    $('#submit').click(omw.formSubmitHandler);

    // Cancel geolocation finding if asked
    $('#cur-loc a').click(function(event) {
      $(this).parent().hide();
      $('#from').show();
    });

    // Go back to the home page
    $('#back-btn').click(function(event) {
      $('#results').hide();
      $('#home').show();
    });


    // Testing: DELETE ME
    // $('#to').val('535 west 112th street, new york');
    // $('#onmyway').val('ice cream');
    
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
      display = omw.stepDisplay,
      recs = data.recommendations,
      origMarker = omw.markerInit(orig.lat, orig.lng),
      destMarker = omw.markerInit(dest.lat, dest.lng);
    var mapOptions = {
      mapTypeId: google.maps.MapTypeId.ROADMAP
    };
    var map = new google.maps.Map($('#map-canvas').get()[0], mapOptions);

    var attachText = function(display, marker, text) {
      google.maps.event.addListener(marker, 'click', function() {
        display.setContent(text);
        display.open(map, marker);
        $(".button-call").click(function() {
          console.log("worked!");
          for (var mark in omw.markerArray) {
            omw.markerArray[mark].setMap(null);
          }
          omw.markerArray = [];
//          var marker = omw.markerInit($(this).attr("data-lat"), $(this).attr("data-lng"));
//          omw.markerArray.push(marker);
//          marker.setMap(map);
          directionsRenderer.setMap(map);
          var request = {  
            origin: new google.maps.LatLng(orig.lat, orig.lng),
      			waypoints: [{
      				location: new google.maps.LatLng($(this).attr("data-lat"),
                  $(this).attr("data-lng")),
      				stopover: true
      			}],
            destination: new google.maps.LatLng(dest.lat, dest.lng),
            travelMode: google.maps.TravelMode.DRIVING
          };

          omw.directionsService.route(request, function(result, status) {
            if (status == google.maps.DirectionsStatus.OK) {
              directionsRenderer.setDirections(result);
      			  showSteps(result);
            } else {
              console.log("Soemthing went wrong " + status);
            }
          });
        });
      });
    }; //attachText

	  function showSteps(directionResult) {
		  var instructions = omw.instructions = [];
      directionResult.routes[0].legs[0].steps.forEach(function(step) {
        var marker = new google.maps.Marker({
          position: step.start_point,
          map: map
        });
        instructions.push([marker, step.instructions]);
      });

      directionResult.routes[0].legs[1].steps.forEach(function(step) {
        var marker = new google.maps.Marker({
          position: step.start_point
        });
        instructions.push([marker, step.instructions]);
      });

      console.log("show directions");
      $('#dir-view').show();
      $('#dir-content').html(omw.instructions[0][1]);
      $('#rarr').click(function(event) {
        incrInstructions(1);
      });
      $('#larr').click(function(event) {
        incrInstructions(-1);
      });

      function incrInstructions(step) {
        console.log("incr instructions by" + step);
        var newCur = omw.curDirStep + step;
        if (newCur < 0 || newCur >= omw.instructions.length) {
          return;
        }
        $('#dir-content').html(omw.instructions[newCur][1]); // set content
        if (step === 1)
          omw.instructions[newCur][0].setMap(map);
        else
          omw.instructions[newCur+1][0].setMap(null);
        // map.setCenter(omw.instructions[newCur][0].getPosition());
        omw.curDirStep = newCur;
      }
    } //showSteps

	  
    // Plot the markers
    omw.markerArray = [];
    recs.forEach(function(rec) {
      var marker = omw.markerInit(rec.location.latitude, rec.location.longitude);
      omw.markerArray.push(marker);
      marker.setMap(map);
      var text = 
        "<div style='font-weight:bold; font-size:13px; float:left;'>" + 
          rec.name  + "</div>" +
        "<div style='color:#444; font-size:11px; clear:left; float:left;'>" + 
          rec.formatted_address + "</div>" + 
        "<div style='float: right;padding-right:2px;font-size: 12px;'>" + 
          rec.rating + " / 5.0</div>" + 
        "<div style='clear:both;text-align:right;padding-top:3px;'><button data-lat='" + 
          rec.location.latitude + "' data-lng='" + rec.location.longitude + 
          "' class='button-call'>Select This</button></div>";
      attachText(display, marker, text);
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
      } else {
        console.log("Soemthing went wrong " + status);
      }
    });

    // UI magic
    $('#loading').hide();
    $('#home').hide();
    $('#results').show();
    $('#map-canvas').height($(window).height() - 80);
  };


  // Kick things off
  omw.init();

});