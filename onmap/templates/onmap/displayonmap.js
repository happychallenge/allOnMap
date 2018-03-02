<script>
var markers = [];
var pos, map;



function initMap() {

  map = new google.maps.Map(document.getElementById('map'), {
      zoom: 14,
      center: pos
  });

  bounds = new google.maps.LatLngBounds();

  var pictures = [
    {% for picture in position.pictures.all %}
        {id: {{picture.id}}, location: {lat: {{picture.lat}}, lng: {{picture.lng}} }, icon: '{{picture.file.url}}' },
    {% endfor %}
  ];

  for (var i = 0; i < pictures.length; i++) {
      position = new google.maps.LatLng( parseFloat(pictures[i].location.lat), 
            parseFloat(pictures[i].location.lng) );
      var id = pictures[i].id;
      var icon = pictures[i].icon;

      // new CustomMarker(position, map, pictures[i].icon);
      var marker = new google.maps.Marker({
          map: map,
          position: position,
          icon: icon,
          id: id
      });

      bounds.extend(position);
      // console.log("Position Lat : " + position.lat() + " " + position.lng());
      // console.log("Bounds   Lat : " + bounds.f.b + " " + bounds.b.f );
  }
  
    // console.log("FitBounds function", theme);
  if (pictures.length >= 2) {
      map.fitBounds(bounds);
  } else {
      map.panTo(pos);
  }
}

//adapted from http://gmaps-samples-v3.googlecode.com/svn/trunk/overlayview/custommarker.html
function CustomMarker(latlng, map, imageSrc){
    // Once the LatLng and text are set, add the overlay to the map.  This will
    // trigger a call to panes_changed which should in turn call draw.
    this.latlng_ = latlng;
    this.imageSrc = imageSrc;
    this.setMap(map);
}

CustomMarker.prototype = new google.maps.OverlayView();

CustomMarker.prototype.draw = function () {
    // Check if the div has been created.
    var div = this.div_;
    if (!div) {
        // Create a overlay text DIV
        div = this.div_ = document.createElement('div');
        // Create the DIV representing our CustomMarker
        div.className = "customMarker"


        var img = document.createElement("img");
        img.src = this.imageSrc;
        div.appendChild(img);


        // Then add the overlay to the DOM
        var panes = this.getPanes();
        panes.overlayImage.appendChild(div);
    }

    // Position the overlay 
    var point = this.getProjection().fromLatLngToDivPixel(this.latlng_);
    if (point) {
        div.style.left = point.x + 'px';
        div.style.top = point.y + 'px';
    }
};

CustomMarker.prototype.remove = function () {
    // Check if the overlay was on the map and needs to be removed.
    if (this.div_) {
        this.div_.parentNode.removeChild(this.div_);
        this.div_ = null;
    }
};

CustomMarker.prototype.getPosition = function () {
    return this.latlng_;
};
</script>