from api.database import db

# Association Tables (many-to-many relationships)

# Book_Title <-> Reading_List (many-to-many)
contains_book = db.Table(
    'contains_book',
    db.Column('book_title_id', db.Integer, db.ForeignKey('Book_Title.book_title_id'), primary_key=True),
    db.Column('reading_list_id', db.Integer, db.ForeignKey('Reading_List.reading_list_id'), primary_key=True)
)

# Book_Title <-> Genre (many-to-many)
is_genre = db.Table(
    'is_genre',
    db.Column('book_title_id', db.Integer, db.ForeignKey('Book_Title.book_title_id'), primary_key=True),
    db.Column('genre_id', db.Integer, db.ForeignKey('Genre.genre_id'), primary_key=True)
)

# Author <-> Book_Title (many-to-many)
written_by = db.Table(
    'written_by',
    db.Column('author_id', db.Integer, db.ForeignKey('Author.author_id'), primary_key=True),
    db.Column('book_title_id', db.Integer, db.ForeignKey('Book_Title.book_title_id'), primary_key=True)
)

# User <-> User friendship (self-referential many-to-many)
friends_with = db.Table(
    'friends_with',
    db.Column('user_id', db.Integer, db.ForeignKey('User.user_id'), primary_key=True),
    db.Column('friend_id', db.Integer, db.ForeignKey('User.user_id'), primary_key=True),
    db.Column('status', db.String(255), nullable=False),
    db.Column('created_at', db.Integer, default=0)
)


# Main Models

class Region(db.Model):
    __tablename__ = 'Region'

    region_id = db.Column(db.Integer, primary_key=True)
    region_name = db.Column(db.String(255), nullable=False)
    region_coord_lat = db.Column(db.Float)
    region_coord_lon = db.Column(db.Float)
    zipcode = db.Column(db.Integer, nullable=False)
    population = db.Column(db.Integer, default=0)

    # Relationships
    users = db.relationship('User', back_populates='region')


class UserInfo(db.Model):
    __tablename__ = 'User_Info'

    user_info_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    is_active = db.Column(db.Boolean)

    # Relationships
    user = db.relationship('User', back_populates='user_info', uselist=False)


class User(db.Model):
    __tablename__ = 'User'

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    user_info_id = db.Column(db.Integer, db.ForeignKey('User_Info.user_info_id'))
    region_id = db.Column(db.Integer, db.ForeignKey('Region.region_id'))
    date_joined = db.Column(db.Integer)
    books_borrowed_current = db.Column(db.Integer)
    books_borrowed_lifetime = db.Column(db.Integer)
    books_owned = db.Column(db.Integer)

    # Relationships
    user_info = db.relationship('UserInfo', back_populates='user')
    region = db.relationship('Region', back_populates='users')
    books = db.relationship('Book', back_populates='owner', foreign_keys='Book.owner_id')
    reading_lists = db.relationship('ReadingList', back_populates='owner')
    
    # Lending relationships
    loans_as_lender = db.relationship('LendingRecord', back_populates='lender', foreign_keys='LendingRecord.lender_id')
    loans_as_borrower = db.relationship('LendingRecord', back_populates='borrower', foreign_keys='LendingRecord.borrower_id')

    # Self-referential friendship relationship
    friends = db.relationship(
        'User',
        secondary=friends_with,
        primaryjoin=(user_id == friends_with.c.user_id),
        secondaryjoin=(user_id == friends_with.c.friend_id),
        backref='friended_by'
    )


class Author(db.Model):
    __tablename__ = 'Author'

    author_id = db.Column(db.Integer, primary_key=True)
    last_name = db.Column(db.String(255))
    first_name = db.Column(db.String(255))
    birthyear = db.Column(db.Integer)

    # Relationships
    books_written = db.relationship('BookTitle', secondary=written_by, back_populates='authors')


class Genre(db.Model):
    __tablename__ = 'Genre'

    genre_id = db.Column(db.Integer, primary_key=True)
    genre_name = db.Column(db.String(255), unique=True)
    count_books = db.Column(db.Integer)

    # Relationships
    book_titles = db.relationship('BookTitle', secondary=is_genre, back_populates='genres')


class BookTitle(db.Model):
    __tablename__ = 'Book_Title'

    book_title_id = db.Column(db.Integer, primary_key=True)
    book_title_name = db.Column(db.String(255), nullable=False)
    date_of_publication = db.Column(db.Integer)

    # Relationships
    authors = db.relationship('Author', secondary=written_by, back_populates='books_written')
    genres = db.relationship('Genre', secondary=is_genre, back_populates='book_titles')
    books = db.relationship('Book', back_populates='title')
    reading_lists = db.relationship('ReadingList', secondary=contains_book, back_populates='book_titles')


class Book(db.Model):
    __tablename__ = 'Book'

    book_id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('User.user_id'), nullable=False)
    title_id = db.Column(db.Integer, db.ForeignKey('Book_Title.book_title_id'), nullable=False)
    date_added = db.Column(db.Integer)
    times_borrowed = db.Column(db.Integer)
    is_lendable = db.Column(db.Boolean)
    is_being_lent = db.Column(db.Boolean)
    quality = db.Column(db.String(511))

    # Relationships
    owner = db.relationship('User', back_populates='books', foreign_keys=[owner_id])
    title = db.relationship('BookTitle', back_populates='books')
    lending_records = db.relationship('LendingRecord', back_populates='book')


class ReadingList(db.Model):
    __tablename__ = 'Reading_List'

    reading_list_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, default='Untitled Reading List')
    description = db.Column(db.String(511))
    owner_id = db.Column(db.Integer, db.ForeignKey('User.user_id'))

    # Relationships
    owner = db.relationship('User', back_populates='reading_lists')
    book_titles = db.relationship('BookTitle', secondary=contains_book, back_populates='reading_lists')


class LendingRecord(db.Model):
    __tablename__ = 'Lending_Record'

    lending_record_id = db.Column(db.Integer, primary_key=True)
    lender_id = db.Column(db.Integer, db.ForeignKey('User.user_id'), nullable=False)
    borrower_id = db.Column(db.Integer, db.ForeignKey('User.user_id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('Book.book_id'), nullable=False)
    borrowed_start = db.Column(db.Integer)
    borrowed_end = db.Column(db.Integer)
    actively_borrowed = db.Column(db.Boolean)

    # Relationships
    lender = db.relationship('User', back_populates='loans_as_lender', foreign_keys=[lender_id])
    borrower = db.relationship('User', back_populates='loans_as_borrower', foreign_keys=[borrower_id])
    book = db.relationship('Book', back_populates='lending_records')
