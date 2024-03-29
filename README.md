# Generate table from raw ABET II behavioral data
## Description
This code takes raw data generated by the ABET II behavioral software and creates an organized table of relevant task events. 

.csv files generated by ABET are read in as a Pandas data frame, and then a series of functions pulls out relevant task events, including: 

- Trial block (1, 2, 3)
- Trial type (Forced vs. Free)
- Reward size (Large vs. Small)
- Shock (Shock vs. No shock)
- Trial start time (s)
- Reward choice time (s)
- Reward collection time (s)

These events are then concatenated in a table (a separate Pandas data frame) according to the trial number, using the Pandas groupby and apply methods. 

This table will then be used to filter on certain trial types (or combinations of trial types), which will allow us to align our neural data (bulk GCaMP-mediated fluorescence measured using fiber photometry) to particular behavioral epochs.

The TDT SDK (see "Required Items" below) provides a template for filtering based on user input.

## Required Items
[Anaconda Navigator NOTE:You must download python 3.7](https://www.anaconda.com/distribution/)

[ABET II](http://lafayetteneuroscience.com/products/abetii-operant-ctrl-software)
### Helpful Hints
[Instructions for use with Synapse Photometry System](www.tdt.com/support/python-sdk)

