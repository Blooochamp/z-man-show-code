import discord
from discord.ext import commands
import json
import urllib.request
import re

def SiteContents(url):
    Request = urllib.request.Request(url, headers={"User-Agent":'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'})
    Response = urllib.request.urlopen(Request)
    return Response.read()

Roles = json.loads(open("RobloxRoles.json").read())

API = "http://verify.eryn.io/api/user/"

def HasVerified(ID):
    JSON = SiteContents(API + str(ID))
    Data = json.loads(JSON)

    Status = Data['status']
    if Status == "ok":
        ROBLOXUsername = Data['robloxUsername']
        ROBLOXID = Data['robloxId']
        return ROBLOXUsername, ROBLOXID
    else:
        return "no sir"

def IsVerified(ID):
    JSON = SiteContents(API + str(ID))
    Data = json.loads(JSON)

    Status = Data['status']
    if Status == "ok":
        return True
    else:
        return False

def GroupRank(RobloxID, Group):
    Content = SiteContents("https://roblox.com/Game/LuaWebService/HandleSocialRequest.ashx?method=GetGroupRank&playerid=" + str(RobloxID) + "&groupid=" + str(Group))
    Rank = int(re.findall("\d+", str(Content))[0])
    return Rank

async def VerifyMember(self, Guild, ID):
    Member = Guild.get_member(ID)
    if Member:
        if HasVerified(ID) == "no sir":
            await self.bot.send_message(Member, "Hi there! You are not verified, please verify by going to https://verify.eryn.io")
            pass
        else:
            Name, RobloxID = HasVerified(ID)
            #await DM(Member, "You have been verified! Please allow up to 1 minute for your roles to be given.")
            for RoleName, RoleInformation in Roles.items():
                print(RoleName)
                Group = RoleInformation['GroupID']
                RequiredRank = int(RoleInformation['Rank'])
                GiveToAbove = RoleInformation['GiveToAbove']
                Role = GetRole(Guild, RoleName)
                if GiveToAbove:
                    if GroupRank(RobloxID, Group) >= RequiredRank:
                        await self.bot.add_roles(Member, Role)
                    elif GroupRank(RobloxID, Group) < RequiredRank:
                        await self.bot.remove_roles(Member, Role)
                else:
                    if GroupRank(RobloxID, Group) == RequiredRank:
                        await self.bot.add_roles(Member, Role)
                    elif GroupRank(RobloxID, Group) < RequiredRank:
                        await self.bot.remove_roles(Member, Role)
            
            await self.bot.change_nickname(Member, Name)
    

def GetRole(Guild, Name):
    Role = discord.utils.get(Guild.roles, name=Name)
    return Role

class RobloxCommands:
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(pass_context=True)
    async def verify(self, ctx):
        Message = ctx.message
        Guild = Message.server
        try:
            Member = Guild.get_member(Message.author.id)
            #await bot.delete_message(Message)
            await VerifyMember(self, Guild, Member.id)
        except:
            pass
    
    @commands.command(pass_context=True)
    async def update(self, ctx, user : discord.User):
        Message = ctx.message
        Channel = Message.channel
        Guild = Message.server
        if IsVerified(user.id):
            Member = Guild.get_member(user.id)
            to_edit = await self.bot.send_message(Channel, ":bulb: Updating <@%s>..." % user.id)
            await VerifyMember(self, Guild, Member.id)
            await self.bot.edit_message(to_edit, ":white_check_mark:  <@%s> has successfully been updated :white_check_mark:" % user.id) 
        elif IsVerified(user.id) == False:
            await self.bot.send_message(Channel, "<%s> is not verified. Head to https://verify.eryn.io and verify" % user.id)


def setup(bot):
    bot.add_cog(RobloxCommands(bot))
