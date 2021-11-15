import os
import sys
import csv
import xml.etree.ElementTree as ET

class PAN19Preprocessor:

    def preprocess(self):

        with open("./DataPreprocessing/Output/PAN19-Preprocessed.csv", "w", encoding="utf-8") as preprocessed_file:
            # We may have multiple pan19-author-profiling folders
            list_subfolders_with_paths = [f.path + "/en/" for f in os.scandir("./DataPreprocessing/Input") if f.is_dir() and f.name.startswith("pan19-author-profiling")]
            for folder_path in list_subfolders_with_paths:
                truth_table = []
                with open(folder_path + "truth.txt") as truth_file:
                    # We get a list of account ids that match the name of a XML file with all tweets of this account
                    for line in truth_file.readlines():
                        line_split = line.split(":::")
                        # [0] -> ID [1] -> either bot or human. We treat bot as 1, human as 0
                        truth_table.append((line_split[0], 1 if line_split[1] == "bot" else 0 ))
                for account in truth_table:
                    tree = ET.parse(folder_path + account[0] + ".xml")
                    root = tree.getroot()
                    concatenated_tweets = "\""
                    for document in root[0]:
                        tweet = document.text.replace("\"", "'")
                        concatenated_tweets += " " + tweet # Concatenating with a space, maybe something different?
                    concatenated_tweets += "\""
                    preprocessed_file.write(account[0] + "," + str(account[1]) + "," + concatenated_tweets + "\n")               


class CresciPreprocessor:

    def fix_nulls(self, file):
        for line in file:
            yield line.replace('\0', '')

    def preprocess(self):        
        with open("./DataPreprocessing/Output/Cresci-Preprocessed.csv", "w", encoding="utf-8") as preprocessed_file:
            # Assume every folder that is not from pan19 is from Cresci et al.
            list_subfolders_with_paths = [f.path + "/" for f in os.scandir("./DataPreprocessing/Input") if f.is_dir() and not f.name.startswith("pan19-author-profiling")]
            for folder_path in list_subfolders_with_paths:
                is_bot = 0 if "genuine_accounts" in folder_path else 1
                tweets_by_account_dict = {}
                with open(folder_path + "tweets.csv", "r", encoding='utf-8', errors='ignore') as tweets_file:
                    reader = csv.reader(self.fix_nulls(tweets_file), delimiter=',')
                    next(reader, None) # skip headers
                    for line in reader:
                        tweet = line[1].replace("\"", "'")
                        if line[3] in tweets_by_account_dict:
                            tweets_by_account_dict[line[3]] += ' ' + tweet
                        else:
                            tweets_by_account_dict[line[3]] = "\"" + tweet
                for account_id, concatenated_tweets in tweets_by_account_dict.items():
                    concatenated_tweets += "\""
                    preprocessed_file.write(str(account_id) + "," + str(is_bot) + "," + concatenated_tweets + "\n")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Please enter argument on which dataset you wish to preprocess (python preprocessor.py pan19/cresci)")
        quit()
    dataset = sys.argv[1]
    preprocessor = None
    if dataset == 'pan19':
        preprocessor = PAN19Preprocessor()
    elif dataset == 'cresci':
        preprocessor = CresciPreprocessor()
    else:
        print("Available dataset options are pan19 and cresci")
        quit()
                
    preprocessor.preprocess()
