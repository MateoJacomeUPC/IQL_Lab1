# Read freq tables
test = read.table("../out/ca.txt", header = FALSE)
test

# Tau correlation test
cor.test(test$V2, test$V3, method="kendall")
#cor(test$V2, test$V3, method="kendall")

# Holm-Bonferroni correction
#p.adjust(c(0.1,0.7), method="holm")

mean_word_length <- function(freq_table){
  # Obtain relative frequency
  sum_freq = sum(freq_table$V3)
  rel_freq = freq_table$V3/sum_freq
  # Summation of relative freq by word length
  mean_len = 0
  for(i in 1:nrow(freq_table)){
    mean_len = mean_len + rel_freq[i]*freq_table$V2[i]
  }
  return(mean_len)
}

# Mean word length
l = mean_word_length(test)
print(l)


# Random baseline
rand_table = test
rand_table$V2 = sample(rand_table$V2)
lr = mean_word_length(rand_table)
print(lr)


# Minimum baseline
min_table = test
min_table$V2 = sort(min_table$V2, decreasing=FALSE)
min_table$V3 = sort(min_table$V3, decreasing=TRUE)
lmin = mean_word_length(min_table)
print(lmin)


# Degree of optimality
degree_opt = lmin/l
print(degree_opt)

# Optimality score
opt_score = (lr-l)/(lr-lmin)
print(opt_score)
