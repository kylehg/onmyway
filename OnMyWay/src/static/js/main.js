/**
 * OnMyWay Frontend JS
 */

'use strict';
$(function() {

  var omw = omw || {
    position: null
	};

  omw.init = function() {

		omw.getLoc(function(position) {		// If we can get the location
      var lat = position.coords.latitude,
        lng = position.coords.longitude;
  		$('#from').addClass('cur-log').val('My Location');
    });

	};

  omw.getLoc = function(cb, error) {
		navigator.geolocation.getCurrentPosition(function(position) {
      omw.position = position;
      cb(position);
    }, (error || function(msg) { console.log(msg); }));
	};

  // Kick things off
  omw.init();

});