from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Post
from groups.models import Group
from users.models import Profile
from favorites.models import Favorite

#Google imports
from google.cloud import storage

#Python imports
import random, string, os

#Set variable for Cloud storage access
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="creds.json"

#Upload photo and create post
@api_view(['POST'])
def upload_photo(request):
    if request.method == "POST":
        group = Group.objects.get(u_id=request.data["group_u_id"])
        profile = Profile.objects.get(user=request.user)
        caption = request.data["caption"]
        post_u_id = generate_post_id()

        storage_client = storage.Client()
        bucket = storage_client.get_bucket("tack-media-store")
        blob = bucket.blob(post_u_id)

        photo = request.data["photo"]
        blob.upload_from_file(photo, content_type="image/png")
        blob.make_public()

        new_post = Post.objects.create(url=blob.public_url, u_id=post_u_id,
                                       caption=caption, by=profile, group=group)
        group.posts.add(new_post)
        profile.posts.add(new_post)
        return Response({"message": "photo was posted"})

#Create favorite for a post
@api_view(['POST'])
def favorite_post(request, u_id):
    if request.method == "POST":
        profile = Profile.objects.get(user=request.user)
        post = Post.objects.get(u_id=u_id)

        favorite = Favorite.objects.create(profile=profile, post=post)
        post.favorites.add(favorite)
        profile.favorites.add(post)
        return Response({"message": "post was favorited"})

#Delete favorite and remove post from favorites
@api_view(['GET'])
def unfavorite_post(request, u_id):
    if request.method == "GET":
        post = Post.objects.get(u_id=u_id)
        profile = Profile.objects.get(user=request.user)

        favorite = Favorite.objects.get(profile=profile, post=post)
        post.favorites.remove(favorite)
        profile.favorites.remove(post)
        favorite.delete()
        return Response({"message": "post unfavorited"})

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
