"""
AUD currency conversion commands
Information taken from www.xe.com
"""

from discord.ext import commands
from bs4 import BeautifulSoup
import aiohttp

from utils.chat_formatter import codebox, heading


class CurrencyConversion(commands.Cog):
    # Country currency codes supported be xe.com
    VALID_CURRENCIES = {
        'AED', 'ALL', 'AMD', 'ARS', 'AUD', 'AZN', 'BAM', 'BBD', 'BDT', 'BGN',
        'BHD', 'BND', 'BOB', 'BSD', 'BTN', 'BWP', 'CAD', 'CHF', 'CLP', 'COP',
        'CRC', 'CVE', 'CZK', 'DJF', 'DKK', 'DOP', 'DZD', 'EGP', 'EUR', 'FJD',
        'GBP', 'GEL', 'GHS', 'GMD', 'GNF', 'GTQ', 'HKD', 'HNL', 'HUF', 'IDR',
        'ILS', 'INR', 'JMD', 'JOD', 'JPY', 'KES', 'KRW', 'KWD', 'KZT', 'LKR',
        'LSL', 'MAD', 'MGA', 'MKD', 'MUR', 'MXN', 'MYR', 'MZN', 'NAD', 'NGN',
        'NOK', 'NPR', 'NZD', 'OMR', 'PEN', 'PGK', 'PHP', 'PKR', 'PLN', 'PYG',
        'QAR', 'RON', 'RSD', 'RWF', 'SAR', 'SBD', 'SEK', 'SGD', 'SLE', 'SRD',
        'THB', 'TJS', 'TND', 'TOP', 'TRY', 'TTD', 'TWD', 'UGX', 'USD', 'UYU',
        'VND', 'VUV', 'WST', 'XCD', 'XPF', 'ZAR'
    }

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    def _build_xe_url(self, amount: float, orig: str, targ: str) -> str:
        """
        Build link for www.xe.com currency conversion

        Parameters
        amount - converting amount of orig currency to targ currency
        orig - country code for original country currency
        targ - country code for target country currency 

        Returns
        xe_link - the link to www.xe.com with specified inputs
        """
        xe_link = f"https://www.xe.com/en-au/currencyconverter/convert/?Amount={amount}&From={orig}&To={targ}"
        return xe_link

    @commands.command()
    async def currencies(self, ctx):
        """List all supported currency codes"""
        # Format list into comma-seperated values
        currency_list = ', '.join(self.VALID_CURRENCIES)

        # Output currencies in codebox with small header
        await ctx.send(heading("Valid Currencies", 3))
        await ctx.send(codebox(currency_list))

    @commands.command()
    async def convert(self, ctx, amount: float, orig: str, targ: str):
        """Convert currency amount from original to target."""

        if amount <= 0:
            return await ctx.send("Amount must be positive.")

        orig = orig.upper()
        targ = targ.upper()

        # xe.com converter will only accept specific currency codes (those listed in self.VALID_CURRENCIES)
        if orig not in self.VALID_CURRENCIES:
            return await ctx.send(f"Invalid original currency supplied {orig}. Examples: USD, EUR, AUD")
        if targ not in self.VALID_CURRENCIES:
            return await ctx.send(f"Invalid target currency supplied {targ}. Examples: USD, EUR, AUD")

        try:
            # Conversion information can be retrieved by inputting parameters into website link
            xe_link = self._build_xe_url(amount, orig, targ)

            async with aiohttp.ClientSession() as session:
                async with session.get(xe_link) as response:
                    # Parse through text found on xe.com
                    text = await response.text()
                    soup = BeautifulSoup(text, 'html.parser')

                    # Conversion data is held in <p> elements with classes:
                    # 'sc-c5062ab2-0 cFcKFA' for original (orig) currency
                    # 'sc-c5062ab2-1 jKDFIr' for target (targ) currency
                    original_amount = soup.find(
                        'p', class_="sc-c5062ab2-0 cFcKFA").getText()
                    new_amount = soup.find(
                        'p', class_="sc-c5062ab2-1 jKDFIr").getText()

                    # Handle case where beautiful soup fails (e.g. if site structure changes)
                    if not original_amount or not new_amount:
                        return await ctx.send(f"Conversion data could not be retrieved.")

                    # Original data is in format: '<amount> <orig name> ='
                    # Target data is in format: '<converted amount> <targ name>'
                    return await ctx.send(f"{original_amount} {new_amount}")

        except aiohttp.ClientError:
            return await ctx.send("Error occurred while querying xe.com for conversion data.")

    @commands.command()
    async def erate(self, ctx, orig: str, targ: str):
        """Get the exchange rates between two currencies"""
        await self.convert(ctx, 1, orig, targ)


async def setup(bot: commands.Bot):
    await bot.add_cog(CurrencyConversion(bot=bot))
