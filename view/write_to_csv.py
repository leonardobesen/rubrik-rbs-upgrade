import os
from datetime import datetime
import pandas as pd
import rubrik_cdm


def create_file(rubrik_conn: rubrik_cdm.Connect, REPORT_PATH: str, data: list[dict]):
    # Get now datetime info formatted
    now = datetime.now().strftime("%d-%m-%Y_%H_%M_%S")

    cluster = rubrik_conn.get('internal', '/cluster/me/name')

    # Set path and file information
    file_name = f'Rubrik_{cluster}_RBS_versions_{now}.xlsx'

    report_name = os.path.join(REPORT_PATH, file_name)

    df = pd.DataFrame(data)
    df.to_csv(report_name, encoding='utf-8', index=False)

    print(f"File saved on {report_name}")
