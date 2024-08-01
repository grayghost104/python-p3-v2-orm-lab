from __init__ import CURSOR, CONN
from department import Department
from employee import Employee


class Review:

    # Dictionary of objects saved to the database.
    all = {}

    def __init__(self, year, summary, employee_id, id=None):
        self.id = id
        self.year = year
        self.summary = summary
        self.employee_id = employee_id

    def __repr__(self):
        return (
            f"<Review {self.id}: {self.year}, {self.summary}, "
            + f"Employee: {self.employee_id}>"
        )
    def get_year(self):
        return self._year
   
    def set_year(self, value):
        if isinstance(value, int) and value >= 2000:
            self._year = value 
        else: 
            raise ValueError(
                "The year must be integer and less than or equal to 2000"
            )
    year = property(get_year,set_year)

    def get_summary(self):
        return self._summary

 
    def set_summary(self, value):
        if isinstance(value, str)and len(value) > 0:
            self._summary = value
        else:
            raise ValueError(
                "The summary has to be a non-empty string"
            )
    summary= property(get_summary, set_summary)
    def get_employee_id(self):
        return self._employee_id
  
    def set_employee_id(self, value):
        if type(value) is int and Employee.find_by_id(value):
            self._employee_id = value
        else:
            raise ValueError("The employee id must match to an employee in the database")
    employee_id = property(get_employee_id, set_employee_id)
    @classmethod
    def create_table(cls):
        """ Create a new table to persist the attributes of Review instances """
        sql = """
            CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY,
            year INT,
            summary TEXT,
            employee_id INTEGER,
            FOREIGN KEY (employee_id) REFERENCES employee(id))
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        """ Drop the table that persists Review  instances """
        CURSOR.execute('DROP TABLE IF EXISTS reviews;')
        CONN.commit()

    def save(self):
        """ Insert a new row with the year, summary, and employee id values of the current Review object.
        Update object id attribute using the primary key value of new row.
        Save the object in local dictionary using table row's PK as dictionary key"""
        saving= '''
            INSERT INTO reviews (year, summary, employee_id) 
            VALUES (?,?,?)
        '''
        CURSOR.execute(saving, (self.year, self.summary, self.employee_id))
        CONN.commit()
        self.id = CURSOR.lastrowid
        # type(self).all[self.id] = self

    @classmethod
    def create(cls, year, summary, employee_id):
        """ Initialize a new Review instance and save the object to the database. Return the new instance. """
        review_instance = cls(year, summary, employee_id)
        review_instance.save()

        return review_instance
   
    @classmethod
    def instance_from_db(cls, row):
        """Return an Review instance having the attribute values from the table row."""
        review = cls.all.get(row[0])
        if review:
            review.year = row[1]
            review.summary = row[2]
            review.employee_id = row[3]
        else:
            review = cls(row[1], row[2], row[3])
            review.id = row[0]
            cls.all[review.id] = review
        return review   

    @classmethod
    def find_by_id(cls, id):
        """Return a Review instance having the attribute values from the table row."""
        finding = 'SELECT * FROM reviews WHERE id = ?'
        row = CURSOR.execute(finding, (id,)).fetchone()
        return cls.instance_from_db(row) if row else None 

    def update(self):
        """Update the table row corresponding to the current Review instance."""
        brand_new='''
            UPDATE reviews 
            SET year = ?, summary = ?
            WHERE id = ?
        '''
        CURSOR.execute(brand_new, (self.year, self.summary, self.employee_id))
        CONN.commit()
        

    def delete(self):
        """Delete the table row corresponding to the current Review instance,
        delete the dictionary entry, and reassign id attribute"""
        CURSOR.execute(f'DELETE FROM reviews WHERE id ={self.id}')
        CONN.commit()
        del type(self).all[self.id]
        self.id = None

    @classmethod
    def get_all(cls):
        """Return a list containing one Review instance per table row"""
        everything = 'SELECT * FROM reviews'
        rows = CURSOR.execute(everything).fetchall()
        return [cls.instance_from_db(row) for row in rows ]

