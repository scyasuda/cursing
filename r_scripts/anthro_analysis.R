library('irr')

dq1 <- read.csv("/Users/sarahwagner/Documents/RoboticsLab/data_analysis/short_answer/DQ1.csv")
dq2 <- read.csv("/Users/sarahwagner/Documents/RoboticsLab/data_analysis/short_answer/DQ2.csv")
dq3 <- read.csv("/Users/sarahwagner/Documents/RoboticsLab/data_analysis/short_answer/DQ3.csv")
dq4 <- read.csv("/Users/sarahwagner/Documents/RoboticsLab/data_analysis/short_answer/DQ4.csv")

sq1 <- read.csv("/Users/sarahwagner/Documents/RoboticsLab/data_analysis/short_answer/SQ1.csv")
sq2 <- read.csv("/Users/sarahwagner/Documents/RoboticsLab/data_analysis/short_answer/SQ2.csv")
sq3 <- read.csv("/Users/sarahwagner/Documents/RoboticsLab/data_analysis/short_answer/SQ3.csv")
sq4 <- read.csv("/Users/sarahwagner/Documents/RoboticsLab/data_analysis/short_answer/SQ4.csv")

norm.vars <- read.csv("/Users/sarahwagner/Documents/RoboticsLab/data_analysis/norm_vars.csv")

#put all data into a list and clean
#all.data <- list(dq1, sq1, dq2, sq2, dq3, sq3, dq4, sq4)
all.data <- list(dq2, sq2)
all.data.d <- list(dq4)
all.data.s <- list(sq4)

num_samps <- 2
num_samps_cohen <- 1

for( i in 1:num_samps){
  all.data[[i]] <- na.omit(all.data[[i]])
}
for( i in 1:num_samps_cohen){
  all.data.d[[i]] <- na.omit(all.data.d[[i]])
  all.data.s[[i]] <- na.omit(all.data.s[[i]])  
}

#grab anthro data
anthro <- data.frame(id = integer(), condition = character(), anthro = integer())
anthro.d <- data.frame(id = integer(), condition = character(), anthro = integer())
anthro.s <- data.frame(id = integer(), condition = character(), anthro = integer())
names(anthro) <- c("Participant.ID", "anthro?", "condition")

want <- c("Participant.ID", "anthropomorphized", "condition")
for (i in 1:num_samps){
  df <- all.data[[i]][(which(colnames(all.data[[i]]) %in% want))]
  anthro<-rbind (anthro, df)
}

for (i in 1:num_samps_cohen){
  df.d <- all.data.d[[i]][(which(colnames(all.data.d[[i]]) %in% want))]
  anthro.d<-rbind (anthro.d, df.d)
}

for (i in 1:num_samps_cohen){
  df.s <- all.data.s[[i]][(which(colnames(all.data.s[[i]]) %in% want))]
  anthro.s<-rbind (anthro.s, df.s)
}

#Cohen's Kappa
ratings <- cbind(anthro.s$anthropomorphized, anthro.d$anthropomorphized)
kappa2(ratings)

anthro <- cbind(aggregate(anthro$anthropomorphized, by= list(Category=anthro$Participant.ID), FUN=sum), all.data[[1]]$condition)
names(anthro) <- c("Participant.ID", "anthro?", "condition")
anthro <- merge(anthro, norm.vars)

#split by condition
a.curse <- anthro[which(anthro$condition == 2), ]
a.control <- anthro[which(anthro$condition == 3), ]
print(mean(a.curse$`anthro?`))
print(mean(a.control$`anthro?`))

cond <- aov(anthro$`anthro?` ~ anthro$condition + anthro$Gender + anthro$use.profanity + anthro$around.you.use.profanity)
aov.pval <- summary(cond)[[1]][["Pr(>F)"]][1]
print(aov.pval)
aov.fval <- summary(cond)[[1]][["F value"]][1]
print(aov.fval)

exp_cond1_on_with_group <- glm(anthro$`anthro?` ~ anthro$condition + anthro$Gender + anthro$use.profanity + anthro$around.you.use.profanity, family = "binomial")
print(exp_cond1_on_with_group)
summary(exp_cond1_on_with_group)



