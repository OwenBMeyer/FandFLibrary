--
-- File generated with SQLiteStudio v3.4.18 on Sat Dec 20 13:39:30 2025
--
-- Text encoding used: System
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Table: Author
CREATE TABLE IF NOT EXISTS Author (
    author_id INT Primary Key,
    last_name VARCHAR(255),
    first_name VARCHAR(255),
    birthyear INT
);

-- Table: Book
CREATE TABLE IF NOT EXISTS Book(
    book_id INT PRIMARY KEY,
    owner_id INT NOT NULL,
    title_id INT NOT NULL,
    date_added INT,
    times_borrowed INT,
    is_lendable BOOLEAN,
    is_being_lent BOOLEAN,
    quality VARCHAR(511),
    FOREIGN KEY (owner_id)
        REFERENCES User(user_id)
            ON DELETE CASCADE
            ON UPDATE NO ACTION
    FOREIGN KEY (title_id)
        REFERENCES Book_Title(book_title_id)
            ON DELETE CASCADE
            ON UPDATE NO ACTION
);

-- Table: Book_Title
CREATE TABLE IF NOT EXISTS Book_Title (
    book_title_id INT PRIMARY KEY,
    book_title_name VARCHAR(255) NOT NULL,
    date_of_publication INT
    -- Author handled in seperate table to account for chance of multiple authors
);

-- Table: contains_book
CREATE TABLE IF NOT EXISTS contains_book(
    book_title_id INT,
    reading_list_id INT,
    PRIMARY KEY (book_title_id, reading_list_id),
    FOREIGN KEY (book_title_id)
        REFERENCES Book_Title(book_title_id)
            ON DELETE CASCADE
            ON UPDATE NO ACTION
    FOREIGN KEY (reading_list_id)
        REFERENCES Reading_List(reading_list_id)
            ON DELETE CASCADE
            ON UPDATE NO ACTION
);

-- Table: friends_with
CREATE TABLE IF NOT EXISTS friends_with(
    user_id INT,
    friend_id INT NOT NULL,
    status VARCHAR(255) NOT NULL,
    created_at INT DEFAULT 0,
    PRIMARY KEY (user_id, friend_id),
    FOREIGN KEY (user_id)
        REFERENCES User(user_id)
            ON DELETE CASCADE
            ON UPDATE NO ACTION
    FOREIGN KEY (friend_id)
        REFERENCES User(user_id)
            ON DELETE CASCADE
            ON UPDATE NO ACTION
);

-- Table: Genre
CREATE TABLE IF NOT EXISTS Genre (
    genre_id INT Primary Key,
    genre_name VARCHAR(255) UNIQUE,
    count_books INT
);

-- Table: is_genre
CREATE TABLE IF NOT EXISTS is_genre (
    book_title_id INT,
    genre_id INT,
    PRIMARY KEY (book_title_id, genre_id),
    FOREIGN KEY (book_title_id)
        REFERENCES Book_Title(book_title_id)
            ON DELETE CASCADE
            ON UPDATE NO ACTION
    FOREIGN KEY (genre_id)
        REFERENCES Genre(genre_id)
            ON DELETE CASCADE
            ON UPDATE NO ACTION
);

-- Table: Lending_Record
CREATE TABLE IF NOT EXISTS Lending_Record(
    lending_record_id INT PRIMARY KEY,
    lender_id INT NOT NULL,
    borrower_id INT NOT NULL,
    book_id INT NOT NULL,
    borrowed_start INT,
    borrowed_end INT,
    actively_borrowed BOOLEAN,
    FOREIGN KEY (lender_id)
        REFERENCES User(user_id)
            ON DELETE CASCADE
            ON UPDATE NO ACTION
    FOREIGN KEY (borrower_id)
        REFERENCES User(user_id)
            ON DELETE CASCADE
            ON UPDATE NO ACTION
    FOREIGN KEY (book_id)
        REFERENCES Book(book_id)
            ON DELETE CASCADE
            ON UPDATE NO ACTION
);

-- Table: Reading_List
CREATE TABLE IF NOT EXISTS Reading_List(
    reading_list_id INT PRIMARY KEY,
    name VARCHAR(255) NOT NULL DEFAULT 'Untitled Reading List',
    description VARCHAR(511),
    owner_id INT,
    FOREIGN KEY (owner_id)
        REFERENCES User(user_id)
            ON DELETE CASCADE
            ON UPDATE NO ACTION
);

-- Table: Region
CREATE TABLE IF NOT EXISTS Region (region_id INT PRIMARY KEY, region_name VARCHAR (255) NOT NULL, region_coord_lat REAL, region_coord_lon REAL, zipcode INT NOT NULL, population INTEGER DEFAULT (0));

-- Table: User
CREATE TABLE IF NOT EXISTS User (
    user_id INT PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    user_info_id INT, -- Foreign Key
    region_id INT, -- Foreign Key
    date_joined INT,
    books_borrowed_current INT,
    books_borrowed_lifetime INT,
    books_owned INT,
    FOREIGN KEY (user_info_id)
        REFERENCES User_Info(user_info_id)
            ON DELETE CASCADE
            ON UPDATE NO ACTION
    FOREIGN KEY (region_id)
        REFERENCES Region(region_id)
            ON DELETE CASCADE
            ON UPDATE NO ACTION
);

-- Table: User_Info
CREATE TABLE IF NOT EXISTS User_Info (
    user_info_id INT PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    is_active BOOLEAN
);

-- Table: written_by
CREATE TABLE IF NOT EXISTS written_by (
    author_id INT,
    book_title_id INT,
    PRIMARY KEY (author_id, book_title_id),
    FOREIGN KEY (author_id)
        REFERENCES Author(author_id)
            ON DELETE CASCADE
            ON UPDATE NO ACTION,
    FOREIGN KEY (book_title_id)
        REFERENCES Book_Title(book_title_id)
            ON DELETE CASCADE
            ON UPDATE NO ACTION
);

COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
