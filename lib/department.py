from lib.__init__ import CURSOR, CONN

class Department:

    def __init__(self, name, location, id=None):
        if not name or not location:
            raise ValueError("Both 'name' and 'location' must be provided.")

        self.id = id
        self.name = name
        self.location = location

    def __repr__(self):
        return f"<Department {self.id}: {self.name}, {self.location}>"

    def __str__(self):
        return f"{self.name} Department in {self.location}"

    @classmethod
    def create_table(cls):
        """Create a new table to persist the attributes of Department instances."""
        sql = """
            CREATE TABLE IF NOT EXISTS departments (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                location TEXT NOT NULL
            )
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        """Drop the table that persists Department instances."""
        sql = "DROP TABLE IF EXISTS departments;"
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        """Insert a new row with the name and location of this Department instance."""
        sql = """
            INSERT INTO departments (name, location)
            VALUES (?, ?)
        """
        CURSOR.execute(sql, (self.name, self.location))
        CONN.commit()

        self.id = CURSOR.lastrowid


    @classmethod
    def create(cls, name, location):
        """Initialize and save a new Department instance."""
        department = cls(name, location)
        department.save()
        return department

    def update(self):
        """Update the table row corresponding to this Department instance."""
        if self.id is None:
            raise ValueError("Cannot update a department that hasn't been saved yet.")

        sql = """
            UPDATE departments
            SET name = ?, location = ?
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.name, self.location, self.id))
        CONN.commit()

    def delete(self):
        """Delete the table row corresponding to this Department instance."""
        if self.id is None:
            raise ValueError("Cannot delete a department that hasn't been saved yet.")

        sql = "DELETE FROM departments WHERE id = ?"
        CURSOR.execute(sql, (self.id,))
        CONN.commit()

    @classmethod
    def get_all(cls):
        """Retrieve all department records from the database."""
        sql = "SELECT * FROM departments"
        rows = CURSOR.execute(sql).fetchall()
        return [cls(id=row[0], name=row[1], location=row[2]) for row in rows]

    @classmethod
    def find_by_id(cls, id):
        """Find a department by its ID."""
        sql = "SELECT * FROM departments WHERE id = ?"
        row = CURSOR.execute(sql, (id,)).fetchone()
        return cls(id=row[0], name=row[1], location=row[2]) if row else None
