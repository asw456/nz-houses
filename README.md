## NZ housing market data analysis

This project was set up a while ago for collecting residential and rental listing information, historical market information, and analyzing this information to inform a house purchase.

Data is predominantly collected from the [Trademe](http://trademe.co.nz) API. Additional information such as school zone, geographical info, and demographic data is collected from the [Koordinates](http://koordinates.com) API and [Stats NZ](http://stats.govt.nz).

### Working

- clients for the Trademe and Koordinates APIs
- sqlite3 database with residential and rental listings for Christchurch, NZ since July 2013
- data exploration scripts and some monte carlo interest rate 'forecasting' code

### To Do

- what's the best mortgage size for a given deposit over a 10-year period?
- refactor the exploration scripts
