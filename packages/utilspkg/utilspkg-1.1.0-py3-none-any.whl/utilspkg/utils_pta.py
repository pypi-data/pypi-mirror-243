import os
from datetime import datetime, timedelta
import pytz
import json
from slack_sdk.errors import SlackApiError
from functools import reduce

# do all of my standard imports to start a script
from utilspkg import utils_init

# creates a logger
logger = utils_init.setup_logger(__name__)

# loads ENV file when running locally
if __name__ == '__main__':
    utils_init.load_env_variables_from_yaml('/Users/croft/VScode/ptagit/env_vars.yaml')

# my custom Slack, DB, GPT, etc connections file
from utilspkg import utils_connections #, utils_times

# creates instances of my Slack, DB, GPT, etc classes
db, slack, gpt = utils_connections.get_connections()

EXCLUDED_SLACK_IDS = os.environ.get("EXCLUDED_SLACK_IDS", "")
logger.info(f"EXCLUDED_SLACK_IDS: {EXCLUDED_SLACK_IDS}")
if not EXCLUDED_SLACK_IDS:
    logger.error("EXCLUDED_SLACK_IDS not set in .env file*******")

# DB Tables
tasks_table = 'Tasks'
messages_table = 'Messages' 
channels_table = 'Slack Channels'
students_table = 'Students'
slack_users_table = 'Slack Users'
all_messages_table = 'All Messages' 
profile_pic_changed_table = 'OB-ProfilePicChangedUsers'
introduction_posted_table = 'OB-IntroductionPostedUsers'
onboarding_done_table = 'OB-OnboardingDoneUsers'
onboarding_table = "Onboarding Status"



def get_student_link(email='', slack_id=None):
    #db, slack, gpt = utils_connections.get_connections()
    filter_formula = ''
    student_records = []
    # get BOT_ALERTS_CHANNEL from env. if not available, get TESTING_CHANNEL
    bot_alerts_channel = os.getenv("BOT_ALERTS_CHANNEL")
    if not bot_alerts_channel:
        bot_alerts_channel = os.environ["TESTING_CHANNEL"]
        if not bot_alerts_channel:
            logger.error("BOT_ALERTS_CHANNEL not found in env variables. Please add it to your env variables or to the env_vars.yaml file.")
            # exit(1)

    # if we have email and it's a valid email
    if email and email.find("@") > 0 :
        filter_formula = f'FIND("{email}", {{Email - Search}})'
        # logger.error(f"Formula in get_student_link(): {filter_formula}")
    elif slack_id:
        filter_formula = f'FIND("{slack_id}", {{Slack ID}})'

    if filter_formula: #don't search if we don't have a valid filter formula
        student_records = db.get_records(students_table, formula=filter_formula)

    if len(student_records) == 0:
        # logger.error(f"No student found! {email}")
        link_to_student = []
    else:
        link_to_student = [student_records[0]['id']]
        # logger.info(f"CHALLENGER FOUND: {link_to_student}. {email}")

    # SEND MYSELF SOME WARNING MESSAGES 
    if not filter_formula:
        # that's weird. alert me
        message = f"WEIRD: No email and no slack_id sent to get_student_link just now"
        slack.send_dm_or_channel_message (bot_alerts_channel, message)

    if len(student_records) > 1:
        message = f"CS TEAM - FIX THIS: Found more than one challenger with email {email}"
        logger.warning(message)
        slack.send_dm_or_channel_message (bot_alerts_channel, message)

    return link_to_student


def add_slack_id_to_db(user_id):
    #db, slack, gpt = utils_connections.get_connections()

    # Query Slack API to fetch user's profile data
    result = slack.slack_client.users_info(user=user_id)
    new_user = result['user']
    return add_slack_user_to_db(new_user)


