# pause.ts
create session with weight 1 as 'show_pause':
    get '/bar'
    pause between 1 and 3 seconds
    get '/foo'

create load:                
    spawn users every 1 seconds for 1 seconds
