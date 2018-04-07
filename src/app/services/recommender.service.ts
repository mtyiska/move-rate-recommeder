import { Injectable } from '@angular/core';
import {
	Http,
	Response,
	RequestOptions,
	Headers,
	HttpModule
} from '@angular/http';
import 'rxjs/add/operator/map';


@Injectable()
export class RecommenderService {

  apiRoot: string = "http://localhost:4200";


  constructor(private http:Http) { }

    getAllRatings(){

      let url = `${this.apiRoot}/`;
      return this.http.get(url).map(res=>res.json());

    }

    getMyRec(){

      let url = `${this.apiRoot}/myrec`;
      return this.http.get(url).map(res=>res.json());

    }

    updateRating(_id,obj){

      let url = `${this.apiRoot}/city/`;
      return this.http.put(url+_id, obj).map(res=>res.json());
      

    }

}
