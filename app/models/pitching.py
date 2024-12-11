import os
import csv

class Pitching:
    def __init__(self, playerID, yearID, stint, teamID, lgID, W, L, G, GS, CG, SHO, SV, IPouts, H, ER, HR, BB, SO,
                 BAOpp, ERA, IBB, WP, HBP, BK, BFP, GF, R, SH, SF, GIDP):
        self.playerID = playerID
        self.yearID = yearID
        self.stint = stint
        self.teamID = teamID
        self.lgID = lgID
        self.W = W
        self.L = L
        self.G = G
        self.GS = GS
        self.CG = CG
        self.SHO = SHO
        self.SV = SV
        self.IPouts = IPouts
        self.H = H
        self.ER = ER
        self.HR = HR
        self.BB = BB
        self.SO = SO
        self.BAOpp = BAOpp
        self.ERA = ERA
        self.IBB = IBB
        self.WP = WP
        self.HBP = HBP
        self.BK = BK
        self.BFP = BFP
        self.GF = GF
        self.R = R
        self.SH = SH
        self.SF = SF
        self.GIDP = GIDP

    @staticmethod
    def load_pitching_data():
        """Load data directly from pitching.csv."""
        try:
            csv_folder = os.path.join(os.getcwd(), 'csv')  # Ensure the CSV folder is in the project directory
            file_path = os.path.join(csv_folder, 'pitching.csv')
            data = []
            with open(file_path, mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    data.append(Pitching(
                        playerID=row['playerID'],
                        yearID=int(row['yearID']),
                        stint=int(row['stint']),
                        teamID=row['teamID'],
                        lgID=row['lgID'],
                        W=int(row['W']),
                        L=int(row['L']),
                        G=int(row['G']),
                        GS=int(row['GS']),
                        CG=int(row['CG']),
                        SHO=int(row['SHO']),
                        SV=int(row['SV']),
                        IPouts=int(row['IPouts']),
                        H=int(row['H']),
                        ER=int(row['ER']),
                        HR=int(row['HR']),
                        BB=int(row['BB']),
                        SO=int(row['SO']),
                        BAOpp=float(row['BAOpp']) if row['BAOpp'] else None,
                        ERA=float(row['ERA']) if row['ERA'] else None,
                        IBB=int(row['IBB']) if row['IBB'] else None,
                        WP=int(row['WP']) if row['WP'] else None,
                        HBP=int(row['HBP']) if row['HBP'] else None,
                        BK=int(row['BK']) if row['BK'] else None,
                        BFP=int(row['BFP']) if row['BFP'] else None,
                        GF=int(row['GF']) if row['GF'] else None,
                        R=int(row['R']) if row['R'] else None,
                        SH=int(row['SH']) if row['SH'] else None,
                        SF=int(row['SF']) if row['SF'] else None,
                        GIDP=int(row['GIDP']) if row['GIDP'] else None,
                    ))
            return data
        except FileNotFoundError:
            print(f"File not found: {file_path}")
            return []
        except Exception as e:
            print(f"Error reading CSV file: {e}")
            return []
