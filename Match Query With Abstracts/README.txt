The query documents should be named as cran.qry and the abstracts should be named as cran.all.1400
Both of the files should be under the same directory as the ad_hoc_ir.py file.
To run the system, simply use
python ad_hoc_ir.py
The output file is named output.txt
I use the framing that all documents and queries have features with the same length,
and they represent the same set of words. I choose all the words that has shown in either the query
or the abstract, or both.
In order to get a better MAP score, I truncated the similarity scores to leave only 100 highest abstracts.
As for the term frequency, I tried the to use the logarithm and just the count.
It turns out that the logarithm got the better MAP score. I use add one smoothing to avoid log(0) situations.
For tokenization, I use python split() function.