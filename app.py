#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for, abort
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
import sys
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# TODO: connect to a local postgresql database

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#


class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    artist_id = db.Column(db.Integer, db.ForeignKey(
        'Artist.id'))
    artist = db.relationship('Artist', backref='artist', lazy=True)

    # TODO: implement any missing fields, as a database migration using Flask-Migrate


class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    venue_id = db.Column(db.Integer, db.ForeignKey(
        'Venue.id'))
    venue = db.relationship('Venue', backref='venue', lazy=True)

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#


def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format, locale='en')


app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#


@app.route('/')
def index():
    dataList = []
    try:
        fetchedData = Show.query.order_by(db.desc(Show.start_time))
        for data in fetchedData:
            dataList.append({
                'artist_id': data.artist_id,
                'artist_name': data.artists.name,
                'artist_image_link': data.artists.image_link,
                'artist_state': data.artists.state,
                'venue_id': data.venue_id,
                'venue_name': data.venues.name,
                'venue_image_link': data.venues.image_link,
                'venue_state':data.venues.state
            })
        db.session.commit()
    except:
        db.session.rollback()
        error = True
        print(sys.exc_info)
    finally:
        db.session.close()
    if error:
        abort(500)
    else:
        return render_template('pages/home.html', show=dataList)


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
    # TODO: replace with real venues data.
    #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
    data = []
    try:
        data = Venue.query.all()
        db.session.commit()
    except:
        db.session.rollback()
        error = True
        print(sys.exc_info)
    finally:
        db.session.close()
    if error:
        abort(500)
    else:
        return render_template('pages/venues.html', areas=data)


@app.route('/venues/search', methods=['POST'])
def search_venues():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for Hop should return "The Musical Hop".
    # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
    response = ''
    try:
        response = request.get_json()['search_term']
        db.session.commit()
    except:
        db.session.rollback()
        error = True
        print(sys.exc_info)
    finally:
        db.session.close()
    if error:
        abort(500)
    else:
        return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    # shows the venue page with the given venue_id
    # TODO: replace with real venue data from the venues table, using venue_id
    data = []
    try:
        data = Venue.query.get(venue_id)
        db.session.commit()
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
        if error == True:
            abort(400)
        else:
            return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------


@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    # TODO: insert form data as a new Venue record in the db, instead
    # TODO: modify data to be the data object returned from db insertion

    # on successful db insert, flash success
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/

    body = {}
    error = False
    try:
        name = request.get_json()['name']
        city = request.get_json()['city']
        state = request.get_json()['state']
        address = request.get_json()['address']
        phone = request.get_json()['phone']
        image_link = request.get_json()['image_link']
        facebook_link = request.get_json()['facebook_link']
        artist_id = request.get_json()['artist_id']
        venue = Venue(name=name, artist_id=artist_id, city=city, state=state, address=address,
                      phone=phone, image_link=image_link, facebook_link=facebook_link,)
        body['name'] = venue.name
        body['city'] = venue.city
        body['state'] = venue.state
        body['address'] = venue.address
        body['phone'] = venue.phone
        body['image_link'] = venue.image_link
        body['facebook_link'] = venue.facebook_link
        db.session.add(venue)
        db.session.commit()
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        flash('Venue ' + request.form['name'] + ' was successfully listed!')
        db.session.close()
        if error == True:
            flash('An error occurred. Venue ' +
                  body.name + ' could not be listed.')
            abort(400)
        else:
            return jsonify(body)


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    # TODO: Complete this endpoint for taking a venue_id, and using
    # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

    # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
    # clicking that button delete it from the db then redirect the user to the homepage
    try:
        venue = Venue.query.get(venue_id)
        db.session.delete(venue)
        db.session.commit()
    except:
        db.session.rollback()
        error = True
    finally:
        db.session.close()
    if error:
        abort(500)
    else:
        return redirect(url_for('index'))

#  Artists
#  ----------------------------------------------------------------


@app.route('/artists')
def artists():
    # TODO: replace with real data returned from querying the database
    data = []
    try:
        data = Artist.query.all()
        db.session.commit()
    except:
        db.session.rollback()
        error = True
        print(sys.exc_info)
    finally:
        db.session.close()
    if error:
        abort(500)
    else:
        return render_template('pages/artists.html', artists=data)


@app.route('/artists/search', methods=['POST'])
def search_artists():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
    # search for "band" should return "The Wild Sax Band".
    response = ''
    try:
        response = request.get_json()['search_term']
        db.session.commit()
    except:
        db.session.rollback()
        error = True
        print(sys.exc_info)
    finally:
        db.session.close()
    if error:
        abort(500)
    else:
        return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    # shows the artist page with the given artist_id
    # TODO: replace with real artist data from the artist table, using artist_id
    singleArtist = []
    try:
        singleArtist = Artist.query.get(artist_id)
        db.session.commit()
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
        if error == True:
            abort(400)
        else:
            data = list(filter(lambda d: d['id']
                        == artist_id, singleArtist))[0]
            return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------


