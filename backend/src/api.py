from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
from flask_migrate import Migrate
import json
from flask_cors import CORS
from sqlalchemy.exc import SQLAlchemyError

from .database.models import db_drop_and_create_all, setup_db, Drink, db
from .auth.auth import AuthError, requires_auth

app = Flask(__name__, static_folder='../build', static_url_path='/')
setup_db(app)
migrate = Migrate(app, db)
CORS(app)

'''
@TODO uncomment the following line to initialize the database
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
!! Running this function will add one
'''
#db_drop_and_create_all()

@app.after_request
def after_request(response):
    '''
    Returns a response object
        Parameters:
            response (Object): A response object
        Returns:
            response (Object): A response object
    '''
    response.headers.add(
        'Access-Control-Allow-Headers', 'Content-Type,Authorization,true'
    )
    response.headers.add(
        'Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE'
    )
    return response


# ROUTES
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/')
@app.route('/tabs/drink-menu')
@app.route('/tabs/user-page')
def index():
    '''
        Test api endpoint on heroku
    '''
    # add one demo row which is helping in POSTMAN test
    """ drink = Drink(
        title='water2',
        recipe='[{"name": "water", "color": "blue", "parts": 1}]'
    )

    drink.insert() """
    
    """ return jsonify({
        'message': 'Mock data successfully created'
    }) """
    return app.send_static_file('index.html')

@app.route('/drinks')
def get_drinks():
    '''
    An endpoint that fetches all the drinks from the database
        Parameters:
            None
        Returns:
            [success] bool: successful transaction
            [drinks] array<Drink>: an array of drinks object
    '''

    # Fetch an array of drinks
    drinks = [ drink.short() for drink in Drink.query.all()]

    if not drinks:
        abort(404)

    return jsonify({
        'success': True,
        'drinks': drinks
        })

'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def get_drinks_detail(payload):
    '''
    An endpoint that fetches all the drinks detail from the database
        Parameters:
            None
        Returns:
            [success] bool: successful transaction
            [drinks] array<Drink>: an array of drink objects
    '''

    # Fetch an array of drinks
    drinks = [ drink.long() for drink in Drink.query.all()]

    if not drinks:
        abort(404)

    return jsonify({
        'success': True,
        'drinks': drinks
        })


'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def create_drink(payload):
    '''
    An endpoint that creates a drink
        Parameters:
            None
        Returns:
            [success] bool: successful transaction
            [drinks] array<Drink>: an array of the created drink
    '''
    body = request.get_json()

    if not all(body.values()):
        abort(400)

    try:
        title = body['title']
        recipe = json.dumps(body['recipe'])
        drink = Drink(title=title, recipe=recipe)
        drink.insert()

        return jsonify({
            'success': True,
            'drinks': [drink.long()]
            })

    except SQLAlchemyError as e:
        abort(400)


'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:drink_id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drink(payload, drink_id):
    '''
    An endpoint that updates a question rating
        Parameters:
            drink_id (int): id of drink to be updated
        Returns:
            [success] bool: successful transaction
            [drinks] array<Drink>: an array of the created drink
    '''
    body = request.get_json()

    try:
        drink = Drink.query.filter(Drink.id==drink_id).one_or_none()

        if drink is None:
            abort(404)

        if 'title' in body.keys():
            drink.title = body['title']

        if 'recipe' in body.keys():
            drink.recipe = json.dumps(body['recipe'])

        drink.update()

        result = Drink.query.filter(Drink.id==drink_id).one_or_none()

        return jsonify({
            'success': True,
            'drinks': [result.long()]
            })

    except SQLAlchemyError :
        abort(400)


'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:drink_id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(payload, drink_id):
    '''
    An endpoint that deletes a drink
        Parameters:
            drink_id (int): id of drink to be deleted
        Returns:
            [success] bool: successful transaction
            [id] int: id of deleted drink
    '''
    # Get question with id: question_id
    drink = Drink.query.filter(Drink.id==drink_id).one_or_none()

    if drink is None:
        abort(404)

    try:
        drink.delete()
        return jsonify({
            'success': True,
            'id': drink_id
        })
    except SQLAlchemyError :
        abort(500)


# Error Handling
'''
Example error handling for unprocessable entity
'''


@app.errorhandler(422)
def unprocessable(error):
    return(
        jsonify({
            'success': False,
            'error': 422,
            'message': 'unprocessable'
            }), 422
        )


'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''

'''
@TODO implement error handler for 404
    error handler should conform to general task above
'''
@app.errorhandler(400)
def bad_request(error):
    return (
        jsonify({
            'success': False,
            'error': 400,
            'message': 'Bad request'}),
        400
    )

@app.errorhandler(401)
def bad_request(error):
    return (
        jsonify({
            'success': False,
            'error': 401,
            'message': 'Unauthorized access'}),
        401
    )

@app.errorhandler(403)
def bad_request(error):
    return (
        jsonify({
            'success': False,
            'error': 403,
            'message': 'Forbidden'}),
        403
    )

@app.errorhandler(404)
def not_found(error):
    return (
        jsonify({
            'success': False,
            'error': 404,
            'message': 'Resource not found'}),
        404
    )

@app.errorhandler(500)
def server_error(error):
    return (
        jsonify({
            'success': False,
            'error': 500,
            'message': 'Server error'}),
        500
    )

'''
@TODO implement error handler for AuthError
    error handler should conform to general task above
'''
@app.errorhandler(AuthError)
def auth_error(_error):
    error_msg, status_code = _error.error, _error.status_code
    return(
        jsonify({
            'success': False,
            'error': status_code,
            'message': error_msg['message']
        }),
        status_code
    )
