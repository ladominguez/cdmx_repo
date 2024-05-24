import pandas as pd

names = ['No', 'Date', 'Time', 'latitude', 'longitude', 'Depth', 'Mag', 'CC', 'MAD', 'Reference']
dtypes = {'No': int, 'Date': str, 'Time': str, 'latitude': float, 'longitude': float, 'Depth': float, 'Mag': float,
          'CC': float, 'MAD': float, 'Reference': str}

def load_TM_catalog(filename, exclude_templates=True, MAD_min=9.0):
    catalog =  pd.read_csv(filename, sep='\s+', header = 0, names=names, dtype=dtypes)
    catalog = catalog[catalog['MAD'] >= MAD_min]
    catalog['Date'] = catalog['Date'].str.cat(catalog['Time'], sep=' ')
    catalog['Date'] = pd.to_datetime(catalog['Date'], format='%Y/%m/%d %H:%M:%S.%f')
    catalog = catalog.drop(columns=['Time'])
    if exclude_templates:
        catalog, no_templates = _exclude_templates(catalog)
    else:
        no_templates = 0
    return catalog, no_templates

def _exclude_templates(catalog):
    k = 0
    for index, row in catalog.iterrows():
        detection_id = row['Date'].strftime('%Y%m%d%H%M%S')
        template_id = row['Reference'].split('.')[0]
        if detection_id == template_id:
            catalog.drop(index, inplace=True)
            k += 1
    return catalog, k

