from flask import Flask, request
from flask_restful import Api, Resource, reqparse
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
import logging
import os
import json

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ProductName = db.Column(db.String(100), nullable=False)
    ProductCode = db.Column(db.String(100), unique=True, nullable=False)
    Price = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True),server_default=func.now())

    def __repr__(self):
        return f"{self.ProductName} - {self.ProductCode} - {self.Price} - {self.created_at}"


@app.before_first_request
def create_tables():
    db.create_all()


@app.route('/')
def hello():
    if request.method == "GET":
        return "Please use our API Services! Path = 'api/v1/<service_name>'"


@app.route("/api/v1/product", methods=["POST","GET"])
def addproduct():
    if request.method == "POST":
        content_type = request.headers.get('Content-Type')
        if content_type == 'application/json':
            data = request.json
            try:
                newproduct = Product(ProductName=data['ProductName'], ProductCode=data['ProductCode'],
                                     Price=data['Price'])
                db.session.add(newproduct)
                db.session.commit()
                app.logger.info(f"{newproduct}")
            except:
                return f"{data['ProductCode']} already exists! Please check and try again!", 400
            return "", 200
        return "Content-Type not supported!"
    if request.method == "GET":
        productcode = request.args.get('ProductCode')
        app.logger.info(f"Querry for {productcode}")
        if productcode:
            try:
                check_product = Product.query.filter_by(ProductCode=productcode).first()
                data = {
                        "ProductName": f"{check_product.ProductName}",
                        "ProductCode": f"{check_product.ProductCode}",
                        "Price": f"{check_product.Price}",
                        "Added": f"{check_product.created_at}"
                        }
                return data, 200
            except:
                app.logger.error(f"NOT FOUND {productcode}")
                return f"{productcode} Not found", 404


if __name__ == "__main__":
    logging.basicConfig(filename='logs.log', level=logging.DEBUG)
    app.run(host="0.0.0.0", debug=True, port=3251)