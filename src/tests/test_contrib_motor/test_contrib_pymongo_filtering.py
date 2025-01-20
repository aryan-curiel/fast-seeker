from fast_seeker.contrib.motor.filtering import MotorFilterer


def test_motor_filterer_default_resolver__should_return_valid_dict():
    filterer = MotorFilterer()
    translated_args = filterer.default_resolver(None, None, "field", "value")
    assert translated_args == {"field": "value"}


def test_motor_filterer_execute__should_return_filtered_queryset(motor_collection):
    filterer = MotorFilterer()
    expressions = [{"field": "value"}]
    filterer.execute(motor_collection, expressions)
    motor_collection.find.assert_called_once_with(*expressions)
