# ====================================== load database ===============================================
rm(list=ls())
options(stringsAsFactors = FALSE)

library(RSQLite)
library(ggplot2)
library(data.table)
library(sqldf)
library(plyr)
library(lubridate)

drv <- dbDriver("SQLite")
con <- dbConnect(drv, dbname="/Users/james/development/personal/nz-houses/db/prod1.db") 

rs <- dbSendQuery(con,"select * from residential_listings;") # where day between '22-Aug-2012' and '02-Sep-2012'
residential_raw <- data.table(fetch(rs,n=-1))
dbClearResult(rs)

rs <- dbSendQuery(con,"select * from rental_listings;") # where day between '22-Aug-2012' and '02-Sep-2012'
rental_raw <- data.table(fetch(rs,n=-1))
dbClearResult(rs)

dbDisconnect(con)
dbUnloadDriver(drv)
rm(con,drv,rs)

# ====================================== load functions ===============================================

datefunctionOne <- function(x) { y <- as.POSIXlt(as.numeric(gsub("d", "", x))/1000, origin="1970-01-01"); return(y) }

# ====================================== pre process ================================================

residential <- residential_raw
residential$StartDate <- data.frame(datefunctionOne(residential$StartDate))
residential <- subset(residential, StartDate > as.POSIXct('2013-01-01') & StartPrice != -99 & StartPrice < 1000000)
rental <- rental_raw
rental$StartDate <- data.frame(datefunctionOne(rental$StartDate))
rental <- subset(rental, StartDate >as.POSIXct('2013-01-01'))


# ====================================== three bdrm vs two bdrm ================================================

three_bdrm_rent_by_suburb <- data.table(ddply(subset(rental,Bedrooms==3), .(Suburb), summarise, counts=length(Suburb),rent_mean=mean(RentPerWeek), rent_median=median(RentPerWeek),rent_sd=sd(RentPerWeek)))[order(rent_mean)][order(-rent_median)]
three_bdrm_price_by_suburb <- data.table(ddply(subset(residential,StartPrice != -99), .(Suburb), summarise, counts=length(Suburb),price_mean=mean(StartPrice), price_median=median(StartPrice), price_sd=sd(StartPrice)))[order(price_mean)]
three_bdrm_by_suburb <- data.table(sqldf("SELECT three_bdrm_rent_by_suburb.Suburb, rent_median, price_median, three_bdrm_rent_by_suburb.counts AS rent_count, three_bdrm_price_by_suburb.counts AS price_count FROM three_bdrm_rent_by_suburb JOIN three_bdrm_price_by_suburb ON three_bdrm_rent_by_suburb.Suburb == three_bdrm_price_by_suburb.Suburb"))[order(-price_median)]
three_bdrm_by_suburb$ratio <- (three_bdrm_by_suburb$rent_median/three_bdrm_by_suburb$price_median)

two_bdrm_rent_by_suburb <- data.table(ddply(subset(rental,Bedrooms==2), .(Suburb), summarise, counts=length(Suburb),rent_mean=mean(RentPerWeek), rent_median=median(RentPerWeek),rent_sd=sd(RentPerWeek)))[order(rent_mean)][order(-rent_median)]
two_bdrm_price_by_suburb <- data.table(ddply(subset(residential,StartPrice != -99), .(Suburb), summarise, counts=length(Suburb),price_mean=mean(StartPrice), price_median=median(StartPrice), price_sd=sd(StartPrice)))[order(price_mean)]
two_bdrm_by_suburb <- data.table(sqldf("SELECT two_bdrm_rent_by_suburb.Suburb, rent_median, price_median, two_bdrm_rent_by_suburb.counts AS rent_count, two_bdrm_price_by_suburb.counts AS price_count FROM two_bdrm_rent_by_suburb JOIN two_bdrm_price_by_suburb ON two_bdrm_rent_by_suburb.Suburb == two_bdrm_price_by_suburb.Suburb"))[order(-price_median)]
two_bdrm_by_suburb$ratio <- (two_bdrm_by_suburb$rent_median/two_bdrm_by_suburb$price_median)

