library('irr')

dq1 <- read.csv("/Users/sarahwagner/Documents/RoboticsLab/data_analysis/short_answer/DQ1.csv")
dq1<- na.omit(dq1)
dq2 <- read.csv("/Users/sarahwagner/Documents/RoboticsLab/data_analysis/short_answer/DQ2.csv")
dq3 <- read.csv("/Users/sarahwagner/Documents/RoboticsLab/data_analysis/short_answer/DQ3.csv")
dq4 <- read.csv("/Users/sarahwagner/Documents/RoboticsLab/data_analysis/short_answer/DQ4.csv")

sq1 <- read.csv("/Users/sarahwagner/Documents/RoboticsLab/data_analysis/short_answer/SQ1.csv")
sq2 <- read.csv("/Users/sarahwagner/Documents/RoboticsLab/data_analysis/short_answer/SQ2.csv")
sq3 <- read.csv("/Users/sarahwagner/Documents/RoboticsLab/data_analysis/short_answer/SQ3.csv")
sq4 <- read.csv("/Users/sarahwagner/Documents/RoboticsLab/data_analysis/short_answer/SQ4.csv")

norm.vars <- read.csv("/Users/sarahwagner/Documents/RoboticsLab/data_analysis/norm_vars.csv")

num_samps <- 2
num_samps_cohen <- 4

#put all data into a list and clean
#all.data <- list(dq1, sq1, dq2, sq2, dq3, sq3, dq4, sq4)
all.data <- list(dq1, sq1)
all.data.d <- list(dq1, dq2, dq3, dq4)
all.data.s <- list(sq1, sq2, sq3, sq4)
rm(dq1, dq2, dq3, dq4, sq1, sq2, sq3, sq4)

for( i in 1:num_samps){
  all.data[[i]] <- na.omit(all.data[[i]])
}
for( i in 1:num_samps_cohen){
  all.data.d[[i]] <- na.omit(all.data.d[[i]])
}
for( i in 1:num_samps_cohen){
  all.data.s[[i]] <- na.omit(all.data.s[[i]])
}

#grab active verb data
active <- data.frame(id = integer(), all.verbs = integer(), active.verbs =integer(), condition = character())
active.d <- data.frame(id = integer(), all.verbs = integer(), active.verbs =integer(), condition = character())
active.s <- data.frame(id = integer(), all.verbs = integer(), active.verbs =integer(), condition = character())
want <- c("Participant.ID", "verb.phrases.total", "verb.phrases.active","condition")
for (i in 1:num_samps){
  df <- all.data[[i]][(which(colnames(all.data[[i]]) %in% want))]
  active<-rbind (active, df)
}
for (i in 1:num_samps_cohen){
  df.d <- all.data.d[[i]][(which(colnames(all.data.d[[i]]) %in% want))]
  active.d<-rbind (active.d, df.d)
}
for (i in 1:num_samps_cohen){
  df.s <- all.data.s[[i]][(which(colnames(all.data.s[[i]]) %in% want))]
  active.s<-rbind (active.s, df.s)
}

#Cohen's Kappa
ratings <- cbind(active.s$verb.phrases.active/active.s$verb.phrases.total, active.d$verb.phrases.active/active.d$verb.phrases.total)
ratings[is.nan(ratings)] <- -1
kappa2(ratings)

active.total <- aggregate(active$verb.phrases.total, by= list(Category=active$Participant.ID), FUN=sum)
names(active.total)<-c("Participant.ID", "verb.phrases.total")
active.active <- aggregate(active$verb.phrases.active, by= list(Category=active$Participant.ID), FUN=sum)
names(active.active)<-c("Participant.ID", "verb.phrases.active")
active <- cbind (merge(active.total, active.active), all.data[[1]]$condition)
active <- cbind(active, active$verb.phrases.active/active$verb.phrases.total)
#names(active) <- c("Participant.ID", "anthro?", "condition")

active<- merge(active, norm.vars)
active <- active[complete.cases(active),]

cond <- aov(active$`active$verb.phrases.active/active$verb.phrases.total` ~ active$`all.data[[1]]$condition`+ active$Gender + active$use.profanity + active$around.you.use.profanity)
aov.pval <- summary(cond)[[1]][["Pr(>F)"]][1]
print(aov.pval)
aov.fval <- summary(cond)[[1]][["F value"]][1]
print(aov.fval)

