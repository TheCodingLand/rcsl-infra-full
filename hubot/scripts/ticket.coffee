module.exports = (robot) ->
  robot.commands.push "hubot créer ticket - provoque la création d'un ticket dans omnitracker"
  robot.commands.push "hubot fermer ticket [id] - fermer ticket"
  robot.commands.push "hubot mes tickets - recherche mes tickets dans Omnitracker"
  robot.commands.push "hubot chercher ticket [Titre] - cherche un ticket contenant les termes dans le Titre"
  robot.commands.push "hubot admin tickets - recherche les tickets assignés aux admins au à l'utilisateur en cours"

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


  robot.respond /chercher ticket (.*)/i, (search) ->
    text = search.match[1]
    name = search.message.user.name
    ticket_search = {stage_search: 1, text: text}
    variablename = "#{name}_search"
    robot.brain.set variablename, ticket_search
    search.send "setup variablename.stage_search to #{ticket_search.stage_search}, text to #{ticket_search.text}"


  robot.on "ticketlist", (msg, params) ->
    name = msg.message.user.name
    msg.reply "Liste des tickets contenant le mot : #{params.text}"
    args = ['/myhubot/pythonscripts/ticket-module/ticket.py',"search", "#{params.text}", "#{name}", "False", '-u']
    #deploy code goes here
    spawn = require('child_process').spawn
    build = spawn '/usr/bin/python', args
    build.stdout.setEncoding('utf8')
    result = ""
    build.stdout.on "data", (data) ->
      result += data.toString()
    build.stderr.on "data", (data) ->
      result += data.toString()
    build.stdout.on 'end', () ->
      msg.reply result.toString()

  robot.on "pdf-publication", (msg, params) ->
    msg.reply "Le document doit respecter des normes spécifiques à resa. (#{params.typedepot} , #{params.typesociete}"




  robot.hear /(.*)/i, (msg) ->
    name = msg.message.user.name
    variablename = "#{name}_search"
    ticket_search = robot.brain.get(variablename) or null
    if ticket_search != null
      msg.send "setup variablename.stage_search to #{ticket_search.stage_search}, text to #{ticket_search.text}"
      answer = msg.match[1]
      switch ticket_search.stage_search
        when 1
          msg.reply "chercher les tickets fermés ? (y/n)"
        when 2
          ticket_search.close = answer
      ticket_search.stage_search += 1
      robot.brain.set variablename, ticket_search
      if ticket_search.stage_search > 2
        msg.send "setup variablename.stage_search to #{ticket_search.stage_search}, text to #{ticket_search.text}"
        if /y/i.test(ticket_search.close)
          msg.send "recherche dans les ticket fermés"
          args = ['/myhubot/pythonscripts/ticket-module/ticket.py',"search", "#{ticket_search.text}", "#{name}", "True", '-u']
        else
          "recherche uniquement dans les fichiers ouverts"
          args = ['/myhubot/pythonscripts/ticket-module/ticket.py',"search", "#{ticket_search.text}", "#{name}", "False", '-u']
        msg.send "lancement de la recherche"
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
        robot.brain.remove variablename


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
        build.stderr.on "data", (data) ->
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

  robot.respond /admin tickets/i, (tickets) ->
    name = tickets.message.user.name
    spawn = require('child_process').spawn
    args = ['/myhubot/pythonscripts/ticket-module/ticket.py',"admin", "#{name}", '-u']
    build = spawn '/usr/bin/python', args
    build.stdout.setEncoding('utf8')
    result = ""
    build.stdout.on "data", (data) ->
      result += data.toString()
    build.stdout.on 'end', () ->
      tickets.send result.toString()





  #robot.respond /chercher ticket (.*)/i, (search) ->
  #  text = search.match[1]
  #  name = search.message.user.name
  #  spawn = require('child_process').spawn
  #  args = ['/myhubot/pythonscripts/ticket-module/ticket.py',"search", "#{text}", "#{name}", '-u']
  #  build = spawn '/usr/bin/python', args
  #  build.stdout.setEncoding('utf8')
  #  result = ""
  #  build.stdout.on "data", (data) ->
  #    result += data.toString()
  #  build.stdout.on 'end', () ->
  #    search.send result.toString()
