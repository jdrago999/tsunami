# A sample tsunami code file

create session with weight 4 as 'test1':
    get '/api'
    pause between 1.5 and 3.2 seconds
    delete '/view/view1'
    post '/view?name=view2&value=foo'
        ensure match /^{"success": "View 'view2' created"}$/
        ensure match /success/

create session with weight 12 as 'test2':
    var pin is a unique number from 1000 to 9999
    var username is a random string of length 10
    var pass_code is a random number from 1000 to 9999
    post '/user/create?username=$username&pass_code=$pass_code&pin=$pin'

create load:                
    spawn 2 users every 4 seconds for 10 minutes up to 100 users
    spawn 5 users every 10 seconds for 50 minutes
