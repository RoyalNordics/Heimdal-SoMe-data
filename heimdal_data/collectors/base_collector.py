from abc import ABC, abstractmethod
from datetime import datetime
import logging
from typing import Dict, List, Any, Optional
import os
from pathlib import Path

# Create logs directory if it doesn't exist
logs_dir = Path(os.path.dirname(os.path.abspath(__file__))).parent / "logs"
logs_dir.mkdir(exist_ok=True)

# Log file path
log_file = logs_dir / "data_collection.log"

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)

class BaseCollector(ABC):
    """
    Base class for all data collectors.
    """
    
    def __init__(self, name: str):
        """
        Initialize the collector.
        
        Args:
            name (str): Name of the collector.
        """
        self.name = name
        self.logger = logging.getLogger(f"collector.{name}")
        self.logger.info(f"Initializing {name} collector")
    
    @abstractmethod
    async def collect(self) -> List[Dict[str, Any]]:
        """
        Collect data from the source.
        
        Returns:
            List[Dict[str, Any]]: List of collected data items.
        """
        pass
    
    @abstractmethod
    async def save(self, data: List[Dict[str, Any]]) -> bool:
        """
        Save the collected data to the database.
        
        Args:
            data (List[Dict[str, Any]]): List of data items to save.
            
        Returns:
            bool: True if the data was saved successfully, False otherwise.
        """
        pass
    
    async def run(self) -> bool:
        """
        Run the collector: collect data and save it to the database.
        
        Returns:
            bool: True if the collection and saving was successful, False otherwise.
        """
        try:
            self.logger.info(f"Starting data collection for {self.name}")
            start_time = datetime.now()
            
            # Collect data
            data = await self.collect()
            if not data:
                self.logger.warning(f"No data collected from {self.name}")
                return False
            
            self.logger.info(f"Collected {len(data)} items from {self.name}")
            
            # Save data
            success = await self.save(data)
            if not success:
                self.logger.error(f"Failed to save data from {self.name}")
                return False
            
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            self.logger.info(f"Data collection for {self.name} completed in {duration:.2f} seconds")
            
            return True
        except Exception as e:
            self.logger.exception(f"Error in {self.name} collector: {e}")
            return False
