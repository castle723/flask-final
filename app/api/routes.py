from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Book, book_schema, books_schema

api = Blueprint('api',__name__, url_prefix='/api')

@api.route('/getdata')
def getdata():
    return {'yee': 'haw'}

@api.route('/books', methods = ['POST'])
@token_required
def create_book(current_user_token):
    title = request.json['title']
    author = request.json['author']
    ISBN_number = request.json['ISBN_number']
    page_number = request.json['page_number']
    cover_type = request.json['cover_type']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    book = Book(title, author, ISBN_number, page_number, cover_type, user_token = user_token )

    db.session.add(book)
    db.session.commit()

    response = book_schema.dump(book)
    return jsonify(response)

@api.route('/books', methods = ['GET'])
@token_required
def get_book(current_user_token):
    a_user = current_user_token.token
    books = Book.query.filter_by(user_token = a_user).all()
    response = books_schema.dump(books)
    return jsonify(response)

@api.route('/books/<id>', methods = ['GET'])
@token_required
def get_book_two(book_user_token, id):
    fan = book_user_token.token
    if fan == book_user_token.token:
        car = Book.query.get(id)
        response = book_schema.dump(car)
        return jsonify(response)
    else:
        return jsonify({"message": "Valid Token Required"}),401

@api.route('/book/<id>', methods = ['POST','PUT'])
@token_required
def update_book(current_user_token,id):
    book = Book.query.get(id) 
    book.author = request.json['author']
    book.title = request.json['title']
    book.ISBN_number = request.json['ISBN_number']
    book.page_number = request.json['page_number']
    book.cover_type = request.json['cover_type']
    book.user_token = current_user_token.token

    db.session.commit()
    response = book_schema.dump(book)
    return jsonify(response)

@api.route('/books/<id>', methods = ['DELETE'])
@token_required
def delete_book(current_user_token, id):
    book = Book.query.get(id)
    db.session.delete(book)
    db.session.commit()
    response = book_schema.dump(book)
    return jsonify(response)