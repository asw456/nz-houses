## Data mining the NZ housing market

An over-the-top approach to buying a house in NZ. Aims to pull together publicly available price, location, and geographical data for as many properties as possible. Some early ideas are price, school zone and decile, sunset and sunrise, Stats NZ Deprivation Index and Meshblock, nearby POI, and more as I think of it.

The code currently contains authorized API clients for [Trademe](http://trademe.co.nz) and [Koordinates](http://koordinates.com).

### Brief description
apiTrademe.py downloads a json object containing up to 500 listings, parses it, and inserts the result into the database. If more than 500 listings are returned, it downloads and inserts the additional objects. apiKoordinates.py downloads school zones, the Deprivation Index, and more and inserts into another table. daoSqlite.py contains the transform and insert functions for the api calls.

### TODO

- download trademe descriptions for each property individually, taking api rate limits into account
- match school zone with Decile and possibly national standards
- download Zenbu area data
- look for other data sources to add
- NLP on property descriptions and other modelling
- browser client

