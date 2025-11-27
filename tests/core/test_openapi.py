from fastapi import FastAPI

from app.core.openapi import set_openapi_generator


def test_set_openapi_generator() -> None:
    """Test set_openapi_generator attaches the function."""
    app = FastAPI()
    set_openapi_generator(app)

    # The app.openapi attribute should be a bound method or partial
    # We can verify that calling app.openapi() returns a schema
    schema = app.openapi()
    assert schema is not None
    assert schema["openapi"] == "3.1.0"

    # Call it again to test caching (line 70 coverage)
    schema2 = app.openapi()
    assert schema2 is schema
