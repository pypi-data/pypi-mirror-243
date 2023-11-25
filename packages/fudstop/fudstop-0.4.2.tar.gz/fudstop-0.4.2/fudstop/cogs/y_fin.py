import os
from dotenv import load_dotenv
load_dotenv()
import disnake
from disnake.ext import commands
from apis.y_finance.yf_sdk import yfSDK




class yfCOG(commands.Cog):
    def __init__(self, bot):
        self.bot=bot
        self.sdk = yfSDK()



    @commands.slash_command()
    async def infos(self, inter):
        pass


    @infos.sub_command()
    async def mf(self, inter: disnake.AppCmdInter, ticker: str):
        """Gets mutual fund holdings for a ticker - top 10"""
        await inter.response.defer()
        try:
            data = self.sdk.mutual_fund_holders(ticker)
            
            filename = f'data/yf_{ticker}_mf_holders.csv'
            data.to_csv(filename)
            
            embed = disnake.Embed(
                title=f"Mutual Fund Holders - {ticker}", 
                description=f"Your Download is Ready!", 
                color=disnake.Colour.dark_teal()
            )
            embed.set_footer(text=f'Implemented by FUDSTOP')
            
            await inter.edit_original_message(embed=embed)
            await inter.send(file=disnake.File(filename))
        except Exception as e:
            await inter.edit_original_message(f"An error occurred: {e}")


    @infos.sub_command()
    async def balance(self, inter:disnake.AppCmdInter, ticker: str):
        """Gets balance sheet information for a ticker"""
        await inter.response.defer()
        try:
            data = self.sdk.balance_sheet(ticker)
            
            filename = f'data/yf_balance_sheet.csv'
            data.to_csv(filename)
            
            await inter.edit_original_message(f"Balance Sheet for {ticker}:")
            await inter.edit_original_message(file=disnake.File(filename))
        except Exception as e:
            await inter.edit_original_message(f"An error occurred: {e}")

    @infos.sub_command()
    async def cashflow(self, inter:disnake.AppCmdInter, ticker: str):
        """Gets cash flow information for a ticker"""
        await inter.response.defer()
        try:
            data = self.sdk.get_cash_flow(ticker)
            
            filename = f'data/yf_cash_flow.csv'
            data.to_csv(filename)
            
            await inter.edit_original_message(f"Cash Flow for {ticker}:")
            await inter.edit_original_message(file=disnake.File(filename))
        except Exception as e:
            await inter.edit_original_message(f"An error occurred: {e}")

    @infos.sub_command()
    async def financials(self, inter:disnake.AppCmdInter, ticker: str):
        """Gets all financials for a ticker"""
        await inter.response.defer()
        try:
            data = self.sdk.financials(ticker)
            
            filename = f'data/yf_financials.csv'
            data.to_csv(filename)
            
            await inter.edit_original_message(f"Financials for {ticker}:")
            await inter.edit_original_message(file=disnake.File(filename))
        except Exception as e:
            await inter.edit_original_message(f"An error occurred: {e}")


    # Command for the income_statement method within yfSDK
    @infos.sub_command()
    async def statement(self, inter:disnake.AppCmdInter, ticker: str, frequency: str = 'quarterly', pretty: bool = False, as_dict: bool = False):
        """Gets the income statement for a ticker"""
        await inter.response.defer()
        data = self.sdk.income_statement(ticker, frequency=frequency, pretty=pretty, as_dict=as_dict)
        filename = f'data/yf_income_statement.csv'
        data.to_csv(filename)
        await inter.edit_original_message(file=disnake.File(filename))

    # Command for the get_info method within yfSDK
    @infos.sub_command()
    async def info(self, inter:disnake.AppCmdInter, ticker: str):
        """Returns a large dictionary of information for a ticker"""
        await inter.response.defer()
        data = self.sdk.get_info(ticker)
        filename = f'data/yf_info.csv'
        data.to_csv(filename)
        await inter.edit_original_message(file=disnake.File(filename))

    # Command for the institutional_holdings method within yfSDK
    @infos.sub_command()
    async def whales(self, inter:disnake.AppCmdInter, ticker: str):
    
        """Gets institutional holdings for a ticker"""
        await inter.response.defer()
        data = self.sdk.institutional_holdings(ticker)
        filename = f'data/yf_institutional_holdings.csv'
        data.to_csv(filename)
        await inter.edit_original_message(file=disnake.File(filename))


    @infos.sub_command()
    async def div(self, inter:disnake.AppCmdInter, ticker: str):
        """Gets dividends for a ticker - if any."""
        await inter.response.defer()
        data = self.sdk.dividends(ticker)
        filename = f'data/dividends.csv'
        data.to_csv(filename)
        await inter.edit_original_message(file=disnake.File(filename))


    @infos.sub_command()
    async def allinfo(self, inter:disnake.AppCmdInter, ticker: str):
        """Gets all relevant company data for a ticker."""
        await inter.response.defer()
        data = self.sdk.fast_info(ticker)
        filename = f'data/fast_info.csv'
        data.to_csv(filename)
        await inter.edit_original_message(file=disnake.File(filename))


    @infos.sub_command()
    async def candles(self, inter:disnake.AppCmdInter, *, ticker: str):
        """Gets all candlestick data for a ticker"""
        await inter.response.defer()
        data = self.sdk.get_all_candles(ticker)
        filename = f'data/all_candles.csv'
        data.to_csv(filename)
        await inter.edit_original_message(file=disnake.File(filename))


    # Command for the news method within yfSDK
    @infos.sub_command()
    async def news(self, inter:disnake.AppCmdInter, ticker: str):
        """Gets ticker news"""
        await inter.response.defer()
        data = self.sdk.news(ticker)
        filename = f'data/yf_news.csv'
        data.to_csv(filename)
        await inter.edit_original_message(file=disnake.File(filename))

    # Command for the atm_calls method within yfSDK
    @infos.sub_command()
    async def calls(self, inter:disnake.AppCmdInter, ticker: str):
        """Gets at the money calls for a ticker"""
        await inter.response.defer()
        data = self.sdk.atm_calls(ticker)
        data.to_csv('data/atm_calls.csv')
        filename = f'data/atm_calls.csv'
        data.to_csv(filename, index=False)
        await inter.edit_original_message(file=disnake.File(filename))

    # Command for the atm_calls method within yfSDK
    @infos.sub_command()
    async def puts(self, inter:disnake.AppCmdInter, ticker: str):
        """Gets at the money puts for a ticker"""
        await inter.response.defer()
        data = self.sdk.atm_puts(ticker)
        data.to_csv('data/atm_puts.csv')
        filename = f'data/atm_puts.csv'
        data.to_csv(filename, index=False)
        await inter.edit_original_message(file=disnake.File(filename))

def setup(bot: commands.Bot):
    bot.add_cog(yfCOG(bot))


    print(f'YF COG - READY')