# adding to slack users table (not students table)
def add_slack_user_to_db (user):
    #db, slack, gpt = utils_connections.get_connections()

    profile = user.get('profile', {})
    email = profile.get('email', '').lower()
    is_email_confirmed = user.get('is_email_confirmed', False)
    slack_id = user.get('id', '')
    real_name = user.get('real_name', '')
    tz_offset = user.get('tz_offset')
    tz = user.get('tz')
    # display_name = user.get('display_name', '')
    # logger.warning("DISPLAY NAME EMPTY!") if not display_name else None
    display_name = profile.get('display_name', '')
    display_name = display_name if display_name else real_name
    raw_data = json.dumps(user)

    # Updated fields
    is_bot = user.get('is_bot', False)
    is_bot = True if slack_id in EXCLUDED_SLACK_IDS else is_bot
    custom_image = profile.get('is_custom_image', False)
    deactivated = user.get('deleted', False)

    # edit the existing record if it exists
    records = db.search_table(slack_users_table, 'Slack ID', slack_id)
    
    link_to_student_table = get_student_link(email=email) if email else [] 
    
    # if deactivated, don't link to students table (since they'll have multiple slack ids)
    if deactivated:
        link_to_student_table = []
    else:  
        # Check if record already exists with a manually matched student
        link_to_student_existing = records[0]['fields'].get('Student',[]) if records else []

        # use the existing student link if it exists (bcause we might have done it manually?)
        # if not link_to_student_table:
        if link_to_student_existing:
            link_to_student_table = link_to_student_existing

    fields = {
        'Email': email,
        'Student': link_to_student_table,
        'Confirmed Email?': is_email_confirmed,
        'Slack ID': slack_id,
        'Real Name': real_name,
        'Timezone': tz,
        'TZ Offset': tz_offset,
        'Raw Data': raw_data,
        'Ignore': is_bot,  # New field: checkbox true if user is a bot
        'Custom Profile Pic': custom_image,  # New field: checkbox true if custom image is true
        'Deactivated': deactivated,  # New field: checkbox true if "deleted" is true
        # new field - fyi in case it errors!
        'Display Name': display_name, 
    }

    if records:
        # Record exists, update the existing record
        record_id = records[0]['id']
        try:
            db.update_record(slack_users_table, record_id, fields)
            record = None
        except Exception as e:
            logger.error(f"Error updating record: {e}")
    else:
        # Record not found, insert new record
        try:
            record = db.insert_record(slack_users_table, fields)
        except Exception as e:
            logger.error(f"Error inserting record: {e}")

    return record
    

def get_challenge_start_date(optional_date=None, optional_timezone='US/Eastern'):
    """
    Unless specified, uses NOW() and US/Eastern. Returns the MONDAY start date of the current challenge as a date-only datetime object. 
    
    Optional args: 
    - date (defaults to today)
    - timezone (defaults to US/Eastern)
    """
    # in case i accidentally override the default but send nothing
    if optional_timezone is None:
        optional_timezone='US/Eastern'

    timezone = pytz.timezone(optional_timezone)

    if optional_date is None:
        optional_date = datetime.now(timezone)

    # if it's Monday, return today's date. Otherwise, return the previous Monday's date
    if optional_date.weekday() == 0:
        challenge_start_date = optional_date
    # if it's a Sunday, return tomorrow's (Monday) date
    elif optional_date.weekday() == 6:
        challenge_start_date = optional_date + timedelta(days=1)    
    else:
        challenge_start_date = optional_date - timedelta(days=optional_date.weekday())
    
    # return the date-only datetime object
    challenge_start_date = datetime(challenge_start_date.year, challenge_start_date.month, challenge_start_date.day)

    return challenge_start_date

def get_challenge_start_date_formatted(optional_date=None, optional_timezone='US/Eastern'):
    """
    Unless specified, uses NOW() and US/Eastern. Returns the MONDAY start date of the current challenge as a date-only datetime object.
    Formatted as YYYY-MM-DD

    optional args:
    - date (defaults to today)
    - timezone (defaults to US/Eastern)
    """
    startDate = get_challenge_start_date(optional_date, optional_timezone)
    return startDate.strftime("%Y-%m-%d")


def get_current_week_growth_targets_for_slack_user(slack_id):
    """
    Gets all growth targets that have been selected for the slack user for the current week
    """
    growthTargetsForUser = db.search_table('Growth Week Targets', 'Slack ID', slack_id)
    formattedStartDate = get_challenge_start_date_formatted()
    growthTargetRowForThisWeek = list(filter(lambda row: str(formattedStartDate) in row['fields'].get('Name'), growthTargetsForUser))
    hasAlreadySetTargetsForWeek = growthTargetRowForThisWeek is not None and len(growthTargetRowForThisWeek) > 0 and growthTargetRowForThisWeek[0].get('fields').get('Targets') is not None
    targetList = []

    if hasAlreadySetTargetsForWeek:
        formula = 'OR('
        for target in growthTargetRowForThisWeek[0].get('fields').get('Targets'):
            formula += f"RECORD_ID()='{target}',"    

        formula = formula[:-1] + ')'

        selectedTargets = db.get_records('Training Skills', formula=formula)
        for target in selectedTargets:
            thing = {}
            thing['id'] = target.get('id')
            thing['title'] = target.get('fields').get('Skill')
            targetList.append(thing)

    return targetList

