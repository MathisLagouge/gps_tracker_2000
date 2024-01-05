import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { LeafletModule } from '@asymmetrik/ngx-leaflet';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { MapComponent } from './map/map.component';
import { WebsocketService } from './websocket.service';
import { CommonModule } from '@angular/common';

@NgModule({
  declarations: [
    AppComponent,
   
  ],
  imports: [
    BrowserModule,
    CommonModule,
    AppRoutingModule,
    LeafletModule,
    MapComponent
  ],
  providers: [WebsocketService],
  bootstrap: [AppComponent]
})
export class AppModule { }
