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

# summary stats
MeanRentPerSuburb <- data.table(ddply(rental, .(Suburb), summarise, rent_mean=mean(RentPerWeek), rent_sd=sd(RentPerWeek)))[order(rent_mean)]
MeanPricePerSuburb <- data.table(ddply(subset(residential,StartPrice != -99), .(Suburb), summarise, price_mean=mean(StartPrice), price_sd=sd(StartPrice)))[order(price_mean)]

residential_west <- sqldf("SELECT * FROM residential WHERE StartPrice > 100000 AND StartPrice < 500000 AND District == 'Christchurch City'
                           AND PropertyType != 'Apartment' AND PropertyType != 'Section' AND Longitude < 172.639332") # around manchester street
residential_east <- sqldf("SELECT * FROM residential WHERE StartPrice > 100000 AND StartPrice < 500000 AND District == 'Christchurch City'
                           AND PropertyType != 'Apartment' AND PropertyType != 'Section' AND Longitude >= 172.639332") # around manchester street

view <- residential_west[order(StartPrice)]
view <- subset(view, select = c(ListingId,Title, StartPrice, Suburb, Address, PropertyType))


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
