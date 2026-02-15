# -*- coding: utf-8 -*-
"""
Integration tests for darwinex_ticks package.
These tests require real Darwinex FTP credentials.

Run with:
    DARWINEX_USER=xxx DARWINEX_PASS=xxx DARWINEX_HOST=xxx pytest tests/test_integration.py -v
    
Or set credentials in environment before running.
"""

import os
import sys
import pytest

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def get_credentials():
    """Get credentials from environment or return None."""
    return {
        'user': os.environ.get('DARWINEX_USER'),
        'pass': os.environ.get('DARWINEX_PASS'),
        'host': os.environ.get('DARWINEX_HOST', 'tickdata.darwinex.com'),
    }


@pytest.fixture
def darwinex_credentials():
    """Fixture to get Darwinex credentials."""
    creds = get_credentials()
    if not creds['user'] or not creds['pass']:
        pytest.skip("Darwinex credentials not provided. Set DARWINEX_USER and DARWINEX_PASS environment variables.")
    return creds


class TestDarwinexIntegration:
    """Integration tests with real Darwinex FTP server."""

    def test_connection_and_list_assets(self, darwinex_credentials):
        """Test connection to Darwinex and listing assets."""
        from darwinex_ticks import DarwinexTicksConnection
        
        conn = DarwinexTicksConnection(
            dwx_ftp_user=darwinex_credentials['user'],
            dwx_ftp_pass=darwinex_credentials['pass'],
            dwx_ftp_hostname=darwinex_credentials['host']
        )
        
        # Should have some assets available
        assert len(conn.available_assets) > 0
        
        # Common forex pairs should be available
        assets = conn.available_assets
        print(f"Available assets: {assets[:10]}...")  # Print first 10
        
        conn.close()

    def test_list_files_for_asset(self, darwinex_credentials):
        """Test listing files for a specific asset."""
        from darwinex_ticks import DarwinexTicksConnection
        
        conn = DarwinexTicksConnection(
            dwx_ftp_user=darwinex_credentials['user'],
            dwx_ftp_pass=darwinex_credentials['pass'],
            dwx_ftp_hostname=darwinex_credentials['host']
        )
        
        # Try EURUSD
        files = conn.list_of_files('EURUSD')
        
        assert len(files) > 0
        assert 'file' in files.columns
        
        conn.close()

    def test_download_ticks_data(self, darwinex_credentials):
        """Test downloading real tick data."""
        from darwinex_ticks import DarwinexTicksConnection
        
        conn = DarwinexTicksConnection(
            dwx_ftp_user=darwinex_credentials['user'],
            dwx_ftp_pass=darwinex_credentials['pass'],
            dwx_ftp_hostname=darwinex_credentials['host']
        )
        
        # Download a small time range
        data = conn.ticks_from_darwinex(
            'EURUSD',
            start='2024-01-01 08',
            end='2024-01-01 09'
        )
        
        # Should have some data
        assert len(data) > 0
        
        # Should have Ask and Bid columns
        assert 'Ask' in data.columns or 'Bid' in data.columns
        
        conn.close()

    def test_download_multiple_assets(self, darwinex_credentials):
        """Test downloading data for multiple assets."""
        from darwinex_ticks import DarwinexTicksConnection
        
        conn = DarwinexTicksConnection(
            dwx_ftp_user=darwinex_credentials['user'],
            dwx_ftp_pass=darwinex_credentials['pass'],
            dwx_ftp_hostname=darwinex_credentials['host']
        )
        
        # Download two assets
        data = conn.ticks_from_darwinex(
            ['EURUSD', 'GBPUSD'],
            start='2024-01-01 08',
            end='2024-01-01 09'
        )
        
        # Should have both assets
        assert 'EURUSD' in data.columns.get_level_values(0)
        assert 'GBPUSD' in data.columns.get_level_values(0)
        
        conn.close()

    def test_spread_function_on_real_data(self, darwinex_credentials):
        """Test spread function on real downloaded data."""
        from darwinex_ticks import DarwinexTicksConnection, spread
        
        conn = DarwinexTicksConnection(
            dwx_ftp_user=darwinex_credentials['user'],
            dwx_ftp_pass=darwinex_credentials['pass'],
            dwx_ftp_hostname=darwinex_credentials['host']
        )
        
        data = conn.ticks_from_darwinex(
            'EURUSD',
            start='2024-01-01 10',
            end='2024-01-01 11',
            fill=True
        )
        
        # Calculate spread
        spreads = spread(data)
        
        # Should have calculated values
        assert len(spreads) > 0
        assert spreads.max() > 0  # Spread should be positive
        
        conn.close()

    def test_darwinex_time_conversion(self, darwinex_credentials):
        """Test Darwinex time zone conversion."""
        from darwinex_ticks import DarwinexTicksConnection, to_darwinex_time
        
        conn = DarwinexTicksConnection(
            dwx_ftp_user=darwinex_credentials['user'],
            dwx_ftp_pass=darwinex_credentials['pass'],
            dwx_ftp_hostname=darwinex_credentials['host']
        )
        
        data = conn.ticks_from_darwinex(
            'EURUSD',
            start='2024-01-01 14',
            end='2024-01-01 15',
            darwinex_time=False  # Get UTC first
        )
        
        # Convert to Darwinex time
        data_dw = to_darwinex_time(data)
        
        # Index should be different from UTC
        assert data.index.tz is not None
        assert data_dw.index.tz is not None
        
        conn.close()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
