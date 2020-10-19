# Enron Emails
Repository looking into the enron emails to practice some big data techniques with Spark. 

## Environment Prep

### Anaconda
have anaconda installed with python version 3.7+ 

install dependencies and create a new venv with:
```
conda env create -f spark_enron_email.yml
```

### PySpark
Have pySpark and spark running natively in conda environment
here is one example tutorial I found helpful:
https://www.tutorialspoint.com/pyspark/pyspark_environment_setup.htm


## Extraction
+
download data from https://www.cs.cmu.edu/~./enron/ and place in /data/ folder

This app solves the problem by looping iteratively through each folder and uses the built in python email parser to load objects at a record level. These records are loaded into a pandas dataframe and then exported as a CSV per person as an interim export step compatible with apache spark. If the data was coming from an API or DB it would be merged using incremental sync based on the email id value. Initially I felt it best to load all the data from all the folders so make sure nothing was inadvertantly filtered out initially. 


edit line 7 of 'extract.py' to match the extracted location
```
path = Path("C:\workspace\Spark_EnronEmail\data\maildir")
```

then run this command to launch the app

```
python extract.py
```

a CSV containing all the email data person  will output to "./export" folder

## Analysis
This application uses apache spark and the python ( pyspark ) API to do some crunching of the data. Spark is able to use distribution file systems to efficently load teh data and perform the queries we need even with 1.5 millon rows of initial data. 

a 'valid' email is defined as one with a matching "XXX.AAA.Javamail.XX" pattern. An email could show up in multiple inboxes as well as the sent account of a user so this Id is used to determine uniqueness. 

run the following command to launch spark and run the analysis job
```
python transform.py
```

answers are output to sub folder or command window. 