def get_all_growth_targets_for_slack_user(slack_id):
    """
    Gets all growth targets that have been selected for the slack user
    """
    targetsResultRows = db.get_records('Growth Week Targets', formula=f"AND({{Slack ID}}='{slack_id}', {{Targets}})")
    # targetsResultRows = db.get_records('Growth Week Targets', formula=f"{{Slack ID}}='{slack_id}'")

    itemList = []
    if not targetsResultRows or len(targetsResultRows) == 0:
        logger.info(f'No targets for slack user {slack_id}')
        return itemList
    
    targetList = list(map(lambda x: x['fields']['Targets'], targetsResultRows))
    historicalSkillsForUser = list(set(reduce(lambda x, y: x + y, targetList)))
    allSkills = get_all_available_training_skills()

    historicalGrowthTargets = list(filter(lambda x: x['id'] in historicalSkillsForUser, allSkills))

    return list(map(lambda t: {"id": t['id'], "title":t['title']}, historicalGrowthTargets))

def get_all_available_training_skills():
    """
    Gets all available training skills available from Airtable
    
    """

    dbResult = db.get_records('Training Skills')

    skillList = []
    for record in dbResult:
        fields = record['fields']
        skill = {}
        skill['id'] = record.get('id')
        skill['title'] = fields.get('Skill')
        skill['shortname'] = fields.get('Skill Shortname')
        skill['notes'] = fields.get('Notes')
        skillList.append(skill)

    return skillList


def set_growth_targets_for_user(user_slack_id: str, skill_record_ids: list[str]):
    skill_record_ids = list(set(skill_record_ids))

    allSkills = get_all_available_training_skills()
    allSkillRecordIds = list(map(lambda s: s['id'], allSkills))

    # Check if all skill_record_ids exist in allSkills      
    allValid = all(skill in allSkillRecordIds for skill in skill_record_ids)
    
    if len(skill_record_ids) > 0 and not allValid:
        logger.info('Invalid record IDs. Will not continue')
        return None

    weekStartDate = get_challenge_start_date()
    formattedStartDate = weekStartDate.strftime("%Y-%m-%d")
    existingRow = db.get_records('Growth Week Targets', formula=f"AND({{Slack ID}}='{user_slack_id}', {{Formatted Start Date}}='{formattedStartDate}')")
 
    record = None
    if existingRow and len(existingRow) > 0:
        # Just Add new targets
        row = existingRow[0]
        payload = {
            "Targets": skill_record_ids
        }

        return db.update_record('Growth Week Targets', row['id'], payload)
    else: 
        studentRecord = db.get_records('Students', formula=f"{{Slack ID}}='{user_slack_id}'")[0]
        return db.insert_record("Growth Week Targets", {
            "Student": [studentRecord['id']],
            "Targets": skill_record_ids,
            "Week Start Date": weekStartDate.isoformat()
        })
    
def set_worked_on_growth_targets_for_user(user_slack_id: str, skill_record_ids: list[str]):

    skill_record_ids = list(set(skill_record_ids))

    allSkills = get_all_available_training_skills()
    allSkillRecordIds = list(map(lambda s: s['id'], allSkills))

    # Check if all skill_record_ids exist in allSkills      
    allValid = all(skill in allSkillRecordIds for skill in skill_record_ids)
    
    if len(skill_record_ids) > 0 and not allValid:
        logger.info('Invalid record IDs. Will not continue')
        return None

    weekStartDate = get_challenge_start_date()
    formattedStartDate = weekStartDate.strftime("%Y-%m-%d")
    existingRow = db.get_records('Growth Week Targets', formula=f"AND({{Slack ID}}='{user_slack_id}', {{Formatted Start Date}}='{formattedStartDate}')")
 
    record = None
    if existingRow and len(existingRow) > 0:
        # Just Add new targets
        row = existingRow[0]
        payload = {
            "Skills for this week": skill_record_ids
        }

        return db.update_record('Growth Week Targets', row['id'], payload)
    else: 
        logger.error('Row does not exist. Nothing to update.')



