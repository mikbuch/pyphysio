__author__ = 'AleB'

import pandas

import pyPhysio




# We use the included example data
from Extra.Snippets.example_data import Test2
# and the windows collection with the linear time windows generator with windows of 40s every 20s.
# This windows generator uses the labels data included in the data series to split the signal.
windows = pyPhysio.LabeledSegments(Test2.data_series)
# The windows mapper will do all the rest of the work, we just need to put
# there every Time (TD) and Frequency (FD) Domain and every Non Linear Index
mapper = pyPhysio.WindowsIterator(
    Test2.data_series,
    windows,
    pyPhysio.features.TDFeatures.__all__ +
    pyPhysio.features.FDFeatures.__all__ +
    pyPhysio.features.NonLinearFeatures.__all__)
mapper.compute_all()
# We convert the results to a example_data frame
data_frame = pandas.DataFrame(mapper.results)
# to give it an header
data_frame.columns = mapper.labels
# and to save it in a csv file, without the line number (index)
data_frame.to_csv("example2_results.csv", sep="\t", index=False)
# This results can be compared to the ones in Test2.results