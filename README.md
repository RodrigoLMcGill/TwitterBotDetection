# TwitterBotDetection
Final Project of COMP-550 (NLP) - McGill University - Fall 2021
Team members:
- <rodrigo.lisboamirco@mail.mcgill.ca>, <260929545>
- <neshma.metri@mail.mcgill.ca>, <260847343>
- <madelaine.mareschal@mail.mcgill.ca>, <260716143>

# -- IMPORTANT -- 
The datasets present in this repository contain confidential information of real genuine Twitter accounts.
Their access was granted for educational purposes only and they should not be made public or shared.

The datasets present in this repository contain only a very small sample of the real datasets that we used.
The original preprocessed datasets had 1.03GB. The original raw datasets had 3.87GB.
We only gathered a small amount of each dataset in order to get the total size down to less than 100MB.

As expected, running our experiments on this much smaller dataset yields a very different result.
The scores present in the report are results from running the entire datasets.
Even with these smaller datasets, expect the model code to run for up to 3 minutes.
During our real experiments, the biggest datasets ran for up to 3 hours.

# WHERE ARE PLACED THE DATASETS
There are two types of datasets. The files with raw data as we got them and the preprocessed files after we ran the raw data in our preprocessor.py script.
- The raw sample datasets are placed in the DataPreprocessing/Input folder.
- The preprocessed sample datasets are placed in the Model/Datasets folder.

# HOW TO RUN
We coded two programs - a preprocessor that gets rid of information that is not useful for our task and the model itself.

- To run the preprocessors:
From the root of the repository, run: (you can choose between *pan19* or *cresci* as the argument)
    - python DataPreprocessing/preprocessor.py dataset

- To run the model:
From the root of the repository, run: (you can choose between *fake_followers_sample.csv*, *social_spambots_1_sample.csv*, *social_spambots_2_sample.csv*, *social_spambots_3_sample.csv*, *traditional_spambots_1_sample.csv* or *PAN19-Preprocessed_sample.csv*)
    - python Model/model.py filename.csv
