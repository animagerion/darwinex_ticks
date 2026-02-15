# Darwinex-ticks
Darwinex tick data python API.

The broker Darwinex offers to their real accounts a historical data dowload 
service using a ftp server. 

This basic API connects with your server account 
and download the data of one or several assets available. 

The data is returned as a Pandas dataframe. 


## Installation

`pip install Darwinex-ticks`
    
### Requirements
- pandas >= 1.5.0
- ipywidgets >= 8.0.0 (optional, for progress bar in Jupyter notebooks)

For development/testing:
- pytest >= 7.0.0


## Testing

Run tests with pytest:

```bash
pip install pytest
pytest tests/ -v
```

### Integration Tests

To run integration tests with real Darwinex FTP credentials:

```bash
export DARWINEX_USER="your_username"
export DARWINEX_PASS="your_password"
export DARWINEX_HOST="tickdata.darwinex.com"  # optional, default provided
pytest tests/test_integration.py -v
```

Integration tests will be skipped if credentials are not provided.


## Example 



Quick usage.
```
import darwinex_ticks
dwt = darwinex_ticks.DarwinexTicksConnection(dwx_ftp_user='<your Darwinex username>',
                       dwx_ftp_pass='<your Darwinex ftp password>',
                       dwx_ftp_hostname='<Darwinex ftp host eg. tickdata.darwinex.com>',
                       dwx_ftp_port='<assigned port>')
                       
data = dwt.ticks_from_darwinex('EURUSD', start='2018-08-02 08', 
                                end='2018-08-02 12')                 
```
You could check the example notebook too.


## Command line usage.

It's possible use the package at terminal. 
You need have installed python, pandas and darwinex_ticks.

`python -m darwinex_ticks EURGBP EURGBP USDJPY -u paduel -w kyK8omxZm8pxp -n 
tickdata.darwinex.com -s "2018-10-08 10" -e "2018-10-08 12" -g`

This command line connect the darwinex ticks data ftp  with 
the passed user, password and hostname, download the ticks data
 of EURGBP, EURGBP and USDJPY from 2018/10/08 10:00 to 28/10/08 12:59, and 
 save (-g) user, password and hostname at config file, so the next time you 
 don't need to pass its. 