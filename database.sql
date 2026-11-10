CREATE DATABASE IF NOT EXISTS store_db;
CREATE USER IF NOT EXISTS 'store_user'@'localhost' IDENTIFIED BY 'change_this_password';
GRANT ALL PRIVILEGES ON store_db.* TO 'store_user'@'localhost';
FLUSH PRIVILEGES;

USE store_db;

CREATE TABLE IF NOT EXISTS items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(150) NOT NULL UNIQUE,
    quantity INT NOT NULL DEFAULT 0,
    unit_price DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    CHECK (quantity >= 0)
);

CREATE TABLE IF NOT EXISTS sales (
    id INT AUTO_INCREMENT PRIMARY KEY,
    item_id INT NOT NULL,
    quantity INT NOT NULL,
    unit_price DECIMAL(10, 2) NOT NULL,
    sold_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (item_id) REFERENCES items(id),
    CHECK (quantity > 0)
);
