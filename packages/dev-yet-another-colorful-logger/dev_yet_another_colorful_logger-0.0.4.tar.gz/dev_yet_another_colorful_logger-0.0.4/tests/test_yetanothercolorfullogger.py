from yetanothercolorfullogger import YetAnotherColorfulLogger
import pytest

@pytest.fixture
def yetanothercolorfulLogger():
    return YetAnotherColorfulLogger('TEST')

def test_debug(yetanothercolorfulLogger):
    yetanothercolorfulLogger.debug("This is a debug message")

def test_info(yetanothercolorfulLogger):
    yetanothercolorfulLogger.info("This is an info message")
    
def test_warning(yetanothercolorfulLogger):
    yetanothercolorfulLogger.warning("This is a warning message")

def test_error(yetanothercolorfulLogger):
    yetanothercolorfulLogger.error("This is an error message")

def test_critical(yetanothercolorfulLogger):
    with pytest.raises(SystemExit) as exception_info:
        yetanothercolorfulLogger.critical("This is a critical message")
    assert exception_info.value.code == -1
