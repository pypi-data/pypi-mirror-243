# Version
from ._version import __version__

# API info functions
from .client import (
    set_api_key,
    set_server_url,
    get_api_key,
    get_server_url,
    get_user_information,
    get_versions,
)

# API dataset functions
from .client import (
    upload_dataset,
    list_datasets,
    query_dataset,
    view_dataset,
    delete_dataset,
)

# API campaign functions
from .client import (
    train_campaign,
    list_campaigns,
    query_campaign,
    view_campaign,
    predict_campaign,
    sample_campaign,
    active_learn_campaign,
    solve_inverse_campaign,
    optimise_campaign,
    score_campaign,
    get_calibration_curve_campaign,
    delete_campaign,
)
