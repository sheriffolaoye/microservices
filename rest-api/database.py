import pymysql
import config

class Database(object):
    def __init__(self):
        self.db_username = config.db_username
        self.db_host = config.db_endpoint
        self.db_name = config.db_name
        self.db_password = config.db_password        
        self.connection = None
        

    def connect(self):
        try:
            self.connection = pymysql.connect(host=self.db_host, user=self.db_username, db=self.db_name, password=self.db_password)
            self.cursor = self.connection.cursor()
            return True
        except:
            print("Couldn't connect to database")
            return False
            

    def add_user(self, email, f_name, l_name, passw_hash, hash_salt):
        if self.connect():
            query = """INSERT INTO Login(email, first_name, last_name, password, hash_salt) VALUES
                        ('{}', '{}', '{}', '{}', '{}')""".format(email, f_name, l_name, passw_hash, hash_salt)
            self.cursor.execute(query)
            self.connection.commit()
            self.connection.close()
            return True
        
        return False


    def validate_user(self, email):
        if self.connect():
            query = """SELECT password, hash_salt, first_name, last_name FROM Login 
                        WHERE email='{}'""".format(email)
            self.cursor.execute(query)
            result = self.cursor.fetchone()
            return result
        
        return None

    
    def check_user(self, email):
        if self.connect():
            query = "SELECT * FROM Login WHERE email='{}'".format(email)
            self.cursor.execute(query)
            result = self.cursor.fetchone()
            self.connection.close()

            # email is available
            if result == None:
                return True
            # username is taken(not available)
            else:
                return False
        
        return None

    
    def add_admin(self, email, f_name, l_name, passw_hash, hash_salt):
        if self.connect():
            query = """INSERT INTO Admin(email, first_name, last_name, password, hash_salt) VALUES
                        ('{}', '{}', '{}', '{}', '{}')""".format(email, f_name, l_name, passw_hash, hash_salt)
            self.cursor.execute(query)
            self.connection.commit()
            self.connection.close()
            return True
        
        return False


    def validate_admin(self, email):
        if self.connect():
            query = """SELECT password, hash_salt, first_name, last_name FROM Admin 
                        WHERE email='{}'""".format(email)
            self.cursor.execute(query)
            result = self.cursor.fetchone()
            return result
        return None


    def check_admin(self, email):
        if self.connect():
            query = "SELECT * FROM Admin WHERE email='{}'".format(email)
            self.cursor.execute(query)
            result = self.cursor.fetchone()
            self.connection.close()

            # email is available
            if result == None:
                return True
            # username is taken(not available)
            else:
                return False
        
        return None


    def add_item(self, name, quantity, tags, description, price, image_url):
        if self.connect():
            query = """INSERT INTO Item(name, quantity, tags, description, price, image_url) VALUES
                        ('{}', {}, '{}', '{}', {}, '{}')""".format(name, quantity, tags, description, price, image_url)
            self.cursor.execute(query)
            self.connection.commit()
            self.connection.close()
            return True

        return False


    def get_items(self):
        if self.connect():
            query = "SELECT * FROM Item"
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            self.connection.close()

            # return all Items
            if result:
                return result
        
        return None


    def item_by_id(self, item_id):
        if self.connect():
            query = "SELECT * FROM Item WHERE id={}".format(item_id)
            self.cursor.execute(query)
            result = self.cursor.fetchone()
            self.connection.close()

            # return all Items
            if result:
                return result
        
        return None



    def item_quantity(self, item_id):
        if self.connect():
            query = "SELECT quantity FROM Item WHERE id='{}'".format(item_id)
            self.cursor.execute(query)
            result = self.cursor.fetchone()
            self.connection.close()

            if result:
                return result[0]
            else:
                return 0
        
        return None


    def add_to_cart(self, email, item_id, quantity):
        if self.connect():
            query = """INSERT INTO Cart(email, item_id, quantity) 
                       VALUES('{}', {}, {})""".format(email, item_id, quantity)
            self.cursor.execute(query)
            self.connection.commit()
            self.connection.close()
            return True

        return False


    def in_cart(self, email, item_id):
        if self.connect():
            query = "SELECT * FROM Cart WHERE email='{}' AND item_id={}".format(email, item_id)
            self.cursor.execute(query)
            result = self.cursor.fetchone()
            self.connection.close()

            if result == None:
                return False
            else:
                return True
        
        return None


    def get_user_cart(self, email):
        if self.connect():
            query = "SELECT item_id, quantity FROM Cart WHERE email='{}'".format(email)
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            self.connection.close()

            if result != None:
                return result

        return None

    # method to increase quantity of item already in Cart
    def increase_quantity(self, email, item_id):
        if self.connect():
            query = """UPDATE Cart SET quantity=quantity + 1  
                       WHERE email='{}' AND item_id={}""".format(email, item_id)
            self.cursor.execute(query)
            self.connection.commit()
            self.connection.close()
            return True
        
        return False