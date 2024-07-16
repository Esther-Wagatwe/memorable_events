from flask import request, jsonify, render_template
from flask_login import login_required, current_user
from models.reviews import Reviews 
from models.engine import Session
from views import app_views
import datetime

@app_views.route('/reviews/', methods=['GET'])
@login_required
def get_reviews():
    session = Session()
    try:
        reviews = session.query(Reviews).all()
        return jsonify([review.serialize() for review in reviews])
        # return render_template('reviews.html', reviews=reviews)
    finally:
        session.close()

@app_views.route('/reviews/<int:review_id>', methods=['GET'])
def get_review(review_id):
    session = Session()
    try:
        review = session.query(Reviews).get(review_id)
        if review:
            return jsonify(review.serialize())
        else:
            return jsonify({'error': 'Review not found'}), 404
    finally:
        session.close()

@app_views.route('/reviews/', methods=['POST'])
def create_review():
    data = request.json
    
    if not all(key in data for key in ('rating', 'comment', 'vendor_id', 'event_id')):
        return jsonify({'error': 'Missing required fields'}), 400
    
    new_review = Reviews(
        rating=data['rating'],
        comment=data['comment'],
        review_date=datetime.datetime.now(),
        vendor_id=data['vendor_id'],
        event_id=data['event_id'],
        user_id = current_user.user_id
    )
    
    session = Session()
    try:
        session.add(new_review)
        session.commit()
        return jsonify({'message': 'Review created successfully'}), 201
    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()

@app_views.route('/reviews/<int:review_id>', methods=['PUT'])
def edit_review(review_id):
    session = Session()
    review = session.query(Reviews).get(review_id)
    
    if not review:
        session.close()
        return jsonify({'error': 'Review not found'}), 404
    
    try:
        data = request.json
        
        if 'rating' in data:
            review.rating = data['rating']
        
        if 'comment' in data:
            review.comment = data['comment']
        
        if 'vendor_id' in data:
            review.vendor_id = data['vendor_id']
        
        if 'event_id' in data:
            review.event_id = data['event_id']
        
        if 'user_id' in data:
            review.user_id = data['user_id']
        
        session.commit()
        return jsonify({'message': 'Review updated successfully'})
    
    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()

@app_views.route('/reviews/<int:review_id>', methods=['DELETE'])
# @login_required
def delete_review(review_id):
    session = Session()
    review = session.query(Reviews).get(review_id)
    
    if review:
        session.delete(review)
        session.commit()
        session.close()
        return jsonify({'message': 'Review deleted successfully'})
    else:
        session.close()
        return jsonify({'error': 'Review not found'}), 404
