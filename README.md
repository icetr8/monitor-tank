# monitoring-tank
DjangoRest Heroku Postgres


## RECIEVING SMS POST REQUEST EXAMPLE

* [http://localhost:8000/v1/smsreciever/](http://localhost:8000/v1/smsreciever/) - Development
* [https://monitor-tank.herokuapp.com/v1/smsreciever](https://monitor-tank.herokuapp.com/v1/smsreciever) - Production

```
{
  "inboundSMSMessageList":{
      "inboundSMSMessage":[
         {
            "dateTime":"Fri Nov 22 2013 12:12:13 GMT+0000 (UTC)",
            "destinationAddress":"tel:21581234",
            "messageId":null,
            "message":" 'ph': '7', 'temp': '29', 'oxygen': '13', 'water': 'normal' ",
            "resourceURL":null,
            "senderAddress":"tel:+639171234567"
         }
       ],
       "numberOfMessagesInThisBatch":1,
       "resourceURL":null,
       "totalNumberOfPendingMessages":null
   }
}
```
In SMS type the following format
```
'ph': '7', 'temp': '39', 'oxygen': '13', 'water': 'normal'
```

## Openweather api for tanay rizal

- 1683319	Tanay	14.496800	121.284599	PH
```
id = 1683319
nm = Tanay
lat = 14.1496800
lon = 121.284599
loc = PH
```
* 5 day forecast
https://pyowm.readthedocs.io/en/latest/pyowm.webapi25.html#pyowm.webapi25.forecast.Forecast

* 5 day forecast day, get present up to 38 incremented by 3 hours per index

```
fc.get_forecast().get_weathers()[0].get_reference_time(timeformat='unix')
```

* 5 day forecast day get time GMT

```
fc.get_forecast().get_weathers()[0].get_reference_time(timeformat='unix')
```

* get temp in kelvins

```
fc.get_forecast().get_weathers()[0].get_temperature()['temp']
```

* get detailed status
```
fc.get_forecast().get_weathers()[0].get_detailed_status()
```
