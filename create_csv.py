import pandas as pd

def create_csv(tweets):
    # Data to be written to the CSV file
    data = {
        'text': tweets
    }

    # Create a DataFrame
    df = pd.DataFrame(data)

    # Specify the file name
    filename = 'tweet.csv'

    # Save the DataFrame to a CSV file
    df.to_csv(filename, index=False)

    print(f'CSV file "{filename}" created successfully.')
