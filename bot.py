import discord
import requests
from io import BytesIO
import matplotlib.pyplot as plt
import json
from scipy import stats
import numpy as np
from datetime import datetime, timedelta

TOKEN = 'YOUR_TOKEN_ID'
CHANNEL_ID = YOUR_CHANNEL_ID  # Use the actual channel ID here, as an integer

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

client = discord.Client(intents=intents)

def generate_graph(data):
    positions = np.array([point['Position'] for point in data['MeasurePoints']])
    values = np.array([point['Value'] for point in data['MeasurePoints']])
    final_hfr_position = np.argmin(np.abs(values - data['FinalHFR']))  # Assuming FinalHFR is in 'data'
    
    plt.figure(figsize=(10, 5))
    # Plotting the focus line with increased thickness
    plt.plot(positions, values, marker='o', linestyle='-', color='#36A2EB', label='Focus Curve', linewidth=4)  # Adjusted line thickness
    
    # Overlaying each MeasurePoint in pink
    plt.scatter(positions, values, color='#FF6384', zorder=5, label='Measure Points')

    # Splitting the data around the FinalHFR position and plotting trend lines
    left_positions = positions[:final_hfr_position + 1]
    left_values = values[:final_hfr_position + 1]
    right_positions = positions[final_hfr_position:]
    right_values = values[final_hfr_position:]

    if len(left_positions) > 1:  # Ensure there are enough points for regression
        slope, intercept, _, _, _ = stats.linregress(left_positions, left_values)
        plt.plot(left_positions, intercept + slope * left_positions, linestyle='--', color='#BA7C40', label='Trend', linewidth=2)  # Adjusted line thickness

    if len(right_positions) > 1:  # Ensure there are enough points for regression
        slope, intercept, _, _, _ = stats.linregress(right_positions, right_values)
        plt.plot(right_positions, intercept + slope * right_positions, linestyle='--', color='#BA7C40', linewidth=2)  # Adjusted line thickness

    # Highlighting the Final HFR position
    plt.scatter(positions[final_hfr_position], data['FinalHFR'], color='yellow', zorder=5, label='Final HFR')

    plt.gca().set_facecolor('#36393F')
    plt.grid(color='black', linestyle='-', linewidth=0.5)
    plt.tick_params(axis='x', colors='white')
    plt.tick_params(axis='y', colors='white')
    plt.xlabel('Focuser Position', color='black', fontsize=12)  
    plt.ylabel('HFR Value', color='black', fontsize=12)
    legend = plt.legend(loc='upper left', bbox_to_anchor=(0, -0.2), ncol=4, frameon=False, fontsize='medium')  # Adjusted legend position

    # Set legend text color to white
    for text in legend.get_texts():
        text.set_color('white')

    plt.tight_layout()

    buf = BytesIO()
    plt.savefig(buf, format='png', facecolor='#36393F', bbox_inches='tight', pad_inches=0.5)
    buf.seek(0)
    plt.close()

    return buf

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.channel.id != CHANNEL_ID or message.author == client.user:
        return

    for attachment in message.attachments:
        if attachment.filename.endswith('.json'):
            response = requests.get(attachment.url)
            data = response.json()
            graph_image = generate_graph(data)

            # Post the graph image
            file = discord.File(fp=graph_image, filename='graph.png')
            await message.channel.send(file=file)
            
            # Extracting existing autofocus values
            calculated_focus_position = int(data["CalculatedFocusPoint"]["Position"])
            hyperbolic_r_squared = f'{data["RSquares"]["Hyperbolic"]:.2f}'
            left_trend_r_squared = f'{data["RSquares"]["LeftTrend"]:.2f}'
            right_trend_r_squared = f'{data["RSquares"]["RightTrend"]:.2f}'
            
            # Extracting Time, Duration, and FinalHFR values
            time = data.get("Time", "N/A")
            duration = data.get("Duration", "N/A")
            final_hfr = data.get("FinalHFR", "N/A")

            # Correctly extracting BacklashCompensation values
            backlash_method = data.get("BacklashCompensation", {}).get("BacklashCompensationModel", "N/A")
            backlash_in = data.get("BacklashCompensation", {}).get("BacklashIN", "N/A")
            backlash_out = data.get("BacklashCompensation", {}).get("BacklashOUT", "N/A")

            embed = discord.Embed(color=0x7289da)
            
            # Extracting Duration from the JSON
            duration_str = data.get("Duration", "N/A")

            # Formatting Duration to display with only two decimal places for seconds
            if duration_str != "N/A":
                duration_parts = duration_str.split(":")
                duration_seconds = float(duration_parts[-1])
                formatted_duration = f"{duration_parts[0]}:{duration_parts[1]}:{duration_seconds:.2f}"
            else:
                formatted_duration = "N/A"

            # Extracting Time from the JSON
            time_str = data.get("Timestamp", "N/A")

            # Formatting Time to display the date and time portion with milliseconds
            if time_str != "N/A":
                # Splitting the timestamp string into date and time portions
                date_part, time_part = time_str.split("T")
                # Formatting the time portion to include milliseconds
                time_with_milliseconds = f"{time_part.split('.')[0]}.{time_part.split('.')[1][:2]}"
                # Combining the date and time portions
                formatted_time = f"{date_part} {time_with_milliseconds}"
            else:
                formatted_time = "N/A"

            # Extracting Duration from the JSON
            duration_str = data.get("Duration", "N/A")

            # Formatting Duration to display with only two decimal places for seconds
            if duration_str != "N/A":
                duration_parts = duration_str.split(":")
                duration_seconds = float(duration_parts[-1])
                formatted_duration = f"{duration_parts[0]}:{duration_parts[1]}:{duration_seconds:.2f}"
            else:
                formatted_duration = "N/A"

            # Extracting FinalHFR from the JSON
            final_hfr = data.get("FinalHFR", None)

            # Formatting FinalHFR to display with two decimal places
            formatted_final_hfr = "{:.2f}".format(final_hfr) if final_hfr is not None else "N/A"

            # Assuming data['Temperature'] is a float value representing temperature
            # Round the temperature to two decimal places
            temperature_rounded = round(data['Temperature'], 2)

            # Add the AutoFocus Details field with a newline after its name
            embed.add_field(name="AutoFocus Details\n", value=f"**Method:** {data['Method']}  |  **Fitting:** {data['Fitting']}  |  **Temperature:** {temperature_rounded}\n"
                                                            f"**Step-Size:** {data['FocuserOptions']['AutoFocusStepSize']}  |  **Calculated-Focus-Position:** {calculated_focus_position}  |  **Filter:** {data['Filter']}\n"
                                                            f"**Backlash Method:** {backlash_method}  |  **Backlash IN:** {backlash_in}  |  **Backlash OUT:** {backlash_out}\n",
                            inline=False)

            # Add the Coefficient of Determination field
            embed.add_field(name="R² - Coefficient of determination", value=f"**Hyperbolic:** {hyperbolic_r_squared}  |  **Left Trend:** {left_trend_r_squared}  |  **Right Trend:** {right_trend_r_squared}",
                            inline=False)

            # Add the Time, Duration, and FinalHFR fields with adjusted formatting
            embed.add_field(name="Date & Time", value=formatted_time, inline=True)
            embed.add_field(name="AF Duration", value=formatted_duration, inline=True)
            embed.add_field(name="Final HFR", value=formatted_final_hfr, inline=True)

            await message.channel.send(embed=embed)


client.run(TOKEN)
