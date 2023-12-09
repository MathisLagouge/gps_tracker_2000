import { Component, OnInit } from '@angular/core';
import { LeafletModule } from '@asymmetrik/ngx-leaflet';
import * as Leaflet from 'leaflet';
import { WebsocketService } from '../websocket.service';

@Component({
  selector: 'app-map',
  standalone: true,
  imports: [LeafletModule],
  templateUrl: './map.component.html',
  styleUrl: './map.component.css',
})
export class MapComponent implements OnInit{
  map!: Leaflet.Map;
  markers: Leaflet.Marker[] = [];
  options = {
    layers: [
      Leaflet.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution:
          '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
      }),
    ],
    zoom: 16,
    // Center on paris by default
    center: { lat: 48.866667, lng: 2.333333 },
  };

  public constructor(public ws: WebsocketService) {
    this.ws.markers$.subscribe((markers) => {
      // console.log('MapComponent received markers');
      // console.log(markers);
      this.updateMarkers();
    });
  }
  ngOnInit(): void {
    const iconRetinaUrl = 'assets/marker-icon-2x.png';
    const iconUrl = 'assets/marker-icon.png';
    const shadowUrl = 'assets/marker-shadow.png';
    const iconDefault = Leaflet.icon({
      iconRetinaUrl,
      iconUrl,
      shadowUrl,
      iconSize: [25, 41],
      iconAnchor: [12, 41],
      popupAnchor: [1, -34],
      tooltipAnchor: [16, -28],
      shadowSize: [41, 41]
    });
    Leaflet.Marker.prototype.options.icon = iconDefault;
    setInterval(() => {
      this.ws.sendMessage('u');
    }, 2000);
  }

  generateMarker(data: any, index: number) {
    return Leaflet.marker(data.position, { draggable: data.draggable })
      .on('click', (event) => this.markerClicked(event, index))
      .on('dragend', (event) => this.markerDragEnd(event, index));
  }

  onMapReady($event: Leaflet.Map) {
    this.map = $event;

  
  }

  mapClicked($event: any) {
    console.log($event.latlng.lat, $event.latlng.lng);


  }

  markerClicked($event: any, index: number) {
    console.log($event.latlng.lat, $event.latlng.lng);
  }

  markerDragEnd($event: any, index: number) {
    console.log($event.target.getLatLng());
  }

  updateMarkers() {
    // console.log('updating markers');
    // console.log(this.ws.markers);

  

    this.ws.markers.forEach((marker, index) => {
      // Check if marker is already on the map
      for (let i = 0; i < this.markers.length; i++) {
        if (this.markers[i].getLatLng().lat == marker.LAT && this.markers[i].getLatLng().lng == marker.LONG) {
          // console.log('marker already exists');
          return;
        }
      }
      if (!marker) {
        // console.log('marker is null');
        return;
      }
      const data = {
        position: { lat: marker.LAT, lng: marker.LONG },
        draggable: false,
      };
      let i = this.markers.length > 0 ? this.markers.length - 1 : 0;
      let mk = this.generateMarker(data, i);
      mk.addTo(this.map).bindPopup(
        `<b>${marker.IP} - ${marker.timestamp} </b> :  ${data.position.lat},  ${data.position.lng}`
      );
      this.markers.push(mk);
    });
  }
}
