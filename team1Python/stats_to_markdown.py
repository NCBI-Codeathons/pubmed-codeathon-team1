# this reads in data/statistics.csv sorts it and dumps out a chunk of markdown

from pathlib import Path
import pandas as pd

#pd.options.display.float_format = '{:.2f}'.format
pd.set_option('display.float_format', '{:.2f}'.format)

def main():
    # Load the dataset
    load_dest = Path("./data/")
    f_save = load_dest / "statistics.csv"

    df = pd.read_csv(f_save)
    df['Direction'] = ''
    df = df.sort_values(['feature','comparison'])
    df['feature'] = df['feature'].str.strip()
    df['feature'] = df.apply(lambda row : '**'+row['feature']+'**' if (row['p_value']<=0.01 and row['power']>0.3) else row['feature'], axis=1)
    df['feature'] = df.apply(lambda row : '_'+row['feature']+'_' if (row['p_value']<=0.01 and row['power']<0.3) else row['feature'], axis=1)
    df['Direction'] = df.apply(lambda row: what_direction(row['comparison'],row['t_score']), axis=1)
    df['p_value'] = df['p_value'].round(2)
    df['power'] = df['power'].round(2)
    df['p_value'] = df.apply(lambda row: '{:.2f}'.format(float(row['p_value'])), axis=1)
    df['p_value'] = df.apply(lambda row: '<0.01' if float(row['p_value'])<0.01 else row['p_value'], axis=1)
    df = df[['feature','comparison','p_value','power','Direction']]
    df.columns = ['Feature', 'Comparison', 'p-value', 'Power','Direction']
    print(df.to_markdown(index=False, floatfmt='.2f'))
    df.to_markdown(buf=Path("./data/out/statistics.md"), index=False, floatfmt='.2f', colalign=('left','left','right','right','left'))
    print(df.dtypes)
    
def what_direction(comparison,t_score):
    direction = ''
    # If t_score is < 0 then report in a new column Date if t_score > 0 report Best Match. If the query is on page,
    #  the t_score >0 report Page 1, for t_score <0 report Page 2 (edited) 
    if comparison.count('Page 1')==1 and comparison.count('Page 2') == 1:
        if t_score > 0:
            direction = 'Page 1'
        elif t_score < 0:
            direction = 'Page 2'
    else:
        if t_score > 0:
            direction = 'Best Match'
        elif t_score < 0:
            direction = 'Date'
    return direction

if __name__ == '__main__':
    main()