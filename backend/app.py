from flask import Flask, jsonify, request, redirect, url_for
from flasgger import Swagger, swag_from
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from models import Base, Transaction
from config import Config
import logging

app = Flask(__name__)
app.config.from_object(Config)

engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
Session = sessionmaker(bind=engine)

swagger = Swagger(app)

logging.basicConfig(
    filename=app.config['LOG_FILE'],
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s'
)
@app.route('/')
def redirect_to_docs():
    """Redirect to Swagger documentation"""
    return redirect(url_for('flasgger.apidocs'), code=302)

@app.route('/transactions', methods=['GET'])
@swag_from({
    'tags': ['Transactions'],
    'parameters': [
        {
            'name': 'page',
            'in': 'query',
            'type': 'integer',
            'description': 'Page number (default: 1)',
            'default': 1
        },
        {
            'name': 'per_page',
            'in': 'query',
            'type': 'integer',
            'description': 'Items per page (default: 10)',
            'default': 10
        }
    ],
    'responses': {
        200: {
            'description': 'List of transactions',
            'schema': {
                'type': 'object',
                'properties': {
                    'transactions': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'id': {'type': 'integer'},
                                'message': {'type': 'string'},
                                'sender': {'type': 'string'},
                                'receiver': {'type': 'string'},
                                'amount': {'type': 'integer'},
                                'date': {'type': 'string'},
                                'transaction_type': {'type': 'string'}
                            }
                        }
                    },
                    'total': {'type': 'integer'},
                    'page': {'type': 'integer'},
                    'per_page': {'type': 'integer'}
                }
            }
        }
    }
})
def get_transactions():
    """Get paginated list of transactions"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    session = Session()
    try:
        transactions = session.query(Transaction).limit(per_page).offset((page - 1) * per_page).all()
        total = session.query(func.count(Transaction.id)).scalar()
        result = [{
            'id': t.id,
            'message': t.message,
            'sender': t.sender,
            'receiver': t.receiver,
            'amount': t.amount,
            'date': t.date.isoformat() if t.date else None,
            'transaction_type': t.transaction_type
        } for t in transactions]
        return jsonify({
            'transactions': result,
            'total': total,
            'page': page,
            'per_page': per_page
        })
    finally:
        session.close()

@app.route('/transactions/<int:id>', methods=['GET'])
@swag_from({
    'tags': ['Transactions'],
    'parameters': [
        {
            'name': 'id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'Transaction ID'
        }
    ],
    'responses': {
        200: {
            'description': 'Transaction details',
            'schema': {
                'type': 'object',
                'properties': {
                    'id': {'type': 'integer'},
                    'message': {'type': 'string'},
                    'sender': {'type': 'string'},
                    'receiver': {'type': 'string'},
                    'amount': {'type': 'integer'},
                    'date': {'type': 'string'},
                    'transaction_type': {'type': 'string'}
                }
            }
        },
        404: {'description': 'Transaction not found'}
    }
})
def get_transaction(id):
    """Get details of a specific transaction"""
    session = Session()
    try:
        transaction = session.query(Transaction).get(id)
        if not transaction:
            return jsonify({'error': 'Transaction not found'}), 404
        return jsonify({
            'id': transaction.id,
            'message': transaction.message,
            'sender': transaction.sender,
            'receiver': transaction.receiver,
            'amount': transaction.amount,
            'date': transaction.date.isoformat() if transaction.date else None,
            'transaction_type': transaction.transaction_type
        })
    finally:
        session.close()

@app.route('/filter', methods=['GET'])
@swag_from({
    'tags': ['Transactions'],
    'parameters': [
        {
            'name': 'type',
            'in': 'query',
            'type': 'string',
            'description': 'Transaction type (e.g., Incoming Money)'
        },
        {
            'name': 'start_date',
            'in': 'query',
            'type': 'string',
            'description': 'Start date (YYYY-MM-DD)'
        },
        {
            'name': 'end_date',
            'in': 'query',
            'type': 'string',
            'description': 'End date (YYYY-MM-DD)'
        },
        {
            'name': 'min_amount',
            'in': 'query',
            'type': 'integer',
            'description': 'Minimum amount'
        },
        {
            'name': 'max_amount',
            'in': 'query',
            'type': 'integer',
            'description': 'Maximum amount'
        }
    ],
    'responses': {
        200: {
            'description': 'Filtered transactions',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'id': {'type': 'integer'},
                        'message': {'type': 'string'},
                        'sender': {'type': 'string'},
                        'receiver': {'type': 'string'},
                        'amount': {'type': 'integer'},
                        'date': {'type': 'string'},
                        'transaction_type': {'type': 'string'}
                    }
                }
            }
        }
    }
})
def filter_transactions():
    """Filter transactions by type, date, or amount"""
    session = Session()
    try:
        query = session.query(Transaction)
        if request.args.get('type'):
            query = query.filter(Transaction.transaction_type == request.args.get('type'))
        if request.args.get('start_date'):
            query = query.filter(Transaction.date >= request.args.get('start_date'))
        if request.args.get('end_date'):
            query = query.filter(Transaction.date <= request.args.get('end_date'))
        if request.args.get('min_amount'):
            query = query.filter(Transaction.amount >= request.args.get('min_amount', type=int))
        if request.args.get('max_amount'):
            query = query.filter(Transaction.amount <= request.args.get('max_amount', type=int))
        transactions = query.all()
        result = [{
            'id': t.id,
            'message': t.message,
            'sender': t.sender,
            'receiver': t.receiver,
            'amount': t.amount,
            'date': t.date.isoformat() if t.date else None,
            'transaction_type': t.transaction_type
        } for t in transactions]
        return jsonify(result)
    finally:
        session.close()

@app.route('/summary', methods=['GET'])
@swag_from({
    'tags': ['Transactions'],
    'parameters': [
        {
            'name': 'group_by',
            'in': 'query',
            'type': 'string',
            'enum': ['type', 'month'],
            'description': 'Group by transaction type or month'
        }
    ],
    'responses': {
        200: {
            'description': 'Transaction summaries',
            'schema': {
                'type': 'object',
                'properties': {
                    'summary': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'key': {'type': 'string'},
                                'total_amount': {'type': 'integer'},
                                'count': {'type': 'integer'}
                            }
                        }
                    }
                }
            }
        }
    }
})
def get_summary():
    """Get transaction summaries (by type or month)"""
    session = Session()
    try:
        group_by = request.args.get('group_by', 'type')
        if group_by == 'type':
            summary = session.query(
                Transaction.transaction_type,
                func.sum(Transaction.amount).label('total_amount'),
                func.count(Transaction.id).label('count')
            ).group_by(Transaction.transaction_type).all()
        else: 
            summary = session.query(
                func.strftime('%Y-%m', Transaction.date).label('month'),
                func.sum(Transaction.amount).label('total_amount'),
                func.count(Transaction.id).label('count')
            ).group_by(func.strftime('%Y-%m', Transaction.date)).all()
        result = [{'key': row[0], 'total_amount': row[1], 'count': row[2]} for row in summary]
        return jsonify({'summary': result})
    finally:
        session.close()

if __name__ == '__main__':
    app.run(debug=True)