module.exports = (robot) ->
  robot.commands.push "hubot créer ticket - provoque la création d'un ticket dans omnitracker"
  robot.commands.push "hubot fermer ticket [id] - fermer ticket"
  robot.commands.push "hubot mes tickets - recherche mes tickets dans Omnitracker"
  robot.commands.push "hubot chercher ticket [Titre] - cherche un ticket contenant les termes dans le Titre"

  robot.respond /créer ticket/i, (res) ->
    res.reply "Ok :"
    ticket = {stage_create: 1}
    name = res.message.user.name
    robot.brain.set name, ticket



  robot.respond /fermer ticket (.*)/i, (fermer) ->
    id = fermer.match[1]
    name = fermer.message.user.name

    fermer.reply "Ok, fermeture du ticket :"
    ticket_fermer = {stage_fermer: 1, ticket_id : id}
    name = fermer.message.user.name
    variablename = "#{name}_fermer"
    robot.brain.set variablename, ticket_fermer

  robot.hear /(.*)/i, (msg) ->
    name = msg.message.user.name
    variablename = "#{name}_fermer"
    ticket_fermer = robot.brain.get(variablename) or null


    if ticket_fermer != null
      answer = msg.match[1]
      switch ticket_fermer.stage_fermer
        when 1
          msg.reply "Texte de la solution a ajouter ?"
        when 2
          ticket_fermer.solution = answer
      ticket_fermer.stage_fermer += 1

      robot.brain.set variablename, ticket_fermer

      if ticket_fermer.stage_fermer > 2
        spawn = require('child_process').spawn
        args = ['/myhubot/pythonscripts/ticket-module/ticket.py',"fermer", "#{ticket_fermer.ticket_id}", "#{name}", "#{ticket_fermer.solution}"]
        build = spawn '/usr/bin/python', args
        build.stdout.setEncoding('utf8')
        result = ""
        build.stdout.on "data", (data) ->
          result += data.toString()
        build.stdout.on 'end', () ->
          msg.send result.toString()
        robot.brain.remove variablename

  robot.hear /(.*)/i, (msg) ->

    name = msg.message.user.name
    ticket = robot.brain.get(name) or null
    if ticket != null
      answer = msg.match[1]
      switch ticket.stage_create
        when 1
          msg.reply "Titre du ticket ?"
        when 2
          ticket.title=answer
          msg.reply "Description ?"
        when 3
          ticket.description=answer
          msg.reply "etes vous sur ? (y/n)"
        when 4
          ticket.confimation=answer
      ticket.stage_create += 1
      robot.brain.set name, ticket

      if ticket.stage_create > 4 #End of process
        if /y/i.test(ticket.confimation)
          spawn = require('child_process').spawn
          args = ['/myhubot/pythonscripts/ticket-module/ticket.py', "create", "#{ticket.title}", "#{ticket.description}","#{name}", '-u']
          build = spawn '/usr/bin/python', args
          build.stdout.setEncoding('utf8')
          build.stdout.on "data", (data) -> msg.send data.toString()
          msg.reply "Ticket #{ticket.title} for #{name} created."
        else
          msg.reply "ticket creation aborted"
        robot.brain.remove name




  robot.respond /test/i, (mess) ->
    spawn = require('child_process').spawn
    args = ['/myhubot/pythonscripts/ticket-module/ticket.py', "test", '-u']
    build = spawn '/usr/bin/python', args
    build.stdout.setEncoding('utf8')
    build.stdout.on "data", (data) -> mess.send data.toString()



  robot.respond /mes tickets/i, (tickets) ->
    name = tickets.message.user.name
    spawn = require('child_process').spawn
    args = ['/myhubot/pythonscripts/ticket-module/ticket.py',"get", "#{name}", '-u']
    build = spawn '/usr/bin/python', args
    build.stdout.setEncoding('utf8')
    result = ""
    build.stdout.on "data", (data) ->
      result += data.toString()
    build.stdout.on 'end', () ->
      tickets.send result.toString()






  robot.respond /chercher ticket (.*)/i, (search) ->
    text = search.match[1]
    name = search.message.user.name
    spawn = require('child_process').spawn
    args = ['/myhubot/pythonscripts/ticket-module/ticket.py',"search", "#{text}", "#{name}", '-u']
    build = spawn '/usr/bin/python', args
    build.stdout.setEncoding('utf8')
    result = ""
    build.stdout.on "data", (data) ->
      result += data.toString()
    build.stdout.on 'end', () ->
      search.send result.toString()
