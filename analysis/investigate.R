
library(RSQLite)
library(ggplot2)
library(data.table)
library(sqldf)

drv <- dbDriver("SQLite")
con <- dbConnect(drv, dbname="/Users/james/development/resources/nz-houses/db/test.db") 

rs <- dbSendQuery(con,"select * from residential_listings;") # where day between '22-Aug-2012' and '02-Sep-2012'
h_listings <- data.table(fetch(rs,n=-1))
dbClearResult(rs)

dbDisconnect(con)
dbUnloadDriver(drv)
rm(con,drv,rs)

# subsets
h_west <- subset(h_listings, h_listings$Longitude < 172.639332) # around Manchester Street
h_east <- subset(h_listings, h_listings$Longitude >= 172.639332) # http://itouchmap.com/latlong.html

h_west_cheap <- subset(h_west, h_west$StartPrice < 300000)
h_west_cheap <- subset(h_west_cheap, h_west_cheap$StartPrice > 190000)
h_west_cheap <- subset(h_west_cheap, h_west_cheap$StartPrice != -99)
h_west_cheap <- subset(h_west_cheap, h_west_cheap$District == "Christchurch City")
h_west_cheap <- subset(h_west_cheap, h_west_cheap$PropertyType != "Apartment")
h_west_cheap <- subset(h_west_cheap, h_west_cheap$PropertyType != "Section")
head(h_west_cheap[order(StartPrice)])

view <- subset(h_west_cheap, select = c(ListingId,Title, StartPrice, Suburb, Address, PropertyType))

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

# more plotting

# rm(h_listings)