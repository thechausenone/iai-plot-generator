import matplotlib.pyplot as plt
from argparse import ArgumentParser
import pandas as pd
import numpy as np


def generate_plot(feature_name):
    df = pd.read_csv('/Users/dchau/Documents/ai-bias/propensity_plots/data/kanetix-fairness-bias.csv')

    # plot 1: binary setup
    feature_df = df.pivot(columns=feature_name, values='pr_sold')

    # plot 1: conditional setup for age
    # temp = df[[feature_name, 'pr_sold']]
    # feature_df = pd.DataFrame()
    # feature_df['gte25'] = np.where(temp[feature_name] >= 25, temp['pr_sold'], float('NaN'))
    # feature_df['lt25'] = np.where(temp[feature_name] < 25, temp['pr_sold'], float('NaN'))

    # # plot 2: binary setup
    # temp = df.where(df['status'] == 'experimental')
    # temp = temp[pd.notnull(temp[feature_name])]
    # feature_df = temp.pivot(columns=feature_name, values='pr_sold')
    # feature_df.columns = [False, True] if np.array_equal(feature_df.columns.values, [0, 1]) else feature_df.columns

    # # plot 2: conditional setup for age
    # temp = df.where(df['status'] == 'experimental')
    # temp = temp[pd.notnull(temp[feature_name])]
    # temp = temp[[feature_name, 'pr_sold']]
    # feature_df = pd.DataFrame()
    # feature_df['gte25'] = np.where(temp[feature_name] >= 25, temp['pr_sold'], np.nan)
    # feature_df['lt25'] = np.where(temp[feature_name] < 25, temp['pr_sold'], np.nan)

    # debug
    print(feature_df)

    # create the plots
    __create_and_save_histograms(feature_df, feature_name)


# redefine file path and folders!
def __create_and_save_histograms(feature_df, feature_name):
    # plot multiple
    for column in feature_df:
        plt.figure()
        plt.hist(feature_df[column], alpha=0.5, density=True)
        plt.xlabel("Propensity")
        plt.ylabel("Frequency")
        plt.xticks([i / 10 for i in range(0, 11)])
        plt.xlim(left=0, right=1)
        plt.title('Propensity Distribution for {}, {}'.format(feature_name, column))
        plt.savefig('/Users/dchau/Documents/ai-bias/propensity_plots/data/all/{}_{}.png'.format(feature_name, column))

    # plot aggregate
    plt.figure()
    feature_df.plot.hist(bins=100, alpha=0.5, stacked=True)
    plt.xlabel("Propensity")
    plt.ylabel("Frequency")
    plt.xticks([i / 10 for i in range(0, 11)])
    plt.xlim(left=0, right=1)
    plt.title('Propensity Distribution for {}'.format(feature_name))
    # plt.savefig('/Users/dchau/Documents/ai-bias/propensity_plots/data/all/{}_aggregate.png'.format(feature_name))


def __get_options():
    parser = ArgumentParser()
    parser.add_argument("--feature", action="store", required=True,
                        help="specify name of the feature containing your groupings",
                        dest="feature", type=str)

    args = parser.parse_args()
    feature = args.feature

    return {
        "feature": feature
    }


def main():
    options = __get_options()
    generate_plot(options.get('feature'))


if __name__ == "__main__":
    main()
