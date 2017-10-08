library(readr)
library(arules)
generateAssociationRule <- function(){
    data_set <- read_csv("../datasets_csv/Brisbane_Inner_Merged_Information.csv")
    data_set_min <-subset(data_set,select=c("Suburb","QpsOffence","Solved","Unemployment_rating"))
    part_of_data <- data_set_min[,1:4]
    part_of_data <-data.frame(sapply(part_of_data,as.factor))
    rules <- apriori(part_of_data,parameter = list(supp=0.01, conf=0.55,minlen=2))
    rules <- sort(rules, by="confidence")
   
    inspect(rules)
    
}


generateAssociationRule()

