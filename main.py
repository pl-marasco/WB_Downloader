import os
import requests
import pandas as pd
from tqdm import tqdm


def downloader():

    user = ''
    psw = ''

    folder = 'D:/Data/WB/1K'

    url = 'https://land.copernicus.vgt.vito.be/PDF/datapool/Water/Water_Bodies/WB_Africa_V1/'

    session = requests.Session()
    session.auth = (user, psw)

    manifest = session.get(url, allow_redirects=True)

    yrs = pd.read_html(manifest.text)[2][1:]['Year']

    for yr in yrs:
        for month in range(1, 13):
            for day in iter([1, 11, 21]):
                if (int(yr) == 1998 and int(month) < 4) or (int(yr) == 1998 and int(month) == 4 and day == 1):
                    continue

                try:
                    day = str(day).zfill(2)
                    month = str(month).zfill(2)

                    product = f'WB_{yr}{month}{day}0000_AFRI_VGT_V1.4'
                    file = f'g2_BIOPAR_WB_{yr}{month}{day}0000_AFRI_VGT_V1.4.zip'
                    addendum = f'{yr}/{month}/{day}/{product}/{file}'
                    url_f = f'{url}{addendum}'

                    r = session.get(url_f, stream=True)

                    total_size = int(r.headers.get('content-length', 0))
                    block_size = 1024  # 1 Kibibyte
                    t = tqdm(total=total_size, unit='iB', unit_scale=True)
                    out_file = os.path.join(folder, file)
                    with open(out_file, 'wb') as f:
                        for data in r.iter_content(block_size):
                            t.update(len(data))
                            f.write(data)
                    t.close()

                    if total_size != 0 and t.n != total_size:
                        raise IOError

                except Exception as e:
                    print(f'ERROR, something went wrong {e}')
                    continue
    print('Done')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    downloader()
