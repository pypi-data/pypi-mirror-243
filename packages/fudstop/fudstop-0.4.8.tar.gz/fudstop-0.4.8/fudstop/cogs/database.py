import os
import re
from dotenv import load_dotenv
load_dotenv()
from disnake.ext import commands
import disnake
import pandas as pd
from datetime import datetime
from apis.webull.webull_options import WebullOptions
from disnake import TextInputStyle
from tabulate import tabulate
from bot_menus.pagination import AlertMenus
from apis.webull.modal import WebullModal, VolumeAnalysisModal

options = WebullOptions(connection_string=os.environ.get('WEBULL_OPTIONS'))



class MyModal(disnake.ui.Modal):
    def __init__(self, selected_columns, ticker:str):
        self.ticker = ticker.upper()
        self.default_columns = ['symbol', 'strike_price', 'call_put', 'expiry_date']
        self.selected_columns = selected_columns
        # Placeholder text for specific fields
        placeholders = {
            'call_put': "Enter 'call' or 'put'",
            'expiry_date': "Enter a date (e.g., '2023-12-31')",
            'open_interest': "Enter a numerical threshold (e.g., '> 1000.. <= 500..')",
            'open_interest_change': "Enter a change value (e.g., '< -50')",
            'strike_price': "Enter a strike price (e.g., '= 300')",
            # You can continue to add more fields with specific placeholders if needed.
            'volume': "Enter a volume amount (e.g., '>= 50000')",
            'bid_price': "Enter a bid price threshold(e.g., '< 5.00')",
            'ask_price': "Enter an ask price thredhold (e.g., '> 5.00')",
            'theta': "Enter a theta value threshold",
            'gamma': "Enter a gamma value threshold",
            # Add any additional fields relevant to your options data and what users may want to query.
        }
        # Default placeholder for fields not in the dictionary
        default_placeholder = "Enter condition (e.g., '> 100')"
        
        components = [
            disnake.ui.TextInput(
                label=f"{column}",
                placeholder=placeholders.get(column, default_placeholder),  # Use specific placeholder if available
                custom_id=f"condition_{column}",
                style=TextInputStyle.short,
            )
            for column in selected_columns  # Create a TextInput for each selected column
        ]
        
        super().__init__(title="Query Options Database", components=components)

    async def callback(self, inter: disnake.ModalInteraction):
        await options.connect()


        # Retrieve the conditions from the modal's text inputs
        conditions = []
        params = []

        for column in self.selected_columns:
            user_input = inter.text_values[f"condition_{column}"].strip()
            if not user_input:  # Skip if there's no user input for this column
                continue

            if column == 'strike_price':
                try:
                    # If the input is expected to be a float/int, attempt to convert it
                    numeric_value = float(user_input)  # Using float as an example, could be int
                    conditions.append(f"{column} = '{user_input}'")
                    params.append(numeric_value)  # Append the converted numeric value
                except ValueError:
                    # Handle the case where the input was not a valid number
                    # This could involve logging the error, informing the user, etc.
                    continue  # Skip adding this condition if the input isn't a valid number
            elif column == 'open_interest':
                # This will match input like '>= 1000', '< 5000', etc.
                match = re.match(r"([<>]=?|=?)\s*(\d+)$", user_input)
                print(user_input)
                if match:
                    operator, number = match.groups()
                    try:
                        numeric_value = float(number)  # Convert the number part to a float/int
                        conditions.append(f"{column} {operator} {numeric_value}")

                        params.append(numeric_value)  # Append the numeric value only
                    except ValueError:
                        # Log the error or inform the user that the input was invalid
                        continue  # Skip this condition
                else:
                    # Inform the user about the invalid format, or log this as an error
                    continue  # Skip this condition if the regex match failed

            elif column == 'volume':
                # This will match input like '>= 1000', '< 5000', etc.
                match = re.match(r"([<>]=?|=?)\s*(\d+)$", user_input)
                print(user_input)
                if match:
                    operator, number = match.groups()
                    try:
                        numeric_value = float(number)  # Convert the number part to a float/int
                        conditions.append(f"{column} {operator} {numeric_value}")

                        params.append(numeric_value)  # Append the numeric value only
                    except ValueError:
                        # Log the error or inform the user that the input was invalid
                        continue  # Skip this condition
                else:
                    # Inform the user about the invalid format, or log this as an error
                    continue  # Skip this condition if the regex match failed
            elif column == 'open_interest_change':
                # This will match input like '>= 1000', '< 5000', etc.
                match = re.match(r"([<>]=?|=?)\s*(\d+)$", user_input)
                print(user_input)
                if match:
                    operator, number = match.groups()
                    try:
                        numeric_value = float(number)  # Convert the number part to a float/int
                        conditions.append(f"{column} {operator} {numeric_value}")

                        params.append(numeric_value)  # Append the numeric value only
                    except ValueError:
                        # Log the error or inform the user that the input was invalid
                        continue  # Skip this condition
                else:
                    # Inform the user about the invalid format, or log this as an error
                    continue  # Skip this condition if the regex match failed

            elif column == 'ask_price':
                # This will match input like '>= 0.05', '< 0.55', etc.
                match = re.match(r"([<>]=?|=?)\s*(\d+)$", user_input)
                print(user_input)
                if match:
                    operator, number = match.groups()
                    try:
                        numeric_value = float(number)  # Convert the number part to a float/int
                        conditions.append(f"{column} {operator} {numeric_value}")

                        params.append(numeric_value)  # Append the numeric value only
                    except ValueError:
                        # Log the error or inform the user that the input was invalid
                        continue  # Skip this condition
                else:
                    # Inform the user about the invalid format, or log this as an error
                    continue  # Skip this condition if the regex match failed

            elif column == 'bid_price':
                # This will match input like '>= 0.05', '< 0.55', etc.
                match = re.match(r"([<>]=?|=?)\s*(\d+)$", user_input)
                print(user_input)
                if match:
                    operator, number = match.groups()
                    try:
                        numeric_value = float(number)  # Convert the number part to a float/int
                        conditions.append(f"{column} {operator} {numeric_value}")

                        params.append(numeric_value)  # Append the numeric value only
                    except ValueError:
                        # Log the error or inform the user that the input was invalid
                        continue  # Skip this condition
                else:
                    # Inform the user about the invalid format, or log this as an error
                    continue  # Skip this condition if the regex match failed

            elif column == 'theta':
                # This will match input like '>= -0.05', '< -0.10', etc.
                match = re.match(r"([<>]=?|=?)\s*(\d+)$", user_input)
                print(user_input)
                if match:
                    operator, number = match.groups()
                    try:
                        numeric_value = float(number)  # Convert the number part to a float/int
                        conditions.append(f"{column} {operator} {numeric_value}")

                        params.append(numeric_value)  # Append the numeric value only
                    except ValueError:
                        # Log the error or inform the user that the input was invalid
                        continue  # Skip this condition
                else:
                    # Inform the user about the invalid format, or log this as an error
                    continue  # Skip this condition if the regex match failed

            elif column == 'call_put':
                # For 'call_put', you expect either 'call' or 'put' as valid inputs
                if user_input.lower() in ['call', 'put']:
                    conditions.append(f"{column} = '{user_input}'")
                    params.append(user_input.lower())
            elif column == 'expiry_date':
                # For 'expiry_date', you expect the input in the format 'YYYY-MM-DD'
                conditions.append(f"{column} = '{user_input}'")
                params.append(user_input)

        # Combine all conditions with ' AND '
        condition_str = ' AND '.join(conditions)

  
        query = f"""
        SELECT symbol, strike_price, call_put, expiry_date, FROM options_data
        WHERE symbol = '{self.ticker}' AND {condition_str} LIMIT 25;
        """
        print(query)
        # Execute the query
        try:
            data = await options.fetch(query)
            if data:
                df = pd.DataFrame(data, columns=['sym', 'strike', 'c/p', 'exp', f'{column}'])
                table = tabulate(df, headers='keys', tablefmt='fancy', showindex=False)
                embed = disnake.Embed(title="Database Query Results", description=f"```py\n{table}```", color=disnake.Colour.dark_orange())
                embed.set_footer(text=f'Query: {query}')
                await inter.response.send_message(embed=embed)
            else:
                await inter.response.send_message("No data found for the given conditions.")
        except Exception as e:
            await inter.response.send_message(f"An error occurred: {e}")
        finally:
            await options.close_pool()


