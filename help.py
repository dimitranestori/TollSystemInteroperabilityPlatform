import csv

# Define the input and output file paths
csv_file_path = 'c:/Users/el200/softeng24-10/uploads/passes-sample.csv'
output_file_path = 'c:/Users/el200/softeng24-10/database/temporary/populate_charges.sql'

# Open the CSV file and read its contents
with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    print(reader.fieldnames)
    
    # Open the output file for writing
    with open(output_file_path, 'w', encoding='utf-8') as sqlfile:
        # Write the initial SQL command
        sqlfile.write("USE softeng;\n\n")
        
        # Write the SQL command to insert tags
        sqlfile.write("INSERT INTO Tags (tagRef, tagHomeID) VALUES\n")
        
        # Iterate over the rows in the CSV file to insert tags
        rows = list(reader)
        tags = set()
        for row in rows:
            tag = (row['tagRef'], row['tagHomeID'])
            if tag not in tags:
                tags.add(tag)
                sqlfile.write(f"('{tag[0]}', '{tag[1]}'),\n")
        
        # Remove the last comma and newline, and add a semicolon
        sqlfile.seek(sqlfile.tell() - 2, 0)
        sqlfile.write(";\n\n")
        
        # Write the SQL command to insert charges
        sqlfile.write("INSERT INTO Charges (amount, date, toll_ID, to_op_ID, op_ID, tagRef) VALUES\n")
        
        # Iterate over the rows in the CSV file to insert charges
        for i, row in enumerate(rows):
            # Format the SQL values for the current row
            values = (
                row['charge'],
                row['\ufefftimestamp'],
                row['tollID'],
                row['tagHomeID'],
                row['tagRef']
            )
            # Write the SQL values to the output file
            sqlfile.write(f"({values[0]}, '{values[1]}', '{values[2]}', '{values[3]}', '{values[4]}')")
            
            # Add a comma after each row except the last one
            if i < len(rows) - 1:
                sqlfile.write(",\n")
            else:
                sqlfile.write(";\n")

print(f"SQL script has been saved to {output_file_path}")