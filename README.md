# orca-noise-analysis

This repo was started during the 2020 Amazon hackathon (12/11/2020). Here you will find Python and other scripts to access Orcasound and Conserve.io S3 buckets holding near-realtime data, including sound samples (.flac format) and AIS reports from the M2 radar/camera system on San Juan Island.

The general plan:

1) Aquire recent data via AWS CLI calls to S3 or M2 API
2) Ingest FLAC files into Python and compute "delta" noise level 
3) Call M2 API for time of closest point of approach (CPA) and ship metadata 
4) Use MMSI # of ship to lookup or scrape other ship metadata (e.g. type)
5) Write resultant time series to a .csv file and/or database

At that point data should be acquired and visualized by front end code at [https://github.com/orcasound/orca-shipnoise](https://github.com/orcasound/orca-shipnoise)
