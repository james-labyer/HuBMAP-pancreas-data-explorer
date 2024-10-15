import pandas as pd

df = pd.read_csv('assets/HuBMAP_ili_data10-11-24.csv')
df2 = pd.DataFrame(0,index=range(0,1440), columns=df.columns)

j = 0
for i in df.index:
    for k in range(8):
        # copy over old row
        df2.iloc[j] = df.iloc[i]
        # update values
        df2.loc[j, 'Block ID'] = df.loc[i, 'Block ID'] + (k * .1)
        if k % 2 == 0:
            df2.loc[j, 'X Center'] = df.loc[i, 'X Center'] - 25
        else:
            df2.loc[j, 'X Center'] = df.loc[i, 'X Center'] + 24.999
        if k in [0, 1, 4, 5]:
            df2.loc[j, 'Y Center'] = df.loc[i, 'Y Center'] - 26.5
        else:
            df2.loc[j, 'Y Center'] = df.loc[i, 'Y Center'] + 26.499
        if k in [0, 1, 2, 3]:
            df2.loc[j, 'Z Center'] = df.loc[i, 'Z Center'] - 17.5
        else:
            df2.loc[j, 'Z Center'] = df.loc[i, 'Z Center'] + 17.499
        j += 1

df2.to_csv('assets/rectangles_output.csv')