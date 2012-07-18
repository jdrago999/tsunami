create session with weight 1 as 'test1':
    get '/foo'

create load:                
    spawn 1 users every 1 seconds for 1 minutes up to 1 users
