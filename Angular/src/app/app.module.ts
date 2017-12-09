import { NgModule }      from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule }   from '@angular/forms';
import { AppComponent }   from './app.component';
import {BrowserAnimationsModule} from "@angular/platform-browser/animations";
import { HttpModule } from '@angular/http';
import {MatProgressBarModule} from '@angular/material/progress-bar';

@NgModule({
    imports:      [ BrowserModule, FormsModule, BrowserAnimationsModule, HttpModule, MatProgressBarModule ],
    exports: [ MatProgressBarModule ],
    declarations: [ AppComponent ],
    bootstrap:    [ AppComponent ]
})
export class AppModule { }