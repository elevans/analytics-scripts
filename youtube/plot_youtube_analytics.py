import argparse
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

def load_csv(path: str) -> pd.DataFrame:
    """Load data from a CSV file into a pandas dataframe.
    """
    return pd.read_csv(path, sep=",")


def filter_dataframe(data: pd.DataFrame, monthly: bool=False) -> pd.DataFrame:
    """Filter and re-format the YouTube pandas dataframe.
    """
    # remove zero view entries
    data = data[data['Views'] != 0]

    # squash date and view counts into one entry
    data.loc[:, 'Date'] = pd.to_datetime(data['Date'])
    data = data.groupby(['Date', 'Channel'])['Views'].sum().reset_index()

    # store channel name and reset 'Channel' column
    ch = data['Channel'][0]
    if monthly:
        # resample the data to be monthly
        data.set_index('Date', inplace=True)
        data_monthly = data.resample('ME').sum()
        data_monthly.reset_index(inplace=True)
        data_monthly['Channel'] = ch
        return data_monthly
    else:
        return data


def lineplot(data: pd.DataFrame, x: str="Date", y: str="Views"):
    """Plot a lineplot of the given data.
    """
    return sns.lineplot(data=data,
                        x=x,
                        y=y,
                        markers=True,
                        dashes=False,
                        hue="Channel",
                        style="Channel")


# set up argparse
parser = argparse.ArgumentParser(description="Plot YouTube analytics")
parser.add_argument("-i", "--input", required=True, help="Path to YouTube analytics CSV file.")
pargs = parser.parse_args()

# set up plot style
sns.set_style("darkgrid")

# plot the data
df = load_csv(pargs.input)
df = filter_dataframe(df)
g = lineplot(df)
plt.show()
