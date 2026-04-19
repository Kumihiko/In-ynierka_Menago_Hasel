import pytest
from src.infrastructure.database import DatabaseManager

@pytest.fixture
def memory_db():
    db = DatabaseManager(":memory:")
    yield db
    db.close()

def test_database_initialization(memory_db):
    memory_db.initialize_schema()

    cursor = memory_db.connection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]
    
    assert "config" in tables
    assert "vault" in tables
    
def test_save_and_load_config(memory_db):
    memory_db.initialize_schema()
    
    memory_db.save_config("salt", b"super_tajna_sol")
    memory_db.save_config("salt", b"nowa_sol_nadpisana")
    
    loaded_salt = memory_db.get_config("salt")
    assert loaded_salt == b"nowa_sol_nadpisana"
    
    assert memory_db.get_config("brak_klucza") is None

def test_add_and_get_vault_record(memory_db):
    memory_db.initialize_schema()
    
    record_id = memory_db.add_record(
        title="Konto Bankowe",
        encrypted_login=b"enc_log",
        encrypted_password=b"enc_pass",
        record_iv=b"iv_123"
    )
    
    assert record_id == 1
    
    records = memory_db.get_all_records()
    assert len(records) == 1
    assert records[0]['title'] == "Konto Bankowe"
    assert records[0]['encrypted_password'] == b"enc_pass"