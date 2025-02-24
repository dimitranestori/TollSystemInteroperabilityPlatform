-- Δημιουργία της βάσης δεδομένων
DROP DATABASE IF EXISTS softeng;
CREATE DATABASE softeng;
USE softeng;

-- Δημιουργία του πίνακα Operator
CREATE TABLE Operator (
    op_ID VARCHAR(10) NOT NULL,
    operator VARCHAR(255) NOT NULL,
    PRIMARY KEY (op_ID)
);

-- Δημιουργία του πίνακα Toll
CREATE TABLE Toll (
    toll_ID VARCHAR(10) NOT NULL,
    operator_id VARCHAR(10),
    name VARCHAR(255) NOT NULL,
    locality VARCHAR(255),
    PM CHAR(2),
    road VARCHAR(255),
    price1 FLOAT,
    price2 FLOAT,
    price3 FLOAT,
    price4 FLOAT,
    PRIMARY KEY (toll_ID),
    FOREIGN KEY (operator_id) REFERENCES Operator(op_ID) ON DELETE CASCADE
);

-- Δημιουργία του πίνακα Tags
CREATE TABLE Tags(
    tagRef VARCHAR(255) NOT NULL,
    tagHomeID VARCHAR(10) NOT NULL,
    PRIMARY KEY (tagRef),
    FOREIGN KEY (tagHomeID) REFERENCES Operator(op_ID) ON DELETE CASCADE
);

-- Δημιουργία του πίνακα Charges
CREATE TABLE Charges (
    transaction_ID INT NOT NULL AUTO_INCREMENT,
    amount FLOAT NOT NULL,
    date TIMESTAMP NOT NULL,
    toll_ID VARCHAR(10),
    op_ID VARCHAR(10),
    tagRef VARCHAR(255),
    PRIMARY KEY (transaction_ID),
    FOREIGN KEY (toll_ID) REFERENCES Toll(toll_ID) ON DELETE CASCADE,
    FOREIGN KEY (op_ID) REFERENCES Operator(op_ID) ON DELETE CASCADE,
    FOREIGN KEY (tagRef) REFERENCES Tags(tagRef) ON DELETE CASCADE
);

-- Δημιουργία του πίνακα OperatorUser
CREATE TABLE OperatorUser (
    ID INT NOT NULL AUTO_INCREMENT,
    username VARCHAR(255) NOT NULL,
    password INT NOT NULL,
    role VARCHAR(255),
    PRIMARY KEY (ID)
);




