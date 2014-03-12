mydata <- read.csv("databyzip.txt")

library(maps)
map("state")
for (i in 1:length(mydata$lat)) {
  count <- mydata[i,2]
  lat <- mydata[i,3]
  lon <- mydata[i,4]
  points(lon, lat, pch=19, col="red", cex=0.2*count)
}