import csv
import pandas as pd
import datetime

def upload_csv(mysql, csv_filename, table_name, date_columns=[]):
    conn = mysql.connection
    cursor = conn.cursor()
    try:
        df = pd.read_csv(csv_filename)
        columns_list = df.columns.tolist()

        for index, row in df.iterrows():
            formatted_values = []

            for column in columns_list:
                value = row[column]

                if column in date_columns:
                    formatted_time = datetime.datetime.strptime(value, '%m/%d/%Y').strftime('%Y-%m-%d')
                    formatted_values.append(formatted_time)
                else:
                    formatted_values.append(value)

            placeholders = ', '.join('%s' for _ in columns_list)
            query = f"INSERT INTO {table_name} ({', '.join(columns_list)}) VALUES ({placeholders})"
            cursor.execute(query, tuple(formatted_values))

        conn.commit()
        print("CSV uploaded successfully!")
    except Exception as e:
        conn.rollback()
        print("Error uploading CSV:", e)

    # Close the cursor
    cursor.close()

