from app import app as application
from app import db
from app.models import Customers, Bids, Logs_product, Products, Comments
import sqlalchemy as sa
import sqlalchemy.orm as so

if __name__ == "__main__":
    application.run(debug=True)
    @application.shell_context_processor
    def make_shell_context():
        return {'sa': sa, 'so': so, 'db': db, 'Customers': Customers, 'Bids': Bids, 'Products': Products, 'Comments': Comments, 'Logs_product': Logs_product}
