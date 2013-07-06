
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

ggplot(subset(h_listings,StartPrice > 0 & PropertyType == 'House')) + geom_histogram(aes(StartPrice)) + xlim(0,500000)
ggplot(h_listings) + geom_histogram(aes(x=h_listings$LandArea)) + xlim(100,2000)

h_listings=data.table(h_listings)
average_section <- h_listings[, list(ss=mean(LandArea)), by=factor(Suburb)]
average_section <- subset(average_section,ss>1)[order(ss)]
ggplot(average_section) + geom_bar(aes(x=factor,y=ss),stat="identity")

#rm(h_listings)