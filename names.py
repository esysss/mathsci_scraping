import pandas

def fixingNames(df):

    for i,names in enumerate(df['Name']):
        found = True
        for na in range(1,len(names)):
            if names[na] != ' ' and found:
                for j in range(na,len(names)):
                    if names[j] == '\n':
                        df.at[i,'Name'] = names[na:j]
                        found = False

    return df