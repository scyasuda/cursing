library(ggplot2)
require(gridExtra)
require(likert)
library(cowplot)

dat <- read.csv("/Users/sarahwagner/Documents/RoboticsLab/data_analysis/data.csv")

#Clean unnecessary rows and columns
dat <- dat[, !(names(dat) == "Timestamp")]
dat <- dat[!(dat$Participant.ID == 123) & !(dat$Participant.ID == 139), ] #discard data point due to bad study
dat <- dat[!(dat$True.Condition == 1), ] #discard cheating points
dat <- na.omit(dat)

#remove string labels from numbers
dat <- data.frame(lapply(dat, function(x){
  gsub("1 - Never", "1", x)
}))
dat <- data.frame(lapply(dat, function(x){
  gsub("1 - Definitely Not Associated", "1", x)
}))
dat <- data.frame(lapply(dat, function(x){
  gsub("7 - All the Time", "7", x)
}))
dat <- data.frame(lapply(dat, function(x){
  gsub("7 - All the time", "7", x)
}))
dat <- data.frame(lapply(dat, function(x){
  gsub("7 - Definitely Associated", "7", x)
}))


#convert factors to the same levels
for(i in names(dat)[8:35]){
  #print(i)
  levels(dat[[i]])<- c(1, 2, 3, 4, 5, 6, 7)
  dat[[i]]
}

#extract control columns
normalizing.variables <- dat[,c(2,3, 9, 10)]
write.csv(normalizing.variables, "norm_vars.csv", row.names = FALSE)

#split into cheat, curse, and control
cheat <- dat[dat$True.Condition == 1, ]
curse <- dat[dat$True.Condition == 2, ]
control <- dat[dat$True.Condition == 3, ]

traits <- c("Interactive", "did.speak.to.Nao", "want.to.speak.to.Nao")

#likert plots
plot(likert(curse[15:33])) + labs(title= "Curse")
plot(likert(control[15:33]))+ labs(title = "Control")
plot(likert(curse[which(colnames(curse) %in% traits)])) + labs(title= "Curse")
plot(likert(control[which(colnames(curse) %in% traits)])) + labs(title = "Control")
speak.to.nao <- likert(dat[34:35])
plot(speak.to.nao)

for (t in traits){
  print(t)
  colnum = which(colnames(control)==t)
  plot1 <- ggplot(control, aes(x=control[,colnum]))+geom_bar(fill="blue", alpha = 0.3) + scale_x_discrete(drop=FALSE)+labs(title=paste(t," Control")) +xlab("1= Definitely Not Associated")
  plot2 <- ggplot()+geom_bar(aes(x=curse[,colnum]), fill="red", alpha = 0.5)+ scale_x_discrete(drop=FALSE) + labs(title=paste(t," Curse")) + xlab("7= Definitely Associated")
  print(plot_grid(plot1, plot2, ncol=2))
}

colnum = which(colnames(control)=="Aggressive")
ggplot() + stat_count(aes(x=control[,colnum]), fill="blue", alpha = 0.2)+
  stat_count(aes(x=curse[,colnum]), fill="red", alpha = 0.2)+
  labs(title="Aggressive")


#overlapping histograms of relevant survey quantities
ggplot() + stat_count(aes(x=control$Aggressive), fill="blue", alpha = 0.2)+
  stat_count(aes(x=curse$Interactive), fill="red", alpha = 0.2)

########  STATISTICS: T-TEST AND ANOVA
dat <- read.csv("/Users/sarahwagner/Documents/RoboticsLab/data_analysis/data.csv")

#Clean unnecessary rows and columns
dat <- dat[, !(names(dat) == "Timestamp")]
dat <- dat[!(dat$Participant.ID == 123) & !(dat$Participant.ID == 139), ] #discard data point due to bad study
dat <- dat[!(dat$True.Condition == 1), ] #discard cheating points
dat <- na.omit(dat)

#remove string labels from numbers
dat <- data.frame(lapply(dat, function(x){
  gsub("1 - Never", "1", x)
}))
dat <- data.frame(lapply(dat, function(x){
  gsub("1 - Definitely Not Associated", "1", x)
}))
dat <- data.frame(lapply(dat, function(x){
  gsub("7 - All the Time", "7", x)
}))
dat <- data.frame(lapply(dat, function(x){
  gsub("7 - All the time", "7", x)
}))
dat <- data.frame(lapply(dat, function(x){
  gsub("7 - Definitely Associated", "7", x)
}))

#convert factors to numerics
for(i in names(dat)[9:35]){
  print(i)
  dat[[i]]<- as.numeric(levels(dat[[i]]))[dat[[i]]]
  dat[[i]]
}

#split into cheat, curse, and control
cheat <- dat[dat$True.Condition == 1, ]
curse <- dat[dat$True.Condition == 2, ]
control <- dat[dat$True.Condition == 3, ]

questions <- c("Question", "ANOVA p value", "ANOVA F value","Welch T-Test p value")

for(i in 15:35){
  print(names(dat)[i])
  #run anova
  cond <- aov(dat[,i] ~ True.Condition + dat$use.profanity + 
                dat$around.you.use.profanity + dat$Gender, data=dat)
  aov.pval <- summary(cond)[[1]][["Pr(>F)"]][1]
  print(aov.pval)
  aov.fval <- summary(cond)[[1]][["F value"]][1]
  
  #run t-test
  ttest= t.test(curse[,i], control[,i])
  print(ttest$p.value)
  
  questions <- rbind(questions, c(names(dat)[i], aov.pval, aov.fval, ttest$p.value))
}

#run t-test
for( i in 14:35){
  ttest= t.test(curse[,i], control[,i])
  print(names(dat)[i])
  print(ttest$p.value)
}

write.csv(questions, file = "all_p_values.csv")

bar_graph <- data.frame(Question=character(), Condition=character(), Mean=double(),SE=double())
names(bar_graph) <- c("Question", "condition", "mean", "SE")


#bar graph for likert
traits <- c("Interactive", "Awful", "Aggressive", "did.speak.to.Nao", "want.to.speak.to.Nao")

for(t in traits){
  i = which(colnames(control)==t)
  mean.curse <- mean(curse[,i])
  stand_dev.curse <- sd(curse[,i])
  mean.control <-mean(control[,i])
  stand_dev.control<- sd(control[,i])
  de <- rbind(c(t, "Control", mean.control, stand_dev.control),c(t, "Curse", mean.curse, stand_dev.curse))
  names(de) <- c("Question", "condition", "mean", "SE")
  bar_graph <- rbind(bar_graph,de)
}

names(bar_graph) <- c("Question", "condition", "mean", "se")
bar_graph$mean <- as.numeric(as.character(bar_graph$mean))
bar_graph$se <- as.numeric(as.character(bar_graph$se))

bar_graph$Question <- factor(bar_graph$Question)
ggplot(bar_graph, aes(x=Question, y=mean, fill=condition)) + 
  geom_bar(position=position_dodge(), stat="identity") +
  theme(axis.text.x = element_text(angle = 45, hjust = 1)) +
  geom_errorbar(aes(ymin=mean-se, ymax=mean+se),
                width=.2,                    # Width of the error bars
                position=position_dodge(.9))

write.csv(bar_graph, "bar_graph_data.csv")

 ##Laughing analysis

exp_cond1_on_with_group <- glm(dat$laughed ~ dat$True.Condition + dat$Gender + dat$use.profanity + 
                                 dat$around.you.use.profanity, data = dat, family = "binomial")
print(exp_cond1_on_with_group)
summary(exp_cond1_on_with_group)