bedroom_comparison <- data.table(sqldf("SELECT three_bdrm_by_suburb.Suburb, three_bdrm_by_suburb.ratio AS three_bdrm_ratio, two_bdrm_by_suburb.ratio AS two_bdrm_ratio, three_bdrm_by_suburb.price_median AS three_bdrm_price, two_bdrm_by_suburb.price_median AS two_bdrm_price,
                                       three_bdrm_by_suburb.price_count AS three_bdrm_price_count, two_bdrm_by_suburb.price_count AS two_bdrm_price_count, three_bdrm_by_suburb.rent_count AS three_bdrm_rent_count, two_bdrm_by_suburb.rent_count AS two_bdrm_rent_count,
                                       three_bdrm_by_suburb.rent_median AS three_bdrm_rent, two_bdrm_by_suburb.rent_median AS two_bdrm_median FROM three_bdrm_by_suburb JOIN two_bdrm_by_suburb ON three_bdrm_by_suburb.Suburb == two_bdrm_by_suburb.Suburb"))

bedroom_comparison$three_bdrm_to_two_bdrm_ratio <- (bedroom_comparison$three_bdrm_ratio / bedroom_comparison$two_bdrm_ratio)
bedroom_comparison <- bedroom_comparison[order(-three_bdrm_to_two_bdrm_ratio)]

bedroom_comparison_10_plus <- (subset(bedroom_comparison, two_bdrm_price_count > 9 & three_bdrm_price_count > 9 & two_bdrm_rent_count > 9 & three_bdrm_rent_count > 9))

bedroom_comparison_10_plus$Suburb <- factor(bedroom_comparison_10_plus$Suburb, levels=bedroom_comparison_10_plus$Suburb[order(bedroom_comparison_10_plus$three_bdrm_to_two_bdrm_ratio)])
ggplot(bedroom_comparison_10_plus, aes(Suburb, three_bdrm_to_two_bdrm_ratio)) +
  geom_bar(stat="identity",color='dark grey',fill='dark grey') +
  coord_flip() +
  ylab("3 bedroom (rent/price) vs 2 bedroom (rent/price)") + xlab("") + ylim(0,2) +
  labs(title = "Three bedrooms is nearly 1.5 times better than two bedrooms") + theme(plot.title = element_text(size = rel(1.5))) +
  geom_bar(data=subset(bedroom_comparison_10_plus, Suburb %in% c('Spreydon','Addington','Woolston')), aes(Suburb, three_bdrm_to_two_bdrm_ratio), fill="pink", stat="identity")


# ====================     investigate suburbs

residential3 <- subset(residential,Bedrooms==3)
price_by_suburb <- data.table(Suburb=residential3$Suburb,StartPrice=residential3$StartPrice)
price_by_suburb <- price_by_suburb[,list(price=median(StartPrice)),by=Suburb]

price_by_suburb$Suburb <- factor(price_by_suburb$Suburb, levels=price_by_suburb$Suburb[order(price_by_suburb$price)])
ggplot(price_by_suburb, aes(Suburb, price)) +
  geom_bar(stat="identity",color='dark grey',fill='dark grey') +
  coord_flip() +
  ylab("Price") + xlab("") +#+ ylim(0,2) +
  labs(title = "Median Price by Suburb") + theme(plot.title = element_text(size = rel(1.5))) +
  geom_bar(data=subset(price_by_suburb, Suburb %in% c('Spreydon','Addington','Woolston')), aes(Suburb, price), fill="pink", stat="identity")

bedroom_comparison_10_plus$Suburb <- factor(bedroom_comparison_10_plus$Suburb, levels=bedroom_comparison_10_plus$Suburb[order(bedroom_comparison_10_plus$three_bdrm_ratio)])
ggplot(bedroom_comparison_10_plus, aes(Suburb, three_bdrm_ratio)) +
  geom_bar(stat="identity",color='dark grey',fill='dark grey') +
  coord_flip() +
  ylab("Ratio of rent to price") + xlab("Suburb") +
  labs(title = "Rent as a fraction of Price, by Suburb") + theme(plot.title = element_text(size = rel(1.5))) +
  geom_bar(data=subset(bedroom_comparison_10_plus, Suburb %in% c('Spreydon','Addington','Woolston')), aes(Suburb, three_bdrm_ratio), fill="pink", stat="identity")

ggplot(subset(rental,Suburb %in% c('Spreydon','Addington','Woolston') & Bedrooms==3)) + geom_density(aes(x=RentPerWeek,color=Suburb),binwidth=20) + xlim(250,650)
ggplot(subset(residential, Suburb %in% c('Spreydon','Addington','Woolston') & Bedrooms==3)) + geom_density(aes(x=StartPrice,color=Suburb)) + xlim(100000,500000)



# ====================================== prices by time ================================================

sub_residential <- subset(residential,StartDate >= as.POSIXct('2013-08-02') & StartPrice < 500000 & StartPrice > 200000)
price_over_time <- data.table(Suburb=sub_residential$Suburb,date=sub_residential$StartDate,StartPrice=sub_residential$StartPrice)
price_over_time$month <- data.frame(round_date(price_over_time$date, "month"))
median_monthly_price <- price_over_time[, list(price = mean(StartPrice),count=length(StartPrice)), by=month][order(month)]
#ggplot(median_monthly_price) + geom_line(aes(x=month,y=price), colour = 'dark grey')


sub_residential <- subset(residential, StartPrice < 500000 & StartPrice > 200000)
sub_residential$month <- data.frame(round_date(sub_residential$StartDate, "month"))
variation_by_month <- data.table(sub_residential[, list(price = median(StartPrice)), by = month(StartDate)])[order(month)]
ggplot(variation_by_month, aes(factor(month),price)) + geom_bar(color='dark grey',fill='dark grey') + xlab('month of the year') + ylab('mean (median price for the month) since April 2011') +
  xlab('Month') + ylab('Median Price in Christchurch') + 
  labs(title = "When to Buy a House: March and April") + theme(plot.title = element_text(size = rel(1.5)))


sub_residential <- subset(residential,StartDate >= as.POSIXct('2013-08-02'))
price_over_time <- data.table(Suburb=sub_residential$Suburb,date=sub_residential$StartDate,StartPrice=sub_residential$StartPrice)
price_over_time$month <- data.frame(round_date(price_over_time$date, "month"))
ggplot(price_over_time) + geom_point(aes(x=date,y=StartPrice,color=Suburb),size=1, show_guide=FALSE) + xlim(as.POSIXct('2013-08-01'),as.POSIXct('2014-01-03')) + ylim(1.5e5,5.5e5) +
  geom_line(data = median_monthly_price, aes(x=month, y=price), colour="#000099", show_guide = FALSE) + #group=sample_column
  xlab('Month') + ylab('Median Price in Christchurch') + 
  labs(title = "Median Prices went up by $50k August to December 2013") + theme(plot.title = element_text(size = rel(1.5)))







# ====================     how many houses have a price listed
ListingsWithPrice <- data.table(ddply(residential_raw, .(), summarise, count_total=length(Suburb), count_noprice=count(StartPrice==-99)$freq[1],count_hasprice=count(StartPrice==-99)$freq[2]))
ListingsWithPriceBySuburb <- data.table(ddply(residential, .(Suburb), summarise, count_total=length(Suburb), count_noprice=count(StartPrice==-99)$freq[1],count_hasprice=count(StartPrice==-99)$freq[2]))[order(-count_total)]

# ====================     areas of interest
residential_west <- sqldf("SELECT * FROM residential WHERE StartPrice > 100000 AND StartPrice < 500000 AND District == 'Christchurch City'
                           AND PropertyType != 'Apartment' AND PropertyType != 'Section' AND Longitude < 172.639332") # around manchester street
residential_west_3plusbedrooms <- data.table(sqldf("SELECT * FROM residential WHERE Bedrooms >= 3 AND District == 'Christchurch City'
                           AND PropertyType != 'Apartment' AND PropertyType != 'Section' AND Longitude < 172.639332"))[order(StartDate)] # around manchester street
residential_northwest_3plusbedrooms <- sqldf("SELECT * FROM residential WHERE Bedrooms >= 3 AND District == 'Christchurch City'
                           AND PropertyType != 'Apartment' AND PropertyType != 'Section' AND Longitude < 172.639332 AND Latitude > -43.541174") # around manchester street
residential_east <- sqldf("SELECT * FROM residential WHERE StartPrice > 100000 AND StartPrice < 500000 AND District == 'Christchurch City'
                           AND PropertyType != 'Apartment' AND PropertyType != 'Section' AND Longitude >= 172.639332") # around manchester street

residential_northwest_3plusbedrooms <- data.table(residential_northwest_3plusbedrooms)[order(StartPrice)]
residential_northwest_3plusbedrooms_fewcolumns <- subset(residential_northwest_3plusbedrooms, select = c(ListingId,Title, StartPrice, Suburb, Address, PropertyType))

MeanPricePerSuburb_northwest_3plusbedrooms <- data.table(ddply(subset(residential_northwest_3plusbedrooms,StartPrice != -99), .(Suburb), summarise, counts=length(Suburb),price_mean=mean(StartPrice), price_median=median(StartPrice), price_sd=sd(StartPrice)))[order(price_mean)]





cheap <- data.table(sqldf("SELECT ListingId,Title,Suburb,StartPrice,StartDate,EndDate FROM residential WHERE District == 'Christchurch City' AND Suburb != 'New Brighton' AND StartPrice != -99 AND StartPrice > 250000 AND StartPrice < 350000
                                       AND PropertyType != 'Apartment' AND PropertyType != 'Section' AND Longitude < 172.639332 AND Bedrooms == 3"))[order(Suburb)]

cheap$StartDate <- data.frame(datefunctionOne(cheap[["StartDate"]]))
cheap$EndDate <- data.frame(datefunctionOne(cheap[["EndDate"]]))
cheap <- subset(cheap,EndDate > Sys.time())
cheap <- cheap[order(StartDate)]
View(cheap)







# paste('http://www.trademe.co.nz/Browse/Listing.aspx?id=','ListingId',sep="")
# system('/usr/bin/open -a \"/Applications/Google Chrome.app\" \'http://www.trademe.co.nz/Browse/Listing.aspx?id=626464683\'')

# plotting
ggplot(subset(residential,StartPrice > 0 & PropertyType == 'House')) + geom_histogram(aes(StartPrice)) + xlim(0,1000000)
ggplot(residential) + geom_histogram(aes(x=residential$LandArea)) + xlim(100,2000)

# analysis
h_listings=data.table(h_listings)
average_section <- h_listings[, list(ss=mean(LandArea)), by=factor(Suburb)]
average_section <- subset(average_section,ss>1)[order(ss)]
ggplot(average_section) + geom_bar(aes(x=factor,y=ss),stat="identity")


hillie <- data.table(subset(residential,Suburb == 'Huntsbury' | Suburb == 'aa' ))[order(StartDate)]
ggplot(hillie) + geom_histogram(aes(x=StartPrice))

ggplot(hillie, aes(Suburb, three_bdrm_ratio)) +
  geom_bar(stat="identity",color='dark grey',fill='dark grey') +
  coord_flip() +
  ylab("Ratio of rent to price") + xlab("Suburb") +
  labs(title = "Rent as a fraction of Price, by Suburb") + theme(plot.title = element_text(size = rel(1.5))) +
  geom_bar(data=subset(bedroom_comparison_10_plus, Suburb %in% c('Spreydon','Addington','Woolston')), aes(Suburb, three_bdrm_ratio), fill="pink", stat="identity")

