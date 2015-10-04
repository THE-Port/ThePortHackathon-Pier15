# ThePortHackathon

Part 1 (Analysis)
    
    -   Finding the peaks in the graph
    -   Input is time vs amplitude that is present in input.txt, export_elpho_drug_ISZ.txt and export_elpho_drug_ISZ+RIF.txt (two columns of x and y)
    -   Baseline found using mean, PeakUtils regression, sigma approximation of a Gaussian function, and PeakUtils of data with a threshold and PeakUtils of data with peaks removed 
    -   peakfind.py returns all the peaks with their corresponding time, identifies local minima using a mean approximation of baseline, and calculates area of each peak 
    - 	baseline.py returns peaks, finds baseline using PeakUtils, finds baseline using PeakUtils after cutting data with a treshold, finds baseline using PeakUtils after identifying and removing peaks in data 
    - 	Using iPython and Jupyter to wrap python in a notebook for users to access online

Part 2 (Blockchain)

Part 3 (Heatmap)