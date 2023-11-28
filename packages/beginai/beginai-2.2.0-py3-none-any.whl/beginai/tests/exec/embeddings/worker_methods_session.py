from freezegun import freeze_time
from .mock_service import BeginWorkerMock
import datetime

APP_ID = 1
LICENSE_KEY = 10


@freeze_time("2021-05-16")
def test_start_session_when_no_session_exists():
    bw = BeginWorkerMock(APP_ID, LICENSE_KEY)

    bw.register_user("123")

    bw.start_session()

    session_data = bw.get_data()['session_raw_data']

    formatted_date = '16-05-2021'
    
    assert len(session_data) == 1
    assert len(session_data[formatted_date]) == 1
    assert session_data[formatted_date][0]["start"] == datetime.datetime.now(datetime.timezone.utc)
    assert session_data[formatted_date][0]["end"] == None

@freeze_time("2021-05-16")
def test_start_session_dont_add_anything_if_session_is_already_happening():
    bw = BeginWorkerMock(APP_ID, LICENSE_KEY)

    bw.register_user("123")

    bw.start_session()

    # "Starts 2nd session"
    bw.start_session()

    session_data = bw.get_data()['session_raw_data']

    formatted_date = '16-05-2021'
    
    assert len(session_data) == 1
    assert len(session_data[formatted_date]) == 1
    assert session_data[formatted_date][0]["start"] == datetime.datetime.now(datetime.timezone.utc)
    assert session_data[formatted_date][0]["end"] == None

@freeze_time("2021-05-16")
def test_start_session_on_two_days():
    bw = BeginWorkerMock(APP_ID, LICENSE_KEY)

    bw.set_data({
        "session_raw_data": {
            "15-05-2021": [{
                "start": None,
                "end": None
            }]
        },
        "user": {
            "1234": []
        }
    })

    # "Starts 2nd session"
    bw.start_session()

    session_data = bw.get_data()['session_raw_data']

    formatted_date = '16-05-2021'
    
    assert len(session_data) == 2
    assert len(session_data[formatted_date]) == 1
    assert session_data[formatted_date][0]["start"] == datetime.datetime.now(datetime.timezone.utc)
    assert session_data[formatted_date][0]["end"] == None

@freeze_time("2021-05-16")
def test_start_session_on_same_day_when_another_session_finished():
    bw = BeginWorkerMock(APP_ID, LICENSE_KEY)

    date = datetime.datetime.now(datetime.timezone.utc)

    bw.set_data({
        "session_raw_data": {
            "16-05-2021": [{
                "start": date,
                "end": date
            }]
        },
        "user": {
            "123": []
        }
    })

    # "Starts 2nd session"
    bw.start_session()

    session_data = bw.get_data()['session_raw_data']

    formatted_date = '16-05-2021'
    
    assert len(session_data) == 1
    assert len(session_data[formatted_date]) == 2
    assert session_data[formatted_date][0]["start"] == date
    assert session_data[formatted_date][0]["end"] == date
    assert session_data[formatted_date][1]["start"] == date
    assert session_data[formatted_date][1]["end"] == None

@freeze_time("2021-05-16")
def test_end_session_when_there_is_one_session_open_and_one_day():
    bw = BeginWorkerMock(APP_ID, LICENSE_KEY)

    date = datetime.datetime.now(datetime.timezone.utc)

    bw.register_user("123")

    bw.start_session()
    bw.end_session()

    session_data = bw.get_data()['session_raw_data']

    formatted_date = '16-05-2021'
    
    assert len(session_data) == 1
    assert len(session_data[formatted_date]) == 1
    assert session_data[formatted_date][0]["start"] == date
    assert session_data[formatted_date][0]["end"] == date

@freeze_time("2021-05-16")
def test_end_session_when_there_is_two_sessions_on_the_same_day():
    bw = BeginWorkerMock(APP_ID, LICENSE_KEY)

    date = datetime.datetime.now(datetime.timezone.utc)
    bw.register_user("123")

    bw.start_session()
    bw.end_session()

    # 2nd session on the same day
    bw.start_session()
    bw.end_session()

    session_data = bw.get_data()['session_raw_data']

    formatted_date = '16-05-2021'
    
    assert len(session_data) == 1
    assert len(session_data[formatted_date]) == 2
    assert session_data[formatted_date][0]["start"] == date
    assert session_data[formatted_date][0]["end"] == date 
    assert session_data[formatted_date][1]["start"] == date
    assert session_data[formatted_date][1]["end"] == date    

@freeze_time("2021-05-16")
def test_end_session_when_no_start_session_for_that_date():
    bw = BeginWorkerMock(APP_ID, LICENSE_KEY)

    bw.end_session()

    session_data = bw.get_data()['session_raw_data']
    
    assert len(session_data) == 0

@freeze_time("2021-05-16")
def test_end_session_when_no_session_left_open():
    bw = BeginWorkerMock(APP_ID, LICENSE_KEY)

    bw.register_user("123")

    bw.start_session()
    bw.end_session()

    # Nothing to end here
    bw.end_session()

    formatted_date = '16-05-2021'

    session_data = bw.get_data()['session_raw_data']

    date = datetime.datetime.now(datetime.timezone.utc)
    
    assert len(session_data) == 1
    assert len(session_data[formatted_date]) == 1
    assert session_data[formatted_date][0]["start"] == date
    assert session_data[formatted_date][0]["end"] == date 

