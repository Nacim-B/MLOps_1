-- name: create_table
CREATE TABLE IF NOT EXISTS pima_diabetes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pregnancies INT,
    glucose FLOAT,
    blood_pressure FLOAT,
    skin_thickness FLOAT,
    insulin FLOAT,
    bmi FLOAT,
    diabetes_pedigree FLOAT,
    age INT,
    diabetes INT
);

-- name: select_all
SELECT * FROM pima_diabetes;
