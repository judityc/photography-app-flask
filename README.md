# Film Photography Portfolio Platform
_Judita Cicėnaitė, Vilnius, Lithuania_

#### Video Demo:  https://youtu.be/oPBBXwUEGvY
#### Demo: https://photography-app-flask.vercel.app/

> [!WARNING]  
> This app is deployed on Vercel. Currently login functionality does not work because vercel does not support SQLite.
> TODO: use Vercel supported database.

## Description:
Film Pgotography Portfolio Website is a website created for photographer. Aim of the project is:
- Show gallery of photos taken by photographer

!([Readme-img/gallery.png](https://github.com/judityc/photography-app-flask/assets/123310773/efc38e48-2f9a-47c5-bbef-067be93798e0)) 
- Intoduce user about photographer, his worldview and aim of photography

!([Readme-img/about.png](https://github.com/judityc/photography-app-flask/assets/123310773/27d9813e-670e-4d85-a24d-345ea9c190c9))
- Write a message to photographer to book a photoshoot by leaving contacts and general message about wanted photoshoot to photograpgher

!([Readme-img/contacts.png](https://github.com/judityc/photography-app-flask/assets/123310773/73bce204-f813-48ae-80f7-4badba6062fe))

For photographer (website owner):

!([Readme-img/login.png](https://github.com/judityc/photography-app-flask/assets/123310773/c4fe310c-fdd4-447f-bc8e-2c18806cdad3))

- Read messages from users in admin page
- Upload new images to portfolio gallery page

!([Readme-img/adimin_page.png](https://github.com/judityc/photography-app-flask/assets/123310773/63d1a4b0-f7bc-4817-b675-8e02d1f6b109))

## Technologies used:
These programming languages were chosen for this project: JavaScript, CSS, HTML and Python with Flask.

Project structure:
- static/
    - libr-caslon-fontfacekit/ (font package used for website styling)
    - photos/
        - gallery/ (consists of all gallery photos uploaded by admin user and displayed in gallery.html file)
        - other photos (photos used for index.html and about.html page and website logo)
    - css files used for styling webpage:
        - `global.css` - consists of header styling used in all html pages and index.html styling
        - `form.css` - styling all form blocks in website
        - `about.css`, `admin.css`, `gallery.css` - styling files for coresponding html files
    - javascript
        - `toggleBurgerMenu()`- used in mobile web version for burger menu button, lets user to toggle button to show and hide menu list
        - `setActiveLink()` - adds "active" class list for current window nav bar for different styling
        - `refreshLoginPage()` - failure.html button "Try Again!" on click initiates page refresh
        - `fullSizeImage()` - image on click shows full size photo on window
        - `closeImage()` - on span click or on keydown esc full size photo window is closed
- templates/
    - html files:
        - `layout.html` - base stucture html file of all html pages that include website header
        - `index.html` - displays main website page
        - `galllery.html` - displays galley grid
        - `about.html` - displays article about photographer
        - `contacts.html` - displays contact message form
        - `login.html` - displays login page for admin
        - `failure.html` - displays error if users entered invalid username or password and try again button
        - `admin.html` - displays submitted contact messages for admin user and displays form for image upload
- app.py
    - consists of requred libraries and modules, application, session, upload folder configurations, database library and all app routes
    - route `/` uses `GET` method for rendering index.html tempalte
    - route `/gallery` iterates over images in upload folder checks for correct extensions and adds photo to image list which is rendered via `GET` method in gallery.html file
    - route `/about` uses `GET` method for rendering about.html tempalte
    - route `/contacts` method `POST` is used if the user submits the form, imput fields are selected and users entered information is added to database and redirected to home `/` page. `GET` method used for rendering contacts.html file
    - route `/login` is created for admin user. After clearing session via `POST` method entered username and password is checked in database, if username or password is incorret failure.html template is rendered. If login is successful admin is redirected to `/admin` route. `GET` method used for rendering login.html tempalte

    > [!NOTE]
    > For now there is only one admin user(site owner) in users database table, therefore register route does not exist. The platform is dedicated single user only

    - route `/admin` via `GET` method renders admin.html template with messeges from database and upload images form. `POST` method ensures allowed file format is selected and after secure version convertion file is added to uploas folder, admin session is cleard and admin is redirected to `/gallery` route.

    > [!NOTE]
    > `/admin` route can be accessed only after admin logins, `login_required()` is implemented

- helpers.py
    - declares `UPLOAD_FORLDER` path `'static/photos/gallery'`
    - declares `ALLOWED_EXTENSIONS` used in upload filed  `'png', 'jpg', 'jpeg', 'gif'`
    - `login_required()` -  ensures route can be reached after users login
    - `allowed_file()` - returns boolean value. Checks filename format in `ALLOWED_EXTENSIONS` object
- contacts.db
    - user table:
    ```sql
    CREATE TABLE user(
    username TEXT NOT NULL,
    hash TEXT NOT NULL);
    ```
    - contacts table:
    ```sql
    CREATE TABLE contacts (
    name TEXT NOT NULL,
    number INTEGER NOT NULL,
    email TEXT NOT NULL,
    message TEXT NOT NULL);
    ```
- requirements.txt
    - contains a list of packages and libraries needed to work on a project

## How To Run the Project:
```flask
$ flask run
```

## Login Credentials
For full admin user experiance visit route `/login`:
- username: judita
- password: cs50projectX

## Why Flask
- suitable for this type of project full stack approach that was introduced in week 9 CS50 course
- separate frontend `http-server` and backend `flask run` method was tried but due to codespace issues with cors and authorization was not pursued to implement

## Why Local Folder In Static For Photos Storage
- images in `SQL` database should be up to 2MB size. For this specific case the images are to big in size and could affect the database capacity to load photos. Therefore, before adding images to `SQL` database photos must be optimized and encoded with `base64`. Because of these reasons a local folder in project scope was chosen.

## For The Future:
- System expansion and optimization:
    - creation of register page (maybe for assistant or other admin users)
    - improve auto logout function or implement manual logout button
    - optimize uploaded images in size
    - implement ability to delete or rearrange gallery pictures for the admin user# photography-app-flask
