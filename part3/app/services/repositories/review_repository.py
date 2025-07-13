"""
Review-specific repository for handling review database operations.
"""

from app.models.review import Review
from app.persistence.repository import SQLAlchemyRepository


class ReviewRepository(SQLAlchemyRepository):
    """
    Repository class for Review entity with review-specific operations.
    """
    
    def __init__(self):
        super().__init__(Review)

    def get_reviews_by_rating(self, rating):
        """
        Retrieve reviews by specific rating.
        
        Args:
            rating (int): Rating value (1-5)
            
        Returns:
            List[Review]: List of reviews with the specified rating
        """
        return self.model.query.filter_by(rating=rating).all()

    def get_reviews_by_rating_range(self, min_rating, max_rating):
        """
        Retrieve reviews within a rating range.
        
        Args:
            min_rating (int): Minimum rating
            max_rating (int): Maximum rating
            
        Returns:
            List[Review]: List of reviews within the rating range
        """
        return self.model.query.filter(
            Review.rating >= min_rating,
            Review.rating <= max_rating
        ).all()

    def get_reviews_above_rating(self, min_rating):
        """
        Get reviews above a minimum rating.
        
        Args:
            min_rating (int): Minimum rating threshold
            
        Returns:
            List[Review]: List of reviews above the minimum rating
        """
        return self.model.query.filter(Review.rating >= min_rating).all()

    def get_reviews_below_rating(self, max_rating):
        """
        Get reviews below a maximum rating.
        
        Args:
            max_rating (int): Maximum rating threshold
            
        Returns:
            List[Review]: List of reviews below the maximum rating
        """
        return self.model.query.filter(Review.rating <= max_rating).all()

    def search_reviews_by_text(self, text_query):
        """
        Search reviews by text content.
        
        Args:
            text_query (str): The text to search for
            
        Returns:
            List[Review]: List of reviews matching the search query
        """
        return self.model.query.filter(
            Review.text.ilike(f'%{text_query}%')
        ).all()

    def get_reviews_ordered_by_rating(self, ascending=True):
        """
        Get reviews ordered by rating.
        
        Args:
            ascending (bool): Whether to sort in ascending order
            
        Returns:
            List[Review]: List of reviews ordered by rating
        """
        if ascending:
            return self.model.query.order_by(Review.rating.asc()).all()
        else:
            return self.model.query.order_by(Review.rating.desc()).all()

    def get_reviews_ordered_by_date(self, ascending=True):
        """
        Get reviews ordered by creation date.
        
        Args:
            ascending (bool): Whether to sort in ascending order
            
        Returns:
            List[Review]: List of reviews ordered by creation date
        """
        if ascending:
            return self.model.query.order_by(Review.created_at.asc()).all()
        else:
            return self.model.query.order_by(Review.created_at.desc()).all()

    def get_positive_reviews(self):
        """
        Get positive reviews (rating >= 4).
        
        Returns:
            List[Review]: List of positive reviews
        """
        return self.get_reviews_above_rating(4)

    def get_negative_reviews(self):
        """
        Get negative reviews (rating <= 2).
        
        Returns:
            List[Review]: List of negative reviews
        """
        return self.get_reviews_below_rating(2)
