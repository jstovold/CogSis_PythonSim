library(tidyverse)
CDM <- read_csv('~/Documents/VM Shared/intervention.log')
random <- read_csv('~/Documents/VM Shared/control.log')

df <- tibble()
branch <- rep('CDM', 15)
branch2 <- rep('Control', 15)
df <- tibble(branch = branch, val=CDM$`124846263045`/6e10)
df2<- tibble(branch = branch2, val=random$`54340925058`/6e10)
df <- rbind(df,df2)

df %>% ggplot(aes(x = branch, y = val, group=branch)) + 
  geom_violin() 
  # geom_boxplot(width=0.1)
