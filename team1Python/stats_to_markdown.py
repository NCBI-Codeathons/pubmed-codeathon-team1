# this reads in data/statistics.csv sorts it and dumps out a chunk of markdown

from pathlib import Path
import pandas as pd

def main():
    print('hello')
    # Load the dataset
    load_dest = Path("./data/")
    f_save = load_dest / "statistics.csv"

    df = pd.read_csv(f_save)
    df.drop(['t_score', 'cohens_d'], axis=1, inplace=True)
    df = df.sort_values(['feature','comparison'])
    df['feature'] = df['feature'].str.strip()
    df['feature'] = df.apply(lambda row : '**'+row['feature']+'**' if (row['p_value']<=0.01 and row['power']>0.3) else row['feature'], axis=1)
    df['feature'] = df.apply(lambda row : '_'+row['feature']+'_' if (row['p_value']<=0.01 and row['power']<0.3) else row['feature'], axis=1)
    print(df.to_markdown(index=False))
    df.to_markdown(buf=Path("./data/out/statistics.md"), index=False)

if __name__ == '__main__':
    main()