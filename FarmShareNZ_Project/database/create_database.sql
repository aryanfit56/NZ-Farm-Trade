CREATE DATABASE IF NOT EXISTS farmshare_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER IF NOT EXISTS 'farmshare_user'@'localhost' IDENTIFIED BY 'ChangeThisPassword!';
GRANT ALL PRIVILEGES ON farmshare_db.* TO 'farmshare_user'@'localhost';
FLUSH PRIVILEGES;
-- Django migrations create application tables. Do not manually duplicate ORM tables.
