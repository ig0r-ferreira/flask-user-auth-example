from flask.testing import FlaskCliRunner


def test_init_db(runner: FlaskCliRunner, monkeypatch):
    class Recorder:
        called = False

    def fake_create_tables():
        Recorder.called = True

    monkeypatch.setattr(
        'flask_user_auth.commands.create_tables', fake_create_tables
    )
    with runner.app.app_context():
        result = runner.invoke(args=['init-db'])

    assert 'Initialized' in result.output
    assert Recorder.called
