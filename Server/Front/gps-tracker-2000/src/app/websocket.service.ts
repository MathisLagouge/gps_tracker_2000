import { Injectable } from '@angular/core';
import { webSocket } from 'rxjs/webSocket';
import { CoordinatesI } from './coordinates-i';
import { Subject } from 'rxjs';
@Injectable()
export class WebsocketService {
  public markers: Array<CoordinatesI> = [];
  private markersSubject = new Subject<Array<CoordinatesI>>();
  markers$ = this.markersSubject.asObservable();
  subject = webSocket('ws://localhost:81/ws');
  constructor() {
    console.log('WebsocketService created, connecting');
    this.subject.subscribe({
      next: (msg) => {
        // Called whenever there is a message from the server.
        // Parse the message
        const data = JSON.parse(msg as string);
        // Check if the message is a marker
        if (!data.hasOwnProperty('LAT') || !data.hasOwnProperty('LONG')) {
          // console.log('not a marker');
          return;
        }
        // Check if the marker already exists
        for (let i = 0; i < this.markers.length; i++) {
          if (this.markers[i].LAT == data.LAT && this.markers[i].LONG == data.LONG) {
            // console.log('marker already exists');
            return;
          }
        }
        this.markers.push(data as CoordinatesI);
        this.markersSubject.next(this.markers);
         
      },
      error: (err) => {
        // Called if at any point WebSocket API signals some kind of error.
        // console.log('ws err: ' + err);
      },
      complete: () => {
        // Called when connection is closed (for whatever reason).
        // console.log('ws complete');
      }, 
    });
  }

  sendMessage(msg: string) {
    this.subject.next(msg);
  }
}
