from database import Database

class User():

    db = Database.getInstance().getConnection()
    
    # PRIMARY KEY
    user_id: int

    first_name: str 
    last_name: str
    email: str
    password: str 

    school_class: str 
    user_type: str

    def __init__(self, user_id: int, first_name: str, last_name: str, email: str, password: str, school_class: str, user_type: str):
        self.user_id = user_id

        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password

        self.school_class = school_class
        self.user_type = user_type

        
        cursor = self.db.cursor()
        cursor.execute('SELECT EXISTS(SELECT 1 FROM users WHERE email=?);', (email,))
        
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?)", (user_id, first_name, last_name, 
                                                                     email, password, school_class, user_type))
        else:
            raise RuntimeError("User already exists!")

        self.db.commit()



    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.email

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        return False


database = Database.getInstance()

new_user = User(2, "yarom", "bar_akiva", "yaro", "123", "1", "1")

print(new_user.user_id)