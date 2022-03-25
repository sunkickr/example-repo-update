"""Test the validity of all DAGs. **USED BY DEV PARSE COMMAND DO NOT EDIT**"""
from contextlib import contextmanager
import logging
import os

import pytest

from airflow.models import DagBag, Variable
from airflow.hooks.base import BaseHook


# The following code patches errors caused by missing OS Variables, Airflow Connections, and Airflow Variables

# =========== MONKEYPATCH BaseHook.get_connection() ===========
def basehook_get_connection_monkeypatch(key: str):
    print(f"user tried fetching connection {key}")


BaseHook.get_connection = basehook_get_connection_monkeypatch
# # =========== /MONKEYPATCH BASEHOOK.GET_CONNECTION() ===========

# =========== MONKEYPATCH OS.GETENV() ===========
def os_getenv_monkeypatch(key: str, default=None):
    print(f"user tried fetching var {key}")


os.getenv = os_getenv_monkeypatch
# # =========== /MONKEYPATCH OS.GETENV() ===========

# =========== MONKEYPATCH VARIABLE.GET() ===========
def variable_get_monkeypatch(key: str):
    print(f"user tried fetching var {key}")


Variable.get = variable_get_monkeypatch
# # =========== /MONKEYPATCH VARIABLE.GET() ===========


@contextmanager
def suppress_logging(namespace):
	"""
	Suppress logging within a specific namespace to keep tests "clean" during build
	"""
	logger = logging.getLogger(namespace)
	old_value = logger.disabled
	logger.disabled = True
	try:
		yield
	finally:
		logger.disabled = old_value

def get_import_errors():
	"""
	Generate a tuple for import errors in the dag bag
	"""
	with suppress_logging('airflow') :
		dag_bag = DagBag(include_examples=False)

		def strip_path_prefix(path):
			return os.path.relpath(path ,os.environ.get('AIRFLOW_HOME'))

		
		# we prepend "(None,None)" to ensure that a test object is always created even if its a no op.
		return [(None,None)] +[ ( strip_path_prefix(k) , v.strip() ) for k,v in dag_bag.import_errors.items()]

	
@pytest.mark.parametrize("rel_path,rv", get_import_errors(), ids=[x[0] for x in get_import_errors()])
def test_file_imports(rel_path,rv):
	""" Test for import errors on a file """
	if rel_path and rv : #Make sure our no op test doesn't raise an error
		raise Exception(f"{rel_path} failed to import with message \n {rv}")