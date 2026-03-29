from models.report_model import add_report
from models.block_model import add_block
from models.like_model import remove_like

def report_user(reporter_id, reported_id, reason=None):
    if reporter_id == reported_id:
        raise Exception("You cannot report yourself")

    add_report(reporter_id, reported_id, reason)

    # Un report bloque automatiquement
    add_block(reporter_id, reported_id)
    remove_like(reporter_id, reported_id)
    remove_like(reported_id, reporter_id)