"""
Laboratory Work 5: Weather Data Analysis
Processes meteorological datasets using Pandas and Matplotlib.
"""

import pandas as pd
import matplotlib.pyplot as plt

def main():
    PERIOD_VARIANT = 8
    
    df = pd.read_csv("weather.csv")
    out_df = df.copy()
    
    # Robust extraction and cleaning of numeric values from strings with units
    df["precipitation"].replace("-", "0.01", inplace=True)

    floated_cloudiness = df["cloudiness"].astype(str).str.extract(r'(\d+\.?\d*)')[0].astype(float)
    floated_precipitation = df["precipitation"].astype(str).str.extract(r'(\d+\.?\d*)')[0].fillna(0.01).astype(float)
    floated_days_tmp = df["day_temperature"].astype(str).str.extract(r'(-?\d+\.?\d*)')[0].astype(float)
    floated_nights_tmp = df["night_temperature"].astype(str).str.extract(r'(-?\d+\.?\d*)')[0].astype(float)
    floated_wind_force = df["wind_speed"].astype(str).str.extract(r'(\d+)')[0].astype(int)
    month = pd.to_datetime(df["period"]).dt.month

    df["precipitation"] = floated_precipitation
    df["day_temperature"] = floated_days_tmp
    df["night_temperature"] = floated_nights_tmp
    df["cloudiness"] = floated_cloudiness
    df["wind_speed"] = floated_wind_force
    df["period"] = month

    df_variant = df.loc[df["period"] == PERIOD_VARIANT]

    # Plot 1: Subplots for variant period
    fig, graphic = plt.subplots(nrows=2, ncols=2, figsize=(11, 11))

    graphic[0, 1].plot(df_variant["day"], df_variant["day_temperature"])
    graphic[0, 1].set_xlabel("Day")
    graphic[0, 1].set_ylabel("Day Temperature (°C)")

    graphic[1, 1].plot(df_variant["day"], df_variant["night_temperature"])
    graphic[1, 1].set_xlabel("Day")
    graphic[1, 1].set_ylabel("Night Temperature (°C)")

    graphic[0, 0].plot(df_variant["day"], df_variant["cloudiness"])
    graphic[0, 0].set_xlabel("Day")
    graphic[0, 0].set_ylabel("Cloudiness (%)")

    graphic[1, 0].plot(df_variant["day"], df_variant["wind_speed"])
    graphic[1, 0].set_xlabel("Day")
    graphic[1, 0].set_ylabel("Wind Speed (m/s)")

    plt.tight_layout()
    plt.savefig("weather_subplots.png")
    plt.close()

    # Scatter plot with precipitation bubble size
    bubble_size = df_variant["precipitation"] * 50
    plt.figure(figsize=(8, 6))
    plt.scatter(df_variant["day"], df_variant["day_temperature"], s=bubble_size, alpha=0.6, edgecolors="black")
    plt.xlabel("Day")
    plt.ylabel("Day Temperature (°C)")
    plt.title("Day Temperature vs Day (Bubble size = Precipitation)")
    plt.savefig("weather_scatter.png")
    plt.close()

    # Temperature deviation analysis
    tmp_difference = df["night_temperature"] - df["day_temperature"]
    out_df["deviation"] = tmp_difference.abs()
    
    max_deviation = out_df["deviation"].abs().max()
    print("Maximum temperature deviation record:")
    print(out_df[out_df["deviation"].abs() == max_deviation])

    # Pie chart for days with precipitation per period
    df_filtered = out_df[out_df["precipitation"] != "-"]
    df_precipitation_counts = df_filtered.groupby("period")["precipitation"].count()

    plt.figure(figsize=(8, 8))
    plt.pie(df_precipitation_counts, labels=df_precipitation_counts.index, autopct="%1.1f%%", startangle=90)
    plt.axis("equal")
    plt.title("Distribution of Days with Precipitation by Period")
    plt.savefig("weather_precipitation_pie.png")
    plt.close()

    # Cloud type classification and bar chart
    out_df["cloud_type"] = ""
    out_df.loc[df["cloudiness"] > 70, "cloud_type"] = "Cloudy Days"
    out_df.loc[df["cloudiness"] < 35, "cloud_type"] = "Sunny Days"
    out_df.loc[(df["cloudiness"] <= 70) & (df["cloudiness"] >= 35), "cloud_type"] = "Partly Cloudy Days"

    cloudness_counter = out_df.groupby("period")["cloud_type"].value_counts().unstack("cloud_type", fill_value=0)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    cloudness_counter.plot(kind="bar", stacked=True, ax=ax)
    plt.legend(loc="upper right")
    plt.xticks(rotation=45)
    plt.xlabel("Period")
    plt.ylabel("Number of Days")
    plt.title("Cloud Type Distribution by Period")
    plt.tight_layout()
    plt.savefig("weather_cloud_bars.png")
    plt.close()

    # Temperature deviation histogram
    plt.figure(figsize=(8, 6))
    out_df["deviation"].hist(bins=20, grid=False, edgecolor="black")
    plt.xlabel("Temperature Deviation (°C)")
    plt.ylabel("Frequency")
    plt.title("Histogram of Night vs Day Temperature Deviation")
    plt.savefig("weather_deviation_hist.png")
    plt.close()

    print("Weather analysis completed successfully. All plots and statistics generated.")


if __name__ == "__main__":
    main()
