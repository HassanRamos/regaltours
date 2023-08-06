First
```
1.) Install docker into your environment
2.) Install docker-compose
```

Next
```
 run this command : docker-compose up --build
```

This will spin up 
```
1.) Database (postgres) 
2.) Queue (Redis) 
3.) Application (Django)
```

We have 4 integrations at the moment ,
```
1.) TBO (soap api integration) - provides hotels
2.) viator (rest api integration) -provides tours and attraction sites
3.) Amadeus (iframe integration) -provides flights capability
4.) DPO (soap api integration) - provides checkout capability
```
