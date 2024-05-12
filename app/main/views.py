import json
from flask import render_template, redirect, url_for, abort, flash, request, \
    current_app, make_response
from . import main
from .forms import SearchCaseForm
from .utils import send_search_query


@main.route('/shutdown')
def server_shutdown():
    if not current_app.testing:
        abort(404)
    shutdown = request.environ.get('werkzeug.server.shutdown')
    if not shutdown:
        abort(500)
    shutdown()
    return 'Shutting down...'


@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@main.route('/search_cases', methods=['GET', 'POST'])
def search_cases():
    form = SearchCaseForm()
    if form.validate_on_submit():
        json_response = send_search_query(form.casename.data)

        try:
            resp = json.loads(json_response)
        except json.JSONDecodeError as e:
            flash(f'Error decoding JSON: {e}')
            return redirect(url_for('.index'))

        if resp is not None:
            return render_template('search_results.html', resp=resp, form=form)
        else:
            flash('No Search Results')
            return redirect(url_for('.index'))
    return render_template('search_cases.html', form=form)
