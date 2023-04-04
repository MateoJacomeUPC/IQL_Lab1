library(hash)

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

languages = c("ca", "es", "da", "en")
langs = hash()

for(j in 1:length(languages)){
  lang_file = paste("../out/", languages[j], ".txt", sep="")
  lang_info = hash()
  
  # Read freq tables
  lang_table = read.table(lang_file, header = FALSE)
  
  # Tau correlation test
  corr = cor.test(lang_table$V2, lang_table$V3, method="kendall")
  #cor(lang_table$V2, lang_table$V3, method="kendall")
  
  # Holm-Bonferroni correction
  #p.adjust(c(0.1,0.7), method="holm")
  
  # Mean word length
  l = mean_word_length(lang_table)
  print(l)
  
  # Random baseline
  rand_table = lang_table
  rand_table$V2 = sample(rand_table$V2)
  lr = mean_word_length(rand_table)
  print(lr)
  
  # Minimum baseline
  min_table = lang_table
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
  
  lang_info["p-value"] = corr$p.value
  lang_info["tau"] = corr$estimate
  lang_info["l"] = l
  lang_info["lr"] = lr
  lang_info["lmin"] = lmin
  lang_info["degree_opt"] = degree_opt
  lang_info["opt_score"] = opt_score
  
  langs[languages[j]] = lang_info
}



