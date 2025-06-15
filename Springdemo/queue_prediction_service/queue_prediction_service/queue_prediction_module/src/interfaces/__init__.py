"""
接口模块
"""

from .prediction_api import PredictionAPI, PredictionAPIError
from .data_interface import (
    DatabaseInterface, 
    ExternalDataInterface, 
    DataAdapter, 
    DataInterfaceError
)

__all__ = [
    'PredictionAPI',
    'PredictionAPIError',
    'DatabaseInterface',
    'ExternalDataInterface', 
    'DataAdapter',
    'DataInterfaceError'
] 