import os
import csv

class Master:
    def __init__(self, ID, playerID, nameFirst, nameLast, birthYear, birthCountry, birthState, height, weight, bats, throws):
        self.ID = ID
        self.playerID = playerID
        self.nameFirst = nameFirst
        self.nameLast = nameLast
        self.birthYear = birthYear
        self.birthCountry = birthCountry
        self.birthState = birthState
        self.height = height
        self.weight = weight
        self.bats = bats
        self.throws = throws

    @staticmethod
    def load_master_data():
        """Load data directly from Master.csv."""
        try:
            csv_folder = os.path.join(os.getcwd(), 'csv')  # Ensure the CSV folder is in the project directory
            file_path = os.path.join(csv_folder, 'Master.csv')
            file_path = r"C:\Users\recep\Desktop\CommitCrew\csv\Master.csv"

            data = []
            with open(file_path, mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    data.append(Master(
                        ID=row['ID'],
                        playerID=row['playerID'],
                        nameFirst=row['nameFirst'],
                        nameLast=row['nameLast'],
                        birthYear=int(row['birthYear']),
                        birthCountry=row['birthCountry'],
                        birthState=row['birthState'],
                        height=int(row['height']),
                        weight=int(row['weight']),
                        bats=row['bats'],
                        throws=row['throws'],
                    ))
            return data
        except FileNotFoundError:
            print(f"File not found: {file_path}")
            return []
        except Exception as e:
            print(f"Error reading CSV file: {e}")
            return []

    @staticmethod
    def search_and_sort(search_query):
        """Search for specific data in Master.csv."""
        data = Master.load_master_data()
        return [row for row in data if search_query.lower() in row.playerID.lower()]
