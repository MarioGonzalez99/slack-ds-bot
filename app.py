from cgitb import text
from lib2to3.pytree import Base
import os
import datetime
from slackeventsapi import SlackEventAdapter
from slack import WebClient
from flask import Flask, Response, request, json
from flask_sqlalchemy import SQLAlchemy
from views.ds_view import ds_view
from views.report_view import report_text, report_blocks

app = Flask(__name__)

app.config.from_mapping(
    SECRET_KEY=os.environ.get('SECRET_KEY') or 'dev_key',
    SQLALCHEMY_DATABASE_URI=os.environ.get(
        'DATABASE_URL').replace("://", "ql://", 1),
    SQLALCHEMY_TRACK_MODIFICATIONS=False
)


db = SQLAlchemy(app)

# DB Models


class User(db.Model):
    id = db.Column(db.String(100), primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    dailys = db.relationship('DailyStandup', back_populates='user')


class DailyStandup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    yesterday_question = db.Column(db.String(3000), nullable=False)
    today_question = db.Column(db.String(3000), nullable=False)
    blockers_question = db.Column(db.String(3000), nullable=False)
    user_id = db.Column(db.String(100), db.ForeignKey(
        'user.id'), nullable=False)
    user = db.relationship('User', back_populates='dailys')

# Helper functions for DB operations


def check_if_user_in_db(user_id):
    return False if User.query.get(user_id) is None else True


def convert_string_to_date(date_text):
    try:
        return datetime.datetime.strptime(date_text, '%Y-%m-%d')
    except ValueError:
        raise ValueError('Incorrect data format, should be YYYY-MM-DD')


def get_dailys_by_date(date):
    return DailyStandup.query.filter_by(date=date).all()


# Slack objects


slack_web_client = WebClient(token=os.environ.get('SLACK_TOKEN'))

slack_events_adapter = SlackEventAdapter(os.environ.get(
    'SIGNING_SECRET'), '/slack/events', app)


# Endpoints routes


@app.route('/')
def entry_point():
    return {
        'status': 'ok',
        'version': '1.0'
    }, 200


@app.route('/slack/daily-standup', methods=['POST'])
def daily_standup():
    data = request.form
    trigger_id = data.get('trigger_id')
    view = ds_view
    slack_web_client.views_open(trigger_id=trigger_id, view=view)
    return Response(), 200


@app.route('/slack/ds-submissions', methods=['POST'])
def submissions():
    data = request.form.to_dict()
    data_parsed = json.loads(data['payload'])
    user_id = data_parsed['user']['id']
    username = data_parsed['user']['username']
    date = data_parsed['view']['state']['values']['date-block']['date-action']['selected_date']
    yesterday_question = data_parsed['view']['state']['values']['yesterday-block']['yesterday-action']['value']
    today_question = data_parsed['view']['state']['values']['today-block']['today-action']['value']
    blockers_question = data_parsed['view']['state']['values']['blockers-block']['blockers-action']['value']
    user_in_db = check_if_user_in_db(user_id)
    if not user_in_db:
        new_user = User(id=user_id, username=username)
        db.session.add(new_user)

    new_daily = DailyStandup(date=date, yesterday_question=yesterday_question,
                             today_question=today_question, blockers_question=blockers_question, user_id=user_id)
    db.session.add(new_daily)
    db.session.commit()
    return Response(), 200


@app.route('/slack/ds-reports', methods=['POST'])
def reports():
    try:
        data = request.form
        channel_id = data.get('channel_id')
        date_text = data.get('text')
        if not date_text:
            date_parsed = datetime.date.today()
            date_text = str(date_parsed)
        else:
            date_parsed = convert_string_to_date(date_text)
        dailys = get_dailys_by_date(date_parsed)
        blocks = report_blocks(dailys)
        report = report_text(blocks=blocks, date=date_text,
                             channel_id=channel_id)
        slack_web_client.chat_postMessage(**report)
    except ValueError as err:
        app.logger.error(msg=err, exc_info=1)
        slack_web_client.chat_postMessage(
            channel=channel_id, text=f':no_good: Could not generate Daily Standup Report: {err}')
        return Response(), 200
    except BaseException as err:
        app.logger.error(msg=err, exc_info=1)
        return Response(), 400

    return Response(), 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
