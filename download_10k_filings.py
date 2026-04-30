"""Script to download 10-K filings organized by sector."""

from src.data_loaders.SEC_downloader import SECDownloader
from src.config_loader import load_config
from pathlib import Path


def main():
    """Download 10-K filings for all companies."""
    # Load configuration
    edgar_config = load_config('config/edgar_config.yaml')

    # Set paths
    yaml_config = Path('config/companies_list.yaml')
    output_dir = Path('data/raw/filings')

    # Get user agent from config
    user_agent = edgar_config['edgar']['user_agent']

    # Initialize downloader
    downloader = SECDownloader(
        yaml_config_path=yaml_config,
        base_output_path=output_dir
    )

    # Download filings
    print("Starting 10-K filings download...")
    print(f"Output directory: {output_dir}\n")
    downloader.download_10k_filings(user_agent=user_agent)
    print("\nDownload complete!")


if __name__ == "__main__":
    main()
