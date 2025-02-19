CREATE DATABASE IF NOT EXISTS student_db;
USE student_db;

DROP TABLE IF EXISTS students;

CREATE TABLE students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    age INT NOT NULL,
    grade VARCHAR(10) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert sample data
INSERT INTO students (name, age, grade) VALUES
    ('John Doe', 20, 'A'),
    ('Jane Smith', 19, 'B'),
    ('Mike Johnson', 21, 'A-'),
    ('Sarah Williams', 20, 'B+');