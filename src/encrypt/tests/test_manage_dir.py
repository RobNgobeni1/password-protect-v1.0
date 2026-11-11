from utils.manager_dir import ManageFolder

def test_create_folder(tmp_path):
    assert ManageFolder(tmp_path).create_directory()


def test_delete_folder(tmp_path):
    assert ManageFolder(tmp_path).drop_folder()