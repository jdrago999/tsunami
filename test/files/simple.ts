# A sample tsunami code file

create session with weight 4 as 'test1':
    get '/api'
    delete '/view/view1'
    post '/view?name=view2&value=foo'
        ensure match /^{"success": "View 'view2' created"}$/
        ensure match /success/


create session with weight 12 as 'test2':
    get '/api'

create load:                
    spawn 2 users every 4 seconds for 10 minutes up to 100 users
    spawn 5 users every 10 seconds for 50 minutes
