import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import {
	Http,
	HttpModule
} from '@angular/http';


import { AppComponent } from './app.component';
import { Ng2CarouselamosModule } from 'ng2-carouselamos';
import {NgbModule} from '@ng-bootstrap/ng-bootstrap';
import { RecommenderService } from './services/recommender.service';
import { HttpClientModule } from '@angular/common/http';
import {NavComponent} from './nav/nav.component';



@NgModule({
  declarations: [
    AppComponent,
    NavComponent,
  ],
  imports: [
    BrowserModule,
    HttpModule,
    Ng2CarouselamosModule,
    HttpClientModule,
    NgbModule.forRoot(),
  ],
  providers: [RecommenderService],
  bootstrap: [AppComponent]
})
export class AppModule { }
