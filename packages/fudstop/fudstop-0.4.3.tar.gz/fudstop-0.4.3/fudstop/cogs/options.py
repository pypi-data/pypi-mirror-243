import os
from dotenv import load_dotenv
load_dotenv()
import matplotlib.pyplot as plt
import disnake
import aiohttp
from disnake.ext import commands
from bot_menus.pagination import AlertMenus, PageSelect
from apis.polygonio.polygon_options import PolygonOptions
from apis.webull.webull_options import WebullOptions
from apis.webull.webull_trading import WebullTrading
from tabulate import tabulate
import asyncio
from apis.helpers import format_large_numbers_in_dataframe
import pandas as pd


class OptionsCOG(commands.Cog):
    def __init__(self, bot):
        self.bot=bot
        self.options = PolygonOptions()
        self.wt = WebullTrading()
        self.wb = WebullOptions(os.environ.get('WEBULL_OPTIONS'))



    @commands.slash_command()
    async def opts(self, inter):
        pass


    @opts.sub_command()
    async def full_skew(self, inter:disnake.AppCmdInter, ticker:str):
        """Gets the lowest IV call/put option for all expirations for a ticker"""
        ticker = ticker.upper()
        await inter.response.defer()
        full_skew, price = await self.options.full_skew(ticker)
        full_skew['iv'] = (full_skew['iv'] * 100).round(2)
        full_skew = full_skew.rename(columns={'strike': 'skew_strike'})
        full_skew = full_skew.drop(columns=['cp'])
        table = tabulate(full_skew, headers='keys', tablefmt='fancy', showindex=False)


        chunks = [table[i:i + 3860] for i in range(0, len(table), 3860)]
        embeds=[]
        for chunk in chunks:
            embed = disnake.Embed(title=f"Full Skew - {ticker}", description=f"> Current Price: **${price}**\n```py\n{chunk}```", color=disnake.Colour.dark_orange())
            embed.add_field(name=f"Full Skew for: {ticker}",value=f"> Price: **{price}**")
            embed.set_footer(text=f'Full Skew: {ticker} | Data by Polygon.io | Implemented by FUDSTOP')
            embeds.append(embed)

        button = disnake.ui.Button(style=disnake.ButtonStyle.blurple, label='Download')
        button.callback = lambda interaction: interaction.response.send_message(file=disnake.File('full_skew.csv'))

        
        await inter.edit_original_message(embed=embeds[0], view=AlertMenus(embeds).add_item(PageSelect(embeds)).add_item(button).add_item(OptsSelect(ticker)))


    @opts.sub_command()
    async def top_vol_strikes(self, inter:disnake.AppCmdInter, ticker:str):
        """
        Gets the top volume strikes across all expirations for calls/puts.
        
        """
        await inter.response.defer()
        ticker = ticker.upper()

        data = await self.options.vol_oi_top_strike(ticker)

        # Ensure 'expiry' is a datetime column
        data['expiry'] = pd.to_datetime(data['expiry'])

        # Change date format to 'YY-MM-DD'
        data['expiry'] = data['expiry'].dt.strftime('%y-%m-%d')

        data = format_large_numbers_in_dataframe(data)
        data = data.drop(columns=['ticker'])
        data.to_csv('top_vol_strikes.csv', index=False)
        table = tabulate(data, headers='keys', tablefmt='fancy', showindex=False)


        chunks = [table[i:i + 3860] for i in range(0, len(table), 3860)]
        embeds=[]
        for chunk in chunks:
            embed = disnake.Embed(title=f"TopVol Strikes - {ticker}", description=f"```py\n{chunk}```", color=disnake.Colour.dark_orange())
            embed.set_footer(text=f'TopVol Strikes: {ticker} | Data by Polygon.io | Implemented by FUDSTOP')
            embeds.append(embed)

        button = disnake.ui.Button(style=disnake.ButtonStyle.blurple, label='Download')
        button.callback = lambda interaction: interaction.response.send_message(file=disnake.File('top_strike_vol.csv'))

        
        await inter.edit_original_message(embed=embeds[0], view=AlertMenus(embeds).add_item(PageSelect(embeds)).add_item(button).add_item(OptsSelect(ticker)))

    @opts.sub_command()
    async def lowest_theta(self, inter:disnake.AppCmdInter, ticker:str):
        """
        Gets all options ranked by THETA from decreasing to increasing.
        """

        await inter.response.defer()
        # Ensure 'expiry' is a datetime column
        data = await self.options.lowest_theta(ticker)
        data['expiry'] = pd.to_datetime(data['expiry'])

        # Change date format to 'YY-MM-DD'
        data['expiry'] = data['expiry'].dt.strftime('%y-%m-%d')

        data = format_large_numbers_in_dataframe(data)
        data = data.drop(columns=['ticker'])
        data.to_csv('lowest_theta.csv', index=False)
        columns_to_keep = ['strike', 'cp', 'expiry', 'theta']
        data = data[columns_to_keep]
        table = tabulate(data, headers='keys', tablefmt='fancy', showindex=False)

        data = data[::-1]
        chunks = [table[i:i + 3860] for i in range(0, len(table), 3860)]
        embeds=[]
        for chunk in chunks:
            embed = disnake.Embed(title=f"Lowest Theta Strikes - {ticker}", description=f"```py\n{chunk}```", color=disnake.Colour.dark_orange())
            embed.set_footer(text=f'Lowest Theta Strikes: {ticker} | Data by Polygon.io | Implemented by FUDSTOP')
            embed.add_field(name=f"Viewing:", value=f"> **Lowest THETA options per expiry for {ticker}**")
            embeds.append(embed)

        button = disnake.ui.Button(style=disnake.ButtonStyle.blurple, label='Download')
        button.callback = lambda interaction: interaction.response.send_message(file=disnake.File('lowest_theta.csv'))

        
        await inter.edit_original_message(embed=embeds[0], view=AlertMenus(embeds).add_item(PageSelect(embeds)).add_item(button).add_item(OptsSelect(ticker)))

    @opts.sub_command()
    async def highest_velocity(self, inter:disnake.AppCmdInter, ticker:str):
        """
        Gets all options ranked by THETA from decreasing to increasing.
        """
        ticker = ticker.upper()
        await inter.response.defer()
        # Ensure 'expiry' is a datetime column
        data = await self.options.highest_velocity(ticker)
        data['expiry'] = pd.to_datetime(data['expiry'])

        # Change date format to 'YY-MM-DD'
        data['expiry'] = data['expiry'].dt.strftime('%y-%m-%d')

        data = format_large_numbers_in_dataframe(data)
        data = data.drop(columns=['ticker'])
        data.to_csv('high_velocity.csv', index=False)
        columns_to_keep = ['strike', 'expiry', 'cp', 'velocity']
        data = data[columns_to_keep]
        table = tabulate(data, headers='keys', tablefmt='fancy', showindex=False)


        chunks = [table[i:i + 3860] for i in range(0, len(table), 3860)]
        embeds=[]
        for chunk in chunks:
            embed = disnake.Embed(title=f"Highest Velocity Strikes - {ticker}", description=f"```py\n{chunk}```", color=disnake.Colour.dark_orange())
            embed.set_footer(text=f'Highest Velocity Strikes: {ticker} | Data by Polygon.io | Implemented by FUDSTOP')
            embed.add_field(name=f"Viewing:", value=f"> **Highest velocity options per expiry for {ticker}**")
            embeds.append(embed)

        button = disnake.ui.Button(style=disnake.ButtonStyle.blurple, label='Download')
        button.callback = lambda interaction: interaction.response.send_message(file=disnake.File('high_velocity.csv'))

        
        await inter.edit_original_message(embed=embeds[0], view=AlertMenus(embeds).add_item(PageSelect(embeds)).add_item(button).add_item(OptsSelect(ticker)))


    @opts.sub_command()
    async def volume_analysis(self, inter:disnake.AppCmdInter, ticker:str, date:str):
        """Enter a date in YYYY-MM-DD and view the volume analysis per strike!"""
        ticker =ticker.upper()
        await inter.response.defer()

        
        headers = self.wb.headers
        option_ids = await self.wb.get_option_ids(ticker)  # Adjust based on actual return structure

        async with aiohttp.ClientSession(headers=headers) as session:
            tasks = [self.wb.fetch_volume_analysis(session, option_symbol, id, underlying_ticker) for option_symbol, id, underlying_ticker in option_ids]
            dfs = await asyncio.gather(*tasks)  # Run all tasks concurrently
            
        final_df = pd.concat(dfs, ignore_index=True)
        print(final_df)
        price = await self.wt.stock_quote(ticker)
        price_ = price.web_stock_close
        final_df['underlying_price'] = price_
        final_df = final_df.sort_values('buy', ascending=False)
        final_df.to_csv(f'volume_analysis.csv', index=False)

        def plot_volume_by_strike_for_date(df, target_date, option_type='all', dark_background=True):
            # Extract data for the specific date
            target_df = df[(df['expiry'] == pd.to_datetime(target_date)) & (df['cp'] == option_type)]
            
            # If no data available for the target_date, inform and return without plotting
            if target_df.empty:
                print(f"No data available for the date: {target_date} and type: {option_type}")
                return

            plt.style.use('dark_background' if dark_background else 'default')
            
            # Create a plot with dark background
            fig, ax = plt.subplots(figsize=(12, 6), facecolor='black' if dark_background else 'white')
            
            # Plot buy and sell volumes for calls and puts separately
            calls = target_df[target_df['option'] == 'call']
            puts = target_df[target_df['option'] == 'put']
            
            width = (target_df['strike'].max() - target_df['strike'].min()) / len(target_df['strike'].unique()) * 0.4
            
            # Call Volumes
            ax.bar(calls['strike'] - width/2, calls['buy'], width=width, label='Call Buy Volume', color='blue', alpha=0.7)
            ax.bar(calls['strike'] - width/2, -calls['sell'], width=width, label='Call Sell Volume', color='lightblue', alpha=0.7)
            
            # Put Volumes
            ax.bar(puts['strike'] + width/2, puts['buy'], width=width, label='Put Buy Volume', color='purple', alpha=0.7)
            ax.bar(puts['strike'] + width/2, -puts['sell'], width=width, label='Put Sell Volume', color='pink', alpha=0.7)
            
            # Set title and axes labels with gold color and high readability
            ax.set_title(f'Call/Put Buy/Sell Volume by Strike for Expiry: {pd.to_datetime(target_date).strftime("%Y-%m-%d")}', color='gold')
            ax.set_xlabel('Strike Price', color='gold')
            ax.set_ylabel('Volume', color='gold')
            
            # Tick parameters for readability
            ax.tick_params(axis='x', colors='gold')
            ax.tick_params(axis='y', colors='gold')

            # Adding grid for better readability, with a lighter color
            ax.grid(True, color='dimgray')
            
            # Show legend with readable font color
            ax.legend(facecolor='darkgray', edgecolor='gold', fontsize='large')
            
            # Show the plot
            plt.tight_layout()
            plt.savefig('plot.png')
            plt.show()

        # Example usage:
        # Load the data (make sure to parse the 'date' and 'expiry' columns correctly)
        df = pd.read_csv('volume_analysis.csv', parse_dates=['date', 'expiry'])

        # Filter out rows with missing values in the volume, strike, or expiry columns if necessary
        # df = df.dropna(subset=['buy_volume', 'sell_volume', 'strike', 'expiry'])

        # Call the function with the chosen date
        plot_volume_by_strike_for_date(df, date, dark_background=True)
        file = disnake.File('plot.png', filename='plot.png')
        embed = disnake.Embed(title=f"Volume Analysis - {ticker} | {date}")
        
        embed.set_image(url="attachment://plot.png")

        await inter.edit_original_message(embed=embed, file=file)
