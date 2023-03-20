
# **[image-upload-drf-api](https://github.com/fazzkusiak/image-upload-drf-api)**

## Description
API written in DRF that allows users separated on tiers upload their own photos according to their permissions

There are 3 already built in tiers - 
*Basic* - can get 200px thumbnail.
*Premium* - same as Basic, also 400px thumbnail and source photo
*Enterprise* - same as Premium, also possibility to create temporary images.

Admin can create custom tiers.

## Executing 

1. git clone https://github.com/fazzkusiak/image-upload-drf-api
2. docker build -t images .
3. docker run -p 8000:8000 images



## Endpoints

```
/admin/
```
points to admin panel, where you can add users, tiers or view photos, expired links.
***
```
/api-auth/login/
```
points to users log in panel
***
```
/api/photos/
```
shows all images added by current logged in user and allows users to upload them
***
```
/api/links/
```
allows user to choose image and generate unique link with image that expires after given time (300 to 30000 seconds)
