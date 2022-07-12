library(tidyverse)
library(effsize)

CDM <- read_csv('~/Documents/VM Shared/homeostasis/intervention.log', col_names=FALSE) %>% tail(25)
random <- read_csv('~/Documents/VM Shared/homeostasis/control.log', col_names=FALSE) %>% tail(25)

colnames(CDM)<-c('data')
colnames(random)<-c('data')
df <- tibble()
branch <- rep('CDM', length(CDM$data))
branch2 <- rep('Control', length(random$data))
df <- tibble(branch = branch, val=CDM$data/6e10)
df2<- tibble(branch = branch2, val=random$data/6e10)
df <- rbind(df2,df)

CDM %>%  mutate(val = data / 6e10) %>% select(val) -> CDM2
random %>% mutate(val = data / 6e10) %>% select(val) -> random2
# k <- ks.test(CDM2$val, random2$val)
# k$p.value
u <- wilcox.test(CDM2$val, random2$val)
pval = u$p.value

a <- VD.A(CDM2$val, random2$val)
aval = a$estimate
a$magnitude

df %>% #filter(val < 750) %>% 
  mutate(branch = as_factor(branch)) %>% 
  ggplot(aes(x = branch, y = val, group=branch)) + 
   # geom_violin() 
  geom_boxplot() + 
  geom_jitter(alpha=0.6, size=0.4, width=0.1) +
  theme_bw() + 
  theme_classic() +
  labs(x = '', y = 'Survival time (mins*)', title='Simulated Homeostasis Experiment', subtitle = paste0('(p=', round(pval, 3),  ', A=', round(aval, 2), ')')) +
  theme(text = element_text(size=20)) +
  theme(plot.title = element_text(size=18,hjust = 0.5), plot.subtitle = element_text(size=18,hjust=0.5)) 
  
  
  
 


CDM <- read_csv('~/Documents/VM Shared/conflict/intervention.log', col_names = FALSE)
random <- read_csv('~/Documents/VM Shared/conflict/control.log', col_names=FALSE)

colnames(CDM)<-c('data')
colnames(random)<-c('data')
df <- tibble()
branch <- rep('CDM', length(CDM$data))
branch2 <- rep('Control', length(random$data))
df <- tibble(branch = branch, val=CDM$data/6e10)
df2<- tibble(branch = branch2, val=random$data/6e10)
df <- rbind(df2,df)


CDM %>%  mutate(val = data / 6e10) %>% select(val) -> CDM2
random %>% mutate(val = data / 6e10) %>% select(val) -> random2
# k <- ks.test(CDM2$val, random2$val)
# k$p.value
u <- wilcox.test(CDM2$val, random2$val)
pval = u$p.value

a <- VD.A(CDM2$val, random2$val)
aval = a$estimate
a$magnitude

df %>% #filter(val < 750) %>% 
  mutate(branch = as_factor(branch)) %>% 
  ggplot(aes(x = branch, y = val, group=branch)) + 
  # geom_violin() 
  geom_boxplot() + 
  geom_jitter(alpha=0.6, size=0.4, width=0.1) +
  theme_bw() + 
  theme_classic() +
  labs(x = '', y = 'Survival time (mins*)', title='Simulated Conflict Experiment', subtitle = paste0('(p=', round(pval, 3),  ', A=', round(aval, 2), ')')) +
  theme(text = element_text(size=20)) +
  theme(plot.title = element_text(size=18,hjust = 0.5), plot.subtitle = element_text(size=18,hjust=0.5)) 
  

