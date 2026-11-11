from utils.delete_existing_file import DeleteFile


def test_delete_file(tmp_path):
    temp_file = tmp_path / "temporary_file.txt"
    temp_file.write_text("Test File")
    
    assert temp_file.exists()

    DeleteFile(temp_file).delete_if_exists()

    assert not temp_file.exists()
