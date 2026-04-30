import yaml
import os
from pathlib import Path
from secedgar import filings, FilingType


class SECDownloader:
    """Download 10-K filings from SEC EDGAR by sector."""

    def __init__(self, yaml_config_path, base_output_path):
        """
        Initialize downloader.

        Args:
            yaml_config_path: Path to companies_list.yaml
            base_output_path: Base directory for saving filings
        """
        self.yaml_config_path = yaml_config_path
        self.base_output_path = Path(base_output_path)
        self.companies = self._load_companies()

    def _load_companies(self):
        """Load companies from YAML config file."""
        with open(self.yaml_config_path, 'r') as file:
            data = yaml.safe_load(file)
        return data['companies']

    def _create_sector_folders(self):
        """Create folders for each sector."""
        for sector in self.companies.keys():
            sector_path = self.base_output_path / sector
            if sector_path.exists():
                print(f"Folder already exists: {sector_path}")
            else:
                sector_path.mkdir(parents=True, exist_ok=True)
                print(f"  Created folder: {sector_path}")

    def download_10k_filings(self, user_agent):
        """
        Download 10-K filings for all companies organized by sector.

        Args:
            user_agent: User agent string for SEC API (required)
        """
        self._create_sector_folders()

        for sector, companies in self.companies.items():
            sector_path = self.base_output_path / sector
            print(f"\nDownloading 10-K filings for {sector}")

            for company in companies:
                name = company['name']
                cik = company['cik']

                try:
                    company_path = sector_path / name
                    print(f"  Downloading {name} (CIK: {cik})...")

                    sec_filing = filings.Filing(
                        cik=cik,
                        filing_type=FilingType.FILING_10K,
                        user_agent=user_agent
                    )
                    sec_filing.save(company_path)
                    print(f"Saved to {company_path}")

                except Exception as e:
                    print(f"Error downloading {name}: {str(e)}") 
          