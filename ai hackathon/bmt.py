import csv
import os

class BoneMarrowTransplantSystem:
    def _init_(self):
        self.DONOR_CSV = "donors.csv"
        self.PATIENT_CSV = "patients.csv"
        self.DONOR_FIELDS = ["Name", "Age", "Phone", "Blood Group", "HLA"]
        self.PATIENT_FIELDS = ["Name", "Age", "Disease", "HLA"]
        self.initialize_csv_files()
        self.load_data()

    def initialize_csv_files(self):
        # Create donors.csv if missing
        if not os.path.exists(self.DONOR_CSV):
            with open(self.DONOR_CSV, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(self.DONOR_FIELDS)

        # Create patients.csv if missing
        if not os.path.exists(self.PATIENT_CSV):
            with open(self.PATIENT_CSV, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(self.PATIENT_FIELDS)

    def load_data(self):
        # Load donors
        self.donors = []
        with open(self.DONOR_CSV, 'r') as f:
            reader = csv.DictReader(f)
            self.donors = list(reader)

        # Load patients
        self.patients = []
        with open(self.PATIENT_CSV, 'r') as f:
            reader = csv.DictReader(f)
            self.patients = list(reader)

    def add_donor(self, name, age, phone, blood_group, hla):
        if not all([name, phone, hla]):
            return False, "All fields are required"

        new_donor = {
            "Name": name,
            "Age": str(age),
            "Phone": phone,
            "Blood Group": blood_group,
            "HLA": hla
        }
        self.donors.append(new_donor)

        # Save to CSV
        with open(self.DONOR_CSV, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=self.DONOR_FIELDS)
            writer.writeheader()
            writer.writerows(self.donors)
        return True, "Donor added successfully"

    def add_patient(self, name, age, disease, hla):
        if not all([name, hla]):
            return False, "Name and HLA are required"

        new_patient = {
            "Name": name,
            "Age": str(age),
            "Disease": disease,
            "HLA": hla
        }
        self.patients.append(new_patient)

        # Save to CSV
        with open(self.PATIENT_CSV, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=self.PATIENT_FIELDS)
            writer.writeheader()
            writer.writerows(self.patients)
        return True, "Patient added successfully"

    def find_donor_match(self, patient_hla):
        if not patient_hla:
            return False, "Patient HLA is required"
        
        matched_donors = [
            donor for donor in self.donors 
            if donor["HLA"].lower() == patient_hla.lower()
        ]
        
        if matched_donors:
            return True, matched_donors
        return False, "No matching donors found"

    def list_donors(self):
        return self.donors

    def list_patients(self):
        return self.patients


def get_valid_age(prompt, min_age, max_age):
    while True:
        try:
            age = int(input(prompt))
            if min_age <= age <= max_age:
                return age
            print(f"Age must be between {min_age} and {max_age}")
        except ValueError:
            print("Please enter a valid number")


def get_valid_blood_group():
    valid_groups = ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"]
    while True:
        blood_group = input("Enter blood group (A+/A-/B+/B-/O+/O-/AB+/AB-): ").upper()
        if blood_group in valid_groups:
            return blood_group
        print("Invalid blood group. Please try again.")


def main():
    try:
        system = BoneMarrowTransplantSystem()
        
        while True:
            print("\n=== Bone Marrow Transplant Management System ===")
            print("1. Add Donor")
            print("2. Add Patient")
            print("3. Find Donor Match")
            print("4. List All Donors")
            print("5. List All Patients")
            print("6. Exit")
            
            choice = input("\nEnter your choice (1-6): ").strip()
            
            if choice == "1":
                print("\n--- Add New Donor ---")
                name = input("Enter donor name: ").strip()
                age = get_valid_age("Enter donor age (18-65): ", 18, 65)
                phone = input("Enter phone number: ").strip()
                blood_group = get_valid_blood_group()
                hla = input("Enter HLA type: ").strip()
                
                success, message = system.add_donor(name, age, phone, blood_group, hla)
                print(f"\n{'Success' if success else 'Error'}: {message}")

            elif choice == "2":
                print("\n--- Add New Patient ---")
                name = input("Enter patient name: ").strip()
                age = int(input("Enter patient age: "))
                disease = input("Enter disease/condition: ").strip()
                hla = input("Enter HLA type: ").strip()
                
                success, message = system.add_patient(name, age, disease, hla)
                print(f"\n{'Success' if success else 'Error'}: {message}")

            elif choice == "3":
                print("\n--- Find Donor Match ---")
                hla = input("Enter patient HLA type to match: ").strip()
                success, result = system.find_donor_match(hla)
                if success:
                    print("\nMatching donors found:")
                    print(" | ".join(system.DONOR_FIELDS))
                    print("-" * (sum(len(field) for field in system.DONOR_FIELDS) + 3 * (len(system.DONOR_FIELDS) - 1)))
                    for donor in result:
                        print(" | ".join(donor[field] for field in system.DONOR_FIELDS))
                else:
                    print(f"\nError: {result}")

            elif choice == "4":
                print("\n--- All Donors ---")
                donors = system.list_donors()
                if donors:
                    print(" | ".join(system.DONOR_FIELDS))
                    print("-" * (sum(len(field) for field in system.DONOR_FIELDS) + 3 * (len(system.DONOR_FIELDS) - 1)))
                    for donor in donors:
                        print(" | ".join(donor[field] for field in system.DONOR_FIELDS))
                else:
                    print("No donors registered yet")

            elif choice == "5":
                print("\n--- All Patients ---")
                patients = system.list_patients()
                if patients:
                    print(" | ".join(system.PATIENT_FIELDS))
                    print("-" * (sum(len(field) for field in system.PATIENT_FIELDS) + 3 * (len(system.PATIENT_FIELDS) - 1)))
                    for patient in patients:
                        print(" | ".join(patient[field] for field in system.PATIENT_FIELDS))
                else:
                    print("No patients registered yet")

            elif choice == "6":
                print("\nThank you for using the system. Goodbye!")
                break

            else:
                print("\nInvalid choice. Please try again.")

    except KeyboardInterrupt:
        print("\nProgram interrupted. Exiting...")


if __name__ == "_main_":
    main()