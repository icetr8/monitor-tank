# monitoring-tank
DjangoRest Heroku Postgres


## RECIEVING SMS POST REQUEST EXAMPLE

[http://localhost:8000/v1/smsreciever/](http://localhost:8000/v1/smsreciever/) - Development
[https://monitor-tank.herokuapp.com/v1/smsreciever](https://monitor-tank.herokuapp.com/v1/smsreciever) - Production

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
