# I Was There - TESTING

## Bugs

### Fixed Bugs

- Static Files: During the development I had a hard time with staticfiles as they were not loading on Cloudinary. After watching the new CI Django Blog video, I installed whitenoise. Still had the same issue. After some attempts, I fixed the issue with the help of these two links: 
    - Changing the order of the INSTALLED_APPS on settings.py: [https://pypi.org/project/dj3-cloudinary-storage/](https://pypi.org/project/dj3-cloudinary-storage/).
    - Collecting static folder running python3 manage.py collectstatic [StackOverflow](https://stackoverflow.com/questions/69077368/in-django-whitenoise-do-not-show-static-files)