import pandas as pd
import matplotlib.pyplot as plt

# Helper functions for analysis

def groupByColumn(df,column_name):
    grouped_df = df.groupby(column_name, observed=True)
    return grouped_df



def plot_ticker(ax, df, ticker, color=None):
    data = df[df['ticker'] == ticker]
    ax.plot(data['date'], data['close'], label=ticker, color=color)
    ax.set_title(ticker, fontsize=12, weight='bold')
    ax.tick_params(axis='x', labelrotation=45)
    ax.grid(True, linestyle='--', alpha=0.4)
    ax.legend(loc='best', fontsize=8)

def removeNSE(df):
    return (
        df.loc[df['ticker'] != 'NSEBANK']
          .assign(ticker=lambda x: x['ticker'].str.replace('.NS', '', regex=False))
          .copy()
    )

def rotateXLabels(ax, angle=45):
    ax.tick_params(axis='x', labelrotation=angle)

def graphTuning(ax, title, xlabel, ylabel, grid=False):
    ax.set_title(title, fontsize=14, weight='bold', color='white')
    ax.set_xlabel(xlabel, fontsize=12, color='white')
    ax.set_ylabel(ylabel, fontsize=12, color='white')
    ax.tick_params(colors='white')
    if grid:
        ax.grid(True, linestyle='--', alpha=0.4)
    else:
        ax.grid(False)
    ax.set_facecolor('black')
    for spine in ax.spines.values():
        spine.set_color('white')



