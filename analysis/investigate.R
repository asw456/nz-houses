
library(RSQLite)
library(ggplot2)
library(data.table)
library(sqldf)

drv <- dbDriver("SQLite")
con <- dbConnect(drv, dbname="/Users/alanw/development/resources/nz-houses/db/test.db") 

rs <- dbSendQuery(con,"select * from residential_listings limit 10;") # where day between '22-Aug-2012' and '02-Sep-2012'
h_listings <- fetch(rs,n=-1)
dbClearResult(rs)



dbDisconnect(con)
dbUnloadDriver(drv)
rm(con,drv,rs)


head(h_listings)
rm(h_listings)