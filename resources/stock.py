from flask_restful import Resource, reqparse
from models.stock import StockModel
from models.portfolio import PortfolioModel
from utilities import validate_token


class Stock(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('portfolio_id',
                        type=int,
                        required=True,
                        help="This field cannot be left blank!")
    parser.add_argument('symbol',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!")
    parser.add_argument('purchase_price',
                        type=float,
                        required=True,
                        help="This field cannot be left blank!")
    parser.add_argument('buy',
                        type=bool,
                        required=True,
                        help="This field cannot be left blank!")
    parser.add_argument('quantity',
                        type=int,
                        required=True,
                        help="This field cannot be left blank!")
    parser.add_argument('date',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!")

    @validate_token
    def post(self, current_user=None):
        data = Stock.parser.parse_args()
        portfolio_id = data["portfolio_id"]
        portfolio = PortfolioModel.find_by_portfolio_id(portfolio_id)
        if current_user.id != portfolio.user_id:
            return {"message": "This user doesn't own this portfolio"}, 401

        stock = StockModel(data["portfolio_id"],
                           data["symbol"],
                           data["purchase_price"],
                           data["buy"],
                           data["quantity"],
                           data["date"])

        stock.save_to_db()
        return {"message": "Stock added successfully"}, 201
