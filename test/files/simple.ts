# A sample tsunami code file

create session with weight 4 as 'test1':
    get '/api'
    pause between 1 and 3 seconds
    delete '/view/view1'
    var coincidence is a random number from 1 to 2
    post '/view' with data 'name=view2&value=foo'
        ensure match /^{"success": "View 'view$coincidence' created"}$/
        ensure match /success/
    get all '/'

create session with weight 12 as 'test2':
    using view_name, view_value from 'views.csv' randomly
    var pin is a unique number from 1000 to 1005 # short range to
                                                 # make testing easy
    var username is a random string of length 10
    var pass_code is a random number from 1000 to 9999
    post '/user/create' with data 'username=$username&pass_code=$pass_code&pin=$pin'
create load:                
    spawn users every 4 seconds for 2 minutes up to 100 users
    spawn users every 10 seconds for 3 minutes