class QueryView(disnake.ui.View):
    def __init__(self, ticker:str):

        self.ticker=ticker
        super().__init__(timeout=None)

        self.add_item(QueryOptions(ticker))
        self.add_item(QueryVolumeAnalysis(ticker))






class QueryOptions(disnake.ui.Select):
    def __init__(self, ticker:str):
        self.ticker=ticker
        super().__init__( 
            placeholder='Select Your Columns -->',
            min_values=1,
            max_values=4,
            custom_id='querydatabase',
            options = [ 
                disnake.SelectOption(label='strike_price', description=f'Add strike to the query.'),
                disnake.SelectOption(label='call_put', description='Add contract type to the query.'),
                disnake.SelectOption(label='expiry_date', description=f'Add the expiration date to the query.'),
                disnake.SelectOption(label='open_interest', description=f'Adds open_interest to the query.'),
                disnake.SelectOption(label='volume', description=f'Adds volume to the query.'),
                disnake.SelectOption(label='oi_change',description='Adds open_interest_change to the query.'),
                disnake.SelectOption(label='ask_price', description=f'Adds ask_price to the query.'),
                disnake.SelectOption(label='bid_price', description='Adds bid_price to the query.'),
                disnake.SelectOption(label='theta', description='Adds theta to the query.'),
                disnake.SelectOption(label='gamma', description='Adds gamma to the query.'),

            ]
        )


    async def callback(self, inter: disnake.MessageInteraction):
        # Get the selected options
        selected_columns = self.values

        # Create and send the modal
        modal = WebullModal(selected_columns, self.ticker)
        await inter.response.send_modal(modal)

