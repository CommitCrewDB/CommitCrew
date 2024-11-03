CREATE DATABASE Baseball;
USE Baseball;

CREATE TABLE TeamsFranchises (
    franchID VARCHAR(10) PRIMARY KEY,
    franchName VARCHAR(100),
    active CHAR(1),       -- Y veya N
    NAassoc VARCHAR(10)
);


CREATE TABLE teams (
    yearID INT,
    lgID VARCHAR(10),
    teamID VARCHAR(10) PRIMARY KEY,
    franchID VARCHAR(10),
    divID VARCHAR(10),
    `Rank` INT,  -- Tırnak içine aldık
    G INT,
    GHome INT,
    W INT,
    L INT,
    DivWin CHAR(1),        -- Y veya N
    WCWin CHAR(1),         -- Y veya N
    LgWin CHAR(1),         -- Y veya N
    WSWin CHAR(1),         -- Y veya N
    R INT,
    AB INT,
    H INT,
    `2B` INT,              -- İki basamaklı isimler için tırnak işareti kullandık
    `3B` INT,              -- Üç basamaklı isimler için tırnak işareti kullandık
    HR INT,
    BB INT,
    SO INT,
    SB INT,
    CS INT,
    HBP INT,
    SF INT,
    RA INT,
    ER INT,
    ERA DECIMAL(4, 2),
    CG INT,
    SHO INT,
    SV INT,
    IPOuts INT,
    HA INT,
    HRA INT,
    BBA INT,
    SOA INT,
    E INT,
    DP INT,
    FP DECIMAL(4, 3),
    name VARCHAR(100),
    park VARCHAR(100),
    attendance INT,
    BPF INT,
    PPF INT,
    teamIDBR VARCHAR(10),
    teamIDlahman45 VARCHAR(10),
    teamIDretro VARCHAR(10),
    FOREIGN KEY (franchID) REFERENCES TeamsFranchises(franchID) 
);


