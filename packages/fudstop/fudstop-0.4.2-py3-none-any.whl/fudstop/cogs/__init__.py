from .accounting import Accounting, AccountingSelect
from .fed_print import FedPrintCog
from .fiscal_service import FiscalService
from .gex import Gex
from .ibrs import IBRS
from .ta import TACog
from .register import FedRegisterCog
from .y_fin import yfCOG

import disnake
from disnake.ext import commands


class MainView(disnake.ui.View):
    def __init__(self):
        self.select = select
        super().__init__(timeout=None)


    @disnake.ui.button(style=disnake.ButtonStyle.blurple, label='-', custom_id='-1', row=0, disabled=True)
    async def one(self, button:disnake.ui.Button, inter:disnake.AppCmdInter):
        pass

    @disnake.ui.button(style=disnake.ButtonStyle.grey, label='-', custom_id='-2', row=0, disabled=True)
    async def two(self, button:disnake.ui.Button, inter:disnake.AppCmdInter):
        pass

    @disnake.ui.button(style=disnake.ButtonStyle.blurple, label='-', custom_id='-3', row=0, disabled=True)
    async def three(self, button:disnake.ui.Button, inter:disnake.AppCmdInter):
        pass

    @disnake.ui.button(style=disnake.ButtonStyle.grey, label='-', custom_id='-4', row=0, disabled=True)
    async def four(self, button:disnake.ui.Button, inter:disnake.AppCmdInter):
        pass

    @disnake.ui.button(style=disnake.ButtonStyle.blurple, label='-', custom_id='-5', row=0, disabled=True)
    async def five(self, button:disnake.ui.Button, inter:disnake.AppCmdInter):
        pass

    @disnake.ui.button(style=disnake.ButtonStyle.green, label='GEX', custom_id='gex', row=1)
    async def gex(self, button:disnake.ui.Button, inter:disnake.AppCmdInter):
        pass


    @disnake.ui.button(style=disnake.ButtonStyle.green, label='INFO', custom_id='info', row=1)
    async def info(self, button:disnake.ui.Button, inter:disnake.AppCmdInter):
        pass

    @disnake.ui.button(style=disnake.ButtonStyle.green, label='REG', custom_id='reg', row=1)
    async def reg(self, button:disnake.ui.Button, inter:disnake.AppCmdInter):
        pass


    @disnake.ui.button(style=disnake.ButtonStyle.green, label='FS', custom_id='fiscal', row=1)
    async def fs(self, button:disnake.ui.Button, inter:disnake.AppCmdInter):
        pass

    @disnake.ui.button(style=disnake.ButtonStyle.green, label='ACC', custom_id='accounting', row=1)
    async def acc(self, button:disnake.ui.Button, inter:disnake.AppCmdInter):
        self.add_item(AccountingSelect())
        


