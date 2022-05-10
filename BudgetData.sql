CREATE TABLE Account (
    AccountID SERIAL PRIMARY KEY,
    AccountName VARCHAR(50) NOT NULL
);

CREATE TABLE BudgetUser (
    UserID SERIAL PRIMARY KEY,
    UserName VARCHAR NOT NULL
);

CREATE TABLE Category (
    CategoryID SERIAL PRIMARY KEY,
    CategoryName VARCHAR NOT NULL,
    ParentID INTEGER NULL,
    Goal DECIMAL(14, 2) NULL,
    AccountID INTEGER NULL,
    FOREIGN KEY (ParentID) REFERENCES Category(CategoryID),
    FOREIGN KEY (AccountID) REFERENCES Account(AccountID)
);

CREATE TABLE Ledger (
    LedgerID SERIAL PRIMARY KEY,
    LedgerName VARCHAR NOT NULL,
    Balance DECIMAL(14, 2) NOT NULL,
    LedgerAccount INTEGER NULL,
    FOREIGN KEY (LedgerAccount) REFERENCES Account(AccountID)
);

CREATE TABLE TransactionSchedule (
    ScheduleID SERIAL PRIMARY KEY,
    ScheduleName VARCHAR NOT NULL,
    StartDate DATE NOT NULL,
    EndDate DATE NULL,
    LastRunDate DATE NULL,
    Frequency VARCHAR NOT NULL,
    FrequencyDays INTEGER NOT NULL,
    Amount DECIMAL(14, 2) NOT NULL,
    ScheduleDescription VARCHAR(30) NOT NULL,
    ScheduleCategory INTEGER NULL,
    ScheduleLedger INTEGER NULL,
    ScheduleUser INTEGER NULL,
    FOREIGN KEY (ScheduleCategory) REFERENCES Category(CategoryID),
    FOREIGN KEY (ScheduleLedger) REFERENCES Ledger(LedgerID),
    FOREIGN KEY (ScheduleUser) REFERENCES BudgetUser(UserID)
);

CREATE TABLE "Transaction" (
    TransactionID SERIAL PRIMARY KEY,
    Amount DECIMAL(14, 2) NOT NULL,
    TransactionDescription VARCHAR(30) NOT NULL,
    TransactionCategory INTEGER NULL,
    TransactionDate DATE NOT NULL,
    TransactionLedger INTEGER NULL,
    TransactionUser INTEGER NULL,
    FOREIGN KEY (TransactionCategory) REFERENCES Category(CategoryID),
    FOREIGN KEY (TransactionLedger) REFERENCES Ledger(LedgerID),
    FOREIGN KEY (TransactionUser) REFERENCES BudgetUser(UserID)
);

