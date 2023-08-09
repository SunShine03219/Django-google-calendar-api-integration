from django import template

register = template.Library()

@register.filter
def get_star_rating_image(rating):
    if rating is None:
        return 'https://upload.wikimedia.org/wikipedia/commons/4/4a/Star_rating_0_of_5.png'
    if rating == 5:
        return "https://upload.wikimedia.org/wikipedia/commons/1/17/Star_rating_5_of_5.png"
    elif 4 < rating < 5:
        return "https://upload.wikimedia.org/wikipedia/commons/b/b9/Star_rating_4.5_of_5.png"
    elif rating == 4:
        return "https://upload.wikimedia.org/wikipedia/commons/f/fa/Star_rating_4_of_5.png"
    elif 3 < rating < 4:
        return "https://upload.wikimedia.org/wikipedia/commons/e/eb/Star_rating_3.5_of_5.png"
    elif rating == 3:
        return "https://upload.wikimedia.org/wikipedia/commons/2/2f/Star_rating_3_of_5.png"
    elif 2 < rating < 3:
        return "https://upload.wikimedia.org/wikipedia/commons/b/bf/Star_rating_2.5_of_5.png"
    elif rating == 2:
        return "https://upload.wikimedia.org/wikipedia/commons/9/95/Star_rating_2_of_5.png"
    elif 1 < rating < 2:
        return "https://upload.wikimedia.org/wikipedia/commons/a/a7/Star_rating_1.5_of_5.png"
    elif rating == 1:
        return "https://upload.wikimedia.org/wikipedia/commons/d/dd/Star_rating_1_of_5.png"
    elif rating == 0.5:
        return "https://upload.wikimedia.org/wikipedia/commons/8/82/Star_rating_0.5_of_5.png"
    else:
        return "https://upload.wikimedia.org/wikipedia/commons/4/4a/Star_rating_0_of_5.png"



@register.filter
def star_rating(value):
    if value is None:
        return 'https://upload.wikimedia.org/wikipedia/commons/4/4a/Star_rating_0_of_5.png'
    elif value == 5:
        return 'https://upload.wikimedia.org/wikipedia/commons/1/17/Star_rating_5_of_5.png'
    elif 4 <= value < 5:
        return 'https://upload.wikimedia.org/wikipedia/commons/b/b9/Star_rating_4.5_of_5.png'
    elif value == 4:
        return 'https://upload.wikimedia.org/wikipedia/commons/f/fa/Star_rating_4_of_5.png'
    elif 3 <= value < 4:
        return 'https://upload.wikimedia.org/wikipedia/commons/e/eb/Star_rating_3.5_of_5.png'
    elif value == 3:
        return 'https://upload.wikimedia.org/wikipedia/commons/2/2f/Star_rating_3_of_5.png'
    elif 2 <= value < 3:
        return 'https://upload.wikimedia.org/wikipedia/commons/b/bf/Star_rating_2.5_of_5.png'
    elif value == 2:
        return 'https://upload.wikimedia.org/wikipedia/commons/9/95/Star_rating_2_of_5.png'
    elif 1 <= value < 2:
        return 'https://upload.wikimedia.org/wikipedia/commons/a/a7/Star_rating_1.5_of_5.png'
    elif value == 1:
        return 'https://upload.wikimedia.org/wikipedia/commons/d/dd/Star_rating_1_of_5.png'
    elif value == 0.5:
        return 'https://upload.wikimedia.org/wikipedia/commons/8/82/Star_rating_0.5_of_5.png'
    else:
        return 'https://upload.wikimedia.org/wikipedia/commons/4/4a/Star_rating_0_of_5.png'
