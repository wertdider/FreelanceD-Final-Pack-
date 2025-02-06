import csv

def save_to_csv(data, filename='freelancers.csv'):
    """Write to CSV"""
    header = ['Name', 'Skills', 'Country', 'Hourly Rate']
    
    with open(filename, 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        # Write header only if file is empty
        if file.tell() == 0:
            writer.writerow(header)
        
        for row in data:
            writer.writerow(row)
