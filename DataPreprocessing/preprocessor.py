import os
import xml.etree.ElementTree as ET

class PAN19Preprocessor:

    def preprocess(self):
        # We get a list of account ids that match the name of a XML file with all tweets

        # We may have multiple pan19-author-profiling folders
        with open("./DataPreprocessing/Output/PAN19-Preprocessed.csv", "w", encoding="utf-8") as preprocessed_file:
            list_subfolders_with_paths = [f.path + "/en/" for f in os.scandir("./DataPreprocessing/Input") if f.is_dir() and f.name.startswith("pan19-author-profiling")]
            for folder_path in list_subfolders_with_paths:
                truth_table = []
                with open(folder_path + "truth.txt") as truth_file:
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
                    

if __name__ == "__main__":
    pan19Preprocessor = PAN19Preprocessor()
    pan19Preprocessor.preprocess()