def add_message_to_db (event, table=messages_table, extra_fields=True, return_existing_record=False, message_ts=True):
    
    try:
        TESTING_FLAG = os.getenv("TESTING_FLAG")
        slack_id = event.get('user', '')
        logger.info(f"IN 'add message to db.' TESTING_FLAG: {TESTING_FLAG}. slack_id: {slack_id}")
        if TESTING_FLAG:
            logger.error(f"TESTING_FLAG is set to {TESTING_FLAG}. If this is in production...WHY!?.")
        # No user when it's an action response to a block. Skip it.
        if not slack_id or event.get('bot_id'):
            logger.info(f"SKIPPING: block action event (or '{event.get('bot_id')}' bot_id)")
            return None
        
        if (slack_id in EXCLUDED_SLACK_IDS or slack_id == 'USLACKBOT') and not TESTING_FLAG:
            logger.info(f"SKIPPING: MESSAGE FROM EXCLUDED BOT/USER: {slack_id}; {event.get('bot_id')}")
            return None
        
        logger.info(f"Processing message from {slack_id}...")
        
        ts = event.get('thread_ts', event.get('ts')) # IMPORTANT UPDATE MADE 8/26/23: if it's a thread, store the thread_ts instead of the ts
        if message_ts:
            ts = event.get('ts')
        channel = event.get('channel')
        logger.info(f"checking for existing message with ts: {ts}")
        # Check if the message with the same ts already exists in the Messages table
        # existing_message = db.search_table(table, 'Timestamp', ts)

        if True:
            # Find the corresponding channel and student records
            channel_records = db.search_table(channels_table, 'Channel ID', channel)
            channel_record = channel_records[0] if channel_records else None

            # student_records = db.search_table(students_table, 'Slack ID', slack_id)
            # student_record = student_records[0] if student_records else None
            slack_records = db.search_table(slack_users_table, 'Slack ID', slack_id)
            slack_record = slack_records[0] if slack_records else None
            slack_timezone = slack_record['fields'].get('Timezone','') if slack_record else None

            student_record = get_student_link (slack_id=slack_id)
            # Call the chat.getPermalink method using the slackclient (part of slack object)
            try:
                result = slack.slack_client.chat_getPermalink(channel=channel, message_ts=ts)
                permalink = result.get('permalink')
            except SlackApiError as e:
                permalink = ''
                # You will get a SlackApiError if "ok" is False
                assert e.response["ok"] is False
                assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
                logger.error(f"Got an error: {e.response['error']}")
            
            # set the has files veraible if files are attached
            has_files = True if event.get('files') else False

            # adding conditional so that my other workspace can use this function without the challenge fields
            if extra_fields:
                # need to add the challenge date to the message record
                challenge_start_date = get_challenge_start_date(optional_timezone=slack_timezone)
                logger.warning(f"Calculated challenge start date: {challenge_start_date}")

                tz_for_today = pytz.timezone(slack_timezone)
                # but need to take into account that messages posted in goal for the week and introduce yourself should be the following week if they are posted on Thursday to Saturday. (If posted Sunday, they default to next week, which is fine.)
                if channel_record and channel_record['fields'].get('Channel Name') in ['-goal-for-the-week', '--introduce-yourself']:
                    if datetime.now(tz=tz_for_today).weekday() >= 3 and datetime.now(tz=tz_for_today).weekday() <= 5:
                        challenge_start_date = challenge_start_date + timedelta(days=7)
                        logger.warning(f"Adjusted challenge start date: {challenge_start_date}")

                # formatting for airtable iso format, date only
                challenge_start_date = challenge_start_date.date().isoformat()
            
            # Add a new row to the Messages table
            new_message = {
                'Channel ID': channel,
                'Channel': [channel_record['id']] if channel_record else [],
                'Timestamp': ts,
                'Raw Data': json.dumps(event),
                'Message Link': permalink,
                'Message Text': event.get('text'),
                'Slack User': [slack_record['id']] if slack_record else [],
                'Has Files': has_files,
                'Student': student_record,
                'Slack ID': slack_id,
            }

            # adding conditional so that my other workspace can use this function without the challenge fields  
            if extra_fields:
                new_message['Challenge Date'] = challenge_start_date


            #dumb search because this isn't bolt app and flask is sending duplicate events
            existing_message = db.search_table(table, 'Timestamp', ts)

            if not existing_message:
                #logger.info(f"Airtable array to insert: {new_message}")
                new_record = db.insert_record(table, new_message)
                # new_record_id = new_record['id']
                logger.info("SUCCESS! Written to airtable")
                return new_record
            else:
                if return_existing_record:
                    return existing_message[0]
                logger.info(f"SKIPPING: MESSAGE ALREADY IN OUR DATABASE!: {ts}")
                return None
            
    except Exception as e:
        logger.error(f"**utils_pta.py - error writing to Airtable: {e}")
        raise

