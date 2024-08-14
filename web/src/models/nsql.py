
"""

create Model class for inheritance

"""

from core import db


class Model(object):
    
    def put(self):
        """
        Save a model instance.
        
        :return: Model instance
        """
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        """
        Delete a model instance
        
        :return: db.session.commit()'s result # need to change after test
        """
        db.session.delete(self)
        db.session.commit()