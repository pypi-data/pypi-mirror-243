"""
gam_purification.models

Model-specific implementations of purification.
"""

from gam_purification.models.ebm import purify_and_update, purify_ebm, update_ebm
from gam_purification.models.xgb import get_mains_and_pairs