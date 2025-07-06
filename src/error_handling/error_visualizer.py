import matplotlib.pyplot as plt
import pandas as pd

class ErrorVisualizer:
    def __init__(self, error_data=None):
        self.error_data = error_data if error_data is not None else []

    def add_error(self, error_type, timestamp):
        self.error_data.append({"type": error_type, "timestamp": timestamp})

    def plot_error_trends(self):
        if not self.error_data:
            print("No error data to plot.")
            return

        df = pd.DataFrame(self.error_data)
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df.set_index("timestamp", inplace=True)

        # Plot error count over time
        error_counts = df.resample('H').size().fillna(0) # Resample by hour, fill missing with 0
        plt.figure(figsize=(12, 6))
        plt.plot(error_counts.index, error_counts.values, marker='o', linestyle='-')
        plt.title('Error Count Over Time')
        plt.xlabel('Time')
        plt.ylabel('Number of Errors')
        plt.grid(True)
        plt.tight_layout()
        plt.show()

        # Plot error distribution by type
        error_distribution = df['type'].value_counts()
        plt.figure(figsize=(10, 6))
        error_distribution.plot(kind='bar')
        plt.title('Error Distribution by Type')
        plt.xlabel('Error Type')
        plt.ylabel('Count')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    # Example Usage:
    visualizer = ErrorVisualizer()
    from datetime import datetime, timedelta

    # Simulate some error data
    visualizer.add_error("ModuleNotFoundError", datetime.now() - timedelta(hours=3))
    visualizer.add_error("KeyError", datetime.now() - timedelta(hours=2, minutes=30))
    visualizer.add_error("TypeError", datetime.now() - timedelta(hours=2))
    visualizer.add_error("ModuleNotFoundError", datetime.now() - timedelta(hours=1, minutes=45))
    visualizer.add_error("bytes_too_short", datetime.now() - timedelta(hours=1, minutes=15))
    visualizer.add_error("KeyError", datetime.now() - timedelta(minutes=45))
    visualizer.add_error("bytes_too_short", datetime.now() - timedelta(minutes=15))

    visualizer.plot_error_trends()