opts = OptionsCOG(commands.Bot)


class OptsSelect(disnake.ui.Select):
    def __init__(self, ticker=None):
        self.ticker=ticker

        super().__init__( 
            placeholder='Choose a command -->',
            min_values=1,
            max_values=1,
            custom_id='optsCOGselect',
            options = [ 
                disnake.SelectOption(label='Full Skew',value='0', description=f'View the skew across all expirations.'),
                disnake.SelectOption(label='Top Vol. Strikes',value='1', description=f'View top volume strikes across all expirations.'),
                disnake.SelectOption(label='Lowest Theta', value='2',description=f'Find the options per expiry that have least theta decay.'),
                disnake.SelectOption(label='Highest Velocity', value='3', description='View the strikes with higehst velocity.')
            ]
        )


    async def callback(self, inter:disnake.AppCmdInter):
        if self.values[0] == '0':
            await opts.full_skew(inter, self.ticker)

        elif self.values[0] == '1':
            await opts.top_vol_strikes(inter, self.ticker)
 
        elif self.values[0] == '2':
            await opts.lowest_theta(inter, self.ticker)

        elif self.values[0] == '3':
            await opts.highest_velocity(inter, self.ticker)
def setup(bot: commands.Bot):
    bot.add_cog(OptionsCOG(bot))
    print(f'Options command - Ready')