module.exports = (robot) ->

  robot.commands.push "hubot classement ticket - recherche les tickets assignés aux admins au à l'utilisateur en cours"

  robot.respond /classer ticket/i, (res) ->
    res.reply "Ok :"
    classer = {stage_classer: 1}
    name = res.message.user.name
    robot.brain.set "#{name}_classer", classer
    args = ['/myhubot/pythonscripts/ticket-module/ticket.py',"classement", "#{name}", '-u']
    spawn = require('child_process').spawn
    build = spawn '/usr/bin/python', args
    build.stdout.setEncoding('utf8')
    result = ""
    build.stdout.on "data", (data) ->
      result += data.toString()
    build.stderr.on "data", (data) ->
      result += data.toString()
    build.stdout.on 'end', () ->
      res.send result.toString()





  robot.hear /(.*)/i, (msg) ->
    name = msg.message.user.name
    variablename = "#{name}_classer"
    ticket_classer = robot.brain.get(variablename) or null
    if ticket_classer != null
      answer = msg.match[1]

      switch ticket_classer.stage_classer
        when 1
          msg.reply "entrer le numéro id :"
        when 2
          ticket_classer.selected = answer
          msg.reply "quelle categorie ?"
          spawn = require('child_process').spawn
          args = ['/myhubot/pythonscripts/ticket-module/ticket.py',"listcategories", '-u']
          build = spawn '/usr/bin/python', args
          build.stdout.setEncoding('utf8')
          result = ""
          build.stdout.on "data", (data) ->
            result += data.toString()
          build.stderr.on "data", (data) ->
            result += data.toString()
          build.stdout.on 'end', () ->
            msg.send result.toString()


      ticket_classer.stage_classer += 1
      robot.brain.set variablename, ticket_classer
      if ticket_classer.stage_classer == 4
        ticket_classer.category = answer
        msg.reply "changement de catégorie du ticket #{ticket_classer.selected} en categorie #{ticket_classer.category}"
        args = ['/myhubot/pythonscripts/ticket-module/ticket.py',"assigncategory", "#{ticket_classer.selected}", "#{ticket_classer.category}",'-u']
        spawn = require('child_process').spawn
        build = spawn '/usr/bin/python', args
        build.stdout.setEncoding('utf8')
        result = ""
        build.stdout.on "data", (data) ->
          result += data.toString()
        build.stderr.on "data", (data) ->
          result += data.toString()
        build.stdout.on 'end', () ->
          msg.send result.toString()
         msg.reply 'gentrez un autre id ou "terminer"'
      if ticket_classer.stage_classer == 5
        if answer == annuler:
          robot.brain.remove variablename
        else:
          ticket_classer.stage_classer = 2
          robot.brain.set variablename, ticket_classer

