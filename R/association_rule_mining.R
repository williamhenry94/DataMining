library(readr)
library(arules)
args = commandArgs(trailingOnly=TRUE)
generateAssociationRule <- function(){
    data_set <- read_csv("/Users/williamhenry/Documents/DataMining.Main/datasets_csv/All_datas.csv") #args[1]
    data_set_min <-subset(data_set,select=c('Unemployment_rating','QpsOffence','Solved','Suburb','MeshBlockId','OffenceCount'))
    part_of_data <- data_set_min[,1:4]
    part_of_data <-data.frame(sapply(part_of_data,as.factor))
    rules <- apriori(part_of_data,parameter = list(supp=0.001, conf=0.4,minlen=2))
    rules <- sort(rules, by="lift")
   
    inspect(rules)

    write(rules,
      file = "../rules/association_rules.csv",
      sep = ",",
      quote = TRUE,
      row.names = FALSE)

    # itemsets <- unique(generatingItemsets(rules))
    # itemsets.df <- as(itemsets, "data.frame")
    # View (itemsets.df)
    # frequentItemsets <- itemsets.df[with(itemsets.df, order(-support,items))]
    # names(frequentItemsets)[1] <- "itemset"
    # write.table(frequentItemsets, file = "Rules-East.txt", sep = ",", row.names = FALSE)
    
}


generateAssociationRule()

