library(ggplot2)

setwd('/home/lea/Dropbox/MSc Bioinformatik/Bioimage Analysis and Phenotyping/Project')
data = read.csv('Plan.csv', header = TRUE, sep = ",")
part = data[,c(3,21)]


leafs = c(1,2,3,4)
leaf_means = c()
leaf_sd = c()

for(l in leafs){
  leaf_rows = which(data$number_of_leafs == l)
  leaf_means[l] = mean(data[leaf_rows,"percent_of_day0"])
  leaf_sd[l] = sd(data[leaf_rows,"percent_of_day0"])
}


plot(part, main='main', xlab='Number of leafs on day 0',ylab='Percentage of leaf size')
#lines(leaf_means+leaf_sd, pch=18, col="blue", type="b", lty=2)
#lines(leaf_means, type="b", pch=19, col="darkgreen", xlab="x", ylab="y")
#lines(leaf_means-leaf_sd, pch=18, col="blue", type="b", lty=2)
points(leaf_means+leaf_sd, pch=18, col='blue')
points(leaf_means, pch=15, col='darkgreen')
points(leaf_means-leaf_sd, pch=18, col='blue')
legend(1, 20, legend=c("mean", "standard deviation"), col=c("darkgreen", "blue"), cex=0.8)





# Compare leaf sizes
part = data[,c(3,21)]
size_comparison = ggplot(part, aes(x=as.factor(number_of_leafs), y=percent_of_day0)) + 
  geom_boxplot(fill="slateblue", alpha=0.2) + 
  theme_minimal() +
  xlab("Number of leafs") +
  ylab('Percentage of difference in leaf surface area') + 
  ggtitle('Results of leaf size comparison') +
  scale_y_continuous(labels = scales::percent_format(accuracy = 1)) +
  theme(plot.title = element_text(hjust = 0.5))
size_comparison
ggsave("Leafsize_comparison.png", plot = size_comparison, device = "png", dpi = 600) 


# Size day 0
part = data[,c(3,6)]
size_day0 = ggplot(part, aes(x=as.factor(number_of_leafs), y=surface_area_0_cm2)) + 
  geom_boxplot(fill="slateblue", alpha=0.2) + 
  theme_minimal() +
  xlab("Number of leafs") +
  ylab('Totla leaf size in cm²') + 
  ggtitle('Leaf surface area on day 0') +
  theme(plot.title = element_text(hjust = 0.5))
size_day0
ggsave("Leafsize_day0.png", plot = size_day0, device = "png", dpi = 600) 

# Size day 0
part = data[,c(3,20)]
size_day74 = ggplot(part, aes(x=as.factor(number_of_leafs), y=final_surface_area_cm2)) + 
  geom_boxplot(fill="slateblue", alpha=0.2) + 
  theme_minimal() +
  xlab("Number of leafs") +
  ylab('Total leaf size in cm²') + 
  ggtitle('Leaf surface area on day 74') +
  theme(plot.title = element_text(hjust = 0.5))
size_day74
ggsave("Leafsize_day74.png", plot = size_day74, device = "png", dpi = 600) 
