library(readr)
library(arules)
generateAssociationRule <- function(){
    data_set <- read_csv("../datasets_csv/Brisbane_Inner_Merged_Information.csv")
    data_set_min <-subset(data_set,select=c("Suburb","Postcode","OffenceCount","QpsOffence","Solved","Unemployment_rating"))
    part_of_data <- data_set_min[,4:6]
    part_of_data <-data.frame(sapply(part_of_data,as.factor))
    rules <- apriori(part_of_data,parameter = list(supp=0.2, conf=0.5,minlen=2))
    rules <- sort(rules, by="lift")
    inspect(rules)
}


generateAssociationRule()

