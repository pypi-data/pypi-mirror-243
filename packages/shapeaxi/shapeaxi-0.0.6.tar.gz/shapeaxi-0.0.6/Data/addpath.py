import csv

def add_pathdata(row):
    subject_id = row['Subject_ID']
    age = int(row['Age'])
    version = 'V12' if age == 1 else 'V06'
    row['PathLeftEACSF'] = f"/ASD/Autism/IBIS/Proc_Data/IBIS_sa_eacsf_thickness/{subject_id}/{version}/eacsf/left_eacsf.txt"
    row['PathRightEACSF'] = f"/ASD/Autism/IBIS/Proc_Data/IBIS_sa_eacsf_thickness/{subject_id}/{version}/eacsf/right_eacsf.txt"
    row['PathLeftSa'] = f"/ASD/Autism/IBIS/Proc_Data/IBIS_sa_eacsf_thickness/{subject_id}/{version}/sa/left_sa.txt"
    row['PathRightSa'] = f"/ASD/Autism/IBIS/Proc_Data/IBIS_sa_eacsf_thickness/{subject_id}/{version}/sa/right_sa.txt"
    row['PathLeftThickness'] = f"/ASD/Autism/IBIS/Proc_Data/IBIS_sa_eacsf_thickness/{subject_id}/{version}/thickness/left_thickness.txt"
    row['PathRightThickness'] = f"/ASD/Autism/IBIS/Proc_Data/IBIS_sa_eacsf_thickness/{subject_id}/{version}/thickness/right_thickness.txt"

def process_csv(input_file, output_file):
    with open(input_file, 'r') as csv_in, open(output_file, 'w', newline='') as csv_out:
        reader = csv.DictReader(csv_in)
        fieldnames = reader.fieldnames + ['PathLeftEACSF', 'PathRightEACSF', 'PathLeftSa', 'PathRightSa', 'PathLeftThickness', 'PathRightThickness']
        writer = csv.DictWriter(csv_out, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            add_pathdata(row)
            writer.writerow(row)

if __name__ == "__main__":
    input_file = 'V06-12.csv'  # Replace with the actual file name
    output_file = 'V06-12path.csv'  # Replace with the desired output file name
    process_csv(input_file, output_file)
