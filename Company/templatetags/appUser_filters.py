from django import template
from Company.models import Rating

register = template.Library()

@register.filter
def average_rating(user_id):
    ratings = Rating.objects.filter(provider=user_id, rate__isnull=False).exclude(rate=0)
    if ratings.exists():
        return sum(rating.rate for rating in ratings) / len(ratings)
    else:
        return None
    
@register.filter
def rating_comments(user_id):
    ratings = Rating.objects.filter(provider=user_id).exclude(rate=0).exclude(rate__isnull=True)
    comment = []
    for rating in ratings:
        comment.append((rating.comment, rating.rate))
    return comment