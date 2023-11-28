import pandas as pd
import matplotlib.pyplot as plt

# Load the DataFrame from the Excel file
df = pd.read_excel("/home/cazorla/Images/Train_mon_LR/perf.xlsx")

# Get a list of unique training values
unique_trainings = df["Labels percentage"].unique()

# Set up a color map for differentiating training curves
color_map = plt.cm.get_cmap("tab20", len(unique_trainings))

# Create a figure and axis
fig, ax = plt.subplots()

# Plot each training curve with a different color
for i, training in enumerate(unique_trainings):
    training_df = df[df["Labels percentage"] == training]
    ax.plot(training_df["epochs_nb"], training_df["ap0"], label=training, color=color_map(i))

# Add labels and legend
ax.set_xlabel("Number of Epochs")
ax.set_ylabel("Average Precision")
ax.set_title("Evolution of Mean Segmentation Precision over Epochs\nBased on Annotated Pixel Percentage")
ax.legend()

# Save the plot as a PDF file
pdf_filename = "training_curves.pdf"
plt.savefig(pdf_filename, format="pdf")

# Show the plot
plt.show()
