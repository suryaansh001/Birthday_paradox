import streamlit as st
import csv
from collections import defaultdict
import io
import matplotlib.pyplot as plt

# Read the CSV file and create a dictionary mapping dates to names
def read_csv_to_dict(csv_file):
    birthday_dict = defaultdict(list)  # Dictionary to store dates and the list of names
    csv_reader = csv.DictReader(io.StringIO(csv_file.decode('utf-8')))
    num_rows=0
    for row in csv_reader:
        dd = row['Date']
        date = f"{dd[0:2]}"  # Extract day
        name = row['Name']
        num_rows+=1
        birthday_dict[date].append(name)
    return birthday_dict,num_rows

# Count how many people share the same birthday and include names
def count_shared_birthdays(birthday_dict):
    shared_birthdays = {}
    for date, names in birthday_dict.items():
        if len(names) > 1:
            shared_birthdays[date] = {
                'count': len(names),
                'names': names
            }
    return shared_birthdays

# Streamlit app
def main():
    st.title("Birthday Shared Finder")

    st.write("Upload your CSV file containing birthday data.")

    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    
    if uploaded_file is not None:
        # Read and process the CSV file
        birthday_dict,rows = read_csv_to_dict(uploaded_file.getvalue())
         
        # Count shared birthdays
        shared_birthdays = count_shared_birthdays(birthday_dict)
        count_of_people_with_same_bday = 0
        # Display the results
        if shared_birthdays:
            st.write("Birthdays shared by multiple people:")
            for date, info in shared_birthdays.items():
                count = info['count']
                count_of_people_with_same_bday += count
                names = ', '.join(info['names'])
                st.write(f"Date {date}: {count} people")
                st.write(f"Names: {names}")
        else:
            st.write("No birthdays are shared by multiple people.")
        st.write("the probablity of shared birthdays is",count_of_people_with_same_bday/rows)

        # Plot the graph
        if shared_birthdays:
            fig, ax = plt.subplots()
            dates = list(shared_birthdays.keys())
            counts = [info['count'] for info in shared_birthdays.values()]
            
            ax.bar(dates, counts, color='skyblue')
            ax.set_xlabel("Date")
            ax.set_ylabel("Number of Shared Birthdays")
            ax.set_title("Shared Birthdays by Date")
            st.pyplot(fig)

if __name__ == "__main__":
    main()

