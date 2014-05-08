# R Code
# Preprocessing
# L.P.F. Garcia, D. Santos, R.G. Mantovani, A.C.P.L.F. Carvalho, 2014
# Remove constant attributes and format the header


require(foreign);


preprocessing = function(file) {

	# read the file
	data = read.arff(file);
	print(file);

	# remove constant attributes
	for(i in colnames(data)) {	

		# categorical attributes
		if(is.factor(data[,i])) {
			if(nlevels(data[,i]) == 1) {
				data[,i] = NULL;
			}
		# numeric attributes	
		} else {
			if(sd(data[,i]) == 0) {
				data[,i] = NULL;
			# z-score	
			} else {
				data[,i] = (data[,i] - mean(data[,i]))/sd(data[,i]);
			}
		}
	}

	# remove duplicated examples
	aux = which(duplicated(data));
	data = data[-aux,];

	# format the header
	colnames(data) = c(paste("V", rep(1:(ncol(data)-1)), sep=""), "Class");
	data$Class = factor(data$Class);
	rownames(data) = NULL;

	# save the arff file
	write.arff(data, file);
}

# execute the script
setwd("~/ucipp/uci/");
files = list.files();
for(file in files)
	preprocessing(file);

