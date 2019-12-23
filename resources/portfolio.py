from flask import jsonify
from flask_restful import Resource, reqparse
from models.portfolio import PortfolioModel
from utilities import validate_token


class Portfolio(Resource):

    @validate_token
    def get(self, current_user=None):
        portfolios = PortfolioModel.find_by_user_id(current_user.id)

        output = []
        for portfolio in portfolios:
            portfolio_data = dict()
            portfolio_data['id'] = portfolio.id
            portfolio_data['name'] = portfolio.name
            output.append(portfolio_data)

        return jsonify({'portfolios': output})
