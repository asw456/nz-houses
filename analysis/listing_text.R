options(stringsAsFactors = FALSE)

library(RSQLite)
library(ggplot2)
library(data.table)
library(sqldf)
library(plyr)

drv <- dbDriver("SQLite")
con <- dbConnect(drv, dbname="/Users/james/development/resources/nz-houses/db/test.db") 

rs <- dbSendQuery(con,"select * from residential_individual_listings;") # where day between '22-Aug-2012' and '02-Sep-2012'
residential <- data.table(fetch(rs,n=-1))
dbClearResult(rs)

dbDisconnect(con)
dbUnloadDriver(drv)
rm(con,drv,rs)



