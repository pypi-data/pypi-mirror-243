import json
import numpy as np
import matplotlib.pyplot as plt


def visualize_share_of_users_per_segment(data, base_path):
    # Extract data
    share_of_users_per_segment = data['share_of_users_per_segment_distribution']
    segments = list(share_of_users_per_segment.keys())
    values = [100*x for x in share_of_users_per_segment.values()]

    # Create and customize the plot
    plt.figure(figsize=(10, 6))
    plt.barh(segments, values)
    plt.xlabel('Share of Users [%]')
    plt.ylabel('Segment')
    plt.title('Share of Users per Segment Distribution')
    plt.tight_layout()

    # Save the plot as a PNG file
    plt.savefig(base_path + 'share_of_users_per_segment.png')
    plt.close()


def visualize_demographics(data, base_path):


    # Extract demographics data
    demographics_distributions = data['demographics_distributions']


    # Extract age and gender values
    age_values = set()
    gender_values = set()
    for demo in demographics_distributions.keys():
        age, gender = demo.split('||')
        age_values.add(age)
        gender_values.add(gender)

    age_values = sorted(age_values)
    gender_values = sorted(gender_values)

    heatmap_data_all_users = np.zeros((len(age_values), len(gender_values)))
    heatmap_data_authenticated_users = np.zeros((len(age_values), len(gender_values)))

    total_all_users = sum([v[0] for k, v in demographics_distributions.items() if k != "n/a||n/a"])
    total_authenticated_users = sum([v[1] for k, v in demographics_distributions.items() if k != "n/a||n/a"] )

    for i, age in enumerate(age_values):
        for j, gender in enumerate(gender_values):
            demo_key = f'{age}||{gender}'
            values = demographics_distributions.get(demo_key, [0, 0])  # Use [0, 0] if key not found
            share_all_users = values[0]
            share_authenticated_users = values[1]

            if age == "n/a" and gender == "n/a":
                heatmap_data_all_users[i, j] = 1 - total_all_users
                heatmap_data_authenticated_users[i, j] = 1 - total_authenticated_users
            else:
                heatmap_data_all_users[i, j] = share_all_users
                heatmap_data_authenticated_users[i, j] = share_authenticated_users

    # Find the maximum value in both heatmap data arrays
    max_value = max(np.max(heatmap_data_all_users), np.max(heatmap_data_authenticated_users))

    # Create and customize the heatmaps
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    cax1 = axes[0].matshow(heatmap_data_all_users, cmap='coolwarm', vmin=0, vmax=max_value)
    plt.colorbar(cax1, ax=axes[0], label='Share (%) (All Users)')
    axes[0].set_xticks(np.arange(len(gender_values)))
    axes[0].set_yticks(np.arange(len(age_values)))
    axes[0].set_xticklabels(gender_values)
    axes[0].set_yticklabels(age_values)
    for i in range(len(age_values)):
        for j in range(len(gender_values)):
            axes[0].text(j, i, f'{heatmap_data_all_users[i, j] * 100:.1f}%',
                         ha='center', va='center', color='w')
    axes[0].set_xlabel('Gender')
    axes[0].set_ylabel('Age Group')
    axes[0].set_title('Demographics Distribution (All Users)')

    cax2 = axes[1].matshow(heatmap_data_authenticated_users, cmap='coolwarm', vmin=0, vmax=max_value)
    plt.colorbar(cax2, ax=axes[1], label='Share (%) (Authenticated Users)')
    axes[1].set_xticks(np.arange(len(gender_values)))
    axes[1].set_yticks(np.arange(len(age_values)))
    axes[1].set_xticklabels(gender_values)
    axes[1].set_yticklabels(age_values)
    for i in range(len(age_values)):
        for j in range(len(gender_values)):
            axes[1].text(j, i, f'{heatmap_data_authenticated_users[i, j] * 100:.1f}%',
                         ha='center', va='center', color='w')
    axes[1].set_xlabel('Gender')
    axes[1].set_ylabel('Age Group')
    axes[1].set_title('Demographics Distribution (Authenticated Users)')

    # Adjust layout and save the heatmaps as PNG files
    plt.tight_layout()
    plt.savefig(base_path + 'demographics_heatmaps.png')
    plt.close()

def visualize_unique_users(data, base_path):
    # Extract data
    original_unique_users = data['original_number_of_unique_users']
    filtered_unique_users = data['filtered_number_of_unique_users']
    segments = list(original_unique_users.keys())
    original_values = list(original_unique_users.values())
    filtered_values = list(filtered_unique_users.values())

    # Create and customize the barplot
    x = range(len(segments))
    width = 0.4  # Width of the bars
    plt.figure(figsize=(10, 6))
    plt.bar(x, original_values, width, label='Original')
    plt.bar([i + width for i in x], filtered_values, width, label='Filtered')
    plt.ylabel('Number of Unique Users')
    plt.xticks([i + width/2 for i in x], segments, rotation='vertical')
    plt.legend()
    plt.tight_layout()

    # Save the plot as a PNG file
    plt.savefig(base_path + 'unique_users_barplot.png')
    plt.close()

def visualize_segments_per_user(data, base_path):
    # Extract data
    segments_per_user = data['segments_per_user_distributions']
    sorted_segments = sorted(segments_per_user.keys(), key=lambda x: int(x))
    all_users_values = [segments_per_user[seg][0] * 100 for seg in sorted_segments]
    authenticated_users_values = [segments_per_user[seg][1] * 100 for seg in sorted_segments]

    # Create and customize the barplot
    x = range(len(sorted_segments))
    width = 0.4  # Width of the bars
    plt.figure(figsize=(10, 6))
    plt.bar(x, all_users_values, width, label='All Users')
    plt.bar([i + width for i in x], authenticated_users_values, width, label='Authenticated Users')
    plt.xlabel('Segments')
    plt.ylabel('Percentage [%]')
    plt.title('Segments per User Distribution')
    plt.xticks([i + width/2 for i in x], sorted_segments)
    plt.legend()
    plt.tight_layout()

    # Save the plot as a PNG file
    plt.savefig(base_path + 'segments_per_user_barplot.png')
    plt.close()


base_path = "/Users/dstur/dq/code/delta2/delta/trusted/python-libs/dq-media-dcr/misc/generated_data/publisher_data_statistics_second_goldbach_run_15382434_None/"
# Load data from JSON file
with open(base_path + 'statistics.json', 'r') as json_file:
    data = json.load(json_file)


visualize_demographics(data, base_path)
visualize_share_of_users_per_segment(data, base_path)
visualize_unique_users(data, base_path)
visualize_segments_per_user(data, base_path)
