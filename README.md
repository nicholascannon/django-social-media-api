# Wall: A very lean social media API

![travisci](https://travis-ci.com/nicholascannon1/wall.svg?branch=master)

An extremely lean and basic social media REST API built with **Django and Django-REST-Framework (DRF)** that allows users to register for accounts, create posts, comment on posts and _pin_ (like) other posts to the _wall_. Authentication is done using [SimpleJWT](https://github.com/SimpleJWT/django-rest-framework-simplejwt). Testing implemented with [`django-nose`](https://github.com/jazzband/django-nose) and `coverage` (see coverage report below).

**Project Goals:**

- Complete a project with Django and DJango-REST-Framework
- Implement a **test driven approach** for developing a REST API
- Use **Travis-CI** to run automated tests when committing new code
- Learn class based and generic views in Django and DRF

## REST Endpoints

- `GET` -> `/posts/` -> returns current users posts (_auth required_)
- `POST` -> `/posts/` -> create new post (_auth required_)
- `GET` -> `/posts/<uuid>/` -> return post details
- `PUT` -> `/posts/<uuid>/` -> make an edit to the post text (_author only_)
- `DELETE` -> `/posts/<uuid>/` -> delete post (_author only_)
- `PUT` -> `/posts/<uuid>/pin/` -> increment post pins by 1 (_auth required_)
- `GET` -> `/posts/<uuid>/comments/` -> returns all comments for post with uuid
- `POST` -> `/posts/<uuid>/comments/` -> create new comment on post with uuid (_auth required_)
- `GET` -> `/posts/<post_uuid>/comments/<comment_uuid>/` -> comment details
- `DELETE` -> `/posts/<post_uuid>/comments/<comment_uuid>/` -> delete comment (_author only_)

_View the users `urls.py` file for the user account endpoints._

## Coverage Report

```
Name                   Stmts   Miss  Cover
------------------------------------------
posts/permissions.py       6      0   100%
posts/serializers.py      17      0   100%
posts/views.py            45      0   100%
users/managers.py         18      7    61%
users/serializers.py      23      0   100%
users/views.py            32      2    94%
------------------------------------------
TOTAL                    141      9    94%
----------------------------------------------------------------------
Ran 40 tests in 6.803s

OK
```

**Written by Nicholas Cannon**
