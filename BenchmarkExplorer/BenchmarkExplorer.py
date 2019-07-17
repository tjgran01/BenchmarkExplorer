import sys
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from statistics import mean

class BenchmarkExplorer():
    def __init__(self, data_fname=None, data_fnames=[],
                 data_dir="../SampleData/"):
        self.data_dir = data_dir
        self.data_file = self.determine_data_file_schema(data_fname, data_fnames,
                                                         data_dir)
        self.performance_dict = self.generate_performance_scores(Reaction_Time=True)
        self.plot_performance_by_task()

    # def __repr__(self):
    #     return self.data_fname

# -------------------------------------------- File Reading --------------------

    def determine_data_file_schema(self, data_fname, data_fnames, data_dir):

        if not data_fname:
            if not data_fnames:
                print("No file to operate over.")
                sys.exit()
            else:
                self.data_fname = data_fname
                self.data_fnames = data_fnames
                self.using_type = "multiple"
        else:
            self.data_fname = data_fname
            self.data_fnames = data_fnames
            self.using_type = "single"

        if self.using_type == "single":
            return self.read_data_file()
        else:
            self.data_file = self.append_files_to_single()
            if not self.data_file:
                print("No data file could be created.")
                sys.exit()


    def read_data_file(self):
        """Read a single data file using self.data_fname attribute and return
        DataFrame of file.
        Args:
            self.data_fname(str): The PATH to the data file.
        Return:
            self.data_file(pd.DataFrame): The DataFrame of the data file.
        """
        return pd.read_csv(f"{self.data_dir}{self.data_fname}")


    def append_files_to_single(self):
        """Take a list of data file names, read the files, and append the
        contents of each file together into one large file.
        Args:
            self.data_fnames(list[str]): The PATHs to the data files.
        Return:
            self.data_file(pd.DataFrame): The DataFrame of the data file.
        """
        return

# -------------------------------------------- Scoring Performance -------------


    def generate_performance_scores(self, Reaction_Time=False):
        """Returns a dictionary of performance scores with ID_Session # as
        keys.
        Args:
            self.data_file(pd.DataFrame): The DataFrame of the data file.
        Return:
            performance_dict(dict): A dictionary of performance values in file.
        """


        performance_dict = {}

        by_block_split = self.data_file.groupby(["subject_id", "session_number",
                                                "task", "block"])
        for i, block in enumerate(by_block_split):
            # Calc Performance
            dict_key = "_".join(str(i) for i in block[0])
            performance_col = block[1]["Performance"].tolist()
            total = len(performance_col)
            correct_amt = len([ans for ans in performance_col if ans == "Correct"])
            perf = correct_amt / total
            performance_dict[f"{dict_key}"] = {"Performance": 0, "Reaction_Time": 0}
            performance_dict[f"{dict_key}"]["Performance"] = perf
            # Calc Avg Rt.
            rt_col = block[1]["Reaction_Time"].tolist()
            rt_vals = [val for val in rt_col if val not in [-1, 0, 1]]
            performance_dict[f"{dict_key}"]["Reaction_Time"] = mean(rt_vals)

        return performance_dict


# -------------------------------------------- Df manips -----------------------




# ------------------------------------------- Plotting Performance -------------

    def plot_performance_by_task(self):

        sns.set(style="darkgrid")

        df = pd.DataFrame(self.performance_dict)
        df = df.transpose()
        print(df)

        regplot = sns.jointplot("Reaction_Time", "Performance", data=df, kind="reg")
        plt.show()








be = BenchmarkExplorer(data_fname="arm1_performance.csv")
