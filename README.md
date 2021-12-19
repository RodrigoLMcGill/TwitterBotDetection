# TwitterBotDetection
Final Project of COMP-550 (NLP) - McGill University - Fall 2021
Team members:
- <rodrigo.lisboamirco@mail.mcgill.ca>, <260929545>
- <neshma.metri@mail.mcgill.ca>, <260847343>
- <madelaine.mareschal@mail.mcgill.ca>, <260716143>

# -- IMPORTANT -- 
The datasets present in the submission zip file contain confidential information of real genuine Twitter accounts.
Their access was granted for educational purposes only and they should not be made public or shared.

The datasets present in the submission zip file are only a very small sample of the real datasets that we used.
The original preprocessed datasets had 1.03GB. The original raw datasets had 3.87GB.
We only gathered a small amount of each dataset in order to get the total size down to less than 100MB.

As expected, running our experiments on this much smaller dataset yields a very different result.
The scores present in the report are results from running the entire datasets.
Even with these smaller datasets, expect the model code to run for up to 3 minutes.
During our real experiments, the biggest datasets ran for up to 3 hours.

# -- WHERE TO PLACE THE DATASETS --
There are two zip files with datasets.
- The raw_sample_datasets.zip file must be unzipped and the 8 folders within it must be placed in the DataPreprocessing/Input folder.
- The preprocessed_sample_datasets.zip file must be unzipped and 7 csv files within it must be placed in the Model/Datasets folder.

# -- HOW TO RUN --
We coded two programs - a preprocessor that gets rid of information that is not useful for our task and the model itself.

- To run the preprocessors:
From the root of the repository, run: (choose between *pan19* or *cresci* as the argument)
    - python DataPreprocessing/preprocessor.py (pan19/cresci)

- To run the model:
From the root of the repository, run: (you can choose between *fake_followers_sample.csv*, *social_spambots_1_sample.csv*, *social_spambots_2_sample.csv*, *social_spambots_3_sample.csv*, *traditional_spambots_1_sample.csv* or *PAN19-Preprocessed_sample.csv*)
    - python Model/model.py filename.csv
