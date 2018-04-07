import { Component, Injectable ,OnInit } from '@angular/core';
import { RecommenderService } from './services/recommender.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
})


export class AppComponent implements OnInit {
  title = 'app';


   
  public allcityRates = []
  public cityRates = []
  readonly = true;


  constructor(private recommenderService:RecommenderService){}


    ngOnInit(){
      this.getMyRecommendations();
      this.getAllCities();

    }

    changeRating(index,d){
      d.allcity_rating = index+1;
      console.log(d);

    }


    getAllCities(){
       
      this.recommenderService.getAllRatings()
      .subscribe(
        resone=>{
          let allresponseData = resone; 
          var allcities = []
           var alldata ={}
           alldata = allresponseData

              for(var i in alldata['id']){
                allcities.push({
                  "allcity_id":alldata['id'][i],
                  "allcity_name":alldata['cityname'][i],
                  "allcity_rating":alldata['rating'][i],
                  "allcity_user_id":alldata['user_id'][i],
                })
              }

            this.allcityRates = allcities;
            console.log(this.allcityRates)

        });
    }



    getMyRecommendations(){
  
      this.recommenderService.getMyRec()
      .subscribe(
        restwo=>{
          let myresponseData = restwo;
          var cities = []
          var mydata ={} 

             mydata = myresponseData.rating
           // console.log(this.mydata);
            for (var mycity in mydata) {
              cities.push({"mycity_name":mycity, "mycity_rating":mydata[mycity]})

            }
            this.cityRates = cities;
            // console.log(this.cityRates);

        });

    }

    updateMyRecommendations(rating,obj1){
        var obj2 ={
          "id":'',
          "userid": '',
          "cityname": '',
          "rating": ''
        }


       
        obj2= {
          "id":obj1.allcity_id,
          "userid": obj1.allcity_user_id,
          "cityname": obj1.allcity_name,
          "rating": obj1.allcity_rating
        }

        obj2.rating = rating+1;


      this.recommenderService.updateRating(obj2.id,obj2)
      .subscribe(
        res => {
          console.log(res);
          this.getMyRecommendations();
          this.getAllCities();
        },
        err => {
          console.log("Error occured");
        }
      );

    }

  

  

}