class QueryVolumeAnalysis(disnake.ui.Select):
    def __init__(self, ticker:str):
        self.ticker = ticker
        super().__init__(
            placeholder='Select Volume Analysis Columns -->',
            min_values=1,
            max_values=5,  # Adjust the max_values as per your requirements
            custom_id='queryvolumeanalysis',
            options=[
                disnake.SelectOption(label='total_trades', description='Add total trades to the query.'),
                disnake.SelectOption(label='total_volume', description='Add total volume to the query.'),
                disnake.SelectOption(label='avg_price', description='Add average price to the query.'),
                disnake.SelectOption(label='buy_volume', description='Add buy volume to the query.'),
                disnake.SelectOption(label='sell_volume', description='Add sell volume to the query.'),
                disnake.SelectOption(label='neutral_volume', description='Add neutral volume to the query.'),
                # Add more options as per the columns in your volume_analysis table
            ]
        )

    async def callback(self, inter: disnake.MessageInteraction):
        # Get the selected options
        selected_columns = self.values

        # Create and send the modal for the volume_analysis table
        modal = VolumeAnalysisModal(selected_columns, self.ticker)
        await inter.response.send_modal(modal)

class Database(commands.Cog, WebullOptions):
    def __init__(self, bot):
        self.bot=bot
        self.connection_string = os.environ.get('WEBULL_OPTIONS')


    @commands.slash_command()
    async def db(self, inter):
        pass



    @db.sub_command()
    async def top_oi_change(self, inter:disnake.AppCmdInter):
        """
        Gets all options for a ticker from the database.
        
        """
        await inter.response.defer()
        await self.connect()

        query = f"""SELECT ticker, open_interest_change, strike_price, call_put, expiry_date
                    FROM options_data
                    WHERE open_interest_change IS DISTINCT FROM 'NaN'
                    AND (open_interest_change > 0 OR open_interest_change < 0)
                    ORDER BY open_interest_change DESC NULLS LAST;"""
        
        results = await self.fetch(query)


        df = pd.DataFrame(results, columns=['sym', 'oi_change', 'strike', 'c/p', 'exp'])


        table = tabulate(df, headers='keys', tablefmt='fancy', showindex=False)
        chunks = [table[i:i + 4000] for i in range(0, len(table), 4000)]

        embeds = []
        for chunk in chunks:
            embed = disnake.Embed(title=f"Open Interest Changes - All", description=f"```py\n{chunk}```", color=disnake.Colour.dark_orange())
            embed.set_footer(text='Viewing open interest changes across all options.')
            embeds.append(embed)
        await inter.edit_original_message(embed=embeds[0], view=AlertMenus(embeds))





def setup(bot: commands.Bot):
    bot.add_cog(Database(bot))

    print(f"Database commands - READY!")