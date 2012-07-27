create session with weight 4 as 'test1':
    get "/"

create session with weight 1 as 'test2':
    get '/about/'

create load:
    spawn users every 1 seconds for 1 minutes
