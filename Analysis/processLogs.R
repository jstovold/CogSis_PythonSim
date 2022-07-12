library(tidyverse)
library(effsize)

CDM <- read_csv('~/Documents/VM Shared/intervention.log', col_names=FALSE)
random <- read_csv('~/Documents/VM Shared/control.log', col_names=FALSE)


CDM <- read_csv('~/Documents/VM Shared/conflict/intervention.log', col_names = FALSE)
random <- read_csv('~/Documents/VM Shared/conflict/control.log', col_names=FALSE)
colnames(CDM)<-c('data')
colnames(random)<-c('data')
df <- tibble()
branch <- rep('CDM', length(CDM$data))
branch2 <- rep('Control', length(random$data))
df <- tibble(branch = branch, val=CDM$data/6e10)
df2<- tibble(branch = branch2, val=random$data/6e10)
df <- rbind(df,df2)

df %>% #filter(val < 750) %>% 
  ggplot(aes(x = branch, y = val, group=branch)) + 
   # geom_violin() 
  geom_boxplot() + 
  geom_jitter(alpha=0.6, size=0.4, width=0.1)
 
CDM %>%  mutate(val = data / 6e10) %>% select(val) -> CDM2
random %>% mutate(val = data / 6e10) %>% select(val) -> random2
k <- ks.test(CDM2$val, random2$val)
k$p.value
u <- wilcox.test(CDM2$val, random2$val)
u$p.value

a <- VD.A(CDM2$val, random2$val)
a$magnitude
a$estimate



