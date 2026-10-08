"""F3_drive_public.py — Sirf public."""
def make_public(service, file_id):
    try:
        service.permissions().create(
            fileId=file_id,
            body={"type": "anyone", "role": "reader"}).execute()
        return True
    except Exception:
        return False
