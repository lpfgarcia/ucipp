# R Code
# Preprocessing
# L.P.F. Garcia, D. Santos, R.G. Mantovani, A.C.P.L.F. Carvalho, 2014
# Remove constant attributes and format the header


require(foreign);


preprocessing = function(file) {

	print(file);
	data = read.arff(file);

	for(i in colnames(data)) {	

		if(is.factor(data[,i])) {
			if(nlevels(data[,i]) == 1) {
				data[,i] = NULL;
			}
		} else {
			if(sd(data[,i]) == 0) {
				data[,i] = NULL;
			}
		}

	}

	colnames(data) = c(paste("V", rep(1:(ncol(data)-1)), sep=""), "Class");
	data$Class = factor(data$Class);
	rownames(data) = NULL;

	write.arff(data, file);
}


files = list.files("../uci/", full.names=TRUE);
for(file in files)
	preprocessing(file);

