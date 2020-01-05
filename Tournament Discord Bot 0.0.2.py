import discord
import requests

teamsDict = dict()
teamHolder = list()
tournamentCodeIndex = 0
touramentCodeList = list()
#DiscordServerid = 662831092549681192


class Player():

    def __init__(self,ign):
        self.role = "No Role"
        self.ign = ign
        self.position = "No position"
        self.id = 0

    def set_role(self,role):
        self.role = role

    def set_ign(self,ign):
        self.ign = ign

    def set_position(self,position):
        self.position = position

    def set_id(self,id):
        self.id = int(id)

class Team():

    def __init__(self,teamName,abbr):
        self.teamName = teamName
        self.abbr = abbr
        self.playerPool = []
        self.starters = []
        self.subs = []

    def set_teamName(self,newName):
        self.teamName = newName

    def set_teamAbbr(self,newAbbr):
        self.abbr = newAbbr

    def add_starter(self,starter):
        self.starters.append(starter)

    def add_sub(self,sub):
        self.subs.append(sub)

    def add_player(self,player):
        self.playerPool.append(player)

    def remove_player(self,player):
        self.playerPool.remove(player)

    def remove_starter(self,player):
        self.starters.remove(player)

    def remove_sub(self,player):
        self.subs.remove(player)


class MyClient(discord.Client):

    async def on_ready(self):
        #Make sure the bot is up and running
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        if message.author == self.user:
            return

        if (message.content.startswith('#addTeam')):
            #Adds a team into the global team dictionary
            #command : #addTeam "Team Abbr." "Team Name"
            userInput = message.content.split()
            teamAbbr = userInput[1]
            teamName = " ".join(userInput[2:])
            teamHolder.append(Team(teamName,teamAbbr))
            await message.channel.send(f'{teamAbbr} {teamName} has been added')

        elif (message.content.startswith('#addMem')):
            #Adds a member to a team using the
            #command : #addMem  'Enter Team Abbreviation' 'Enter Player Name'
            try:
                userInput = message.content.split()
                teamAbbr = userInput[1]
                playerName = " ".join(userInput[2:])
                for teams in teamHolder:
                    if teams.abbr == teamAbbr:
                        teams.add_player(Player(playerName))
                await message.channel.send(f'{playerName} has been added to {teamAbbr}')
            except:
                await message.channel.send("#addMem  'Enter Team Abbreviation' 'Enter Player Name'")


        elif(message.content.startswith('#setRole')):
            #Sets the role of a player
            #command : #setRole 'Enter Player Name' 'Enter Role Number'
            #Top: "001" Jg: "002" Mid: "003" ADC: "004 Supp: "005 Fill: "006" "
            roleNumbers = {"001": "Top", "002": "Jungle", "003": "Mid", "004": "Marksman", "005": "Support", "006": "Fill"}
            userInput = message.content.split()
            for words in userInput:
                if words in roleNumbers:
                    roleIndex = userInput.index(words)
            playerName = " ".join(userInput[1:roleIndex])
            role = roleNumbers[userInput[roleIndex]]
            for teams in teamHolder:
                for players in teams.playerPool:
                    if players.ign == playerName:
                        players.set_role(role)
                        await message.channel.send(f'{role} has been added to {playerName}')
                        break
                for players in teams.starters:
                    if players.ign == playerName:
                        players.set_role(role)
                        await message.channel.send(f'{role} has been added to {playerName}')
                        break
                for players in teams.subs:
                    if players.ign == playerName:
                        players.set_role(role)
                        await message.channel.send(f'{role} has been added to {playerName}')
                        break

        elif (message.content.startswith('#setPos')):
            #sets the position of a player
            #command : #setPos 'Enter Player Name' 'Enter Position (starter or sub)'
            posList = {"starter":"Starter", "sub":"Sub"}
            userInput = message.content.split()
            for i in userInput:
                if i in posList:
                    posIndex = userInput.index(i)
            position = posList[userInput[posIndex]]
            playerName = " ".join(userInput[1:posIndex])
            for teams in teamHolder:
                for players in teams.playerPool:
                    if players.ign == playerName:
                        players.set_position(position)
                        if position == "Starter":
                            teams.add_starter(players)
                            teams.remove_player(players)
                        elif position == "Sub":
                            teams.add_sub(players)
                            teams.remove_player(players)
                        await message.channel.send(f'{playerName} has been set to {position}')
                        break
                for players in teams.starters:
                    if players.ign == playerName:
                        players.set_position(position)
                        if position == "Starter":
                            continue
                        elif position == "Sub":
                            teams.add_sub(players)
                            teams.remove_starter(players)
                        await message.channel.send(f'{playerName} has been set to {position}')
                        break
                for players in teams.subs:
                    if players.ign == playerName:
                        players.set_position(position)
                        if position == "Starter":
                            teams.add_starter(players)
                            teams.remove_sub(players)
                        elif position == "Sub":
                            continue
                        await message.channel.send(f'{playerName} has been set to {position}')
                        break

        elif(message.content.startswith('#setID')):
            #sets the ID of a player by @'ing them in discord
            #command: #setID @Example#1234 "Enter in player Name"
            userInput = message.content.split()
            id = userInput[1][3:-1]
            playerName = " ".join(userInput[2:])
            for teams in teamHolder:
                for players in teams.playerPool:
                    if players.ign == playerName:
                        players.set_id(id)
                        await message.channel.send(f'{playerName} got his ID set')
                        break
                for players in teams.starters:
                    if players.ign == playerName:
                        players.set_id(id)
                        await message.channel.send(f'{playerName} got his ID set')
                        break
                for players in teams.subs:
                    if players.ign == playerName:
                        players.set_id(id)
                        await message.channel.send(f'{playerName} got his ID set')
                        break

        elif (message.content.startswith('#teams')):
            #Displays all the team with its players under it
            #command: #teams
            for team in teamHolder:
                await message.channel.send(f'{team.abbr} {team.teamName}: ')
                for players in team.playerPool:
                    await message.channel.send(f'IGN: {players.ign} Role: {players.role} Position: {players.position}')
                for players in team.starters:
                    await message.channel.send(f'IGN: {players.ign} Role: {players.role} Position: {players.position}')
                for players in team.subs:
                    await message.channel.send(f'IGN: {players.ign} Role: {players.role} Position: {players.position}')

        elif (message.content.startswith('#remoPlayer')):
            #Deletes a player from a team
            #command: #remoPlayer "Enter Player Name"
            userInput = message.content.split()
            playerName = " ".join(userInput[1:])
            for teams in teamHolder:
                for players in teams.playerPool:
                    if players.ign == playerName:
                        teams.remove_player(players)
                        await message.channel.send(f'{playerName} has been removed from {teams.abbr}')
                        break
                for players in teams.starters:
                    if players.ign == playerName:
                        teams.remove_starter(players)
                        await message.channel.send(f'{playerName} has been removed from {teams.abbr}')
                        break
                for players in teams.subs:
                    if players.ign == playerName:
                        teams.remove_sub(players)
                        await message.channel.send(f'{playerName} has been removed from {teams.abbr}')
                        break

        elif (message.content.startswith('#remoTeam')):
            #Deletes a team from the database
            #command: #remoTeam "Enter Team Name"
            userInput = message.content.split()
            teamName = " ".join(userInput.index[1:])
            for teams in teamHolder:
                if teams.teamName == teamName:
                    teamHolder.remove(teams)
                    await message.channel.send(f'{teamName} has been removed')
                    break
            await message.channel.send(f'{teamName} was not able to be found')

        elif (message.content.startswith('#teamRename')):
            #Rename a team
            #command: #teamRename "Enter Old Team Abbr." "Enter New Team Abbr." "Enter New Team Name"
            userInput = message.content.split()
            oldTeamAbbr = userInput[1]
            newTeamAbbr = userInput[2]
            newTeamName = userInput[3:]
            for teams in teamHolder:
                if teams.abbr == oldTeamAbbr:
                    teams.set_teamAbbr(newTeamAbbr)
                    teams.set_teamName(newTeamName)
            await message.channel.send(f'{oldTeamAbbr} has been renamed to {newTeamAbbr} {newTeamName}')

        elif (message.content.startswith('#playerRename')):
            '''Brent this one is for you'''
            #Rename a player
            #command:
            userInput = message.content.split()
            pass

        elif (message.content.startswith('#DMTeams')):
            #DM the teams tournament codes using the command : #DMTeams team1: "enter team 1" team2: "enter team 2"
            id = client.get_guild(662831092549681192)
            userInput = message.content.split()
            message = getTournCode()
            user = userInput[1][3:-1]
            user = client.get_user(int(user))
            await user.send(message)

        elif (message.content.startswith('#genTournCode')):
            #Generates tournaments as a command
            global tournamentCodeIndex
            global touramentCodeList
            tournamentCodeIndex = 0
            touramentCodeList = requests.get("INSERT RIOT URL")
            pass

        elif (message.content.startswith('#getCurrTournIndex')):
            #Tells the user what the current tournament code index is within the list above
            await message.channel.send(tournamentCodeIndex)

        elif (message.content.startswith('#getTournCode')):
            # returns the tournament code at the list index of "index given as an argument"
            await message.channel.send(touramentCodeList[message.content.split()[1]])


def getTournCode():
    #returns a tournament code using the tournament code list and tournament index
    return touramentCodeList[tournamentCodeIndex]

client = MyClient()
client.run("NjYyODMwMzk0NTE2NzAxMjMz.Xg_wsA.XVPq4ain1vEHB4ZM4ZGVW_O4_iI")
