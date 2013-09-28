options(stringsAsFactors = FALSE)

library(RSQLite)
library(ggplot2)
library(data.table)
library(sqldf)
library(plyr)

drv <- dbDriver("SQLite")
con <- dbConnect(drv, dbname="/Users/james/development/resources/nz-houses/db/test.db") 

rs <- dbSendQuery(con,"select * from residential_listings;") # where day between '22-Aug-2012' and '02-Sep-2012'
residential <- data.table(fetch(rs,n=-1))
dbClearResult(rs)

rs <- dbSendQuery(con,"select * from rental_listings;") # where day between '22-Aug-2012' and '02-Sep-2012'
rental <- data.table(fetch(rs,n=-1))
dbClearResult(rs)

dbDisconnect(con)
dbUnloadDriver(drv)
rm(con,drv,rs)



# ====================     summary stats
MeanRentPerSuburb_Overall <- data.table(ddply(rental, .(Suburb), summarise, counts=length(Suburb),rent_mean=mean(RentPerWeek), rent_median=median(RentPerWeek),rent_sd=sd(RentPerWeek)))[order(rent_mean)]
MeanPricePerSuburb_Overall <- data.table(ddply(subset(residential,StartPrice != -99), .(Suburb), summarise, counts=length(Suburb),price_mean=mean(StartPrice), price_median=median(StartPrice), price_sd=sd(StartPrice)))[order(price_mean)]

# ====================     how many houses have a price listed
ListingsWithPrice <- data.table(ddply(residential, .(), summarise, count_total=length(Suburb), count_noprice=count(StartPrice==-99)$freq[1],count_hasprice=count(StartPrice==-99)$freq[2]))
ListingsWithPriceBySuburb <- data.table(ddply(residential, .(Suburb), summarise, count_total=length(Suburb), count_noprice=count(StartPrice==-99)$freq[1],count_hasprice=count(StartPrice==-99)$freq[2]))[order(-count_total)]

# ====================     areas of interest
residential_west <- sqldf("SELECT * FROM residential WHERE StartPrice > 100000 AND StartPrice < 500000 AND District == 'Christchurch City'
                           AND PropertyType != 'Apartment' AND PropertyType != 'Section' AND Longitude < 172.639332") # around manchester street
residential_west_3plusbedrooms <- sqldf("SELECT * FROM residential WHERE Bedrooms >= 3 AND District == 'Christchurch City'
                           AND PropertyType != 'Apartment' AND PropertyType != 'Section' AND Longitude < 172.639332") # around manchester street
residential_northwest_3plusbedrooms <- sqldf("SELECT * FROM residential WHERE Bedrooms >= 3 AND District == 'Christchurch City'
                           AND PropertyType != 'Apartment' AND PropertyType != 'Section' AND Longitude < 172.639332 AND Latitude > -43.541174") # around manchester street
residential_east <- sqldf("SELECT * FROM residential WHERE StartPrice > 100000 AND StartPrice < 500000 AND District == 'Christchurch City'
                           AND PropertyType != 'Apartment' AND PropertyType != 'Section' AND Longitude >= 172.639332") # around manchester street

residential_northwest_3plusbedrooms <- data.table(residential_northwest_3plusbedrooms)[order(StartPrice)]
residential_northwest_3plusbedrooms_fewcolumns <- subset(residential_northwest_3plusbedrooms, select = c(ListingId,Title, StartPrice, Suburb, Address, PropertyType))

MeanPricePerSuburb_northwest_3plusbedrooms <- data.table(ddply(subset(residential_northwest_3plusbedrooms,StartPrice != -99), .(Suburb), summarise, counts=length(Suburb),price_mean=mean(StartPrice), price_median=median(StartPrice), price_sd=sd(StartPrice)))[order(price_mean)]



yaldhurt <- data.table(sqldf("SELECT * FROM residential WHERE Bedrooms >= 3 AND District == 'Christchurch City' AND Suburb == 'Yaldhurst '
                           AND PropertyType != 'Apartment' AND PropertyType != 'Section' AND Longitude < 172.639332"))[order(-StartPrice)]



# paste('http://www.trademe.co.nz/Browse/Listing.aspx?id=','ListingId',sep="")
# system('/usr/bin/open -a \"/Applications/Google Chrome.app\" \'http://www.trademe.co.nz/Browse/Listing.aspx?id=626464683\'')

# plotting
ggplot(subset(h_listings,StartPrice > 0 & PropertyType == 'House')) + geom_histogram(aes(StartPrice)) + xlim(0,500000)
ggplot(h_listings) + geom_histogram(aes(x=h_listings$LandArea)) + xlim(100,2000)

# analysis
h_listings=data.table(h_listings)
average_section <- h_listings[, list(ss=mean(LandArea)), by=factor(Suburb)]
average_section <- subset(average_section,ss>1)[order(ss)]
ggplot(average_section) + geom_bar(aes(x=factor,y=ss),stat="identity")
