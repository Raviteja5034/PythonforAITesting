from backend.manifest import save_manifest, changed_files


def test_manifest_round_trip(tmp_path):
    manifest_path = tmp_path / 'manifest.json'
    data = {'a.txt': {'sha256': '123', 'chunk_count': 2}}
    save_manifest(data, str(manifest_path))
    from backend.manifest import load_manifest
    assert load_manifest(str(manifest_path)) == data


def test_changed_files_detects_add_modify_delete(tmp_path):
    docs = tmp_path / 'docs'
    docs.mkdir()
    (docs / 'a.txt').write_text('hello', encoding='utf-8')

    result = changed_files({}, str(docs), {'.txt'}, [])
    assert len(result['added']) == 1

    manifest = {
        'a.txt': {
            'relative_path': 'a.txt',
            'sha256': result['added'][0]['sha256'],
        },
        'gone.txt': {
            'relative_path': 'gone.txt',
            'sha256': 'x',
        }
    }
    (docs / 'a.txt').write_text('hello updated', encoding='utf-8')
    result2 = changed_files(manifest, str(docs), {'.txt'}, [])
    assert len(result2['modified']) == 1
    assert len(result2['deleted']) == 1


def test_changed_files_detects_rename_as_delete_plus_add(tmp_path):
    docs = tmp_path / 'docs'
    docs.mkdir()
    old_file = docs / 'old.txt'
    old_file.write_text('hello', encoding='utf-8')
    first = changed_files({}, str(docs), {'.txt'}, [])
    manifest = {
        'old.txt': {
            'relative_path': 'old.txt',
            'sha256': first['added'][0]['sha256'],
        }
    }

    old_file.rename(docs / 'renamed.txt')
    result = changed_files(manifest, str(docs), {'.txt'}, [])
    assert len(result['added']) == 1
    assert result['added'][0]['relative_path'] == 'renamed.txt'
    assert len(result['deleted']) == 1
    assert result['deleted'][0]['relative_path'] == 'old.txt'