@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    form = ArtistForm()
    artist = []
    try:
        artist = Artist.query.get(artist_id)
        for fields in form:
            if fields != '':
                artist[0].fields = fields
            else:
                return
        db.session.add(artist)
        db.session.commit()
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
        if error == True:
            abort(400)
        else:
            # TODO: populate form with fields from artist with ID <artist_id>
            return render_template('forms/edit_artist.html', form=form, artist=artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    # TODO: take values from the form submitted, and update existing
    # artist record with ID <artist_id> using the new attributes
    artist = []
    try:
        artist = Artist.query.get(artist_id)
        for fields in artist:
            if fields != '':
                artist[0].fields = fields
            else:
                return
        db.session.add(artist)
        db.session.commit()
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
        if error == True:
            abort(400)
        else:
            return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    form = VenueForm()
    venue = []
    try:
        venue = Venue.query.get(venue_id)
        for fields in form:
            if fields != '':
                venue[0].fields = fields
            else:
                return
        db.session.add(venue)
        db.session.commit()
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
        if error == True:
            abort(400)
        else:
            # TODO: populate form with values from venue with ID <venue_id>
            return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    # TODO: take values from the form submitted, and update existing
    venue = []
    try:
        venue = Venue.query.get(venue_id)
        for fields in venue:
            if fields != '':
                venue[0].fields = fields
            else:
                return
        db.session.add(venue)
        db.session.commit()
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
        if error == True:
            abort(400)
        else:
            # venue record with ID <venue_id> using the new attributes
            return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------


@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    # called upon submitting the new artist listing form
    # TODO: insert form data as a new Venue record in the db, instead
    # TODO: modify data to be the data object returned from db insertion
    body = {}
    error = False
    try:
        name = request.get_json()['name']
        city = request.get_json()['city']
        genres = request.get_json()['genres']
        website_link = request.get_json()['website_link']
        phone = request.get_json()['phone']
        image_link = request.get_json()['image_link']
        facebook_link = request.get_json()['facebook_link']
        seeking_description = request.get_json()['seeking_description']
        seeking_venue = request.get_json()['seeking_venue']
        venue = Venue(name=name, city=city, genres=genres, website_link=website_link,
                      phone=phone, image_link=image_link, facebook_link=facebook_link, seeking_description=seeking_description, seeking_venue=seeking_venue)
        body['name'] = venue.name
        body['city'] = venue.city
        body['genres'] = venue.genres
        body['phone'] = venue.phone
        body['website_link'] = venue.website_link
        body['image_link'] = venue.image_link
        body['facebook_link'] = venue.facebook_link
        body['seeking_venue'] = venue.seeking_venue
        body['seeking_description'] = venue.seeking_description
        db.session.add(body)
        db.session.commit()
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        flash('Artist ' + request.form['name'] + ' was successfully listed!')
        db.session.close()
        if error == True:
            flash('An error occurred. Artist ' +
                  body.name + ' could not be listed.')
            abort(400)
        else:
            # on successful db insert, flash success
            # TODO: on unsuccessful db insert, flash an error instead.
            # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
            return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
    # displays list of shows at /shows
    # TODO: replace with real venues data.
    data = []
    try:
        data = Venue.query.order_by('id').all()
        db.session.commit()
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
        if error == True:
            abort(400)
        else:
            return render_template('pages/shows.html', shows=data)


@app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    # called to create new shows in the db, upon submitting new show listing form
    # TODO: insert form data as a new Show record in the db, instead
    body = {}
    error = False
    try:
        artist_id = request.get_json()['artist_id']
        venue_id = request.get_json()['venue_id']
        start_time = request.get_json()['start_time']
        shows = Venue(artist_id=artist_id, venue_id=venue_id,
                      start_time=start_time)
        body['artist_id'] = shows.artist_id
        body['venue_id'] = shows.venue_id
        body['start_time'] = shows.start_time
        db.session.add(shows)
        db.session.commit()
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        flash('Show was successfully listed!')
        db.session.close()
        if error == True:
            flash('An error occurred. Show could not be listed.')
            abort(400)
        else:
            # on successful db insert, flash success
            # TODO: on unsuccessful db insert, flash an error instead.
            # e.g., flash('An error occurred. Show could not be listed.')
            # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
            return render_template('pages/home.html')


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
