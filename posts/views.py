from django.shortcuts import render

from .models import Post

import random, string

#Upload photo and create post
def upload_photo(request):
    if request.method == "POST":
        pass

#Generate unique post id
def generate_post_id():
    unique = False
    random_id = 0

    #Check if id already exists
    while not unique:
        random_id = ''.join([random.choice(string.ascii_letters +
            string.digits) for n in range(11)])

        if Post.objects.filter(u_id=random_id).exists():
            unique = False
        else:
            unique = True

    return random_id
