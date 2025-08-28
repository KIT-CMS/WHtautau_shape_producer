import ROOT
import argparse
import uproot
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser(
        description="Small script to copy files from one folder to another with gfal-copy using a queue-based approach",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
parser.add_argument(
    "--channel",
    type=str,
    default=15,
    help="Number of parallel threads to be used for copying.",
)
parser.add_argument(
    "--input",
    type=str,
    default=15,
    help="Number of parallel threads to be used for copying.",
)
    
    


# Function to normalize histograms
def normalize_histogram(hist):
    hist = hist / hist.sum()  # Normalize by the sum of all bin values (integral)
    return hist

# Main script to plot pt_123met distribution
def plot_pt_123met_distribution(input_root_file, channel):
    # Open the ROOT file using uproot
    file = uproot.open(input_root_file)
    
    # Define the list of processes
    processes = ["WH_htt_plus#{CH}-H#Nominal#pt_123met".format(CH=channel), "WZ#{CH}-VV#Nominal#pt_123met".format(CH=channel), "jetFakes#{CH}-jetFakes#Nominal#pt_123met".format(CH=channel)]
    label_dict={"WH_htt_plus#{CH}-H#Nominal#pt_123met".format(CH=channel): r"WH$(\tau\tau)$", "WZ#{CH}-VV#Nominal#pt_123met".format(CH=channel): "WZ", "jetFakes#{CH}-jetFakes#Nominal#pt_123met".format(CH=channel): "jet fakes"}
    # Create a figure for plotting
    plt.figure(figsize=(8, 6))
    
    # Colors for different processes
    colors = ["#b9ac70", "#3f90da", "#e76300", 'm']
    
    # Loop over the processes and retrieve the histograms
    for i, process in enumerate(processes):
        # Retrieve the histogram from the ROOT file
        hist = file[process].to_numpy()  # Get histogram as numpy array (values, edges)
        
        hist_values, bin_edges = hist  # Extract values and bin edges
        
        # Normalize the histogram
        hist_values = normalize_histogram(hist_values)
        
        # Plot the histogram
        plt.hist(bin_edges[:-1], bins=bin_edges, weights=hist_values, histtype='step', color=colors[i], label=label_dict[process])
    
    
    
    # Set labels and title
    plt.xlabel(r"pt_123met (GeV)")
    plt.ylabel("Normalized Entries")
    
    # Set y-axis limit to 0.5
    plt.ylim(0, 0.5)
    
    # Add a legend
    plt.legend(loc='upper right')
    
    # Save the plot as a .png file
    plt.savefig("pt_123met_distribution_normalized_{CH}.pdf".format(CH=channel))
    
    # Display the plot
    #plt.show()


# Example usage of the function
if __name__ == "__main__":
    args = parser.parse_args()
    input_root_file = args.input
    channel=args.channel  # Change this to your actual file path
    plot_pt_123met_distribution(input_root_file,channel)