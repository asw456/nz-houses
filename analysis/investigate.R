
library(RSQLite)
library(ggplot2)
library(data.table)
library(sqldf)

drv <- dbDriver("SQLite")
con <- dbConnect(drv, dbname="/Users/alanw/development/resources/nz-houses/db/test.db") 

rs <- dbSendQuery(con,"select * from residential_listings;") # where day between '22-Aug-2012' and '02-Sep-2012'
h_listings <- fetch(rs,n=-1)
dbClearResult(rs)

dbDisconnect(con)
dbUnloadDriver(drv)
rm(con,drv,rs)

head(h_listings)

h_listings = subset(h_listings,LandArea < 2000)
h_listings = subset(h_listings,LandArea > 100)

ggplot(h_listings) + geom_histogram(aes(x=h_listings$LandArea)) + xlim(100,2000)

#rm(h_listings)